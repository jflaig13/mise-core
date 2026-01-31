"""Domain routing for the Transrouter.

Maps classified intents + extracted entities to the correct downstream workflow
adapter (payroll, inventory for v1).

The router dispatches requests to domain agents, which use Claude to parse
and process the input according to their workflow specs loaded from the brain.
"""

import logging
from typing import Any, Callable, Dict

from .schemas import RouterResponse
from .agents import handle_payroll_request, handle_inventory_request

log = logging.getLogger(__name__)


DEFAULT_AGENT_REGISTRY: Dict[str, Callable[[Dict[str, Any]], Dict[str, Any]]] = {
    "payroll": handle_payroll_request,
    "inventory": handle_inventory_request,
}


def route_request(
    domain_agent: str,
    intent_type: str,
    entities: Dict[str, Any],
    meta: Dict[str, Any],
    agent_registry: Dict[str, Callable[[Dict[str, Any]], Dict[str, Any]]] | None = None,
) -> RouterResponse:
    """Dispatch to the appropriate domain handler and return a RouterResponse.

    Args:
        domain_agent: The domain to route to (e.g., "payroll", "inventory").
        intent_type: The classified intent type.
        entities: Extracted entities from the input.
        meta: Metadata including transcript and other context.
        agent_registry: Optional override for agent registry (for testing).

    Returns:
        RouterResponse with the agent's output or error.
    """
    registry = agent_registry or DEFAULT_AGENT_REGISTRY

    handler = registry.get(domain_agent)
    if handler is None:
        log.error("Unknown domain agent: %s", domain_agent)
        return RouterResponse(
            domain=domain_agent,
            intent=intent_type,
            entities=entities,
            payload=None,
            errors=[f"Unknown domain agent: {domain_agent}"],
        )

    log.info("Routing to %s agent (intent=%s)", domain_agent, intent_type)

    request_payload = {"intent_type": intent_type, "entities": entities, "meta": meta}
    try:
        agent_response = handler(request_payload)
    except Exception as exc:
        log.exception("Agent '%s' failed with exception", domain_agent)
        return RouterResponse(
            domain=domain_agent,
            intent=intent_type,
            entities=entities,
            payload=None,
            errors=[f"Agent '{domain_agent}' failed: {exc}"],
        )

    # Check if agent returned an error status
    if agent_response.get("status") == "error":
        log.warning("Agent '%s' returned error: %s", domain_agent, agent_response.get("error"))

    return RouterResponse(
        domain=domain_agent,
        intent=intent_type,
        entities=entities,
        payload=agent_response,
        errors=[],
    )
