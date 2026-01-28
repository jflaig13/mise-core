"""Simple authentication for Mise demo."""
import bcrypt

# Pre-computed bcrypt hashes
# Generated using: bcrypt.hashpw(b"password", bcrypt.gensalt()).decode()
_MISE2026_HASH = "$2b$12$ONnO9oGhkL46OeOhjGxghegrDjAbw74ixWooWW7gjQeT78AntEy8K"
_PAPASURF2026_HASH = "$2b$12$kI66z11Ko81l5lbDsiU2AOD.ZUvfjwzSbTx4IC1OLGxhT7K2x06HK"

# User accounts with restaurant_id for multi-tenancy
DEMO_USERS = {
    "sowalhouse": {
        "password_hash": _MISE2026_HASH,
        "name": "SoWal House",
        "location": "Seaside, FL",
        "restaurant_id": "sowalhouse",
    },
    "papasurf": {
        "password_hash": _PAPASURF2026_HASH,
        "name": "Papa Surf",
        "location": "Panama City Beach, FL",
        "restaurant_id": "papasurf",
    }
}

def verify_credentials(username: str, password: str) -> dict | None:
    """Verify username/password and return user dict if valid."""
    user = DEMO_USERS.get(username.lower())
    if not user:
        return None
    if bcrypt.checkpw(password.encode(), user["password_hash"].encode()):
        return {"username": username.lower(), **user}
    return None

def get_session_user(request) -> dict | None:
    """Get current user from session."""
    if request.session.get("authenticated"):
        username = request.session.get("username")
        return DEMO_USERS.get(username)
    return None
