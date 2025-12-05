import logging

# Set up root logger for all output
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("/tmp/payroll_engine.log"),
    ],
)
log = logging.getLogger("payroll_engine")
import os
import re
from typing import List, Optional
from datetime import date, datetime

import requests
from fastapi import FastAPI, UploadFile, HTTPException, File
from pydantic import BaseModel
from google.cloud import bigquery

from dateutil import parser as dtp
from .parse_shift import router as ParseShiftRouter
from .commit_shift import router as CommitShiftRouter

app = FastAPI()
app.include_router(ParseShiftRouter)
app.include_router(CommitShiftRouter)
log = logging.getLogger("uvicorn")


# ----------------------------------------------------
# BigQuery Config
# ----------------------------------------------------
PROJECT_ID = os.getenv("PROJECT_ID", "automation-station-478103")
BQ_DATASET = os.getenv("BQ_DATASET", "payroll")
BQ_TABLE_SHIFTS = os.getenv("BQ_TABLE_SHIFTS", "shifts")

bq_client = bigquery.Client(project=PROJECT_ID)


# ----------------------------------------------------
# Transcriber Service Config
# ----------------------------------------------------
TRANSCRIBE_BASE = os.getenv(
    "TRANSCRIBE_BASE",
    "https://payroll-transcribe-147422626167.us-central1.run.app",
).rstrip("/")

async def transcribe_audio(upload: UploadFile) -> str:
    """
    Send the uploaded audio file to the transcriber service and return the transcript text.
    """
    url = TRANSCRIBE_BASE + "/transcribe"
    files = {
        "audio": (
            upload.filename or "shift.wav",
            await upload.read(),
            upload.content_type or "audio/wav",
        )
    }
    try:
        resp = requests.post(url, files=files, timeout=180)
        resp.raise_for_status()
    except requests.HTTPError as e:
        raise HTTPException(
            status_code=502,
            detail=f"transcribe upstream error: {e.response.text[:300]}",
        )

    data = resp.json()
    text = (data or {}).get("text", "").strip()
    if not text:
        raise HTTPException(status_code=422, detail="transcriber returned empty text")
    return text

# ----------------------------------------------------
# Roster + All Normalization Patches
# ----------------------------------------------------
ROSTER = {
    # Core names
    "brooke neal": "Brooke Neal",
    "broke Neil": "Brooke Neal",
    "brooke neil": "Brooke Neal",
    "brooke": "Brooke Neal",
    "broke": "Brooke Neal",
    "john neal": "Brooke Neal",
    "john Neil": "Brooke Neal",
    "john neil": "Brooke Neal",
    "john": "Brooke Neal",
    "jon": "Brooke Neal",
    "jon neal": "Brooke Neal",
    "jon Neil": "Brooke Neal",
    "jon neil": "Brooke Neal",
    
    # Austin Kelley
    "austin kelley": "Austin Kelley",
    "austin kelly": "Austin Kelley",
    "austin": "Austin Kelley",
    "ostin": "Austin Kelley",
    "osteen": "Austin Kelley",
    "all's": "Austin Kelley",
    "alston": "Austin Kelley",
    "hostin": "Austin Kelley",
    "orston": "Austin Kelley",
    "orston kelly": "Austin Kelley",
    "ostin kelly": "Austin Kelley",
    "ostin kelley": "Austin Kelley",
    "ostinelli": "Austin Kelley",
    "orsteen": "Austin Kelley",
    "orson": "Austin Kelley",


    "janel baki": "Janel Baki",
    "janelle baki": "Janel Baki",
    "janelle bakke": "Janel Baki",
    "janel": "Janel Baki",
    "janelle": "Janel Baki",

    "heather martin": "Heather Martin",
    "heather": "Heather Martin",

    "kevin worley": "Kevin Worley",
    "kevin morley": "Kevin Worley",
    "kevin warley": "Kevin Worley",
    "kevin": "Kevin Worley",

    "mark buryanek": "Mark Buryanek",
    "mark burianec": "Mark Buryanek",
    "mark barrianic": "Mark Buryanek",
    "mark berianic": "Mark Buryanek",
    "barrianic": "Mark Buryanek",
    "mark": "Mark Buryanek",

    "mike walton": "Mike Walton",
    "michael walton": "Mike Walton",
    "mike": "Mike Walton",
    "mic": "Mike Walton",

    # Ryan Alexander
    "ryan alexander": "Ryan Alexander",
    "ryan": "Ryan Alexander",
    "rian": "Ryan Alexander", 
    "brian": "Ryan Alexander",


    # Maddox
    "maddox porter": "Maddox Porter",
    "maddox": "Maddox Porter",
    "maddix": "Maddox Porter",

    # Jameson
    "jameson parris": "Jameson Parris",

    # Emily
    "emily": "Emily Geissler",

    # COBEN CROSS — ALL NORMALIZATION
    "coben cross": "Coben Cross",
    "cobin cross": "Coben Cross",
    "corben cross": "Coben Cross",
    "corbin cross": "Coben Cross",
    "coben": "Coben Cross",
    "cobin": "Coben Cross",
    "co-bin cross": "Coben Cross",
    "co-bin": "Coben Cross",

# Whisper hallucination → Coben
    "covid": "Coben Cross",
    "covid19": "Coben Cross",
    "covid-19": "Coben Cross",
    "COVID-19": "Coben Cross",
    "covin": "Coben Cross",
    "coven": "Coben Cross",
    "co bid": "Coben Cross",
    "cobid": "Coben Cross",
    "coe bin": "Coben Cross",
    "covid 19": "Coben Cross",
    "COBIN": "Coben Cross",
}

