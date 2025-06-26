import enum
from typing import Literal

from msgspec import Struct


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
