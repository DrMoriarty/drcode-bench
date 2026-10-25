"""Journal entry records."""


class JournalEntry:
    """One double-entry record: debit and credit in minor units."""

    __slots__ = ("account", "debit", "credit")

    def __init__(self, account: str, debit: int, credit: int) -> None:
        self.account = account
        self.debit = debit
        self.credit = credit

    def net(self) -> int:
        """Signed effect of the entry on its account."""
        return self.debit - self.credit
