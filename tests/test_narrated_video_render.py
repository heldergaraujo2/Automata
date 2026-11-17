import unittest
from pathlib import Path
from automata.narrated_video_render import render_narrated_video, ffmpeg_subtitle_path

class NarratedVideoRenderTests(unittest.TestCase):
    def test_execution_disabled(self):
        with self.assertRaises(PermissionError):
            render_narrated_video(Path("video.mp4"), Path("voice.wav"), Path("out.mp4"))

    def test_subtitle_path_escapes_colon(self):
        self.assertIn("subtitles.srt", ffmpeg_subtitle_path(Path("subtitles.srt")))

if __name__ == "__main__":
    unittest.main()
