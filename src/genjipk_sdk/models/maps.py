import datetime
import re
from typing import Annotated, Literal, Optional

import msgspec

from ..utilities import difficulties
from ..utilities.types import MapCategory, Mechanics, OverwatchCode, OverwatchMap, Restrictions

# All possible map attrs


# code: OverwatchCode  # noqa: ERA001
# name: OverwatchMap  # noqa: ERA001
# category: list[MapCategory]  # noqa: ERA001
# primary_creator_id: int  # noqa: ERA001
# checkpoints: int  # noqa: ERA001
# difficulty: float  # noqa: ERA001
# playtest_id: Optional[int] = None  # noqa: ERA001
# official: bool = True  # noqa: ERA001
# playtesting: bool = True  # noqa: ERA001
# archived: bool = False  # noqa: ERA001
# secondary_creator_id: Optional[int] = None  # noqa: ERA001
# tertiary_creator_id: Optional[int] = None  # noqa: ERA001
# description: Optional[str] = None  # noqa: ERA001
# mechanics: list[Mechanics] = []  # noqa: ERA001
# restrictions: list[restrictions] = []  # noqa: ERA001
# giudes  # noqa: ERA001
# gold: float = 0  # noqa: ERA001
# silver: float = 0  # noqa: ERA001
# bronze: float = 0  # noqa: ERA001
PlaytestStatus = Literal["Approved", "In Progress", "Rejected"]


class BaseMap(msgspec.Struct, kw_only=True):
    code: OverwatchCode
    name: OverwatchMap
    category: MapCategory
    creator_ids: list[int]
    checkpoints: Annotated[int, msgspec.Meta(gt=0)]
    difficulty: difficulties.DifficultyT
    hidden: bool = False
    raw_difficulty: Optional[Annotated[float, msgspec.Meta(gt=0, lt=10)]] = None
    archived: bool = False
    mechanics: list[Mechanics] = []
    restrictions: list[Restrictions] = []
    description: Optional[str] = None
    gold: Optional[float] = None
    silver: Optional[float] = None
    bronze: Optional[float] = None
    map_banner: str = ""

    def __post_init__(self) -> None:
        """Validate extra fields."""
        if self.raw_difficulty is None:
            self.raw_difficulty = difficulties.DIFFICULTY_MIDPOINTS[self.difficulty]
        _map = re.sub(r"[^a-zA-Z0-9]", "", self.name)
        sanitized_name = _map.lower().strip().replace(" ", "")
        self.map_banner = f"https://bkan0n.com/assets/images/map_banners/{sanitized_name}.png"

    @property
    def primary_creator_id(self) -> int:
        """Get the primary creator.

        It will always be the first index in self.creator_ids.
        """
        return self.creator_ids[0]

    @property
    def medals(self) -> bool:
        """Get the truthy value of medals."""
        return all((self.gold, self.silver, self.bronze))


class PlaytestMetaSubmission(msgspec.Struct):
    thread_id: int
    initial_difficulty: difficulties.DifficultyT
    map_id: Optional[int] = None
    code: Optional[OverwatchCode] = None

    def __post_init__(self) -> None:
        """Validate additional fields."""
        if not (self.code or self.map_id):
            raise ValueError("map_id or code must be provided.")


class MessageQueueCreatePlaytest(msgspec.Struct):
    map_id: int


class PartialPlaytestResponse(msgspec.Struct, kw_only=True):
    map_id: int
    code: OverwatchCode
    difficulty: difficulties.DifficultyT
    creator_name: str
    name: OverwatchMap
    checkpoints: int

    @property
    def thread_name(self) -> str:
        """Return the thread name."""
        return f"{self.code} | {self.difficulty} {self.name} by {self.creator_name}"[:100]


class MapResponse(BaseMap, kw_only=True):
    id: int
    official: bool
    playtesting: PlaytestStatus
    created_at: datetime.datetime
    updated_at: datetime.datetime
    creator_is_primary_flags: list[bool]
    creator_names: list[str]
    guide_urls: list[str] | None = None
    thread_id: int
    ratings: float | None
    playtest_vote_average: float | None
    playtest_vote_count: int | None
    playtest_voters: list[int] | None
    verification_id: int | None
    initial_difficulty: float
    playtest_created_at: datetime.datetime
    playtest_updated_at: datetime.datetime
    playtest_completed: bool


class PlaytestVote(msgspec.Struct):
    map_id: int
    difficulty: float
