from typing import Any

from cassandra.cqlengine.columns import Text, Boolean, BigInt
from cassandra.cqlengine.models import Model


class Provider(Model):
    __table_name__ = "providers"
    id = Text(primary_key=True)
    address = Text()
    businessId = Text(custom_index=True)
    city = Text()
    country = Text()
    description = Text()
    isActive = Boolean()
    name = Text()
    postalnumber = Text()
    tel = Text()
    hubspotId = Text(custom_index=True)
    employeeCount = BigInt()
    updatedAt = BigInt()
    createdAt = BigInt()
    netvisorId = Text(custom_index=True)
    billingDetails = Text()
    netvisorPaymentTime = Text()
    isPrivate = Boolean()

    def reformat_db_obj_into_hubspot_format(self) -> dict[str, Any]:
        return {
            "address": self.address or None,
            "business_id": self.businessId or None,
            "city": self.city or None,
            "country": self.country or None,
            "description": self.description or None,
            "name": self.name or None,
            "zip": self.postalnumber or None,
            "phone": self.tel or None,
            "hs_object_id": self.hubspotId or None,
            "employee_count": self.employeeCount,
        }


class Shop(Model):
    __table_name__ = "shops"
    id = Text(primary_key=True)
    address = Text()
    businessId = Text(custom_index=True)
    city = Text()
    country = Text()
    description = Text()
    isActive = Boolean()
    name = Text()
    tel = Text()
    www = Text()
    hubspotId = Text(custom_index=True)
    employeeCount = BigInt()
    updatedAt = BigInt()
    createdAt = BigInt()
    webflowId = Text(custom_index=True)

    def reformat_db_obj_into_hubspot_format(self) -> dict[str, Any]:
        return {
            "address": self.address or None,
            "business_id": self.businessId or None,
            "city": self.city or None,
            "country": self.country or None,
            "description": self.description or None,
            "name": self.name or None,
            "phone": self.tel or None,
            "website": self.www or None,
            "hs_object_id": self.hubspotId or None,
            "employee_count": self.employeeCount or None,
        } or None


class LogIntegration(Model):
    __table_name__ = "logsintegration"
    id = Text(primary_key=True)
    loggedAt = BigInt()
    day = BigInt()
    month = BigInt()
    year = BigInt()
    description = Text()
    method = Text()
    dbToHs = Boolean()
    hsToDb = Boolean()
    hubspotId = Text()
    target = Text()
    targetId = Text()
    dbToWf = Boolean()
    webflowId = Text()
    dbToNv = Boolean()
    netvisorId = Text()
