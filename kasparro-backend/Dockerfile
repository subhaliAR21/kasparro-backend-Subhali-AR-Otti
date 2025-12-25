# Stage 1: Builder
FROM python:3.11-slim AS builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies into a local folder
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt || \
    pip install --user --no-cache-dir fastapi uvicorn[standard] sqlalchemy psycopg2-binary requests pandas pydantic python-dotenv

# Stage 2: Final Runtime
FROM python:3.11-slim

WORKDIR /app

# Install only the runtime library for Postgres
RUN apt-get update && apt-get install -y libpq-dev && rm -rf /var/lib/apt/lists/*

# Copy only the installed packages from the builder stage
COPY --from=builder /root/.local /root/.local
COPY . .

# Ensure the local bin is in the PATH
ENV PATH=/root/.local/bin:$PATH

EXPOSE 8000

# Automated ETL Pipeline: Run ingestion first, then start the API
CMD python -m ingestion.pipeline && python -m uvicorn api.main:app --host 0.0.0.0 --port 8000
