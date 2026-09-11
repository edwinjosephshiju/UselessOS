#!/bin/bash
set -e

echo "=== Configuring Openbox for Custom UselessOS Shell ==="

# 1. Configure LightDM Auto-login to Openbox
mkdir -p /etc/lightdm/lightdm.conf.d
cat > /etc/lightdm/lightdm.conf.d/50-autologin.conf <<EOF
[Seat:*]
autologin-user=vagrant
autologin-user-timeout=0
user-session=openbox
EOF

# 2. Configure Openbox rc.xml by preserving standard distribution defaults
mkdir -p /home/vagrant/.config/openbox
if [ -f /etc/xdg/openbox/rc.xml ]; then
    cp /etc/xdg/openbox/rc.xml /home/vagrant/.config/openbox/rc.xml
    # Inject application rule for Useless Shell to stay on desktop layer
    sed -i '/<\/applications>/i \  <application title="*Useless Shell*" class="*">\n    <layer>below<\/layer>\n    <desktop>all<\/desktop>\n  <\/application>' /home/vagrant/.config/openbox/rc.xml
    # Disable slow iconify animations for instant window responsiveness
    sed -i 's/<animateIconify>yes<\/animateIconify>/<animateIconify>no<\/animateIconify>/g' /home/vagrant/.config/openbox/rc.xml
fi

# 3. High-Performance Compositor Configuration (Damage-Aware, No Software Shadows)
mkdir -p /etc/xdg
cat > /etc/xdg/picom.conf <<EOF
# UselessOS 3.0 High-Performance Compositor Config
backend = "xrender";
use-damage = true;
vsync = false;
shadow = false;
fading = false;
inactive-opacity = 1.0;
active-opacity = 1.0;
frame-opacity = 1.0;
unredir-if-possible = true;
EOF

# 4. Configure Openbox Autostart for Vagrant user
cat > /home/vagrant/.config/openbox/autostart <<EOF
# Set solid Neobrutalist canvas background
which xsetroot >/dev/null 2>&1 && xsetroot -solid "#f5f4f0" || true

# Disable screen blanking & DPMS power saving
which xset >/dev/null 2>&1 && xset s off || true
which xset >/dev/null 2>&1 && xset s noblank || true
which xset >/dev/null 2>&1 && xset -dpms || true

# Start VirtualBox guest integration daemons if present
which VBoxClient >/dev/null 2>&1 && VBoxClient --vmsvga || true
which VBoxClient >/dev/null 2>&1 && VBoxClient --clipboard || true

# Start damage-aware picom compositor
which picom >/dev/null 2>&1 && picom -b --config /etc/xdg/picom.conf || true

# Start the Custom UselessOS PyQt Shell
python3 /opt/uselessos/useless_shell.py &
EOF

# Make sure vagrant owns its config
chown -R vagrant:vagrant /home/vagrant/.config

# 5. Fix audio permissions
usermod -aG audio,video vagrant

# 6. Optimize Boot Services (disable non-essential daily timers)
systemctl disable apt-daily.timer apt-daily-upgrade.timer man-db.timer 2>/dev/null || true

echo "=== System Configured ==="
