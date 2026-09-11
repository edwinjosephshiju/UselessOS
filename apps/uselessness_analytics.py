#!/usr/bin/env python3
import sys
from qt_compat import *
import useless_style

class UselessnessAnalytics(useless_style.UselessWindow):
    def __init__(self):
        super().__init__(
            title="Uselessness Analytics™",
            subtitle="Week-to-date non-value addition telemetry index",
            icon_name="uselessness_analytics.png",
            accent_color="#ea34df",
            width=580,
            height=500
        )
        layout = self.content_layout

        grid = QGridLayout()
        grid.setSpacing(12)
        self.add_stat(grid, 0, 0, "48h 17m", "Total Screen Staring", "#0e0e0d")
        self.add_stat(grid, 0, 1, "2h 04m", "Marginal Productivity", "#244638")
        self.add_stat(grid, 1, 0, "13h 31m", "Questionable Browsing", "#ffb800")
        self.add_stat(grid, 1, 1, "32h 42m", "Unapologetic Procrastination", "#e82803")
        layout.addLayout(grid)

        score_lbl = QLabel("USELESSNESS SCORE: 94 / 100")
        score_lbl.setStyleSheet("background: #0e0e0d; color: #ea34df; font-family: monospace; font-weight: 900; font-size: 14pt; padding: 10px; border-radius: 12px;")
        score_lbl.setAlignment(AlignCenter)
        layout.addWidget(score_lbl)
        
        ach_card = QGroupBox("🏆 Certified Achievements")
        a_layout = QVBoxLayout(ach_card)
        a_layout.setSpacing(6)
        achievements = [
            "Opened laptop with conviction, immediately opened Reddit",
            "Watched a 40-minute tutorial on a skill never to be practiced",
            "Reorganized desktop wallpapers 6 times",
            "Overthought an email for 3 days before sending 'Sounds good!'"
        ]
        for ach in achievements:
            lbl = QLabel(f"• {ach}")
            lbl.setStyleSheet("font-weight: 600; font-size: 9.5pt; color: #0e0e0d;")
            a_layout.addWidget(lbl)
        layout.addWidget(ach_card)
            
        layout.addStretch()

        btn = QPushButton("🖨️  Print Certified Certificate of Inefficacy")
        btn.clicked.connect(lambda: QMessageBox.critical(self, "Printer Error", "Printer disconnected. Also, out of cyan ink. Please reboot reality."))
        layout.addWidget(btn)

    def add_stat(self, grid, row, col, val, label, color="#ea34df"):
        w = QWidget()
        w.setStyleSheet("background: #f5f4f0; border: 2px solid #0e0e0d; border-radius: 14px; padding: 8px;")
        l = QVBoxLayout(w)
        l.setSpacing(2)
        
        v_lbl = QLabel(val)
        v_lbl.setStyleSheet(f"font-size: 18pt; font-weight: 900; color: {color}; border: none; background: transparent; font-family: Helvetica;")
        v_lbl.setAlignment(AlignCenter)
        
        l_lbl = QLabel(label)
        l_lbl.setStyleSheet("font-size: 8.5pt; font-weight: 800; color: #0e0e0d; text-transform: uppercase; border: none; background: transparent; font-family: Helvetica;")
        l_lbl.setAlignment(AlignCenter)
        
        l.addWidget(v_lbl)
        l.addWidget(l_lbl)
        grid.addWidget(w, row, col)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    useless_style.apply_corporate_style(app)
    win = UselessnessAnalytics()
    win.show()
    run_app(app)
