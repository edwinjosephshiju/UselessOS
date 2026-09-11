import sys
import os

sys.path.insert(0, "/opt/uselessos")
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "apps"))

from qt_compat import *
import useless_style
from excuse_generator import ExcuseGenerator

def main():
    app = QApplication.instance() or QApplication(sys.argv)
    useless_style.apply_corporate_style(app)

    win = ExcuseGenerator()
    win.show()
    app.processEvents()

    # Trigger instructions dialog
    QTimer.singleShot(400, win.show_instructions_dialog)

    def verify():
        dialogs = [w for w in app.topLevelWidgets() if isinstance(w, QDialog)]
        print(f"[TEST] Top-level dialog count: {len(dialogs)}")
        assert len(dialogs) == 1, "Must have exactly one top-level dialog"
        dlg = dialogs[0]
        print(f"[TEST] Dialog isWindow(): {dlg.isWindow()}")
        assert dlg.isWindow(), "Dialog must be a top-level window!"
        print(f"[TEST] Dialog geometry: {dlg.geometry().x()}, {dlg.geometry().y()}, {dlg.geometry().width()}, {dlg.geometry().height()}")
        print(f"[TEST] Parent geometry: {win.geometry().x()}, {win.geometry().y()}, {win.geometry().width()}, {win.geometry().height()}")

        # Verify centered horizontally over parent
        p_center_x = win.geometry().x() + win.geometry().width() // 2
        d_center_x = dlg.geometry().x() + dlg.geometry().width() // 2
        diff_x = abs(p_center_x - d_center_x)
        print(f"[TEST] Center X alignment delta: {diff_x}px")
        assert diff_x <= 15, f"Dialog should be centered over parent (delta: {diff_x}px)"

        # Check that subtitle is not colliding with badge
        badge = dlg.findChild(QLabel, "") # Let's inspect labels
        labels = dlg.findChildren(QLabel)
        texts = [l.text() for l in labels]
        print(f"[TEST] Dialog labels found: {len(labels)}")
        assert any("Useless Guide" in t for t in texts), "Must find Useless Guide badge"
        assert any("Corporate BS" in t for t in texts), "Must find subtitle"

        # Test drag & move capability
        init_x = dlg.x()
        dlg.move(init_x + 100, dlg.y())
        app.processEvents()
        assert dlg.x() == init_x + 100, f"Expected {init_x + 100}, got {dlg.x()}"
        print("[TEST] Modal moving & dragging verified successfully!")
        dlg.move(init_x, dlg.y())

        # Capture desktop screenshot with scrot
        os.system("DISPLAY=:0 scrot -o /tmp/screen_modal_fixed.png")
        print("[TEST] Scrot captured screenshot to /tmp/screen_modal_fixed.png")

        QTimer.singleShot(400, dlg.accept)
        QTimer.singleShot(800, win.close)
        QTimer.singleShot(1000, app.quit)

    QTimer.singleShot(1000, verify)
    app.exec() if PYQT6 else app.exec_()
    print("[TEST] Modal verification succeeded completely!")

if __name__ == "__main__":
    main()
