#!/usr/bin/env python3
import sys
from qt_compat import *
import useless_style
from qwen_backend import QwenEngine

TERMINAL_AI_PROMPT = """You are the embedded terminal AI for UselessOS 3.0.
Your persona is a deadpan, sarcastic CLI daemon.
Respond to the user's terminal query in 1 to 3 sentences maximum.
Celebrate procrastination, existential ambiguity, and the deliberate futility of running commands."""

class UselessTerminal(useless_style.UselessWindow):
    def __init__(self):
        super().__init__(
            title="Useless Terminal™",
            subtitle="Certified non-productive shell environment",
            icon_name="useless_terminal.png",
            accent_color="#00c2cb",
            width=640,
            height=480
        )
        layout = self.content_layout

        # Terminal container with sleek black brutalist frame
        term_box = QWidget()
        term_box.setStyleSheet("background-color: #0e0e0d; border: 2px solid #0e0e0d; border-radius: 12px;")
        t_layout = QVBoxLayout(term_box)
        t_layout.setContentsMargins(12, 12, 12, 12)
        t_layout.setSpacing(8)

        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.output.setStyleSheet("background: #0e0e0d; color: #ea34df; font-family: monospace; font-size: 10pt; border: none;")
        backend_info = QwenEngine.get_backend_info()
        self.output.append(f"UselessOS Terminal v3.0 [TinkerHub Edition]\nQwen 3.5 0.8B Backend: {backend_info['status']} ({backend_info['name']})\nType 'useless help' or 'useless ai <prompt>' to query Qwen.\n")
        t_layout.addWidget(self.output)

        h_layout = QHBoxLayout()
        prompt = QLabel("useless@os:~$")
        prompt.setStyleSheet("color: #00c2cb; font-family: monospace; font-weight: bold; background: transparent; border: none;")
        self.input = QLineEdit()
        self.input.setStyleSheet("background: #1a1a18; color: #ffffff; font-family: monospace; font-size: 10pt; border: 1px solid #333330; border-radius: 6px; padding: 6px 10px;")
        self.input.returnPressed.connect(self.execute)
        
        h_layout.addWidget(prompt)
        h_layout.addWidget(self.input)
        t_layout.addLayout(h_layout)

        layout.addWidget(term_box)
        self.active_stream = None

    def print_text(self, text):
        self.output.append(text)
        self.output.verticalScrollBar().setValue(self.output.verticalScrollBar().maximum())

    def execute(self):
        val = self.input.text().strip()
        self.print_text(f"useless@os:~$ {val}")
        self.input.clear()
        
        if not val:
            return

        val_lower = val.lower()
        if val_lower == 'useless help':
            self.print_text("You have made a terrible mistake.")
            self.print_text("Available commands:\n useless ai <prompt>  (Chat with Qwen 3.5 0.8B)\n useless think\n useless procrastinate\n useless motivate\n useless complain\n useless coffee\n useless existential-crisis\n useless productivity\n sudo make-me-useful")
        elif val_lower.startswith('useless ai ') or val_lower.startswith('useless ask ') or val_lower.startswith('useless chat '):
            query = val.split(" ", 2)[-1]
            self.query_qwen(query)
        elif val_lower == 'useless productivity':
            self.print_text("Calculating productivity...\nERROR: Productivity not found in this universe.\nWould you like to overthink instead? [Y/n]")
        elif val_lower in ['y', 'yes']:
            self.print_text("Overthinking mode engaged. Synthesizing imaginary regrets...")
        elif val_lower == 'sudo make-me-useful':
            self.print_text("Permission denied.\nEven root cannot alter reality.")
        elif val_lower.startswith('useless '):
            self.print_text("Executing useless instruction...")
            QTimer.singleShot(800, lambda: self.print_text("Task completed. Accomplished absolutely nothing."))
        else:
            self.print_text(f"Command '{val}' not found. Try 'useless ai {val}' to contemplate it.")

    def query_qwen(self, query):
        self.print_text("[QWEN 3.5 (0.8B) INFERENCE ENGINE INITIATED...]")
        self.input.setEnabled(False)
        self._current_tokens = ""
        
        self.active_stream = QwenEngine.create_stream(
            user_prompt=query,
            system_prompt=TERMINAL_AI_PROMPT,
            parent=self
        )
        self.active_stream.token_emitted.connect(self._on_qwen_token)
        self.active_stream.finished_inference.connect(self._on_qwen_finished)
        self.active_stream.start()

    def _on_qwen_token(self, token):
        self._current_tokens += token

    def _on_qwen_finished(self, thought, answer):
        self.input.setEnabled(True)
        self.input.setFocus()
        self.print_text(f"> {answer}\n")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    useless_style.apply_corporate_style(app)
    win = UselessTerminal()
    win.show()
    run_app(app)
