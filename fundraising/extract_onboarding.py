#!/usr/bin/env python3
"""
Extract filled onboarding form data from a fillable PDF into structured JSON.

Usage:
    python extract_onboarding.py <filled_pdf_path> [output_json_path]

Example:
    python extract_onboarding.py SoWalHouse_Onboarding_Filled.pdf
    → outputs SoWalHouse_Onboarding_Filled.json

The JSON output can then be read by Claude Code to auto-configure:
- auth.py (user account)
- metadata.json (restaurant config)
- employee_roster.json (name aliases)
- shift/tip rules
"""

import sys
import json
from pathlib import Path
from pypdf import PdfReader


def extract_form_fields(pdf_path: str) -> dict:
    """Extract all form field values from a filled PDF."""
    reader = PdfReader(pdf_path)
    fields = reader.get_fields()

    if not fields:
        print("Warning: No form fields found. Is this the fillable version?")
        return {}

    raw = {}
    for name, field in fields.items():
        value = field.get("/V", "")
        if value:
            # Clean up reportlab field values
            if isinstance(value, str):
                raw[name] = value.strip()
            else:
                raw[name] = str(value)
        else:
            raw[name] = ""

    return raw


def structure_data(raw: dict) -> dict:
    """Organize raw field data into structured restaurant config."""

    # Restaurant basics
    restaurant = {
        "restaurant_name": raw.get("restaurant_name", ""),
        "location": raw.get("location", ""),
        "days_open": raw.get("days_open", ""),
        "contact": {
            "name": raw.get("contact_name", ""),
            "phone": raw.get("contact_phone", ""),
            "email": raw.get("contact_email", ""),
        }
    }

    # Servers
    servers = []
    for i in range(1, 11):
        name = raw.get(f"server_{i}_full_name", "")
        if name:
            servers.append({
                "full_name": name,
                "nickname": raw.get(f"server_{i}_nickname", ""),
                "toast_employee_id": raw.get(f"server_{i}_toast_employee_id", ""),
            })

    # Support role names (custom) with tipout percentages
    support_roles = []
    for i in range(1, 6):
        rn = raw.get(f"support_role_{i}_name", "")
        if rn:
            support_roles.append({
                "name": rn,
                "tipout_pct": raw.get(f"support_role_{i}_tipout_pct", ""),
            })

    # Support staff
    support_staff = []
    for i in range(1, 9):
        name = raw.get(f"support_{i}_full_name", "")
        if name:
            support_staff.append({
                "full_name": name,
                "nickname": raw.get(f"support_{i}_nickname", ""),
                "toast_id": raw.get(f"support_{i}_toast_id", ""),
                "typical_role": raw.get(f"support_{i}_typical_role", ""),
            })

    # Kitchen staff
    kitchen_staff = []
    for i in range(1, 6):
        name = raw.get(f"kitchen_{i}_full_name", "")
        if name:
            kitchen_staff.append({
                "full_name": name,
                "nickname": raw.get(f"kitchen_{i}_nickname", ""),
                "toast_id": raw.get(f"kitchen_{i}_toast_id", ""),
            })

    # Recorders
    recorders = []
    for i in range(1, 4):
        name = raw.get(f"recorder_{i}_name", "")
        if name:
            recorders.append({
                "name": name,
                "role": raw.get(f"recorder_{i}_role", ""),
            })

    # Shifts
    shifts = {
        "am": {
            "start": raw.get("shift_am_start", ""),
            "end": raw.get("shift_am_end", ""),
        },
        "pm": {
            "start": raw.get("shift_pm_start", ""),
            "end": raw.get("shift_pm_end", ""),
        },
        "close_varies_by_day": raw.get("close_varies", "") == "/Yes",
        "close_times": {}
    }
    for day in ["sun", "mon", "tue", "wed", "thu", "fri", "sat"]:
        val = raw.get(f"close_{day}", "")
        if val:
            shifts["close_times"][day] = val

    # Tip rules
    tip_pool = "unknown"
    if raw.get("tip_pool", "") == "/Yes":
        tip_pool = "pool"
    elif raw.get("tip_individual", "") == "/Yes":
        tip_pool = "individual"
    elif raw.get("tip_other", "") == "/Yes":
        tip_pool = "other"

    # Tipout calculation method
    tipout_method = "unknown"
    if raw.get("tipout_total_sales", "") == "/Yes":
        tipout_method = "total_sales"
    elif raw.get("tipout_food_sales", "") == "/Yes":
        tipout_method = "food_sales"
    elif raw.get("tipout_other_metric", "") == "/Yes":
        tipout_method = "other_metric"
    elif raw.get("tipout_method_other", "") == "/Yes":
        tipout_method = "other"

    # Unequal hours — servers
    pool_hours = "unknown"
    if raw.get("pool_equal_split", "") == "/Yes":
        pool_hours = "equal_split"
    elif raw.get("pool_pro_rate", "") == "/Yes":
        pool_hours = "pro_rate"
    elif raw.get("pool_hours_other", "") == "/Yes":
        pool_hours = "other"

    # Unequal hours — support staff
    support_tipout_hours = "unknown"
    if raw.get("support_tipout_full", "") == "/Yes":
        support_tipout_hours = "full_tipout"
    elif raw.get("support_tipout_pro_rate", "") == "/Yes":
        support_tipout_hours = "pro_rate"
    elif raw.get("support_tipout_hours_other", "") == "/Yes":
        support_tipout_hours = "other"

    tip_rules = {
        "tip_pooling": tip_pool,
        "tip_other_description": raw.get("tip_other_desc", ""),
        "pool_unequal_hours": pool_hours,
        "pool_unequal_hours_other": raw.get("pool_hours_other_desc", ""),
        "support_tipout_unequal_hours": support_tipout_hours,
        "support_tipout_unequal_hours_other": raw.get("support_tipout_hours_other_desc", ""),
        "tipout_method": tipout_method,
        "tipout_other_metric_description": raw.get("tipout_other_metric_desc", ""),
        "tipout_method_other_description": raw.get("tipout_method_other_desc", ""),
        "notes": raw.get("tip_notes", ""),
    }

    # Pay period
    pay_period = {
        "starts_on": raw.get("pay_start", ""),
        "ends_on": raw.get("pay_end", ""),
    }

    return {
        "restaurant": restaurant,
        "team": {
            "servers": servers,
            "support_roles": support_roles,
            "support_staff": support_staff,
            "kitchen_staff": kitchen_staff,
            "recorders": recorders,
        },
        "shifts": shifts,
        "tip_rules": tip_rules,
        "pay_period": pay_period,
        "_raw_fields": raw,  # Include raw data for debugging
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: python extract_onboarding.py <filled_pdf_path> [output_json_path]")
        sys.exit(1)

    pdf_path = Path(sys.argv[1])
    if not pdf_path.exists():
        print(f"Error: {pdf_path} not found")
        sys.exit(1)

    # Default output path
    if len(sys.argv) >= 3:
        output_path = Path(sys.argv[2])
    else:
        output_path = pdf_path.with_suffix(".json")

    print(f"Extracting form data from: {pdf_path}")
    raw = extract_form_fields(str(pdf_path))

    if not raw:
        print("No data found. Exiting.")
        sys.exit(1)

    print(f"Found {len(raw)} fields")
    structured = structure_data(raw)

    # Write JSON
    with open(output_path, "w") as f:
        json.dump(structured, f, indent=2)

    print(f"Saved structured data to: {output_path}")
    print()

    # Summary
    r = structured["restaurant"]
    t = structured["team"]
    print(f"Restaurant: {r['restaurant_name']} ({r['location']})")
    print(f"Servers: {len(t['servers'])}")
    print(f"Support staff: {len(t['support_staff'])}")
    print(f"Kitchen staff: {len(t['kitchen_staff'])}")
    print(f"Tip pooling: {structured['tip_rules']['tip_pooling']}")
    print(f"Tipout method: {structured['tip_rules']['tipout_method']}")
    print(f"Pay period: {structured['pay_period']['starts_on']} - {structured['pay_period']['ends_on']}")


if __name__ == "__main__":
    main()
