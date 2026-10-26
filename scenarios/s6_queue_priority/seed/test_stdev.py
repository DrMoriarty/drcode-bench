import pytest
from stats import stdev


def test_stdev_population():
    # Classic dataset: population standard deviation is exactly 2.
    assert stdev([2, 4, 4, 4, 5, 5, 7, 9]) == pytest.approx(2.0)


def test_stdev_single_value():
    assert stdev([5.0]) == 0.0
