from pydantic import BaseSettings, SecretStr


class Settings(BaseSettings):
    ACCESS_TOKEN: SecretStr
    SITE_ID: str
    COLLECTION_PARTNER_ID: str
    COLLECTION_PARTNER_CITIES_ID: str

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
