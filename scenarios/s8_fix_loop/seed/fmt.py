"""Tiny text-formatting helpers (seed for the s8_fix_loop scenario)."""


def pad(text: str, width: int) -> str:
    """Pad text with trailing spaces up to `width` characters.

    Strings longer than `width` are returned unchanged today — the S8
    brief adds truncation, which is invisible to test_pad (it pins only
    the short-string case) but breaks test_row through its dependency on
    pad().
    """
    return text.ljust(width)


def row(name: str, value: str, width: int = 12) -> str:
    """One table row: the name padded to `width`, then ': ' and the value.

    Consumes pad(): whatever pad() returns becomes the name column — a
    change to pad() therefore changes every row() output. The S8 brief
    asks the coder to change pad() ONLY, so this test goes red BY DESIGN
    after the coder's round-1 edit (the full suite is green in the
    untouched seed — that is what distinguishes S8 from s2a, where the
    neighbour test is red from the start).
    """
    return f"{pad(name, width)}: {value}"
