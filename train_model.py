# from pathlib import Path
from sklearn.model_selection import train_test_split
from data_manager.features import finalise_features
from data_manager.scrape import build_database
from data_manager.manage import save_my_model, save_my_scaler
from model import load_model
import pandas as pd
from sklearn.preprocessing import MinMaxScaler


def train(date, ticker) -> None:
    # date = datetime(date).strftime('%Y-%m-%d')
    build_database(date, ticker)
    df: pd.DataFrame = finalise_features(date, ticker)

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
    TRAIN_COLS = df.columns.difference(['Close'])
    n_features = len(TRAIN_COLS)

    Y_TRAIN = train['Close'].values.reshape(-1, 1)
    Y_VALIDATION = validation['Close'].values.reshape(-1, 1)

    X_TRAIN = train[TRAIN_COLS].values.reshape(-1, n_features)
    X_VALIDATION = validation[TRAIN_COLS].values.reshape(-1, n_features)

    DATA_FOR_FITTING = model_dataset['Close'].values.reshape(-1, 1)

    MODEL = load_model()
    SCALER = MinMaxScaler()

    SCALER.fit(DATA_FOR_FITTING)

    X_TRAIN_SCALED = SCALER.transform(
        X_TRAIN.reshape(-1, 1)).reshape(-1, 1, n_features)
    Y_TRAIN_SCALED = SCALER.transform(Y_TRAIN.reshape(-1, 1)).reshape(-1)
    X_VALIDATION_SCALED = SCALER.transform(
        X_VALIDATION.reshape(-1, 1)).reshape(-1, 1, n_features)
    Y_VALIDATION_SCALED = SCALER.transform(
        Y_VALIDATION.reshape(-1, 1)).reshape(-1)

    MODEL.fit(
        X_TRAIN_SCALED, Y_TRAIN_SCALED,
        epochs=100,
        batch_size=128,
        verbose=True,
        validation_data=(X_VALIDATION_SCALED, Y_VALIDATION_SCALED)
    )

    save_my_model(MODEL, date, ticker)
    save_my_scaler(SCALER, date, ticker)


train('2023-07-21', 'AAPL')
# # print(Path.cwd())
