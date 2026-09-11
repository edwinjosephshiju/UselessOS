import sys
import os
import time
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "apps"))

import useless_style
from qwen_backend import QwenEngine

class TestPerformanceBenchmark(unittest.TestCase):
    def test_asset_caching_speedup(self):
        """Verify that get_icon_path and get_asset_path benefit from LRU caching."""
        # Prime cache
        useless_style.get_icon_path("excuses.png")
        useless_style.get_asset_path("hero_canvas.svg")
        
        # Measure 10,000 cached calls
        start = time.perf_counter()
        for _ in range(10000):
            p1 = useless_style.get_icon_path("excuses.png")
            p2 = useless_style.get_asset_path("hero_canvas.svg")
        elapsed = time.perf_counter() - start
        
        # 10,000 cached lookups should finish in under 50ms (0.05s)
        self.assertLess(elapsed, 0.05, f"10k asset lookups took {elapsed:.4f}s; expected < 0.05s")
        print(f"\n[BENCHMARK] 10,000 asset lookups completed in {elapsed*1000:.2f} ms ({10000/elapsed:.0f} ops/sec)")

    def test_streaming_latency(self):
        """Verify that standalone synthesis emits response in sub-second time."""
        stream = QwenEngine.create_stream("What is the meaning of life?", system_prompt="Test")
        tokens = []
        finished = []
        
        stream.token_emitted.connect(lambda t: tokens.append(t))
        stream.finished_inference.connect(lambda th, ans: finished.append((th, ans)))
        
        start = time.perf_counter()
        stream.start()
        
        while not finished and time.perf_counter() - start < 3.0:
            time.sleep(0.01)
            
        total_time = time.perf_counter() - start
        self.assertTrue(len(finished) > 0, "Stream did not finish")
        self.assertLess(total_time, 1.5, f"Inference streaming took {total_time:.2f}s; expected < 1.5s")
        print(f"[BENCHMARK] Full cognitive synthesis & streaming completed in {total_time*1000:.1f} ms")

if __name__ == "__main__":
    unittest.main()
