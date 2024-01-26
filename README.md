# mlSteamCleaner
Clean a stream of location data using machine learning

![Predict the correct point.](https://github.com/ksandom/mlSteamCleaner/blob/24fe69ce224d1677ea56c83ce621a9cf8b5a46c3/data/img/2023-06-20-104227-accurateWaypoints.csv-1019-1029-C.csv.png)

* **Orange** is the **raw data** that came from the flight simulator.
* **Blue** is the **prediction** of what the value should be.

This project is very much a prototype to play with concepts. It is not production-ready code.

Processing GPS data is a mature problem, and there are likely many libraries already available to help you.

## Installation

```bash
pip install -r requirements.txt
```

## Training the models yourself

### Prep the data for use

Run prepAll to create samples from the raw data.

```bash
./util/prepAll
```

This will take a few minutes, and create a fair bit of data.

```bash
ksandom@delli:~/files/develop/mlSteamCleaner/data$ du -sh *
123M    graphImages
6.8M    graphPDFs
32M     prepped
3.9M    raw
498M    samples
```

In particular, you may be interested in the visualisations in `graphImages` and `graphPDFs`.

**Expected time:** ~3.5 minutes on 2018 hardware.

### Train the recognition model

```bash
./train_reconition.py
```

_SNIP_

```
Epoch 193/200
491/491 [==============================] - 0s 1ms/step - loss: 7.3645e-04 - accuracy: 1.0000
Epoch 194/200
491/491 [==============================] - 0s 991us/step - loss: 7.1789e-04 - accuracy: 1.0000
Epoch 195/200
491/491 [==============================] - 0s 978us/step - loss: 7.1819e-04 - accuracy: 1.0000
Epoch 196/200
491/491 [==============================] - 0s 1ms/step - loss: 7.0502e-04 - accuracy: 1.0000
Epoch 197/200
491/491 [==============================] - 0s 1ms/step - loss: 6.9199e-04 - accuracy: 1.0000
Epoch 198/200
491/491 [==============================] - 0s 983us/step - loss: 6.9663e-04 - accuracy: 1.0000
Epoch 199/200
491/491 [==============================] - 0s 1ms/step - loss: 6.8089e-04 - accuracy: 1.0000
Epoch 200/200
491/491 [==============================] - 0s 997us/step - loss: 6.8595e-04 - accuracy: 1.0000

badWaypointDetection-train: Predict.
126/126 [==============================] - 0s 756us/step
accuracy_score: 0.9922519370157461
```

**Expected time:** ~2 minutes on 2018 hardware.

### Train the prediction model

```bash
./train_prediction.py
```

**Expected time:** ~4.5 minutes on 2018 hardware.

### Using your own data

If you'd like to try the models on your own data, you can place it in data/raw before doing the [Prep the data for use](#prep-the-data-for-use) steps.

Overview:

1. Place data that you want to import into the data/raw directory.
1. Do the [Prep the data for use](#prep-the-data-for-use) steps.

The data that you place in the data/raw directory must be:

* CSV files (as many as you want).
* Contain the following fields:
    * `long`
    * `lat`
    * `default_airspeed-kt` (Optional) - Datapoints below 10 knots will be excluded.
    * Anything else will be ignored.

You can use `./util/extraAll` to create these files. Note that it is set up for my data source, where these fields are originally called `default_longitude-deg` and `default_latitude-deg`. So you'll likely need to adapt it to your needs.
