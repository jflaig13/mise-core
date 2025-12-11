"""Domain routing stub for the Transrouter.

Maps classified intents + extracted entities to the correct downstream workflow
adapter (payroll, inventory for v1).
"""

from typing import Any, Callable, Dict
from .schemas import RouterResponse


def _payroll_agent(request: Dict[str, Any]) -> Dict[str, Any]:
    return {"agent": "payroll", "status": "not_implemented", "request": request}


def _inventory_agent(request: Dict[str, Any]) -> Dict[str, Any]:
    return {"agent": "inventory", "status": "not_implemented", "request": request}


DEFAULT_AGENT_REGISTRY: Dict[str, Callable[[Dict[str, Any]], Dict[str, Any]]] = {
    "payroll": _payroll_agent,
    "inventory": _inventory_agent,
}


def route_request(
    domain_agent: str,
    intent_type: str,
    entities: Dict[str, Any],
    meta: Dict[str, Any],
    agent_registry: Dict[str, Callable[[Dict[str, Any]], Dict[str, Any]]] = DEFAULT_AGENT_REGISTRY,
) -> RouterResponse:
    """Dispatch to the appropriate domain handler and return a RouterResponse."""
    handler = agent_registry.get(domain_agent)
    if handler is None:
        return RouterResponse(
            domain=domain_agent,
            intent=intent_type,
            entities=entities,
            payload=None,
            errors=[f"Unknown domain agent: {domain_agent}"],
        )

    request_payload = {"intent_type": intent_type, "entities": entities, "meta": meta}
    try:
        agent_response = handler(request_payload)
    except Exception as exc:  # pragma: no cover - defensive
        return RouterResponse(
            domain=domain_agent,
            intent=intent_type,
            entities=entities,
            payload=None,
            errors=[f"Agent '{domain_agent}' failed: {exc}"],
        )

    return RouterResponse(domain=domain_agent, intent=intent_type, entities=entities, payload=agent_response, errors=[])
