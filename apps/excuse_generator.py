#!/usr/bin/env python3
import sys
import random
from qt_compat import *
import useless_style
from qwen_backend import QwenEngine, CORPORATE_EXCUSE_PROMPT

class ExcuseGenerator(useless_style.UselessWindow):
    def __init__(self):
        super().__init__(
            title="Excuse Generator™",
            subtitle="Automated Corporate BS Mitigation Matrix",
            icon_name="excuse_generator.png",
            accent_color="#ea34df",
            width=620,
            height=640
        )
        layout = self.content_layout

        # Form Card
        group = QGroupBox("Absence Context && Target")
        form_layout = QVBoxLayout(group)
        form_layout.setContentsMargins(14, 24, 14, 14)
        form_layout.setSpacing(6)
        
        self.category = QComboBox()
        self.category.setFixedHeight(34)
        self.category.addItems([
            "Quantum & Spatiotemporal Anomalies",
            "Unscheduled Pet/Biological Events", 
            "Corporate Infrastructure Glitches",
            "Existential Dread",
            "Household Appliance Rebellion"
        ])
        form_layout.addWidget(QLabel("Excuse Category:"))
        form_layout.addWidget(self.category)

        self.recipient = QComboBox()
        self.recipient.setFixedHeight(34)
        self.recipient.addItems([
            "Direct Line Manager",
            "Human Resources Dept",
            "The Entire Slack Channel",
            "Self-Justification Console"
        ])
        form_layout.addWidget(QLabel("Target Recipient:"))
        form_layout.addWidget(self.recipient)

        self.keyword = QLineEdit()
        self.keyword.setFixedHeight(34)
        self.keyword.setPlaceholderText("e.g. spilled espresso, sentient toaster")
        form_layout.addWidget(QLabel("Key Keyword (Optional):"))
        form_layout.addWidget(self.keyword)
        layout.addWidget(group)

        # Absurdity Calibration
        abs_group = QGroupBox("Absurdity Calibration")
        abs_layout = QHBoxLayout(abs_group)
        self.slider = QSlider(Horizontal)
        self.slider.setMinimum(1)
        self.slider.setMaximum(100)
        self.slider.setValue(42)
        self.slider_lbl = QLabel("42%")
        self.slider_lbl.setStyleSheet("font-weight: 900; color: #ea34df; font-size: 11pt;")
        self.slider.valueChanged.connect(lambda v: self.slider_lbl.setText(f"{v}%"))
        abs_layout.addWidget(self.slider)
        abs_layout.addWidget(self.slider_lbl)
        layout.addWidget(abs_group)

        # Action Buttons Row
        btn_row = QHBoxLayout()
        btn_row.setSpacing(10)
        self.btn = QPushButton("GENERATE STANDARD")
        self.btn.setFixedHeight(40)
        self.btn.setCursor(QCursor(PointingHandCursor))
        self.btn.setStyleSheet("""
            QPushButton {
                background-color: #f5f4f0;
                color: #0e0e0d;
                font-weight: 800;
                border: 2px solid #0e0e0d;
                border-radius: 12px;
                padding: 8px 14px;
            }
            QPushButton:hover {
                background-color: #ea34df;
                color: #ffffff;
            }
        """)
        self.btn.clicked.connect(self.generate)
        btn_row.addWidget(self.btn)

        self.ai_btn = QPushButton("✨ AI SYNTHESIS (Qwen 3.5 0.8B)")
        self.ai_btn.setFixedHeight(40)
        self.ai_btn.setCursor(QCursor(PointingHandCursor))
        self.ai_btn.setStyleSheet("""
            QPushButton {
                background-color: #0e0e0d;
                color: #00c2cb;
                font-weight: 900;
                border: 2px solid #0e0e0d;
                border-radius: 12px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #00c2cb;
                color: #0e0e0d;
            }
        """)
        self.ai_btn.clicked.connect(self.generate_ai)
        btn_row.addWidget(self.ai_btn)
        layout.addLayout(btn_row)

        # Output Card
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.output.setFixedHeight(120)
        self.output.setPlaceholderText("Your certified incontrovertible excuse will materialize here...")
        layout.addWidget(self.output)

        self.active_stream = None

    def generate(self):
        cat = self.category.currentText()
        rec = self.recipient.currentText()
        kw = self.keyword.text().strip() or "the fundamental laws of physics"
        absurdity = self.slider.value()

        templates = [
            f"Dear {rec},\n\nPlease be advised that due to an unexpected {cat.lower()} directly involving {kw}, my physical presence is currently suspended in accordance with ISO-9001 compliance standards. Estimated latency: indefinite.",
            f"MEMORANDUM TO: {rec}\nSUBJECT: Absence Event 404\n\nRegrettably, an escalation in {kw} has triggered an emergency audit by {cat}. I cannot attend scheduled obligations without causing catastrophic organizational resonance.",
            f"Hi {rec},\n\nI was fully prepared to report for duty; however, {kw} collapsed into a localized anomaly under {cat}. Risk assessment indicates 99.4% probability of unproductive sighing if I proceed."
        ]

        excuse = random.choice(templates)
        if absurdity > 70:
            excuse += "\n\nPS: If anyone asks, I was already granted verbal immunity by the Department of Ambiguous Delays."

        self.output.setText(excuse)

    def generate_ai(self):
        cat = self.category.currentText()
        rec = self.recipient.currentText()
        kw = self.keyword.text().strip() or "quantum spatiotemporal lag"
        absurdity = self.slider.value()

        prompt = f"Write a corporate excuse memorandum to '{rec}' regarding an absence caused by '{cat}' specifically involving '{kw}'. Absurdity level: {absurdity}%."
        
        self.output.setText("[QWEN 3.5 (0.8B) NEURAL ENGINE SYNTHESIZING EXCUSE...]")
        self.ai_btn.setEnabled(False)
        self._ai_buffer = ""

        self.active_stream = QwenEngine.create_stream(
            user_prompt=prompt,
            system_prompt=CORPORATE_EXCUSE_PROMPT,
            parent=self,
            temperature=0.8
        )
        self.active_stream.token_emitted.connect(self._on_ai_token)
        self.active_stream.finished_inference.connect(self._on_ai_finished)
        self.active_stream.start()

    def _on_ai_token(self, token):
        self._ai_buffer += token
        self.output.setText(self._ai_buffer)

    def _on_ai_finished(self, thought, answer):
        self.ai_btn.setEnabled(True)
        self.output.setText(f"{answer}\n\n[Verified by Qwen 3.5 0.8B Cognitive Engine]")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    useless_style.apply_corporate_style(app)
    win = ExcuseGenerator()
    win.show()
    run_app(app)
