from typing import Any, Generic, Optional, Type, TypeVar

from cassandra.cqlengine.models import Model
from cassandra.cqlengine.query import BatchQuery

from . import helper, logging_config, models

logger = logging_config.setup_logging(__name__)

ModelT = TypeVar("ModelT", bound=Model)


def start_batch() -> BatchQuery:
    return BatchQuery()


def end_batch(batch: BatchQuery) -> None:
    batch.execute()


class CRUDBase(Generic[ModelT]):
    def __init__(self, model: Type[ModelT], table_name: str):
        self.model = model
        self.table_name = table_name

    def get_all(self) -> Optional[list[Type[ModelT]]]:
        return list(self.model.objects().all()) or None

    def get_all_business_ids(self) -> Optional[list[str]]:
        objs = self.get_all()
        if not objs:
            return None
        business_ids = [obj.businessId for obj in objs]
        return business_ids or None

    def get_business_ids_without_hubspot_company_info(self) -> Optional[set[str]]:
        objs = self.get_all()
        if not objs:
            return None
        business_ids_without_hubspot_ids = {
            obj.businessId for obj in objs if not obj.hubspotId
        }
        return business_ids_without_hubspot_ids or None

    def get_duplicated_business_ids(self) -> Optional[set[str]]:
        business_ids = self.get_all_business_ids()
        if not business_ids:
            return None
        duplicated_business_ids = {
            business_id
            for business_id in business_ids
            if business_ids.count(business_id) > 1
        }
        return duplicated_business_ids or None

    def get_many_by_business_id(self, business_id: str) -> Optional[list[Type[ModelT]]]:
        return list(self.model.objects(businessId=business_id).allow_filtering()) or None

    def get_many_by_hubspot_id(self, hubspot_id: str) -> Optional[list[Type[ModelT]]]:
        return list(self.model.objects(hubspotId=hubspot_id).allow_filtering()) or None

    def get_many_by_netvisor_id(self, netvisor_id: str) -> Optional[list[Type[ModelT]]]:
        return list(self.model.objects(netvisorId=netvisor_id).allow_filtering()) or None

    def update_hubspot_company_info(
        self, hubspot_company_info: Optional[list[dict[str, Any]]]
    ) -> None:
        if hubspot_company_info:
            db_batch = start_batch()
            for company_info in hubspot_company_info:
                for business_id in company_info:
                    objs = self.get_many_by_business_id(business_id=business_id)
                    if objs:
                        hubspot_id = company_info[business_id].get("hs_object_id", None)
                        employee_count = company_info[business_id].get(
                            "employee_count", None
                        )
                        for obj in objs:
                            if hubspot_id and obj.hubspotId != hubspot_id:
                                obj.hubspotId = hubspot_id
                                obj.batch(db_batch).save()
                            if employee_count and obj.employeeCount != employee_count:
                                obj.employeeCount = employee_count
                                obj.batch(db_batch).save()
            end_batch(db_batch)

    @staticmethod
    def log(
        batch: BatchQuery,
        id: str,
        logged_at: float,
        day: int,
        month: int,
        year: int,
        description: str,
        method: str,
        db_to_hs: bool,
        hs_to_db: bool,
        hubspot_id: str,
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
            dbToHs=db_to_hs,
            hsToDb=hs_to_db,
            hubspotId=hubspot_id,
            target=target,
            targetId=target_id,
        )

    # skip `name`
    def reformat_hubspot_obj(self, hubspot_obj: dict[str, Any]) -> dict[str, Any]:
        pass

    @staticmethod
    def get_different_values_between_db_and_hubspot_objs(
        db_obj: dict[str, Any],
        hubspot_obj: dict[str, Any],
        hubspot_to_db_integration: bool = True,
    ) -> Optional[dict[str, Any]]:
        if hubspot_to_db_integration:
            return {
                field: hubspot_obj[field]
                for field in hubspot_obj
                if hubspot_obj[field] and hubspot_obj[field] not in db_obj.values()
            } or None
        return None

    def update_for_hubspot_to_db_integration(
        self,
        db_batch: BatchQuery,
        obj: Type[ModelT],
        different_values: dict[str, Any],
        log_batch: Optional[BatchQuery],
    ) -> bool:
        pass

    def create_for_hubspot_to_db_integration(
        self,
        db_batch: BatchQuery,
        hubspot_obj: dict[str, Any],
        log_batch: Optional[BatchQuery],
    ) -> bool:
        pass

    def integrate_from_hubspot_to_db(
        self,
        objs_changed_last_minutes_in_hubspot: Optional[list[dict[str, Any]]],
        duplicated_business_ids: Optional[set[str]],
    ) -> Optional[bool]:
        db_batch = start_batch()
        log_batch = start_batch()
        if objs_changed_last_minutes_in_hubspot:
            for hubspot_obj in objs_changed_last_minutes_in_hubspot:
                business_id = hubspot_obj.get("business_id", None)
                hubspot_id = hubspot_obj.get("hs_object_id", None)

                # if business_id is found in the list of duplicated business_id
                # do nothing
                if duplicated_business_ids and business_id in duplicated_business_ids:
                    logger.warning(
                        "Warning: There are more than 1 company with the same `businessId`: {0} in `table`: {1} in DB".format(
                            business_id, self.table_name
                        )
                    )
                    logger.debug("Skip integration for this businessId")
                    continue

                # search for companies in DB with hubspotId or businessId
                db_objs = self.get_many_by_hubspot_id(
                    hubspot_id=hubspot_id
                ) or self.get_many_by_business_id(business_id=business_id)
                if db_objs:
                    for db_obj in db_objs:
                        db_obj_last_modified = db_obj.updatedAt or None
                        hubspot_obj_last_modified_date = helper.format_date_time(
                            hubspot_obj.get("hs_lastmodifieddate", None)[:-1]
                        )

                        # if does not exist yet or `updatedAt` is lte than `hs_lastmodifeddate`
                        # update these changes in DB
                        if (
                            not db_obj_last_modified
                            or db_obj_last_modified <= hubspot_obj_last_modified_date
                        ):
                            reformatted_db_obj = (
                                db_obj.reformat_db_obj_into_hubspot_format()
                            )
                            reformatted_hubspot_obj = self.reformat_hubspot_obj(
                                hubspot_obj=hubspot_obj
                            )
                            different_values_in_hubspot_vs_db = (
                                self.get_different_values_between_db_and_hubspot_objs(
                                    db_obj=reformatted_db_obj,
                                    hubspot_obj=reformatted_hubspot_obj,
                                )
                            )
                            if different_values_in_hubspot_vs_db:
                                self.update_for_hubspot_to_db_integration(
                                    db_batch=db_batch,
                                    log_batch=log_batch,
                                    obj=db_obj,
                                    different_values=different_values_in_hubspot_vs_db,
                                )
                                logger.debug(
                                    "UPDATE 1 company with `businessId` {0} in table `{1}`".format(
                                        business_id, self.table_name
                                    )
                                )
                            else:
                                logger.debug(
                                    "No integration for this `businessId` {0}. "
                                    "No value different from HubSpot".format(
                                        business_id
                                    )
                                )
                        else:
                            if (
                                db_obj_last_modified
                                and db_obj_last_modified
                                > hubspot_obj_last_modified_date
                            ):
                                logger.debug(
                                    "No integration for this `businessId` {0}. "
                                    "`updatedAt` is later than `hsLastModifiedDate`: "
                                    "{1} > {2}".format(
                                        business_id,
                                        db_obj_last_modified,
                                        hubspot_obj_last_modified_date,
                                    )
                                )

                # no company exists at all
                else:

                    self.create_for_hubspot_to_db_integration(
                        db_batch=db_batch, log_batch=log_batch, hubspot_obj=hubspot_obj
                    )
                    logger.debug(
                        "CREATE 1 company with `hubspotId` {0} `businessId` {1} in table `{2}`".format(
                            hubspot_id, business_id, self.table_name
                        )
                    )
            end_batch(db_batch)
            end_batch(log_batch)
            return True
        else:
            logger.debug(
                "No `{0}` changed in the last minutes in HubSpot. No integration made.".format(
                    self.table_name
                )
            )
        return None

    def get_all_objs_without_webflow_ids(self) -> Optional[list[Type[ModelT]]]:
        objs = self.get_all()
        if objs:
            return [obj for obj in objs if not obj.webflowId] or None
        return None

    def get_objs_changed_last_minutes(self):
        return (
            list(
                self.model.filter(
                    self.model.updatedAt >= helper.get_last_minutes_date_time()
                ).allow_filtering()
            )
            or None
        )

    def update_webflow_ids(
        self,
        webflow_objs: Optional[list],
        duplicated_business_ids_webflow: Optional[set[str]],
    ) -> None:
        db_batch = start_batch()
        log_batch = start_batch()
        objs = self.get_all_objs_without_webflow_ids()
        duplicated_business_ids = self.get_duplicated_business_ids()
        if objs and webflow_objs:
            for obj in objs:
                business_id = obj.businessId
                if business_id:
                    # skip processing duplicated objs in DB and WF
                    if (
                        duplicated_business_ids_webflow
                        and business_id in duplicated_business_ids_webflow
                    ):
                        logger.warning(
                            "Warning: There are more than 1 partner with the same `businessId`: {0} in Webflow".format(
                                business_id,
                            )
                        )
                        logger.debug("Skip integration for this `businessId`")
                        continue
                    if (
                        duplicated_business_ids
                        and business_id in duplicated_business_ids
                    ):
                        logger.warning(
                            "Warning: There are more than 1 partner with the same `businessId`: {0} in DB".format(
                                business_id,
                            )
                        )
                        logger.debug("Skip integration for this `businessId`")
                        continue

                    for webflow_obj in webflow_objs:
                        webflow_business_id = (
                            webflow_obj.get("business-id", None) or None
                        )
                        if webflow_business_id and webflow_business_id.strip(
                            " "
                        ) == business_id.strip(" "):
                            webflow_id = webflow_obj["_id"]
                            if obj.webflowId != webflow_id:
                                obj.webflowId = webflow_id
                                obj.batch(db_batch).save()
        end_batch(db_batch)
        end_batch(log_batch)

    def get_all_objs_without_netvisor_ids(self) -> Optional[list[Type[ModelT]]]:
        objs = self.get_all()
        if objs:
            return [obj for obj in objs if not obj.netvisorId] or None
        return None

    def update_netvisor_ids(
            self,
            netvisor_objs: Optional[list],
            duplicated_business_ids_netvisor: Optional[set[str]],
    ) -> None:
        db_batch = start_batch()
        log_batch = start_batch()
        objs = self.get_all_objs_without_netvisor_ids()
        duplicated_business_ids = self.get_duplicated_business_ids()
        if objs and netvisor_objs:
            for obj in objs:
                business_id = obj.businessId
                if business_id:
                    # skip processing duplicated objs in DB and WF
                    if (
                            duplicated_business_ids_netvisor
                            and business_id in duplicated_business_ids_netvisor
                    ):
                        logger.warning(
                            "Warning: There are more than 1 partner with the same `businessId`: {0} in Netvisor".format(
                                business_id,
                            )
                        )
                        logger.debug("Skip integration for this `businessId`")
                        continue
                    if (
                            duplicated_business_ids
                            and business_id in duplicated_business_ids
                    ):
                        logger.warning(
                            "Warning: There are more than 1 partner with the same `businessId`: {0} in DB".format(
                                business_id,
                            )
                        )
                        logger.debug("Skip integration for this `businessId`")
                        continue

                    for netvisor_obj in netvisor_objs:
                        netvisor_business_id = (
                                netvisor_obj.get("OrganisationIdentifier", None) or None
                        )
                        if netvisor_business_id and netvisor_business_id.strip(
                                " "
                        ) == business_id.strip(" "):
                            netvisor_id = netvisor_obj["Netvisorkey"]
                            if obj.netvisorId != netvisor_id:
                                obj.netvisorId = netvisor_id
                                obj.batch(db_batch).save()
        end_batch(db_batch)
        end_batch(log_batch)
