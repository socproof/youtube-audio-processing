import yt_dlp
import os

def download_audio(url, output_dir="assets/audio"):
    """
    Downloads a YouTube video by URL and extracts the audio track
    in WAV format using yt-dlp, saving it with the video's title.

    Args:
        url: YouTube video URL.
        output_dir: Directory to save the audio file.
    """

    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    try:
        ydl_opts = {
            'format': 'bestaudio',
            'extract-audio': True,
            'audio-format': 'wav',
            'outtmpl': f"{output_dir}/%(title)s.wav",
            'noplaylist' : True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        print(f"Audio downloaded successfully to {output_dir}")

    except Exception as e:
        print(f"An error occurred: {e}")