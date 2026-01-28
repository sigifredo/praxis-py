import tarfile


def compress_directory(dst_file, src_directory):
    '''
    Comprime un directorio en un archivo .tar.gz.

    :param src_directory: Ruta del directorio que se desea comprimir.
    :param dst_file: Nombre del archivo .tar.gz que se generará.
    '''

    with tarfile.open(dst_file, 'w:gz') as file_tar:
        file_tar.add(src_directory, arcname=os.path.basename(src_directory))

    print(f'Directorio "{src_directory}" comprimido en "{dst_file}".')
