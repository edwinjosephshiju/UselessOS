#!/usr/bin/env python3
import sys
from qt_compat import *
import useless_style

class ScreenTime(useless_style.UselessWindow):
    def __init__(self):
        super().__init__(
            title="Screen Time Calculator™",
            subtitle="Empirically proving nothing was accomplished",
            icon_name="screen_time.png",
            accent_color="#c0326b",
            width=480,
            height=440
        )
        layout = self.content_layout

        card = QGroupBox("Activity Breakdown")
        c_layout = QVBoxLayout(card)
        c_layout.setSpacing(8)

        data = [
            ("Doomscrolling:", "4h 21m", "#ea34df"),
            ("YouTube Rabbit Holes:", "3h 47m", "#e82803"),
            ("Configuring Themes:", "1h 14m", "#ffb800"),
            ("Actual Work:", "4m 12s", "#244638")
        ]
        
        for name, val, color in data:
            h = QHBoxLayout()
            lbl_name = QLabel(name)
            lbl_name.setStyleSheet("font-weight: 700; font-family: Helvetica; font-size: 10pt;")
            lbl_val = QLabel(val)
            lbl_val.setStyleSheet(f"font-weight: 900; font-family: Helvetica; font-size: 10.5pt; color: {color};")
            h.addWidget(lbl_name)
            h.addStretch()
            h.addWidget(lbl_val)
            c_layout.addLayout(h)
        layout.addWidget(card)
            
        summary = QWidget()
        summary.setStyleSheet("background: #f5f4f0; border: 2px solid #0e0e0d; border-radius: 14px; padding: 12px;")
        s_layout = QVBoxLayout(summary)
        s_layout.setSpacing(4)
        
        s1 = QLabel("You have dedicated:")
        s1.setStyleSheet("font-weight: 700; font-size: 9.5pt; color: #716f64;")
        s1.setAlignment(AlignCenter)
        s_layout.addWidget(s1)
        
        s2 = QLabel("18% of your conscious life")
        s2.setStyleSheet("font-size: 16pt; color: #e82803; font-weight: 900; font-family: Helvetica;")
        s2.setAlignment(AlignCenter)
        s_layout.addWidget(s2)
        
        s3 = QLabel("staring intensely at glowing glass rectangles.")
        s3.setStyleSheet("font-weight: 800; font-size: 10pt; color: #0e0e0d;")
        s3.setAlignment(AlignCenter)
        s_layout.addWidget(s3)
        
        s4 = QLabel("Equivalent to watching 137 episodes of a documentary you do not care about.")
        s4.setStyleSheet("font-size: 8.5pt; color: #716f64; font-style: italic;")
        s4.setAlignment(AlignCenter)
        s_layout.addWidget(s4)
        
        layout.addWidget(summary)
        
        btn = QPushButton("🤦 Acknowledge Reality & Suffer")
        btn.clicked.connect(lambda: QMessageBox.information(self, "Acknowledged", "Congratulations. Sufferance recorded in telemetry."))
        layout.addWidget(btn)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    useless_style.apply_corporate_style(app)
    win = ScreenTime()
    win.show()
    run_app(app)
