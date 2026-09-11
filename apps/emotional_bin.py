#!/usr/bin/env python3
import sys
import random
from qt_compat import *
import useless_style

class EmotionalBin(useless_style.UselessWindow):
    def __init__(self):
        super().__init__(
            title="Emotional Support Bin™",
            subtitle="Recycle unexpressed thoughts into the void",
            icon_name="emotional_bin.png",
            accent_color="#244638",
            width=380,
            height=380
        )
        self.setAcceptDrops(True)
        layout = self.content_layout
        
        self.dialog = QLabel("Drop mental baggage here, or just click me. I don't care.")
        self.dialog.setStyleSheet("""
            QLabel {
                background: #f5f4f0;
                border: 2px solid #0e0e0d;
                padding: 16px;
                border-radius: 14px;
                font-weight: 800;
                font-family: Helvetica;
                font-size: 10.5pt;
                color: #0e0e0d;
            }
        """)
        self.dialog.setAlignment(AlignCenter)
        self.dialog.setWordWrap(True)
        layout.addWidget(self.dialog)
        
        self.bin_btn = QPushButton("🗑️")
        self.bin_btn.setCursor(QCursor(PointingHandCursor))
        self.bin_btn.setStyleSheet("""
            QPushButton {
                font-size: 64px;
                border: 2px solid #0e0e0d;
                border-radius: 30px;
                background-color: #ffffff;
                padding: 16px;
            }
            QPushButton:hover {
                background-color: #244638;
            }
        """)
        self.bin_btn.clicked.connect(self.interact)
        layout.addWidget(self.bin_btn)

        self.responses = [
            "Finally. Something productive.",
            "We need to talk.",
            "Understandable.",
            "Again?",
            "I'm not angry. I'm disappointed.",
            "Did you really need to do that?",
            "I will remember this.",
            "Sigh.",
            "Baggage successfully incinerated."
        ]

    def interact(self):
        res = random.choice(self.responses)
        self.dialog.setText(res)

    def dragEnterEvent(self, e):
        e.accept()

    def dropEvent(self, e):
        self.interact()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    useless_style.apply_corporate_style(app)
    win = EmotionalBin()
    win.show()
    run_app(app)
