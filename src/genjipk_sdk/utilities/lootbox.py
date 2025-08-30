import re


def sanitize_string(string: str | None) -> str:
    """Sanitize string."""
    if not string:
        return ""
    string = re.sub(r"[^a-zA-Z\s0-9]", "", string)
    string = string.strip().replace(" ", "_")
    return string.lower()
