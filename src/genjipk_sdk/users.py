import enum
from typing import Literal

from msgspec import UNSET, Struct, UnsetType

from .difficulties import DifficultyTop

__all__ = (
    "NOTIFICATION_TYPES",
    "CommunityLeaderboardResponse",
    "Creator",
    "CreatorFull",
    "Notification",
    "OverwatchUsernameItem",
    "OverwatchUsernamesResponse",
    "OverwatchUsernamesUpdateRequest",
    "RankDetailResponse",
    "SettingsUpdateRequest",
    "UserCreateRequest",
    "UserResponse",
    "UserUpdateRequest",
)


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


class SettingsUpdateRequest(Struct):
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


class UserResponse(Struct):
    id: int
    global_name: str
    nickname: str
    overwatch_usernames: list[str] | None
    coalesced_name: str | None = None
    coins: int = 0


class UserCreateRequest(Struct):
    id: int
    global_name: str
    nickname: str


class UserUpdateRequest(Struct):
    global_name: str | UnsetType = UNSET
    nickname: str | UnsetType = UNSET


class OverwatchUsernameItem(Struct):
    username: str
    is_primary: bool = False


class OverwatchUsernamesUpdateRequest(Struct):  # TODO Rework this to use primary/secondary/tertiary
    usernames: list[OverwatchUsernameItem]

    def __post_init__(self) -> None:
        """Post-initialization processing to enforce primary username constraints."""
        primary_count = sum(1 for item in self.usernames if item.is_primary)
        if primary_count > 1:
            raise ValueError("Only one Overwatch username can be primary.")
        if primary_count == 0 and self.usernames:
            raise ValueError("One Overwatch username must be designated as primary.")


class OverwatchUsernamesResponse(Struct):
    user_id: int
    primary: str | None
    secondary: str | None
    tertiary: str | None


class RankDetailResponse(Struct):
    difficulty: DifficultyTop
    completions: int
    gold: int
    silver: int
    bronze: int
    rank_met: bool
    gold_rank_met: bool
    silver_rank_met: bool
    bronze_rank_met: bool


class CommunityLeaderboardResponse(Struct):
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
