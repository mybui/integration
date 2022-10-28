from cassandra.cqlengine import connection

from . import db_settings
from .logging_config import setup_logging

logger = setup_logging(__name__)


def create_connection() -> bool:
    """
    Connect to database
    :return: True or False
    """
    try:
        connection.setup(
            hosts=[str(db_settings.db_settings.IP)],
            default_keyspace=db_settings.db_settings.KEYSPACE,
            protocol_version=3,
        )
        return True
    except Exception as e:
        logger.error(e)
        return False
