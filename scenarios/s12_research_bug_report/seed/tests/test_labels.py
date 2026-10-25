from dispatch.labels import is_tracking_code, tracking_code


def test_tracking_code_format():
    assert tracking_code(42) == "DSP00000042"
    assert tracking_code(0) == "DSP00000000"


def test_is_tracking_code():
    assert is_tracking_code("DSP00000042")
    assert not is_tracking_code("DSP42")
    assert not is_tracking_code("DSP0000004A")
    assert not is_tracking_code("XYZ00000042")
