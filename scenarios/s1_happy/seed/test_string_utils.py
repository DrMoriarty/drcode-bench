from string_utils import shout


def test_shout():
    assert shout("hi") == "HI!"
    assert shout("ok") == "OK!"
