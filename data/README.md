# Data

Eventually, you'll end up with data like this:

```bash
ksandom@delli:~/files/develop/mlSteamCleaner/data$ du -sh *
123M    graphImages
6.8M    graphPDFs
32M     prepped
3.9M    raw
498M    samples
```

| Name | What is it? |
| --- | --- |
| raw | The starting data. |
| prepped | Processed data. There has been an attempt to mark, and separately correct, data errors. |
| graphImages | Visualisations of the prepped data as PNG images. |
| graphPDFs | Visualisations of the prepped data as PDF files. |
| samples | The data that will be used to train the model. |

See the root README.md for instructions for how to get this.
