from typing import Literal
from uuid import UUID

from msgspec import Struct


class JobStatusResponse(Struct):
    id: UUID
    status: Literal["processing", "succeeded", "failed", "timeout", "queued"]
    error_code: str | None = None
    error_msg: str | None = None


class JobStatusUpdateRequest(Struct):
    status: Literal["processing", "succeeded", "failed", "timeout", "queued"]
    error_code: str | None = None
    error_msg: str | None = None


class ClaimCreateRequest(Struct):
    key: str


class ClaimResponse(Struct):
    claimed: bool
