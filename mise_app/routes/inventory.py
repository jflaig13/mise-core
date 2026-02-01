"""Inventory (Shelfy) routes for Mise app.

Shelfy Lite - Demo-ready inventory recording feature.
Voice recording for inventory counts, organized by area and category.
"""

from __future__ import annotations

import logging
from datetime import datetime
from pathlib import Path
from typing import Optional

import requests
from fastapi import APIRouter, File, Form, Request, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse

from mise_app.shelfy_storage import (
    KITCHEN_AREAS,
    BAR_AREAS,
    get_shelfy_storage,
    normalize_period_id,
    generate_shelfy_id,
    get_audio_archive_path,
)
from mise_app.gcs_audio import upload_audio_to_gcs
from mise_app.tenant import require_restaurant, get_template_context

log = logging.getLogger(__name__)

router = APIRouter(prefix="/inventory", tags=["Inventory"])

# Recordings storage directory (same as payroll)
RECORDINGS_DIR = Path(__file__).parent.parent.parent / "recordings"


def save_shelfy_recording(
    audio_bytes: bytes,
    period_id: str,
    category: str,
    area: str,
    original_filename: str = None
) -> Path:
    """Archive shelfy audio recording - PERMANENT STORAGE.

    Args:
        audio_bytes: The raw audio bytes
        period_id: Inventory period ID (e.g., '2026-01-31')
        category: 'kitchen' or 'bar'
        area: Area name (e.g., 'Walk-in', 'Back Bar')
        original_filename: Original filename from upload

    Returns:
        Path to the saved file
    """
    # Create period-specific archive directory
    period_dir = RECORDINGS_DIR / period_id
    period_dir.mkdir(parents=True, exist_ok=True)

    # Determine file extension
    ext = ".webm"  # Default for browser recordings
    if original_filename:
        if original_filename.endswith(".wav"):
            ext = ".wav"
        elif original_filename.endswith(".m4a"):
            ext = ".m4a"
        elif original_filename.endswith(".mp3"):
            ext = ".mp3"

    # Build filename: {Category}_{Area}_{timestamp}{ext}
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    category_cap = category.capitalize()
    area_clean = area.replace(" ", "").replace("/", "")
    filename = f"{category_cap}_{area_clean}_{timestamp}{ext}"

    filepath = period_dir / filename
    filepath.write_bytes(audio_bytes)

    log.info(f"🗄️ ARCHIVED (local): {filepath.relative_to(RECORDINGS_DIR.parent)} ({len(audio_bytes):,} bytes)")

    # Also upload to Google Cloud Storage for permanent cloud storage
    try:
        gcs_path = upload_audio_to_gcs(
            audio_bytes, period_id, filename
        )
        if not gcs_path:
            log.warning(f"Failed to upload to GCS (continuing anyway)")
    except Exception as e:
        log.warning(f"Failed to upload to GCS (continuing anyway): {e}")

    return filepath


