#!/usr/bin/env python3
import sys
from qt_compat import *
import useless_style

class UselessSettings(useless_style.UselessWindow):
    def __init__(self):
        super().__init__(
            title="System Settings™",
            subtitle="Fine-tune your existential operating experience",
            icon_name="useless_settings.png",
            accent_color="#244638",
            width=680,
            height=500
        )
        layout = self.content_layout

        pane_layout = QHBoxLayout()
        pane_layout.setSpacing(16)

        # macOS style Sidebar
        self.list = QListWidget()
        self.list.setFixedWidth(170)
        self.list.addItems(["⚡ Performance", "🔒 Privacy", "🎨 Personalization", "🔔 Notifications", "⚙️ Advanced"])
        self.list.currentRowChanged.connect(self.change_tab)
        pane_layout.addWidget(self.list)

        self.stack = QStackedWidget()
        pane_layout.addWidget(self.stack)
        layout.addLayout(pane_layout)

        self.setup_performance()
        self.setup_privacy()
        self.setup_personalization()
        self.setup_notifications()
        self.setup_advanced()

        self.list.setCurrentRow(0)

    def change_tab(self, i):
        self.stack.setCurrentIndex(i)

    def add_header(self, layout, text):
        lbl = QLabel(text)
        lbl.setStyleSheet("font-family: Helvetica; font-size: 14pt; font-weight: 900; color: #0e0e0d;")
        layout.addWidget(lbl)
        
    def setup_performance(self):
        w = QWidget()
        l = QVBoxLayout(w)
        l.setSpacing(12)
        self.add_header(l, "Optimize Uselessness")
        
        card = QGroupBox("Resource Allocation")
        c_layout = QVBoxLayout(card)
        c_layout.addWidget(QLabel("Procrastination Multiplier"))
        slider = QSlider(Horizontal)
        slider.setValue(70)
        c_layout.addWidget(slider)
        c_layout.addWidget(QCheckBox("Enable background anxiety generation", checked=True))
        c_layout.addWidget(QCheckBox("Hardware accelerated overthinking"))
        l.addWidget(card)
        l.addStretch()
        self.stack.addWidget(w)

    def setup_privacy(self):
        w = QWidget()
        l = QVBoxLayout(w)
        l.setSpacing(12)
        self.add_header(l, "Hide Nothing")
        
        card = QGroupBox("Mandatory Transparency")
        c_layout = QVBoxLayout(card)
        cb1 = QCheckBox("Broadcast minor mistakes to internet")
        cb1.setChecked(True)
        cb1.setEnabled(False)
        c_layout.addWidget(cb1)
        
        cb2 = QCheckBox("Share browser history with refrigerator")
        cb2.setChecked(True)
        cb2.setEnabled(False)
        c_layout.addWidget(cb2)
        
        lbl = QLabel("These settings are managed by your own guilt.")
        lbl.setStyleSheet("color: #716f64; font-style: italic; font-size: 9pt;")
        c_layout.addWidget(lbl)
        l.addWidget(card)
        l.addStretch()
        self.stack.addWidget(w)

    def setup_personalization(self):
        w = QWidget()
        l = QVBoxLayout(w)
        l.setSpacing(12)
        self.add_header(l, "Shades of Absurdity")
        
        card = QGroupBox("Appearance")
        c_layout = QVBoxLayout(card)
        c_layout.addWidget(QLabel("Theme Color Palette"))
        combo = QComboBox()
        combo.addItems(["TinkerHub Brutalist (Default)", "Existential Magenta", "Crimson Panic", "Forest Solitude"])
        c_layout.addWidget(combo)
        l.addWidget(card)
        l.addStretch()
        self.stack.addWidget(w)

    def setup_notifications(self):
        w = QWidget()
        l = QVBoxLayout(w)
        l.setSpacing(12)
        self.add_header(l, "Placebo Alerts")
        
        card = QGroupBox("Notification Rules")
        c_layout = QVBoxLayout(card)
        c_layout.addWidget(QCheckBox("Notify when I'm dangerously productive", checked=True))
        c_layout.addWidget(QCheckBox("Random existential dread alarms", checked=True))
        l.addWidget(card)
        l.addStretch()
        self.stack.addWidget(w)

    def setup_advanced(self):
        w = QWidget()
        l = QVBoxLayout(w)
        l.setSpacing(12)
        self.add_header(l, "Advanced Configuration")
        
        self.warn_widget = QWidget()
        wl = QVBoxLayout(self.warn_widget)
        wl.setAlignment(AlignCenter)
        warn = QLabel("⚠️ CAUTION")
        warn.setStyleSheet("color: #e82803; font-size: 16pt; font-weight: 900; font-family: Helvetica;")
        warn.setAlignment(AlignCenter)
        wl.addWidget(warn)
        wl.addWidget(QLabel("These settings are extremely advanced.\nWe recommend not touching them."))
        btn = QPushButton("Continue Anyway")
        btn.clicked.connect(self.show_adv)
        wl.addWidget(btn)
        l.addWidget(self.warn_widget)
        
        self.adv_widget = QWidget()
        al = QVBoxLayout(self.adv_widget)
        
        al.addWidget(QLabel("Uselessness Kernel Scheduler"))
        c1 = QComboBox()
        c1.addItems(["Round-Robin Procrastination", "O(N^3) Time Wasting"])
        al.addWidget(c1)
        
        al.addWidget(QLabel("Quantum Procrastination State"))
        c2 = QComboBox()
        c2.addItems(["Superposition", "Collapsed (Doing Work)"])
        al.addWidget(c2)
        
        al.addWidget(QCheckBox("Enable Neural Excuse Cache", checked=True))
        l.addWidget(self.adv_widget)
        self.adv_widget.hide()
        
        l.addStretch()
        self.stack.addWidget(w)

    def show_adv(self):
        self.warn_widget.hide()
        self.adv_widget.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    useless_style.apply_corporate_style(app)
    win = UselessSettings()
    win.show()
    run_app(app)
