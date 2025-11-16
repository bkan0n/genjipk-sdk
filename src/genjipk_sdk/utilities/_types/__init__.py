"""Deprecated compatibility layer for shared types.

Import from :mod:`genjipk_sdk.types` instead.
"""
from genjipk_sdk import types
from genjipk_sdk.types import *  # noqa: F401,F403

__all__ = [*types.__all__]
