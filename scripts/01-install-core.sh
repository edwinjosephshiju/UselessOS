#!/bin/bash
set -e

echo "=== Installing Core UselessOS Packages (Openbox + Native PyQt6) ==="

export DEBIAN_FRONTEND=noninteractive

# Update package lists
apt-get update

# Install Openbox, LightDM, PyQt6/PyQt5, fonts, and tools
apt-get install -y --no-install-recommends \
    xserver-xorg \
    xserver-xorg-video-all \
    xserver-xorg-input-all \
    openbox \
    lightdm \
    lightdm-gtk-greeter \
    python3 \
    python3-pip \
    python3-pyqt6 \
    python3-pyqt6.qtsvg \
    python3-pyqt5 \
    python3-pyqt5.qtsvg \
    fonts-nanum \
    fonts-noto \
    x11-xserver-utils \
    python3-xdg \
    git \
    wget \
    unzip \
    alsa-utils \
    pulseaudio \
    wmctrl \
    xdotool \
    rfkill \
    picom

echo "=== Core Packages Installed ==="
