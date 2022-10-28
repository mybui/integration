from pydantic import BaseModel, Field

from netvisor_integration import settings


class NetvisorHeadersBase(BaseModel):
    content_type: str = Field(default_factory=lambda: "text/plain",
                              alias="Content-Type")
    sender: str = Field(default_factory=lambda: settings.settings.CLIENT,
                        alias="X-Netvisor-Authentication-Sender")
    customer_id: str = Field(default_factory=lambda: settings.settings.CUSTOMER_ID,
                             alias="X-Netvisor-Authentication-CustomerId")
    partner_id: str = Field(default_factory=lambda: settings.settings.PARTNER_ID,
                            alias="X-Netvisor-Authentication-PartnerId")
    langcode: str = Field(default_factory=lambda: settings.settings.LANGCODE,
                          alias="X-Netvisor-Interface-Language")
    cid: str = Field(default_factory=lambda: settings.settings.CID,
                     alias="X-Netvisor-Organisation-ID")
    algorithm: str = Field(default_factory=lambda: "SHA256",
                           alias="X-Netvisor-Authentication-MACHashCalculationAlgorithm")


class NetvisorCustomerListHeaders(BaseModel):
    timestamp: str = Field(alias="X-Netvisor-Authentication-Timestamp")
    transaction_id: str = Field(alias="X-Netvisor-Authentication-TransactionId")
    h_mac: str = Field(alias="X-Netvisor-Authentication-MAC")


# to be created based on the Netvisor data model (see the Webflow integration program)
class NetvisorCustomerUpdate(BaseModel):
    pass


class NetvisorCustomerCreate(BaseModel):
    pass