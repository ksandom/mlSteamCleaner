""" Make a prediction. """

import sys
import math

import tensorflow as tf

import pandas as pd
# import pandas.DataFrame
# from tensorflow import keras
from tensorflow.keras.models import Sequential, load_model
import matplotlib.pyplot as plt
# from tensorflow.keras import layers

# from sklearn.metrics import accuracy_score

from .debug import Debug

class Predict:
    def __init__(self, model):
        print()
        self.debug = Debug("Predict")

        self.debug.log("Model: " + model)
        # self.answer_field = 'answer_value'

        self.columns = 9
        self.unScaled = 0.1
        self.nUnScaled = self.unScaled * -1
        self.angle_base = math.pi / 800

        self.debug.log("Tensorflow version: " + str(tf.__version__))

        self.load_model(model)

    def load_model(self, model):
        self.debug.log("Load model " + model)

        self.model = load_model("models/" + model)

    def load_sample(self, sample_file):
        self.debug.log("Load sample " + sample_file)

        self.df_raw = pd.read_csv(sample_file)
        self.df_raw_without_answer = self.df_raw[:-1]
        self.df_answers = self.df_raw['angleDiff']
        self.df_prediction_beginning = self.df_raw_without_answer['angleDiff']


        # self.prediction_input = pd.DataFrame([self.df_raw_without_answer['angleDiffDiff']])
        self.prediction_input = {}
        index =0
        for col in self.df_raw_without_answer['angleDiffDiff']:
            key = 'angleDiffDiff_' + str(index)
            self.prediction_input[key] = {}
            self.prediction_input[key][0] = self.transform_for_prediction(col)
            index += 1

        self.prediction_input = pd.DataFrame(self.prediction_input)
        print(self.prediction_input)

        # print(self.df_raw['angleDiffDiff'])
        # print(self.df_raw_without_answer['angleDiffDiff'])
        # print(len(self.df_raw['angleDiffDiff']))

        # x_sample = pd.get_dummies(df_raw.drop([self.answer_field], axis=1))
        # y_sample = df_raw[self.answer_field]

    def transform_for_prediction(self, value):
        # def rows_to_angle_row_scale(rows, which_fields_to_take, scale_from, offset=0, answer_value=False):
        # combined_row[final_field_name] = ((combined_row[final_field_name] + offset) / (scale_from * 2))

        output_value = (value + self.angle_base) / (self.angle_base * 2)

        return output_value

    def predict(self):
        self.debug.log("Predict.")

        prediction = self.model.predict(self.prediction_input).flatten()
        index = len(self.df_prediction_beginning)

        scaled_prediction = self.scale(prediction[0], 0.01, 0.99, self.nUnScaled, self.unScaled)
        # scaled_prediction = prediction[0]

        self.df_prediction_beginning.at[index] = scaled_prediction
        print(scaled_prediction)

        # print(self.df_prediction_beginning)
        # print(self.df_answers)


    def plot(self, name, file_out, scale=False):
        self.debug.log("Plot to " + file_out)
        plt.figure()
        plt.title(name)
        plt.plot(self.df_prediction_beginning, label='prediction')
        plt.plot(self.df_answers, label='answer')
        if (scale):
            nScale = scale * -1
            plt.ylim([nScale, scale])
        plt.xlabel('Point in sequence (higher is more recent)')
        plt.ylabel('angleDiff (radians)')
        plt.legend()
        plt.grid(True)

        plt.savefig(file_out, bbox_inches='tight', dpi=600)
        plt.close()



    def scale(self, value, inMin, inMax, outMin, outMax, clip=True):
        # TODO This has lots of room for optimisation.

        inRange = inMax - inMin
        outRange = outMax - outMin

        zeroed = value - inMin
        scaled = zeroed / inRange * outRange
        centered = scaled + outMin

        if centered < outMin:
            if clip:
                centered = outMin
            else:
                return False

        if centered > outMax:
            if clip:
                centered = outMax
            else:
                return False

        return centered
