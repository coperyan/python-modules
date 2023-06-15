from .constants import *
from datetime import datetime, date, time


def get_format(format_type: str = "standard_datetime"):
    return FORMATS.get(format_type.split("_")[1]).get(format_type.split("_")[0])


def now(format_type: str = "standard_datetime"):
    return datetime.now().strftime(get_format(format_type))
