#!/bin/bash
set -e

echo "=== Provisioning Qwen 3.5 0.8B Cognitive Backend ==="

mkdir -p /opt/uselessos/models

# Download model if not already present
if [ ! -f "/opt/uselessos/models/Qwen3.5-0.8B-Q4_K_M.gguf" ]; then
    echo "[INFO] Downloading Qwen 3.5 0.8B GGUF weights..."
    python3 /opt/uselessos/download_model.py || true
fi

# Set proper permissions
chown -R vagrant:vagrant /opt/uselessos/models || true
chmod 644 /opt/uselessos/models/*.gguf 2>/dev/null || true

echo "=== Qwen 3.5 Backend Provisioned ==="
