from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime
import os

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is required")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class UnifiedPrice(Base):
    __tablename__ = "unified_prices"

    id = Column(Integer, primary_key=True, index=True)
    asset = Column(String, unique=True, index=True)   # e.g., 'BTC' - canonical asset identifier
    price_usd = Column(Float)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

# Correct way to initialize the database
def init_db():
    Base.metadata.create_all(bind=engine)
