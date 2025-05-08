from time import sleep
import os
import platform
import re
import sys
import yt_dlp


def validate_url(url):
    """Validar que la URL sea de YouTube"""
    youtube_regex = r'^(https?://)?(www\.)?(youtube\.com|youtu\.?be)/.+$'
    if not re.match(youtube_regex, url):
        raise ValueError("La URL no parece ser una URL válida de YouTube")
    return True


def get_ffmpeg_path():
    """Detectar el sistema operativo y devolver la ruta apropiada para FFmpeg"""
    system = platform.system()
    if system == "Windows":
        # Intenta encontrar FFmpeg en la ruta proporcionada o en PATH
        if os.path.exists(r'C:\ffmpeg\bin\ffmpeg.exe'):
            return r'C:\ffmpeg\bin\ffmpeg.exe'
        else:
            return 'ffmpeg'  # Asume que está en PATH
    elif system in ["Linux", "Darwin"]:  # Linux o MacOS
        return 'ffmpeg'  # Asume que está en PATH
    else:
        return None  # Sistema desconocido


def progress_hook(d):
    """Función para mostrar el progreso de la descarga"""
    if d['status'] == 'downloading':
        percentage = d.get('_percent_str', 'Desconocido')
        speed = d.get('_speed_str', 'Desconocido')
        eta = d.get('_eta_str', 'Desconocido')
        sys.stdout.write(f"\rDescargando: {percentage} | Velocidad: {speed} | ETA: {eta}")
        sys.stdout.flush()
    elif d['status'] == 'finished':
        print("\nDescarga completada. Procesando archivo...")


def download_audio_yt_dlp(video_url, output_path="./", audio_quality='192'):
    """Descargar audio de YouTube con opciones mejoradas"""
    try:
        validate_url(video_url)

        ffmpeg_path = get_ffmpeg_path()
        if not ffmpeg_path:
            print("Advertencia: No se pudo determinar la ubicación de FFmpeg. Asegúrate de tenerlo instalado.")

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': audio_quality,
            }],
            'outtmpl': f'{output_path}/%(title)s.%(ext)s',
            'verbose': False,
            'ignoreerrors': True,
            'min_views': 10,
            'progress_hooks': [progress_hook],
        }

        # Agregar la ubicación de FFmpeg si está disponible
        if ffmpeg_path:
            ydl_opts['ffmpeg_location'] = ffmpeg_path

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

        print("\n¡Descarga finalizada con éxito!")
    except ValueError as ve:
        print(f"Error de validación: {ve}")
    except yt_dlp.utils.DownloadError as de:
        print(f"Error de descarga: No se pudo acceder al contenido. {de}")
    except yt_dlp.utils.ExtractorError as ee:
        print(f"Error al extraer información: {ee}")
    except Exception as e:
        print(f"Error inesperado: {e}")


def show_disclaimer():
    # Mantiene la función original sin cambios
    print("=" * 80)
    print("AVISO LEGAL / LEGAL DISCLAIMER")
    print("=" * 80)

    # Spanish version
    print("[ESPAÑOL]")
    print("Este software ha sido desarrollado en España con fines exclusivamente:")
    print("- Educativos y de aprendizaje en programación")
    print("- Demostración de portfolio personal")
    print("- Uso personal y privado")
    print("\nDeclaración de responsabilidad:")
    print("- Este es un proyecto sin ánimo de lucro")
    print("- Los usuarios son responsables del uso conforme a la legislación española")
    print("- El desarrollador no almacena ni distribuye contenido protegido")
    print("- El uso se limita a contenido autorizado según la Ley de Propiedad Intelectual")
    print("- La copia privada debe respetar los límites establecidos en la normativa vigente")
    print("\nAl usar este software, aceptas cumplir con la legislación española aplicable.")

    print("\n" + "=" * 80 + "\n")

    # English version
    print("[ENGLISH]")
    print("This software has been developed in Spain exclusively for:")
    print("- Educational and programming learning purposes")
    print("- Personal portfolio demonstration")
    print("- Personal and private use")
    print("\nLiability statement:")
    print("- This is a non-profit project")
    print("- Users are responsible for compliance with Spanish legislation")
    print("- The developer does not store or distribute protected content")
    print("- Usage is limited to authorized content under Spanish Intellectual Property Law")
    print("- Private copying must respect the limits established by current regulations")
    print("\nBy using this software, you agree to comply with applicable Spanish legislation.")
    print("=" * 80)


def main():
    try:
        show_disclaimer()
        sleep(1)
        print("Welcome to YaDownloader!")
        print("Your favorite YouTube audio downloader")
        print("-" * 40)

        video_url = input("Enter the YouTube video/playlist URL: ")

        output_path = input("Enter the folder to save the audio (leave empty for current folder): ")
        output_path = output_path if output_path else "./"

        # Nueva opción para calidad de audio
        audio_quality_options = {
            "1": "128",
            "2": "192",
            "3": "256",
            "4": "320"
        }
        print("\nSelect audio quality:")
        print("1. 128 kbps (menor tamaño)")
        print("2. 192 kbps (calidad estándar)")
        print("3. 256 kbps (alta calidad)")
        print("4. 320 kbps (calidad máxima)")
        quality_choice = input("Choose an option [2]: ").strip() or "2"

        audio_quality = audio_quality_options.get(quality_choice, "192")

        print("-" * 40)
        print(f"Descargando en calidad {audio_quality}kbps...")
        download_audio_yt_dlp(video_url, output_path, audio_quality)

        print("-" * 40)
        print("Thanks for using YaDownloader!")
        print("See you next time!")
    except Exception as e:
        print("-" * 40)
        print("Oops! Something went wrong:")
        print(f"Error: {str(e)}")
        print("\nNeed help? Contact the developer:")
        print("Email: developer@yadownloader.com")
        print("GitHub: github.com/yadownloader")
        print("Discord: discord.gg/yadownloader")
    finally:
        print("-" * 40)
        sleep(3)


if __name__ == "__main__":
    main()