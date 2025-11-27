import pandas as pd

NFP_DATES = [
    "2024-10-04 08:30:00",  # Oct 2024
    "2024-09-06 08:30:00",  # Sep 2024
    "2024-08-02 08:30:00",  # Aug 2024
    "2024-07-05 08:30:00",  # Jul 2024
    "2024-06-07 08:30:00",  # Jun 2024
    "2024-05-03 08:30:00",  # May 2024
]

def get_nfp_events():
    events = []
    for date_str in NFP_DATES:
        dt = pd.to_datetime(date_str).tz_localize('America/New_York')
        events.append({
            'event': 'Non-Farm Payrolls',
            'datetime_et': dt
        })
    return pd.DataFrame(events)

if __name__ == "__main__":
    print(get_nfp_events())