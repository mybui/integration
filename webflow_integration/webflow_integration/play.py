import core.db as db
import core.models as models
import unidecode

import crud_shop as crud
import webflow_models

db.create_connection()

crud_shop = crud.CRUDShop(models.Shop, table_name="shops")

print(webflow_models.WebflowPartnerUpdate(**{"_archived": True}).dict(by_alias=True))