import uuid
from typing import Literal

from msgspec import Struct

from .maps import MapReadDTO


class JobStatus(Struct):
    id: uuid.UUID
    status: Literal["processing", "succeeded", "failed", "timeout", "queued"]
    error_code: str | None = None
    error_msg: str | None = None


class JobUpdate(Struct):
    status: Literal["processing", "succeeded", "failed", "timeout", "queued"]
    error_code: str | None = None
    error_msg: str | None = None


class SubmitCompletionReturnDTO(Struct):
    job_status: JobStatus
    completion_id: int


class UpvoteSubmissionReturnDTO(Struct):
    job_status: JobStatus | None
    upvotes: int | None


class CreateMapReturnDTO(Struct):
    job_status: JobStatus | None
    data: MapReadDTO


class CreatePublishNewsfeedReturnDTO(Struct):
    job_status: JobStatus
    newsfeed_id: int


class ClaimRequest(Struct):
    key: str


class ClaimResponse(Struct):
    claimed: bool
