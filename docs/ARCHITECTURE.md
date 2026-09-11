# UselessOS Technical Architecture

## 1. System Overview

UselessOS is an appliance operating system engineered specifically for the TinkerHub Useless Projects 3.0 competition. Unlike typical web-wrapped wrappers or electronic toy demos, UselessOS is a complete, self-contained Linux desktop appliance built directly on native GUI controls, Linux X11 display architecture, and bespoke window management.

```
┌────────────────────────────────────────────────────────────────────────┐
│                        UselessOS Appliance                             │
├────────────────────────────────────────────────────────────────────────┤
│  Top Bar (macOS Layout)  │  Status Indicators  │  Control Center Pull  │
├──────────────────────────┴─────────────────────┴───────────────────────┤
│                                                                        │
│   Desktop Canvas (Pure #ffffff / Cream #f5f4f0, Ink #0e0e0d)           │
│   ├── Floating Frameless Windows (Y >= 40px Top Bar Collision Ceiling) │
│   │   └── Custom Traffic Lights (🔴 🟡 🟢), Help Modal [?], Brutal UI │
│   ├── Launchpad Drawer (Full-Height Scrollable App Grid)               │
│   └── Sarcastic Mascot & Philosophical Easter Eggs                     │
│                                                                        │
├────────────────────────────────────────────────────────────────────────┤
│      Brutalist Dock App Switcher (Live Process Indicators ●)           │
├────────────────────────────────────────────────────────────────────────┤
│           Native PyQt6 Runtime & Theme Engine (useless_style)          │
├────────────────────────────────────────────────────────────────────────┤
│            Picom Compositor (ARGB Translucency & Soft Shadows)         │
├────────────────────────────────────────────────────────────────────────┤
│            Openbox Window Manager (rc.xml Application Layering)        │
├────────────────────────────────────────────────────────────────────────┤
│            X11 Display Server (xserver-xorg, LightDM Auto-login)       │
├────────────────────────────────────────────────────────────────────────┤
│            Debian 12 (Bookworm 64-bit Linux Kernel 6.1)                │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Base Operating System & Display Pipeline

- **Distribution Base:** Debian 12 (*Bookworm*), 64-bit minimal installation.
- **Display Server:** X.Org X Server (`xserver-xorg`).
- **Display Manager:** LightDM with passwordless auto-login configured for the `vagrant` user via `/etc/lightdm/lightdm.conf.d/50-autologin.conf`.
- **Window Manager:** Openbox. Custom rules in `/home/vagrant/.config/openbox/rc.xml` ensure the underlying desktop shell sits at the proper window layer.
- **Compositor:** `picom` running with the `xrender` backend, providing border anti-aliasing and true ARGB window translucency without GPU overhead.
- **Session Autostart:** Managed by `/home/vagrant/.config/openbox/autostart`:
  1. Sets canvas color with `xsetroot -solid "#ffffff"`.
  2. Disables screen blanking and DPMS (`xset s off`, `xset -dpms`).
  3. Initializes VirtualBox Guest Additions (`VBoxClient --vmsvga`, `VBoxClient --clipboard`).
  4. Launches `picom -b`.
  5. Executes `python3 /opt/uselessos/useless_shell.py &`.

---

## 3. Desktop Shell Architecture (`apps/useless_shell.py`)

The desktop shell is implemented as a single, highly integrated PyQt6 application orchestrating the entire workspace:

### A. Top Bar (`TopBarFrame`)
- 40px fixed-height header spanning the screen with continuous `2px solid #0e0e0d` lower border.
- Left side: Apple-style TinkerHub mascot menu providing system-level actions (About UselessOS, Settings, Sleep, Restart, Shutdown) and whimsical curiosity dialogs (*Why Does This OS Exist?*, *Calibrate Sarcasm Matrix*).
- Center: Dynamic active application title and spatiotemporal metrics.
- Right side: Live digital clock and the **Control Center Trigger Button**.

### B. Control Center Drawer (`ControlCenterDrawer`)
- Slide-out brutalist drawer querying live hardware devices via subprocess calls:
  - **Wi-Fi:** Queries `nmcli device wifi list` and `nmcli connection show --active` with simulated fallback when running in virtual environments without wireless NICs.
  - **Bluetooth:** Queries `rfkill` and `bluetoothctl devices`.
  - **Audio Volume:** Interacts directly with PulseAudio / ALSA `amixer`.
  - **Screen Brightness:** Adjusts display brightness via `xrandr`.

