import pandas as pd


# Fechas base
now = pd.Timestamp.now()

crrnt_full_date = now.strftime("%Y%m%d")          # p.ej. 20251101
crrnt_year      = now.year

prev_month_ts   = now - pd.DateOffset(months=1)
prev_month_year = prev_month_ts.year
prev_month_str  = prev_month_ts.strftime("%Y%m")  # p.ej. 202510
num_months_back = (now.year - prev_month_ts.year) * 12 + (now.month - prev_month_ts.month)
print(prev_month_str)
