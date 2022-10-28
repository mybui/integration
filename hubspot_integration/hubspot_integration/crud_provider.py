import uuid
from typing import Any, Optional, Type

from cassandra.cqlengine.query import BatchQuery
from pydantic import BaseModel, Field

import core.crud_base as crud_base
import core.helper as helper
import core.models as models
from core.logging_config import setup_logging

logger = setup_logging(__name__)


class ProviderUpdate(BaseModel):
    address: Optional[str]
    city: Optional[str]
    country: Optional[str]
    description: Optional[str]
    isActive: Optional[bool] = True
    name: Optional[str]
    postalnumber: Optional[str] = Field(alias="zip")
    tel: Optional[str] = Field(alias="phone")
    hubspotId: Optional[str] = Field(alias="hs_object_id")
    employeeCount: Optional[int] = Field(alias="employee_count")
    updatedAt: int = Field(default_factory=helper.get_timestamp_now)


class ProviderCreate(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    address: Optional[str]
    businessId: Optional[str] = Field(alias="business_id")
    city: Optional[str]
    country: Optional[str]
    description: Optional[str]
    isActive: Optional[bool] = True
    name: Optional[str]
    postalnumber: Optional[str] = Field(alias="zip")
    tel: Optional[str] = Field(alias="phone")
    hubspotId: Optional[str] = Field(alias="hs_object_id")
    employeeCount: Optional[int] = Field(alias="employee_count")
    updatedAt: int = Field(default_factory=helper.get_timestamp_now)
    createdAt: int = Field(default_factory=helper.get_timestamp_now)


class CRUDProvider(crud_base.CRUDBase[models.Provider]):
    @staticmethod
    def reformat_hubspot_obj(hubspot_obj: dict[str, Any]) -> dict[str, Any]:
        return ProviderUpdate(**hubspot_obj).dict(by_alias=True)

    def update_for_hubspot_to_db_integration(
        self,
        db_batch: BatchQuery,
        obj: Type[models.Provider],
        different_values: dict[str, Any],
        log_batch: Optional[BatchQuery],
    ) -> bool:
        try:
            provider = ProviderUpdate(**different_values)
            for key, value in provider.dict(exclude_none=True).items():
                setattr(obj, key, value)
                obj.batch(db_batch).save()

            if log_batch:
                day, month, year = helper.get_datetime_now()
                self.log(
                    batch=log_batch,
                    id=str(uuid.uuid4()),
                    logged_at=helper.get_timestamp_now(),
                    day=day,
                    month=month,
                    year=year,
                    description="Update an existing `provider` in DB from HS with new values: {0}".format(
                        different_values
                    ),
                    method="UPDATE",
                    db_to_hs=False,
                    hs_to_db=True,
                    hubspot_id=obj.hubspotId
                    or different_values.get("hs_object_id", None)
                    or None,
                    target="providers",
                    target_id=obj.id,
                )
            return True
        except Exception as e:
            logger.error(e)
            return False

    def create_for_hubspot_to_db_integration(
        self,
        db_batch: BatchQuery,
        hubspot_obj: dict[str, Any],
        log_batch: Optional[BatchQuery],
    ) -> bool:
        try:
            provider = ProviderCreate(**hubspot_obj)
            obj = self.model.batch(db_batch).create(**provider.dict())

            if log_batch:
                day, month, year = helper.get_datetime_now()
                self.log(
                    batch=log_batch,
                    id=str(uuid.uuid4()),
                    logged_at=helper.get_timestamp_now(),
                    day=day,
                    month=month,
                    year=year,
                    description="Create a new `provider` in DB from HS",
                    method="CREATE",
                    db_to_hs=False,
                    hs_to_db=True,
                    hubspot_id=hubspot_obj.get("hs_object_id", None) or None,
                    target="providers",
                    target_id=obj.id,
                )
            return True
        except Exception as e:
            logger.error(e)
            return False
