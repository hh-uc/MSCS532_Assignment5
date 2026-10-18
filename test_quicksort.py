"""Correctness tests for deterministic and randomized Quicksort."""

from __future__ import annotations

import random
import unittest

from quicksort import quicksort, randomized_quicksort


class QuicksortTests(unittest.TestCase):
    """Run the same cases against both implementations."""

    def assert_both_sort(self, values: list[int]) -> None:
        expected = sorted(values)

        deterministic = list(values)
        returned_deterministic = quicksort(deterministic)
        self.assertIs(returned_deterministic, deterministic)
        self.assertEqual(deterministic, expected)

        randomized = list(values)
        returned_randomized = randomized_quicksort(
            randomized, rng=random.Random(532)
        )
        self.assertIs(returned_randomized, randomized)
        self.assertEqual(randomized, expected)

    def test_empty_input(self) -> None:
        self.assert_both_sort([])

    def test_single_value(self) -> None:
        self.assert_both_sort([7])

    def test_duplicates_and_negatives(self) -> None:
        self.assert_both_sort([4, -2, 4, 0, -2, 9, 1])

    def test_sorted_input(self) -> None:
        self.assert_both_sort(list(range(100)))

    def test_reverse_sorted_input(self) -> None:
        self.assert_both_sort(list(range(99, -1, -1)))

    def test_large_ordered_inputs(self) -> None:
        self.assert_both_sort(list(range(1200)))
        self.assert_both_sort(list(range(1199, -1, -1)))

    def test_large_equal_input(self) -> None:
        self.assert_both_sort([7] * 1200)

    def test_many_random_inputs(self) -> None:
        generator = random.Random(532)
        for size in range(101):
            with self.subTest(size=size):
                values = [generator.randint(-500, 500) for _ in range(size)]
                self.assert_both_sort(values)


if __name__ == "__main__":
    unittest.main()
