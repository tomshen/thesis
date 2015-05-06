# JuntoProPPR

## Setup
```sh
> git submodule init
> git submodule update
```

In `./lib/ProPPR`:

```sh
> ant clean build
```

In `./lib/junto`:

```sh
> export PATH="$PATH:$JUNTO_DIR/bin"
> bin/build update compile
```

## Conversion

```
usage: convert.py [-h] [-p SAMPLE_PERCENT] [-d GRAPH_DIR] junto_config

Convert Junto graphs to ProPPR SRW graphs.

positional arguments:
  junto_config       Junto config file

optional arguments:
  -h, --help         show this help message and exit
  -p SAMPLE_PERCENT  Percent of Junto graph edges to use in the SRW graph
  -d GRAPH_DIR       Directory to write SRW graphs to
```

## Running

```
usage: runner.py [-h] [--mem MEM_SIZE] [-o OUTPUT_FILE] [--threads THREADS]
                 {junto,srw} junto_config

Runs Junto or SRW

positional arguments:
  {junto,srw}
  junto_config       Junto config file

optional arguments:
  -h, --help         show this help message and exit
  --mem MEM_SIZE     Java memory size
  -o OUTPUT_FILE
  --threads THREADS  Number of threads for SRW
```

## Analysis

```
usage: analyze.py [-h] [--config [JUNTO_CONFIG]] [--test [JUNTO_TEST_FILE]]
                  results_file

Analyze a results file from Junto or ProPPR SRW.

positional arguments:
  results_file          Results file

optional arguments:
  -h, --help            show this help message and exit
  --config [JUNTO_CONFIG]
                        Junto config file
  --test [JUNTO_TEST_FILE]
                        Junto test_file
```

## Todo
* Figure out why output from Propagator keeps getting cut off
