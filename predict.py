import joblib
import numpy as np
import pandas as pd
from pathlib import Path
from data_manager.scrape import get_stocks
from data_manager.features import clean_features
from data_manager.manage import load_dataframe
from tensorflow import keras
from keras.saving import load_model


def predict(dates, ticker):
    n_features = 2
    DIRECTORY = Path.cwd()/Path("./trained_models")
    for file in DIRECTORY.iterdir():
        if file.is_file() and ticker in file.name and 'model' in file.name:
            MODEL = load_model(file)
            break
    for file in DIRECTORY.iterdir():
        if file.is_file() and ticker in file.name and 'scaler' in file.name:
            SCALAR = joblib.load(open(file, "rb"))
            break
    df = get_stocks(dates, ticker)
    input_cols = df.columns.difference(['Close'])
    # print(input_cols)
    X_INPUT = df[input_cols].values
    print(X_INPUT)
    X_INPUT_SCALED = SCALAR.transform(
        X_INPUT.reshape(-1, 1)).reshape(-1, 1, n_features)
    PREDICTIONS_SCALED = MODEL.predict(X_INPUT_SCALED)
    PREDICTIONS = SCALAR.inverse_transform(PREDICTIONS_SCALED).reshape(-1)
    print(PREDICTIONS, PREDICTIONS_SCALED)
    return PREDICTIONS


ticker = 'AAPL'
dates = ['2023-06-24', '2023-06-25', '2023-06-26', '2023-06-27', '2023-06-28']
pred = predict(dates, ticker)
dir = Path.cwd()/Path('dataset')
for file in dir.iterdir():
    if file.is_file() and ticker in file.name:
        df = pd.DataFrame(load_dataframe(
            file_name=file, ticker="AAPL").copy())
        break
# actual = df.loc[dates]
print("PREDICTIONS :", pred)
# print("ACTUAL :", actual)
