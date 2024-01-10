#!/usr/bin/env python3
"""
Train based on the dataset in data/

Loosely based on https://www.youtube.com/watch?v=6_2hzRopPbQ

Syntax:
./train_recognition.py modelFile trainData testData

"""

import sys
import pandas as pd
#from sklearn.model_selection import train_test_split
from mlsc.train_recognition import TrainRecognition
from mlsc.debug import Debug

# Fiure out parameters.
if len(sys.argv) > 1:
    model_file = sys.argv[1]
else:
    model_file = "badWaypointDetection"

if len(sys.argv) > 2:
    train_data = sys.argv[2]
else:
    train_data = "data/samples/10/combinedBinaryA.csv"

if len(sys.argv) > 3:
    test_data = sys.argv[3]
else:
    test_data = "data/samples/10/combinedBinaryB.csv"

debug = Debug(model_file + "-startup")

# Get data.
debug.log("Load data.")
df_train = pd.read_csv(train_data)
x_train = pd.get_dummies(df_train.drop(['good'], axis=1))
y_train = df_train['good']

df_test = pd.read_csv(test_data)
x_test = pd.get_dummies(df_test.drop(['good'], axis=1))
y_test = df_test['good']

print (x_train.head())
print (y_train.head())

train_recognition = TrainRecognition(model_file, x_train, x_test, y_train, y_test)
train_recognition.train()
