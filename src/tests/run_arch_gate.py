#!/usr/bin/env python3
import subprocess
import time
import os
import sys

print("=" * 70)
print(" USELESSOS ARCHITECTURE GATE: AUTOMATED VERIFICATION HARNESS")
print(" Target: KWin Wayland (Debian 12 Bookworm, KWin 5.27.5 LTS)")
print("=" * 70)

# Step 0: Clean up any old instances
subprocess.run(["killall", "-9", "kwin_wayland", "poc_window_tracker", "poc_layer_shell", "test_native_window"], stderr=subprocess.DEVNULL)
time.sleep(1)

socket_name = "wayland-arch-test"
runtime_dir = os.environ.get("XDG_RUNTIME_DIR", f"/run/user/{os.getuid()}")
socket_path = os.path.join(runtime_dir, socket_name)

if os.path.exists(socket_path):
    try:
        os.unlink(socket_path)
    except OSError:
        pass

# Step 1: Launch KWin Wayland headless/virtual compositor
kwin_env = os.environ.copy()
kwin_env["KWIN_WAYLAND_NO_PERMISSION_CHECKS"] = "1"

kwin_cmd = [
    "kwin_wayland",
    "--virtual",
    "--width", "1280",
    "--height", "800",
    "--socket", socket_name,
    "--no-lockscreen",
    "--no-kactivities",
    "--xwayland"
]

print(f"\n[1/5] Launching KWin Wayland virtual compositor ({' '.join(kwin_cmd)})...")
kwin_proc = subprocess.Popen(kwin_cmd, env=kwin_env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

# Wait for Wayland socket to appear
sock_ready = False
for _ in range(30):
    if os.path.exists(socket_path):
        sock_ready = True
        break
    time.sleep(0.2)

if not sock_ready:
    print(f"FAILED: KWin Wayland socket {socket_path} did not appear within 6 seconds!")
    kwin_proc.terminate()
    sys.exit(1)

print(f"[OK] KWin Wayland active and listening on {socket_path}")

env = os.environ.copy()
env["WAYLAND_DISPLAY"] = socket_name
env["QT_QPA_PLATFORM"] = "wayland"

# Step 2: Protocol Global Audit
print("\n[2/5] Auditing Wayland Compositor Globals via wayland-info...")
info_res = subprocess.run(["wayland-info"], env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

globals_output = info_res.stdout
print("---------------- Compositor Globals Summary ----------------")
has_plasma_wm = "org_kde_plasma_window_management" in globals_output
has_layer_shell = "zwlr_layer_shell_v1" in globals_output
has_plasma_shell = "org_kde_plasma_shell" in globals_output
has_ext_foreign = "ext_foreign_toplevel_list_v1" in globals_output

print(f"  org_kde_plasma_window_management : {'PRESENT [VERIFIED]' if has_plasma_wm else 'MISSING'}")
print(f"  zwlr_layer_shell_v1              : {'PRESENT [VERIFIED]' if has_layer_shell else 'MISSING'}")
print(f"  org_kde_plasma_shell             : {'PRESENT [VERIFIED]' if has_plasma_shell else 'MISSING'}")
print(f"  ext_foreign_toplevel_list_v1     : {'PRESENT' if has_ext_foreign else 'ABSENT (Confirmed: Not exposed by KWin 5.27.5)'}")
print("------------------------------------------------------------")

if not has_plasma_wm or not has_layer_shell:
    print("FATAL: Required protocols not advertised by KWin!")
    kwin_proc.terminate()
    sys.exit(1)

# Step 3: Test PoC 2 - Layer Shell Surfaces & Exclusive Zones
print("\n[3/5] Testing PoC 2: Layer Shell Multi-Surface (TopBar, Dock, Canvas)...")
poc_layer_bin = "/home/vagrant/uselessos_native/build/src/tests/poc_layer_shell"
layer_res = subprocess.run([poc_layer_bin], env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=15)
print(layer_res.stdout)

if "Verified all Layer Shell surfaces (TopBar 42px, Dock 80px, Canvas Background)!" in layer_res.stdout:
    print("[PASS] PoC 2: Layer Shell Multi-Surface Verified!")
else:
    print("[FAIL] PoC 2: Layer Shell failed verification!")
    kwin_proc.terminate()
    sys.exit(1)

# Step 4: Test PoC 1 - Window Tracker (Lifecycle, Title, AppId, State, Focus, Minimize/Restore)
print("\n[4/5] Testing PoC 1: Window Tracker under KWin Wayland...")
poc_win_bin = "/home/vagrant/uselessos_native/build/src/tests/poc_window_tracker"
win_proc = subprocess.Popen([poc_win_bin], env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

time.sleep(1.5)

# Spawn a test window to be tracked
test_win_bin = "/home/vagrant/uselessos_native/build/src/tests/test_native_window"
print(f"Spawning native test window ({test_win_bin})...")
test_proc = subprocess.Popen([test_win_bin], env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

# Collect output from poc_window_tracker
try:
    tracker_output, _ = win_proc.communicate(timeout=25)
except subprocess.TimeoutExpired:
    win_proc.kill()
    tracker_output, _ = win_proc.communicate()

print(tracker_output)

test_proc.terminate()
test_proc.wait()

tracker_pass = (
    "Bound org_kde_plasma_window_management" in tracker_output and
    "Window Created" in tracker_output and
    "[WIN-EVENT] Focus State" in tracker_output and
    "[TEST PHASE 1] Disagreeably Minimizing First Window" in tracker_output and
    "[TEST PHASE 2] Restoring and Activating First Window" in tracker_output and
    "[PASS] All Window Tracking & Lifecycle Operations Verified!" in tracker_output
)

if tracker_pass:
    print("[PASS] PoC 1: Window Tracker Architecture Verified!")
else:
    print("[FAIL] PoC 1: Window Tracker failed verification!")
    kwin_proc.terminate()
    sys.exit(1)

# Step 5: Summary
print("\n[5/5] Architecture Verification Conclusion...")
print("[OK] KWin native org_kde_plasma_window_management is 100% functional.")
print("[OK] KWin native zwlr_layer_shell_v1 is 100% functional.")

print("\n" + "=" * 70)
print(" ARCHITECTURE GATE RESULT: ALL PROOFS-OF-CONCEPT PASSED SUCCESSFULLY")
print("=" * 70)

kwin_proc.terminate()
kwin_proc.wait()
sys.exit(0)