### C. Launchpad Drawer (`LaunchpadDrawer`)
- Full-screen slide-down app drawer displaying all 10 registered UselessOS applications in a clean grid.
- Wrapped in a custom `QScrollArea` with tailored brutalist scrollbars, guaranteeing zero clipping on any display resolution.

### D. Dock App Switcher (`DockBar`)
- Bottom-centered brutalist pill container hosting application launch icons.
- Tracks running child processes. Displays active status indicators (`●`) under open apps.
- Interacts with `wmctrl` and `xdotool` to focus, raise, or minimize running windows when clicked.

---

## 4. Application Framework & Styling (`apps/useless_style.py`)

Every child application inherits from `UselessWindow`, ensuring 100% design consistency:
- **Frameless Windowing:** Completely bypasses default OS window chrome. Provides custom drag handles with a strict `y >= 40` collision boundary to prevent windows from covering the top bar.
- **Traffic-Light Titlebar:** macOS-inspired brutalist controls:
  - 🔴 Red: Close window.
  - 🟡 Yellow: Minimize to dock.
  - 🟢 Green: Maximize / Restore geometry.
  - ❓ Help: Displays the in-app guidance modal (`APP_GUIDES`), detailing usage instructions and philosophical satirical rationale.
- **Theming & Typography:** Injects custom typography (Nanum, Outfit, monospace) and standardized QSS color tokens across all Qt widgets.

---

## 5. Embedded Cognitive Engine & Model Loading Pipeline (`apps/qwen_backend.py`)

UselessOS features a native **Qwen 3.5 0.8B** neural cognitive backend providing inference for chat-like applications (`Hmm AI`, `Useless Terminal`, and `Excuse Generator`):
- **Model Quantization & Loading:**
  - Standard weight artifact: `unsloth/Qwen3.5-0.8B-GGUF` (`Qwen3.5-0.8B-Q4_K_M.gguf`, ~507 MB).
  - Multi-tier inference discovery:
    1. **Tier 1 (Local `llama-server`):** Direct HTTP SSE streaming from `http://127.0.0.1:8080/v1/chat/completions`.
    2. **Tier 2 (Python `llama-cpp-python`):** In-process streaming via native bindings when installed.
    3. **Tier 3 (Subprocess `llama-cli`):** Piped CLI execution using `/opt/uselessos/models/*.gguf`.
    4. **Tier 4 (Self-Contained Fallback Engine):** Offline-first semantic reasoning engine conditioned on system prompt persona, ensuring 100% demo uptime prior to weight downloads.
- **Dynamic System Prompt Steering:**
  - Prompts are formatted using official Qwen ChatML specification (`<|im_start|>system\n{system_prompt}<|im_end|>\n<|im_start|>user\n{user_prompt}<|im_end|>\n<|im_start|>assistant\n`).
  - Reasoning trace extraction: Automatically captures `<think>...</think>` tags to render distinct thought processes before generating answers.
  - Persona presets: Includes *Profound Hesitation (Hmm...)*, *Corporate Bureaucrat*, *Overthinking Paranoia*, *Sarcastic OS Mascot*, and live in-app custom system prompt editing.
- **Provisioning Automation:**
  - `apps/download_model.py` and `scripts/04-setup-qwen.sh` automate downloading weights to `/opt/uselessos/models/`.
---

## 6. Build & Packaging Pipeline

1. **Vagrant Base:** Provisions a clean Debian 12 image using `Vagrantfile`.
2. **Provisioners (`scripts/`):**
   - `01-install-core.sh`: Installs X11, Openbox, LightDM, PyQt6, QtSvg, audio utilities, fonts, and window manipulation tools.
   - `02-configure-system.sh`: Configures autologin, X11 permissions, and desktop autostart.
   - `03-deploy-apps.sh`: Deploys source code to `/opt/uselessos/` and registers system fonts.
3. **Appliance Export (`build.ps1`):** Shuts down the VM and exports `release/UselessOS.ova` via `VBoxManage export`.
4. **Host Launchers (`START-UselessOS.bat` / `INSTALL-UselessOS.bat`):** Dynamically detects VirtualBox, checks machine state, imports the OVA if required, and boots the VM with clear user shortcuts.
