import datetime
from typing import Annotated, Literal

import msgspec
from msgspec import UNSET, Meta, Struct, UnsetType, ValidationError

from genjipk_sdk.utilities.lootbox import sanitize_string

from ..utilities import difficulties
from ..utilities.maps import get_map_banner
from ..utilities.types import (
    GuideURL,
    MapCategory,
    Mechanics,
    OverwatchCode,
    OverwatchMap,
    PlaytestStatus,
    Restrictions,
)
from .users import Creator, CreatorFull

MAX_CREATORS = 3


class Medals(msgspec.Struct):
    gold: float
    silver: float
    bronze: float

    def __post_init__(self) -> None:
        """Validate medals.

        All medals must be present and be in order.
        """
        if not (self.bronze > self.silver > self.gold):
            raise ValidationError("Bronze medal must be larger than silver, and silver larger than gold.")


class Guide(msgspec.Struct):
    url: GuideURL
    user_id: int


class GuideFull(Guide):
    usernames: list[str] = []


class MapCreateDTO(msgspec.Struct):
    code: OverwatchCode
    map_name: OverwatchMap
    category: MapCategory
    creators: Annotated[list[Creator], msgspec.Meta(max_length=3)]
    checkpoints: Annotated[int, msgspec.Meta(gt=0)]
    difficulty: difficulties.DifficultyAll
    official: bool = True
    hidden: bool = True
    playtesting: PlaytestStatus = "In Progress"
    archived: bool = False
    mechanics: list[Mechanics] = []
    restrictions: list[Restrictions] = []
    description: str | None = None
    medals: Medals | None = None
    guide_url: GuideURL | None = None
    title: str | None = None
    custom_banner: str | None = None

    @property
    def primary_creator_id(self) -> int:
        """Get the primary creator."""
        res = next((element for element in self.creators if element.is_primary), None)
        if not res:
            raise ValueError("No primary creator found.")
        return res.id


class MapPatchDTO(msgspec.Struct, kw_only=True):
    code: OverwatchCode | UnsetType = UNSET
    map_name: OverwatchMap | UnsetType = UNSET
    category: MapCategory | UnsetType = UNSET
    creators: list[Creator] | UnsetType = UNSET
    checkpoints: Annotated[int, msgspec.Meta(gt=0)] | UnsetType = UNSET
    difficulty: difficulties.DifficultyAll | UnsetType = UNSET
    hidden: bool | UnsetType = UNSET
    official: bool | UnsetType = UNSET
    playtesting: PlaytestStatus | UnsetType = UNSET
    archived: bool | UnsetType = UNSET
    mechanics: list[Mechanics] | UnsetType | None = UNSET
    restrictions: list[Restrictions] | UnsetType | None = UNSET
    description: str | UnsetType | None = UNSET
    medals: Medals | UnsetType | None = UNSET
    title: str | UnsetType | None = UNSET
    custom_banner: str | UnsetType | None = UNSET


class ArchivalStatusPatchDTO(msgspec.Struct):
    codes: list[OverwatchCode]
    status: Literal["Archive", "Unarchived"]


class MapReadPlaytestDTO(msgspec.Struct):
    thread_id: int
    vote_average: float | None
    vote_count: int | None
    voters: list[int] | None
    verification_id: int | None
    initial_difficulty: float
    completed: bool


class MapReadDTO(msgspec.Struct):
    id: int
    code: OverwatchCode
    map_name: OverwatchMap
    category: MapCategory
    creators: list[CreatorFull]
    checkpoints: Annotated[int, msgspec.Meta(gt=0)]
    difficulty: difficulties.DifficultyAll
    official: bool
    playtesting: PlaytestStatus
    archived: bool
    hidden: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime
    ratings: float | None
    playtest: MapReadPlaytestDTO | None
    guides: list[GuideURL] | None = None
    raw_difficulty: Annotated[float, msgspec.Meta(ge=0, le=10)] | None = None
    mechanics: list[Mechanics] = []
    restrictions: list[Restrictions] = []
    description: str | None = None
    medals: Medals | None = None
    title: str | None = None
    map_banner: str | None = ""
    time: float | None = None
    total_results: int | None = None

    def __post_init__(self) -> None:
        """Post init."""
        self.creators.sort(key=lambda c: not c.is_primary)
        if not self.map_banner:
            self.map_banner = get_map_banner(self.map_name)

    @property
    def primary_creator_id(self) -> int:
        """Get the primary creator."""
        res = next((element for element in self.creators if element.is_primary), None)
        if not res:
            raise ValueError("No primary creator found.")
        return res.id

    @property
    def primary_creator_name(self) -> str:
        """Get the primary creator."""
        res = next((element for element in self.creators if element.is_primary), None)
        if not res:
            raise ValueError("No primary creator found.")
        return res.name


class PlaytestCreatePartialDTO(msgspec.Struct):
    code: OverwatchCode
    initial_difficulty: difficulties.DifficultyAll


class PlaytestAssociateIDThread(msgspec.Struct):
    playtest_id: int
    thread_id: int


