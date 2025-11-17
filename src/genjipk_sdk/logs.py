import datetime as dt
from typing import Literal

from msgspec import Struct

from .maps import OverwatchCode

__all__ = (
    "LogCreateRequest",
    "MapClickCreateRequest",
)


class LogCreateRequest(Struct):
    command_name: str
    user_id: int
    created_at: dt.datetime
    namespace: dict


class MapClickCreateRequest(Struct):
    code: OverwatchCode
    ip_address: str
    user_id: int | None
    source: Literal["web", "bot"] = "web"
