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

