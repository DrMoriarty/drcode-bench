"""Text summaries of ledger state."""


def balance(entries, currency: str = "RUB") -> str:
    """Render the net total as a currency string, e.g. '1 250,00 RUB'."""
    total = sum(e.debit - e.credit for e in entries)
    body = f"{abs(total):,}".replace(",", " ")
    sign = "-" if total < 0 else ""
    return f"{sign}{body},00 {currency}"
