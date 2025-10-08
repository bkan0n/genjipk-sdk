import re
from typing import Annotated, Literal

import msgspec

__all__ = (
    "URL_PATTERN",
    "URL_REGEX",
    "GuideURL",
    "MapCategory",
    "Mechanics",
    "OverwatchCode",
    "OverwatchMap",
    "Restrictions",
)


URL_PATTERN = r"(https?:\/\/)([\w\-])+\.{1}([a-zA-Z]{2,63})([\/\w-]*)*\/?\??([^#\n\r]*)?#?([^\n\r]*)"
URL_REGEX = re.compile(URL_PATTERN)

OverwatchCode = Annotated[str, msgspec.Meta(min_length=4, max_length=6, pattern="^[A-Z0-9]*$")]
GuideURL = Annotated[
    str,
    msgspec.Meta(
        pattern=URL_PATTERN,
        description="Must be a valid URL starting with http:// or https://.",
    ),
]

MapCategory = Literal[
    "Classic",
    "Increasing Difficulty",
    "XP Based",
]

OverwatchMap = Literal[
    "Circuit Royal",
    "Runasapi",
    "Practice Range",
    "Route 66",
    "Midtown",
    "Junkertown",
    "Colosseo",
    "Lijiang Tower (Lunar New Year)",
    "Dorado",
    "Throne of Anubis",
    "Castillo",
    "Blizzard World (Winter)",
    "Hollywood (Halloween)",
    "King's Row",
    "Black Forest (Winter)",
    "Petra",
    "Framework",
    "Eichenwalde",
    "Workshop Island",
    "Chateau Guillard (Halloween)",
    "New Junk City",
    "Necropolis",
    "Kanezaka",
    "Havana",
    "Oasis",
    "Ayutthaya",
    "Volskaya Industries",
    "Hanamura",
    "Workshop Expanse",
    "Hanaoka",
    "Lijiang Tower",
    "Busan (Lunar New Year)",
    "Suravasa",
    "King's Row (Winter)",
    "Ecopoint: Antarctica",
    "Hanamura (Winter)",
    "Blizzard World",
    "Chateau Guillard",
    "Paraiso",
    "Workshop Green Screen",
    "Watchpoint: Gibraltar",
    "Shambali",
    "Eichenwalde (Halloween)",
    "Tools",
    "Nepal",
    "Samoa",
    "Horizon Lunar Colony",
    "Paris",
    "Esperanca",
    "Black Forest",
    "Antarctic Peninsula",
    "Workshop Chamber",
    "Hollywood",
    "New Queen Street",
    "Rialto",
    "Busan",
    "Malevento",
    "Temple of Anubis",
    "Ilios",
    "Ecopoint: Antarctica (Winter)",
    "Numbani",
    "Adlersbrunn",
    "Aatlis",
]

Mechanics = Literal[
    "Edge Climb",
    "Bhop",
    "Save Climb",
    "High Edge",
    "Distance Edge",
    "Quick Climb",
    "Slide",
    "Stall",
    "Dash",
    "Ultimate",
    "Emote Save Bhop",
    "Death Bhop",
    "Triple Jump",
    "Multi Climb",
    "Vertical Multi Climb",
    "Standing Create Bhop",
    "Crouch Edge",
    "Bhop First",
    "Create Bhop",
    "Save Double",
]

Restrictions = Literal[
    "Wall Climb",
    "Create Bhop",
    "Dash Start",
    "Death Bhop",
    "Triple Jump",
    "Multi Climb",
    "Standing Create Bhop",
    "Emote Save Bhop",
    "Double Jump",
    "Bhop",
]

PlaytestStatus = Literal["Approved", "In Progress", "Rejected"]

MedalType = Literal["Gold", "Silver", "Bronze"]
