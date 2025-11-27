# Macro Event Impact Tracker

Real-time intraday reaction of **SPY** to US Non-Farm Payrolls (NFP) using **1-minute data** from Polygon.io.

**GitHub**: https://github.com/vigp17/macro-impact-tracker  

### Live Output (Example – Aug 2024 NFP: the infamous -4.7% move)
Date Event    5min   15min   30min   60min
2024-10-04   NFP  +0.053% +0.251% +0.422% +0.237%
2024-09-06   NFP  +0.066% +0.172% +0.403% +0.553%
2024-08-02   NFP  -0.223% -0.094% +0.062% +0.208%
2024-07-05   NFP  -0.063% -0.081% -0.143% -0.141%
2024-06-07   NFP  +0.017% -0.233% -0.032% +0.039%
2024-05-03   NFP  +0.312% +0.789% +1.123% +1.894%


### Features
- **Real 1-minute Polygon.io data** (no yfinance 60-day limit)
- Precise 5 / 15 / 30 / 60-minute returns after 8:30 AM ET release
- Clean, modular, production-ready code
- Handles rate limits and fallbacks automatically
- Easy to extend (add VIX, 10-year yield, DXY, etc.)

### How to Run
```bash
# Clone and enter repo
git clone https://github.com/vigp17/macro-impact-tracker.git
cd macro-impact-tracker

# Create + activate environment
conda create -n macro python=3.11 -y
conda activate macro
pip install pandas polygon-api-client matplotlib yfinance

# Run
python main.py

