import uuid
from typing import Any, Optional, Tuple

from cassandra.cqlengine.query import BatchQuery
from webflowpy.Webflow import Webflow

import core.crud_base as crud
import core.helper as helper
import core.models as models
from core.logging_config import setup_logging
from webflow_integration import webflow_models
from webflow_integration import webflow_settings as settings

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
    db_to_wf: bool,
    webflow_id: str,
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
        dbToWf=db_to_wf,
        webflowId=webflow_id,
        target=target,
        targetId=target_id,
    )


class WebflowCollectionBase:
    def __init__(self):
        self.client = Webflow(token=settings.settings.ACCESS_TOKEN.get_secret_value())
        self.site_id = settings.settings.SITE_ID
        self.collection_partner_id = settings.settings.COLLECTION_PARTNER_ID
        self.collection_partner_cities_id = (
            settings.settings.COLLECTION_PARTNER_CITIES_ID
        )

    def get_all_partners(self) -> Optional[list[dict[str, Any]]]:
        return (
            self.client.items(collection_id=self.collection_partner_id, all=True).get(
                "items", None
            )
            or None
        )

    def get_duplicated_business_ids(self) -> Optional[set[str]]:
        partners = self.get_all_partners()
        if partners:
            ids = [
                partner.get("business-id", None)
                for partner in partners
                if partner.get("business-id", None)
            ]
            return set([id for id in ids if ids.count(id) > 1]) or None
        return None

    def get_all_partner_cities(self) -> Optional[list[dict[str, Any]]]:
        return (
            self.client.items(
                collection_id=self.collection_partner_cities_id, all=True
            ).get("items", None)
            or None
        )

    def get_a_partner(self, item_id: str) -> Optional[dict[str, Any]]:
        partners = self.get_all_partners()
        if partners:
            partner = [
                partner for partner in partners if partner.get("_id", None) == item_id
            ]
            return partner[0] if partner else None
        return None

    def create_a_partner(
        self, item_data: dict[str, Any], live: Optional[bool] = False
    ) -> Optional[dict[str, Any]]:
        response = self.client.createItem(
            collection_id=self.collection_partner_id, item_data=item_data, live=live
        )
        if "err" not in response and "_id" in response:
            return response
        return None

    def create_a_partner_city(
        self, item_data: dict[str, Any], live: Optional[bool] = False
    ) -> Optional[dict[str, Any]]:
        response = self.client.createItem(
            collection_id=self.collection_partner_cities_id,
            item_data=item_data,
            live=live,
        )
        if "err" not in response and "_id" in response:
            return response
        return None

    def update_a_partner(
        self, item_id: str, item_data: dict[str, Any], live: Optional[bool] = False
    ) -> Optional[dict[str, Any]]:
        response = self.client.patchItem(
            collection_id=self.collection_partner_id,
            item_id=item_id,
            item_data=item_data,
            live=live,
        )
        if "err" not in response and "_id" in response:
            return response
        return None

    @staticmethod
    def reformat_db_obj_into_webflow_format(db_obj: crud.ModelT) -> dict[str, Any]:
        return webflow_models.WebflowPartnerUpdate(
            **{
                "business-id": db_obj.businessId,
                "locations": db_obj.city,
                "name": db_obj.name,
                "slug": helper.get_slug(db_obj.name),
                "website": db_obj.www,
            }
        ).dict(by_alias=True)

    @staticmethod
    def reformat_webflow_obj(obj: dict[str, Any]) -> dict[str, Any]:
        return webflow_models.WebflowPartnerCreate(**obj).dict(by_alias=True)

    def get_different_values_between_db_and_webflow_objs(
        self,
        db_obj: Optional[dict[str, Any]],
        webflow_obj: Optional[dict[str, Any]],
    ) -> Optional[dict[str, Any]]:
        if db_obj and webflow_obj:
            output = dict()
            for field in db_obj:
                if db_obj[field] and db_obj[field] not in webflow_obj.values():
                    if field == "location-s-2":
                        continue
                    if field == "locations":
                        if db_obj[field] in webflow_obj[field]:
                            continue
                        else:
                            updated_locations = (
                                webflow_obj[field] + ", " + db_obj[field]
                            )
                            output["locations"] = updated_locations
                            output["location-s-2"] = self.get_partner_city_id(
                                locations=updated_locations.split(", ")
                            )
                            continue
                    output[field] = db_obj[field]
            return output
        return None

    def get_partner_city_id(
        self, locations: Optional[list[str]], live: Optional[bool] = False
    ) -> Optional[list[str]]:
        if locations:
            partner_cities = self.get_all_partner_cities()
            output = list()
            for location in locations:
                if not location:
                    continue
                search_result = (
                    [
                        obj["_id"]
                        for obj in partner_cities
                        if obj.get("name", None) == location
                    ]
                    if partner_cities
                    else None
                )
                if not search_result:
                    new_location_obj = self.create_a_partner_city(
                        item_data=webflow_models.WebflowPartnerCityCreate(
                            **{
                                "name": location,
                                "slug": helper.get_slug(string=location),
                            }
                        ).dict(by_alias=True),
                        live=live,
                    )
                    if new_location_obj:
                        output.append(new_location_obj["_id"])
                else:
                    output.append(search_result[0])
            return output or None
        return None

    def update_for_webflow_to_db_integration(
        self,
        db_obj_info: Tuple[str, str, str],
        different_values: dict[str, Any],
        log_batch: Optional[BatchQuery] = None,
        live: Optional[bool] = False,
    ) -> bool:
        try:
            id, business_id, webflow_id = db_obj_info
            updated_webflow_obj = self.update_a_partner(
                item_id=webflow_id,
                item_data=webflow_models.WebflowPartnerUpdate(**different_values).dict(
                    exclude_none=True, by_alias=True
                ),
                live=live,
            )

            if updated_webflow_obj:
                # update log
                if log_batch:
                    day, month, year = helper.get_datetime_for_log(
                        updated_webflow_obj.get("updated-on", None)[:-1]
                    )
                    log(
                        batch=log_batch,
                        id=str(uuid.uuid4()),
                        logged_at=helper.format_date_time(
                            string=updated_webflow_obj.get("updated-on", None)[:-1]
                        ),
                        day=day,
                        month=month,
                        year=year,
                        description="Update an existing `partner` in WF from DB with new values: {0}".format(
                            different_values
                        ),
                        method="PATCH",
                        db_to_wf=True,
                        webflow_id=webflow_id,
                        target="shops",
                        target_id=id,
                    )

                logger.debug(
                    "UPDATE 1 partner with `businessId` {0} `webflowId` {1}".format(
                        business_id, webflow_id
                    )
                )
                return True
            else:
                logger.error(
                    "ERROR: UPDATE 1 partner with `businessId` {0} `webflowId` {1}".format(
                        business_id, webflow_id
                    )
                )
                return False
        except Exception as e:
            logger.error(e)
            return False

    def create_for_webflow_to_db_integration(
        self,
        db_obj: crud.ModelT,
        db_batch: Optional[BatchQuery] = None,
        log_batch: Optional[BatchQuery] = None,
        live: Optional[bool] = False,
    ) -> bool:
        try:
            # reformat a db obj for creating a new partner in Webflow
            reformatted_db_obj = self.reformat_db_obj_into_webflow_format(db_obj)
            reformatted_db_obj["location-s-2"] = self.get_partner_city_id(
                locations=[reformatted_db_obj.get("locations", None)]
            )

            # create a new partner in Webflow
            created_webflow_obj = self.create_a_partner(
                item_data=webflow_models.WebflowPartnerCreate(
                    **reformatted_db_obj
                ).dict(by_alias=True),
                live=live,
            )

            if created_webflow_obj:
                if db_batch:
                    # update the db obj with `webflowId` and `updatedAt`
                    db_obj.webflowId = created_webflow_obj.get("_id", None)
                    db_obj.updatedAt = helper.get_timestamp_now()
                    db_obj.batch(db_batch).save()

                # update log
                if log_batch:
                    day, month, year = helper.get_datetime_for_log(
                        created_webflow_obj.get("updated-on", None)[:-1]
                    )
                    log(
                        batch=log_batch,
                        id=str(uuid.uuid4()),
                        logged_at=helper.format_date_time(
                            string=created_webflow_obj.get("updated-on", None)[:-1]
                        ),
                        day=day,
                        month=month,
                        year=year,
                        description="Create a new `provider` in WF from DB",
                        method="CREATE",
                        db_to_wf=True,
                        webflow_id=created_webflow_obj.get("_id", None),
                        target="shops",
                        target_id=db_obj.id,
                    )

                logger.debug(
                    "CREATE 1 partner with `businessId` {0} `webflowId` {1}".format(
                        db_obj.businessId, created_webflow_obj.get("_id", None)
                    )
                )
                return True
            else:
                logger.error(
                    "ERROR: CREATE 1 partner with `businessId` {0}".format(
                        db_obj.businessId
                    )
                )
                return False
        except Exception as e:
            logger.error(e)
            return False

    def archive_for_webflow_to_db_integration(
        self,
        db_obj_info: Tuple[str, str, str],
        log_batch: Optional[BatchQuery] = None,
        live: Optional[bool] = False,
    ) -> bool:
        try:
            id, business_id, webflow_id = db_obj_info
            updated_webflow_obj = self.update_a_partner(
                item_id=webflow_id,
                item_data={"_archived": True},
                live=live,
            )

            if updated_webflow_obj:
                # update log
                if log_batch:
                    day, month, year = helper.get_datetime_for_log(
                        updated_webflow_obj.get("updated-on", None)[:-1]
                    )
                    log(
                        batch=log_batch,
                        id=str(uuid.uuid4()),
                        logged_at=helper.format_date_time(
                            string=updated_webflow_obj.get("updated-on", None)[:-1]
                        ),
                        day=day,
                        month=month,
                        year=year,
                        description="Archive an existing `partner` in WF from DB",
                        method="PATCH",
                        db_to_wf=True,
                        webflow_id=webflow_id,
                        target="shops",
                        target_id=id,
                    )

                logger.debug(
                    "ARCHIVE 1 partner with `businessId` {0} `webflowId` {1}".format(
                        business_id, webflow_id
                    )
                )
                return True
            else:
                logger.error(
                    "ERROR: ARCHIVE 1 partner with `businessId` {0} `webflowId` {1}".format(
                        business_id, webflow_id
                    )
                )
                return False
        except Exception as e:
            logger.error(e)
            return False

    def integrate_from_db_to_webflow(
        self,
        db_objs: list[crud.ModelT],
        duplicated_business_ids_db: Optional[set[str]],
        live: Optional[bool] = False,
    ) -> None:
        if db_objs:
            db_batch = crud.start_batch()
            log_batch = crud.start_batch()
            duplicated_business_ids_webflow = self.get_duplicated_business_ids()
            for db_obj in db_objs:
                db_obj_business_id = db_obj.businessId

                # skip processing duplicated objs in DB and WF
                if (
                    duplicated_business_ids_webflow
                    and db_obj_business_id in duplicated_business_ids_webflow
                ):
                    logger.warning(
                        "Warning: There are more than 1 partner with the same `businessId`: {0} in Webflow".format(
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

                db_obj_webflow_id = db_obj.webflowId or None
                if db_obj_webflow_id:
                    obj = self.get_a_partner(item_id=db_obj_webflow_id)
                    if obj:
                        db_obj_last_modified = db_obj.updatedAt or None
                        obj_last_modified_date = helper.format_date_time(
                            obj.get("updated-on", None)[:-1]
                        )
                        # if does not exist yet or `updatedAt` is gte `updated-on`
                        # update these changes in WF
                        if (
                            not db_obj_last_modified
                            or db_obj_last_modified >= obj_last_modified_date
                        ):
                            # if a db obj is set as inactive, archive it in Webflow
                            if db_obj.isActive is False:
                                self.archive_for_webflow_to_db_integration(
                                    db_obj_info=(
                                        str(db_obj.id),
                                        str(db_obj_business_id),
                                        str(db_obj_webflow_id),
                                    ),
                                    log_batch=log_batch,
                                    live=live,
                                )
                                continue

                            # reformat a db obj for updating an existing partner in Webflow
                            reformatted_db_obj = (
                                self.reformat_db_obj_into_webflow_format(db_obj)
                            )
                            reformatted_webflow_obj = self.reformat_webflow_obj(obj=obj)
                            different_values_in_db_vs_webflow = (
                                self.get_different_values_between_db_and_webflow_objs(
                                    db_obj=reformatted_db_obj,
                                    webflow_obj=reformatted_webflow_obj,
                                )
                            )
                            # update an existing partner in Webflow
                            if different_values_in_db_vs_webflow:
                                self.update_for_webflow_to_db_integration(
                                    db_obj_info=(
                                        str(db_obj.id),
                                        str(db_obj_business_id),
                                        str(db_obj_webflow_id),
                                    ),
                                    log_batch=log_batch,
                                    different_values=different_values_in_db_vs_webflow,
                                    live=live,
                                )
                        else:
                            if (
                                db_obj_last_modified
                                and db_obj_last_modified < obj_last_modified_date
                            ):
                                logger.debug(
                                    "No integration for this `businessId` {0}. "
                                    "`updatedAt` is earlier than Webflow `updated-on`: "
                                    "{1} < {2}".format(
                                        db_obj_business_id,
                                        db_obj_last_modified,
                                        obj_last_modified_date,
                                    )
                                )
                    else:
                        logger.warning(
                            "Warning: Wrong `webflowId` set for this `businessId`: {0}. "
                            "Proceed with resetting this `webflowId`.".format(
                                db_obj_business_id
                            )
                        )
                        db_obj.webflowId = None
                        db_obj.batch(db_batch).save()
                else:
                    # if a db obj is set as inactive, pass creating it
                    if db_obj.isActive is False:
                        logger.debug(
                            "No integration for this `businessId` {0}. "
                            "`isActive` is False.".format(
                                db_obj_business_id,
                            )
                        )
                        continue
                    else:
                        self.create_for_webflow_to_db_integration(
                            db_batch=db_batch,
                            db_obj=db_obj,
                            log_batch=log_batch,
                            live=live,
                        )
            crud.end_batch(batch=db_batch)
            crud.end_batch(batch=log_batch)
        else:
            logger.debug(
                "No `shops` changed in the last minutes in DB. No integration made.".format()
            )


class WebflowCollectionShop(WebflowCollectionBase):
    pass
