from .constants import *
from datetime import datetime, date, time, timedelta
from typing import Tuple


def get_format(format_type: str = "standard_datetime"):
    return FORMATS.get(format_type.split("_")[1]).get(format_type.split("_")[0])


def now(format_type: str = "standard_datetime"):
    return datetime.now().strftime(get_format(format_type))


def get_dates_in_range(min_date: str, max_date: str = now("standard_date")) -> list:
    days = []
    min_date = datetime.strptime(min_date, get_format("standard_date"))
    max_date = datetime.strptime(max_date, get_format("standard_date"))
    while min_date <= max_date:
        days.append(min_date)
        min_date + timedelta(days=1)
    return [x.strftime(get_format("standard_date")) for x in days]


def convert_epoch_ms_to_dt(epoch_ms: Tuple[float, int]) -> datetime:
    return datetime.fromtimestamp(epoch_ms / 1000.0)
