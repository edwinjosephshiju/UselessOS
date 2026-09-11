#!/usr/bin/env python3
import sys
from qt_compat import *
import useless_style

class UselessAlarm(useless_style.UselessWindow):
    def __init__(self):
        super().__init__(
            title="Alarm That Doesn't Wake You™",
            subtitle="Respecting your bad sleep decisions unconditionally",
            icon_name="useless_alarm.png",
            accent_color="#e82803",
            width=460,
            height=420
        )
        layout = self.content_layout

        self.clock = QLabel()
        self.clock.setStyleSheet("""
            QLabel {
                font-size: 34pt;
                font-weight: 900;
                font-family: monospace;
                background: #f5f4f0;
                border: 2px solid #0e0e0d;
                border-radius: 14px;
                color: #0e0e0d;
                padding: 10px;
            }
        """)
        self.clock.setAlignment(AlignCenter)
        layout.addWidget(self.clock)

        card = QGroupBox("Awakening Preferences")
        c_layout = QVBoxLayout(card)
        lbl = QLabel("Select target awakening time:")
        lbl.setStyleSheet("font-weight: 700;")
        c_layout.addWidget(lbl)
        
        self.time_edit = QTimeEdit()
        self.time_edit.setTime(QTime.currentTime())
        c_layout.addWidget(self.time_edit)
        layout.addWidget(card)

        btn = QPushButton("Set Gentle Disappointment")
        btn.clicked.connect(self.set_alarm)
        layout.addWidget(btn)

        self.msg = QLabel("GOOD MORNING.\n\nYour alarm has been ringing silently for 17 minutes.\nWe decided not to interfere with your rest.\nSleep well.")
        self.msg.setStyleSheet("color: #e82803; font-weight: 800; font-size: 10pt; background: #ffffff; border: 2px solid #e82803; border-radius: 12px; padding: 10px;")
        self.msg.setAlignment(AlignCenter)
        self.msg.hide()
        layout.addWidget(self.msg)

        self.alarm_time = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)
        self.update_time()

    def update_time(self):
        now = QTime.currentTime()
        self.clock.setText(now.toString("HH:mm:ss"))
        
        if self.alarm_time and now.hour() == self.alarm_time.hour() and now.minute() == self.alarm_time.minute():
            self.msg.show()
            self.alarm_time = None

    def set_alarm(self):
        self.alarm_time = self.time_edit.time()
        self.msg.hide()
        QMessageBox.information(self, "Alarm Set", f"Alarm set for {self.alarm_time.toString('HH:mm')}. We will definitely not wake you.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    useless_style.apply_corporate_style(app)
    win = UselessAlarm()
    win.show()
    run_app(app)
