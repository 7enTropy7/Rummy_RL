import tensorflow as tf
import numpy as np
from keras.models import Sequential, Model
from keras.layers import Dense, Dropout, Activation, Flatten, Input
from keras.layers import Convolution2D, MaxPooling2D
from keras.utils import np_utils

class Brain():
    def __init__(self, input_shape=(4,13,1)):
        self.input_shape = input_shape
        self.model = self.build_model()

    def build_model(self):
        visible = Input(shape=self.input_shape)
        x = Convolution2D(32, kernel_size=3, activation='relu',padding='same')(visible)
        x = MaxPooling2D(pool_size=(2, 2))(x)
        flat = Flatten()(x)
        print(flat.shape)
        suit = Dense(4, activation='softmax')(flat)
        value = Dense(13, activation='softmax')(flat)
        model = Model(inputs=visible, outputs=[suit, value])
        
        print(model.summary())
        return model