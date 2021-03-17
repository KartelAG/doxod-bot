''' this file is copied from https://github.com/alexey-goloburdin/tinkoff-analytics
    hope, this is not a crime :)
'''
from datetime import datetime

from pytz import timezone


def localize(d: datetime) -> datetime:
    return timezone('Asia/Yekaterinburg').localize(d)


def get_now() -> datetime:
    return localize(datetime.now())