@router.post("/get_upload_url")
async def get_upload_url(request: Request):
    """Get a signed GCS URL for direct audio upload (for files >32MB).

    This endpoint returns a signed URL that allows direct upload to GCS,
    bypassing Cloud Run's 32MB request limit.

    Request body (JSON):
        - area: Area name
        - category: "kitchen" or "bar"
        - file_extension: ".wav", ".m4a", ".webm", etc.
        - period_id: Optional inventory period

    Response:
        - upload_url: Signed GCS URL for PUT upload
        - gcs_path: GCS path where file will be stored
        - shelfy_id: Pre-generated shelfy ID for processing
        - expires_in: Seconds until URL expires (3600)
    """
    try:
        body = await request.json()
    except Exception:
        return JSONResponse(
            {"status": "error", "error": "Invalid JSON body"},
            status_code=400
        )

    area = body.get("area")
    category = body.get("category")
    file_extension = body.get("file_extension", ".webm")
    period_id = body.get("period_id")

    if not area or not category:
        return JSONResponse(
            {"status": "error", "error": "Missing required fields: area, category"},
            status_code=400
        )

    # Validate category
    category = category.lower()
    if category not in ("kitchen", "bar"):
        return JSONResponse(
            {"status": "error", "error": f"Invalid category: {category}"},
            status_code=400
        )

    # Normalize period_id if not provided
    if not period_id:
        period_id = normalize_period_id()

    # Generate shelfy ID and GCS path
    shelfy_id = generate_shelfy_id(area)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    category_cap = category.capitalize()
    area_clean = area.replace(" ", "").replace("/", "")
    filename = f"{category_cap}_{area_clean}_{timestamp}{file_extension}"
    gcs_path = f"gs://mise-production-data/recordings/{period_id}/{filename}"

    # Generate signed URL for upload (valid for 1 hour)
    # Use IAM signBlob API directly since Cloud Run doesn't have service account keys
    from datetime import datetime as dt, timedelta
    import base64
    import hashlib
    import binascii
    from google.cloud import iam_credentials_v1
    import google.auth

    try:
        # Get default credentials and project
        credentials, project = google.auth.default()

        # Get service account email
        import requests as http_requests
        metadata_url = "http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/email"
        service_account_email = http_requests.get(
            metadata_url,
            headers={"Metadata-Flavor": "Google"},
            timeout=5
        ).text.strip()

        # Build the string to sign (GCS v4 signing format)
        # IMPORTANT: Use same timestamp for all date calculations to avoid drift
        now = dt.utcnow()
        expiration_time = now + timedelta(hours=1)
        expiration_timestamp = int(expiration_time.timestamp())

        # Credential scope
        datestamp = now.strftime('%Y%m%d')
        credential_scope = f"{datestamp}/auto/storage/goog4_request"
        credential = f"{service_account_email}/{credential_scope}"

        # Canonical request components
        method = "PUT"
        resource_path = f"/mise-production-data/recordings/{period_id}/{filename}"
        goog_date = now.strftime('%Y%m%dT%H%M%SZ')
        canonical_query_params = f"X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential={credential.replace('/', '%2F')}&X-Goog-Date={goog_date}&X-Goog-Expires=3600&X-Goog-SignedHeaders=content-type%3Bhost"
        canonical_headers = "content-type:audio/wav\nhost:storage.googleapis.com\n"
        signed_headers = "content-type;host"
        payload_hash = "UNSIGNED-PAYLOAD"

        # Canonical request
        canonical_request = f"{method}\n{resource_path}\n{canonical_query_params}\n{canonical_headers}\n{signed_headers}\n{payload_hash}"

        # String to sign
        canonical_request_hash = hashlib.sha256(canonical_request.encode()).hexdigest()
        string_to_sign = f"GOOG4-RSA-SHA256\n{dt.utcnow().strftime('%Y%m%dT%H%M%SZ')}\n{credential_scope}\n{canonical_request_hash}"

        # Sign using IAM signBlob API
        iam_client = iam_credentials_v1.IAMCredentialsClient(credentials=credentials)
        service_account_name = f"projects/-/serviceAccounts/{service_account_email}"

        sign_response = iam_client.sign_blob(
            request={
                "name": service_account_name,
                "payload": string_to_sign.encode()
            }
        )

        # Convert signature to hex
        signature = binascii.hexlify(sign_response.signed_blob).decode()

        # Build final signed URL
        upload_url = f"https://storage.googleapis.com{resource_path}?{canonical_query_params}&X-Goog-Signature={signature}"

        return JSONResponse({
            "status": "success",
            "upload_url": upload_url,
            "gcs_path": gcs_path,
            "shelfy_id": shelfy_id,
            "area": area,
            "category": category,
            "period_id": period_id,
            "expires_in": 3600
        })
    except Exception as e:
        log.error(f"Failed to generate upload URL: {e}")
        return JSONResponse(
            {"status": "error", "error": f"Failed to generate upload URL: {str(e)}"},
            status_code=500
        )


