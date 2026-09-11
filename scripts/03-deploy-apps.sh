#!/bin/bash
set -e

echo "=== Deploying UselessOS Python Apps & Shell ==="

# Clean nginx (no longer needed, but remove if it was installed)
apt-get remove -y nginx || true

# Copy apps, fonts, assets, and custom shell to /opt/uselessos
mkdir -p /opt/uselessos
cp -r /vagrant/apps/* /opt/uselessos/
chmod +x /opt/uselessos/*.py

# Install fonts system-wide so all apps render them smoothly
mkdir -p /usr/local/share/fonts/uselessos
cp -r /opt/uselessos/fonts/* /usr/local/share/fonts/uselessos/ 2>/dev/null || true
which fc-cache >/dev/null 2>&1 && fc-cache -f /usr/local/share/fonts/uselessos || true

# Precompile Python bytecode for instant application startup
python3 -m compileall -q /opt/uselessos

echo "=== Applications Deployed ==="
