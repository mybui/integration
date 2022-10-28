from typing import Optional

import validators
from pydantic import BaseModel, Field, validator


class WebflowPartnerUpdate(BaseModel):
    business_id: Optional[str] = Field(alias="business-id")
    locations: Optional[str]
    location_s_2: Optional[list[str]] = Field(alias="location-s-2")
    name: Optional[str]
    slug: Optional[str]
    website: Optional[str]

    @validator("website")
    def validate_url(cls, v):
        if v and not validators.url(v) and not validators.domain(v):
            v = None
        return v


class WebflowPartnerCreate(BaseModel):
    business_id: str = Field(alias="business-id")
    locations: Optional[str]
    location_s_2: Optional[list[str]] = Field(alias="location-s-2")
    name: str
    slug: str
    website: Optional[str]
    archived: bool = Field(default_factory=lambda: False, alias="_archived")
    draft: bool = Field(default_factory=lambda: False, alias="_draft")

    @validator("website")
    def validate_url(cls, v):
        if v and not validators.url(v) and not validators.domain(v):
            v = None
        return v


class WebflowPartnerCityCreate(BaseModel):
    name: str
    slug: str
    archived: bool = Field(default_factory=lambda: False, alias="_archived")
    draft: bool = Field(default_factory=lambda: False, alias="_draft")
