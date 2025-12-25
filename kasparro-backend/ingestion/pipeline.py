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

    # Collect prices by asset for normalization
    asset_prices = {}

    for fetch_func in sources:
        try:
            data = fetch_func()
            asset = data.asset
            if asset not in asset_prices:
                asset_prices[asset] = []
            asset_prices[asset].append(data.price_usd)
            print(f"✅ Fetched from {data.source}: {asset} = ${data.price_usd}")
        except Exception as e:
            print(f"❌ Failed {fetch_func.__name__}: {e}")

    # Create unified records (average prices across sources)
    for asset, prices in asset_prices.items():
        avg_price = sum(prices) / len(prices)
        unified_record = UnifiedPrice(
            asset=asset,
            price_usd=round(avg_price, 2),
            timestamp=datetime.utcnow()
        )
        db.add(unified_record)
        print(f"✅ Unified {asset}: ${avg_price:.2f} (from {len(prices)} sources)")

    db.commit()
    db.close()

if __name__ == "__main__":
    run_etl()