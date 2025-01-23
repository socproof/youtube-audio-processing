from audio_processing.download import download_audio

if __name__ == "__main__":
    video_url = input("Enter the YouTube video URL: ")
    download_audio(video_url) # will be stored in the assets/audio dir by default