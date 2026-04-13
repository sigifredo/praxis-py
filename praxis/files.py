import pathlib
import typing


def get_exclude_names(directory: str | pathlib.Path, file_name: str = '.signore') -> list[str]:
    '''
    Read an ignore file and return the names to be excluded.

    Args:
        directory: Directory where the ignore file is searched.
        file_name: Name of the ignore file. Defaults to `.signore`.

    Returns:
        A list of file or directory names (or patterns) to ignore.
    '''

    directory = pathlib.Path(directory)
    exclude_names: list[str] = []
    ignore_path = directory / file_name

    if ignore_path.is_file():
        with open(ignore_path, 'r', encoding='utf-8') as f_ignore:
            for raw_line in f_ignore:
                line = raw_line.strip()

                if not line or line.startswith('#'):
                    continue

                exclude_names.append(line)

    return exclude_names


def get_files(
    root: str | pathlib.Path,
    include_hidden: bool = False,
    include_extensions: typing.Iterable[str] | None = None,
    exclude_extensions: typing.Iterable[str] | None = None,
    exclude_pattern: typing.Iterable[str] | None = None,
    recursive: bool = False,
) -> tuple[list[pathlib.Path], list[pathlib.Path]]:
    '''
    Recorre un directorio y devuelve subdirectorios y archivos filtrados.

    Args:
        root: Ruta base a explorar.
        include_hidden: Si es True, incluye archivos y directorios ocultos (prefijo '.').
        include_extensions: Extensiones a incluir (p. ej. {"mp4", "mkv"}). Si es None o vacío,
            se incluyen todas las extensiones (salvo las excluidas).
        exclude_extensions: Extensiones a excluir (p. ej. {"png", "jpg"}).
        exclude_pattern: Lista de subcadenas (case-insensitive). Si el nombre contiene
            cualquiera de ellas, se excluye.
        recursive: Si es True, explora subdirectorios de forma recursiva.
            Si es False, solo examina el contenido inmediato de root.

    Returns:
        tuple[list[pathlib.Path], list[pathlib.Path]]: (directories, files)
    '''

    root_path = pathlib.Path(root)

    include_set = {e.lower().lstrip('.') for e in (include_extensions or [])}
    exclude_set = {e.lower().lstrip('.') for e in (exclude_extensions or [])}
    patterns = [p.lower() for p in (exclude_pattern or [])]

    directories: list[pathlib.Path] = []
    files: list[pathlib.Path] = []

    def scan(path: pathlib.Path, inherited_ignores: set[str]) -> None:
        local_ignores = set(inherited_ignores)
        local_ignores.update(get_exclude_names(path))

        if path.name in local_ignores:
            return

        for entry in path.iterdir():
            name = entry.name

            if name in local_ignores:
                continue

            if patterns and any(p in name.lower() for p in patterns):
                continue

            if not include_hidden and name.startswith('.'):
                continue

            if entry.is_file():
                ext = entry.suffix.lstrip('.').lower()
                include_ok = (not include_set) or (ext in include_set)
                exclude_ok = ext not in exclude_set

                if include_ok and exclude_ok:
                    files.append(entry)

            elif entry.is_dir():
                directories.append(entry)

                if recursive:
                    scan(entry, local_ignores)

    if root_path.is_dir():
        scan(root_path, set(get_exclude_names(root_path)))

    return directories, files