@router.post("/process_uploaded")
async def process_uploaded(request: Request):
    """Process an audio file already uploaded to GCS.

    Use this after uploading via signed URL from /get_upload_url.

    Request body (JSON):
        - gcs_path: GCS path to the uploaded file
        - shelfy_id: Shelfy ID from get_upload_url
        - area: Area name
        - category: "kitchen" or "bar"
        - period_id: Inventory period

    Response:
        - Same as /record_shelfy
    """
    try:
        body = await request.json()
    except Exception:
        return JSONResponse(
            {"status": "error", "error": "Invalid JSON body"},
            status_code=400
        )

    gcs_path = body.get("gcs_path")
    shelfy_id = body.get("shelfy_id")
    area = body.get("area")
    category = body.get("category")
    period_id = body.get("period_id")

    if not all([gcs_path, shelfy_id, area, category, period_id]):
        return JSONResponse(
            {"status": "error", "error": "Missing required fields"},
            status_code=400
        )

    config = request.app.state.config
    storage = get_shelfy_storage()

    # Download audio from GCS
    from google.cloud import storage as gcs
    try:
        client = gcs.Client()
        # Parse GCS path: gs://bucket/path/to/file
        if not gcs_path.startswith("gs://"):
            raise ValueError("Invalid GCS path")

        parts = gcs_path[5:].split("/", 1)
        bucket_name = parts[0]
        blob_path = parts[1]

        bucket = client.bucket(bucket_name)
        blob = bucket.blob(blob_path)
        audio_bytes = blob.download_as_bytes()

        log.info(f"📥 Downloaded {len(audio_bytes):,} bytes from {gcs_path}")
    except Exception as e:
        log.error(f"Failed to download from GCS: {e}")
        return JSONResponse(
            {"status": "error", "error": f"Failed to download audio from GCS: {str(e)}"},
            status_code=500
        )

    # Process through transrouter (transcribe + parse)
    try:
        response = requests.post(
            f"{config.transrouter_url}/api/v1/audio/process",
            headers={"X-API-Key": config.transrouter_api_key},
            files={"file": ("recording.wav", audio_bytes, "audio/wav")},
            timeout=120,
        )
        response.raise_for_status()
        result = response.json()
    except requests.RequestException as e:
        log.error(f"Transrouter API error: {e}")
        return JSONResponse(
            {"status": "error", "error": f"Processing failed: {e}"},
            status_code=500
        )

    if result.get("status") != "success":
        error = result.get("error", "Processing failed")
        log.error(f"Processing failed: {error}")
        return JSONResponse(
            {"status": "error", "error": error},
            status_code=400
        )

    transcript = result.get("transcript", "")
    inventory_json = result.get("approval_json", {})

    log.info(f"Processing complete: {len(transcript)} chars, {len(inventory_json.get('items', []))} items")

    # Store shelfy record (audio already in GCS)
    audio_path_str = gcs_path.replace("gs://mise-production-data/", "")

    shelfy = storage.add_shelfy(
        period_id=period_id,
        shelfy_id=shelfy_id,
        area=area,
        category=category,
        transcript=transcript,
        audio_path=audio_path_str,
        inventory_json=inventory_json,
    )

    log.info(f"Created shelfy {shelfy_id} for {area} ({category})")

    return JSONResponse({
        "status": "success",
        "shelfy_id": shelfy_id,
        "area": area,
        "category": category,
        "period_id": period_id,
        "transcript": transcript,
        "inventory_json": inventory_json,
        "audio_path": audio_path_str,
        "status": "pending_approval",
    })


