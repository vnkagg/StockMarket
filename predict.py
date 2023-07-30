import joblib
import numpy as np
import pandas as pd
from pathlib import Path
# import data_manager.scrape as scrape
from data_manager.manage import load_dataframe
# from tensorflow import keras
from keras.saving import load_model
import datetime
import yfinance as yf

n_features = 2


def predict(data, ticker):
    DIRECTORY = Path.cwd()/Path("./trained_models")
    for file in DIRECTORY.iterdir():
        if file.is_file() and ticker in file.name and 'model' in file.name:
            MODEL = load_model(file)
            break
    for file in DIRECTORY.iterdir():
        if file.is_file() and ticker in file.name and 'scaler' in file.name:
            SCALAR = joblib.load(open(file, "rb"))
            break
    X_INPUT_SCALED = SCALAR.transform(
        data.reshape(-1, 1)).reshape(-1, 1, n_features)
    PREDICTIONS_SCALED = MODEL.predict(X_INPUT_SCALED)
    PREDICTIONS = SCALAR.inverse_transform(PREDICTIONS_SCALED).reshape(-1)
    return PREDICTIONS[0]


def last_n_prices(df: pd.DataFrame, n_features):
    df = df.copy().set_index(['Date'])
    for i in range(n_features):
        df[f'{n_features}'] = df['Prediction'].shift(i)
    x = np.array(df.tail(1).values.astype(np.float32))
    return x


def main_predict(till_date, ticker):
    temp = yf.download(ticker, end=till_date).reset_index()
    last_existing_date = temp['Date'][-1:].dt.strftime('%Y-%m-%d').values[0]
    last_n_closing_prices = np.array(
        temp.tail(n_features)['Close'].values.astype(np.float32))

    iterate_dates_obj = datetime.datetime.strptime(
        last_existing_date, '%Y-%m-%d')
    last_existing_date_obj = datetime.datetime.strptime(
        last_existing_date, '%Y-%m-%d')
    target_date_obj = datetime.datetime.strptime(till_date, '%Y-%m-%d')

    if target_date_obj <= iterate_dates_obj:
        # return the actual stocks instead of predicting for now
        return temp['Close'][:target_date_obj.strftime('%Y-%m-%d')]

    df = pd.DataFrame({'Date': [], 'Prediction': []})
    iterate_dates_obj -= datetime.timedelta(days=n_features)
    i = -1
    while (iterate_dates_obj < last_existing_date_obj):
        iterate_dates_obj += datetime.timedelta(days=1)
        if iterate_dates_obj.weekday() > 4:
            continue
        i += 1
        entry = pd.DataFrame([{'Date': iterate_dates_obj.strftime('%Y-%m-%d'),
                              'Prediction': last_n_closing_prices[i]}])
        df = pd.concat([df, entry])

    iterate_dates_obj = datetime.datetime.strptime(
        last_existing_date, '%Y-%m-%d') + datetime.timedelta(days=1)
    while (iterate_dates_obj != target_date_obj):
        prediction = predict(last_n_prices(df, n_features), ticker)
        entry = pd.DataFrame([{'Date': iterate_dates_obj.strftime('%Y-%m-%d'),
                              'Prediction': prediction}])
        df = pd.concat([df, entry], ignore_index=True)
        iterate_dates_obj += datetime.timedelta(days=1)
    return df


ticker = 'AAPL'
till_date = '2023-08-05'
pred = main_predict(till_date, ticker)
# dir = Path.cwd()/Path('dataset')
# for file in dir.iterdir():
#     if file.is_file() and ticker in file.name:
#         df = pd.DataFrame(load_dataframe(
#             file_name=file, ticker="AAPL").copy())
#         break
# actual = df.loc[dates]
print("PREDICTIONS :", pred)
# print("ACTUAL :", actual)
