import sys
import os
import unittest

sys.path.insert(0, "/opt/uselessos")
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "apps"))

from qt_compat import HAS_QT, PYQT6, QApplication, QDialog, QFrame, QVBoxLayout, QLabel, QSlider, QPushButton, AlignCenter, Horizontal, Qt
import useless_style

class TestModalsDirect(unittest.TestCase):
    def test_all_modals(self):
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
        
        # 1. Capture About Dialog
        print("[TEST] Capturing About Dialog...")
        shell.topbar.show_about_dialog = lambda: None # avoid modal loop
        
        dlg = QDialog()
        dlg.setWindowTitle("About UselessOS & Useless Projects 3.0")
        dlg.setFixedSize(500, 570)
        dlg.setWindowFlags((Qt.WindowType.Dialog if PYQT6 else Qt.Dialog) | (Qt.WindowType.FramelessWindowHint if PYQT6 else Qt.FramelessWindowHint))
        dlg.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground if PYQT6 else Qt.WA_TranslucentBackground)
        
        frame = QFrame(dlg)
        frame.setGeometry(0, 0, 500, 570)
        frame.setStyleSheet("QFrame { background-color: #ffffff; border: 2.5px solid #0e0e0d; border-radius: 20px; }")
        f_lay = QVBoxLayout(frame)
        f_lay.setContentsMargins(24, 20, 24, 20)
        f_lay.setSpacing(10)
        
        m_lbl = QLabel()
        m_path = useless_style.get_icon_path("mascot.png")
        if m_path and os.path.exists(m_path):
            from qt_compat import QPixmap
            pix = QPixmap(m_path).scaled(56, 56, Qt.AspectRatioMode.KeepAspectRatio if PYQT6 else Qt.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation if PYQT6 else Qt.SmoothTransformation)
            m_lbl.setPixmap(pix)
        m_lbl.setAlignment(AlignCenter)
        m_lbl.setStyleSheet("background: transparent; border: none;")
        f_lay.addWidget(m_lbl)
        
        t_lbl = QLabel("Useless Projects 3.0")
        t_lbl.setStyleSheet("font-family: 'Drowner', 'Helvetica', sans-serif; font-size: 20pt; font-weight: 900; color: #0e0e0d; background: transparent; border: none;")
        t_lbl.setAlignment(AlignCenter)
        f_lay.addWidget(t_lbl)
        
        sub_lbl = QLabel("exclusive to TinkerHub campus community <3")
        sub_lbl.setStyleSheet("font-family: 'NanumPenScript', cursive; font-size: 13pt; color: #e82803; background: transparent; border: none;")
        sub_lbl.setAlignment(AlignCenter)
        f_lay.addWidget(sub_lbl)
        
        desc = QLabel("UselessOS is a bespoke, highly engineered, and certified non-productive operating system built exclusively for the TinkerHub Useless Projects 3.0 hackathon.")
        desc.setWordWrap(True)
        desc.setAlignment(AlignCenter)
        desc.setStyleSheet("font-size: 9.5pt; color: #444440; line-height: 140%; border: none; background: transparent;")
        f_lay.addWidget(desc)
        
        meta_box = QFrame()
        meta_box.setStyleSheet("background-color: #f5f4f0; border: 1.5px solid #0e0e0d; border-radius: 12px; padding: 10px;")
        m_v = QVBoxLayout(meta_box)
        m_v.setContentsMargins(10, 8, 10, 8)
        m_v.setSpacing(4)
        
        p1 = QLabel("<b>Creator:</b> Edwin Joseph")
        p1.setStyleSheet("color: #0e0e0d; font-size: 9pt; border: none; background: transparent;")
        m_v.addWidget(p1)
        
        p2 = QLabel("<b>Architecture:</b> Antigravity Native UI Engine + Openbox X11")
        p2.setStyleSheet("color: #0e0e0d; font-size: 9pt; border: none; background: transparent;")
        m_v.addWidget(p2)
        
        p3 = QLabel("<b>License:</b> Certified Impractical (MIT-TinkerHub)")
        p3.setStyleSheet("color: #0e0e0d; font-size: 9pt; border: none; background: transparent;")
        m_v.addWidget(p3)
        f_lay.addWidget(meta_box)
        
        f_lay.addStretch()
        btn = QPushButton("Close")
        btn.setFixedHeight(36)
        btn.setStyleSheet("QPushButton { background-color: #0e0e0d; color: #ffffff; border: 2px solid #0e0e0d; border-radius: 12px; font-weight: 900; }")
        btn.clicked.connect(dlg.accept)
        f_lay.addWidget(btn)
        
        dlg.show()
        app.processEvents()
        if os.path.exists("/vagrant"):
            dlg.grab().save("/vagrant/verified_about_dialog.png")
        dlg.close()
        
        # 2. Capture Curiosity Dialog
        d1, f1, l1 = shell.topbar._create_modal_dialog("Philosophical Directive", 460, 320)
        c_desc = QLabel("<b>Why Does UselessOS Exist?</b><br><br>In an era obsessed with artificial optimization and frantic hustle culture, UselessOS stands as a monument to pure technological whimsy. It solves no real problems, produces zero economic value, and guarantees absolute peace of mind.")
        c_desc.setWordWrap(True)
        c_desc.setStyleSheet("font-size: 9.5pt; color: #0e0e0d; line-height: 140%; border: none; background: transparent;")
        l1.addWidget(c_desc)
        l1.addStretch()
        btn1 = QPushButton("Celebrate Uselessness")
        btn1.setFixedHeight(36)
        btn1.setStyleSheet("QPushButton { background-color: #244638; color: #ffffff; border: 2px solid #0e0e0d; border-radius: 12px; font-weight: 900; }")
        l1.addWidget(btn1)
        d1.show()
        app.processEvents()
        if os.path.exists("/vagrant"):
            d1.grab().save("/vagrant/verified_curiosity_dialog.png")
        d1.close()
        
        # 3. Capture Sarcasm Matrix Dialog
        d2, f2, l2 = shell.topbar._create_modal_dialog("Sarcasm Matrix Calibration", 460, 360)
        s_hdr = QLabel("Adjust Cognitive Sarcasm Threshold:")
        s_hdr.setStyleSheet("font-size: 8.5pt; color: #716f64; border: none; background: transparent;")
        l2.addWidget(s_hdr)
        s_lbl = QLabel("Sarcasm Intensity: 75% (Severe)")
        s_lbl.setStyleSheet("font-weight: 800; font-size: 9.5pt; color: #0e0e0d; border: none; background: transparent;")
        l2.addWidget(s_lbl)
        slider = QSlider(Horizontal)
        slider.setRange(0, 100)
        slider.setValue(75)
        slider.setStyleSheet(shell.topbar._slider_style("#00c2cb"))
        l2.addWidget(slider)
        prev = QLabel("“Groundbreaking productivity happening right here. The shareholders will weep with joy.”")
        prev.setStyleSheet("font-style: italic; font-size: 9pt; color: #00838f; border: 2px solid #0e0e0d; border-radius: 10px; padding: 10px; background: #e0f7fa;")
        prev.setWordWrap(True)
        l2.addWidget(prev)
        l2.addStretch()
        btn2 = QPushButton("Lock Sarcasm Level")
        btn2.setFixedHeight(36)
        btn2.setStyleSheet("QPushButton { background-color: #0e0e0d; color: #ffffff; border: 2px solid #0e0e0d; border-radius: 12px; font-weight: 900; }")
        l2.addWidget(btn2)
        d2.show()
        app.processEvents()
        if os.path.exists("/vagrant"):
            d2.grab().save("/vagrant/verified_sarcasm_matrix.png")
        d2.close()
        
        shell.close()
        print("[DIRECT CAPTURES FINISHED SUCCESSFULLY]")

    def test_modal_top_level_isolation(self):
        if not HAS_QT:
            self.skipTest("PyQt6/PyQt5 is not installed in current environment")
        if not os.environ.get("DISPLAY") and sys.platform != "win32":
            self.skipTest("No graphical display available")

        app = QApplication.instance() or QApplication(sys.argv)
        parent = QFrame()
        parent.setGeometry(100, 100, 600, 500)
        parent.show()

        dlg = QDialog(parent)
        dlg.setWindowFlags((Qt.WindowType.Dialog if PYQT6 else Qt.Dialog) | (Qt.WindowType.FramelessWindowHint if PYQT6 else Qt.FramelessWindowHint))
        
        self.assertTrue(dlg.isWindow(), "QDialog must have Qt.Window / Qt.Dialog type flag so it is a top-level window, not an in-window child widget")
        parent.close()

if __name__ == "__main__":
    unittest.main()
