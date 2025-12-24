FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Force install core requirements directly
RUN pip install --no-cache-dir fastapi uvicorn[standard] sqlalchemy psycopg2-binary requests pandas pydantic python-dotenv

# Now copy the rest of your code
COPY . .

EXPOSE 8000

# Use the python -m syntax
# CMD ["python", "-m", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
CMD python -m ingestion.pipeline && python -m uvicorn api.main:app --host 0.0.0.0 --port 8000