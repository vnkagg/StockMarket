import datetime
import tensorflow as tf
from tensorflow import keras
from keras import layers
from keras.optimizers.legacy import Adam
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler


def load_pipeline() -> keras.Sequential():
    tf.random.set_seed = datetime.datetime.now()
    myModel = keras.Sequential()
    n_features = 2  # do make a config file laterwards
    # First GRU Layer
    myModel.add(
        layers.GRU(
            units=100,
            return_sequences=True,
            input_shape=(1, n_features),
            activation='tanh'
        )
    )
    myModel.add(layers.Dropout(0.2))  # to prevent overfitting
    # Second GRU Layer
    myModel.add(
        layers.GRU(
            units=150,
            return_sequences=True,
            input_shape=(1, n_features)
        )
    )
    myModel.add(layers.Dropout(0.2))  # to prevent overfitting
    # Third GRU Layer
    myModel.add(
        layers.GRU(
            units=100,
            activation='tanh'
        )
    )
    myModel.add(layers.Dropout(0.2))  # to prevent overfitting
    # Output layer
    myModel.add(
        layers.Dense(
            units=1,
            kernel_initializer='he_uniform',
            activation='linear'
        )
    )
    # compile model
    myModel.compile(
        loss='mean_squared_error',
        optimizer=Adam(learning_rate=0.001),
        metrics=['mean_squared_error']
    )
    pipe_line = Pipeline(
        [
            ("scaling", MinMaxScaler()),
            ("model", myModel)
        ]
    )
    return pipe_line
