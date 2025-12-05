"""Compatibility shim to keep ``engine.app`` import working.

The main FastAPI app lives in ``engine.payroll_engine``. This wrapper keeps
older imports and tests functioning while delegating everything to the
payroll module.
"""

from .payroll_engine import *  # noqa: F401,F403
