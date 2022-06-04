from datetime import datetime
import pandas as pd

def check_price(checkedin):
    now = datetime.now()
    old_count = 0
    cutoff_time = now - pd.DateOffset(seconds = 10)
    for time in checkedin:
        if time < cutoff_time:
            old_count = old_count + 1
    price = 2 + len(checkedin) - old_count
    return price