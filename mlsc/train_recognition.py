""" Train a model. """

import math
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense
from sklearn.metrics import accuracy_score

from .debug import Debug

class TrainRecognition:
    def __init__(self, name, x_train, x_test, y_train, y_test):
        self.name = name
        self.x_train = x_train
        self.x_test = x_test
        self.y_train = y_train
        self.y_test = y_test

        self.debug = Debug(name + "-train")

        self.debug.log("Training with data sizes:")
        self.debug.log("x_train: " + str(len(self.x_train)))
        self.debug.log("y_train: " + str(len(self.y_train)))

        self.debug.log("x_test: " + str(len(self.x_test)))
        self.debug.log("y_test: " + str(len(self.y_test)))

    def train(self):

        self.build_model()
        self.fit()
        self.predict()

    def build_model(self):
        self.debug.log("Build model.")
        self.model = Sequential()
        self.model.add(Dense(units=32, activation='relu', input_dim=len(self.x_train.columns)))
        self.model.add(Dense(units=64, activation='relu'))
        self.model.add(Dense(units=1, activation='sigmoid'))

        self.model.compile(loss='binary_crossentropy', optimizer='sgd', metrics='accuracy')

    def fit(self):
        self.debug.log("Fit.")
        self.model.fit(self.x_train, self.y_train, epochs=200, batch_size=32)

    def predict(self):
        self.debug.log("Predict.")
        y_hat = self.model.predict(self.x_test)
        y_hat = [0 if val < 0.5 else 1 for val in y_hat]

        print(accuracy_score(self.y_test, y_hat))

    def save(self):
        self.debug.log("Save: " + self.name)
        self.model.save(self.name)
