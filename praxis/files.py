
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



def get_files_recursively(
    root: str | pathlib.Path,
    include_hidden: bool = False,
    include_extensions: typing.Iterable[str] | None = None,
    exclude_extensions: typing.Iterable[str] | None = None,
    exclude_pattern: str = None,
) -> tuple[list[pathlib.Path], list[pathlib.Path]]:
    '''
    Recursively walk a directory and return filtered subdirectories and files.

    Args:
        root: Base path to explore.
        include_hidden: If True, include hidden files and directories ('.' prefix).
        include_extensions: Extensions to include (e.g. {"mp4", "mkv"}). If None or empty,
            all extensions are included unless explicitly excluded.
        exclude_extensions: Extensions to exclude (e.g. {"png", "jpg"}).
        exclude_pattern: Case-insensitive substring. If present in the name, the entry is excluded.

    Returns:
        A tuple (directories, files) where:
            directories: Found subdirectories, excluding those ignored by `.signore`,
                pattern filters, or hidden rules.
            files: Found files, filtered by pattern, hidden rules, and extensions.

    Notes:
        - Paths are returned as `pathlib.Path` objects.
        - Files without an extension have `ext == ""`.
    '''

    root_path = pathlib.Path(root)

    include_set = {e.lower().lstrip('.') for e in (include_extensions or [])}
    exclude_set = {e.lower().lstrip('.') for e in (exclude_extensions or [])}
    pattern = exclude_pattern.lower() if exclude_pattern else None

    directories: list[pathlib.Path] = []
    files: list[pathlib.Path] = []

    def recursive_scan(path: pathlib.Path, inherited_ignores: set[str]) -> None:
        local_ignores = set(inherited_ignores)
        local_ignores.update(get_exclude_names(path))

        if path.name in local_ignores:
            return

        for entry in path.iterdir():
            name = entry.name

            if name in local_ignores:
                continue

            if pattern and pattern in name.lower():
                continue

            if not include_hidden and name.startswith("."):
                continue

            if entry.is_file():
                ext = entry.suffix.lstrip('.').lower()
                include_ok = (not include_set) or (ext in include_set)
                exclude_ok = ext not in exclude_set

                if include_ok and exclude_ok:
                    files.append(entry)

            elif entry.is_dir():
                directories.append(entry)
                recursive_scan(entry, local_ignores)

    if root_path.is_dir():
        recursive_scan(root_path, set(get_exclude_names(root_path)))

    return directories, files
