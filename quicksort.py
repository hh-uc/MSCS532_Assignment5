"""Deterministic and randomized in-place Quicksort implementations."""

from __future__ import annotations

import argparse
import random
from collections.abc import MutableSequence
from typing import TypeVar


T = TypeVar("T")


def _partition(values: MutableSequence[T], low: int, high: int) -> int:
    """Partition values[low:high + 1] around its last element."""
    pivot = values[high]
    low_side_end = low - 1

    # Move each value that belongs on the low side into the next open slot.
    for scan in range(low, high):
        if values[scan] <= pivot:
            low_side_end += 1
            values[low_side_end], values[scan] = (
                values[scan],
                values[low_side_end],
            )

    # Place the pivot between the low and high sides of the partition.
    pivot_index = low_side_end + 1
    values[pivot_index], values[high] = values[high], values[pivot_index]
    return pivot_index


def quicksort(
    values: MutableSequence[T], low: int = 0, high: int | None = None
) -> MutableSequence[T]:
    """Sort values in place with last-element pivots and return values."""
    if high is None:
        high = len(values) - 1

    if low < high:
        pivot_index = _partition(values, low, high)

        # The pivot is in its final location, so sort only the two sides.
        quicksort(values, low, pivot_index - 1)
        quicksort(values, pivot_index + 1, high)

    return values


def _randomized_partition(
    values: MutableSequence[T],
    low: int,
    high: int,
    rng: random.Random,
) -> int:
    """Choose a uniform random pivot, then use the shared partition logic."""
    random_index = rng.randint(low, high)
    values[random_index], values[high] = values[high], values[random_index]
    return _partition(values, low, high)


def randomized_quicksort(
    values: MutableSequence[T],
    low: int = 0,
    high: int | None = None,
    rng: random.Random | None = None,
) -> MutableSequence[T]:
    """Sort values in place with uniformly random pivots and return values."""
    if high is None:
        high = len(values) - 1
    if rng is None:
        rng = random.Random()

    if low < high:
        pivot_index = _randomized_partition(values, low, high, rng)

        # Reuse one generator for the full recursion so seeded runs repeat.
        randomized_quicksort(values, low, pivot_index - 1, rng)
        randomized_quicksort(values, pivot_index + 1, high, rng)

    return values


def main() -> None:
    """Run a small command-line demonstration of both algorithms."""
    parser = argparse.ArgumentParser(
        description="Sort integers with deterministic and randomized Quicksort."
    )
    parser.add_argument(
        "values",
        nargs="*",
        type=int,
        default=[10, 7, 8, 9, 1, 5],
        help="integers to sort",
    )
    args = parser.parse_args()

    deterministic = list(args.values)
    randomized = list(args.values)

    quicksort(deterministic)
    randomized_quicksort(randomized, rng=random.Random(532))

    print(f"Input:         {args.values}")
    print(f"Deterministic: {deterministic}")
    print(f"Randomized:    {randomized}")


if __name__ == "__main__":
    main()
