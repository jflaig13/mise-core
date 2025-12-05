FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install CPU-only PyTorch first
RUN python -m pip install --no-cache-dir --upgrade pip \
 && python -m pip install --no-cache-dir --index-url https://download.pytorch.org/whl/cpu torch torchvision torchaudio

COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt

# Copy the full transcribe package into the image
COPY . /app/transcribe
ENV PYTHONPATH=/app

# Pre-download tiny English Whisper model into the image
ENV WHISPER_CACHE_DIR=/app/whisper-models
RUN python -c "import transcribe.app, whisper, os; whisper.load_model('tiny.en', download_root=os.environ.get('WHISPER_CACHE_DIR'))" \
 && echo 'Whisper model cached.'

ENV PORT=8080
CMD ["python","-m","uvicorn","transcribe.app:app","--host","0.0.0.0","--port","8080","--workers","1"]
