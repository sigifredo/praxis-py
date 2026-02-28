from . import log

import shlex
import subprocess


def run_shell_command(
    command_str: str,
    show_errors: bool = True,
    use_shell: bool = False,
    cwd: str = None,
) -> bool:
    '''
    Ejecuta un comando del sistema de forma segura.

    Args:
        command_str: La cadena de texto con el comando a ejecutar.
        show_errors: Si es True, registra los errores en el log en caso de fallo.
        use_shell: Si es True, ejecuta el comando a través del shell.
        cwd: Directorio de trabajo. Si es None, usa el actual.

    Returns:
        True si el comando tuvo éxito (exit code 0), False de lo contrario.
    '''

    log.info(f'Running command: {command_str}')

    args = command_str if use_shell else shlex.split(command_str)
    error_msg: str = ''

    try:
        result = subprocess.run(
            args,
            shell=use_shell,
            capture_output=True,
            text=True,
            cwd=cwd,
        )

        if result.returncode == 0:
            return True

        stderr = (result.stderr or '').strip()
        stdout = (result.stdout or '').strip()
        error_msg = (
            f'Command failed: {command_str}\n'
            f'Exit Code: {result.returncode}\n'
            f'Stderr: {stderr[:1000]}\n'  # Limitamos a 1000 caracteres por seguridad
            f'Stdout: {stdout[:1000]}'
        )

    except FileNotFoundError:
        error_msg = f'Executable not found: {command_str}'

    except Exception as e:
        error_msg = f'Unexpected error: {e}'

    if show_errors:
        log.error(error_msg)

    return False
