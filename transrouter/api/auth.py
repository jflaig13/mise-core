"""Authentication middleware for the Transrouter API.

Provides API key authentication for protecting endpoints.

API keys are loaded from environment variables:
- MISE_API_KEYS: Comma-separated list of valid API keys
- Example: MISE_API_KEYS="key1:client1,key2:client2"

Usage:
    from transrouter.api.auth import require_api_key

    @router.post("/protected")
    async def protected_endpoint(client: str = Depends(require_api_key)):
        # client contains the client name associated with the API key
        ...
"""

from __future__ import annotations

import logging
import os
from typing import Dict, Optional

from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader

log = logging.getLogger(__name__)

# Header name for API key
API_KEY_HEADER = APIKeyHeader(name="X-API-Key", auto_error=False)


def load_api_keys() -> Dict[str, str]:
    """Load API keys from environment variable.

    Format: MISE_API_KEYS="key1:client1,key2:client2"

    Returns:
        Dict mapping API key → client name
    """
    keys_str = os.getenv("MISE_API_KEYS", "")
    if not keys_str:
        log.warning("No API keys configured (MISE_API_KEYS not set)")
        return {}

    keys = {}
    for entry in keys_str.split(","):
        entry = entry.strip()
        if ":" in entry:
            key, client = entry.split(":", 1)
            keys[key.strip()] = client.strip()
        elif entry:
            # Key without client name - use "default"
            keys[entry] = "default"

    log.info("Loaded %d API keys", len(keys))
    return keys


# Cache loaded keys (reload on startup)
_api_keys: Optional[Dict[str, str]] = None


def get_api_keys() -> Dict[str, str]:
    """Get API keys, loading from env if not cached."""
    global _api_keys
    if _api_keys is None:
        _api_keys = load_api_keys()
    return _api_keys


def reload_api_keys() -> Dict[str, str]:
    """Force reload API keys from environment."""
    global _api_keys
    _api_keys = load_api_keys()
    return _api_keys


async def require_api_key(
    api_key: Optional[str] = Security(API_KEY_HEADER),
) -> str:
    """Dependency that requires a valid API key.

    Args:
        api_key: The API key from the X-API-Key header

    Returns:
        The client name associated with the API key

    Raises:
        HTTPException: 401 if no key provided, 403 if key invalid
    """
    if api_key is None:
        log.warning("Request missing API key")
        raise HTTPException(
            status_code=401,
            detail="Missing API key. Include 'X-API-Key' header.",
        )

    keys = get_api_keys()

    # Check for development mode (no keys configured)
    if not keys:
        log.warning("No API keys configured - allowing request in dev mode")
        return "dev-mode"

    if api_key not in keys:
        log.warning("Invalid API key attempted: %s...", api_key[:8] if len(api_key) > 8 else "***")
        raise HTTPException(
            status_code=403,
            detail="Invalid API key.",
        )

    client = keys[api_key]
    log.debug("Authenticated request from client: %s", client)
    return client


async def optional_api_key(
    api_key: Optional[str] = Security(API_KEY_HEADER),
) -> Optional[str]:
    """Dependency that accepts optional API key.

    Returns client name if valid key provided, None otherwise.
    Does not raise exceptions for missing/invalid keys.
    """
    if api_key is None:
        return None

    keys = get_api_keys()
    return keys.get(api_key)
