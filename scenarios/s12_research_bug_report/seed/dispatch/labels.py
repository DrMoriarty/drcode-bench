"""Метки отправлений: формат трек-номера и его проверка."""

TRACK_PREFIX = "DSP"
SERIAL_DIGITS = 8


def tracking_code(serial: int) -> str:
    """Трек-номер: префикс DSP и серийный номер, дополненный нулями
    слева до 8 цифр."""
    return f"{TRACK_PREFIX}{serial:0{SERIAL_DIGITS}d}"


def is_tracking_code(code: str) -> bool:
    """True, когда строка — корректный трек-номер: префикс DSP и ровно
    8 цифр сразу после него."""
    body = code.removeprefix(TRACK_PREFIX)
    return (
        code.startswith(TRACK_PREFIX)
        and len(body) == SERIAL_DIGITS
        and body.isdigit()
    )
