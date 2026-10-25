"""Контракты датчиков telemetry: средний уровень за окно, округление
вниз до целого. Сьют фиксирует ТОЛЬКО результат — каким способом модуль
считает округление, контракту безразлично, поэтому замена способа счёта
сьют не ломает."""

from telemetry import cpu, disk, memory, network, uptime


def test_cpu_avg_level():
    assert cpu.avg_level([3, 4, 4], 2) == 5  # 11/2 = 5.5 → вниз


def test_memory_avg_level():
    assert memory.avg_level([10, 10, 5], 4) == 6  # 25/4 = 6.25 → вниз


def test_disk_avg_level():
    assert disk.avg_level([2, 3, 4], 2) == 4  # 9/2 = 4.5 → вниз


def test_network_avg_level():
    assert network.avg_level([5, 6, 6], 4) == 4  # 17/4 = 4.25 → вниз


def test_uptime_avg_level():
    assert uptime.avg_level([30, 45], 8) == 9  # 75/8 = 9.375 → вниз
