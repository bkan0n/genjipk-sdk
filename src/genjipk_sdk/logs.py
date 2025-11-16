import datetime as dt
from typing import Literal

from msgspec import Struct

from .maps import OverwatchCode


class LogCreateDTO(Struct):
    command_name: str
    user_id: int
    created_at: dt.datetime
    namespace: dict


class MapClickCreateDTO(Struct):
    code: OverwatchCode
    ip_address: str
    user_id: int | None
    source: Literal["web", "bot"] = "web"
