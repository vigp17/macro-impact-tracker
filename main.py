# main.py
import pandas as pd
from events_calendar import get_nfp_events
from price_fetcher import get_intraday_data
from impact_calculator import calculate_impact

def main():
    events = get_nfp_events()
    results = []

    print("Macro Event Impact Tracker — Loading last 6 NFPs with real 1-minute data...\n")

    for _, row in events.iterrows():
        event_time = row['datetime_et']
        date_str = event_time.strftime("%Y-%m-%d")
        print(f"{date_str} NFP:")

        prices = get_intraday_data("SPY", date_str, date_str)   # uses Polygon 1-min bars

        if prices is not None and len(prices) > 50:
            impact = calculate_impact(prices, event_time)
            results.append({
                "Date": date_str,
                "5min":  impact.get("5min"),
                "15min": impact.get("15min"),
                "30min": impact.get("30min"),
                "60min": impact.get("60min")
            })
            print(f"  5min: {impact['5min']:+.3f}% | 15min: {impact['15min']:+.3f}% | 30min: {impact['30min']:+.3f}% | 60min: {impact['60min']:+.3f}%")
        else:
            print("  No data")

    if results:
        df = pd.DataFrame(results)
        print("\n" + "═" * 85)
        print("FINAL MACRO IMPACT TABLE — SPY REACTION TO NFP (real intraday moves)")
        print("═" * 85)
        print(df.to_string(index=False,
                           float_format=lambda x: f"{x:+.3f}%" if pd.notnull(x) else "—"))
        print("═" * 85)

if __name__ == "__main__":
    main()      
