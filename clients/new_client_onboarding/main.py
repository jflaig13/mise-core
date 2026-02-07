"""Mise Onboarding Web Form — FastAPI micro-service."""

import base64
import json
import logging
import os
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

log = logging.getLogger(__name__)
app = FastAPI(title="Mise Onboarding")

BASE_DIR = Path(__file__).parent
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")


@app.get("/", response_class=HTMLResponse)
async def onboarding_form(request: Request):
    return templates.TemplateResponse("onboarding.html", {"request": request})


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/submit")
async def submit_form(request: Request):
    try:
        data = await request.json()
    except Exception:
        return JSONResponse({"error": "Invalid JSON"}, status_code=400)

    business_name = data.get("restaurant", {}).get("restaurant_name", "Unknown Business")

    # Build human-readable email summary
    summary = format_email_summary(data)

    # Send via SendGrid
    ok = send_onboarding_email(
        subject=f"New Onboarding: {business_name}",
        body=summary,
        json_data=data,
        business_name=business_name,
    )

    if ok:
        return {"status": "ok"}
    else:
        return JSONResponse({"error": "Failed to send email"}, status_code=500)


def format_email_summary(data: dict) -> str:
    r = data.get("restaurant", {})
    t = data.get("team", {})
    s = data.get("shifts", {})
    tip = data.get("tip_rules", {})
    pp = data.get("pay_period", {})

    lines = [
        "=" * 50,
        f"NEW CLIENT ONBOARDING: {r.get('restaurant_name', 'N/A')}",
        "=" * 50,
        "",
        "ABOUT THE BUSINESS",
        f"  Name:     {r.get('restaurant_name', '')}",
        f"  Address:  {r.get('location', '')}",
        f"  Days:     {r.get('days_open', '')}",
        f"  Contact:  {r.get('contact', {}).get('name', '')}",
        f"  Phone:    {r.get('contact', {}).get('phone', '')}",
        f"  Email:    {r.get('contact', {}).get('email', '')}",
        f"  Pay:      {pp.get('starts_on', '')} - {pp.get('ends_on', '')}",
        "",
        "TEAM",
        f"  Servers: {len(t.get('servers', []))}",
    ]
    for sv in t.get("servers", []):
        nick = f" ({sv['nickname']})" if sv.get("nickname") else ""
        lines.append(f"    - {sv.get('full_name', '')}{nick}")

    roles = t.get("support_roles", [])
    if roles:
        lines.append(f"  Support Roles: {len(roles)}")
        for role in roles:
            lines.append(f"    - {role.get('name', '')} @ {role.get('tipout_pct', '?')}%")

    staff = t.get("support_staff", [])
    if staff:
        lines.append(f"  Support Staff: {len(staff)}")
        for s_ in staff:
            lines.append(f"    - {s_.get('full_name', '')} ({s_.get('typical_role', '')})")

    kitchen = t.get("kitchen_staff", [])
    if kitchen:
        lines.append(f"  Kitchen Staff: {len(kitchen)}")
        for k in kitchen:
            lines.append(f"    - {k.get('full_name', '')}")

    recorders = t.get("recorders", [])
    if recorders:
        lines.append(f"  Recorders: {len(recorders)}")
        for rec in recorders:
            contact_info = []
            if rec.get('phone'):
                contact_info.append(rec.get('phone'))
            if rec.get('email'):
                contact_info.append(rec.get('email'))
            contact_str = f" — {', '.join(contact_info)}" if contact_info else ""
            lines.append(f"    - {rec.get('name', '')} ({rec.get('role', '')}){contact_str}")

    lines.extend([
        "",
        "SHIFTS",
        f"  AM: {s.get('am', {}).get('start', '')} - {s.get('am', {}).get('end', '')}",
        f"  PM: {s.get('pm', {}).get('start', '')} - {s.get('pm', {}).get('end', '')}",
    ])
    if s.get("close_varies_by_day"):
        lines.append("  Close times vary by day:")
        for day, time in s.get("close_times", {}).items():
            if time:
                lines.append(f"    {day.capitalize()}: {time}")

    tipout_flow_display = tip.get('tipout_flow', 'N/A')
    if tipout_flow_display == 'servers_to_support':
        tipout_flow_display = 'Servers tip out support'
    elif tipout_flow_display == 'pool_to_support':
        tipout_flow_display = 'Tip pool tips out support'
    elif tipout_flow_display == 'house_handles':
        tipout_flow_display = 'House handles all tipouts'
    elif tipout_flow_display == 'other':
        tipout_flow_display = f"Other: {tip.get('tipout_flow_other_description', '')}"

    lines.extend([
        "",
        "TIP RULES",
        f"  Pooling: {tip.get('tip_pooling', 'N/A')}",
        f"  Who tips out whom: {tipout_flow_display}",
        f"  Tipout method: {tip.get('tipout_method', 'N/A')}",
        f"  Unequal hours (servers): {tip.get('pool_unequal_hours', 'N/A')}",
        f"  Unequal hours (support): {tip.get('support_tipout_unequal_hours', 'N/A')}",
    ])
    if tip.get("notes"):
        lines.append(f"  Notes: {tip['notes']}")

    # Seasonality
    seas = data.get("seasonality", {})
    if seas.get("is_seasonal"):
        lines.extend([
            "",
            "SEASONALITY",
            f"  Busy months: {seas.get('busy_months', 'N/A')}",
            f"  Slow months: {seas.get('slow_months', 'N/A')}",
            f"  Impact level: {seas.get('seasonal_impact', 'N/A')}",
        ])
        if seas.get("hours_change_seasonally"):
            lines.append(f"  Hours change: Yes — {seas.get('hours_change_details', '')}")
        else:
            lines.append("  Hours change: No")
        if seas.get("staffing_changes_seasonally"):
            lines.append(f"  Staffing changes: Yes — {seas.get('staffing_change_details', '')}")
        else:
            lines.append("  Staffing changes: No")
    else:
        lines.extend(["", "SEASONALITY", "  Not a seasonal market"])

    lines.extend([
        "",
        "-" * 50,
        "Full JSON data attached.",
        "Sent from Mise Onboarding (onboard.getmise.io)",
    ])
    return "\n".join(lines)


def send_onboarding_email(subject: str, body: str, json_data: dict, business_name: str) -> bool:
    try:
        from sendgrid import SendGridAPIClient
        from sendgrid.helpers.mail import (
            Mail, Attachment, FileContent, FileName, FileType, Disposition,
        )

        api_key = os.environ.get("SENDGRID_API_KEY")
        if not api_key:
            log.warning("SENDGRID_API_KEY not set — email not sent")
            # In dev, just log the data
            log.info(f"Would send:\n{body}")
            return True  # Return True so the form still shows success locally

        message = Mail(
            from_email="hello@getmise.io",
            to_emails="jon@getmise.io",
            subject=subject,
            plain_text_content=body,
        )

        # Attach JSON
        safe_name = business_name.replace(" ", "_").replace("/", "-")
        json_bytes = json.dumps(json_data, indent=2).encode()
        encoded = base64.b64encode(json_bytes).decode()
        attachment = Attachment(
            FileContent(encoded),
            FileName(f"{safe_name}_onboarding.json"),
            FileType("application/json"),
            Disposition("attachment"),
        )
        message.attachment = attachment

        sg = SendGridAPIClient(api_key)
        response = sg.send(message)
        log.info(f"Onboarding email sent. Status: {response.status_code}")
        return True

    except Exception as e:
        log.error(f"Failed to send onboarding email: {e}")
        return False
