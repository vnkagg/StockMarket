from pathlib import Path
import pandas as pd
import numpy as np
from data_manager.scrape import build_database
from data_manager.manage import load_dataframe
from data_manager.validation import authenticate_holidays
from sklearn.base import BaseEstimator, TransformerMixin


def finalise_features(date, ticker):
    build_database(date, ticker)
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
    n_features = 2
    new_df = data.copy()
    for i in range(1, n_features+1):
        new_df[f'closing_price_{i}_day_before'] = new_df['Close'].shift(i)
    new_df.dropna(inplace=True)
    return new_df

# def invert_feature_set():

# def features_previous_prices(X, Y):
#     n_features = 2
#     new_df = pd.DataFrame({'Close' : X})
#     for i in range(1, n_features+1):
#         new_df[i] = new_df['Close'].shift(i)
#     new_df.dropna(inplace=True)
#     return new_df.drop(['Close']).values.reshape(-1, 1, n_features)


class prep_features(BaseEstimator, TransformerMixin):
    def fit(self, X, Y):
        a = 1

    def transform(self, X):
        a = 1
