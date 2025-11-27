# app.py — Stunning Bloomberg-style dashboard (run with: streamlit run app.py)
import streamlit as st
import pandas as pd
from events_calendar import get_nfp_events
from price_fetcher import get_intraday_data
from impact_calculator import calculate_impact
import time

st.set_page_config(page_title="Macro Impact Tracker", layout="wide")
st.title("SPY Reaction to Non-Farm Payrolls")
st.markdown("**Real 1-minute data • Last 6 releases**")

events = get_nfp_events()
results = []

for _, row in events.iterrows():
    date_str = row['datetime_et'].strftime("%Y-%m-%d")
    with st.spinner(f"Loading {date_str}..."):
        prices = get_intraday_data("SPY", date_str, date_str)
        if prices is not None and len(prices) > 50:
            impact = calculate_impact(prices, row['datetime_et'])
            results.append({
                "Date": date_str,
                "5min": impact["5min"],
                "15min": impact["15min"],
                "30min": impact["30min"],
                "60min": impact["60min"]
            })
        time.sleep(12)  # Stay under free rate limit

if results:
    df = pd.DataFrame(results).set_index("Date")
    st.table(df.style.format("{:+.3f}%").background_gradient(cmap="RdYlGn", axis=None))
    st.success("Live data loaded!")
else:
    st.error("No data — check API key or rate limits")