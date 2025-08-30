from typing import Literal

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
]
