from fastapi import FastAPI, UploadFile, HTTPException
from typing import Optional
import os, tempfile, logging
import whisper

app = FastAPI()
log = logging.getLogger("uvicorn")
MODEL_DIR = os.environ.get("WHISPER_CACHE_DIR", "/app/whisper-models")
_model = None

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
            initial_prompt="write all numbers as digits, like 243.70 not words"
        )

        text = (result.get("text") or "").strip()
        return {"text": text, "language": result.get("language")}

    except Exception as e:
        log.exception("transcribe failed")
        raise HTTPException(status_code=500, detail=f"transcribe error: {e}")

    finally:
        if path:
            try:
                os.remove(path)
            except Exception:
                pass
