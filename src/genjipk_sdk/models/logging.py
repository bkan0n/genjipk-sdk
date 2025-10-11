import datetime as dt

from msgspec import Struct


class LogData(Struct):
    command_name: str
    user_id: int
    created_at: dt.datetime
    namespace: dict
