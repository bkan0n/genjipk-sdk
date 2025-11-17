import datetime as dt
from typing import Annotated, Literal

from msgspec import UNSET, Meta, Struct, UnsetType

from .difficulties import DifficultyAll, DifficultyTop
from .internal import JobStatusResponse
from .maps import GuideURL, MedalType, OverwatchCode, OverwatchMap

__all__ = (
    "CompletionCreateRequest",
    "CompletionCreatedEvent",
    "CompletionPatchRequest",
    "CompletionResponse",
    "CompletionSubmissionJobResponse",
    "CompletionSubmissionResponse",
    "CompletionVerificationUpdateRequest",
    "ExtractedResultResponse",
    "ExtractedTextsResponse",
    "FailedAutoverifyEvent",
    "MapRecordProgressionResponse",
    "OcrResponse",
    "PendingVerificationResponse",
    "QualityUpdateRequest",
    "SuspiciousCompletionCreateRequest",
    "SuspiciousCompletionResponse",
    "SuspiciousFlag",
    "TimePlayedPerRankResponse",
    "UpvoteCreateRequest",
    "UpvoteSubmissionJobResponse",
    "UpvoteUpdateRequest",
    "VerificationChangedEvent",
    "WorldRecordXPCheckResponse",
)


class CompletionSubmissionJobResponse(Struct):
    job_status: JobStatusResponse | None
    completion_id: int


class UpvoteSubmissionJobResponse(Struct):
    job_status: JobStatusResponse | None
    upvotes: int | None


class CompletionCreateRequest(Struct):
    code: OverwatchCode
    user_id: int
    time: float
    screenshot: GuideURL
    video: GuideURL | None


class CompletionResponse(Struct):
    code: OverwatchCode
    user_id: int
    name: str
    also_known_as: str | None
    time: float
    screenshot: str
    video: GuideURL | None
    completion: bool
    verified: bool
    rank: int | None
    medal: MedalType | None
    map_name: OverwatchMap
    difficulty: DifficultyAll
    message_id: int
    legacy: bool
    legacy_medal: MedalType | None
    suspicious: bool
    total_results: int | None = None
    upvotes: int = 0


class CompletionSubmissionResponse(Struct):
    id: int
    user_id: int
    time: float
    screenshot: str
    video: GuideURL | None
    verified: bool
    completion: bool
    inserted_at: dt.datetime
    code: OverwatchCode
    difficulty: DifficultyAll
    map_name: OverwatchMap
    hypothetical_rank: int | None
    hypothetical_medal: MedalType | None
    name: str
    also_known_as: str
    verified_by: int | None
    verification_id: int | None
    message_id: int | None
    suspicious: bool


class CompletionPatchRequest(Struct):
    message_id: int | UnsetType = UNSET
    completion: bool | UnsetType = UNSET
    verification_id: int | UnsetType = UNSET
    legacy: bool | UnsetType = UNSET
    legacy_medal: str | None | UnsetType = UNSET
    wr_xp_check: bool | UnsetType = UNSET


class WorldRecordXPCheckResponse(Struct):
    code: OverwatchCode
    user_id: int


class CompletionVerificationUpdateRequest(Struct):
    verified_by: int
    verified: bool
    reason: str | None


class PendingVerificationResponse(Struct):
    id: int
    verification_id: int


class CompletionCreatedEvent(Struct):
    completion_id: int


class VerificationChangedEvent(Struct):
    completion_id: int
    verified: bool
    verified_by: int
    reason: str | None


SuspiciousFlag = Literal["Cheating", "Scripting"]


class SuspiciousCompletionCreateRequest(Struct):
    context: str
    flag_type: SuspiciousFlag
    flagged_by: int
    message_id: int | None = None
    verification_id: int | None = None


class SuspiciousCompletionResponse(Struct):
    id: int
    user_id: int
    context: str
    flag_type: SuspiciousFlag
    message_id: int | None
    verification_id: int | None
    flagged_by: int


class UpvoteCreateRequest(Struct):
    user_id: int
    message_id: int


class MapRecordProgressionResponse(Struct):
    time: float
    inserted_at: dt.datetime


class TimePlayedPerRankResponse(Struct):
    total_seconds: float
    difficulty: DifficultyTop


class UpvoteUpdateEvent(Struct):
    user_id: int
    message_id: int


class QualityUpdateRequest(Struct):
    user_id: int
    quality: Annotated[int, Meta(ge=1, le=6)]


def to_camel(name: str) -> str:
    """Convert a snake_case field name to camelCase."""
    parts = name.split("_")
    return parts[0] + "".join(p.title() for p in parts[1:])


class CamelConfig(Struct, rename=to_camel):
    """Base struct that renames fields to camelCase during encoding/decoding."""


class ExtractedTextsResponse(CamelConfig):
    top_left: str | None
    top_left_white: str | None
    top_left_cyan: str | None
    banner: str | None
    top_right: str | None
    bottom_left: str | None


class ExtractedResultResponse(CamelConfig):
    name: str | None
    time: float | None
    code: str | None
    texts: ExtractedTextsResponse


class OcrResponse(CamelConfig):
    extracted: ExtractedResultResponse


class FailedAutoverifyEvent(Struct):
    submitted_code: OverwatchCode
    submitted_time: float
    user_id: int
    extracted: ExtractedResultResponse
    code_match: bool
    time_match: bool
    user_match: bool
    extracted_code_cleaned: str | None
    extracted_time: float | None
    extracted_user_id: int | None
