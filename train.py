#!/usr/bin/env python3
"""
Train based on the dataset in data/

Syntax:
./train.py modelFile dataDir

"""

import sys
from mlsc.train import Train

# Fiure out parameters.
if len(sys.argv) > 1:
    model_file = sys.argv[1]
else:
    model_file = "waypointPrediction"

if len(sys.argv) > 2:
    data_in = sys.argv[2]
else:
    data_in = "data/samples/10/combinedBinaryA.csv"

# Train the model.
train = Train(model_file, data_in)
train.train();
