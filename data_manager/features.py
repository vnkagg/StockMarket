import datetime
from pathlib import Path
import pandas as pd
from data_manager.scrape import build_database
from data_manager.manage import load_dataframe
from data_manager.validation import authenticate_holidays


def finalise_features(date, ticker):
    build_database(date, ticker)
    path = Path.cwd()/Path(f'dataset/{ticker}_{date}.csv')
    df = pd.DataFrame(load_dataframe(file_name=path, ticker="AAPL").copy())
    return clean_features(df)


def clean_features(df: pd.DataFrame):
    df = df.set_index('Date').copy()
    # print(df.shape)
    df = df.asfreq('b')
    # print(df.isnull().sum())
    # print(df.shape)
    null_df = df[df.isnull().any(axis=1)]
    null_dates = null_df.index.tolist()
    holidays = authenticate_holidays(null_dates)
    df = df.drop(holidays).bfill(axis="rows")
    df['Close'] = df['Close'].values.astype('float32')
    n_features = 2  # do make a config file laterwards
    return features_previous_prices(df, n_features)

# Modify dataframe to have for every day, there are present
# closing prices of previous days to be input features


def features_previous_prices(data: pd.DataFrame, n_features):
    new_df = data.copy()
    for i in range(1, n_features+1):
        new_df[f'closing_price_{i}_day_before'] = new_df['Close'].shift(i)
    new_df.dropna(inplace=True)
    return new_df


# x = finalise_features('2023-07-10', "AAPL")
# print(x)
# print(x.isnull().sum())
