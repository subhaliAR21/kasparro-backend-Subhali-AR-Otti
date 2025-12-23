import requests
import os
from dotenv import load_dotenv

load_dotenv()

# 1. Test CoinPaprika (Requires Key)
# Make sure you have COINPAPRIKA_API_KEY=your_key in your .env file
paprika_key = os.getenv("COINPAPRIKA_API_KEY")
paprika_url = "https://api.coinpaprika.com/v1/tickers/btc-bitcoin"
headers = {"Authorization": paprika_key}

try:
    p_resp = requests.get(paprika_url, headers=headers)
    p_data = p_resp.json()
    print("--- CoinPaprika BTC Price ---")
    print(f"Symbol: {p_data.get('symbol')}")
    print(f"Price USD: {p_data.get('quotes', {}).get('USD', {}).get('price')}")
except Exception as e:
    print(f"CoinPaprika Error: {e}")

print("\n" + "="*30 + "\n")

# 2. Test CoinGecko (Public / Demo API)
gecko_url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd&include_24hr_vol=true"

try:
    g_resp = requests.get(gecko_url)
    g_data = g_resp.json()
    print("--- CoinGecko BTC Price ---")
    print(f"Price USD: {g_data.get('bitcoin', {}).get('usd')}")
except Exception as e:
    print(f"CoinGecko Error: {e}")