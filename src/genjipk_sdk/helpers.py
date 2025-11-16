# src/genjipk_sdk/helpers.py
import re


def sanitize_string(string: str | None) -> str:
    """Sanitize a string for use in asset paths / URLs."""
    if not string:
        return ""
    string = re.sub(r"[^a-zA-Z0-9\s]", "", string)
    string = string.strip().replace(" ", "_")
    return string.lower()
