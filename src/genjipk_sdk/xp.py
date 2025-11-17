from typing import Literal

from msgspec import Struct

__all__ = (
    "XP_AMOUNTS",
    "XP_TYPES",
    "PlayersPerSkillTierResponse",
    "PlayersPerXPTierResponse",
    "TierChangeResponse",
    "XpGrantEvent",
    "XpGrantRequest",
    "XpGrantResponse",
)

XP_TYPES = Literal["Map Submission", "Playtest", "Guide", "Completion", "Record", "World Record", "Other"]

XP_AMOUNTS: dict[XP_TYPES, int] = {
    "Map Submission": 30,
    "Playtest": 35,
    "Guide": 35,
    "Completion": 5,
    "Record": 15,
    "World Record": 50,
}


class XpGrantResponse(Struct):
    """Return payload when XP is granted."""

    previous_amount: int
    new_amount: int


class XpGrantRequest(Struct):
    amount: int
    type: XP_TYPES


class TierChangeResponse(Struct):
    """Computed tier deltas between old and new XP."""

    old_xp: int
    new_xp: int
    old_main_tier_name: str
    new_main_tier_name: str
    old_sub_tier_name: str
    new_sub_tier_name: str
    old_prestige_level: int
    new_prestige_level: int
    # "Main Tier Rank Up" | "Sub-Tier Rank Up" | None
    rank_change_type: str | None
    prestige_change: bool


class PlayersPerXPTierResponse(Struct):
    tier: str
    amount: int


class PlayersPerSkillTierResponse(Struct):
    tier: str
    amount: int


class XpGrantEvent(Struct):
    user_id: int
    amount: int
    type: XP_TYPES
    previous_amount: int
    new_amount: int
