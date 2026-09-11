# UselessOS Wayland Protocols

This directory contains the protocol XML definitions used by the native UselessOS desktop shell:

1. `plasma-window-management.xml`
   - Defines `org_kde_plasma_window_management` and `org_kde_plasma_window`.
   - Used by the Dock (`WindowTracker`) for toplevel window tracking, title/app-id updates, active window detection, minimization/maximization, workspace management, and activation.

2. `plasma-shell.xml`
   - Defines `org_kde_plasma_shell` and `org_kde_plasma_surface`.
   - Used by TopBar and Desktop Canvas for panel and desktop roles under KWin.

3. `wlr-layer-shell-unstable-v1.xml`
   - Defines `zwlr_layer_shell_v1` and `zwlr_layer_surface_v1`.
   - Standard Layer Shell protocol for exclusive zone management across Wayland compositors.
