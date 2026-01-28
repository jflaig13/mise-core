"""Middleware for injecting restaurant context into requests."""
from starlette.middleware.base import BaseHTTPMiddleware
from mise_app.tenant import get_restaurant_config


class RestaurantContextMiddleware(BaseHTTPMiddleware):
    """Inject restaurant context into all authenticated requests."""

    async def dispatch(self, request, call_next):
        # Extract from session
        restaurant_id = request.session.get("restaurant_id")
        restaurant_name = request.session.get("restaurant_name")

        # Attach to request state
        request.state.restaurant_id = restaurant_id
        request.state.restaurant_name = restaurant_name

        # Load config (cached)
        if restaurant_id:
            request.state.restaurant_config = get_restaurant_config(restaurant_id)
        else:
            request.state.restaurant_config = {}

        response = await call_next(request)
        return response
