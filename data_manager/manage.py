import pickle
import pandas as pd
from pathlib import Path

def load_dataframe(*, file_name, ticker:str):
    df = pd.read_csv(file_name, header=0)
    df['date'] = pd.to_datetime(df['date'])
    df_ticker = df[df['symbol'] == ticker]
    df_ticker = df_ticker.set_index('date')
    return df_ticker

def save_pipeline(pipeline, date, ticker):
    directory = Path.cwd()/Path(f"../trained_models")
    try:
        for file in directory.glob('*'):
            if file.is_file() and ticker not in file.name:
                file.unlink()
    except error as error:
        print(f"An error occured in deleting the model file: {error}")
    pickle.dump(directory/Path(f"{ticker}_{date}.pkl"), pipeline)

def save_database(data, ticker, till_date):
    directory = Path.cwd()/Path("./dataset")
    try:
        for file in directory.glob('*'):
            if file.is_file() and ticker not in file.name:
                file.unlink()
    except error as error:
        print(f"An error occured in deleting the database file: {error}")
    db = pd.DataFrame(data)
    db.to_csv(directory/Path(f'{ticker}_{till_date}.csv'), index=False)