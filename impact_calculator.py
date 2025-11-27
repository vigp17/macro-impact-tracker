import pandas as pd
import numpy as np

def calculate_impact(price_df: pd.DataFrame, event_time_et: pd.Timestamp, windows=[5, 15, 30, 60]):
    if price_df is None or price_df.empty:
        return {f"{w}min": np.nan for w in windows}

    # Remove duplicates
    price_df = price_df[~price_df.index.duplicated(keep='last')]

    # First price AT or AFTER the event (first trade after release)
    post_release = price_df.loc[event_time_et:]
    if post_release.empty:
        return {f"{w}min": np.nan for w in windows}
    
    price_at_release = float(post_release.iloc[0]['Close'])

    results = {}
    for minutes in windows:
        target_time = event_time_et + pd.Timedelta(minutes=minutes)
        later_slice = price_df.loc[target_time:]
        if later_slice.empty:
            results[f"{minutes}min"] = np.nan
        else:
            price_later = float(later_slice.iloc[0]['Close'])
            pct = (price_later / price_at_release - 1) * 100
            results[f"{minutes}min"] = round(pct, 3)
    return results

if __name__ == "__main__":
    from price_fetcher import get_intraday_data
    event_time = pd.to_datetime("2024-10-04 08:30:00").tz_localize("America/New_York")
    prices = get_intraday_data("SPY", "2024-10-04", "2024-10-04")
    impact = calculate_impact(prices, event_time)
    print(impact)