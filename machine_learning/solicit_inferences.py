from joblib import dump, load
import os
import sys
from os import path
from generate_training_data import capture_fred_series
import ta
import pandas as pd
import numpy as np

def solicit_inferences(fred_api_key):

    trained_columns = ['dff', 'bamlh0a0hym2', 'dcoilwtico', 'vixcls', 't10y3m', 'month', 'weekday', 'quarter', 'week', 'dff_aroon_indicator', 'dff_ema_indicator', 'dff_macd_diff', 'dff_trix', 'dff_sma_26', 'dff_sma_12', 'dff_sma_9', 'dff_diff', 'bamlh0a0hym2_aroon_indicator', 'bamlh0a0hym2_ema_indicator', 'bamlh0a0hym2_macd_diff', 'bamlh0a0hym2_trix', 'bamlh0a0hym2_sma_26', 'bamlh0a0hym2_sma_12', 'bamlh0a0hym2_sma_9', 'bamlh0a0hym2_diff', 'dcoilwtico_aroon_indicator', 'dcoilwtico_ema_indicator', 'dcoilwtico_macd_diff', 'dcoilwtico_trix', 'dcoilwtico_sma_26', 'dcoilwtico_sma_12', 'dcoilwtico_sma_9', 'dcoilwtico_diff', 'vixcls_aroon_indicator', 'vixcls_ema_indicator', 'vixcls_macd_diff', 'vixcls_trix', 'vixcls_sma_26', 'vixcls_sma_12', 'vixcls_sma_9', 'vixcls_diff', 'nasdaqcom_aroon_indicator', 'nasdaqcom_ema_indicator', 'nasdaqcom_macd_diff',
                    'nasdaqcom_trix', 'nasdaqcom_sma_26', 'nasdaqcom_sma_12', 'nasdaqcom_sma_9', 'nasdaqcom_log', 't10y3m_aroon_indicator', 't10y3m_ema_indicator', 't10y3m_macd_diff', 't10y3m_trix', 't10y3m_sma_26', 't10y3m_sma_12', 't10y3m_sma_9', 't10y3m_diff', 'month_aroon_indicator', 'month_ema_indicator', 'month_macd_diff', 'month_trix', 'month_sma_26', 'month_sma_12', 'month_sma_9', 'month_diff', 'weekday_aroon_indicator', 'weekday_ema_indicator', 'weekday_macd_diff', 'weekday_trix', 'weekday_sma_26', 'weekday_sma_12', 'weekday_sma_9', 'weekday_diff', 'quarter_aroon_indicator', 'quarter_ema_indicator', 'quarter_macd_diff', 'quarter_trix', 'quarter_sma_26', 'quarter_sma_12', 'quarter_sma_9', 'quarter_diff', 'week_aroon_indicator', 'week_ema_indicator', 'week_macd_diff', 'week_trix', 'week_sma_26', 'week_sma_12', 'week_sma_9', 'week_diff']

    print('Current working directory is: ',os.getcwd())
    model = load(os.path.join('data', 'random_forest_classifier.joblib'))

    fred_series_to_capture = ['DFF', 'BAMLH0A0HYM2',
                            'DCOILWTICO', 'VIXCLS', 'T10Y3M', 'NASDAQCOM']

    dataset = capture_fred_series(
        fred_series_to_capture=fred_series_to_capture, fred_api_key=fred_api_key)

    dataset.set_index(keys='date', inplace=True, drop=True, verify_integrity=True)
    dataset['month'] = dataset.index.month
    dataset['weekday'] = dataset.index.weekday
    dataset['quarter'] = dataset.index.quarter
    dataset['week'] = dataset.index.isocalendar().week

    dataset = dataset[dataset.index.dayofweek < 5]
    dataset.ffill(inplace=True)

    columns_to_make_technical_indicators_from = [col for col in dataset.columns]
    columns_to_make_technical_indicators_from

    for technical_analysis_column in columns_to_make_technical_indicators_from:
        dataset[technical_analysis_column+'_aroon_indicator'] = ta.trend.AroonIndicator(
            dataset[technical_analysis_column], window=14).aroon_indicator()
        dataset[technical_analysis_column+'_ema_indicator'] = ta.trend.EMAIndicator(
            dataset[technical_analysis_column], window=14).ema_indicator()
        dataset[technical_analysis_column+'_macd_diff'] = ta.trend.MACD(
            dataset[technical_analysis_column], window_slow=26, window_fast=12, window_sign=9).macd_diff()
        dataset[technical_analysis_column+'_trix'] = ta.trend.TRIXIndicator(
            dataset[technical_analysis_column], window=14).trix()
        dataset[technical_analysis_column+'_sma_26'] = ta.trend.SMAIndicator(
            dataset[technical_analysis_column], window=26).sma_indicator()
        dataset[technical_analysis_column+'_sma_12'] = ta.trend.SMAIndicator(
            dataset[technical_analysis_column], window=12).sma_indicator()
        dataset[technical_analysis_column+'_sma_9'] = ta.trend.SMAIndicator(
            dataset[technical_analysis_column], window=9).sma_indicator()
        if technical_analysis_column == 'nasdaqcom':
            dataset[technical_analysis_column +
                    '_log'] = np.log(dataset[technical_analysis_column])
        else:
            dataset[technical_analysis_column +
                    '_diff'] = dataset[technical_analysis_column].diff()

    dataset.drop(columns=['nasdaqcom'], inplace=True)

    dataset.head()
    dataset = dataset[trained_columns]
    most_recent_records = dataset.tail(1)

    prediction = model.predict(most_recent_records)

    if path.exists(os.path.join('data', 'prediction.csv')):
        prediction_df = pd.read_csv(os.path.join('data', 'prediction.csv'))
        prediction_df['date'] = pd.to_datetime(prediction_df['date'])

        if most_recent_records.index[0] in prediction_df['date'].values:
            print('Prediction already exists')
        else:
            prediction_df = prediction_df.append(
                {'date': most_recent_records.index[0], 'prediction': prediction[0]}, ignore_index=True)
    else:
        prediction_df = pd.DataFrame(
            {'date': most_recent_records.index, 'prediction': prediction})

    prediction_df.to_csv(os.path.join('data', 'prediction.csv'), index=False)

    print(prediction_df)

    return prediction

# Note that sys.argv[0] is the script name itself and can be ignored
fred_api_key = str(sys.argv[1])
solicit_inferences(fred_api_key = fred_api_key)