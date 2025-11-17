from __future__ import annotations

import datetime as dt
import re
from typing import Annotated, Literal

from msgspec import UNSET, Meta, Struct, UnsetType, ValidationError

from .difficulties import DifficultyAll, DifficultyTop
from .helpers import sanitize_string
from .internal import JobStatusResponse
from .users import Creator, CreatorFull

MAX_CREATORS = 3

URL_PATTERN = r"(https?:\/\/)([\w\-])+\.{1}([a-zA-Z]{2,63})([\/\w-]*)*\/?\??([^#\n\r]*)?#?([^\n\r]*)"
URL_REGEX = re.compile(URL_PATTERN)

OverwatchCode = Annotated[str, Meta(min_length=4, max_length=6, pattern="^[A-Z0-9]*$")]
GuideURL = Annotated[
    str,
    Meta(
        pattern=URL_PATTERN,
        description="Must be a valid URL starting with http:// or https://.",
    ),
]

MapCategory = Literal[
    "Classic",
    "Increasing Difficulty",
    "Other",
]

OverwatchMap = Literal[
    "Circuit Royal",
    "Runasapi",
    "Practice Range",
    "Route 66",
    "Midtown",
    "Junkertown",
    "Colosseo",
    "Lijiang Tower (Lunar New Year)",
    "Dorado",
    "Throne of Anubis",
    "Castillo",
    "Blizzard World (Winter)",
    "Hollywood (Halloween)",
    "King's Row",
    "Black Forest (Winter)",
    "Petra",
    "Framework",
    "Eichenwalde",
    "Workshop Island",
    "Chateau Guillard (Halloween)",
    "New Junk City",
    "Necropolis",
    "Kanezaka",
    "Havana",
    "Oasis",
    "Ayutthaya",
    "Volskaya Industries",
    "Hanamura",
    "Workshop Expanse",
    "Hanaoka",
    "Lijiang Tower",
    "Busan (Lunar New Year)",
    "Suravasa",
    "King's Row (Winter)",
    "Ecopoint: Antarctica",
    "Hanamura (Winter)",
    "Blizzard World",
    "Chateau Guillard",
    "Paraiso",
    "Workshop Green Screen",
    "Watchpoint: Gibraltar",
    "Shambali",
    "Eichenwalde (Halloween)",
    "Tools",
    "Nepal",
    "Samoa",
    "Horizon Lunar Colony",
    "Paris",
    "Esperanca",
    "Black Forest",
    "Antarctic Peninsula",
    "Workshop Chamber",
    "Hollywood",
    "New Queen Street",
    "Rialto",
    "Busan",
    "Malevento",
    "Temple of Anubis",
    "Ilios",
    "Ecopoint: Antarctica (Winter)",
    "Numbani",
    "Adlersbrunn",
    "Aatlis",
]

Mechanics = Literal[
    "Edge Climb",
    "Bhop",
    "Save Climb",
    "High Edge",
    "Distance Edge",
    "Quick Climb",
    "Slide",
    "Stall",
    "Dash",
    "Ultimate",
    "Emote Save Bhop",
    "Death Bhop",
    "Triple Jump",
    "Multi Climb",
    "Vertical Multi Climb",
    "Standing Create Bhop",
    "Crouch Edge",
    "Bhop First",
    "Create Bhop",
    "Save Double",
]

Restrictions = Literal[
    "Wall Climb",
    "Create Bhop",
    "Dash Start",
    "Death Bhop",
    "Triple Jump",
    "Multi Climb",
    "Standing Create Bhop",
    "Emote Save Bhop",
    "Double Jump",
    "Bhop",
]

PlaytestStatus = Literal["Approved", "In Progress", "Rejected"]

MedalType = Literal["Gold", "Silver", "Bronze"]


class MapCreationJobResponse(Struct):
    job_status: JobStatusResponse | None
    data: MapResponse


class MedalsResponse(Struct):
    gold: float
    silver: float
    bronze: float

    def __post_init__(self) -> None:
        """Validate medals.

        All medals must be present and be in order.
        """
        if not (self.bronze > self.silver > self.gold):
            raise ValidationError("Bronze medal must be larger than silver, and silver larger than gold.")


class GuideResponse(Struct):
    url: GuideURL
    user_id: int