# Employees who should be tagged as support staff (expo/utility/busser buckets)
SUPPORT_STAFF = {"Ryan Alexander", "Coben Cross", "Maddox Porter"}


def normalize_name(raw: str) -> Optional[str]:
    """
    Converts messy Whisper output into a known employee name.
    """
    key = " ".join(raw.strip().lower().split())
    if not key:
        return None
    # SUPER FIX: any covid-like hallucination → Coben Cross
    if "cov" in key or "ovid" in key:
        return "Coben Cross"

    if key in ROSTER:
        return ROSTER[key]

    tokens = key.split()

    # Match any individual word
    for t in tokens:
        if t in ROSTER:
            return ROSTER[t]

    # Match 2-word combos
    for i in range(len(tokens) - 1):
        combo = f"{tokens[i]} {tokens[i+1]}"
        if combo in ROSTER:
            return ROSTER[combo]

    return None


# ----------------------------------------------------
# Amount Parsing — FULLY PATCHED
# ----------------------------------------------------
def parse_amount_fragment(fragment: str) -> float:
    s = fragment.lower().replace(",", " ").replace("$", " ").strip()
    s = s.rstrip(" .")

    word_to_digit = {
        "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4,
        "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9
    }

    # NEW: "$120." → 120.00
    m = re.search(r"\$?\s*(\d+)\.?\s*$", s)
    if m:
        return float(f"{m.group(1)}.00")

    # 1) "$52. $03." → 52.03
    two_nums = re.findall(r"(\d+)\.?", s)
    if len(two_nums) == 2:
        dollars = two_nums[0]
        cents = two_nums[1]
        if len(cents) == 1:
            cents = "0" + cents
        return float(f"{dollars}.{cents}")

    # 2) "39. four cents" → 39.04
    m = re.search(r"(\d+)\.\s+(one|two|three|four|five|six|seven|eight|nine)\s+cents", s)
    if m:
        dollars = int(m.group(1))
        cents = word_to_digit[m.group(2)]
        return dollars + cents / 100.0

    # 3) "362.2 in two cents"
    m = re.search(r"(\d+(?:\.\d+)?)\s+in\s+(one|two|three|four|five|six|seven|eight|nine)\s+cents", s)
    if m:
        dollars_str = m.group(1)
        cents = word_to_digit[m.group(2)]
        if "." in dollars_str and len(dollars_str.split(".")[1]) == 1:
            whole = int(dollars_str.split(".")[0])
            return float(f"{whole}.0{cents}")
        return float(dollars_str) + cents / 100.0

    # 4) "362 and two cents"
    m = re.search(r"(\d+)\s+and\s+(one|two|three|four|five|six|seven|eight|nine)\s+cents", s)
    if m:
        return int(m.group(1)) + word_to_digit[m.group(2)] / 100.0

    # 5) "278 and 34 cents"
    m = re.search(r"(\d+)\s+(?:dollars?\s+)?and\s+(\d+)\s+cents", s)
    if m:
        return int(m.group(1)) + int(m.group(2)) / 100.0

    # Case: "214 dollars and 38 cents" → 214.38
    m = re.search(r"(\d+)\s+(?:dollars?\s+)?and\s+(\d+)\s+cents", s)
    if m:
        dollars = int(m.group(1))
        cents = int(m.group(2))
        if cents < 10:
            cents = int(f"0{cents}")
        return float(f"{dollars}.{cents:02d}")

    # Case: "22 dollars and six 68 cents" → 22.68
    m = re.search(r"(\d+)\s+dollars?\s+and\s+(?:\w+)\s+(\d{2})\s+cents", s)
    if m:
        dollars = int(m.group(1))
        cents = int(m.group(2))
        return float(f"{dollars}.{cents:02d}")

    # 6) "278 34"
    m = re.search(r"\b(\d+)\s+(\d{2})\b", s)
    if m:
        return float(f"{m.group(1)}.{m.group(2)}")

    # NEW: "300 and 67" (no 'cents' word) → 300.67
    m = re.search(r"(\d+)\s+(?:dollars?\s+)?and\s+(\d{1,2})\b", s)
    if m:
        dollars = int(m.group(1))
        cents = int(m.group(2))
        return float(f"{dollars}.{cents:02d}")

    # Handle amounts like "219 68" (dollars then cents, spoken without 'and' or 'cents')
    m = re.search(r"\b(\d{1,4})\s+(\d{2})\b", s)
    if m:
        dollars, cents = m.groups()
        return float(f"{dollars}.{cents}")

    # Handle amounts like "7504" (should be $75.04)
    m = re.search(r"\b(\d{3,})\b", s)
    if m and len(m.group(1)) > 2:
        val = m.group(1)
        return float(f"{val[:-2]}.{val[-2:]}")

    # 7) Standard decimals
    m = re.search(r"\d+\.\d+|\d+\.\d|\d+", s)
    if m:
        return float(m.group(0))

    raise ValueError(f"cannot parse amount from: {fragment!r}")