@router.post("/record_shelfy")
async def record_shelfy(
    request: Request,
    file: UploadFile = File(...),
    area: str = Form(...),
    category: str = Form(...),
    period_id: Optional[str] = Form(None),
):
    """Upload shelfy audio and get transcription.

    NOTE: This endpoint has a 32MB file size limit due to Cloud Run.
    For larger files (>32MB), use the two-step process:
    1. POST /inventory/get_upload_url to get a signed GCS URL
    2. PUT audio file directly to that URL
    3. POST /inventory/process_uploaded to process the file

    Request:
        - file: Audio file (webm, wav, m4a, mp3) - MAX 32MB
        - area: Area being counted (e.g., "Walk-in", "Back Bar")
        - category: "kitchen" or "bar"
        - period_id: Optional, will be inferred from transcript if not provided

    Response:
        - shelfy_id: Unique identifier
        - area: Area name
        - category: kitchen or bar
        - period_id: Normalized to last day of month
        - transcript: Transcribed text
        - audio_path: Path to archived recording
        - status: "pending_approval"
    """
    config = request.app.state.config
    storage = get_shelfy_storage()

    # Validate category
    category = category.lower()
    if category not in ("kitchen", "bar"):
        return JSONResponse(
            {"status": "error", "error": f"Invalid category: {category}. Must be 'kitchen' or 'bar'."},
            status_code=400
        )

    # Validate area for category
    valid_areas = KITCHEN_AREAS if category == "kitchen" else BAR_AREAS
    if area not in valid_areas:
        return JSONResponse(
            {"status": "error", "error": f"Invalid area '{area}' for {category}. Valid areas: {valid_areas}"},
            status_code=400
        )

    # Read audio bytes
    audio_bytes = await file.read()
    if not audio_bytes:
        return JSONResponse(
            {"status": "error", "error": "Empty audio file"},
            status_code=400
        )

    log.info(f"🗄️ Processing shelfy for {area} ({category}) from file {file.filename}")

    # Call transrouter API to process inventory (transcript + parsing)
    try:
        response = requests.post(
            f"{config.transrouter_url}/api/v1/audio/process",
            headers={"X-API-Key": config.transrouter_api_key},
            files={"file": ("recording.wav", audio_bytes, "audio/wav")},
            timeout=120,
        )
        response.raise_for_status()
        result = response.json()
    except requests.RequestException as e:
        log.error(f"🗄️ Transrouter API error: {e}")
        return JSONResponse(
            {"status": "error", "error": f"Processing failed: {e}"},
            status_code=500
        )

    if result.get("status") != "success":
        error = result.get("error", "Processing failed")
        log.error(f"🗄️ Processing failed: {error}")
        return JSONResponse(
            {"status": "error", "error": error},
            status_code=400
        )

    transcript = result.get("transcript", "")

    # Extract inventory_json from response (transrouter API returns it as approval_json)
    inventory_json = result.get("approval_json", {})

    log.info(f"🗄️ Processing complete: {len(transcript)} chars, {len(inventory_json.get('items', []) if inventory_json else [])} items parsed")

    # Normalize period_id (detect from transcript or use current month)
    if not period_id:
        period_id = normalize_period_id(transcript)
        log.info(f"🗄️ Inferred period_id: {period_id}")

    # Generate shelfy ID
    shelfy_id = generate_shelfy_id(area)

    # Save recording to archive
    audio_path = save_shelfy_recording(audio_bytes, period_id, category, area, file.filename)
    audio_path_str = str(audio_path.relative_to(RECORDINGS_DIR.parent))

    # Store shelfy record
    shelfy = storage.add_shelfy(
        period_id=period_id,
        shelfy_id=shelfy_id,
        area=area,
        category=category,
        transcript=transcript,
        audio_path=audio_path_str,
        inventory_json=inventory_json,
    )

    log.info(f"🗄️ Created shelfy {shelfy_id} for {area} ({category})")

    return JSONResponse({
        "status": "success",
        "shelfy_id": shelfy_id,
        "area": area,
        "category": category,
        "period_id": period_id,
        "transcript": transcript,
        "inventory_json": inventory_json,
        "audio_path": audio_path_str,
        "status": "pending_approval",
    })


@router.post("/approve_shelfy")
async def approve_shelfy(request: Request):
    """Approve a shelfy and commit to totals.

    Request body:
        - shelfy_id: The shelfy to approve

    Response:
        - success: true/false
        - shelfy_id: The approved shelfy ID
        - status: "approved"
    """
    storage = get_shelfy_storage()

    # Parse JSON body
    try:
        body = await request.json()
        shelfy_id = body.get("shelfy_id")
    except Exception:
        return JSONResponse(
            {"status": "error", "error": "Invalid JSON body"},
            status_code=400
        )

    if not shelfy_id:
        return JSONResponse(
            {"status": "error", "error": "Missing shelfy_id"},
            status_code=400
        )

    # Find the shelfy across all periods (in case period_id not provided)
    # For demo, we'll require looking it up by parsing the shelfy_id
    # shelfy_id format: shelfy_{timestamp}_{area}

    # Try to find in all period directories
    storage_dir = storage.storage_dir / "inventory"
    if not storage_dir.exists():
        return JSONResponse(
            {"status": "error", "error": f"Shelfy not found: {shelfy_id}"},
            status_code=404
        )

    found_period = None
    for period_dir in storage_dir.iterdir():
        if period_dir.is_dir():
            period_id = period_dir.name
            shelfy = storage.get_shelfy(period_id, shelfy_id)
            if shelfy:
                found_period = period_id
                break

    if not found_period:
        return JSONResponse(
            {"status": "error", "error": f"Shelfy not found: {shelfy_id}"},
            status_code=404
        )

    # Approve the shelfy
    success = storage.approve_shelfy(found_period, shelfy_id)

    if success:
        log.info(f"🗄️ Approved shelfy {shelfy_id}")
        return JSONResponse({
            "success": True,
            "shelfy_id": shelfy_id,
            "status": "approved",
        })
    else:
        return JSONResponse(
            {"status": "error", "error": f"Failed to approve shelfy: {shelfy_id}"},
            status_code=500
        )


