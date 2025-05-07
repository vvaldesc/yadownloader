# Descargador de Audio de YouTube

Una herramienta simple para descargar audio de videos de YouTube en formato MP3.

## Requisitos previos

1. Python 3.6 o superior
2. FFmpeg instalado (https://ffmpeg.org/download.html)

## Instalación

1. **Instalar FFmpeg**:
   - Windows: Descarga desde https://ffmpeg.org/download.html
   - Linux: `sudo apt-get install ffmpeg`
   - macOS: `brew install ffmpeg`

2. **Instalar el paquete**:
   ```bash
   pip install youtube-audio-downloader
   ```

## Uso

1. **Desde la línea de comandos**:
   ```bash
   youtube-audio-download
   ```

2. **Como módulo de Python**:
   ```python
   from youtube_audio_downloader.downloader import download_audio_yt_dlp
   
   download_audio_yt_dlp("URL_DEL_VIDEO", "RUTA_DE_SALIDA")
   ```

## Notas
- La ruta de salida es opcional. Por defecto, descarga en el directorio actual.
- Asegúrate de que FFmpeg esté correctamente instalado y configurado en tu sistema.