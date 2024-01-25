#!/usr/bin/env python3
"""
Make a prediction on a single file.

The whole point of this is to make a prediction independently of the knowledge we had while training the model.

Syntax:
./predict.py inputCSV [outputGraph [modelFile]]

"""

import sys
import pandas as pd
from mlsc.predict import Predict
from mlsc.debug import Debug

debug = Debug("Predict-startup")

# Fiure out parameters.
if len(sys.argv) < 2:
    debug.log("Not enough parameters. Syntax: ./predict.py inputCSV [outputGraph [modelFile]]")
    sys.exit(1)


input_csv = sys.argv[1]

if len(sys.argv) > 2:
    output_graph = sys.argv[2]
else:
    output_graph = "data/predictions/graphs/prediction.png"

if len(sys.argv) > 3:
    model_file = sys.argv[3]
else:
    model_file = "waypointPrediction"

predict = Predict(model_file)
predict.load_sample(input_csv)
predict.predict()
predict.plot("Prediction for " + input_csv, output_graph, 0.1)