class PlaytestCreateDTO(msgspec.Struct):
    code: OverwatchCode
    thread_id: int
    initial_difficulty: difficulties.DifficultyAll


class PlaytestReadDTO(msgspec.Struct):
    id: int
    thread_id: int | None
    code: OverwatchCode
    verification_id: int | None
    initial_difficulty: float
    created_at: datetime.datetime
    updated_at: datetime.datetime
    completed: bool
    thread_creation_status: Literal["pending", "processing", "success", "failed"] | None = None
    thread_creation_failure_reason: str | None = None
    thread_creation_last_attempt_at: datetime.datetime | None = None


class PlaytestPatchDTO(msgspec.Struct):
    thread_id: int | UnsetType = UNSET
    verification_id: int | UnsetType = UNSET
    completed: bool | UnsetType = UNSET
    thread_creation_status: Literal["pending", "processing", "success", "failed"] | msgspec.UnsetType = msgspec.UNSET
    thread_creation_failure_reason: str | None | msgspec.UnsetType = msgspec.UNSET
    thread_creation_last_attempt_at: datetime.datetime | msgspec.UnsetType = msgspec.UNSET


class MapReadPartialDTO(msgspec.Struct):
    map_id: int
    code: OverwatchCode
    difficulty: difficulties.DifficultyAll
    creator_name: str
    map_name: OverwatchMap
    checkpoints: int

    @property
    def thread_name(self) -> str:
        """Return the thread name."""
        return f"{self.code} | {self.difficulty} {self.map_name} by {self.creator_name}"[:100]


class MessageQueueCreatePlaytest(msgspec.Struct):
    code: OverwatchCode
    playtest_id: int


class PlaytestVote(msgspec.Struct):
    code: OverwatchCode
    difficulty: float


class PlaytestVoteWithUser(msgspec.Struct):
    user_id: int
    name: str
    difficulty: float


class PlaytestVotesAll(msgspec.Struct):
    votes: list[PlaytestVoteWithUser]
    average: float | None


class MapMasteryCreateDTO(msgspec.Struct):
    user_id: int
    map_name: OverwatchMap
    level: str


class MapMasteryCreateReturnDTO(msgspec.Struct):
    map_name: OverwatchMap
    medal: str
    operation_status: Literal["inserted", "updated"]


class MapMasteryData(msgspec.Struct):
    map_name: OverwatchMap
    amount: int
    level: str | None = None
    icon_url: str | None = None

    def __post_init__(self) -> None:
        """Post init."""
        self.level = self._level()
        self.icon_url = self._icon_url()

    def _level(self) -> str:
        thresholds = [
            (0, "Placeholder"),
            (5, "Rookie"),
            (10, "Explorer"),
            (15, "Trailblazer"),
            (20, "Pathfinder"),
            (25, "Specialist"),
            (30, "Prodigy"),
        ]

        icon_name = "Placeholder"
        for threshold, name in thresholds:
            if self.amount >= threshold:
                icon_name = name
        return icon_name

    def _icon_url(self) -> str:
        _sanitized_map_name = sanitize_string(self.map_name)
        assert self.level
        _lowered_level = self.level.lower()
        return f"assets/mastery/{_sanitized_map_name}_{_lowered_level}.webp"


class PlaytestApproveCreate(msgspec.Struct):
    verifier_id: int


class PlaytestApproveMQ(PlaytestApproveCreate):
    thread_id: int


class PlaytestForceAcceptCreate(msgspec.Struct):
    difficulty: difficulties.DifficultyAll
    verifier_id: int


class PlaytestForceAcceptMQ(PlaytestForceAcceptCreate):
    thread_id: int


class PlaytestForceDenyCreate(msgspec.Struct):
    verifier_id: int
    reason: str


class PlaytestForceDenyMQ(PlaytestForceDenyCreate):
    thread_id: int


class PlaytestResetCreate(msgspec.Struct):
    verifier_id: int
    reason: str
    remove_votes: bool
    remove_completions: bool


class PlaytestResetMQ(PlaytestResetCreate):
    thread_id: int


class PlaytestVoteCastCreate(msgspec.Struct):
    voter_id: int
    difficulty_value: float


class PlaytestVoteCastMQ(PlaytestVoteCastCreate):
    thread_id: int


class PlaytestVoteRemovedCreate(msgspec.Struct):
    voter_id: int


class PlaytestVoteRemovedMQ(PlaytestVoteRemovedCreate):
    thread_id: int


class MapCompletionStatisticsResponse(Struct):
    min: float | None = None
    max: float | None = None
    avg: float | None = None


class MapPerDifficultyStatisticsResponse(Struct):
    difficulty: difficulties.DifficultyTop
    amount: int


class PopularMapsStatisticsResponse(Struct):
    code: OverwatchCode
    completions: int
    quality: float
    difficulty: difficulties.DifficultyTop
    ranking: int


class TopCreatorsResponse(Struct):
    map_count: int
    name: str
    average_quality: float


class MapCountsResponse(Struct):
    map_name: OverwatchMap
    amount: int


class QualityValueDTO(Struct):
    value: Annotated[int, Meta(ge=1, le=6)]
