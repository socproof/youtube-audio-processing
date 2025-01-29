import yt_dlp
import os
import subprocess
import platform
import shutil

def download_audio(url, output_dir="assets/audio"):
    """
    Downloads a YouTube video by URL and extracts the audio track
    in WAV format using yt-dlp, saving it with the video's ID.
    If the downloaded audio is not in WAV format, it will be converted
    using FFmpeg. It first tries to use the system's FFmpeg (if available in PATH),
    otherwise, it falls back to a platform-specific binary in the "deps" directory.

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
            'outtmpl': f"{output_dir}/%(id)s.%(ext)s",
            'noplaylist': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            ydl.download([url])

            audio_filename = f"{output_dir}/{info['id']}.{info['ext']}"
            wav_filename = f"{output_dir}/{info['id']}.wav"

            # Convert to WAV if necessary
            if info['ext'] != 'wav':
                ffmpeg_command = ['ffmpeg', '-i', audio_filename, wav_filename]

                # Check if ffmpeg is in PATH
                if shutil.which('ffmpeg'):
                    subprocess.call(ffmpeg_command)
                else:
                    system = platform.system().lower()
                    ffmpeg_path = os.path.join(
                        "deps", f"{system}", "ffmpeg"
                    )
                    subprocess.call([ffmpeg_path, '-i', audio_filename, wav_filename])

                os.remove(audio_filename)

        print(f"Audio downloaded successfully to {output_dir}")
        return wav_filename

    except Exception as e:
        print(f"An error occurred: {e}")