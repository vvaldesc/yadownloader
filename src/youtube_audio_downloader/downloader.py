from time import sleep

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
            'verbose': False,
            'ignoreerrors': True,
            'min_views': 10
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

        print("Finished!!.")
    except Exception as e:
        print(f"Error!: {e}")


def main():
    try:
        print("Welcome to YaDownloader!")
        print("Your favorite YouTube audio downloader")
        print("-" * 40)
        video_url = input("Enter the YouTube video/playlist URL: ")
        output_path = input("Enter the folder to save the audio (leave empty for current folder): ")
        output_path = output_path if output_path else "./"
        download_audio_yt_dlp(video_url, output_path)
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

