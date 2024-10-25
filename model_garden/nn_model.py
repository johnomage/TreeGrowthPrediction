# NN
import tensorflow as tf
from tensorflow import keras
from keras.models import Sequential
from keras.layers import Dense, LSTM, Flatten

# metrics
from keras.losses import MeanSquaredError


class LSTM:

    # RMSE
    def calculate_rmse(y_true, y_pred):
        mse = MeanSquaredError()(y_true, y_pred)
        return tf.sqrt(mse)