FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies
COPY payroll_agent/CPM/engine/requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy roster module and data (needed by engine)
COPY roster /app/roster
COPY workflow_specs/roster /app/workflow_specs/roster

# Copy payroll_agent package structure (needed for module imports)
COPY payroll_agent/__init__.py /app/payroll_agent/__init__.py
COPY payroll_agent/CPM/__init__.py /app/payroll_agent/CPM/__init__.py

# Copy engine code
COPY payroll_agent/CPM/engine /app/payroll_agent/CPM/engine

# Set Python path for imports
ENV PYTHONPATH=/app

# Run the engine from app root so package imports work correctly
WORKDIR /app
CMD ["uvicorn", "payroll_agent.CPM.engine.payroll_engine:app", "--host", "0.0.0.0", "--port", "8080"]
