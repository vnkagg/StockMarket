from pathlib import Path
import pandas as pd
import numpy as np
from data_manager.manage import load_dataframe
from data_manager.validation import authenticate_holidays


def finalise_features(date, ticker):
    path = Path.cwd()/Path(f'dataset/{ticker}_{date}.csv')
    df = pd.DataFrame(load_dataframe(file_name=path, ticker="AAPL").copy())
    return clean_features(df)


def clean_features(df: pd.DataFrame):
    df = df.set_index('Date').copy()
    df = df.asfreq('b')
    null_df = df[df.isnull().any(axis=1)]
    null_dates = null_df.index.tolist()
    holidays = authenticate_holidays(null_dates)
    df = df.drop(holidays).bfill(axis="rows")
    df['Close'] = df['Close'].values.astype('float32')
    n_features = 2
    return features_previous_prices(df, n_features)
    # return df


def features_previous_prices(data: pd.DataFrame, n_features):
    data = data.copy()
    for i in range(1, n_features + 1):
        data[f'CLOSING_PRICE_{i}_DAYS_AGO'] = data['Close'].shift(i)
    data.dropna(inplace=True)
    return data
