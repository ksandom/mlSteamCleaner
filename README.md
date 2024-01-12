# mlSteamCleaner
Clean a stream of location data using machine learning

## Installation

```bash
pip install -r requirements.txt
```

## Training the model yourself

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

**Expected time:** ~15 minutes on 2018 hardware.

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
    * Anything else will be ignored.

You can use `./util/extraAll` to create these files. Note that it is set up for my data source, where these fields are originally called `default_longitude-deg` and `default_latitude-deg`. So you'll likely need to adapt it to your needs.
