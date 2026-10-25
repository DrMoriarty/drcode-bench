"""Numeric aggregations over journal entries."""


def balance(entries) -> int:
    """Net total of a sequence of entries, in minor units."""
    return sum(e.net() for e in entries)
