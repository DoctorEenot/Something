from keras.models import Sequential
from keras.layers import Dense, Activation

import keras.backend as K
import tensorflow as tf
import keras

class AI:
    def __init__(self):
        self.model = Sequential([
    Dense(200, input_dim=6),
    Activation('relu'),
    Dense(100),
    Activation('tanh'),
    Dense(1),
    Activation('sigmoid'),])
        #self.wnd.update()
        self.model.compile(optimizer='adam',
              loss='mean_absolute_error',
              metrics=['accuracy'])