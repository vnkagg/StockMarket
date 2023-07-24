import pickle
import numpy as np
from pathlib import Path
from pandas import DataFrame
from data_manager.scrape import get_stocks
from data_manager.features import clean_features


def predict(dates, ticker):
    model_file = list(
        Path.cwd()/Path("./trained_models").glob(f'*{ticker}*'))[0]
    model = pickle.load(open(model_file, "rb"))
    df = clean_features(get_stocks(dates, ticker))
    input_cols = df.columns.difference('close')
    scaler_path = list(
        Path.cwd()/Path("./feature_scalers").glob(f'*{ticker}*'))[0]
    scaler = pickle.load(open(scaler_path))
    predictions = scaler.inverse_transform(model.predict(df[input_cols]))
    return np.array(predictions).reshape(-1).copy()
