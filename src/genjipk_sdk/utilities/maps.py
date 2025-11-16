"""Deprecated compatibility module for map helpers.

Import from :mod:`genjipk_sdk.maps` or :mod:`genjipk_sdk.types` instead.
"""
from genjipk_sdk.maps import PLAYTEST_VOTE_THRESHOLD, get_map_banner
from genjipk_sdk.types import GuideURL, MapCategory, Mechanics, MedalType, OverwatchCode, OverwatchMap, PlaytestStatus, Restrictions

__all__ = [
    "PLAYTEST_VOTE_THRESHOLD",
    "get_map_banner",
    "GuideURL",
    "MapCategory",
    "Mechanics",
    "MedalType",
    "OverwatchCode",
    "OverwatchMap",
    "PlaytestStatus",
    "Restrictions",
]
