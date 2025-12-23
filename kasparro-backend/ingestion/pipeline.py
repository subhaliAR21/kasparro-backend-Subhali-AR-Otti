import requests
import pandas as pd
import os
from datetime import datetime
from core.database import SessionLocal, UnifiedPrice
from schemas.price import PriceSchema

def fetch_coinpaprika():
    url = "https://api.coinpaprika.com/v1/tickers/btc-bitcoin"
    headers = {"Authorization": os.getenv("COINPAPRIKA_API_KEY")}
    resp = requests.get(url, headers=headers).json()
    return PriceSchema(
        source="coinpaprika",
        asset="BTC",
        price_usd=resp['quotes']['USD']['price']
    )

def fetch_coingecko():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    resp = requests.get(url).json()
    return PriceSchema(
        source="coingecko",
        asset="BTC",
        price_usd=resp['bitcoin']['usd']
    )

def fetch_csv():
    # Reads from the data/sample_prices.csv we created earlier
    df = pd.read_csv("data/sample_prices.csv")
    latest = df.iloc[-1]
    return PriceSchema(
        source="csv",
        asset=latest['asset'],
        price_usd=float(latest['price_usd'])
    )

def run_etl():
    db = SessionLocal()
    sources = [fetch_coinpaprika, fetch_coingecko, fetch_csv]
    
    print(f"Starting ETL run at {datetime.utcnow()}")
    for fetch_func in sources:
        try:
            data = fetch_func()
            new_record = UnifiedPrice(
                source=data.source,
                asset=data.asset,
                price_usd=data.price_usd,
                timestamp=data.timestamp
            )
            db.add(new_record)
            print(f"✅ Ingested from {data.source}")
        except Exception as e:
            print(f"❌ Failed {fetch_func.__name__}: {e}")
    
    db.commit()
    db.close()

if __name__ == "__main__":
    run_etl()