class GuideFullResponse(GuideResponse):
    usernames: list[str] = []


class MapCreateRequest(Struct):
    code: OverwatchCode
    map_name: OverwatchMap
    category: MapCategory
    creators: Annotated[list[Creator], Meta(max_length=3)]
    checkpoints: Annotated[int, Meta(gt=0)]
    difficulty: DifficultyAll
    official: bool = True
    hidden: bool = True
    playtesting: PlaytestStatus = "In Progress"
    archived: bool = False
    mechanics: list[Mechanics] = []
    restrictions: list[Restrictions] = []
    description: str | None = None
    medals: MedalsResponse | None = None
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


class MapPatchRequest(Struct, kw_only=True):
    code: OverwatchCode | UnsetType = UNSET
    map_name: OverwatchMap | UnsetType = UNSET
    category: MapCategory | UnsetType = UNSET
    creators: list[Creator] | UnsetType = UNSET
    checkpoints: Annotated[int, Meta(gt=0)] | UnsetType = UNSET
    difficulty: DifficultyAll | UnsetType = UNSET
    hidden: bool | UnsetType = UNSET
    official: bool | UnsetType = UNSET
    playtesting: PlaytestStatus | UnsetType = UNSET
    archived: bool | UnsetType = UNSET
    mechanics: list[Mechanics] | UnsetType | None = UNSET
    restrictions: list[Restrictions] | UnsetType | None = UNSET
    description: str | UnsetType | None = UNSET
    medals: MedalsResponse | UnsetType | None = UNSET
    title: str | UnsetType | None = UNSET
    custom_banner: str | UnsetType | None = UNSET


class ArchivalStatusPatchRequest(Struct):
    codes: list[OverwatchCode]
    status: Literal["Archive", "Unarchived"]


class MapPlaytestResponse(Struct):
    thread_id: int
    vote_average: float | None
    vote_count: int | None
    voters: list[int] | None
    verification_id: int | None
    initial_difficulty: float
    completed: bool


class MapResponse(Struct):
    id: int
    code: OverwatchCode
    map_name: OverwatchMap
    category: MapCategory
    creators: list[CreatorFull]
    checkpoints: Annotated[int, Meta(gt=0)]
    difficulty: DifficultyAll
    official: bool
    playtesting: PlaytestStatus
    archived: bool
    hidden: bool
    created_at: dt.datetime
    updated_at: dt.datetime
    ratings: float | None
    playtest: MapPlaytestResponse | None
    guides: list[GuideURL] | None = None
    raw_difficulty: Annotated[float, Meta(ge=0, le=10)] | None = None
    mechanics: list[Mechanics] = []
    restrictions: list[Restrictions] = []
    description: str | None = None
    medals: MedalsResponse | None = None
    title: str | None = None
    map_banner: str | None = ""
    time: float | None = None
    total_results: int | None = None
    linked_code: OverwatchCode | None = None

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


class SendToPlaytestRequest(Struct):
    initial_difficulty: DifficultyAll


class PlaytestCreatePartialRequest(Struct):
    code: OverwatchCode
    initial_difficulty: DifficultyAll


class PlaytestThreadAssociateRequest(Struct):
    playtest_id: int
    thread_id: int


class PlaytestCreateRequest(Struct):
    code: OverwatchCode
    thread_id: int
    initial_difficulty: DifficultyAll


class PlaytestResponse(Struct):
    id: int
    thread_id: int | None
    code: OverwatchCode
    verification_id: int | None
    initial_difficulty: float
    created_at: dt.datetime
    updated_at: dt.datetime
    completed: bool
    thread_creation_status: Literal["pending", "processing", "success", "failed"] | None = None
    thread_creation_failure_reason: str | None = None
    thread_creation_last_attempt_at: dt.datetime | None = None


class PlaytestPatchRequest(Struct):
    thread_id: int | UnsetType = UNSET
    verification_id: int | UnsetType = UNSET
    completed: bool | UnsetType = UNSET
    thread_creation_status: Literal["pending", "processing", "success", "failed"] | UnsetType = UNSET
    thread_creation_failure_reason: str | None | UnsetType = UNSET
    thread_creation_last_attempt_at: dt.datetime | UnsetType = UNSET


