import yaml
import logging
import warnings

from audio_processing.download import download_audio
from audio_processing.speech_processing import process_speech

warnings.filterwarnings("ignore")
logging.basicConfig(level=logging.WARNING)

if __name__ == "__main__":
   video_url = input("Enter the YouTube video URL: ")
   audio_file_path = download_audio(video_url)

   with open("params.yaml", "r", encoding="utf-8") as stream:
    params = yaml.safe_load(stream)
    process_speech(audio_file_path, params=params)