def hms_to_seconds(ts: str) -> float:
    '''Convierte una marca de tiempo a segundos.

    Args:
        ts: Cadena en formato HH:MM:SS(.ms), MM:SS(.ms), SS(.ms), o el
            sentinel '-1' (solo válido como marca de fin, indica
            'hasta el final').

    Returns:
        Duración en segundos como float, o -1.0 si ts es el sentinel.

    Raises:
        ValueError: Si el formato de ts no es válido.
    '''

    ts = ts.strip()

    if ts == '-1':
        return -1.0

    parts = ts.split(':')

    if len(parts) == 1:
        return float(parts[0])
    if len(parts) == 2:
        m, s = parts
        return int(m) * 60.0 + float(s)
    elif len(parts) == 3:
        h, m, s = parts
        return int(h) * 3600.0 + int(m) * 60.0 + float(s)
    else:
        raise ValueError(f'Formato de tiempo inválido: "{ts}"')


def seconds_to_hms(seconds: float) -> str:
    '''Convierte segundos a formato HH:MM:SS.

    Args:
        seconds: Duración en segundos. Puede tener decimales, que se
            redondean al segundo entero más cercano.

    Returns:
        Cadena con la duración en formato HH:MM:SS.

    Raises:
        ValueError: Si seconds es negativo.
    '''

    if seconds < 0:
        raise ValueError('La duración no puede ser negativa.')

    total = int(round(seconds))
    h = total // 3600
    m = (total % 3600) // 60
    s = total % 60

    return f'{h:02}:{m:02}:{s:02}'