@router.get("/totals/{period_id}")
async def get_inventory_totals(request: Request, period_id: str):
    """Get all shelfies for an inventory period.

    Response:
        - period_id: The period
        - shelfies: List of all shelfies for the period
    """
    storage = get_shelfy_storage()

    shelfies = storage.get_all_shelfies(period_id)
    summary = storage.get_period_summary(period_id)

    log.info(f"🗄️ Retrieved {len(shelfies)} shelfies for period {period_id}")

    return JSONResponse({
        "period_id": period_id,
        "shelfies": shelfies,
        "summary": summary,
    })


@router.get("/shelfy/{shelfy_id}")
async def get_shelfy(request: Request, shelfy_id: str):
    """Get individual shelfy details.

    Response:
        - Full shelfy record including transcript, status, timestamps
    """
    storage = get_shelfy_storage()

    # Search across all periods
    storage_dir = storage.storage_dir / "inventory"
    if not storage_dir.exists():
        return JSONResponse(
            {"status": "error", "error": f"Shelfy not found: {shelfy_id}"},
            status_code=404
        )

    for period_dir in storage_dir.iterdir():
        if period_dir.is_dir():
            period_id = period_dir.name
            shelfy = storage.get_shelfy(period_id, shelfy_id)
            if shelfy:
                log.info(f"🗄️ Retrieved shelfy {shelfy_id} from period {period_id}")
                return JSONResponse(shelfy)

    return JSONResponse(
        {"status": "error", "error": f"Shelfy not found: {shelfy_id}"},
        status_code=404
    )


@router.get("/areas")
async def get_areas(request: Request):
    """Get available areas by category.

    Response:
        - kitchen: List of kitchen areas
        - bar: List of bar areas
    """
    return JSONResponse({
        "kitchen": KITCHEN_AREAS,
        "bar": BAR_AREAS,
    })


@router.get("/periods")
async def get_inventory_periods(request: Request):
    """Get list of available inventory periods with data.

    Response:
        - periods: List of period objects with summary stats
    """
    storage = get_shelfy_storage()
    storage_dir = storage.storage_dir / "inventory"

    periods = []
    if storage_dir.exists():
        for period_dir in sorted(storage_dir.iterdir(), reverse=True):
            if period_dir.is_dir():
                period_id = period_dir.name
                summary = storage.get_period_summary(period_id)
                periods.append(summary)

    return JSONResponse({
        "periods": periods,
    })


# ============================================================================
# HTML PAGE ROUTES (Frontend Views)
# ============================================================================


def get_current_period_id_html() -> str:
    """Get the current inventory period (last day of current month)."""
    from datetime import timedelta
    now = datetime.now()
    if now.month == 12:
        last_day = datetime(now.year + 1, 1, 1) - timedelta(days=1)
    else:
        last_day = datetime(now.year, now.month + 1, 1) - timedelta(days=1)
    return last_day.strftime("%Y-%m-%d")


def get_period_label_html(period_id: str) -> str:
    """Convert period_id to human-readable label."""
    try:
        date = datetime.strptime(period_id, "%Y-%m-%d")
        return date.strftime("%B %Y")
    except ValueError:
        return period_id


def get_area_name_from_slug(slug: str, category: str) -> str:
    """Convert area slug back to display name."""
    areas = KITCHEN_AREAS if category == "kitchen" else BAR_AREAS
    for area in areas:
        if slug == area.lower().replace(" ", "-").replace("/", "-"):
            return area
    return slug.replace("-", " ").title()


