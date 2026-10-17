# MSCS 532 Assignment 5

This repository implements deterministic and randomized Quicksort in Python and
compares their behavior on random, sorted, and reverse-sorted inputs.

## Requirements

- Python 3.10 or later
- No third-party packages

## Run the implementations

```text
python3 quicksort.py 10 7 8 9 1 5
```

The script sorts the same values with both implementations and prints the results.

## Run the tests

```text
python3 -m unittest -v
```

The tests cover empty and single-element inputs, duplicates, negative values,
sorted and reverse-sorted inputs, and 101 generated input sizes.

## Run the benchmark

```text
python3 benchmark.py
```

The default benchmark uses input sizes 100, 250, 500, and 750. It reports median
times from nine trials for each algorithm and distribution. To save the same
output as CSV:

```text
python3 benchmark.py --csv benchmark_results.csv
```

## Findings

The deterministic implementation uses the last element as the pivot. It is
competitive on random inputs, but sorted and reverse-sorted inputs repeatedly
create highly unbalanced partitions and expose quadratic growth. Random pivot
selection adds a small amount of overhead on random inputs, but it avoids tying
the partition pattern to the input order. The randomized version therefore
remains much faster on the ordered inputs in this experiment.

See `report.pdf` for the implementation details, theoretical analysis,
measurements, and limitations.
