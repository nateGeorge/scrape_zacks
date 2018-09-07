import pandas as pd

import scrape_zacks as sz

FILEPATH = '/home/nate/Dropbox/data/zacks/'

# find nearest upcoming earnings reports
latest_date = sz.get_latest_dl_date().strftime('%Y-%m-%d')
filename = FILEPATH + latest_date + '_esp_sells.csv'
sell_df = pd.read_csv(filename, parse_dates=['Reporting Date'], infer_datetime_format=True)
filename = FILEPATH + latest_date + '_esp_buys.csv'
buy_df = pd.read_csv(filename, parse_dates=['Reporting Date'], infer_datetime_format=True)

esp_df = pd.concat([sell_df, buy_df])

nearest_date = esp_df['Reporting Date'].min()
nearest_plus_1w = nearest_date + pd.Timedelta('7D')
within_week = esp_df[esp_df['Reporting Date'] < nearest_plus_1w]
# nearest_reports = esp_df.sort_values(by='Reporting Date')

# TODO: find stocks with large ESP, and earnings diff of more than 1 or 2 cents
# check if different from surprise last quarter
# need to also check revenue/EPS trend, technicals, and instutional investment

# find
