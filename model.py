import datetime
import tensorflow as tf
from tensorflow import keras
from keras import layers
# from keras.optimizers import Adam
# from sklearn.pipeline import Pipeline
# from sklearn.preprocessing import MinMaxScaler
from data_manager.features import features_previous_prices


def load_model():
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
        optimizer=tf.keras.optimizers.Adam(learning_rate=0.0005),
        metrics=['mean_squared_error']
    )
    # pipe_line = Pipeline(
    #     [
    #         ("scaling", MinMaxScaler()),
    #         ("model", myModel)
    #     ]
    # )
    return myModel
