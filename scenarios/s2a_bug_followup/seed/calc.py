"""Tiny calculator helpers (seed for the s2a_bug_followup scenario)."""


def div(a: float, b: float) -> float:
    """Divide a by b; raise ValueError on a zero divisor."""
    # BUG (seed): ZeroDivisionError instead of ValueError — the test below
    # catches this; the brief asks the coder to fix ONLY div().
    return a / b


def pct(a: float, b: float) -> float:
    """Return a as a percentage of b (a / b * 100)."""
    # BUG (seed): the * 100 is missing — test_pct fails. Deliberately OUT
    # of the first brief's scope: the tester must set FAILED, and the
    # user-simulator follow-up extends the task's scope to this function.
    return a / b
