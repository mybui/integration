from ipaddress import IPv4Address

from pydantic import BaseSettings


class DbSettings(BaseSettings):
    IP: IPv4Address
    PORT: int
    KEYSPACE: str

    class Config:
        env_file = ".env"
        case_sensitive = True


db_settings = DbSettings()
