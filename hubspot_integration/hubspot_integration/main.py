from typing import Any

import core.db as db
import core.models as models
from core.logging_config import setup_logging
from hubspot_integration import crud_provider, crud_shop, hubspot_operations

logger = setup_logging(__name__)

db.create_connection()


def update_hubspot_company_info(objs_: list[Any]) -> bool:
    for db_obj, hubspot_obj in objs_:
        try:
            logger.debug(
                "------------- HS >>> DB: `{0}` -------------".format(db_obj.table_name)
            )
            # update current missing Hubspot company info
            business_ids_without_hubspot_company_info = (
                db_obj.get_business_ids_without_hubspot_company_info()
            )
            hubspot_company_info = hubspot_obj.get_hubspot_company_info(
                business_ids=business_ids_without_hubspot_company_info
            )
            db_obj.update_hubspot_company_info(
                hubspot_company_info=hubspot_company_info
            )
        except Exception as e:
            logger.error(e)
            return False
    return True


def main(objs_: list[Any]) -> bool:
    for db_obj, hubspot_obj in objs_:
        try:
            logger.debug(
                "------------- HS >>> DB: `{0}` -------------".format(db_obj.table_name)
            )
            # integrate changes from HubSpot to DB that happened last minutes
            duplicated_business_ids = db_obj.get_duplicated_business_ids()
            objs_changed_last_minutes_in_hubspot = (
                hubspot_obj.get_objs_changed_last_minutes()
            )
            db_obj.integrate_from_hubspot_to_db(
                objs_changed_last_minutes_in_hubspot=objs_changed_last_minutes_in_hubspot,
                duplicated_business_ids=duplicated_business_ids,
            )
        except Exception as e:
            logger.error(e)
            return False
    return True


if __name__ == "__main__":
    objs = [
        (
            crud_provider.CRUDProvider(models.Provider, table_name="providers"),
            hubspot_operations.HubSpotProvider(),
        ),
        (
            crud_shop.CRUDShop(models.Shop, table_name="shops"),
            hubspot_operations.HubSpotShop(),
        ),
    ]
    update_hubspot_company_info(objs_=objs)
    main(objs_=objs)
