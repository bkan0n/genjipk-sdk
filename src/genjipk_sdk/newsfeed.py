from __future__ import annotations

import datetime as dt
from typing import Literal

import msgspec

from .maps import get_map_banner

NewsfeedEventType = Literal[
    "new_map",
    "record",
    "archive",
    "unarchive",
    "bulk_archive",
    "bulk_unarchive",
    "guide",
    "legacy_record",
    "map_edit",
    "role",
    "announcement",
    "linked_map",
    "unlinked_map",
]


# Scalars for map_edit diffs, etc.
NewsfeedScalar = str | int | float | bool | None


# ---- Tagged base for all payload variants ----
class _TaggedPayload(msgspec.Struct, tag_field="type"):
    """All payloads inherit this so they're tagged with field 'type'."""


# ---- Payload variants (NOTE: no normal 'type' attributes!) ----


class NewsfeedRecord(_TaggedPayload, tag="record", kw_only=True):
    code: OverwatchCode
    map_name: OverwatchMap
    time: float
    video: GuideURL
    rank_num: int
    name: str
    medal: MedalType | None
    difficulty: DifficultyAll


class NewsfeedNewMap(_TaggedPayload, tag="new_map", kw_only=True):
    code: OverwatchCode
    map_name: OverwatchMap
    difficulty: DifficultyAll
    creators: list[str]
    title: str | None = None
    banner_url: str | None = None
    official: bool = True

    def __post_init__(self) -> None:
        """Set the map banner dynamically."""
        if not self.banner_url:
            self.banner_url = get_map_banner(self.map_name)


class NewsfeedArchive(_TaggedPayload, tag="archive", kw_only=True):
    code: OverwatchCode
    map_name: OverwatchMap
    creators: list[str]
    difficulty: DifficultyAll
    reason: str


class NewsfeedUnarchive(_TaggedPayload, tag="unarchive", kw_only=True):
    code: OverwatchCode
    map_name: OverwatchMap
    creators: list[str]
    difficulty: DifficultyAll
    reason: str


class NewsfeedBulkArchive(_TaggedPayload, tag="bulk_archive", kw_only=True):
    codes: list[OverwatchCode]
    reason: str


class NewsfeedBulkUnarchive(_TaggedPayload, tag="bulk_unarchive", kw_only=True):
    codes: list[OverwatchCode]
    reason: str


class NewsfeedGuide(_TaggedPayload, tag="guide", kw_only=True):
    code: OverwatchCode
    guide_url: GuideURL
    name: str


class NewsfeedLegacyRecord(_TaggedPayload, tag="legacy_record", kw_only=True):
    code: OverwatchCode
    affected_count: int
    reason: str


class NewsfeedFieldChange(msgspec.Struct, kw_only=True):
    field: str
    old: NewsfeedScalar
    new: NewsfeedScalar


class NewsfeedMapEdit(_TaggedPayload, tag="map_edit", kw_only=True):
    code: OverwatchCode
    changes: list[NewsfeedFieldChange]
    reason: str


class NewsfeedRole(_TaggedPayload, tag="role", kw_only=True):
    user_id: int
    name: str
    added: list[str]


class NewsfeedAnnouncement(_TaggedPayload, tag="announcement", kw_only=True):
    title: str
    content: str
    url: str | None
    banner_url: GuideURL | None
    thumbnail_url: GuideURL | None
    from_discord: bool


class NewsfeedLinkedMap(_TaggedPayload, tag="linked_map", kw_only=True):
    official_code: OverwatchCode
    unofficial_code: OverwatchCode
    playtest_id: int | None = None


class NewsfeedUnlinkedMap(_TaggedPayload, tag="unlinked_map", kw_only=True):
    official_code: OverwatchCode
    unofficial_code: OverwatchCode
    reason: str


NewsfeedPayload = (
    NewsfeedRecord
    | NewsfeedNewMap
    | NewsfeedArchive
    | NewsfeedUnarchive
    | NewsfeedBulkArchive
    | NewsfeedBulkUnarchive
    | NewsfeedGuide
    | NewsfeedLegacyRecord
    | NewsfeedMapEdit
    | NewsfeedRole
    | NewsfeedAnnouncement
    | NewsfeedLinkedMap
    | NewsfeedUnlinkedMap
)


class NewsfeedEvent(msgspec.Struct, kw_only=True):
    id: int | None
    timestamp: dt.datetime
    payload: NewsfeedPayload
    event_type: NewsfeedEventType | None = None
    total_results: int | None = None


class NewsfeedQueueMessage(msgspec.Struct, kw_only=True):
    newsfeed_id: int
