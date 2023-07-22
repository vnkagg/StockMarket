from sklearn.model_selection import train_test_split
from data_manager.features import finalise_features
from data_manager.manage import save_pipeline
from model import load_pipeline
from pandas import DataFrame
from datetime import datetime


def train(date, ticker) -> None:
    print("debug")
    date = datetime(date).strftime('%Y-%m-%d')
    df: DataFrame = finalise_features(date, ticker)
    pipe_line = load_pipeline()

    model_dataset, unseen_dataset = train_test_split(
        df,
        test_size=0.2,
        shuffle=False,
        random_state=42
    )

    train, validation = train_test_split(
        model_dataset,
        test_size=0.2,
        shuffle=False,
        random_state=42
    )
    train_cols = df.columns.difference('close')
    X_train = train[train_cols]
    Y_train = train['close']

    X_validation = validation[train_cols]
    Y_validation = validation['close']

    pipe_line.fit(
        X_train, Y_train,
        epochs=100,
        batch_size=128,
        verbose=1,
        validation_data=(X_validation, Y_validation)
    )

    save_pipeline(pipe_line, date, ticker)


train('2023-07-10', 'AAPL')
