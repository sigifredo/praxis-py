from . import log

import typing


def run_main(main_func: typing.Callable[[], int]) -> None:
    '''Ejecuta la función principal y maneja las salidas del sistema limpiamente.

    Args:
        main_func (Callable[[], int]): La función principal del script.
            No debe recibir argumentos y debe retornar un número entero.
    '''
    try:
        raise SystemExit(main_func())
    except KeyboardInterrupt:
        log.error('Script detenido por el usuario')
        raise SystemExit(130)
