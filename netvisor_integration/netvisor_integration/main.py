from typing import Any

import core.db as db
import core.models as models
from core.logging_config import setup_logging
from netvisor_integration import crud_provider as crud
from netvisor_integration import netvisor_operations

logger = setup_logging(__name__)

db.create_connection()


def update_netvisor_company_info(objs_: list[Any]) -> bool:
    for db_obj, netvisor_obj in objs_:
        try:
            logger.debug(
                "------------- NV >>> DB: `{0}` -------------".format(db_obj.table_name)
            )
            # update current missing Netvisor company info
            netvisor_objs = netvisor_obj.get_all_customers()
            duplicated_business_ids_netvisor = netvisor_obj.get_duplicated_business_ids()
            db_obj.update_netvisor_ids(
                netvisor_objs=netvisor_objs,
                duplicated_business_ids_netvisor=duplicated_business_ids_netvisor,
            )
        except Exception as e:
            logger.error(e)
            return False
    return True


if __name__ == "__main__":
    objs = [
        (
            crud.CRUDProvider(models.Provider, table_name="providers"),
            netvisor_operations.Netvisor(),
        ),
    ]
    update_netvisor_company_info(objs_=objs)
