import datetime as dt

from msgspec import Struct


class LogCreateDTO(Struct):
    command_name: str
    user_id: int
    created_at: dt.datetime
    namespace: dict
