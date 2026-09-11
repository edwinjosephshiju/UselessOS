#!/usr/bin/env bash
set -euo pipefail

# ==============================================================================
# UselessOS 3.0: Hybrid Live ISO Generator
# Builds a bootable UEFI + Legacy BIOS Debian 12 Live ISO containing the
# custom UselessOS PyQt6 desktop shell, Neobrutalist theme, and all 10 apps.
# ==============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
BUILD_DIR="$REPO_ROOT/build"
OUTPUT_ISO="$BUILD_DIR/UselessOS-3.0-amd64.iso"

echo "=== [1/6] Preparing Build Environment ==="
mkdir -p "$BUILD_DIR"

# Install required host utilities if running with root privileges
if [ "$(id -u)" -eq 0 ]; then
    export DEBIAN_FRONTEND=noninteractive
    apt-get update -qq
    apt-get install -y -qq \
        debootstrap \
        squashfs-tools \
        xorriso \
        isolinux \
        syslinux-common \
        grub-pc-bin \
        grub-efi-amd64-bin \
        mtools \
        dosfstools
fi

WORK_DIR="$(mktemp -d -t uselessos-iso-XXXXXX)"
ROOTFS="$WORK_DIR/rootfs"
CD_DIR="$WORK_DIR/cd"

cleanup() {
    echo "=== Cleaning up build workspace ==="
    if [ -d "$ROOTFS/proc" ] && mountpoint -q "$ROOTFS/proc"; then
        umount -lf "$ROOTFS/proc" 2>/dev/null || true
    fi
    if [ -d "$ROOTFS/sys" ] && mountpoint -q "$ROOTFS/sys"; then
        umount -lf "$ROOTFS/sys" 2>/dev/null || true
    fi
    if [ -d "$ROOTFS/dev/pts" ] && mountpoint -q "$ROOTFS/dev/pts"; then
        umount -lf "$ROOTFS/dev/pts" 2>/dev/null || true
    fi
    if [ -d "$ROOTFS/dev" ] && mountpoint -q "$ROOTFS/dev"; then
        umount -lf "$ROOTFS/dev" 2>/dev/null || true
    fi
    rm -rf "$WORK_DIR"
}
trap cleanup EXIT

echo "=== [2/6] Debootstrapping Debian 12 Bookworm Base ==="
debootstrap --variant=minbase --arch=amd64 bookworm "$ROOTFS" http://deb.debian.org/debian/

# Mount virtual filesystems for chroot
mount -t proc none "$ROOTFS/proc"
mount -t sysfs none "$ROOTFS/sys"
mount -o bind /dev "$ROOTFS/dev"
mount -t devpts none "$ROOTFS/dev/pts"

echo "=== [3/6] Configuring Live System & Dependencies ==="
cat > "$ROOTFS/etc/apt/sources.list" <<EOF
deb http://deb.debian.org/debian/ bookworm main contrib non-free non-free-firmware
deb http://security.debian.org/debian-security bookworm-security main contrib non-free non-free-firmware
deb http://deb.debian.org/debian/ bookworm-updates main contrib non-free non-free-firmware
EOF

# Set hostname
echo "uselessos" > "$ROOTFS/etc/hostname"
cat > "$ROOTFS/etc/hosts" <<EOF
127.0.0.1   localhost
127.0.1.1   uselessos
EOF

# Install kernel, live-boot, and base system
chroot "$ROOTFS" /bin/bash -c "
    export DEBIAN_FRONTEND=noninteractive
    apt-get update -qq
    apt-get install -y -qq --no-install-recommends \
        linux-image-amd64 \
        live-boot \
        live-boot-initramfs-tools \
        systemd-sysv \
        sudo \
        curl \
        ca-certificates
"

# Create default live user 'vagrant' (matching VM credentials for consistency)
chroot "$ROOTFS" /bin/bash -c "
    useradd -m -s /bin/bash -G sudo,audio,video vagrant
    echo 'vagrant:vagrant' | chpasswd
    echo 'vagrant ALL=(ALL) NOPASSWD:ALL' > /etc/sudoers.d/vagrant
    chmod 0440 /etc/sudoers.d/vagrant
"

echo "=== [4/6] Provisioning UselessOS Shell & Applications ==="
# Copy apps and provisioning scripts into rootfs
mkdir -p "$ROOTFS/vagrant/apps" "$ROOTFS/vagrant/scripts"
cp -r "$REPO_ROOT/apps/"* "$ROOTFS/vagrant/apps/"
cp -r "$REPO_ROOT/scripts/"* "$ROOTFS/vagrant/scripts/"

# Run existing verified provisioning scripts inside chroot
chroot "$ROOTFS" /bin/bash /vagrant/scripts/01-install-core.sh
chroot "$ROOTFS" /bin/bash /vagrant/scripts/02-configure-system.sh
chroot "$ROOTFS" /bin/bash /vagrant/scripts/03-deploy-apps.sh

# Clean package manager cache
chroot "$ROOTFS" /bin/bash -c "
    apt-get clean
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /vagrant
"

