from pydantic import BaseSettings, SecretStr


class Settings(BaseSettings):
    ACCESS_TOKEN: SecretStr

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
