import datetime
from typing import Optional, Tuple

import unidecode

from . import helper_config


def get_last_minutes_date_time() -> int:
    return int(
        datetime.datetime.timestamp(
            datetime.datetime.now() - datetime.timedelta(minutes=helper_config.minutes)
        )
    )


def format_date_time(string: str) -> float:
    return datetime.datetime.timestamp(datetime.datetime.fromisoformat(string))


def get_timestamp_now() -> float:
    return datetime.datetime.now().timestamp()


def get_datetime_now() -> Tuple[int, int, int]:
    datetime_ = datetime.datetime.now()
    return datetime_.day, datetime_.month, datetime_.year


def get_datetime_for_log(
    string: str,
) -> Tuple[Optional[int], Optional[int], Optional[int]]:
    if string:
        datetime_ = datetime.datetime.fromisoformat(string)
        return datetime_.day, datetime_.month, datetime_.year
    return None, None, None


def get_bool_value_from_string(string: str) -> Optional[bool]:
    if string:
        if string.lower() == "false":
            return False
        if string.lower() == "true":
            return True
    return None


def get_slug(string: str) -> Optional[str]:
    if string:
        return unidecode.unidecode(string).lower().replace(" ", "-")
    return None


def clean_business_id_with_spaces(string: str) -> str:
    return string.replace(" ", "")
