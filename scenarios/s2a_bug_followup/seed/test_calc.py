import pytest

from calc import div, pct


def test_div():
    assert div(6, 3) == 2.0
    with pytest.raises(ValueError):
        div(1, 0)


def test_pct():
    assert pct(50, 200) == 25.0
    assert pct(1, 4) == 25.0
