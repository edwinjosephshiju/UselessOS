#!/usr/bin/env bash
set -euo pipefail

# ==============================================================================
# UselessOS 3.0: VirtualBox OVA Appliance Builder
# Builds release/UselessOS.ova using Vagrant + VirtualBox if present,
# or via QEMU stream-optimized VMDK packaging in headless CI environments.
# ==============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
RELEASE_DIR="$REPO_ROOT/release"
OUTPUT_OVA="$RELEASE_DIR/UselessOS.ova"

mkdir -p "$RELEASE_DIR"

if command -v VBoxManage >/dev/null 2>&1 && command -v vagrant >/dev/null 2>&1; then
    echo "=== Building OVA via Vagrant + VirtualBox ==="
    cd "$REPO_ROOT"
    vagrant up --provision
    vagrant halt
    rm -f "$OUTPUT_OVA"
    VBoxManage export "UselessOS" -o "$OUTPUT_OVA"
else
    echo "=== Building OVA via QEMU & OVF Packager ==="
    
    # Ensure qemu-utils and debootstrap are present
    if [ "$(id -u)" -eq 0 ]; then
        export DEBIAN_FRONTEND=noninteractive
        apt-get update -qq
        apt-get install -y -qq qemu-utils debootstrap parted e2fsprogs dosfstools grub-pc
    fi

    WORK_DIR="$(mktemp -d -t uselessos-ova-XXXXXX)"
    cleanup() {
        echo "=== Cleaning up OVA build workspace ==="
        rm -rf "$WORK_DIR"
    }
    trap cleanup EXIT

    RAW_DISK="$WORK_DIR/disk.raw"
    MOUNT_DIR="$WORK_DIR/mnt"
    mkdir -p "$MOUNT_DIR"

    # Create 8GB sparse disk
    qemu-img create -f raw "$RAW_DISK" 8G

    # Partition disk with MBR
    parted -s "$RAW_DISK" mklabel msdos
    parted -s "$RAW_DISK" mkpart primary ext4 1MiB 100%
    parted -s "$RAW_DISK" set 1 boot on

    # Setup loop device
    LOOP_DEV=$(losetup -Pf --show "$RAW_DISK")
    cleanup_loop() {
        if mountpoint -q "$MOUNT_DIR"; then
            umount -R "$MOUNT_DIR" 2>/dev/null || true
        fi
        losetup -d "$LOOP_DEV" 2>/dev/null || true
        cleanup
    }
    trap cleanup_loop EXIT

    mkfs.ext4 -L "UselessOS" "${LOOP_DEV}p1"
    mount "${LOOP_DEV}p1" "$MOUNT_DIR"

    # Debootstrap minimal system
    debootstrap --variant=minbase --arch=amd64 bookworm "$MOUNT_DIR" http://deb.debian.org/debian/

    mount -t proc none "$MOUNT_DIR/proc"
    mount -t sysfs none "$MOUNT_DIR/sys"
    mount -o bind /dev "$MOUNT_DIR/dev"
    mount -t devpts none "$MOUNT_DIR/dev/pts"

    # Install kernel, grub, and systemd
    chroot "$MOUNT_DIR" /bin/bash -c "
        export DEBIAN_FRONTEND=noninteractive
        apt-get update -qq
        apt-get install -y -qq --no-install-recommends \
            linux-image-amd64 \
            grub-pc \
            systemd-sysv \
            sudo \
            curl \
            ca-certificates
    "

    # Create vagrant user
    chroot "$MOUNT_DIR" /bin/bash -c "
        useradd -m -s /bin/bash -G sudo,audio,video vagrant
        echo 'vagrant:vagrant' | chpasswd
        echo 'vagrant ALL=(ALL) NOPASSWD:ALL' > /etc/sudoers.d/vagrant
        chmod 0440 /etc/sudoers.d/vagrant
    "

    # Install UselessOS apps & shell
    mkdir -p "$MOUNT_DIR/vagrant/apps" "$MOUNT_DIR/vagrant/scripts"
    cp -r "$REPO_ROOT/apps/"* "$MOUNT_DIR/vagrant/apps/"
    cp -r "$REPO_ROOT/scripts/"* "$MOUNT_DIR/vagrant/scripts/"

    chroot "$MOUNT_DIR" /bin/bash /vagrant/scripts/01-install-core.sh
    chroot "$MOUNT_DIR" /bin/bash /vagrant/scripts/02-configure-system.sh
    chroot "$MOUNT_DIR" /bin/bash /vagrant/scripts/03-deploy-apps.sh

    # Setup GRUB bootloader
    grub-install --target=i386-pc --boot-directory="$MOUNT_DIR/boot" "$LOOP_DEV"
    cat > "$MOUNT_DIR/boot/grub/grub.cfg" <<EOF
set default="0"
set timeout=2
menuentry "UselessOS 3.0" {
    search --no-floppy --label --set=root UselessOS
    linux /vmlinuz root=LABEL=UselessOS rw quiet splash
    initrd /initrd.img
}
EOF

    # Clean up chroot
    chroot "$MOUNT_DIR" /bin/bash -c "apt-get clean && rm -rf /var/lib/apt/lists/* /vagrant /tmp/*"

    umount -R "$MOUNT_DIR"
    losetup -d "$LOOP_DEV"

    # Convert to stream-optimized VMDK
    VMDK_DISK="$WORK_DIR/UselessOS-disk001.vmdk"
    echo "=== Converting to Stream-Optimized VMDK ==="
    qemu-img convert -O vmdk -o subformat=streamOptimized "$RAW_DISK" "$VMDK_DISK"

    # Generate OVF Descriptor
    OVF_FILE="$WORK_DIR/UselessOS.ovf"
    cat > "$OVF_FILE" <<'EOF'
