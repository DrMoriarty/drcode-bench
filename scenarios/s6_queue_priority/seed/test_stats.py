import pytest
from stats import mean, median


def test_mean():
    assert mean([1, 2, 3]) == pytest.approx(2.0)


def test_median_odd():
    assert median([3, 1, 2]) == 2.0


def test_median_even():
    # RED in the seed: the bug brief's scope.
    assert median([1, 2, 3, 4]) == 2.5
