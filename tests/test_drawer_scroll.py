import sys
import os
import unittest

sys.path.insert(0, "/opt/uselessos")
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "apps"))

from qt_compat import HAS_QT, QApplication
import useless_style

class TestDrawerScroll(unittest.TestCase):
    def test_drawer_scroll(self):
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
        
        shell.toggle_launchpad()
        app.processEvents()
        
        # Scroll down in the App Drawer
        vsb = shell.launchpad.scroll_area.verticalScrollBar()
        vsb.setValue(vsb.maximum() // 2)
        app.processEvents()
        
        save_path = "/vagrant/test_launchpad_scrolled.png"
        if os.path.exists(os.path.dirname(save_path)):
            shell.launchpad.grab().save(save_path)
        shell.close()
        print("[DRAWER SCROLL TEST SUCCESSFUL]")

if __name__ == "__main__":
    unittest.main()
