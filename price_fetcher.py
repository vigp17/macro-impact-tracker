# price_fetcher.py — FIXED FOR POLYGON (1-minute bars, rate-limit safe)
from polygon import RESTClient
import pandas as pd
import time

# Your Polygon key
client = RESTClient("NSECWOrtkBkoZv6GB38LJEj5Wsp3HxCl")

def get_intraday_data(ticker: str, start_date: str, end_date: str, interval="minute"):
    print(f"Downloading {interval} data for {ticker} from {start_date} to {end_date}...", end="")
    try:
        # Polygon requires end_date = start_date + 1 day for single-day data
        if end_date == start_date:
            end_date = pd.to_datetime(end_date) + pd.Timedelta(days=1)
            end_date = end_date.strftime("%Y-%m-%d")
        
        aggs = client.get_aggs(ticker, 1, interval, start_date, end_date, limit=50000)
        if not aggs:
            print(" No data")
            return None
        df = pd.DataFrame(aggs)
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms', utc=True).dt.tz_convert('America/New_York')
        df = df.set_index('timestamp')[['close']].rename(columns={'close': 'Close'})
        print(f" {len(df)} bars ✓")
        return df
    except Exception as e:
        print(f" Error: {e}")
        return None
    
    # Rate limit safety — wait 1 second between calls
    time.sleep(1)

if __name__ == "__main__":
    data = get_intraday_data("SPY", "2024-10-04", "2024-10-04")
    if data is not None:
        print("\nSuccess! Last 5 rows:")
        print(data.tail())
    else:
        print("Test failed.")