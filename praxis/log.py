import sys
import typing

PREFIX_WIDTH = 9  # longitud de '[WARNING]'


def _log(
    label: str,
    color: str | None,
    s: str,
    emit=True,
    file: typing.TextIO = sys.stdout,
) -> None | str:
    '''
    Construye y opcionalmente emite un mensaje de log con prefijo y color ANSI.

    Args:
        label (str): Etiqueta del mensaje (se muestra entre corchetes).
        color (str | None): Código ANSI de color sin el prefijo '\\033['.
            Si es None, no se aplica color.
        s (str): Contenido del mensaje.
        emit (bool): Si True, imprime el mensaje. Si False, lo retorna.
        file (TextIO): Objeto con método .write() donde se emite el mensaje.
            Por defecto sys.stdout.

    Returns:
        None | str: None si emit es True; el mensaje formateado si emit es False.
    '''

    padded = f'[{label}]'.ljust(PREFIX_WIDTH)
    msg = f'\033[{color}m{padded}\033[0m {s}' if color else f'{padded} {s}'

    if emit:
        print(msg, file=file)
        return None

    return msg


def debug(s: str, emit=True, file: typing.TextIO = sys.stdout) -> None | str:
    return _log('DEBUG', '34', s, emit, file)


def info(s: str, emit=True, file: typing.TextIO = sys.stdout) -> None | str:
    return _log('INFO', '32', s, emit, file)


def warning(s: str, emit=True, file: typing.TextIO = sys.stderr) -> None | str:
    return _log('WARNING', '33', s, emit, file)


def error(s: str, emit=True, file: typing.TextIO = sys.stderr) -> None | str:
    return _log('ERROR', '31', s, emit, file)
