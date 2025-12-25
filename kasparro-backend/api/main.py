from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from core.database import init_db, SessionLocal, UnifiedPrice
import time
from fastapi.middleware.cors import CORSMiddleware

# 1. Define the app FIRST
app = FastAPI(title="Kasparro ETL API")

# 2. Add the middleware SECOND
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
def on_startup():
    for i in range(5):
        try:
            init_db()
            break
        except Exception:
            time.sleep(2)

@app.get("/")
def read_root():
    return {"status": "Backend is running", "database": "Connected"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/data")
def get_ingested_data(db: Session = Depends(get_db)):
    prices = db.query(UnifiedPrice).all()
    # Return data in format expected by frontend (normalized data)
    return [{"id": price.id, "source": "unified", "asset": price.asset, "price_usd": price.price_usd} for price in prices]