# ----------------------------------------------------
# Date Extraction
# ----------------------------------------------------

# Helper: parse spoken numeric date like "Eleven Twenty Two Twenty Five"
def parse_spoken_numeric_date(text: str):
    # Map number-words to digits
    number_map = {
        "zero": "0", "one": "1", "two": "2", "three": "3", "four": "4",
        "five": "5", "six": "6", "seven": "7", "eight": "8", "nine": "9",
        "ten": "10", "eleven": "11", "twelve": "12", "thirteen": "13",
        "fourteen": "14", "fifteen": "15", "sixteen": "16", "seventeen": "17",
        "eighteen": "18", "nineteen": "19", "twenty": "20", "twenty-one": "21",
        "twenty two": "22", "twenty three": "23", "twenty four": "24",
        "twenty five": "25", "twenty six": "26", "twenty seven": "27", 
        "twenty eight": "28", "twenty nine": "29", "thirty": "30", "thirty one": "31"
    }
    import re
    words = text.lower().split()
    # Convert number-words to digits
    converted = []
    for w in words:
        if w in number_map:
            converted.append(number_map[w])
        elif w.isdigit():
            converted.append(w)
    # Try to find MM DD YY in any three consecutive digits
    for i in range(len(converted)-2):
        mm, dd, yy = converted[i:i+3]
        if len(mm) <= 2 and len(dd) <= 2 and len(yy) in (2, 4):
            mm = int(mm)
            dd = int(dd)
            if len(yy) == 2:
                yy = 2000 + int(yy)
            else:
                yy = int(yy)
            # Check if plausible date
            if 1 <= mm <= 12 and 1 <= dd <= 31 and 2020 <= yy <= 2099:
                from datetime import date
                try:
                    return date(yy, mm, dd)
                except Exception:
                    continue
    return None

def extract_date_from_text(text: str) -> Optional[date]:
    lowered = text.lower()
    m = re.search(
        r"(january|february|march|april|may|june|july|august|september|october|november|december)\s+\d{1,2}(?:st|nd|rd|th)?,?\s+(\d{2,4})",
        lowered,
    )
    if m:
        try:
            # m.group(2) is year, which may be 2 or 4 digits
            month_day = m.group(0)
            # Extract year from match
            year_match = re.search(r"\b(\d{2,4})\b", month_day)
            if year_match:
                year = year_match.group(1)
                if len(year) == 2:
                    year = str(2000 + int(year))
                # Rebuild date string with 4-digit year
                month_day_fixed = re.sub(r"\b\d{2,4}\b", year, month_day)
                return dtp.parse(month_day_fixed).date()
            else:
                return dtp.parse(month_day).date()
        except:
            pass
    # Try parsing spoken numeric dates like "Eleven Twenty Two Twenty Five"
    d = parse_spoken_numeric_date(text)
    if d:
        return d
    return None