class MapPartialResponse(Struct):
    map_id: int
    code: OverwatchCode
    difficulty: DifficultyAll
    creator_name: str
    map_name: OverwatchMap
    checkpoints: int

    @property
    def thread_name(self) -> str:
        """Return the thread name."""
        return f"{self.code} | {self.difficulty} {self.map_name} by {self.creator_name}"[:100]


class PlaytestCreatedEvent(Struct):
    code: OverwatchCode
    playtest_id: int


class PlaytestVote(Struct):
    difficulty: float


class PlaytestVoteWithUser(Struct):
    user_id: int
    name: str
    difficulty: float


class PlaytestVotesResponse(Struct):
    votes: list[PlaytestVoteWithUser]
    average: float | None


class MapMasteryCreateRequest(Struct):
    user_id: int
    map_name: OverwatchMap
    level: str


class MapMasteryCreateResponse(Struct):
    map_name: OverwatchMap
    medal: str
    operation_status: Literal["inserted", "updated"]


class MapMasteryResponse(Struct):
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


class PlaytestApproveRequest(Struct):
    verifier_id: int


class PlaytestApprovedEvent(Struct):
    verifier_id: int
    difficulty: DifficultyAll
    thread_id: int
    primary_creator_id: int
    code: OverwatchCode


class PlaytestForceAcceptRequest(Struct):
    difficulty: DifficultyAll
    verifier_id: int


class PlaytestForceAcceptedEvent(Struct):
    difficulty: DifficultyAll
    verifier_id: int
    thread_id: int


class PlaytestForceDenyRequest(Struct):
    verifier_id: int
    reason: str


class PlaytestForceDeniedEvent(Struct):
    verifier_id: int
    reason: str
    thread_id: int


class PlaytestResetRequest(Struct):
    verifier_id: int
    reason: str
    remove_votes: bool
    remove_completions: bool


class PlaytestResetEvent(Struct):
    verifier_id: int
    reason: str
    remove_votes: bool
    remove_completions: bool
    thread_id: int


class PlaytestVoteCastRequest(Struct):
    voter_id: int
    difficulty_value: float


class PlaytestVoteCastEvent(Struct):
    voter_id: int
    difficulty_value: float
    thread_id: int


class PlaytestVoteRemovedRequest(Struct):
    voter_id: int


class PlaytestVoteRemovedEvent(Struct):
    voter_id: int
    thread_id: int


class MapCompletionStatisticsResponse(Struct):
    min: float | None = None
    max: float | None = None
    avg: float | None = None


class MapPerDifficultyStatisticsResponse(Struct):
    difficulty: DifficultyTop
    amount: int


class PopularMapsStatisticsResponse(Struct):
    code: OverwatchCode
    completions: int
    quality: float
    difficulty: DifficultyTop
    ranking: int


class TopCreatorsResponse(Struct):
    map_count: int
    name: str
    average_quality: float


class MapCountsResponse(Struct):
    map_name: OverwatchMap
    amount: int


class QualityValueRequest(Struct):
    value: Annotated[int, Meta(ge=1, le=6)]


class XPMultiplierRequest(Struct):
    value: Annotated[float, Meta(ge=1, le=10)]


class TrendingMapResponse(Struct):
    code: OverwatchCode
    map_name: OverwatchMap
    clicks: int
    completions: int
    upvotes: int
    momentum: float
    trend_score: float


class LinkMapsCreateRequest(Struct):
    official_code: OverwatchCode
    unofficial_code: OverwatchCode


class UnlinkMapsCreateRequest(Struct):
    official_code: OverwatchCode
    unofficial_code: OverwatchCode
    reason: str


PLAYTEST_VOTE_THRESHOLD: dict[DifficultyTop, int] = {
    "Easy": 5,
    "Medium": 5,
    "Hard": 5,
    "Very Hard": 3,
    "Extreme": 2,
    "Hell": 1,
}


def get_map_banner(map_name: str) -> str:
    """Get the applicable map banner."""
    _map = re.sub(r"[^a-zA-Z0-9]", "", map_name)
    sanitized_name = _map.lower().strip().replace(" ", "")
    return f"https://bkan0n.com/assets/images/map_banners/{sanitized_name}.png"