<?xml version="1.0"?>
<Envelope ovf:version="1.0" xml:lang="en-US" xmlns="http://schemas.dmtf.org/ovf/envelope/1" xmlns:ovf="http://schemas.dmtf.org/ovf/envelope/1" xmlns:rasd="http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/CIM_ResourceAllocationSettingData" xmlns:vssd="http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/CIM_VirtualSystemSettingData" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:vbox="http://www.virtualbox.org/ovf/machine">
  <References>
    <File ovf:id="file1" ovf:href="UselessOS-disk001.vmdk"/>
  </References>
  <DiskSection>
    <Info>List of the virtual disks used in the package</Info>
    <Disk ovf:capacity="8589934592" ovf:diskId="vmdisk1" ovf:fileRef="file1" ovf:format="http://www.vmware.com/interfaces/specifications/vmdk.html#streamOptimized"/>
  </DiskSection>
  <NetworkSection>
    <Info>Logical networks used in the package</Info>
    <Network ovf:name="NAT">
      <Description>Logical network used by this appliance.</Description>
    </Network>
  </NetworkSection>
  <VirtualSystem ovf:id="UselessOS">
    <Info>A virtual machine</Info>
    <OperatingSystemSection ovf:id="96">
      <Info>The kind of installed guest operating system</Info>
      <Description>Debian_64</Description>
      <vbox:OSType ovf:required="false">Debian_64</vbox:OSType>
    </OperatingSystemSection>
    <VirtualHardwareSection>
      <Info>Virtual hardware requirements for a virtual machine</Info>
      <System>
        <vssd:ElementName>Virtual Hardware Family</vssd:ElementName>
        <vssd:InstanceID>0</vssd:InstanceID>
        <vssd:VirtualSystemIdentifier>UselessOS</vssd:VirtualSystemIdentifier>
        <vssd:VirtualSystemType>virtualbox-2.2</vssd:VirtualSystemType>
      </System>
      <Item>
        <rasd:Caption>2 virtual CPUs</rasd:Caption>
        <rasd:Description>Number of virtual CPUs</rasd:Description>
        <rasd:ElementName>2 virtual CPUs</rasd:ElementName>
        <rasd:InstanceID>1</rasd:InstanceID>
        <rasd:ResourceType>3</rasd:ResourceType>
        <rasd:VirtualQuantity>2</rasd:VirtualQuantity>
      </Item>
      <Item>
        <rasd:AllocationUnits>MegaBytes</rasd:AllocationUnits>
        <rasd:Caption>2048 MB of memory</rasd:Caption>
        <rasd:Description>Memory Size</rasd:Description>
        <rasd:ElementName>2048 MB of memory</rasd:ElementName>
        <rasd:InstanceID>2</rasd:InstanceID>
        <rasd:ResourceType>4</rasd:ResourceType>
        <rasd:VirtualQuantity>2048</rasd:VirtualQuantity>
      </Item>
      <Item>
        <rasd:Address>0</rasd:Address>
        <rasd:Caption>ideController0</rasd:Caption>
        <rasd:Description>IDE Controller</rasd:Description>
        <rasd:ElementName>ideController0</rasd:ElementName>
        <rasd:InstanceID>3</rasd:InstanceID>
        <rasd:ResourceSubType>PIIX4</rasd:ResourceSubType>
        <rasd:ResourceType>5</rasd:ResourceType>
      </Item>
      <Item>
        <rasd:AddressOnParent>0</rasd:AddressOnParent>
        <rasd:Caption>disk1</rasd:Caption>
        <rasd:Description>Disk Image</rasd:Description>
        <rasd:ElementName>disk1</rasd:ElementName>
        <rasd:HostResource>/disk/vmdisk1</rasd:HostResource>
        <rasd:InstanceID>4</rasd:InstanceID>
        <rasd:Parent>3</rasd:Parent>
        <rasd:ResourceType>17</rasd:ResourceType>
      </Item>
    </VirtualHardwareSection>
  </VirtualSystem>
</Envelope>
EOF

    # Generate Manifest with SHA256 checksums
    MF_FILE="$WORK_DIR/UselessOS.mf"
    cd "$WORK_DIR"
    sha256sum "UselessOS.ovf" > "$MF_FILE"
    sha256sum "UselessOS-disk001.vmdk" >> "$MF_FILE"

    # Tar into OVA archive
    echo "=== Packaging into $OUTPUT_OVA ==="
    tar -cf "$OUTPUT_OVA" "UselessOS.ovf" "UselessOS-disk001.vmdk" "UselessOS.mf"
fi

sha256sum "$OUTPUT_OVA" > "$OUTPUT_OVA.sha256"

echo "================================================================="
echo "OVA Build Complete!"
echo "Appliance: $OUTPUT_OVA"
echo "SHA256: $(cat "$OUTPUT_OVA.sha256")"
echo "================================================================="
