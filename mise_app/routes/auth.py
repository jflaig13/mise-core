"""Authentication routes."""
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse

router = APIRouter()

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request, error: str = None):
    """Render login page."""
    templates = request.app.state.templates
    return templates.TemplateResponse(
        "login.html",
        {"request": request, "error": error}
    )

@router.post("/login")
async def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...)
):
    """Process login."""
    from mise_app.auth import verify_credentials

    user = verify_credentials(username, password)
    if user:
        request.session["authenticated"] = True
        request.session["username"] = username.lower()
        request.session["name"] = user["name"]
        request.session["restaurant_id"] = user.get("restaurant_id", username.lower())
        request.session["restaurant_name"] = user["name"]
        request.session["location"] = user.get("location", "")
        return RedirectResponse("/", status_code=302)

    return RedirectResponse("/login?error=invalid", status_code=302)

@router.get("/logout")
async def logout(request: Request):
    """Clear session and redirect to login."""
    request.session.clear()
    return RedirectResponse("/login", status_code=302)
