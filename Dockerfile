FROM python:3.11-slim

# Don't buffer Python output
ENV PYTHONUNBUFFERED=1

# Workdir inside the container
WORKDIR /app

# Install dependencies for the ENGINE service
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy the engine package, roster module, and roster data into the image
COPY engine ./engine
COPY roster ./roster
COPY workflow_specs/roster ./workflow_specs/roster

# Cloud Run will send traffic to $PORT
ENV PORT=8080

# Start the FastAPI app from engine.payroll_engine:app
CMD ["python", "-m", "uvicorn", "engine.payroll_engine:app", "--host", "0.0.0.0", "--port", "8080"]
