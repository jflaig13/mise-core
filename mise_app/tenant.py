"""Tenant/restaurant utilities for multi-tenancy."""
from pathlib import Path
from functools import lru_cache
import json
import logging

log = logging.getLogger(__name__)
STORAGE_DIR = Path(__file__).parent / "data"


@lru_cache(maxsize=10)
def get_restaurant_config(restaurant_id: str) -> dict:
    """Load restaurant metadata (cached)."""
    metadata_file = STORAGE_DIR / restaurant_id / "metadata.json"
    if not metadata_file.exists():
        return {
            "restaurant_id": restaurant_id,
            "name": restaurant_id.title(),
            "branding": {}
        }

    with open(metadata_file) as f:
        return json.load(f)


def require_restaurant(request) -> str:
    """Get restaurant_id from request or raise error."""
    if hasattr(request.state, "restaurant_id") and request.state.restaurant_id:
        return request.state.restaurant_id

    restaurant_id = request.session.get("restaurant_id")
    if not restaurant_id:
        raise ValueError("No restaurant context - user not authenticated")
    return restaurant_id


def get_template_context(request) -> dict:
    """Build template context with restaurant branding."""
    restaurant_id = getattr(request.state, "restaurant_id", None)
    restaurant_config = getattr(request.state, "restaurant_config", {})

    return {
        "request": request,
        "restaurant_id": restaurant_id,
        "restaurant_name": restaurant_config.get("name", "Mise"),
        "restaurant_logo": restaurant_config.get("branding", {}).get("logo_url"),
        "restaurant_colors": restaurant_config.get("branding", {}),
    }
