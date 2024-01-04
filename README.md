# mlSteamCleaner
Clean a stream of data using machine learning

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
