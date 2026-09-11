#!/usr/bin/env python3
"""
Model Downloader for UselessOS:
Fetches Qwen 3.5 0.8B GGUF (Q4_K_M, ~507 MB) from Hugging Face.
"""
import os
import sys
import urllib.request

MODEL_URL = "https://huggingface.co/unsloth/Qwen3.5-0.8B-GGUF/resolve/main/Qwen3.5-0.8B-Q4_K_M.gguf"
DEFAULT_TARGET_DIR = "/opt/uselessos/models"
LOCAL_FALLBACK_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "models")

def download_progress(count, block_size, total_size):
    downloaded = count * block_size
    percent = min(100.0, (downloaded / total_size) * 100.0) if total_size > 0 else 0
    mb_down = downloaded / (1024 * 1024)
    mb_total = total_size / (1024 * 1024) if total_size > 0 else 0
    sys.stdout.write(f"\r[Qwen Downloader] {mb_down:.1f}MB / {mb_total:.1f}MB ({percent:.1f}%)")
    sys.stdout.flush()

def main():
    target_dir = DEFAULT_TARGET_DIR if os.path.exists("/opt/uselessos") else LOCAL_FALLBACK_DIR
    os.makedirs(target_dir, exist_ok=True)
    target_file = os.path.join(target_dir, "Qwen3.5-0.8B-Q4_K_M.gguf")

    print("========================================")
    print("   UselessOS Model Provisioner")
    print("   Target: Qwen 3.5 (0.8B) Q4_K_M GGUF")
    print("========================================")
    print(f"Target Destination: {target_file}")

    if os.path.exists(target_file):
        size = os.path.getsize(target_file)
        if size > 500 * 1024 * 1024:
            print(f"[OK] Model already present ({size / (1024*1024):.1f}MB).")
            return 0
        else:
            print("[INFO] Existing file is incomplete. Resuming download...")

    print(f"Fetching from: {MODEL_URL}...")
    try:
        urllib.request.urlretrieve(MODEL_URL, target_file, reporthook=download_progress)
        print("\n[SUCCESS] Model downloaded successfully!")
        return 0
    except Exception as e:
        print(f"\n[ERROR] Download failed: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