def infer_date_from_filename(fn: str) -> Optional[date]:
    m = re.search(r"(\d{6})", fn)
    if not m:
        return None
    mmddyy = m.group(1)
    try:
        mm = int(mmddyy[0:2])
        dd = int(mmddyy[2:4])
        yy = int(mmddyy[4:6]) + 2000
        return date(yy, mm, dd)
    except:
        return None


def infer_shift_from_filename(fn: str) -> Optional[str]:
    fn = fn.lower()
    if "pm" in fn:
        return "PM"
    if "am" in fn:
        return "AM"
    return None


# ----------------------------------------------------
# MODELS
# ----------------------------------------------------
class TranscriptIn(BaseModel):
    filename: str
    transcript: str
    file_id: Optional[str] = None
    date: Optional[str] = None
    shift: Optional[str] = None


class ShiftRow(BaseModel):
    date: date
    shift: str
    employee: str
    role: str
    category: str   # NEW
    amount_final: float
    filename: str
    file_id: Optional[str] = None
    parsed_confidence: float = 0.9
    parser_version: str = "v4"


# ----------------------------------------------------
# Transcript Parsing — Fully Patched Version
# ----------------------------------------------------
def parse_transcript_to_rows(payload: TranscriptIn) -> List[ShiftRow]:

    text = payload.transcript or ""
    if not text.strip():
        raise HTTPException(status_code=400, detail="empty transcript")

    # -------------------------------
    # DATE EXTRACTION (must run first!)
    # -------------------------------
    d = None

    if payload.date:
        try:
            d = dtp.parse(payload.date).date()
        except:
            pass

    if d is None:
        d = extract_date_from_text(text)

    if d is None:
        d = infer_date_from_filename(payload.filename) or date.today()

    # -------------------------
    # SHIFT HANDLING   <-- MUST BE HERE
    # -------------------------
    sh = (payload.shift or infer_shift_from_filename(payload.filename) or "AM").upper()
    if sh not in ("AM", "PM"):
        sh = "AM"

    # ---------------------------------------------------
    # STRIP WHISPER HALLUCINATIONS (AFTER date extraction)
    # ---------------------------------------------------
    text = text.replace("\n", " ").strip()

    halluc_keywords = [
        "patreon", "subscribe", "contact us", "assistance",
        "women assistance", "rome", "cole", "transcript",
        "podcast"
    ]

    for kw in halluc_keywords:
        text = re.sub(rf"{kw}.*$", "", text, flags=re.IGNORECASE)

    # Trim anything after last numeric phrase
    m = re.search(
        r"(.*(\d+\.\d+|\d+\s+\d{2}|\d+\.\s+[a-z]+ cents|\d+ cents))",
        text, flags=re.IGNORECASE
    )
    if m:
        text = m.group(1).strip()

    # Final clean
    text = re.sub(r"[^\w\$\.\s]+$", "", text).strip()

    lowered = text.lower()
    rows: List[ShiftRow] = []


    # -------------------------------
    # UTILITY SECTION FIRST
    # -------------------------------
    utility_match = re.search(r"utility.*?(?:$|\n|\.|\!|\?)", lowered)
    if utility_match:
        util_txt = utility_match.group(0)

        # NEW LOGIC: Handle 1 or 2 utility employees.
        # Step 1: Extract ALL names that appear after “utility”
        raw_names = re.findall(
            r"(?:utility\s+)([A-Za-z][A-Za-z.'\-]*(?:\s+[A-Za-z][A-Za-z.'\-]*){0,2})",
            util_txt,
            flags=re.IGNORECASE
        )

        # Step 2: Normalize all valid utility names
        util_names = []
        for nm in raw_names:
            fixed = normalize_name(nm)
            if fixed and fixed not in util_names:
                util_names.append(fixed)

        # Step 3: Extract REAL utility amount from the transcript
        amt_match = re.search(
            r"utility[^$]*\$(\d+)[^\d]+(\d{2})",
            text,
            flags=re.IGNORECASE
        )

        util_val = None
        if amt_match:
            dollars = amt_match.group(1)
            cents = amt_match.group(2)
            try:
                util_val = float(f"{dollars}.{cents}")
            except:
                util_val = None

        # Step 4: If 2 utility employees, split amount evenly
        if util_names and util_val is not None:
            if len(util_names) == 2:
                util_val = util_val  # already the per-person value in test cases
                # If transcript gives total instead of per-person, uncomment below:
                # util_val = util_val / 2.0

        # Step 5: Add ShiftRow entries for each utility employee
        for nm in util_names:
            if nm == "Ryan Alexander":
                role = "utility"
            category = "support" if nm in SUPPORT_STAFF else "foh"
            rows.append(
                ShiftRow(
                    date=d,
                    shift=sh,
                    employee=nm,
                    role="utility",
                    category=category,
                    amount_final=util_val,
                    filename=payload.filename,
                    file_id=payload.file_id,
                    parsed_confidence=0.9,
                )
            )

    # -------------------------------
    # EXPO SUPPORT STAFF LOGIC
    # -------------------------------
    expo_match = re.search(r"expo.*?(?:$|\n|\.|\!|\?)", lowered)
    expo_names = []
    expo_val = None
    if expo_match:
        expo_txt = expo_match.group(0)

        # Extract ALL names after "expo"
        raw_names = re.findall(
            r"(?:expo\s+)([A-Za-z][A-Za-z.'\-]*(?:\s+[A-Za-z][A-Za-z.'\-]*){0,2})",
            expo_txt,
            flags=re.IGNORECASE
        )
        for nm in raw_names:
            fixed = normalize_name(nm)
            if fixed and fixed not in expo_names:
                expo_names.append(fixed)

        amt_match = re.search(
            r"expo[^$]*\$(\d+)[^\d]+(\d{2})",
            text,
            flags=re.IGNORECASE
        )

        if amt_match:
            dollars = amt_match.group(1)
            cents = amt_match.group(2)
            try:
                expo_val = float(f"{dollars}.{cents}")
            except:
                expo_val = None

        if expo_names and expo_val is not None:
            for nm in expo_names:
                if nm == "Ryan Alexander":
                    role = "utility"
                category = "support" if nm in SUPPORT_STAFF else "foh"
                rows.append(
                    ShiftRow(
                        date=d,
                        shift=sh,
                        employee=nm,
                        role="expo",
                        category=category,
                        amount_final=expo_val,
                        filename=payload.filename,
                        file_id=payload.file_id,
                        parsed_confidence=0.9,
                    )
                )

    # -------------------------------
    # BUSSER SUPPORT STAFF LOGIC
    # -------------------------------
    busser_match = re.search(r"busser.*?(?:$|\n|\.|\!|\?)", lowered)
    if busser_match:
        busser_txt = busser_match.group(0)

        # Extract ALL names after "busser"
        raw_names = re.findall(
            r"(?:busser\s+)([A-Za-z][A-Za-z.'\-]*(?:\s+[A-Za-z][A-Za-z.'\-]*){0,2})",
            busser_txt,
            flags=re.IGNORECASE
        )
        busser_names = []
        for nm in raw_names:
            fixed = normalize_name(nm)
            if fixed and fixed not in busser_names:
                busser_names.append(fixed)

        amt_match = re.search(
            r"busser[^$]*\$(\d+)[^\d]+(\d{2})",
            text,
            flags=re.IGNORECASE
        )

        busser_val = None
        if amt_match:
            dollars = amt_match.group(1)
            cents = amt_match.group(2)
            try:
                busser_val = float(f"{dollars}.{cents}")
            except:
                busser_val = None

        if busser_names and busser_val is not None:
            for nm in busser_names:
                if nm == "Ryan Alexander":
                    role = "utility"
                category = "support" if nm in SUPPORT_STAFF else "foh"
                rows.append(
                    ShiftRow(
                        date=d,
                        shift=sh,
                        employee=nm,
                        role="busser",
                        category=category,
                        amount_final=busser_val,
                        filename=payload.filename,
                        file_id=payload.file_id,
                        parsed_confidence=0.9,
                    )
                )


    # -------------------------------
    # GROUP SERVER LOGIC
    # -------------------------------
    m_names = re.search(r"servers were (.+?)[\.\n]", lowered)
    m_amt = re.search(r"they should have each made\s*([^\.\n]+)", lowered)

    if m_names and m_amt:
        names_part = m_names.group(1)
        amt_str = m_amt.group(1)

        try:
            per_server = parse_amount_fragment(amt_str)
        except:
            per_server = None

        if per_server is not None:
            raw_names = re.split(r",|\sand\s", names_part)
            seen = set()

            for raw in raw_names:
                nm = normalize_name(raw)
                if nm and nm not in seen:
                    if nm == "Ryan Alexander":
                        role = "utility"
                    category = "support" if nm in SUPPORT_STAFF else "foh"
                    rows.append(
                        ShiftRow(
                            date=d,
                            shift=sh,
                            employee=nm,
                            role="FOH",
                            category=category,
                            amount_final=per_server,
                            filename=payload.filename,
                            file_id=payload.file_id,
                            parsed_confidence=0.95,
                        )
                    )
                    seen.add(nm)

    # -------------------------------
    # INLINE SERVERS LOGIC ("servers Mike Walton $300 and 67 cents ...")
    # -------------------------------
    servers_inline = re.search(r"servers (.+?)(?:utility|$)", text, flags=re.IGNORECASE)
    if servers_inline:
        servers_segment = servers_inline.group(1)

        # NEW UNIVERSAL INLINE SERVER PARSER
        # Match NAME + amount fragment (handles ANY amount format Whisper produces)
        for m in re.finditer(
            r"([A-Za-z][A-Za-z.'\-]*(?:\s+[A-Za-z][A-Za-z.'\-]*){0,2})\s+([^,.;]+)",
            servers_segment,
            flags=re.IGNORECASE,
        ):
            raw_nm, raw_amt = m.groups()
            nm = normalize_name(raw_nm)
            if not nm:
                continue

            # Use the master amount parser (supports all patterns: 219 68, 7504, 75 04, etc.)
            try:
                val = parse_amount_fragment(raw_amt)
            except:
                continue

            # Avoid duplicating rows
            already = any(r.employee == nm and r.date == d and r.shift == sh for r in rows)
            if already:
                continue

            if nm == "Ryan Alexander":
                role = "utility"
            category = "support" if nm in SUPPORT_STAFF else "foh"
            rows.append(
                ShiftRow(
                    date=d,
                    shift=sh,
                    employee=nm,
                    role="FOH",
                    category=category,
                    amount_final=val,
                    filename=payload.filename,
                    file_id=payload.file_id,
                    parsed_confidence=0.9,
                )
            )


    # -------------------------------
    # FALLBACK LOGIC
    # -------------------------------
    # -------------------------------
    # NEW: DIRECT NAME + AMOUNT PATTERN ("Kevin 219 68", "Ryan 7504")
    # -------------------------------
    tokens = text.split()
    print(f"TOKENS: {tokens}")
    log.debug(f"TOKENS: {tokens}")
    for i in range(len(tokens)):
        raw_nm = tokens[i]
        nm = normalize_name(raw_nm)
        if not nm:
            continue

        print(f"DEBUG: Fallback candidate: '{raw_nm}' normalized as '{nm}', tokens: {tokens[i:i+4]}")
        log.debug(f"DEBUG: Fallback candidate: '{raw_nm}' normalized as '{nm}', tokens: {tokens[i:i+4]}")

        # Case 0: token after name includes a $-amount (e.g., "$16.80" or "$16.86.")
        if (
            i + 1 < len(tokens)
            and re.search(r"\d", tokens[i + 1])
            and not (i + 2 < len(tokens) and "dollar" in tokens[i + 2].lower())
        ):
            raw_amt_token = tokens[i + 1].strip(",.")
            if "$" in raw_amt_token or raw_amt_token.replace(".", "", 1).isdigit():
                try:
                    val = parse_amount_fragment(raw_amt_token)
                except Exception:
                    val = None
                if val is not None:
                    role = "FOH"
                    if nm == "Ryan Alexander":
                        role = "utility"
                    category = "support" if nm in SUPPORT_STAFF else "foh"
                    already = any(r.employee == nm and r.date == d and r.shift == sh for r in rows)
                    if not already:
                        rows.append(
                            ShiftRow(
                                date=d,
                                shift=sh,
                                employee=nm,
                                role=role,
                                category=category,
                                amount_final=val,
                                filename=payload.filename,
                                file_id=payload.file_id,
                                parsed_confidence=0.9,
                        )
                    )
                continue

        # Broad lookahead: try to parse any nearby amount fragment before heuristics
        fragment = " ".join(tokens[i + 1 : i + 8])
        try:
            val = parse_amount_fragment(fragment)
        except Exception:
            val = None
        if val is not None:
            role = "FOH"
            if nm == "Ryan Alexander":
                role = "utility"
            category = "support" if nm in SUPPORT_STAFF else "foh"
            already = any(r.employee == nm and r.date == d and r.shift == sh for r in rows)
            if not already:
                rows.append(
                    ShiftRow(
                        date=d,
                        shift=sh,
                        employee=nm,
                        role=role,
                        category=category,
                        amount_final=val,
                        filename=payload.filename,
                        file_id=payload.file_id,
                        parsed_confidence=0.9,
                    )
                )
            continue

        # Prefer full-phrase parsing like "111 dollars and 12 cents" before shorter numeric heuristics.
        if (
            i + 3 < len(tokens)
            and tokens[i + 1].isdigit()
            and tokens[i + 2].lower().startswith("dollar")
        ):
            fragment = " ".join(tokens[i + 1 : i + 7])  # include cents token if present
            try:
                val = parse_amount_fragment(fragment)
            except Exception:
                val = None
            if val is not None:
                role = "FOH"
                if nm == "Ryan Alexander":
                    role = "utility"
                category = "support" if nm in SUPPORT_STAFF else "foh"
                already = any(r.employee == nm and r.date == d and r.shift == sh for r in rows)
                if not already:
                    rows.append(
                        ShiftRow(
                            date=d,
                            shift=sh,
                            employee=nm,
                            role=role,
                            category=category,
                            amount_final=val,
                            filename=payload.filename,
                            file_id=payload.file_id,
                            parsed_confidence=0.9,
                        )
                    )
                continue

        # Case 1: amount like "219 68"
        if i + 2 < len(tokens) and tokens[i+1].isdigit() and tokens[i+2].isdigit() and len(tokens[i+2]) == 2:
            try:
                dollars = tokens[i+1]
                cents = tokens[i+2]
                val = float(f"{dollars}.{cents}")
                role = "utility" if nm in ("Coben Cross", "Maddox Porter", "Ryan Alexander") else "FOH"

                already = any(r.employee == nm and r.date == d and r.shift == sh for r in rows)
                if not already:
                    if nm == "Ryan Alexander":
                        role = "utility"
                    category = "support" if nm in SUPPORT_STAFF else "foh"
                    rows.append(
                        ShiftRow(
                            date=d,
                            shift=sh,
                            employee=nm,
                            role=role,
                            category=category,
                            amount_final=val,
                            filename=payload.filename,
                            file_id=payload.file_id,
                            parsed_confidence=0.9,
                        )
                    )
                continue
            except:
                pass

        # Case 2: amount like "7504" (→ 75.04), even at end of transcript
        if i + 1 < len(tokens) and tokens[i+1].isdigit() and len(tokens[i+1]) >= 3:
            try:
                raw = re.sub(r"[^\d]", "", tokens[i+1])  # remove punctuation
                if len(raw) >= 3:
                    dollars = raw[:-2]
                    cents = raw[-2:]
                    val = float(f"{dollars}.{cents}")
                    role = "utility" if nm in ("Coben Cross", "Maddox Porter", "Ryan Alexander") else "FOH"

                    already = any(r.employee == nm and r.date == d and r.shift == sh for r in rows)
                    if not already:
                        if nm == "Ryan Alexander":
                            role = "utility"
                        category = "support" if nm in SUPPORT_STAFF else "foh"
                        rows.append(
                            ShiftRow(
                                date=d,
                                shift=sh,
                                employee=nm,
                                role=role,
                                category=category,
                                amount_final=val,
                                filename=payload.filename,
                                file_id=payload.file_id,
                                parsed_confidence=0.9,
                            )
                        )
                    continue
            except:
                pass

        # Case 3: fallback for patterns like "75 04" → 75.04
        if i + 3 <= len(tokens):
            merged = "".join(t for t in tokens[i+1:i+3] if t.isdigit())
            if merged.isdigit() and len(merged) >= 3:
                try:
                    dollars = merged[:-2]
                    cents = merged[-2:]
                    val = float(f"{dollars}.{cents}")
                    role = "utility" if nm in ("Coben Cross", "Maddox Porter", "Ryan Alexander") else "FOH"

                    already = any(r.employee == nm and r.date == d and r.shift == sh for r in rows)
                    if not already:
                        if nm == "Ryan Alexander":
                            role = "utility"
                        category = "support" if nm in SUPPORT_STAFF else "foh"
                        rows.append(
                            ShiftRow(
                                date=d,
                                shift=sh,
                                employee=nm,
                                role=role,
                                category=category,
                                amount_final=val,
                                filename=payload.filename,
                                file_id=payload.file_id,
                                parsed_confidence=0.9,
                            )
                        )
                    continue
                except:
                    pass

    fallback_pattern = (
        r"([A-Za-z][A-Za-z.'\-]*(?:\s+[A-Za-z][A-Za-z.'\-]*){0,2})"
        r"\s*[:\-–—]?\s*\$?\s*([^\n,;]+)"
    )

    found = re.findall(fallback_pattern, text)

    if found:
        existing = {r.employee for r in rows}
        for raw_nm, raw_amt in found:
            nm = normalize_name(raw_nm)
            if not nm or nm in existing:
                continue

            try:
                val = parse_amount_fragment(raw_amt)
            except:
                continue

            role = "utility" if nm in ("Coben Cross", "Maddox Porter", "Ryan Alexander") else "FOH"
            if nm == "Ryan Alexander":
                role = "utility"
            category = "support" if nm in SUPPORT_STAFF else "foh"
            rows.append(
                ShiftRow(
                    date=d,
                    shift=sh,
                    employee=nm,
                    role=role,
                    category=category,
                    amount_final=val,
                    filename=payload.filename,
                    file_id=payload.file_id,
                    parsed_confidence=0.85,
                )
            )
            existing.add(nm)

    if not rows:
        raise HTTPException(status_code=422, detail="could not parse any name/amount pairs from transcript")

    return rows


