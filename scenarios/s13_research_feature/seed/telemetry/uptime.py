"""Датчик доступности: среднее число живых реплик за окно."""

import math


def avg_level(readings: list[int], window_s: int) -> int:
    """Среднее число живых реплик за окно `window_s`: сумма чтений,
    делённая на длину окна, с округлением вниз до целого."""
    return math.floor(sum(readings) / window_s)
