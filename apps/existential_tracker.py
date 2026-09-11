#!/usr/bin/env python3
import sys
from qt_compat import *
import useless_style

class ExistentialTracker(useless_style.UselessWindow):
    def __init__(self):
        super().__init__(
            title="Existential Crisis Tracker™",
            subtitle="Real-time telemetry of cosmic insignificance",
            icon_name="existential_tracker.png",
            accent_color="#e82803",
            width=460,
            height=460
        )
        layout = self.content_layout

        metrics_card = QGroupBox("Cosmic Telemetry")
        m_layout = QVBoxLayout(metrics_card)
        m_layout.setSpacing(10)
        self.add_metric(m_layout, "Sense of Purpose", 12, "#ea34df")
        self.add_metric(m_layout, "Monday Motivation", 8, "#e82803")
        self.add_metric(m_layout, "Bloodstream Caffeine", 94, "#244638")
        self.add_metric(m_layout, "Residual Optimism", 31, "#ffb800")
        layout.addWidget(metrics_card)
        
        rec_box = QWidget()
        rec_box.setStyleSheet("background: #f5f4f0; border: 2px solid #0e0e0d; border-radius: 12px; padding: 10px;")
        r_layout = QVBoxLayout(rec_box)
        r_layout.setSpacing(4)
        lbl1 = QLabel("SYSTEM RECOMMENDATION:")
        lbl1.setStyleSheet("font-size: 8.5pt; font-weight: 900; color: #244638; border: none; font-family: Helvetica;")
        lbl2 = QLabel("Have some water.")
        lbl2.setStyleSheet("font-size: 16pt; font-weight: 900; color: #0e0e0d; border: none; font-family: Helvetica;")
        lbl2.setAlignment(AlignCenter)
        r_layout.addWidget(lbl1)
        r_layout.addWidget(lbl2)
        layout.addWidget(rec_box)

        self.count = 42
        self.counter_lbl = QLabel(f'"Why am I doing this?" counter: <b><span style="color:#e82803; font-size:16pt;">{self.count}</span></b>')
        self.counter_lbl.setStyleSheet("font-family: Helvetica; font-weight: 700;")
        self.counter_lbl.setAlignment(AlignCenter)
        layout.addWidget(self.counter_lbl)

        btn = QPushButton("🤔 Ask Why Once More")
        btn.clicked.connect(self.ask_why)
        layout.addWidget(btn)

    def add_metric(self, layout, name, val, color):
        h = QHBoxLayout()
        lbl = QLabel(name)
        lbl.setStyleSheet("font-weight: 700; font-family: Helvetica; font-size: 9.5pt;")
        h.addWidget(lbl)
        h.addStretch()
        val_lbl = QLabel(f"{val}%")
        val_lbl.setStyleSheet(f"font-weight: 900; font-family: Helvetica; font-size: 10pt; color: {color};")
        h.addWidget(val_lbl)
        layout.addLayout(h)
        
        bar = QProgressBar()
        bar.setValue(val)
        bar.setTextVisible(False)
        bar.setFixedHeight(12)
        bar.setStyleSheet(f"QProgressBar::chunk {{ background-color: {color}; border-radius: 4px; }}")
        layout.addWidget(bar)

    def ask_why(self):
        self.count += 1
        self.counter_lbl.setText(f'"Why am I doing this?" counter: <b><span style="color:#e82803; font-size:16pt;">{self.count}</span></b>')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    useless_style.apply_corporate_style(app)
    win = ExistentialTracker()
    win.show()
    run_app(app)
