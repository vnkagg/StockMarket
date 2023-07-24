# from pathlib import Path
from sklearn.model_selection import train_test_split
from data_manager.features import finalise_features
from data_manager.manage import save_pipeline
from model import load_pipeline
from datetime import datetime
import numpy as np
import pandas as pd


def train(date, ticker) -> None:
    # date = datetime(date).strftime('%Y-%m-%d')
    df: pd.DataFrame = finalise_features(date, ticker)
    pipe_line = load_pipeline()

    model_dataset, unseen_dataset = train_test_split(
        df,
        test_size=0.2,
        shuffle=False,
    )

    train, validation = train_test_split(
        model_dataset,
        test_size=0.2,
        shuffle=False,
    )

    model_dataset = pd.DataFrame(model_dataset)
    unseen_dataset = pd.DataFrame(unseen_dataset)
    train = pd.DataFrame(train)
    validation = pd.DataFrame(validation)

    Y_train = train['Close'].values.reshape(-1, 1)
    Y_validation = validation['Close'].values.reshape(-1, 1)

    train_cols = df.columns.difference(['Close'])

    X_train = train[train_cols].values.reshape(-1, len(train_cols) - 1)
    X_validation = validation[train_cols].values.reshape(
        -1, len(train_cols) - 1)

    pipe_line.fit(
        X_train, Y_train,
        model__epochs=100,
        model__batch_size=128,
        model__verbose=1,
        model__validation_data=(X_validation, Y_validation)
    )

    save_pipeline(pipe_line, date, ticker)


train('2023-07-10', 'AAPL')
# print(Path.cwd())
