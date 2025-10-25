import uuid
from typing import Literal

from msgspec import Struct


class JobStatus(Struct):
    id: uuid.UUID
    status: str
    error_code: str | None = None
    error_msg: str | None = None


class JobUpdate(Struct):
    status: Literal["processing", "succeeded", "failed", "timeout", "queued"]
    error_code: str | None = None
    error_msg: str | None = None
