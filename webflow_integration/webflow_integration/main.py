import argparse
from typing import Any, Optional

import crud_shop as crud

import core.db as db
import core.models as models
from core.logging_config import setup_logging
from webflow_integration import webflow_operations

logger = setup_logging(__name__)

db.create_connection()


def update_webflow_company_info(objs_: list[Any]) -> bool:
    for db_obj, webflow_obj in objs_:
        try:
            logger.debug(
                "------------- WF >>> DB: `{0}` -------------".format(db_obj.table_name)
            )
            # update current missing Webflow company info
            webflow_objs = webflow_obj.get_all_partners()
            duplicated_business_ids_webflow = webflow_obj.get_duplicated_business_ids()
            db_obj.update_webflow_ids(
                webflow_objs=webflow_objs,
                duplicated_business_ids_webflow=duplicated_business_ids_webflow,
            )
        except Exception as e:
            logger.error(e)
            return False
    return True


def main(objs_: list[Any], live: Optional[bool] = False) -> bool:
    for db_obj, webflow_obj in objs_:
        try:
            logger.debug(
                "------------- DB >>> WF: `{0}` -------------".format(db_obj.table_name)
            )
            objs_changed_last_minutes = db_obj.get_objs_changed_last_minutes()
            duplicated_business_ids_db = db_obj.get_duplicated_business_ids()
            webflow_obj.integrate_from_db_to_webflow(
                db_objs=objs_changed_last_minutes,
                duplicated_business_ids_db=duplicated_business_ids_db,
                live=live,
            )
        except Exception as e:
            logger.error(e)
            return False
    return True


if __name__ == "__main__":
    # add first run arg
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--live", type=int, help="input 1 for live, default is 0", nargs="?", default=0
    )
    live = bool(parser.parse_args().live)
    objs = [
        (
            crud.CRUDShop(models.Shop, table_name="shops"),
            webflow_operations.WebflowCollectionShop(),
        ),
    ]
    update_webflow_company_info(objs_=objs)
    main(objs_=objs, live=live)
