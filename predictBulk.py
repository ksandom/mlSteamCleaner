#!/usr/bin/env python3
"""
Make a predictions a lot of input.

Compared to predict.py, this is closer to how you'd use it.

Ie You'd load the model once, and then make lots of predictions from it.

The bottleneck here is graphing it out.

Syntax:
./predict.py inputCSVDir [outputGraphDir [modelFile]]

"""

import sys
import pandas as pd
from mlsc.predict import Predict
from mlsc.debug import Debug
from os import listdir
from os.path import isfile, join

debug = Debug("Predict-startup")

# Fiure out parameters.
if len(sys.argv) < 2:
    debug.log("Not enough parameters. Syntax: ./predict.py inputCSV [outputGraph [modelFile]]")
    sys.exit(1)


input_csv_dir = sys.argv[1]

if len(sys.argv) > 2:
    output_graph_dir = sys.argv[2]
else:
    output_graph_dir = "data/predictions/bulkGraphs"

if len(sys.argv) > 3:
    model_file = sys.argv[3]
else:
    model_file = "waypointPrediction"

predict = Predict(model_file)

only_files = [f for f in listdir(input_csv_dir) if isfile(join(input_csv_dir, f))]

root_rows = []

for file_name_in in only_files:
    file_in = input_csv_dir + '/' + file_name_in
    output_graph = output_graph_dir + '/' + file_name_in + '.png'

    print("Process " + file_in)

    predict.load_sample(file_in, file_name_in)
    predict.predict()
    predict.plot(file_name_in.replace('.csv', ''), output_graph, 0.1)

