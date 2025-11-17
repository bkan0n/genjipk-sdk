from typing import Literal

from msgspec import Struct

ChangeRequestType = Literal[
    "Difficulty Change",
    "Map Geometry",
    "Map Edit Required",
    "Framework/Workshop",
    "Other",
]


class ChangeRequestCreateRequest(Struct):
    thread_id: int
    user_id: int
    code: str
    content: str
    change_request_type: ChangeRequestType
    creator_mentions: str


class ChangeRequestResponse(Struct):
    thread_id: int
    user_id: int
    code: str
    content: str
    change_request_type: ChangeRequestType
    creator_mentions: str | None = None
    alerted: bool = False
    resolved: bool = False


class StaleChangeRequestResponse(Struct):
    thread_id: int
    user_id: int
    creator_mentions: str