# Unmount chroot mounts cleanly before squashfs
umount -lf "$ROOTFS/proc" 2>/dev/null || true
umount -lf "$ROOTFS/sys" 2>/dev/null || true
umount -lf "$ROOTFS/dev/pts" 2>/dev/null || true
umount -lf "$ROOTFS/dev" 2>/dev/null || true

echo "=== [5/6] Generating SquashFS Filesystem & Bootloader ==="
mkdir -p "$CD_DIR/live" "$CD_DIR/isolinux" "$CD_DIR/boot/grub"

# Extract kernel and initramfs to live media
cp "$ROOTFS"/boot/vmlinuz-* "$CD_DIR/live/vmlinuz"
cp "$ROOTFS"/boot/initrd.img-* "$CD_DIR/live/initrd.img"

# Compress rootfs
mksquashfs "$ROOTFS" "$CD_DIR/live/filesystem.squashfs" -comp xz -e boot

# Setup ISOLINUX for Legacy BIOS boot
cp /usr/lib/ISOLINUX/isolinux.bin "$CD_DIR/isolinux/" 2>/dev/null || cp /usr/lib/syslinux/modules/bios/isolinux.bin "$CD_DIR/isolinux/" 2>/dev/null || true
for mod in ldlinux.c32 vesamenu.c32 libcom32.c32 libutil.c32; do
    find /usr/lib/ -name "$mod" -exec cp {} "$CD_DIR/isolinux/" \; 2>/dev/null || true
done

cat > "$CD_DIR/isolinux/isolinux.cfg" <<EOF
UI vesamenu.c32
PROMPT 0
TIMEOUT 50
MENU TITLE UselessOS 3.0 Live Boot Menu

LABEL uselessos
  MENU LABEL UselessOS 3.0 Live (Default)
  KERNEL /live/vmlinuz
  APPEND initrd=/live/initrd.img boot=live components quiet splash

LABEL uselessos-failsafe
  MENU LABEL UselessOS 3.0 Live (Failsafe)
  KERNEL /live/vmlinuz
  APPEND initrd=/live/initrd.img boot=live components noapic noacpi nosplash nomodeset
EOF

# Setup GRUB for UEFI boot
cat > "$CD_DIR/boot/grub/grub.cfg" <<EOF
set default="0"
set timeout=5

menuentry "UselessOS 3.0 Live (UEFI)" {
    linux /live/vmlinuz boot=live components quiet splash
    initrd /live/initrd.img
}

menuentry "UselessOS 3.0 Live (Failsafe)" {
    linux /live/vmlinuz boot=live components noapic noacpi nosplash nomodeset
    initrd /live/initrd.img
}
EOF

# Create EFI FAT image for UEFI boot
mkdir -p "$WORK_DIR/efi_temp/EFI/BOOT"
grub-mkstandalone \
    --format=x86_64-efi \
    --output="$WORK_DIR/efi_temp/EFI/BOOT/BOOTX64.EFI" \
    --locales="" \
    --fonts="" \
    "boot/grub/grub.cfg=$CD_DIR/boot/grub/grub.cfg" 2>/dev/null || true

if [ -f "$WORK_DIR/efi_temp/EFI/BOOT/BOOTX64.EFI" ]; then
    dd if=/dev/zero of="$CD_DIR/boot/grub/efi.img" bs=1M count=10 status=none
    mkfs.vfat "$CD_DIR/boot/grub/efi.img" >/dev/null
    mmd -i "$CD_DIR/boot/grub/efi.img" ::EFI ::EFI/BOOT
    mcopy -i "$CD_DIR/boot/grub/efi.img" "$WORK_DIR/efi_temp/EFI/BOOT/BOOTX64.EFI" ::EFI/BOOT/
fi

echo "=== [6/6] Generating Hybrid Bootable ISO ==="
ISOHDPFX=""
for p in /usr/lib/ISOLINUX/isohdpfx.bin /usr/lib/syslinux/isohdpfx.bin /usr/lib/syslinux/bios/isohdpfx.bin; do
    if [ -f "$p" ]; then
        ISOHDPFX="$p"
        break
    fi
done

XORRISO_ARGS=(
    -as mkisofs
    -iso-level 3
    -full-iso-9660-filenames
    -volid "USELESSOS"
    -eltorito-boot isolinux/isolinux.bin
    -eltorito-catalog isolinux/boot.cat
    -no-emul-boot -boot-load-size 4 -boot-info-table
)

if [ -n "$ISOHDPFX" ]; then
    XORRISO_ARGS+=(-isohybrid-mbr "$ISOHDPFX")
fi

if [ -f "$CD_DIR/boot/grub/efi.img" ]; then
    XORRISO_ARGS+=(
        -eltorito-alt-boot
        -e boot/grub/efi.img
        -no-emul-boot
        -isohybrid-gpt-basdat
    )
fi

xorriso "${XORRISO_ARGS[@]}" -output "$OUTPUT_ISO" "$CD_DIR"

sha256sum "$OUTPUT_ISO" > "$OUTPUT_ISO.sha256"

echo "================================================================="
echo "Build Successful!"
echo "ISO Created: $OUTPUT_ISO"
echo "SHA256: $(cat "$OUTPUT_ISO.sha256")"
echo "================================================================="
