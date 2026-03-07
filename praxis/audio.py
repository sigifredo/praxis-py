

import log
import pathlib
import pydub
import tempfile
import typing


TARGET_SR = 16000
TARGET_CH = 1
TARGET_SAMPLE_WIDTH = 2


def convert_to_wav_pydub(input_path: pathlib.Path, output_path: pathlib.Path | None = None) -> pathlib.Path:
    '''
    Convierte un archivo de audio a WAV PCM s16le (16 kHz, mono) usando pydub.

    Carga el archivo de entrada mediante `pydub.AudioSegment`, normaliza la
    frecuencia de muestreo, el número de canales y el ancho de muestra según
    las constantes configuradas (por ejemplo, TARGET_SR, TARGET_CH,
    TARGET_SAMPLE_WIDTH), y exporta el resultado como un archivo WAV temporal
    codificado en `pcm_s16le`.

    Args:
        input_path (pathlib.Path): Ruta al archivo de audio original.
        output_path (pathlib.Path | None, optional):
            Ruta del archivo WAV de salida. Si es `None`, se genera un archivo
            temporal mediante `tempfile.NamedTemporaryFile`.

    Returns:
        pathlib.Path: Ruta del archivo WAV generado.

    Raises:
        Exception: Cualquier excepción propagada por pydub/ffmpeg durante la
            carga o exportación del archivo.
    '''

    seg = pydub.AudioSegment.from_file(str(input_path))
    seg = seg.set_frame_rate(TARGET_SR).set_channels(TARGET_CH).set_sample_width(TARGET_SAMPLE_WIDTH)

    if output_path is None:
        tmp = tempfile.NamedTemporaryFile(prefix='whisper_', suffix='.wav', delete=False)
        tmp_path = pathlib.Path(tmp.name)
        tmp.close()
        output_path = tmp_path

    seg.export(str(output_path), format='wav', codec='pcm_s16le')
    log.info(f'Audio convertido con pydub -> {output_path}')

    return output_path


def needs_wav_conversion(
    info: typing.Optional[typing.Tuple[int, int, int]],
    path: pathlib.Path,
) -> bool:
    '''
    Determina si un archivo de audio requiere conversión a WAV PCM s16le
    (16 kHz, mono, 16-bit).

    Se considera necesaria la conversión cuando:
    - No se pudo obtener información técnica del audio (info es None).
    - La frecuencia de muestreo difiere de TARGET_SR.
    - El número de canales difiere de TARGET_CH.
    - El ancho de muestra difiere de TARGET_SAMPLE_WIDTH.
    - La extensión del archivo no es ".wav".

    Args:
        info (Optional[Tuple[int, int, int]]): Tupla con
            (sample_rate, channels, sample_width en bytes), o None si no se
            pudo leer la metadata.
        path (pathlib.Path): Ruta al archivo de audio original.

    Returns:
        bool: True si el archivo debe convertirse; False si ya cumple con
        las especificaciones requeridas.
    '''

    if info is None:
        return True

    sr, ch, sw = info
    is_wav_ext = path.suffix.lower() == '.wav'

    return not (sr == TARGET_SR and ch == TARGET_CH and sw == TARGET_SAMPLE_WIDTH and is_wav_ext)

def probe_audio(path: pathlib.Path) -> typing.Optional[typing.Tuple[int, int, int]]:
    '''
    Inspecciona las propiedades básicas de un archivo de audio usando pydub.

    Intenta cargar el archivo y extraer:
    - Frecuencia de muestreo (frame_rate)
    - Número de canales (channels)
    - Ancho de muestra en bytes (sample_width)

    Si ocurre algún error durante la lectura o decodificación, registra
    una advertencia y devuelve None sin forzar la conversión.

    Nota:
        pydub decodifica el archivo completo en memoria, lo que puede
        implicar un consumo significativo de RAM en archivos largos.

    Args:
        path (pathlib.Path): Ruta al archivo de audio a inspeccionar.

    Returns:
        Optional[Tuple[int, int, int]]: Tupla (frame_rate, channels,
        sample_width) si la lectura es exitosa; None en caso de error.
    '''

    try:
        seg = pydub.AudioSegment.from_file(str(path))
        return seg.frame_rate, seg.channels, seg.sample_width
    except Exception as e:
        log.warning(f'pydub no pudo abrir/decodificar el archivo: {e}')
        return None




