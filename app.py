# app.py (run with: streamlit run app.py)
import streamlit as st
import pandas as pd
from events_calendar import get_nfp_events
from price_fetcher import get_intraday_data
from impact_calculator import calculate_impact
import time

# --- CONFIG ---
st.set_page_config(page_title="Macro Impact Tracker", layout="wide")
st.title("SPY Reaction to Non-Farm Payrolls")
st.markdown("**Real 1-minute data • Last 6 releases**")

# --- SIDEBAR SETTINGS ---
with st.sidebar:
    st.header("Settings")
    # Allow user to paste key if hardcoded one fails
    api_key_input = st.text_input("Polygon API Key (Optional)", type="password")
    if api_key_input:
        import os
        os.environ["POLYGON_API_KEY"] = api_key_input

# --- MAIN LOGIC ---
events = get_nfp_events()
results = []
progress_bar = st.progress(0)
status_text = st.empty()

total_events = len(events)

for i, (index, row) in enumerate(events.iterrows()):
    date_str = row['datetime_et'].strftime("%Y-%m-%d")
    status_text.text(f"Fetching data for NFP Release: {date_str}...")
    
    # Update progress
    progress_bar.progress((i + 1) / total_events)

    # Fetch Data
    prices = get_intraday_data("SPY", date_str, date_str)
    
    if prices is not None and len(prices) > 50:
        impact = calculate_impact(prices, row['datetime_et'])
        results.append({
            "Date": date_str,
            "5min": impact.get("5min"),
            "15min": impact.get("15min"),
            "30min": impact.get("30min"),
            "60min": impact.get("60min")
        })
    else:
        st.warning(f" No data for {date_str}. Check if market was open or API limit reached.")
    
    # Sleep to respect Polygon Free Tier (5 calls/min = 12s sleep)
    # If you have a paid key, you can reduce this to 0.1
    time.sleep(12) 

status_text.text("Done!")

# --- DISPLAY RESULTS ---
if results:
    df = pd.DataFrame(results).set_index("Date")
    
    st.subheader("Impact Analysis Table")
    # Display colorful table
    st.table(df.style.format("{:+.2f}%").background_gradient(cmap="RdYlGn", axis=None, vmin=-1, vmax=1))
    
    st.success(" Analysis Complete")
    
    # Visualize the first event as an example
    st.subheader(f"Price Action Example: {results[0]['Date']}")
    st.line_chart(prices['Close'] if 'prices' in locals() and prices is not None else [])

else:
    st.error(" No data loaded. Please check:")
    st.write("1. Is your Polygon API Key valid?")
    st.write("2. Did you hit the rate limit (5 calls/min)?")
    st.write("3. Is the market closed on these dates?")
