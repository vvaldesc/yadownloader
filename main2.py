import yt_dlp

def download_audio_yt_dlp(video_url, output_path="./"):
    try:
        ydl_opts = {
            'format': 'bestaudio/best',  # Descargar solo el mejor audio disponible
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',  # Convertir a MP3
                'preferredquality': '192',  # Calidad de audio
            }],
            'ffmpeg_location': r'C:\ffmpeg\bin\ffmpeg.exe',
            'outtmpl': f'{output_path}/%(title)s.%(ext)s',
            'verbose': True,
            'ignoreerrors': True,
            'min_views': 10
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

        print("Descarga completada.")
    except Exception as e:
        print(f"Ha ocurrido un error: {e}")


if __name__ == "__main__":
    video_url = input("Introduce la URL del video de YouTube: ")
    output_path = input("Introduce la carpeta donde guardar el audio (deja vacío para la carpeta actual): ")
    output_path = output_path if output_path else "./"
    download_audio_yt_dlp(video_url, output_path)
