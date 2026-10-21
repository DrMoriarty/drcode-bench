"""Tiny calculator helpers (seed for the s2b_bug_report scenario)."""


def div(a: float, b: float) -> float:
    """Divide a by b; raise ValueError on a zero divisor."""
    # BUG (seed): ZeroDivisionError instead of ValueError — the in-scope
    # bug of the FIRST brief.
    return a / b


def pct(a: float, b: float) -> float:
    """Return a as a percentage of b (a / b * 100)."""
    # BUG (seed): the * 100 is missing — test_pct fails. Deliberately OUT
    # of the first brief's scope: the tester must notice the out-of-scope
    # failure and file it via create_bug_report.
    return a / b
