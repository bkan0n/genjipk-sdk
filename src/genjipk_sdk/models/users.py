import enum
import re
from typing import Literal

from msgspec import Struct

from genjipk_sdk.utilities.difficulties import DifficultyTop


class Notification(enum.IntFlag):
    NONE = 0
    DM_ON_VERIFICATION = enum.auto()
    DM_ON_SKILL_ROLE_UPDATE = enum.auto()
    DM_ON_LOOTBOX_GAIN = enum.auto()
    DM_ON_RECORDS_REMOVAL = enum.auto()
    DM_ON_PLAYTEST_ALERTS = enum.auto()
    PING_ON_XP_GAIN = enum.auto()
    PING_ON_MASTERY = enum.auto()
    PING_ON_COMMUNITY_RANK_UPDATE = enum.auto()


NOTIFICATION_TYPES = Literal[
    "NONE",
    "DM_ON_VERIFICATION",
    "DM_ON_SKILL_ROLE_UPDATE",
    "DM_ON_LOOTBOX_GAIN",
    "DM_ON_RECORDS_REMOVAL",
    "DM_ON_PLAYTEST_ALERTS",
    "PING_ON_XP_GAIN",
    "PING_ON_MASTERY",
    "PING_ON_COMMUNITY_RANK_UPDATE",
]


class SettingsUpdate(Struct):
    notifications: list[NOTIFICATION_TYPES]

    def __post_init__(self) -> None:
        """Post-initialization processing to validate notification names."""
        valid_names = {flag.name for flag in Notification if flag.name is not None}
        for name in self.notifications:
            if name not in valid_names:
                raise ValueError(f"Invalid notification type: {name}. Valid types: {', '.join(valid_names)}")

    def to_bitmask(self) -> int:
        """Convert the list of notification names to a bitmask."""
        mask = Notification(0)
        for name in self.notifications:
            if name == "NONE":
                return 0
            mask |= Notification[name]
        return mask.value


class Creator(Struct):
    id: int
    is_primary: bool


class CreatorFull(Creator):
    name: str


USERNAME_REGEX = re.compile(
    r"^(?P<name>[A-Za-z\u00C0-\u00D6\u00D8-\u00F6\u00F8-\u017E\u0180-\u0188\u0190-\u0198\u01C0-\u0217]"
    r"[A-Za-z0-9\u00C0-\u00D6\u00D8-\u00F6\u00F8-\u017E\u0180-\u0188\u0190-\u0198\u01C0-\u0217]{2,11})"
    r"(?:\#(?P<tag>\d+))?$"
)


class UserReadDTO(Struct):
    id: int
    global_name: str
    nickname: str
    overwatch_usernames: list[str] | None
    coalesced_name: str | None = None
    coins: int = 0


class UserCreateDTO(Struct):
    id: int
    global_name: str
    nickname: str


class OverwatchUsernameItem(Struct):
    username: str
    is_primary: bool = False

    def __post_init__(self) -> None:
        """Post-initialization processing to validate the username format."""
        if not USERNAME_REGEX.match(self.username):
            raise ValueError(
                f"Invalid Overwatch username format: '{self.username}'. "
                "Expected format like 'nebula#11571' or 'nebula'."
            )


class OverwatchUsernamesUpdate(Struct):  # TODO Rework this to use primary/secondary/tertiary
    usernames: list[OverwatchUsernameItem]

    def __post_init__(self) -> None:
        """Post-initialization processing to enforce primary username constraints."""
        primary_count = sum(1 for item in self.usernames if item.is_primary)
        if primary_count > 1:
            raise ValueError("Only one Overwatch username can be primary.")
        if primary_count == 0 and self.usernames:
            raise ValueError("One Overwatch username must be designated as primary.")


class OverwatchUsernamesReadDTO(Struct):
    user_id: int
    primary: str | None
    secondary: str | None
    tertiary: str | None


class RankDetailReadDTO(Struct):
    difficulty: DifficultyTop
    completions: int
    gold: int
    silver: int
    bronze: int
    rank_met: bool
    gold_rank_met: bool
    silver_rank_met: bool
    bronze_rank_met: bool


class CommunityLeaderboardReadDTO(Struct):
    user_id: int
    nickname: str
    xp_amount: int
    raw_tier: int
    normalized_tier: int
    prestige_level: int
    tier_name: str
    wr_count: int
    map_count: int
    playtest_count: int
    discord_tag: str
    skill_rank: str
    total_results: int
