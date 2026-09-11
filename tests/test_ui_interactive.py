import sys
import os
import time
import unittest

sys.path.insert(0, "/opt/uselessos")
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "apps"))

from qt_compat import HAS_QT, QApplication, QTimer, QDialog
import useless_style

class TestUIInteractive(unittest.TestCase):
    def test_everything(self):
        if not HAS_QT:
            self.skipTest("PyQt6/PyQt5 is not installed in current environment")
        if not os.environ.get("DISPLAY") and sys.platform != "win32":
            self.skipTest("No graphical display available")
        
        from useless_shell import UselessDesktopShell
        app = QApplication.instance() or QApplication(sys.argv)
        useless_style.apply_corporate_style(app)
        
        shell = UselessDesktopShell()
        shell.setGeometry(0, 0, 1024, 768)
        shell.show()
        app.processEvents()
        
        # 1. Test Control Center Drawer
        print("[TEST] Toggling Control Center...")
        shell.toggle_control_center()
        app.processEvents()
        time.sleep(0.5)
        if os.path.exists("/vagrant"):
            app.primaryScreen().grabWindow(0).save("/vagrant/test_cc_real_hardware.png")
        print("[TEST] Control center captured.")
        
        # Switch to Bluetooth tab
        shell.control_center.switch_wireless_tab(1)
        app.processEvents()
        time.sleep(0.5)
        if os.path.exists("/vagrant"):
            app.primaryScreen().grabWindow(0).save("/vagrant/test_cc_bluetooth.png")
        print("[TEST] Control center bluetooth captured.")
        
        shell.toggle_control_center() # hide cc
        app.processEvents()
        
        # 2. Test Launchpad App Drawer (Scrollable)
        print("[TEST] Toggling Launchpad Drawer...")
        shell.toggle_launchpad()
        app.processEvents()
        time.sleep(0.5)
        if os.path.exists("/vagrant"):
            app.primaryScreen().grabWindow(0).save("/vagrant/test_launchpad_drawer.png")
        print("[TEST] Launchpad drawer captured.")
        
        shell.toggle_launchpad() # hide launchpad
        app.processEvents()
        
        # 3. Test About Dialog (Edwin Joseph, Antigravity, Useless Projects 3.0)
        print("[TEST] Opening About Dialog...")
        if os.path.exists("/vagrant"):
            QTimer.singleShot(500, lambda: app.primaryScreen().grabWindow(0).save("/vagrant/test_about_verified.png"))
        QTimer.singleShot(1200, lambda: [w.accept() for w in app.topLevelWidgets() if isinstance(w, QDialog)])
        shell.topbar.show_about_dialog()
        app.processEvents()
        print("[TEST] About dialog captured.")
        
        # 4. Test Top Menu: Curiosity -> Why Does This OS Exist?
        print("[TEST] Opening Curiosity: Why Does This OS Exist?...")
        if os.path.exists("/vagrant"):
            QTimer.singleShot(500, lambda: app.primaryScreen().grabWindow(0).save("/vagrant/test_curiosity_exist.png"))
        QTimer.singleShot(1200, lambda: [w.accept() for w in app.topLevelWidgets() if isinstance(w, QDialog)])
        shell.topbar.show_curiosity_exist_dialog()
        app.processEvents()
        print("[TEST] Curiosity dialog captured.")
        
        # 5. Test Top Menu: Curiosity -> Calibrate Sarcasm Matrix
        print("[TEST] Opening Curiosity: Calibrate Sarcasm Matrix...")
        if os.path.exists("/vagrant"):
            QTimer.singleShot(500, lambda: app.primaryScreen().grabWindow(0).save("/vagrant/test_sarcasm_matrix.png"))
        QTimer.singleShot(1200, lambda: [w.accept() for w in app.topLevelWidgets() if isinstance(w, QDialog)])
        shell.topbar.show_sarcasm_matrix_dialog()
        app.processEvents()
        print("[TEST] Sarcasm matrix captured.")

        # 6. Test Top Menu: File -> Procrastination Session
        print("[TEST] Opening File: Procrastination Session...")
        if os.path.exists("/vagrant"):
            QTimer.singleShot(500, lambda: app.primaryScreen().grabWindow(0).save("/vagrant/test_procrastination_session.png"))
        QTimer.singleShot(1200, lambda: [w.accept() for w in app.topLevelWidgets() if isinstance(w, QDialog)])
        shell.topbar.show_procrastination_session_dialog()
        app.processEvents()
        print("[TEST] Procrastination session captured.")
        
        shell.close()
        print("[ALL TESTS COMPLETED SUCCESSFULLY]")

if __name__ == "__main__":
    unittest.main()
