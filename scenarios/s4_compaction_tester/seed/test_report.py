"""Контракт сценария S4: изначально падает — разделитель отчёта неверен."""

from report import format_report


def test_format_report_separates_items():
    out = format_report(["a", "b", "c"])
    assert out == "a\n\nb\n\nc"


def test_format_report_single_item():
    assert format_report(["only"]) == "only"
