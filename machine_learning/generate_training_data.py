from fredapi import Fred
import pandas as pd
import numpy as np
import os
import datetime
from credentials import credentials

def create_date_table(start='1900-01-01', end=pd.Timestamp.today()):
    """This function is meant to create a master date table starting from a start date to an end date with many other columns attached to it that identify quarters, weeks, etc. 

    Args:
        start (str, optional): The start date for your master date table. Defaults to '1900-01-01'.
        end (DateTime, optional): The end date for your master date table. Defaults to pd.Timestamp.today().

    Returns:
        DataFrame: This is a dataframe containing one record for each day between the start and the end date.
    """

    def next_weekday(d, weekday):
        days_ahead = weekday - d.weekday()
        if days_ahead <= 0:
            days_ahead += 7
        return d + datetime.timedelta(days_ahead)

    start = pd.to_datetime(start) - pd.DateOffset(1)
    end = pd.to_datetime(end) + pd.DateOffset(1)

    df = pd.DataFrame({"date": pd.date_range(start, end)})
    df["week"] = df['date'].dt.isocalendar().week
    df["month"] = df['date'].dt.month
    df["quarter"] = df['date'].dt.quarter
    df['quarter_end_date'] = [date - pd.tseries.offsets.DateOffset(
        days=1) + pd.tseries.offsets.QuarterEnd() for date in df['date']]
    df['month_end_date'] = df['date'] + pd.tseries.offsets.MonthEnd(0)
    df['week_end_date'] = df['date'].map(lambda x: next_weekday(
        x, 6) if x.weekday() < 6 else x) - pd.DateOffset(days=1)
    df["year"] = df['date'].dt.year
    df["year_half"] = (df.quarter + 1) // 2
    df['new_week'] = df.week.diff() != 0
    df['new_month'] = df.month.diff() != 0
    df['new_quarter'] = df.quarter.diff() != 0
    df['last_day_of_month'] = df['new_month'].shift(-1)
    df['last_day_of_quarter'] = df['new_quarter'].shift(-1)
    df['new_year'] = df.year.diff() != 0
    df['new_year_half'] = df.year_half.diff() != 0

    df = df.iloc[1:-1, :]  # Remove the first and last record of the dataframe

    df['week'] = np.where(df['new_year'] == True, 1, df['week'])

    return df

def capture_fred_series(fred_series_to_capture, fred_api_key):
    """This function returns a dataframe containing all the values returned from FRED tied to a master calendar. 

    Args:
        fred_series_to_capture (list): A list of FRED series values that should be returned from FRED.
        fred_api_key (string): An account's FRED API key

    Returns:
        DataFrame: This dataframe contains all of the FRED series values along with a master calendar. 
    """

    master_calendar = create_date_table()
    master_calendar = master_calendar[['date']]

    for series in fred_series_to_capture:
        data = None
        data = retrieve_fred_data(
            fred_api_key=fred_api_key, fred_series=series)


        master_calendar = master_calendar.merge(data, on='date', how='left')

    return master_calendar

def retrieve_fred_data(fred_api_key, fred_series):
    """This function returns FRED data as a time series with dates for the latest value as it's known. 

    Args:
        fred_api_key (string): An account's FRED API key
        fred_series (string): The FRED series to capture

    Returns:
        dataframe, int: The first return is a dataframe of the FRED series, the second return is the number of months between observations.
    """
    fred = Fred(api_key=fred_api_key)

    data = fred.get_series(fred_series).to_frame().reset_index()
    data = data.set_axis(['date', fred_series.lower()], axis=1)
    return data

credentials = credentials()

fred_series_to_capture = ['T10Y2Y','DFF','BAMLH0A0HYM2','SP500','BAMLH0A0HYM2EY','DCOILWTICO','DTWEXBGS','VIXCLS','DJIA','NASDAQCOM','T10Y3M']

dataset = capture_fred_series(fred_series_to_capture=fred_series_to_capture, fred_api_key=credentials['FRED API Key'][0])

# Verify integrity just checks that the dataframe has no duplicate dates
dataset.set_index(keys='date', inplace=True, drop=True, verify_integrity=True)
# Remove all weekends from the data set since they are irrelevant
dataset = dataset[dataset.index.dayofweek < 5]

dataset.to_csv(os.path.join('data','dataset_raw.csv'))

if __name__ == '__main__':
    pass