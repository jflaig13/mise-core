"""Domain agents for Mise transrouter."""

from .payroll_agent import handle_payroll_request
from .inventory_agent import handle_inventory_request

__all__ = ["handle_payroll_request", "handle_inventory_request"]
