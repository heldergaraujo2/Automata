import tempfile
import unittest
from pathlib import Path
from automata.local_narration import PiperConfig, narration_text, storyboard_srt, synthesize_piper

class LocalNarrationTests(unittest.TestCase):
    def setUp(self):
        self.board = {"scenes": [{"seconds": 3, "narration": "Olá!"}, {"seconds": 4, "narration": "Veja o produto."}]}

    def test_text_and_subtitles(self):
        self.assertEqual(narration_text(self.board), "Olá! Veja o produto.")
        srt = storyboard_srt(self.board)
        self.assertIn("00:00:03,000 --> 00:00:07,000", srt)

    def test_execution_blocked(self):
        with self.assertRaises(PermissionError):
            synthesize_piper("Olá", PiperConfig("piper", Path("model.onnx"), Path("model.onnx.json")),
                             Path("out.wav"))
if __name__ == "__main__":
    unittest.main()
