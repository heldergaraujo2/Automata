import unittest
from pathlib import Path
from automata.media_render_gate import RenderAsset
from automata.verified_video_workflow import VideoJob, produce_for_review, planned_job_status

class VerifiedVideoWorkflowTests(unittest.TestCase):
    def job(self, **changes):
        asset = RenderAsset(Path("example.mp4"), "a"*64, "video", True)
        values = dict(top=asset, product=asset, split_output=Path("split.mp4"),
                      final_output=Path("final.mp4"), caption="Promoção com link oficial",
                      review_directory=Path("reviews"))
        values.update(changes)
        return VideoJob(**values)
    def test_disabled_by_default(self):
        with self.assertRaises(PermissionError):
            produce_for_review(None, self.job())
    def test_plan_has_no_side_effects(self):
        self.assertFalse(planned_job_status(self.job())["publishing_enabled"])
    def test_requires_video_inputs(self):
        image = RenderAsset(Path("image.jpg"), "a"*64, "image", True)
        with self.assertRaises(ValueError):
            produce_for_review(None, self.job(top=image), allow_execution=True)
    def test_requires_caption(self):
        with self.assertRaises(ValueError):
            produce_for_review(None, self.job(caption=""), allow_execution=True)
    def test_rejects_subtitles_without_voice(self):
        with self.assertRaises(ValueError):
            produce_for_review(None, self.job(subtitles_srt=Path("captions.srt")), allow_execution=True)

if __name__ == "__main__":
    unittest.main()
