# Kasparro Backend ETL

## Setup
1. Add your `COINPAPRIKA_API_KEY` to the `.env` file.
2. Run the system: `docker-compose up -d`

## Ingest Data
Run the ETL pipeline manually:
`docker exec -it kasparro_api python -m ingestion.pipeline`

## View Data
Visit `https://kasparro-backend-subhali-ar-otti.onrender.com/`