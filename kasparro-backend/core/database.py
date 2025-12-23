from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime
import os

# Get URL from environment or fallback to localhost for local testing
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@db:5432/kasparro_etl")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class UnifiedPrice(Base):
    __tablename__ = "unified_prices"

    id = Column(Integer, primary_key=True, index=True)
    source = Column(String)  # 'coinpaprika', 'coingecko', or 'csv'
    asset = Column(String)   # e.g., 'BTC'
    price_usd = Column(Float)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

# Correct way to initialize the database
def init_db():
    Base.metadata.create_all(bind=engine)