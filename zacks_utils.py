import os
import glob

import pandas as pd
import numpy as np


FILEPATH = '/home/nate/Dropbox/data/zacks/'


def load_clean_buy_sell_df(filename):
    # auto date parse doesn't work
    df = pd.read_csv(filename, sep='\t')#, parse_dates=['Date Added'], infer_datetime_format=True)
    pct_cols = ['Dividend Yield(%)',
               'Price Movers: 1 Week(%)',
               'Price Movers: 4 Week(%)',
               'Biggest Est. Chg. Current Year(%)',
               'Biggest Est. Chg. Next Year(%)',
               'Biggest Surprise Last Qtr(%)',
               'Market Cap (mil)', 'P/E (F1)', 'PEG',
               'Projected Earnings Growth (1 Yr)(%)',
               'Projected Earnings Growth (3-5 Yrs)(%)',
               'Price Movers: 1 Day(%)',
               'Price / Sales']

    df.drop('Unnamed: 22', inplace=True, axis=1)
    df[pct_cols] = df[pct_cols].applymap(clean_pcts)
    df['Date Added'] = pd.to_datetime(df['Date Added'], format='%b %d,%Y')
    score_dict = {'A': 1,
                    'B': 2,
                    'C': 3,
                    'D': 4,
                    'E': 5,
                    'F': 6}

    score_cols = ['Value Score', 'Growth Score', 'Momentum Score', 'VGM Score']
    for s in score_cols:
        df[s] = df[s].replace(score_dict)

    return df


def clean_price(x):
    """
    prices look like $1,789.21
    """
    new_x = x.replace('$', '')
    new_x = new_x.replace(',', '')
    return float(new_x)


def clean_pcts(x):
    """
    the 'Chg. %' column and others have entries like +1.24%

    also removes commas
    """
    # if not enough data, will be '-' with investing.com
    if x == '-' or pd.isnull(x):
        return np.nan
    elif x == 'unch':
        return float(0)
    elif type(x) == float:
        return x

    new_x = x.replace('+', '')
    new_x = x.replace(',', '')
    new_x = new_x.replace('%', '')
    new_x = float(new_x) / 100
    return new_x


def get_last_open_trading_day():
    # use NY time so the day is correct -- should also correct for times after
    # midnight NY time and before market close that day
    today_ny = datetime.datetime.now(pytz.timezone('America/New_York'))
    ndq = mcal.get_calendar('NASDAQ')
    open_days = ndq.schedule(start_date=today_ny - pd.Timedelta(str(3*365) + ' days'), end_date=today_ny)
    # basically, this waits for 3 hours after market close if it's the same day
    return open_days.iloc[-1]['market_close'].date().strftime('%Y-%m-%d')


def get_latest_dl_date():
    # gets latest file date
    remove_leftover_files()
    daily_files = glob.glob(FILEPATH + '*.csv')
    if len(daily_files) == 0:
        return None

    daily_dates = [pd.to_datetime(f.split('/')[-1].split('_')[0].split('.')[0]) for f in daily_files]
    last_daily = max(daily_dates)
    return last_daily


def remove_leftover_files():
    filenames = []
    filenames.append(FILEPATH + 'Zacks Earnings Surprise Prediction - Zacks Investment Research.csv')
    filenames.append(FILEPATH + 'rank_5.xls')
    filenames.append(FILEPATH + 'rank_1.xls')
    for f in filenames:
        if os.path.exists(f): os.remove(f)


def load_latest_esp():
    # find nearest upcoming earnings reports
    latest_date = get_latest_dl_date().strftime('%Y-%m-%d')
    filename = FILEPATH + latest_date + '_esp_sells.csv'
    sell_df = pd.read_csv(filename, parse_dates=['Reporting Date'], infer_datetime_format=True)
    filename = FILEPATH + latest_date + '_esp_buys.csv'
    buy_df = pd.read_csv(filename, parse_dates=['Reporting Date'], infer_datetime_format=True)

    esp_df = pd.concat([sell_df, buy_df])
    esp_df['EPS_diff'] = esp_df['Most Accurate Estimate'] - esp_df['Consensus Estimate']

    return esp_df


def get_top_esp(esp_df):
    # filter for ones with greater than 2% difference, and greater than 2c diff
    # get diff between actual and estimate
    esp_df_filtered = esp_df[(esp_df['ESP'].abs() >= 0.02) & (esp_df['EPS_diff'].abs() >= 0.02)]

    nearest_date = esp_df_filtered['Reporting Date'].min()
    nearest_plus_1w = nearest_date + pd.Timedelta('7D')
    within_week = esp_df_filtered[esp_df_filtered['Reporting Date'] < nearest_plus_1w]

    # biggest relative
    biggest_relative_chg = within_week.sort_values(by='ESP')
    biggest_absolute_chg = within_week.sort_values(by='EPS_diff')
    sign_changes = esp_df_filtered[np.sign(esp_df_filtered['Consensus Estimate']) != np.sign(esp_df_filtered['Most Accurate Estimate'])]

    return biggest_relative_chg, biggest_absolute_chg, sign_changes


if __name__ == "__main__":
    esp_df = load_latest_esp()
    biggest_relative_chg, biggest_absolute_chg, sign_changes = get_top_esp(esp_df)


    # nearest_reports = esp_df.sort_values(by='Reporting Date')

    # TODO: find stocks with large ESP, and earnings diff of more than 1 or 2 cents
    # check if different from surprise last quarter
    # need to also check revenue/EPS trend, technicals, and instutional investment

    # find

    # screen
