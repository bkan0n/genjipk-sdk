from genjipk_sdk.utilities.difficulties import DifficultyT

PLAYTEST_VOTE_THRESHOLD: dict[DifficultyT, int] = {
    "Easy": 5,
    "Medium": 5,
    "Hard": 5,
    "Very Hard": 3,
    "Extreme": 2,
    "Hell": 1,
}
