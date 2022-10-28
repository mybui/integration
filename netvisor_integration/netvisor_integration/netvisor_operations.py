import uuid
from typing import Optional, Any, Tuple

import requests
import xmltodict
from cassandra.cqlengine.query import BatchQuery
from dict2xml import dict2xml

import core.crud_base as crud
import core.helper as helper
import core.models as models
from core.logging_config import setup_logging
from netvisor_integration import netvisor_config
from netvisor_integration import netvisor_models

logger = setup_logging(__name__)


def log(
        batch: BatchQuery,
        id: str,
        logged_at: float,
        day: Optional[int],
        month: Optional[int],
        year: Optional[int],
        description: str,
        method: str,
        db_to_nv: bool,
        netvisor_id: str,
        target: str,
        target_id: str,
) -> None:
    models.LogIntegration.batch(batch).create(
        id=id,
        loggedAt=logged_at,
        day=day,
        month=month,
        year=year,
        description=description,
        method=method,
        dbToNv=db_to_nv,
        netvisorId=netvisor_id,
        target=target,
        targetId=target_id,
    )


class Netvisor:
    @staticmethod
    def get_headers(url: str) -> dict[str, Any]:
        customer_list_timestamp, customer_list_transaction_id, customer_list_h_mac = netvisor_config.h_mac(
            url=url
        )
        headers = netvisor_models.NetvisorHeadersBase().dict(
            exclude_none=True, by_alias=True
        )
        headers.update(
            netvisor_models.NetvisorCustomerListHeaders(**{
                "X-Netvisor-Authentication-Timestamp": customer_list_timestamp,
                "X-Netvisor-Authentication-TransactionId": customer_list_transaction_id,
                "X-Netvisor-Authentication-MAC": customer_list_h_mac
            }).dict(
                by_alias=True
            )
        )
        return headers

    def get_all_customers(self) -> Optional[list]:
        try:
            customer_list = requests.get(
                url=netvisor_config.get_customer_list_url,
                headers=self.get_headers(url=netvisor_config.get_customer_list_url)
            )
            if customer_list.status_code == 200:
                return xmltodict.parse(customer_list.text)["Root"]["Customerlist"]["Customer"]
        except Exception as e:
            logger.error(e)
            return None

    def get_duplicated_business_ids(self) -> Optional[set[str]]:
        customers = self.get_all_customers()
        if customers:
            ids = [
                customer.get("OrganisationIdentifier", None)
                for customer in customers
                if customer.get("OrganisationIdentifier", None)
            ]
            return set([id for id in ids if ids.count(id) > 1]) or None
        return None

    def update_a_customer(
            self,
            customer_id: str,
            data: str
    ) -> bool:
        try:
            response = requests.post(
                url=netvisor_config.update_customer_url.format(customer_id),
                headers=self.get_headers(url=netvisor_config.update_customer_url.format(customer_id)),
                data=data
            )
            if response.status_code == 200:
                return True
            return False
        except Exception as e:
            logger.error(e)
            return False

    def create_a_customer(
            self,
            data: str
    ) -> Optional[int]:
        try:
            response = requests.post(
                url=netvisor_config.create_customer_url,
                headers=self.get_headers(url=netvisor_config.create_customer_url),
                data=data
            )
            if response.status_code == 200:
                return xmltodict.parse(response.text)["Root"]["Replies"]["InsertedDataIdentifier"]
            return None
        except Exception as e:
            logger.error(e)
            return None

    def update_for_netvisor_to_db_integration(
            self,
            # other parameters
    ) -> bool:
        try:

            # update a customer in Netvisor
            # update `netvisorId` in DB
            # and add to `logsintegration` table
            # see the Webflow integration program

            pass
            return True
        except Exception as e:
            logger.error(e)
            return False

    def create_for_netvisor_to_db_integration(
            self,
            # other parameters
    ) -> bool:
        try:

            # create a customer in Netvisor
            # update `netvisorId` in DB
            # and add to `logsintegration` table
            # see the Webflow integration program

            pass
            return True
        except Exception as e:
            logger.error(e)
            return False

    @staticmethod
    def reformat_db_obj_into_netvisor_format(db_obj: crud.ModelT) -> dict[str, Any]:
        return netvisor_models.NetvisorCustomerUpdate(
            **{

                # add the matching of Netvisor fields and DB fields here
                # see the Webflow integration program

            }
        ).dict(by_alias=True)

    @staticmethod
    def reformat_netvisor_obj(obj: dict[str, Any]) -> dict[str, Any]:
        return netvisor_models.NetvisorCustomerCreate(**obj).dict(by_alias=True)

    def get_different_values_between_db_and_netvisor_objs(
            self,
            db_obj: Optional[dict[str, Any]],
            netvisor_obj: Optional[dict[str, Any]],
    ) -> Optional[dict[str, Any]]:
        if db_obj and netvisor_obj:
            output = dict()
            for field in db_obj:

                # find the different values between DB and Netvisor objects
                # and output them for body of a post method (create customer) above

                output[field] = db_obj[field]
            return output
        return None

    def integrate_from_db_to_netvisor(
        self,
        db_objs: list[crud.ModelT],
        duplicated_business_ids_db: Optional[set[str]],
    ) -> None:
        if db_objs:
            db_batch = crud.start_batch()
            log_batch = crud.start_batch()
            duplicated_business_ids_netvisor = self.get_duplicated_business_ids()
            for db_obj in db_objs:
                db_obj_business_id = db_obj.businessId

                # skip processing duplicated objs in DB and Netvisor
                if (
                    duplicated_business_ids_netvisor
                    and db_obj_business_id in duplicated_business_ids_netvisor
                ):
                    logger.warning(
                        "Warning: There are more than 1 partner with the same `businessId`: {0} in Netvisor".format(
                            db_obj_business_id,
                        )
                    )
                    logger.debug("Skip integration for this `businessId`")
                    continue
                if (
                    duplicated_business_ids_db
                    and db_obj_business_id in duplicated_business_ids_db
                ):
                    logger.warning(
                        "Warning: There are more than 1 partner with the same `businessId`: {0} in DB".format(
                            db_obj_business_id,
                        )
                    )
                    logger.debug("Skip integration for this `businessId`")
                    continue

                # logic to either update a Netvisor object here

                # or create a Netvisor object here

            crud.end_batch(batch=db_batch)
            crud.end_batch(batch=log_batch)
        else:
            logger.debug(
                "No `providers` changed in the last minutes in DB. No integration made.".format()
            )
    