import sys
import os
import unittest
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "apps"))

from qwen_backend import QwenEngine, DEFAULT_HMM_PROMPT, CORPORATE_EXCUSE_PROMPT, OVERTHINKING_PROMPT, SARCASTIC_MASCOT_PROMPT

class TestQwenBackend(unittest.TestCase):
    def test_presets_exist(self):
        presets = QwenEngine.get_presets()
        self.assertIn("Profound Hesitation (Hmm...)", presets)
        self.assertIn("Corporate Bureaucrat", presets)
        self.assertIn("Overthinking Paranoia", presets)
        self.assertIn("Sarcastic OS Mascot", presets)
        self.assertIn("Custom Persona", presets)

    def test_backend_info(self):
        info = QwenEngine.get_backend_info()
        self.assertIn("name", info)
        self.assertIn("status", info)
        self.assertIn("type", info)

    def test_custom_system_prompt_stream(self):
        custom_prompt = "You are a test system prompt for unit testing."
        stream = QwenEngine.create_stream("test user query", system_prompt=custom_prompt)
        self.assertEqual(stream.system_prompt, custom_prompt)
        self.assertEqual(stream.user_prompt, "test user query")

        tokens = []
        thoughts = []
        finished = []

        stream.token_emitted.connect(lambda t: tokens.append(t))
        stream.thought_emitted.connect(lambda th: thoughts.append(th))
        stream.finished_inference.connect(lambda th, ans: finished.append((th, ans)))

        stream.start()
        # Wait up to 5 seconds for completion
        start = time.time()
        while not finished and time.time() - start < 5.0:
            time.sleep(0.05)

        self.assertTrue(len(finished) > 0, "Inference did not finish in time")
        thought_res, ans_res = finished[0]
        self.assertTrue(len(ans_res) > 0)
        print(f"[TEST SUCCESS] Qwen Stream Result: {ans_res[:50]}...")

if __name__ == "__main__":
    unittest.main()
