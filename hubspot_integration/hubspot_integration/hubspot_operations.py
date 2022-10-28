from time import sleep
from typing import Any, Optional

from hubspot import Client as HubSpotClient
from hubspot.crm.companies import ApiException, PublicObjectSearchRequest
from hubspot.crm.companies.models.simple_public_object import SimplePublicObject

import core.helper as helper
from core.logging_config import setup_logging
from hubspot_integration import hubspot_config, settings

logger = setup_logging(__name__)


class HubSpotBase:
    def __init__(self):
        self.client = HubSpotClient.create(
            access_token=settings.settings.ACCESS_TOKEN.get_secret_value()
        )

    @staticmethod
    def create_filter_groups_for_obj_search(business_id: str) -> list[dict[str, Any]]:
        pass

    @staticmethod
    def create_filter_groups_for_last_minutes_obj_search(
        date_time: int,
    ) -> list[dict[str, Any]]:
        pass

    @staticmethod
    def get_search_properties() -> list[str]:
        pass

    def create_obj_search_request(
        self, business_id: str, limit: Optional[int], after: Optional[int]
    ) -> PublicObjectSearchRequest:
        return PublicObjectSearchRequest(
            filter_groups=self.create_filter_groups_for_obj_search(
                business_id=business_id
            ),
            properties=self.get_search_properties(),
            sorts=[{"propertyName": "hs_lastmodifieddate", "direction": "DESCENDING"}],
            limit=limit,
            after=after,
        )

    def create_last_minutes_obj_search_request(
        self, date_time: int, limit: Optional[int], after: Optional[int]
    ) -> PublicObjectSearchRequest:
        return PublicObjectSearchRequest(
            filter_groups=self.create_filter_groups_for_last_minutes_obj_search(
                date_time=date_time
            ),
            properties=self.get_search_properties(),
            sorts=[{"propertyName": "hs_lastmodifieddate", "direction": "DESCENDING"}],
            limit=limit,
            after=after,
        )

    def get_hubspot_company_info(
        self, business_ids: Optional[set[str]]
    ) -> Optional[list[dict[str, Any]]]:
        if business_ids:
            output = list()
            for business_id in business_ids:
                obj_search_request = self.create_obj_search_request(
                    business_id=business_id, limit=None, after=None
                )
                try:
                    obj_search_result = self.client.crm.companies.search_api.do_search(
                        public_object_search_request=obj_search_request
                    ).results
                    sleep(0.1)
                    if obj_search_result:
                        if len(obj_search_result) > 1:
                            logger.warning(
                                "Warning: There are more than 1 company with the same `business_id`: {0} in HubSpot".format(
                                    business_id
                                )
                            )
                            continue
                        if len(obj_search_result) == 1:
                            output.append(
                                {
                                    business_id: {
                                        "hs_object_id": obj_search_result[
                                            0
                                        ].properties.get("hs_object_id", None)
                                        or None,
                                        "employee_count": obj_search_result[
                                            0
                                        ].properties.get("employee_count", None)
                                        or None,
                                    }
                                }
                            )
                except ApiException as e:
                    logger.error(
                        "Exception when calling search_api->do_search: %s\n" % e
                    )
                    continue
            return output or None
        return None

    @staticmethod
    def get_table_name() -> str:
        pass

    def get_objs_changed_last_minutes(self) -> Optional[list[dict[str, Any]]]:
        last_minutes_date_time = helper.get_last_minutes_date_time() * 1000

        def next_page(
            hubspot_client: HubSpotClient,
            after: Optional[int],
            results: list[SimplePublicObject],
        ) -> Optional[list[SimplePublicObject]]:
            obj_search_request = self.create_last_minutes_obj_search_request(
                date_time=last_minutes_date_time, limit=100, after=after
            )
            obj_search_response = hubspot_client.crm.companies.search_api.do_search(
                public_object_search_request=obj_search_request
            )
            results += obj_search_response.results
            try:
                after = obj_search_response.paging.next.after
                sleep(0.1)
                return next_page(hubspot_client, after=after, results=results)
            except Exception:
                logger.debug(
                    "Finished getting all {0} changed during last minutes in HubSpot".format(
                        self.get_table_name()
                    )
                )
            return [
                obj for obj in results if obj.properties.get("business_id", None)
            ] or None

        objs_changed_last_minutes = next_page(
            hubspot_client=self.client, results=list(), after=None
        )

        if objs_changed_last_minutes:
            for obj in objs_changed_last_minutes:
                employee_count = obj.properties.get("employee_count", None) or None
                if employee_count:
                    obj.properties["employee_count"] = int(employee_count)
                obj.properties["business_id"] = helper.clean_business_id_with_spaces(
                    obj.properties["business_id"]
                )

            logger.debug(
                "{0} `{1}` changed during last minutes in HubSpot".format(
                    len(objs_changed_last_minutes), self.get_table_name()
                )
            )
            return [obj.properties for obj in objs_changed_last_minutes] or None
        else:
            logger.debug(
                "No `{0}` changed during last minutes in HubSpot".format(
                    self.get_table_name()
                )
            )
            return None


class HubSpotProvider(HubSpotBase):
    @staticmethod
    def create_filter_groups_for_obj_search(business_id: str) -> list[dict[str, Any]]:
        return [
            {
                "filters": [
                    {
                        "propertyName": "business_id",
                        "operator": "EQ",
                        "value": str(business_id).strip(" "),
                    },
                    {
                        "propertyName": "customer_type_vapaus",
                        "operator": "IN",
                        "values": ["Benefit Bike Customer", "Shared Fleet Customer"],
                    },
                ]
            }
        ]

    @staticmethod
    def create_filter_groups_for_last_minutes_obj_search(
        date_time: int,
    ) -> list[dict[str, Any]]:
        return [
            {
                "filters": [
                    {
                        "propertyName": "customer_type_vapaus",
                        "operator": "IN",
                        "values": ["Benefit Bike Customer", "Shared Fleet Customer"],
                    },
                    {
                        "propertyName": "hs_lastmodifieddate",
                        "operator": "GTE",
                        "value": date_time,
                    },
                ]
            }
        ]

    @staticmethod
    def get_search_properties() -> list[str]:
        return hubspot_config.provider_search_properties

    @staticmethod
    def get_table_name() -> str:
        return "providers"


class HubSpotShop(HubSpotBase):
    @staticmethod
    def create_filter_groups_for_obj_search(business_id: str) -> list[dict[str, Any]]:
        return [
            {
                "filters": [
                    {
                        "propertyName": "business_id",
                        "operator": "EQ",
                        "value": str(business_id).strip(" "),
                    },
                    {
                        "propertyName": "customer_type_vapaus",
                        "operator": "EQ",
                        "value": "Bike Shop Partner",
                    },
                ]
            }
        ]

    @staticmethod
    def create_filter_groups_for_last_minutes_obj_search(
        date_time: int,
    ) -> list[dict[str, Any]]:
        return [
            {
                "filters": [
                    {
                        "propertyName": "hs_lastmodifieddate",
                        "operator": "GTE",
                        "value": date_time,
                    },
                    {
                        "propertyName": "customer_type_vapaus",
                        "operator": "EQ",
                        "value": "Bike Shop Partner",
                    },
                ]
            }
        ]

    @staticmethod
    def get_search_properties() -> list[str]:
        return hubspot_config.shop_search_properties

    @staticmethod
    def get_table_name() -> str:
        return "shops"
