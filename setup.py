from setuptools import setup, find_packages

setup(
    name="yadownload",
    version="1.0.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "yt-dlp>=2023.0.0",
    ],
    entry_points={
        'console_scripts': [
            'youtube-audio-download=youtube_audio_downloader.downloader:main',
        ],
    },
    author="Tu Nombre",
    description="Descargador de audio de YouTube",
    python_requires=">=3.6",
)