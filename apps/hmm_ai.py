#!/usr/bin/env python3
import sys
import os
from qt_compat import *
import useless_style
from qwen_backend import QwenEngine, DEFAULT_HMM_PROMPT, SYSTEM_PROMPT_PRESETS

class HmmAI(useless_style.UselessWindow):
    def __init__(self):
        super().__init__(
            title="AI That Says Hmm™",
            subtitle="Qwen 3.5 0.8B Cognitive Engine",
            icon_name="hmm_ai.png",
            accent_color="#00c2cb",
            width=620,
            height=540
        )
        layout = self.content_layout

        self.current_system_prompt = DEFAULT_HMM_PROMPT
        self.active_backend = QwenEngine.get_backend_info()

        # Telemetry Header Row
        tele_row = QHBoxLayout()
        self.badge_backend = QLabel(f"{self.active_backend['name']}: {self.active_backend['status']}")
        self.badge_backend.setStyleSheet("""
            background-color: #0e0e0d;
            color: #00c2cb;
            font-family: monospace;
            font-size: 8pt;
            font-weight: 900;
            padding: 4px 10px;
            border-radius: 8px;
        """)
        tele_row.addWidget(self.badge_backend)
        tele_row.addStretch()

        self.telemetry_lbl = QLabel("Tokens: 0 | Speed: 0.0 tok/s | Temp: 0.70 | Context: 2048")
        self.telemetry_lbl.setStyleSheet("""
            color: #716f64;
            font-family: monospace;
            font-size: 8pt;
            font-weight: 700;
        """)
        tele_row.addWidget(self.telemetry_lbl)
        layout.addLayout(tele_row)

        # Persona & System Prompt Control Row
        ctrl_row = QHBoxLayout()
        ctrl_row.setSpacing(8)
        
        p_lbl = QLabel("PERSONA:")
        p_lbl.setStyleSheet("font-family: monospace; font-size: 8pt; font-weight: 900; color: #0e0e0d;")
        ctrl_row.addWidget(p_lbl)

        self.persona_combo = QComboBox()
        self.persona_combo.setStyleSheet("""
            QComboBox {
                background: #ffffff;
                color: #0e0e0d;
                border: 2px solid #0e0e0d;
                border-radius: 8px;
                padding: 4px 10px;
                font-family: Helvetica;
                font-size: 8.5pt;
                font-weight: 700;
            }
            QComboBox::drop-down {
                border: none;
            }
        """)
        for name in SYSTEM_PROMPT_PRESETS.keys():
            self.persona_combo.addItem(name)
        self.persona_combo.currentTextChanged.connect(self.on_persona_changed)
        ctrl_row.addWidget(self.persona_combo)

        self.prompt_btn = QPushButton("⚙ Edit System Prompt")
        self.prompt_btn.setCursor(QCursor(PointingHandCursor))
        self.prompt_btn.setStyleSheet("""
            QPushButton {
                background: #f5f4f0;
                color: #0e0e0d;
                border: 2px solid #0e0e0d;
                border-radius: 8px;
                padding: 4px 12px;
                font-size: 8pt;
                font-weight: 800;
            }
            QPushButton:hover {
                background: #0e0e0d;
                color: #ffffff;
            }
        """)
        self.prompt_btn.clicked.connect(self.open_prompt_editor)
        ctrl_row.addWidget(self.prompt_btn)
        ctrl_row.addStretch()
        layout.addLayout(ctrl_row)

        # Chat Conversation View
        self.chat = QTextEdit()
        self.chat.setReadOnly(True)
        self.chat.setStyleSheet("""
            QTextEdit {
                background-color: #f5f4f0;
                border: 2px solid #0e0e0d;
                border-radius: 12px;
                padding: 14px;
                font-family: Helvetica;
                font-size: 10pt;
                color: #0e0e0d;
                line-height: 140%;
            }
        """)
        self.chat.append("<b style='color: #00c2cb;'>Qwen 3.5 0.8B:</b> System prompt initialized. I am loaded and ready to contemplate your query with profound hesitation.")
        layout.addWidget(self.chat)
        
        # Live Reasoning / Generation Status Banner
        self.status_box = QLabel("")
        self.status_box.setStyleSheet("""
            background: #0e0e0d;
            color: #ffffff;
            font-family: monospace;
            font-weight: 700;
            font-size: 8.5pt;
            padding: 6px 12px;
            border-radius: 8px;
        """)
        self.status_box.hide()
        layout.addWidget(self.status_box)

        # Input Row
        h_layout = QHBoxLayout()
        h_layout.setSpacing(10)
        self.input = QLineEdit()
        self.input.setPlaceholderText("Ask a profound life dilemma or technical question...")
        self.input.returnPressed.connect(self.ask)
        h_layout.addWidget(self.input)

        self.btn = QPushButton("Ask AI")
        self.btn.setCursor(QCursor(PointingHandCursor))
        self.btn.clicked.connect(self.ask)
        h_layout.addWidget(self.btn)
        layout.addLayout(h_layout)

        self.current_stream = None
        self._current_thought_chunk = ""
        self._current_answer_chunk = ""

    def on_persona_changed(self, persona_name):
        preset = SYSTEM_PROMPT_PRESETS.get(persona_name, "")
        if preset:
            self.current_system_prompt = preset
            self.chat.append(f"<div style='color: #716f64; font-size: 8.5pt; margin: 4px 0;'><i>[System Persona switched to: <b>{persona_name}</b>]</i></div>")

    def open_prompt_editor(self):
        """Opens a modal to view and modify the raw system prompt in real time."""
        dlg = QDialog(self)
        dlg.setWindowTitle("Configure System Prompt (Qwen 3.5 0.8B)")
        dlg_w = 540
        dlg_h = 440
        dlg.setFixedSize(dlg_w, dlg_h)
        dlg.setWindowFlags((Qt.WindowType.Dialog if PYQT6 else Qt.Dialog) | (Qt.WindowType.FramelessWindowHint if PYQT6 else Qt.FramelessWindowHint))
        dlg.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground if PYQT6 else Qt.WA_TranslucentBackground)
        if hasattr(Qt, 'WindowModality') and hasattr(Qt.WindowModality, 'ApplicationModal'):
            dlg.setWindowModality(Qt.WindowModality.ApplicationModal)
        elif hasattr(Qt, 'ApplicationModal'):
            dlg.setWindowModality(Qt.ApplicationModal)

        d_frame = QFrame(dlg)
        d_frame.setObjectName("PromptEditorModalFrame")
        d_frame.setStyleSheet("""
            QFrame#PromptEditorModalFrame {
                background-color: #ffffff;
                border: 2.5px solid #0e0e0d;
                border-radius: 20px;
            }
        """)

        d_root_lay = QVBoxLayout(dlg)
        d_root_lay.setContentsMargins(0, 0, 0, 0)
        d_root_lay.addWidget(d_frame)

        d_lay = QVBoxLayout(d_frame)
        d_lay.setContentsMargins(20, 18, 20, 18)
        d_lay.setSpacing(10)

        # Header row
        hdr_row = QHBoxLayout()
        hdr = QLabel("SYSTEM PROMPT CONFIGURATION")
        hdr.setStyleSheet("font-family: Helvetica; font-weight: 900; font-size: 11pt; color: #0e0e0d; border: none; background: transparent;")
        hdr_row.addWidget(hdr)
        hdr_row.addStretch()

        c_btn = QPushButton("✕")
        c_btn.setFixedSize(28, 28)
        c_btn.setCursor(QCursor(PointingHandCursor))
        c_btn.setStyleSheet("""
            QPushButton {
                background-color: #0e0e0d;
                color: #ffffff;
                border-radius: 14px;
                font-weight: 900;
                font-size: 10pt;
                border: none;
            }
            QPushButton:hover {
                background-color: #e82803;
            }
        """)
        c_btn.clicked.connect(dlg.reject)
        hdr_row.addWidget(c_btn)
        d_lay.addLayout(hdr_row)

        info = QLabel("This system prompt is injected into ChatML (<|im_start|>system...<|im_end|>) to steer Qwen's tone and output constraints.")
        info.setWordWrap(True)
        info.setStyleSheet("font-size: 8.5pt; color: #716f64; border: none; background: transparent;")
        d_lay.addWidget(info)

        txt = QTextEdit()
        txt.setStyleSheet("""
            background-color: #f5f4f0;
            color: #0e0e0d;
            font-family: monospace;
            font-size: 9pt;
            border: 2px solid #0e0e0d;
            border-radius: 8px;
            padding: 8px;
        """)
        txt.setPlainText(self.current_system_prompt)
        d_lay.addWidget(txt)

        btn_row = QHBoxLayout()
        btn_row.addStretch()

        reset_btn = QPushButton("Reset to Default")
        reset_btn.setCursor(QCursor(PointingHandCursor))
        reset_btn.setStyleSheet("background: #f5f4f0; color: #0e0e0d; border: 2px solid #0e0e0d; border-radius: 8px; padding: 6px 14px; font-weight: 800;")
        reset_btn.clicked.connect(lambda: txt.setPlainText(DEFAULT_HMM_PROMPT))
        btn_row.addWidget(reset_btn)

        save_btn = QPushButton("Apply System Prompt")
        save_btn.setCursor(QCursor(PointingHandCursor))
        save_btn.setStyleSheet("background: #00c2cb; color: #0e0e0d; border: 2px solid #0e0e0d; border-radius: 8px; padding: 6px 16px; font-weight: 900;")
        
        def save_and_close():
            self.current_system_prompt = txt.toPlainText().strip()
            self.persona_combo.setCurrentText("Custom Persona")
            self.chat.append("<div style='color: #00c2cb; font-size: 8.5pt; margin: 4px 0;'><i>[Custom System Prompt Applied to Qwen 3.5 0.8B Backend]</i></div>")
            dlg.accept()

        save_btn.clicked.connect(save_and_close)
        btn_row.addWidget(save_btn)
        d_lay.addLayout(btn_row)

        # Center over parent window, clamped within screen bounds
        p_geo = self.geometry()
        center_x = p_geo.x() + (p_geo.width() - dlg_w) // 2
        center_y = p_geo.y() + (p_geo.height() - dlg_h) // 2
        screen = QApplication.primaryScreen()
        if screen:
            s_geo = screen.availableGeometry()
            center_x = max(s_geo.x() + 10, min(center_x, s_geo.right() - dlg_w - 10))
            center_y = max(s_geo.y() + 44, min(center_y, s_geo.bottom() - dlg_h - 10))
        dlg.move(center_x, center_y)

        # Enable mouse dragging
        drag_state = {"pos": None}
        def mouse_press(event):
            if event.button() == (Qt.MouseButton.LeftButton if PYQT6 else Qt.LeftButton):
                pos = event.globalPosition().toPoint() if hasattr(event, 'globalPosition') else event.globalPos()
                drag_state["pos"] = pos - dlg.frameGeometry().topLeft()
                event.accept()
        def mouse_move(event):
            if drag_state["pos"] is not None and (event.buttons() & (Qt.MouseButton.LeftButton if PYQT6 else Qt.LeftButton)):
                pos = event.globalPosition().toPoint() if hasattr(event, 'globalPosition') else event.globalPos()
                target = pos - drag_state["pos"]
                scr = QApplication.primaryScreen()
                if scr:
                    sg = scr.availableGeometry()
                    target.setY(max(sg.y() + 40, min(target.y(), sg.bottom() - 60)))
                    target.setX(max(sg.x() - dlg.width() + 100, min(target.x(), sg.right() - 100)))
                dlg.move(target)
                event.accept()
        def mouse_release(event):
            drag_state["pos"] = None
            event.accept()

        d_frame.mousePressEvent = mouse_press
        d_frame.mouseMoveEvent = mouse_move
        d_frame.mouseReleaseEvent = mouse_release

        if PYQT6:
            dlg.exec()
        else:
            dlg.exec_()

    def ask(self):
        query = self.input.text().strip()
        if not query:
            return
        
        self.chat.append(f"<br><b style='color: #ea34df;'>You:</b> {query}")
        self.input.clear()
        
        self.btn.setEnabled(False)
        self.input.setEnabled(False)
        self.status_box.setText("THINKING: Initializing ChatML context tensors...")
        self.status_box.show()
        
        self._current_thought_chunk = ""
        self._current_answer_chunk = ""
        
        self.current_stream = QwenEngine.create_stream(
            user_prompt=query,
            system_prompt=self.current_system_prompt,
            parent=self
        )
        self.current_stream.thought_emitted.connect(self.on_thought_token)
        self.current_stream.token_emitted.connect(self.on_answer_token)
        self.current_stream.stats_updated.connect(self.on_stats_updated)
        self.current_stream.finished_inference.connect(self.on_inference_finished)
        self.current_stream.start()

    def on_thought_token(self, token):
        self._current_thought_chunk += token
        self.status_box.setText(f"<span style='color: #ffb800;'>[REASONING TRACE]</span> {self._current_thought_chunk[-60:]}")

    def on_answer_token(self, token):
        self._current_answer_chunk += token
        self.status_box.setText(f"<span style='color: #00ff66;'>[SYNTHESIZING]</span> {self._current_answer_chunk[-50:]}")

    def on_stats_updated(self, stats):
        tokens = stats.get("tokens", 0)
        speed = stats.get("speed", "0.0 tok/s")
        temp = stats.get("temp", 0.7)
        phase = stats.get("phase", "Active")
        model = stats.get("model", "Qwen3.5-0.8B")
        self.telemetry_lbl.setText(f"{model} | Phase: {phase} | Tokens: {tokens} | Speed: {speed}")

    def on_inference_finished(self, thought, answer):
        self.status_box.hide()
        self.btn.setEnabled(True)
        self.input.setEnabled(True)
        self.input.setFocus()
        
        thought_html = f"<div style='margin: 6px 0px; padding: 8px 12px; background: #e5e5df; border-left: 3px solid #716f64; border-radius: 4px; font-size: 8.5pt; color: #444440;'><b>Thought Process:</b><br>{thought.replace(chr(10), '<br>')}</div>"
        answer_html = f"<b style='color: #00c2cb;'>Qwen 3.5 (0.8B):</b> {answer}"
        
        self.chat.append(thought_html)
        self.chat.append(answer_html)
        self.chat.verticalScrollBar().setValue(self.chat.verticalScrollBar().maximum())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    useless_style.apply_corporate_style(app)
    win = HmmAI()
    win.show()
    run_app(app)
