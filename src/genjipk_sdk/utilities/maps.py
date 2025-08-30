import re

from genjipk_sdk.utilities.difficulties import DifficultyTop

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
