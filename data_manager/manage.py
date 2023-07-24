import pickle
import joblib
import pandas as pd
from pathlib import Path
from tensorflow import keras
# from keras.models import save_model
from keras.saving import save_model


def load_dataframe(*, file_name, ticker: str):
    df = pd.read_csv(file_name, header=0)
    df['Date'] = pd.to_datetime(df['Date'])
    return df


def save_my_model(model, date, ticker):
    directory = Path.cwd()/Path(f"trained_models")
    try:
        for file in directory.glob('*'):
            if file.is_file() and ticker in file.name and 'model' in file.name:
                file.unlink()
                break
    except error as error:
        print(f"An error occured in deleting the model file: {error}")
    FILE_PATH = directory/Path(f"{ticker}_{date}_model.h5")
    with open(FILE_PATH, "wb") as file:
        save_model(model, FILE_PATH)


def save_my_scaler(scaler, date, ticker):
    directory = Path.cwd()/Path(f"trained_models")
    try:
        for file in directory.glob('*'):
            if file.is_file() and ticker in file.name and 'scaler' in file.name:
                file.unlink()
                break
    except error as error:
        print(f"An error occured in deleting the scaler file: {error}")
    FILE_PATH = directory/Path(f"{ticker}_{date}_scaler.pkl")
    with open(FILE_PATH, "wb") as file:
        joblib.dump(scaler, file)


def save_database(data, ticker, till_date):
    directory = Path.cwd()/Path("dataset")
    try:
        for file in directory.glob('*'):
            if file.is_file() and ticker in file.name:
                file.unlink()
    except error as error:
        print(f"An error occured in deleting the database file: {error}")
    db = pd.DataFrame(data)
    db.to_csv(directory/Path(f'{ticker}_{till_date}.csv'), index=False)
