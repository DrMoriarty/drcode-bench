import pytest

from dispatch.pricing import batches_needed, volume_tier


def test_batches_whole_batches():
    assert batches_needed(10, 10) == 1
    assert batches_needed(30, 10) == 3


def test_batches_single_unit_per_batch():
    assert batches_needed(7, 1) == 7


def test_batches_invalid_arguments():
    with pytest.raises(ValueError):
        batches_needed(0, 10)
    with pytest.raises(ValueError):
        batches_needed(5, 0)


def test_volume_tier_boundaries():
    assert volume_tier(1) == "S"
    assert volume_tier(5) == "S"
    assert volume_tier(6) == "M"
    assert volume_tier(20) == "M"
    assert volume_tier(21) == "L"