def get_area_slug(area_name: str) -> str:
    """Convert area name to URL-safe slug."""
    return area_name.lower().replace(" ", "-").replace("/", "-")


@router.get("", response_class=HTMLResponse)
async def inventory_landing_page(request: Request):
    """Render the inventory landing page with 'Record a Shelfy' button."""
    restaurant_id = require_restaurant(request)
    templates = request.app.state.templates
    storage = get_shelfy_storage()

    # Check if any shelfies exist for current period
    period_id = get_current_period_id_html()
    shelfies = storage.get_all_shelfies(period_id)
    has_shelfies = len(shelfies) > 0

    context = get_template_context(request)
    context.update({
        "has_shelfies": has_shelfies,
        "active_tab": "record",
    })
    return templates.TemplateResponse("inventory_landing.html", context)


@router.get("/select-category", response_class=HTMLResponse)
async def select_category_page(request: Request):
    """Render the category selection page (Kitchen vs Bar)."""
    restaurant_id = require_restaurant(request)
    templates = request.app.state.templates

    context = get_template_context(request)
    context.update({"active_tab": "record"})
    return templates.TemplateResponse("inventory_select_category.html", context)


@router.get("/select-area/{category}", response_class=HTMLResponse)
async def select_area_page(request: Request, category: str):
    """Render the area selection page based on category."""
    restaurant_id = require_restaurant(request)
    templates = request.app.state.templates

    if category not in ("kitchen", "bar"):
        return RedirectResponse("/inventory/select-category")

    area_names = KITCHEN_AREAS if category == "kitchen" else BAR_AREAS
    areas = [{"name": a, "slug": get_area_slug(a)} for a in area_names]

    context = get_template_context(request)
    context.update({
        "category": category,
        "areas": areas,
        "active_tab": "record",
    })
    return templates.TemplateResponse("inventory_select_area.html", context)


@router.get("/record/{category}/{area_slug}", response_class=HTMLResponse)
async def record_shelfy_page(request: Request, category: str, area_slug: str):
    """Render the recording interface for a specific area."""
    restaurant_id = require_restaurant(request)
    templates = request.app.state.templates

    if category not in ("kitchen", "bar"):
        return RedirectResponse("/inventory/select-category")

    area_name = get_area_name_from_slug(area_slug, category)

    context = get_template_context(request)
    context.update({
        "category": category,
        "area": area_name,
        "area_slug": area_slug,
        "active_tab": "record",
    })
    return templates.TemplateResponse("inventory_record.html", context)


@router.get("/approve/{shelfy_id}", response_class=HTMLResponse)
async def approve_shelfy_page(request: Request, shelfy_id: str):
    """Render the approval page for a shelfy."""
    restaurant_id = require_restaurant(request)
    templates = request.app.state.templates
    storage = get_shelfy_storage()

    # Search across all periods
    storage_dir = storage.storage_dir / "inventory"
    shelfy = None

    if storage_dir.exists():
        for period_dir in storage_dir.iterdir():
            if period_dir.is_dir():
                period_id = period_dir.name
                found = storage.get_shelfy(period_id, shelfy_id)
                if found:
                    shelfy = found
                    break

    if not shelfy:
        return HTMLResponse(f"Shelfy not found: {shelfy_id}", status_code=404)

    # Add display timestamp if not present
    if "recorded_at_display" not in shelfy and "recorded_at" in shelfy:
        try:
            recorded_dt = datetime.fromisoformat(shelfy["recorded_at"].replace("Z", "+00:00"))
            shelfy["recorded_at_display"] = recorded_dt.strftime("%b %d, %I:%M %p")
        except (ValueError, KeyError):
            shelfy["recorded_at_display"] = shelfy.get("recorded_at", "")

    context = get_template_context(request)
    context.update({
        "shelfy": shelfy,
        "active_tab": "record",
    })
    return templates.TemplateResponse("inventory_approve.html", context)