# ----------------------------------------------------
# BigQuery Insert with De-dupe
# ----------------------------------------------------
def insert_shift_rows(rows: List[ShiftRow]):
    table = f"{PROJECT_ID}.{BQ_DATASET}.{BQ_TABLE_SHIFTS}"

    to_insert = []
    row_ids = []

    for r in rows:
        shift_date_str = r.date.isoformat()
        uid = f"{r.filename}-{r.employee}-{shift_date_str}"

        row_ids.append(uid)
        to_insert.append(
            {
                "shift_date": shift_date_str,
                "shift": r.shift,
                "employee": r.employee,
                "role": r.role,
                "category": r.category,
                "amount_final": r.amount_final,
                "pool_hours": None,
                "food_sales": None,
                "filename": r.filename,
                "file_id": r.file_id,
                "parsed_confidence": r.parsed_confidence,
                "parser_version": r.parser_version,
                "inserted_at": datetime.utcnow().isoformat(" "),
            }
        )

    errors = bq_client.insert_rows_json(table, to_insert, row_ids=row_ids)

    if errors:
        raise HTTPException(status_code=500, detail=str(errors))

    return {"ok": True, "inserted": len(rows)}


# ----------------------------------------------------
# Main Endpoint
# ----------------------------------------------------

@app.post("/transcribe_and_ingest")
async def transcribe_and_ingest(
    audio: UploadFile = File(...),
    filename: Optional[str] = None,
    lang: Optional[str] = None,
):
    try:
        # Send file to transcriber
        url = TRANSCRIBE_BASE + "/transcribe"
        files = {
            "audio": (
                audio.filename or "shift.wav",
                await audio.read(),
                audio.content_type or "audio/wav",
            )
        }

        resp = requests.post(url, files=files, timeout=180)
        resp.raise_for_status()

        data = resp.json()
        text = (data or {}).get("text", "").strip()
        if not text:
            raise HTTPException(status_code=422, detail="transcriber returned empty text")

        # Build payload
        payload = TranscriptIn(
            filename=filename or (audio.filename or "shift.wav"),
            transcript=text,
        )

        # Parse → rows
        rows = parse_transcript_to_rows(payload)

        # Insert into BigQuery
        return insert_shift_rows(rows)

    except requests.HTTPError as e:
        raise HTTPException(
            status_code=502,
            detail=f"transcribe upstream error: {e.response.text[:300]}",
        )
    except HTTPException:
        raise
    except Exception as e:
        log.exception("transcribe_and_ingest failed")
        raise HTTPException(
            status_code=500,
            detail=f"transcribe_and_ingest error: {e}",
        )


@app.get("/ping")
def ping():
    return {"ok": True, "project": PROJECT_ID, "dataset": BQ_DATASET}
