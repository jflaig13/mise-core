# Mise Web App
FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY mise_app/ ./mise_app/

# Copy transrouter (for payroll agent and brain sync)
COPY transrouter/ ./transrouter/

# Copy workflow specs (for roster and rules)
COPY workflow_specs/ ./workflow_specs/

# Copy inventory catalog (for product normalization)
COPY inventory_agent/inventory_catalog.json ./data/inventory_catalog.json

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PORT=8080

EXPOSE 8080

CMD ["sh", "-c", "uvicorn mise_app.main:app --host 0.0.0.0 --port ${PORT:-8080}"]
