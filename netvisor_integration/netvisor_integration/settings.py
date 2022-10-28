from pydantic import BaseSettings, SecretStr


class Settings(BaseSettings):
    CLIENT: str
    CUSTOMER_ID: str
    PRIVATE_KEY: SecretStr
    PARTNER_ID: str
    PARNER_PRIVATE_KEY: SecretStr
    LANGCODE: str
    CID: str

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
