from time import sleep
import os
import platform
import re
import sys
import yt_dlp


def check_copyright_status(video_url):
    """
    Attempts to verify the copyright status of a video.
    Returns: (bool, str) - (is_probably_free, explanatory_message)
    """
    try:
        print("Checking copyright status...")
        # Configuration to extract only metadata without downloading
        ydl_opts = {
            'skip_download': True,
            'quiet': True,
            'no_warnings': True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)

            # Check explicit license (if available)
            license_info = info.get('license', '').lower()
            if 'creative commons' in license_info:
                return True, "The video is under Creative Commons license"

            # Look for terms related to free use in the description
            description = info.get('description', '').lower()
            free_terms = ['free to use', 'no copyright', 'creative commons', 'cc by', 'public domain']
            for term in free_terms:
                if term in description:
                    return True, f"The description mentions '{term}', it could be free to use"

            # Check if there are specific download restrictions
            if info.get('age_limit', 0) > 0:
                return False, "The video has age restrictions, possibly protected content"

            if info.get('is_live', False):
                return False, "The video is a live broadcast, possibly with copyright protection"

            # Check the title and channel for signs of official content
            title = info.get('title', '').lower()
            uploader = info.get('uploader', '').lower()
            official_terms = ['official', 'oficial', 'vevo', 'topic', '- topic']

            for term in official_terms:
                if term in title or term in uploader:
                    return False, f"The video appears to be official content ({term})"

            # If we can't clearly determine, return a warning
            return None, "The copyright status cannot be determined with certainty"

    except Exception as e:
        return None, f"Error checking rights: {e}"


def validate_url(url):
    """Validate that the URL is from YouTube"""
    youtube_regex = r'^(https?://)?(www\.)?(youtube\.com|youtu\.?be)/.+$'
    if not re.match(youtube_regex, url):
        raise ValueError("The URL does not appear to be a valid YouTube URL")
    return True


def get_ffmpeg_path():
    """Detect the operating system and return the appropriate path for FFmpeg"""
    system = platform.system()
    if system == "Windows":
        # Try to find FFmpeg in the provided path or in PATH
        if os.path.exists(r'C:\ffmpeg\bin\ffmpeg.exe'):
            return r'C:\ffmpeg\bin\ffmpeg.exe'
        else:
            return 'ffmpeg'  # Assume it's in PATH
    elif system in ["Linux", "Darwin"]:  # Linux or MacOS
        return 'ffmpeg'  # Assume it's in PATH
    else:
        return None  # Unknown system


def progress_hook(d):
    """Function to display download progress"""
    if d['status'] == 'downloading':
        percentage = d.get('_percent_str', 'Unknown')
        speed = d.get('_speed_str', 'Unknown')
        eta = d.get('_eta_str', 'Unknown')
        sys.stdout.write(f"\rDownloading: {percentage} | Speed: {speed} | ETA: {eta}")
        sys.stdout.flush()
    elif d['status'] == 'finished':
        print("\nDownload completed. Processing file...")


def download_audio_yt_dlp(video_url, output_path="./", audio_quality='192'):
    """Descargar audio de YouTube con opciones mejoradas"""
    try:
        validate_url(video_url)

        # Check copyright status
        is_free, copyright_message = check_copyright_status(video_url)

        if is_free is False:
            print(f"\n⚠️ COPYRIGHT WARNING: {copyright_message}")
            print("This video is likely protected by copyright.")
            proceed = input("Do you want to continue anyway? (y/n): ").lower().strip() == 'y'
            if not proceed:
                print("Download canceled by the user.")
                return
        elif is_free is None:
            print(f"\n⚠️ WARNING: {copyright_message}")
            print("Please ensure you have the right to download this content.")
            proceed = input("Do you want to continue? (y/n): ").lower().strip() == 'y'
            if not proceed:
                print("Download canceled by the user.")
                return
        else:
            print(f"\n✅ INFORMATION: {copyright_message}")

        ffmpeg_path = get_ffmpeg_path()
        if not ffmpeg_path:
            print("Warning: Could not determine the location of FFmpeg. Make sure you have it installed.")

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

    finally:
        print("\nNeed help? Contact the developer:")
        print("Email: vvaldescobos@gmail.com")
        print("-" * 40)
        sleep(3)


if __name__ == "__main__":
    main()