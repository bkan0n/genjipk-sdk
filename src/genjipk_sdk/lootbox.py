from __future__ import annotations

import datetime as dt
from typing import Literal

from msgspec import Struct

from .helpers import sanitize_string

LootboxKeyType = Literal["Classic", "Winter"]


class RewardTypeResponse(Struct):
    name: str
    key_type: LootboxKeyType
    rarity: str
    type: str
    duplicate: bool = False
    coin_amount: int = 0

    url: str | None = None

    def __post_init__(self) -> None:
        """Post init."""
        self.url = _reward_url(self.type, self.name)


class LootboxKeyTypeResponse(Struct):
    name: str


class UserRewardResponse(Struct):
    user_id: int
    earned_at: dt.datetime
    name: str
    type: str
    rarity: str
    medal: str | None

    url: str | None = None

    def __post_init__(self) -> None:
        """Post init."""
        if self.type == "mastery":
            name = sanitize_string(self.name)
            medal = sanitize_string(self.medal)
            self.url = f"assets/mastery/{name}_{medal}.webp"
        else:
            self.url = _reward_url(self.type, self.name)


def _reward_url(type_: str, name: str) -> str:
    sanitized_name = sanitize_string(name)
    if type_ == "spray":
        url = f"assets/rank_card/spray/{sanitized_name}.webp"
    elif type_ == "skin":
        url = f"assets/rank_card/avatar/{sanitized_name}/heroic.webp"
    elif type_ == "pose":
        url = f"assets/rank_card/avatar/overwatch_1/{sanitized_name}.webp"
    elif type_ == "background":
        url = f"assets/rank_card/background/{sanitized_name}.webp"
    elif type_ == "coins":
        url = f"assets/rank_card/coins/{sanitized_name}.webp"
    else:
        url = ""
    return url


class UserLootboxKeyAmountResponse(Struct):
    key_type: LootboxKeyType
    amount: int
