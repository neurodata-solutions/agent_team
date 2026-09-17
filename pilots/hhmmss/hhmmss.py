"""Conversão de segundos para o formato HH:MM:SS.

As horas não sofrem módulo 24: 86400 segundos viram "24:00:00" e
360000 segundos viram "100:00:00".
"""

SECONDS_PER_MINUTE = 60
SECONDS_PER_HOUR = 60 * SECONDS_PER_MINUTE


def seconds_to_hhmmss(seconds) -> str:
    """Formata um número inteiro não negativo de segundos como HH:MM:SS.

    Args:
        seconds: inteiro não negativo de segundos.

    Returns:
        A string no formato "HH:MM:SS", com no mínimo dois dígitos nas
        horas e sem limite superior (horas podem passar de 23 e de dois
        dígitos).

    Raises:
        TypeError: se ``seconds`` não for ``int``. ``bool`` é subclasse de
            ``int`` em Python e é rejeitado explicitamente.
        ValueError: se ``seconds`` for um ``int`` negativo.
    """
    if isinstance(seconds, bool) or not isinstance(seconds, int):
        raise TypeError(
            "seconds deve ser int não negativo, "
            f"recebido {type(seconds).__name__}"
        )
    if seconds < 0:
        raise ValueError(f"seconds deve ser não negativo, recebido {seconds}")

    hours, remainder = divmod(seconds, SECONDS_PER_HOUR)
    minutes, secs = divmod(remainder, SECONDS_PER_MINUTE)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"
