from . import log

import pathlib
import tarfile


def compress_path_to_tar_gz(
    output_path: str | pathlib.Path,
    source_path: str | pathlib.Path,
) -> None:
    '''
    Compress a file or directory into a .tar.gz archive.

    Args:
        output_path: Path to the output .tar.gz file.
        source_path: File or directory to compress.

    Raises:
        FileExistsError: If the output file already exists.
        FileNotFoundError: If the source path does not exist.
    '''

    output_path = pathlib.Path(output_path)
    source_path = pathlib.Path(source_path)

    if output_path.exists():
        raise FileExistsError(f'Output file already exists: "{output_path}"')

    if not source_path.exists():
        raise FileNotFoundError(f'Source path does not exist: "{source_path}"')

    with tarfile.open(output_path, mode="w:gz") as tar:
        tar.add(source_path, arcname=source_path.name)

    log.info(f'"{source_path}" compressed into "{output_path}".')
