# YouTube Audio Processing

## Description

This project helps you download and transcribe the audio from public YouTube videos.

## What You Need

* **Python:** Install Python on your computer from the official website: [https://www.python.org/downloads/](https://www.python.org/downloads/). Choose the version compatible with your operating system and follow the installation instructions.
* **FFmpeg:** This project uses FFmpeg to handle audio conversion.
    * **Windows:** Download the FFmpeg installer from the official site: [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html). Run the installer and follow the on-screen instructions. **Important:** During installation, make sure to check the option to "Add FFmpeg to the system PATH environment variable" so that the script can find FFmpeg.
    * **macOS:** Install FFmpeg using Homebrew (if you have it installed): Open Terminal and run the command `brew install ffmpeg`.
    * **Linux:** Install FFmpeg using your distribution's package manager. For example, on Ubuntu/Debian, run the command `sudo apt-get install ffmpeg`.
* **This Project:** Clone the repository from GitHub [YouTube Audio Processing](https://github.com/socproof/youtube-audio-processing.git) or download the archive manually.

## Installation

1. **Open Terminal/Command Prompt:**
    * **Windows:** Press `Win + R`, type `cmd`, and press `Enter`.
    * **macOS:** Open "Spotlight" (click the magnifying glass icon in the top-right corner), type "Terminal", and press `Enter`.
    * **Linux:** Launch the Terminal from your applications menu.

2. **Navigate to the Project Folder:**
    * In Terminal, type `cd` (with a space after), then drag and drop the project folder from your file manager into the Terminal window, and press `Enter`.

3. **Install Dependencies:**
    * Type the command `pip install -r requirements.txt` and press `Enter`. This will install the necessary libraries for the project to work.

## Usage

1. **Run the Project:**
    * In Terminal, type `python main.py` and press `Enter`.

2. **Enter the Video URL:**
    * The program will ask you for a YouTube video link. Copy the link from your browser's address bar and paste it into the Terminal, then press `Enter`.

3. **Wait for the Download to Finish:**
    * The program will download the audio track of the video, convert it to WAV format, and save it in the `assets/audio` folder inside the project folder. The file name will match the video title.

## Additional Information

* Make sure you have the right to download and use content from YouTube.
* The project is under development.  
