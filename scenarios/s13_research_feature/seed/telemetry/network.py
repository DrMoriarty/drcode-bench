"""Датчик сети: средний трафик в пакетах за окно наблюдения."""

import math


def avg_level(readings: list[int], window_s: int) -> int:
    """Средний трафик за окно `window_s`: сумма чтений, делённая на
    длину окна, с округлением вниз до целого."""
    return math.floor(sum(readings) / window_s)