@router.post("/approve_shelfy_form")
async def approve_shelfy_form(request: Request, shelfy_id: str = Form(...)):
    """Handle form submission for approving a shelfy (HTML form version)."""
    storage = get_shelfy_storage()

    # Search across all periods
    storage_dir = storage.storage_dir / "inventory"
    found_period = None

    if storage_dir.exists():
        for period_dir in storage_dir.iterdir():
            if period_dir.is_dir():
                period_id = period_dir.name
                shelfy = storage.get_shelfy(period_id, shelfy_id)
                if shelfy:
                    found_period = period_id
                    break

    if not found_period:
        return HTMLResponse(f"Shelfy not found: {shelfy_id}", status_code=404)

    # Approve the shelfy
    storage.approve_shelfy(found_period, shelfy_id)
    log.info(f"Approved shelfy {shelfy_id} via form")

    # Redirect to totals page
    return RedirectResponse(f"/inventory/totals-page/{found_period}", status_code=303)


@router.get("/totals-page", response_class=HTMLResponse)
async def inventory_totals_page_current(request: Request):
    """Render totals page for current period."""
    period_id = get_current_period_id_html()
    return await inventory_totals_page(request, period_id)


@router.get("/totals-page/{period_id}", response_class=HTMLResponse)
async def inventory_totals_page(request: Request, period_id: str):
    """Render inventory totals page for a specific period."""
    restaurant_id = require_restaurant(request)
    templates = request.app.state.templates
    storage = get_shelfy_storage()

    # Get shelfies for this period
    shelfies = storage.get_all_shelfies(period_id)

    # Add display timestamps
    for s in shelfies:
        if "recorded_at_display" not in s and "recorded_at" in s:
            try:
                recorded_dt = datetime.fromisoformat(s["recorded_at"].replace("Z", "+00:00"))
                s["recorded_at_display"] = recorded_dt.strftime("%b %d, %I:%M %p")
            except (ValueError, KeyError):
                s["recorded_at_display"] = s.get("recorded_at", "")

    # Group by category
    kitchen_shelfies = [s for s in shelfies if s.get("category") == "kitchen"]
    bar_shelfies = [s for s in shelfies if s.get("category") == "bar"]

    # Get aggregated totals
    kitchen_aggregated = storage.get_aggregated_totals(period_id, category="kitchen")
    bar_aggregated = storage.get_aggregated_totals(period_id, category="bar")

    log.info(f"📊 Totals for {period_id}: kitchen={len(kitchen_aggregated.get('items', []))} items, bar={len(bar_aggregated.get('items', []))} items")

    context = get_template_context(request)
    context.update({
        "period_id": period_id,
        "period_label": get_period_label_html(period_id),
        "shelfies": shelfies,
        "kitchen_shelfies": kitchen_shelfies,
        "bar_shelfies": bar_shelfies,
        "kitchen_aggregated": kitchen_aggregated,
        "bar_aggregated": bar_aggregated,
        "active_tab": "totals",
    })
    return templates.TemplateResponse("inventory_totals.html", context)


@router.get("/shelfy-page/{shelfy_id}", response_class=HTMLResponse)
async def shelfy_detail_page(request: Request, shelfy_id: str):
    """Render individual shelfy detail page."""
    restaurant_id = require_restaurant(request)
    templates = request.app.state.templates
    storage = get_shelfy_storage()

    # Search across all periods
    storage_dir = storage.storage_dir / "inventory"
    shelfy = None

    if storage_dir.exists():
        for period_dir in storage_dir.iterdir():
            if period_dir.is_dir():
                period_id = period_dir.name
                found = storage.get_shelfy(period_id, shelfy_id)
                if found:
                    shelfy = found
                    break

    if not shelfy:
        return HTMLResponse(f"Shelfy not found: {shelfy_id}", status_code=404)

    # Add display timestamp
    if "recorded_at_display" not in shelfy and "recorded_at" in shelfy:
        try:
            recorded_dt = datetime.fromisoformat(shelfy["recorded_at"].replace("Z", "+00:00"))
            shelfy["recorded_at_display"] = recorded_dt.strftime("%b %d, %I:%M %p")
        except (ValueError, KeyError):
            shelfy["recorded_at_display"] = shelfy.get("recorded_at", "")

    context = get_template_context(request)
    context.update({
        "shelfy": shelfy,
        "active_tab": "totals",
    })
    return templates.TemplateResponse("inventory_detail.html", context)
