from calc import export_api


def test_export_api():
    assert export_api() == ["div", "pct"]
