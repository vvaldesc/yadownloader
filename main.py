from pytube import YouTube
import os

def download_audio(video_url, output_path="./"):
    try:
        # Crear objeto YouTube
        yt = YouTube(video_url, use_oauth=True, allow_oauth_cache=True)

        # Obtener la mejor calidad de audio
        audio_stream = yt.streams.filter(only_audio=True).order_by("abr").desc().first()

        # Verificar si se encontró un stream de audio
        if not audio_stream:
            print("No se encontró un stream de audio.")
            return

        # Descargar el audio
        print(f"Descargando: {yt.title}")
        out_file = audio_stream.download(output_path)

        # Renombrar archivo a formato .mp3
        base, ext = os.path.splitext(out_file)
        new_file = base + ".mp3"
        os.rename(out_file, new_file)

        print(f"Audio descargado y guardado como: {new_file}")
    except Exception as e:
        print(f"Ha ocurrido un error: {e}")


# Ejemplo de uso
if __name__ == "__main__":
    video_url = input("Introduce la URL del video de YouTube: ")
    output_path = input("Introduce la carpeta donde guardar el audio (deja vacío para la carpeta actual): ")
    output_path = output_path if output_path else "./"
    download_audio(video_url, output_path)
