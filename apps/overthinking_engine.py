#!/usr/bin/env python3
import sys
import random
from qt_compat import *
import useless_style

class OverthinkingEngine(useless_style.UselessWindow):
    def __init__(self):
        super().__init__(
            title="Overthinking Engine™",
            subtitle="Simulate runaway catastrophic thoughts in milliseconds",
            icon_name="overthinking_engine.png",
            accent_color="#ffb800",
            width=540,
            height=360
        )
        layout = self.content_layout

        card = QGroupBox("Decision Parameters")
        c_layout = QVBoxLayout(card)
        c_layout.setSpacing(10)

        lbl = QLabel("Enter a simple decision you need to make:")
        lbl.setStyleSheet("font-weight: 700; color: #0e0e0d;")
        c_layout.addWidget(lbl)

        self.input = QLineEdit()
        self.input.setPlaceholderText("e.g. Should I reply 'ok' or 'sounds good'?")
        c_layout.addWidget(self.input)
        layout.addWidget(card)

        self.btn = QPushButton("🔮 ANALYZE ALL 14,000,605 SCENARIOS")
        self.btn.clicked.connect(self.analyze)
        layout.addWidget(self.btn)

        self.status = QLabel("Awaiting input...")
        self.status.setAlignment(AlignCenter)
        self.status.setStyleSheet("font-weight: 800; font-family: Helvetica; color: #e82803;")
        layout.addWidget(self.status)

        self.progress = QProgressBar()
        self.progress.setValue(0)
        self.progress.setTextVisible(False)
        layout.addWidget(self.progress)

        self.timer = QTimer()
        self.timer.timeout.connect(self.step)
        self.progress_val = 0
        
        self.steps = [
            "Analyzing parallel universes...",
            "Simulating potential embarrassment...",
            "Calculating long-term existential dread...",
            "Checking planetary alignments...",
            "Synthesizing social anxiety vectors..."
        ]

    def analyze(self):
        if not self.input.text().strip():
            QMessageBox.warning(self, "Error", "You must provide a decision to overthink.")
            return
            
        self.btn.setEnabled(False)
        self.progress_val = 0
        self.progress.setValue(0)
        self.timer.start(300)

    def step(self):
        self.progress_val += random.randint(5, 15)
        if self.progress_val > 100:
            self.progress_val = 100
            
        self.progress.setValue(self.progress_val)
        
        idx = min(self.progress_val // 20, len(self.steps) - 1)
        self.status.setText(self.steps[idx])
        
        if self.progress_val >= 100:
            self.timer.stop()
            self.btn.setEnabled(True)
            self.show_result()

    def show_result(self):
        results = [
            "CONCLUSION: Do absolutely nothing.",
            "CONCLUSION: You have already ruined it. Apologize profusely.",
            "CONCLUSION: Delete your account and move to the mountains.",
            "CONCLUSION: It doesn't matter, the sun will explode in 5 billion years.",
            "CONCLUSION: Just say 'hmm'."
        ]
        res = random.choice(results)
        QMessageBox.information(self, "Analysis Complete", res)
        self.status.setText("Analysis complete. Anxiety increased.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    useless_style.apply_corporate_style(app)
    win = OverthinkingEngine()
    win.show()
    run_app(app)
