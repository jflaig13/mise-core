"""Compatibility shim for legacy imports.

The main payroll engine now lives in ``engine.payroll_engine``. This file keeps
``engine.app`` imports working while the rest of the codebase migrates.
"""

from .payroll_engine import *  # noqa: F401,F403
