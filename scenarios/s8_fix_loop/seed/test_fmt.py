"""Seed contract of s8_fix_loop: the FULL suite is green before any change.

test_pad pins the short-string behaviour of pad() — the brief's change
(truncation of long strings) keeps it green. test_row pins a row() with a
name LONGER than the column, which consumes pad() — the coder's round-1
edit of pad() breaks it by design, and the tester's retry_here fix loop
must bring the suite back to green without user help.
"""

from fmt import pad, row


def test_pad():
    assert pad("ab", 5) == "ab   "


def test_row():
    assert row("configuration", 42) == "configuration: 42"
