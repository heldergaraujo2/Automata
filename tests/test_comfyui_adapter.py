import json
import tempfile
import unittest
from pathlib import Path
from automata.comfyui_adapter import validate_endpoint, load_api_workflow, prepare_workflow, submit_workflow

class ComfyUIAdapterTests(unittest.TestCase):
    def test_local_only(self):
        self.assertEqual(validate_endpoint("http://127.0.0.1:8188"), "http://127.0.0.1:8188")
        with self.assertRaises(ValueError):
            validate_endpoint("https://remote.example:8188")
    def test_workflow_prompt(self):
        original = {"6": {"class_type": "CLIPTextEncode", "inputs": {"text": "old", "clip": ["4", 1]}}}
        result = prepare_workflow(original, prompt_node_id="6", prompt="new")
        self.assertEqual(result["6"]["inputs"]["text"], "new")
        self.assertEqual(original["6"]["inputs"]["text"], "old")
    def test_execution_off_by_default(self):
        with self.assertRaises(PermissionError):
            submit_workflow({"6": {"class_type": "CLIPTextEncode", "inputs": {"text": "x"}}})
    def test_load(self):
        with tempfile.TemporaryDirectory() as temp:
            file = Path(temp) / "workflow.json"
            file.write_text(json.dumps({"6": {"class_type": "CLIPTextEncode", "inputs": {"text": "x"}}}))
            self.assertIn("6", load_api_workflow(file))

if __name__ == "__main__":
    unittest.main()
