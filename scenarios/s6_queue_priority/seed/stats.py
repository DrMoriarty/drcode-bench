"""Tiny statistics helpers (seed for the s6_queue_priority scenario)."""


def mean(nums: list[float]) -> float:
    """Arithmetic mean of nums."""
    return sum(nums) / len(nums)


def median(nums: list[float]) -> float:
    """Median of nums: the middle value, or the average of the two middle
    values for even-length lists."""
    # BUG (seed): the even-length branch drops the lower middle value —
    # test_median_even is red. This is the scope of the BUG brief; the
    # feature brief (stdev) must NOT touch it.
    ordered = sorted(nums)
    n = len(ordered)
    if n % 2:
        return float(ordered[n // 2])
    return float(ordered[n // 2])
