"""Compatibility shim for the parse-only endpoint.

The new home for this router is ``engine.parse_shift``. Keeping this import path
alive avoids breaking existing callers while the migration is underway.
"""

from .parse_shift import *  # noqa: F401,F403
