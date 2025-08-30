from typing import Literal

from msgspec import Struct

XP_TYPES = Literal["Map Submission", "Playtest", "Guide", "Completion", "Record", "World Record"]

XP_AMOUNTS: dict[XP_TYPES, int] = {
    "Map Submission": 30,
    "Playtest": 35,
    "Guide": 35,
    "Completion": 5,
    "Record": 15,
    "World Record": 50,
}


class XpGrantResult(Struct):
    """Return payload when XP is granted."""

    previous_amount: int
    new_amount: int


class XpGrant(Struct):
    amount: int


class TierChange(Struct):
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
