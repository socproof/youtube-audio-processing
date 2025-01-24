import unittest
import os
from audio_processing.download import download_audio

class TestDownloadAudio(unittest.TestCase):

    def setUp(self):
        """Set up for test methods."""
        self.test_url = "https://www.youtube.com/watch?v=tPEE9ZwTmy0"
        self.expected_file = "assets/audio/Shortest Video on Youtube.wav"

    def test_download_audio_success(self):
        """Test successful audio download with valid URL."""
        download_audio(self.test_url)
        self.assertTrue(os.path.exists(self.expected_file))

    def tearDown(self):
        """Cleanup test files."""
        try:
            os.remove(self.expected_file)
        except FileNotFoundError:
            pass

if __name__ == '__main__':
    unittest.main()