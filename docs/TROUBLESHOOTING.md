# UselessOS Troubleshooting Guide

## 1. VirtualBox & Launcher Guidance

### Dynamic Tool Resolution
`START-UselessOS.bat` and `INSTALL-UselessOS.bat` dynamically check:
1. System `PATH` (`where VBoxManage.exe`).
2. Environment variables `%VBOX_MSI_INSTALL_PATH%` and `%VBOX_INSTALL_PATH%`.
3. Standard 64-bit and 32-bit Program Files directories.

If VirtualBox is still not detected, ensure Oracle VM VirtualBox is installed from [virtualbox.org](https://www.virtualbox.org/) or install it automatically via winget:
```cmd
winget install -e --id Oracle.VirtualBox
```

### VM Machine States & Lock Contention
- **State: `running`**: If `START-UselessOS.bat` detects the VM is already running, it brings the existing window to focus rather than attempting duplicate initialization.
- **State: `paused`**: The launcher sends an automatic `resume` command.
- **State: `locked` / `inaccessible`**: If VirtualBox reports a locked session, open the VirtualBox Manager GUI, right-click `UselessOS`, and select **Close → Power Off**, then run `START-UselessOS.bat` again.

### Host Key & Mouse Capture
- **Mouse Trapped in VM Window:** Press the **Right Ctrl** key on your physical keyboard (the VirtualBox Host Key) to release input back to Windows.
- **Fullscreen Mode:** Press **Right Ctrl + F** to toggle fullscreen mode.

---

## 2. Audio & Graphics Configuration

### Audio Playback
- Audio is configured using the **AC97** controller mapped to PulseAudio. If no sound plays, ensure your host audio device is active in Windows sound settings before booting the VM.

### Display Resolution & Scaling
- The native desktop shell dynamically sizes to the screen. If running on a 4K display, you can adjust the scale factor in the VirtualBox VM window via **View → Virtual Screen 1 → Resize / Scale to 150% or 200%**.

---

## 3. Vagrant Build Pipeline Troubleshooting

### Vagrant Discovery
`build.ps1` automatically queries `Get-Command vagrant` as well as default HashiCorp install directories. If building from source:
1. Ensure Vagrant is installed (`winget install -e --id HashiCorp.Vagrant`).
2. Ensure you have at least 5GB of free disk space on your drive.
3. If Debian package installation times out during `01-install-core.sh`, destroy the incomplete container and rebuild:
   ```powershell
   vagrant destroy -f
   .\build.ps1
   ```
