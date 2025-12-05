from fastapi import FastAPI, UploadFile, HTTPException
from typing import Optional
import os, tempfile, logging
import whisper

from transcribe.cleanup.llm_cleanup import LlmCleanupClient

app = FastAPI()
log = logging.getLogger("uvicorn")
MODEL_DIR = os.environ.get("WHISPER_CACHE_DIR", "/app/whisper-models")
_model = None
cleanup_client = LlmCleanupClient()


def load_model():
    global _model
    if _model is None:
        try:
            os.environ.setdefault("TMPDIR", "/tmp")
            _model = whisper.load_model("tiny.en", download_root=MODEL_DIR)  # CPU, English-only, fast
            log.info("Whisper tiny.en loaded from %s", MODEL_DIR)
        except Exception as e:
            log.exception("Model load failed")
            raise HTTPException(status_code=500, detail=f"model load error: {e}")
    return _model


def cleanup_transcript(raw_text: str) -> str:
    """Run the LLM cleanup layer between Whisper and the engine.

    Keeping cleanup here stabilizes the text before payroll parsing so the
    engine sees consistent spacing, casing, and punctuation.
    """

    return cleanup_client.clean_text(raw_text)


@app.get("/ping")
def ping():
    return {"pong": True}


@app.post("/transcribe")
async def transcribe(audio: UploadFile, lang: Optional[str] = None):
    path = None
    try:
        suffix = (os.path.splitext(getattr(audio, "filename", "") or "")[1]) or ".wav"
        with tempfile.NamedTemporaryFile(delete=False, dir="/tmp", suffix=suffix) as tmp:
            tmp.write(await audio.read())
            path = tmp.name

        model = load_model()

        result = model.transcribe(
            path,
            language=(lang or None),
            fp16=False,
            verbose=False,
            initial_prompt="write all numbers as digits, like 243.70 not words",
        )

        # Clean the raw Whisper text before the engine sees it to reduce
        # downstream edge cases.
        raw_text = (result.get("text") or "").strip()
        cleaned_text = cleanup_transcript(raw_text)

        return {
            "text": cleaned_text,
            "raw_text": raw_text,
            "language": result.get("language"),
        }

    except Exception as e:
        log.exception("transcribe failed")
        raise HTTPException(status_code=500, detail=f"transcribe error: {e}")

    finally:
        if path:
            try:
                os.remove(path)
            except Exception:
                pass
