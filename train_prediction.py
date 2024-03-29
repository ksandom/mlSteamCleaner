#!/usr/bin/env python3
"""
Train based on the dataset in data/

Loosely based on https://www.youtube.com/watch?v=-vHQub0NXI4 and
https://www.tensorflow.org/tutorials/keras/regression

Syntax:
./train_prediction.py modelFile trainData testData

"""

import sys
import pandas as pd
from mlsc.train_prediction import TrainPrediction
from mlsc.debug import Debug


# Fiure out parameters.
if len(sys.argv) > 1:
    model_file = sys.argv[1]
else:
    model_file = "waypointPrediction"

if len(sys.argv) > 2:
    train_data = sys.argv[2]
else:
    train_data = "data/samples/10/combinedAngleA.csv"

if len(sys.argv) > 3:
    test_data = sys.argv[3]
else:
    test_data = "data/samples/10/combinedAngleB.csv"

debug = Debug(model_file + "-startup")


# Get data.
debug.log("Load data.")

# TODO This field would need to be updated with a different sample_size.
answer_field = 'answer_value'

df_train = pd.read_csv(train_data)
x_train = pd.get_dummies(df_train.drop([answer_field], axis=1))
y_train = df_train[answer_field]

df_test = pd.read_csv(test_data)
x_test = pd.get_dummies(df_test.drop([answer_field], axis=1))
y_test = df_test[answer_field]

print(x_train.head())
print(y_train.head())

train_prediction = TrainPrediction(model_file, x_train, x_test, y_train, y_test, df_test)
train_prediction.train()

print("Test size: " + str(len(y_test)))
