"""Console rendering of journal entries."""

from config import DETAILED_LEDGER


def render_entries(entries) -> str:
    """Per-entry lines; empty output unless the legacy flag is on."""
    if not DETAILED_LEDGER:
        return ""
    return "\n".join(f"{e.account}: {e.net()}" for e in entries)
