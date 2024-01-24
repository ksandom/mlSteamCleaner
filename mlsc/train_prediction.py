""" Train a prediction model. """

import math
# from tensorflow.keras.models import Sequential, load_model
# from tensorflow.keras.layers import Dense

import tensorflow as tf

import pandas as pd
from tensorflow import keras
import matplotlib.pyplot as plt
from tensorflow.keras import layers

from sklearn.metrics import accuracy_score

from .debug import Debug

class TrainPrediction:
    def __init__(self, name, x_train, x_test, y_train, y_test, full_test_data):
        self.name = name
        self.x_train = x_train
        self.x_test = x_test
        self.y_train = y_train
        self.y_test = y_test
        self.full_test_data = full_test_data
        self.epochs = 300

        self.model_path = "models/" + self.name

        self.debug = Debug(name + "-train")
        self.debug = Debug(self.model_path)

        self.debug.log("Training with data sizes:")
        self.debug.log("x_train: " + str(len(self.x_train)))
        self.debug.log("y_train: " + str(len(self.y_train)))

        self.debug.log("x_test: " + str(len(self.x_test)))
        self.debug.log("y_test: " + str(len(self.y_test)))


        print(tf.__version__)

    def train(self):

        self.build_model()
        self.fit()
        print()
        self.predict()
        self.save()

    def build_model(self):
        self.debug.log("Build model.")

        # self.model = Sequential()
        # self.model.add(Dense(units=32, activation='relu', input_dim=len(self.x_train.columns)))
        # self.model.add(Dense(units=64, activation='relu'))
        # self.model.add(Dense(units=1, activation='sigmoid'))
        #
        # self.model.compile(loss='binary_crossentropy', optimizer='sgd', metrics='accuracy')

        self.model = keras.Sequential([
            layers.Dense(units=32, activation='relu', input_dim=len(self.x_train.columns)),
            layers.Dense(64, activation='relu'),
            layers.Dense(64, activation='relu'),
            layers.Dense(1)
            ])

        metrics = [[
            'accuracy',
            'mse',
            'mae',
            # 'loss'
            ]]
        # metrics = 'accuracy'


        self.model.compile(
            loss='mean_absolute_error',
            optimizer=tf.keras.optimizers.Adam(0.001),
            metrics=metrics)


    def fit(self):
        self.debug.log("Fit.")
        early_stop = keras.callbacks.EarlyStopping(monitor='val_loss', patience=10)
        # early_stop = keras.callbacks.EarlyStopping(monitor='mse', patience=10)
        call_backs = []
        # call_backs.append(early_stop)

        history = self.model.fit(self.x_train, self.y_train, epochs=self.epochs, batch_size=32, validation_split = 0.2, callbacks=call_backs)

        if early_stop.stopped_epoch > 0:
            self.epochs = early_stop.stopped_epoch

        self.plot_loss(history)

    def get_plot_file_name(self, name):
        return self.model_path + '-' + name + '.png'

    def plot_stats(self, name, line1, line2, scale=False):
        plt.figure()
        plt.title(name)
        plt.plot(line1, label='loss')
        plt.plot(line2, label='val_loss')
        if (scale):
            plt.ylim([0, scale])
        plt.xlabel('Epoch')
        plt.ylabel('Error')
        plt.legend()
        plt.grid(True)

        plt.savefig(self.get_plot_file_name(name), bbox_inches='tight', dpi=600)
        plt.close()

    def plot_loss(self, history):
        self.plot_stats('loss', history.history['loss'], history.history['val_loss'], 0.05)

        hist = pd.DataFrame(history.history)
        hist['epoch'] = history.epoch

        self.plot_stats('error-avg', hist['mae'], hist['val_mae'])
        self.plot_stats('error-squared', hist['mse'], hist['val_mse'])

        print (hist.tail())



    def predict(self):
        self.debug.log("Predict.")
        # y_hat = self.model.predict(self.x_test)
        # y_hat = [0 if val < 0.5 else 1 for val in y_hat]

        # print("accuracy_score: " + str(accuracy_score(self.y_test, y_hat)))

        stats = self.model.evaluate(self.x_test, self.y_test, return_dict=True, verbose=0)

        print(stats)

        # TODO Is full_test_data needed?
        # test_predictions = self.model.predict(self.full_test_data).flatten()
        test_predictions = self.model.predict(self.x_test).flatten()

        # plt.figure()
        plt.close()
        a = plt.axes(aspect='equal')
        print(len(self.x_test), len(test_predictions))
        plt.scatter(self.y_test, test_predictions)
        plt.xlabel('True Values')
        plt.ylabel('Predictions')
        lims = [0, 1.5]
        plt.title('Predictions vs reality for ' + str(self.epochs) + ' epochs')
        plt.xlim(lims)
        plt.ylim(lims)
        _ = plt.plot(lims, lims)

        plt.savefig(self.get_plot_file_name('predictions'), bbox_inches='tight', dpi=600)
        plt.close()



    def save(self):
        self.debug.log("Save: " + self.name)
        self.model.save(self.model_path)
