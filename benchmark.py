"""Reproducible timing comparison for both Quicksort implementations."""

from __future__ import annotations

import argparse
import csv
import random
import statistics
import time
from pathlib import Path
from typing import Callable

from quicksort import quicksort, randomized_quicksort


SortFunction = Callable[[list[int]], object]
DISTRIBUTIONS = ("random", "sorted", "reverse-sorted")


def make_input(distribution: str, size: int, rng: random.Random) -> list[int]:
    """Build a distinct-integer input with the requested ordering."""
    values = list(range(size))
    if distribution == "random":
        rng.shuffle(values)
    elif distribution == "reverse-sorted":
        values.reverse()
    elif distribution != "sorted":
        raise ValueError(f"unsupported distribution: {distribution}")
    return values


def time_sort(sort_function: SortFunction, values: list[int]) -> float:
    """Time one sorting call and verify its result."""
    working = list(values)
    expected = sorted(values)

    started = time.perf_counter_ns()
    sort_function(working)
    elapsed_ms = (time.perf_counter_ns() - started) / 1_000_000

    if working != expected:
        raise AssertionError("sorting result does not match Python's sorted output")
    return elapsed_ms


def run_benchmark(
    sizes: list[int], trials: int, seed: int
) -> list[dict[str, str | int | float]]:
    """Return median timings for every algorithm, size, and distribution."""
    rows: list[dict[str, str | int | float]] = []
    input_rng = random.Random(seed)

    for distribution in DISTRIBUTIONS:
        for size in sizes:
            deterministic_times: list[float] = []
            randomized_times: list[float] = []

            for trial in range(trials):
                values = make_input(distribution, size, input_rng)

                deterministic_times.append(time_sort(quicksort, values))

                pivot_rng = random.Random(seed + size * 100 + trial)
                randomized_times.append(
                    time_sort(
                        lambda working, generator=pivot_rng: randomized_quicksort(
                            working, rng=generator
                        ),
                        values,
                    )
                )

            rows.append(
                {
                    "distribution": distribution,
                    "size": size,
                    "trials": trials,
                    "deterministic_median_ms": statistics.median(
                        deterministic_times
                    ),
                    "randomized_median_ms": statistics.median(randomized_times),
                }
            )

    return rows


def write_csv(rows: list[dict[str, str | int | float]], path: Path) -> None:
    """Write benchmark rows to a CSV file."""
    fieldnames = [
        "distribution",
        "size",
        "trials",
        "deterministic_median_ms",
        "randomized_median_ms",
    ]
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def print_rows(rows: list[dict[str, str | int | float]]) -> None:
    """Print a compact table for terminal review."""
    print("distribution,size,trials,deterministic_median_ms,randomized_median_ms")
    for row in rows:
        print(
            f"{row['distribution']},{row['size']},{row['trials']},"
            f"{float(row['deterministic_median_ms']):.6f},"
            f"{float(row['randomized_median_ms']):.6f}"
        )


def main() -> None:
    """Parse arguments, run the benchmark, and display or save results."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sizes", nargs="+", type=int, default=[100, 250, 500, 750])
    parser.add_argument("--trials", type=int, default=9)
    parser.add_argument("--seed", type=int, default=532)
    parser.add_argument("--csv", type=Path, help="optional CSV output path")
    args = parser.parse_args()

    if any(size < 0 for size in args.sizes):
        parser.error("sizes must be nonnegative")
    if args.trials < 1:
        parser.error("trials must be at least 1")

    rows = run_benchmark(args.sizes, args.trials, args.seed)
    print_rows(rows)
    if args.csv:
        write_csv(rows, args.csv)


if __name__ == "__main__":
    main()
