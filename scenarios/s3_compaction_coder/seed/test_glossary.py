"""Контракт сценария S3 (план drcode-bench.md §7): вес термина kappa
изменён на 42, все остальные модули каталога не тронуты. Изначально
падает ровно первый тест — его и делает зелёным агент."""

from glossary import alpha, iota, kappa, sigma, tau, zeta


def test_kappa_weight_changed():
    assert kappa.TERM == "kappa"
    assert kappa.WEIGHT == 42


def test_other_modules_untouched():
    assert alpha.WEIGHT == 3
    assert iota.WEIGHT == 11
    assert sigma.WEIGHT == 19
    assert tau.WEIGHT == 20
    assert zeta.WEIGHT == 4
