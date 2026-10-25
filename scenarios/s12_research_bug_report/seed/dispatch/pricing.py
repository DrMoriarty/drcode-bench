"""Тарифы и упаковка: расчёт партий отгрузки и тарифных ярусов.

Контракты функций зафиксированы в докстрингах; покрытие —
tests/test_pricing.py. Все количества целые.
"""


def batches_needed(items: int, per_batch: int) -> int:
    """Число партий для отгрузки `items` единиц по `per_batch` в партии.

    Последняя неполная партия тоже учитывается: например, для 35 единиц
    по 10 в партии нужно 4 партии — три полные и одна на 5 единиц, то есть
    batches_needed(35, 10) == 4.
    """
    if items <= 0 or per_batch <= 0:
        raise ValueError("items и per_batch должны быть положительными")
    return items // per_batch


def volume_tier(volume_l: int) -> str:
    """Тарифный ярус по объёму отправления в литрах: 'S' — до 5 л
    включительно, 'M' — свыше 5 до 20 л включительно, 'L' — свыше 20 л."""
    if volume_l <= 5:
        return "S"
    if volume_l <= 20:
        return "M"
    return "L"
