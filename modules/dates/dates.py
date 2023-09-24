from .constants import *
from datetime import datetime, date, time, timedelta
from typing import Tuple


def get_format(format_type: str = "standard_datetime"):
    """Will retrieve strftime formats from constants"""
    return FORMATS.get(format_type.split("_")[1]).get(format_type.split("_")[0])


def now(format_type: str = "standard_datetime") -> str:
    """Get Datetime (Now)

    Parameters
    ----------
        format_type (str, optional): str, default "standard_datetime"
            ex. "standard_datetime" = `%Y-%m-%d %H:%M:%S`
            ex. "numeric_date" = `%Y%m%d`

    Returns
    -------
        str
            datetime string
    """
    """Gets now format"""
    return datetime.now().strftime(get_format(format_type))


def get_dates_in_range(min_date: str, max_date: str = now("standard_date")) -> list:
    """Get all dates within range

    Parameters
    ----------
        min_date : str
            start date
        max_date (str, optional): str, default now("standard_date")
            end date

    Returns
    -------
        list
            list of dates
    """
    days = []
    min_date = datetime.strptime(min_date, get_format("standard_date"))
    max_date = datetime.strptime(max_date, get_format("standard_date"))
    while min_date <= max_date:
        days.append(min_date)
        min_date + timedelta(days=1)
    return [x.strftime(get_format("standard_date")) for x in days]


def convert_epoch_ms_to_dt(epoch_ms: Tuple[float, int]) -> datetime:
    """Convert epoch_ms to datetime

    Parameters
    ----------
        epoch_ms : Tuple[float, int]
            epoch timestamp

    Returns
    -------
        datetime
    """
    return datetime.fromtimestamp(epoch_ms / 1000.0)


def x_days_ago(days: int = 0, format_type: str = "standard_date") -> str:
    """Get Date _ Days Ago

    Parameters
    ----------
        days (int, optional): int, default 0
            Number of days ago
        format_type (str, optional): str, default "standard_date"
            datetime.str.format ex `%Y-%m-%d`

    Returns
    -------
        str
            datetime str
    """
    return (datetime.now() - timedelta(days=days)).strftime(format_type)
