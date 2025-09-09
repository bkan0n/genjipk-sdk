import datetime
from typing import Literal

from msgspec import UNSET, Struct, UnsetType

from genjipk_sdk.utilities.difficulties import DifficultyAll, DifficultyTop
from genjipk_sdk.utilities.types.maps import GuideURL, MedalType, OverwatchCode, OverwatchMap


class CompletionCreateDTO(Struct):
    code: OverwatchCode
    user_id: int
    time: float
    screenshot: GuideURL
    video: GuideURL | None


class CompletionReadDTO(Struct):
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
    legacy_medal: str | None
    suspicious: bool
    total_results: int | None = None
    upvotes: int = 0


class CompletionSubmissionReadDTO(Struct):
    id: int
    user_id: int
    time: float
    screenshot: str
    video: GuideURL | None
    verified: bool
    completion: bool
    inserted_at: datetime.datetime
    code: OverwatchCode
    difficulty: DifficultyAll
    map_name: str
    hypothetical_rank: int | None
    hypothetical_medal: MedalType | None
    name: str
    also_known_as: str
    verified_by: int | None
    verification_id: int | None
    message_id: int | None
    suspicious: bool


class CompletionPatchDTO(Struct):
    message_id: int | UnsetType = UNSET
    completion: bool | UnsetType = UNSET
    verification_id: int | UnsetType = UNSET
    legacy: bool | UnsetType = UNSET
    legacy_medal: str | None | UnsetType = UNSET
    wr_xp_check: bool | UnsetType = UNSET


class WorldRecordXPCheckReadDTO(Struct):
    code: OverwatchCode
    user_id: int


class CompletionVerificationPutDTO(Struct):
    verified_by: int
    verified: bool
    reason: str | None


class PendingVerification(Struct):
    id: int
    verification_id: int


class MessageQueueCompletionsCreate(Struct):
    completion_id: int


class MessageQueueVerificationChange(Struct):
    completion_id: int
    verified: bool
    verified_by: int
    reason: str | None


SuspiciousFlag = Literal["Cheating", "Scripting"]


class SuspiciousCompletionWriteDTO(Struct):
    context: str
    flag_type: SuspiciousFlag
    flagged_by: int
    message_id: int | None = None
    verification_id: int | None = None


class SuspiciousCompletionReadDTO(Struct):
    id: int
    user_id: int
    context: str
    flag_type: SuspiciousFlag
    message_id: int | None
    verification_id: int | None
    flagged_by: int


class UpvoteCreateDTO(Struct):
    user_id: int
    message_id: int


class MapRecordProgressionResponse(Struct):
    time: float
    inserted_at: datetime.datetime


class TimePlayedPerRankResponse(Struct):
    total_seconds: float
    difficulty: DifficultyTop


class UpvoteUpdateDTO(Struct):
    user_id: int
    message_id: int
