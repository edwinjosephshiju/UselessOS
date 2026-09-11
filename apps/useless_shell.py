#!/usr/bin/env python3
import os
import sys
import subprocess
import random

from qt_compat import *
import useless_style

def get_asset_path(subpath):
    """Find asset path in /opt/uselessos/assets or local apps/assets."""
    candidates = [
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", subpath),
        os.path.join("/opt/uselessos/assets", subpath),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "useless-repo-check", "public", subpath)
    ]
    for c in candidates:
        if os.path.exists(c):
            return c
    return None

def get_icon_path(filename):
    """Find icon PNG in /opt/uselessos/assets/icons or local apps/assets/icons."""
    candidates = [
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "icons", filename),
        os.path.join("/opt/uselessos/assets", "icons", filename)
    ]
    for c in candidates:
        if os.path.exists(c):
            return c
    return None

APPS_DATA = [
    ("Excuses", "excuse_generator.py", "excuses.png", "#ea34df", "Absence Authorization & Mitigation Matrix"),
    ("Overthink", "overthinking_engine.py", "overthinking.png", "#e82803", "Simulate 14,000,605 Catastrophic Thoughts"),
    ("Hmm AI", "hmm_ai.py", "hmm_ai.png", "#244638", "World's Most Non-Committal Artificial Intelligence"),
    ("Analytics", "uselessness_analytics.py", "analytics.png", "#ea34df", "Certified Enterprise Procrastination Metrics"),
    ("ScreenTime", "screen_time.py", "screentime.png", "#00c2cb", "Track Hours Dedicated to Glowing Rectangles"),
    ("Existential", "existential_tracker.py", "existential.png", "#ffb800", "Real-Time Telemetry of Cosmic Insignificance"),
    ("EmoBin", "emotional_bin.py", "emotional_bin.png", "#ff6b00", "Discard Mental Baggage Without Resolution"),
    ("Alarm", "useless_alarm.py", "alarm.png", "#e82803", "Passive Alarm Respecting Bad Sleep Choices"),
    ("Settings", "useless_settings.py", "settings.png", "#c0326b", "Configure Purely Placebo System Preferences"),
    ("Terminal", "useless_terminal.py", "terminal.png", "#0e0e0d", "Sub-Command Line With Certified Zero Utility")
]

def launch_app(script):
    app_path = os.path.join("/opt/uselessos", script)
    if not os.path.exists(app_path):
        app_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), script)
    print(f"[UselessShell] Launching {app_path}")
    env = os.environ.copy()
    env["DISPLAY"] = os.environ.get("DISPLAY", ":0")
    try:
        proc = subprocess.Popen([sys.executable, app_path], env=env)
        return proc
    except Exception as e:
        print(f"[UselessShell] Error launching {script}: {e}")
        return None

def safe_check_output(cmd, env=None, timeout=0.8, default=""):
    """Execute CLI command safely with strict timeout and no blocking on stdin."""
    try:
        return subprocess.check_output(
            cmd,
            env=env,
            stdin=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            text=True,
            timeout=timeout
        )
    except Exception:
        return default


class ControlCenterDrawer(QFrame):
    """
    macOS-style Control Center in TinkerHub brutalist theme.
    Contains Real System Tools:
    - Real Power Actions (Shutdown, Restart)
    - Interactive Wi-Fi Connection Panel (Active SSID, signal, available networks list, connect/refresh actions)
    - Interactive Bluetooth Device Panel (Active connected devices, available nearby devices, pair/refresh actions)
    - Real Sound volume slider (PulseAudio / ALSA)
    - Real Display Brightness slider (xrandr)
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(360, 560)
        self.setObjectName("ControlCenterFrame")
        self.setStyleSheet("""
            #ControlCenterFrame {
                background-color: #ffffff;
                border: 3px solid #0e0e0d;
                border-radius: 22px;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 16, 18, 20)
        layout.setSpacing(10)
        
        # Header
        h_box = QHBoxLayout()
        title = QLabel("CONTROL CENTER")
        title.setStyleSheet("font-family: Helvetica; font-size: 12pt; font-weight: 900; color: #0e0e0d; background: transparent; border: none;")
        h_box.addWidget(title)
        h_box.addStretch()
        
        close_btn = QPushButton("✕")
        close_btn.setFixedSize(26, 26)
        close_btn.setCursor(QCursor(PointingHandCursor))
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #0e0e0d;
                color: #ffffff;
                border-radius: 13px;
                font-weight: 900;
                font-size: 9pt;
                border: none;
            }
            QPushButton:hover {
                background-color: #e82803;
            }
        """)
        close_btn.clicked.connect(self.hide)
        h_box.addWidget(close_btn)
        layout.addLayout(h_box)
        
        # 1. Real Power Actions (Shutdown, Restart)
        pwr_box = QHBoxLayout()
        pwr_box.setSpacing(10)
        
        self.btn_shutdown = QPushButton("Shutdown")
        self.btn_shutdown.setCursor(QCursor(PointingHandCursor))
        self.btn_shutdown.setFixedHeight(36)
        self.btn_shutdown.setStyleSheet("""
            QPushButton {
                background-color: #e82803;
                color: #ffffff;
                border: 2px solid #0e0e0d;
                border-radius: 12px;
                font-family: Helvetica;
                font-weight: 900;
                font-size: 9pt;
            }
            QPushButton:hover {
                background-color: #0e0e0d;
            }
        """)
        self.btn_shutdown.clicked.connect(self.action_shutdown)
        pwr_box.addWidget(self.btn_shutdown)
        
        self.btn_restart = QPushButton("Restart")
        self.btn_restart.setCursor(QCursor(PointingHandCursor))
        self.btn_restart.setFixedHeight(36)
        self.btn_restart.setStyleSheet("""
            QPushButton {
                background-color: #ffb800;
                color: #0e0e0d;
                border: 2px solid #0e0e0d;
                border-radius: 12px;
                font-family: Helvetica;
                font-weight: 900;
                font-size: 9pt;
            }
            QPushButton:hover {
                background-color: #0e0e0d;
                color: #ffffff;
            }
        """)
        self.btn_restart.clicked.connect(self.action_restart)
        pwr_box.addWidget(self.btn_restart)
        layout.addLayout(pwr_box)
        
        # 2. Wireless Controls Header Buttons (Wi-Fi and Bluetooth Quick Select)
        self.wifi_state = True
        self.bt_state = True
        self.connected_ssid = "TinkerHub-Campus (5GHz)"
        self.connected_bt = ["Magic Keyboard (88%)", "AirPods Pro (Connected)"]
        self.wifi_networks = []
        self.bt_devices = []
        
        net_box = QHBoxLayout()
        net_box.setSpacing(8)
        
        self.btn_wifi_tab = QPushButton("Wi-Fi\nConnected")
        self.btn_wifi_tab.setCursor(QCursor(PointingHandCursor))
        self.btn_wifi_tab.setFixedHeight(46)
        self.btn_wifi_tab.clicked.connect(lambda: self.switch_wireless_tab(0))
        net_box.addWidget(self.btn_wifi_tab)
        
        self.btn_bt_tab = QPushButton("Bluetooth\n2 Devices")
        self.btn_bt_tab.setCursor(QCursor(PointingHandCursor))
        self.btn_bt_tab.setFixedHeight(46)
        self.btn_bt_tab.clicked.connect(lambda: self.switch_wireless_tab(1))
        net_box.addWidget(self.btn_bt_tab)
        layout.addLayout(net_box)
        
        # 3. Interactive Wireless Connections & Devices Panel
        self.wireless_card = QFrame()
        self.wireless_card.setStyleSheet("""
            QFrame {
                background-color: #f5f4f0;
                border: 2px solid #0e0e0d;
                border-radius: 14px;
            }
        """)
        w_card_layout = QVBoxLayout(self.wireless_card)
        w_card_layout.setContentsMargins(10, 8, 10, 10)
        w_card_layout.setSpacing(6)
        
        # Segmented Tab Selector
        seg_layout = QHBoxLayout()
        seg_layout.setSpacing(6)
        self.seg_wifi = QPushButton("Wi-Fi Networks")
        self.seg_wifi.setFixedHeight(28)
        self.seg_wifi.setCursor(QCursor(PointingHandCursor))
        self.seg_wifi.clicked.connect(lambda: self.switch_wireless_tab(0))
        seg_layout.addWidget(self.seg_wifi)
        
        self.seg_bt = QPushButton("Bluetooth Devices")
        self.seg_bt.setFixedHeight(28)
        self.seg_bt.setCursor(QCursor(PointingHandCursor))
        self.seg_bt.clicked.connect(lambda: self.switch_wireless_tab(1))
        seg_layout.addWidget(self.seg_bt)
        w_card_layout.addLayout(seg_layout)
        
        # Stacked Widget for Wi-Fi and Bluetooth
        self.wireless_stack = QStackedWidget()
        
        # --- TAB 0: Wi-Fi Networks View ---
        wifi_view = QWidget()
        wifi_lay = QVBoxLayout(wifi_view)
        wifi_lay.setContentsMargins(0, 4, 0, 0)
        wifi_lay.setSpacing(6)
        
        # Power toggle row
        wifi_pwr_row = QHBoxLayout()
        self.wifi_status_lbl = QLabel("Wi-Fi Status:")
        self.wifi_status_lbl.setStyleSheet("font-weight: 800; font-family: Helvetica; font-size: 8.5pt; color: #0e0e0d; border: none; background: transparent;")
        wifi_pwr_row.addWidget(self.wifi_status_lbl)
        wifi_pwr_row.addStretch()
        
        self.wifi_toggle_btn = QPushButton("ON")
        self.wifi_toggle_btn.setFixedSize(56, 24)
        self.wifi_toggle_btn.setCursor(QCursor(PointingHandCursor))
        self.wifi_toggle_btn.clicked.connect(self.toggle_wifi)
        wifi_pwr_row.addWidget(self.wifi_toggle_btn)
        wifi_lay.addLayout(wifi_pwr_row)
        
        # Connected Network Card
        self.wifi_conn_card = QWidget()
        self.wifi_conn_card.setStyleSheet("background-color: #ffffff; border: 1.5px solid #244638; border-radius: 8px; padding: 4px;")
        wcc_lay = QHBoxLayout(self.wifi_conn_card)
        wcc_lay.setContentsMargins(6, 2, 6, 2)
        self.wifi_conn_lbl = QLabel(f"Connected: {self.connected_ssid}")
        self.wifi_conn_lbl.setStyleSheet("color: #244638; font-weight: 900; font-size: 8.5pt; border: none; background: transparent; font-family: Helvetica;")
        wcc_lay.addWidget(self.wifi_conn_lbl)
        wcc_lay.addStretch()
        self.btn_disconnect_wifi = QPushButton("Disconnect")
        self.btn_disconnect_wifi.setFixedHeight(20)
        self.btn_disconnect_wifi.setStyleSheet("""
            QPushButton {
                background: #f5f4f0;
                color: #e82803;
                border: 1px solid #0e0e0d;
                border-radius: 6px;
                font-size: 7.5pt;
                font-weight: 800;
                padding: 1px 6px;
            }
            QPushButton:hover {
                background: #e82803;
                color: #ffffff;
            }
        """)
        self.btn_disconnect_wifi.clicked.connect(self.disconnect_wifi)
        wcc_lay.addWidget(self.btn_disconnect_wifi)
        wifi_lay.addWidget(self.wifi_conn_card)
        
        # Available Networks List
        avail_hdr = QLabel("Available Networks:")
        avail_hdr.setStyleSheet("font-weight: 800; font-size: 8pt; color: #716f64; text-transform: uppercase; border: none; background: transparent; font-family: Helvetica;")
        wifi_lay.addWidget(avail_hdr)
        
        self.wifi_list = QListWidget()
        self.wifi_list.setFixedHeight(75)
        self.wifi_list.setStyleSheet("""
            QListWidget {
                background-color: #ffffff;
                border: 1.5px solid #0e0e0d;
                border-radius: 8px;
                padding: 2px;
                font-size: 8pt;
                font-family: Helvetica;
            }
            QListWidget::item {
                padding: 4px 6px;
                border-radius: 4px;
            }
            QListWidget::item:hover {
                background-color: #f5f4f0;
            }
            QListWidget::item:selected {
                background-color: #244638;
                color: #ffffff;
            }
        """)
        self.wifi_list.itemDoubleClicked.connect(self.connect_selected_wifi)
        wifi_lay.addWidget(self.wifi_list)
        
        # Scan / Connect Row
        wifi_act_row = QHBoxLayout()
        self.btn_connect_wifi = QPushButton("Connect Selected")
        self.btn_connect_wifi.setFixedHeight(24)
        self.btn_connect_wifi.setStyleSheet("""
            QPushButton {
                background-color: #244638;
                color: #ffffff;
                border: 1.5px solid #0e0e0d;
                border-radius: 8px;
                font-weight: 800;
                font-size: 8pt;
                padding: 2px 8px;
            }
            QPushButton:hover {
                background-color: #0e0e0d;
            }
        """)
        self.btn_connect_wifi.clicked.connect(self.connect_selected_wifi)
        wifi_act_row.addWidget(self.btn_connect_wifi)
        
        self.btn_scan_wifi = QPushButton("Refresh")
        self.btn_scan_wifi.setFixedHeight(24)
        self.btn_scan_wifi.setStyleSheet("""
            QPushButton {
                background-color: #ffffff;
                color: #0e0e0d;
                border: 1.5px solid #0e0e0d;
                border-radius: 8px;
                font-weight: 800;
                font-size: 8pt;
                padding: 2px 8px;
            }
            QPushButton:hover {
                background-color: #f5f4f0;
            }
        """)
        self.btn_scan_wifi.clicked.connect(self.refresh_wifi_networks)
        wifi_act_row.addWidget(self.btn_scan_wifi)
        wifi_lay.addLayout(wifi_act_row)
        
        self.wireless_stack.addWidget(wifi_view)
        
        # --- TAB 1: Bluetooth Devices View ---
        bt_view = QWidget()
        bt_lay = QVBoxLayout(bt_view)
        bt_lay.setContentsMargins(0, 4, 0, 0)
        bt_lay.setSpacing(6)
        
        # Power toggle row
        bt_pwr_row = QHBoxLayout()
        self.bt_status_lbl = QLabel("Bluetooth Status:")
        self.bt_status_lbl.setStyleSheet("font-weight: 800; font-family: Helvetica; font-size: 8.5pt; color: #0e0e0d; border: none; background: transparent;")
        bt_pwr_row.addWidget(self.bt_status_lbl)
        bt_pwr_row.addStretch()
        
        self.bt_toggle_btn = QPushButton("ON")
        self.bt_toggle_btn.setFixedSize(56, 24)
        self.bt_toggle_btn.setCursor(QCursor(PointingHandCursor))
        self.bt_toggle_btn.clicked.connect(self.toggle_bluetooth)
        bt_pwr_row.addWidget(self.bt_toggle_btn)
        bt_lay.addLayout(bt_pwr_row)
        
        # Connected Device Card
        self.bt_conn_card = QWidget()
        self.bt_conn_card.setStyleSheet("background-color: #ffffff; border: 1.5px solid #00c2cb; border-radius: 8px; padding: 4px;")
        bcc_lay = QHBoxLayout(self.bt_conn_card)
        bcc_lay.setContentsMargins(6, 2, 6, 2)
        self.bt_conn_lbl = QLabel("Connected: Magic Keyboard (88%)")
        self.bt_conn_lbl.setStyleSheet("color: #0e0e0d; font-weight: 900; font-size: 8.5pt; border: none; background: transparent; font-family: Helvetica;")
        bcc_lay.addWidget(self.bt_conn_lbl)
        bcc_lay.addStretch()
        self.btn_disconnect_bt = QPushButton("Disconnect")
        self.btn_disconnect_bt.setFixedHeight(20)
        self.btn_disconnect_bt.setStyleSheet("""
            QPushButton {
                background: #f5f4f0;
                color: #e82803;
                border: 1px solid #0e0e0d;
                border-radius: 6px;
                font-size: 7.5pt;
                font-weight: 800;
                padding: 1px 6px;
            }
            QPushButton:hover {
                background: #e82803;
                color: #ffffff;
            }
        """)
        self.btn_disconnect_bt.clicked.connect(self.disconnect_bt)
        bcc_lay.addWidget(self.btn_disconnect_bt)
        bt_lay.addWidget(self.bt_conn_card)
        
        # Available Devices List
        bt_avail_hdr = QLabel("Discovered Devices:")
        bt_avail_hdr.setStyleSheet("font-weight: 800; font-size: 8pt; color: #716f64; text-transform: uppercase; border: none; background: transparent; font-family: Helvetica;")
        bt_lay.addWidget(bt_avail_hdr)
        
        self.bt_list = QListWidget()
        self.bt_list.setFixedHeight(75)
        self.bt_list.setStyleSheet("""
            QListWidget {
                background-color: #ffffff;
                border: 1.5px solid #0e0e0d;
                border-radius: 8px;
                padding: 2px;
                font-size: 8pt;
                font-family: Helvetica;
            }
            QListWidget::item {
                padding: 4px 6px;
                border-radius: 4px;
            }
            QListWidget::item:hover {
                background-color: #f5f4f0;
            }
            QListWidget::item:selected {
                background-color: #00c2cb;
                color: #ffffff;
            }
        """)
        self.bt_list.itemDoubleClicked.connect(self.connect_selected_bt)
        bt_lay.addWidget(self.bt_list)
        
        # Pair / Scan Row
        bt_act_row = QHBoxLayout()
        self.btn_pair_bt = QPushButton("Pair / Connect")
        self.btn_pair_bt.setFixedHeight(24)
        self.btn_pair_bt.setStyleSheet("""
            QPushButton {
                background-color: #00c2cb;
                color: #ffffff;
                border: 1.5px solid #0e0e0d;
                border-radius: 8px;
                font-weight: 800;
                font-size: 8pt;
                padding: 2px 8px;
            }
            QPushButton:hover {
                background-color: #0e0e0d;
            }
        """)
        self.btn_pair_bt.clicked.connect(self.connect_selected_bt)
        bt_act_row.addWidget(self.btn_pair_bt)
        
        self.btn_scan_bt = QPushButton("Discover")
        self.btn_scan_bt.setFixedHeight(24)
        self.btn_scan_bt.setStyleSheet("""
            QPushButton {
                background-color: #ffffff;
                color: #0e0e0d;
                border: 1.5px solid #0e0e0d;
                border-radius: 8px;
                font-weight: 800;
                font-size: 8pt;
                padding: 2px 8px;
            }
            QPushButton:hover {
                background-color: #f5f4f0;
            }
        """)
        self.btn_scan_bt.clicked.connect(self.refresh_bt_devices)
        bt_act_row.addWidget(self.btn_scan_bt)
        bt_lay.addLayout(bt_act_row)
        
        self.wireless_stack.addWidget(bt_view)
        w_card_layout.addWidget(self.wireless_stack)
        layout.addWidget(self.wireless_card)
        
        # 4. Real Sound Volume Slider
        init_vol = self.get_current_volume()
        self.sound_lbl = QLabel(f"Sound Volume: {init_vol}%")
        self.sound_lbl.setStyleSheet("font-weight: 800; font-size: 8.5pt; color: #0e0e0d; background: transparent; border: none; font-family: Helvetica;")
        layout.addWidget(self.sound_lbl)
        
        self.sound_slider = QSlider(Horizontal)
        self.sound_slider.setRange(0, 100)
        self.sound_slider.setValue(init_vol)
        self.sound_slider.setStyleSheet(self._slider_style("#244638"))
        self.sound_slider.valueChanged.connect(self.on_volume_changed)
        layout.addWidget(self.sound_slider)
        
        # 5. Real Display Brightness Slider
        self.bright_lbl = QLabel("Display Brightness: 100%")
        self.bright_lbl.setStyleSheet("font-weight: 800; font-size: 8.5pt; color: #0e0e0d; background: transparent; border: none; font-family: Helvetica;")
        layout.addWidget(self.bright_lbl)
        
        self.bright_slider = QSlider(Horizontal)
        self.bright_slider.setRange(20, 100)
        self.bright_slider.setValue(100)
        self.bright_slider.setStyleSheet(self._slider_style("#ea34df"))
        self.bright_slider.valueChanged.connect(self.on_brightness_changed)
        layout.addWidget(self.bright_slider)
        
        # Initialize wireless & populate
        self.populate_default_connections()
        self.switch_wireless_tab(0)
        self.init_hardware_states()
        
    def _slider_style(self, accent_color):
        return f"""
            QSlider::groove:horizontal {{
                border: 2px solid #0e0e0d;
                height: 10px;
                background: #f5f4f0;
                border-radius: 5px;
            }}
            QSlider::sub-page:horizontal {{
                background: {accent_color};
                border: 2px solid #0e0e0d;
                border-radius: 5px;
            }}
            QSlider::handle:horizontal {{
                background: #ffffff;
                border: 2px solid #0e0e0d;
                width: 22px;
                margin-top: -6px;
                margin-bottom: -6px;
                border-radius: 11px;
            }}
        """

    def switch_wireless_tab(self, index):
        self.wireless_stack.setCurrentIndex(index)
        if index == 0:
            self.seg_wifi.setStyleSheet("background-color: #244638; color: #ffffff; border: 1.5px solid #0e0e0d; border-radius: 8px; font-weight: 900; font-size: 8pt;")
            self.seg_bt.setStyleSheet("background-color: #ffffff; color: #0e0e0d; border: 1.5px solid #0e0e0d; border-radius: 8px; font-weight: 700; font-size: 8pt;")
        else:
            self.seg_wifi.setStyleSheet("background-color: #ffffff; color: #0e0e0d; border: 1.5px solid #0e0e0d; border-radius: 8px; font-weight: 700; font-size: 8pt;")
            self.seg_bt.setStyleSheet("background-color: #00c2cb; color: #ffffff; border: 1.5px solid #0e0e0d; border-radius: 8px; font-weight: 900; font-size: 8pt;")
        self._update_wireless_buttons()

    def _update_wireless_buttons(self):
        # Wi-Fi top tab style
        w_bg = "#244638" if self.wifi_state else "#f5f4f0"
        w_col = "#ffffff" if self.wifi_state else "#716f64"
        w_txt = f"Wi-Fi\n{self.connected_ssid[:15]}..." if self.wifi_state and self.connected_ssid else ("Wi-Fi\nON" if self.wifi_state else "Wi-Fi\nOFF")
        self.btn_wifi_tab.setText(w_txt)
        self.btn_wifi_tab.setStyleSheet(f"""
            QPushButton {{
                background-color: {w_bg};
                color: {w_col};
                border: 2px solid #0e0e0d;
                border-radius: 12px;
                font-family: Helvetica;
                font-weight: 900;
                font-size: 8.5pt;
                text-align: center;
            }}
        """)
        
        # Wi-Fi toggle in card
        self.wifi_toggle_btn.setText("ON" if self.wifi_state else "OFF")
        self.wifi_toggle_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {'#244638' if self.wifi_state else '#e5e5e0'};
                color: {'#ffffff' if self.wifi_state else '#888880'};
                border: 1.5px solid #0e0e0d;
                border-radius: 11px;
                font-weight: 900;
                font-size: 8pt;
            }}
        """)
        self.wifi_conn_card.setVisible(self.wifi_state and bool(self.connected_ssid))
        self.wifi_list.setEnabled(self.wifi_state)
        self.btn_connect_wifi.setEnabled(self.wifi_state)
        self.btn_scan_wifi.setEnabled(self.wifi_state)
        
        # Bluetooth top tab style
        b_bg = "#00c2cb" if self.bt_state else "#f5f4f0"
        b_col = "#ffffff" if self.bt_state else "#716f64"
        b_txt = f"Bluetooth\n{len(self.connected_bt)} Connected" if self.bt_state and self.connected_bt else ("Bluetooth\nON" if self.bt_state else "Bluetooth\nOFF")
        self.btn_bt_tab.setText(b_txt)
        self.btn_bt_tab.setStyleSheet(f"""
            QPushButton {{
                background-color: {b_bg};
                color: {b_col};
                border: 2px solid #0e0e0d;
                border-radius: 12px;
                font-family: Helvetica;
                font-weight: 900;
                font-size: 8.5pt;
                text-align: center;
            }}
        """)
        
        # Bluetooth toggle in card
        self.bt_toggle_btn.setText("ON" if self.bt_state else "OFF")
        self.bt_toggle_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {'#00c2cb' if self.bt_state else '#e5e5e0'};
                color: {'#ffffff' if self.bt_state else '#888880'};
                border: 1.5px solid #0e0e0d;
                border-radius: 11px;
                font-weight: 900;
                font-size: 8pt;
            }}
        """)
        self.bt_conn_card.setVisible(self.bt_state and bool(self.connected_bt))
        self.bt_list.setEnabled(self.bt_state)
        self.btn_pair_bt.setEnabled(self.bt_state)
        self.btn_scan_bt.setEnabled(self.bt_state)

    def update_wifi_ui(self):
        self.wifi_list.clear()
        for ssid, sig in self.wifi_networks:
            item = QListWidgetItem(f"• {ssid}  ({sig})")
            item.setData(Qt.ItemDataRole.UserRole if PYQT6 else Qt.UserRole, ssid)
            self.wifi_list.addItem(item)
            
    def update_bt_ui(self):
        self.bt_list.clear()
        for dname, st in self.bt_devices:
            item = QListWidgetItem(f"• {dname}  [{st}]")
            item.setData(Qt.ItemDataRole.UserRole if PYQT6 else Qt.UserRole, dname)
            self.bt_list.addItem(item)

    def populate_default_connections(self):
        if not self.wifi_networks:
            self.wifi_networks = [
                ("TinkerHub-Guest", "85%"),
                ("Campus-Makerspace", "75%"),
                ("Overthinkers-Wi-Fi", "60%"),
                ("CoffeeShop_Free_5G", "45%"),
                ("Library-Quiet-Zone", "30%")
            ]
        self.update_wifi_ui()
            
        if not self.bt_devices:
            self.bt_devices = [
                ("Overthinking ANC Headphones", "Discovered"),
                ("Bluetooth Precision Mouse", "Paired"),
                ("Pixel Buds Pro", "Discovered"),
                ("Mechanical Keyboard", "Paired")
            ]
        self.update_bt_ui()

    def connect_selected_wifi(self):
        sel = self.wifi_list.currentItem()
        if sel:
            ssid = sel.data(Qt.ItemDataRole.UserRole if PYQT6 else Qt.UserRole)
            if ssid:
                self.connected_ssid = ssid
                self.wifi_conn_lbl.setText(f"● {ssid}")
                self._update_wireless_buttons()
                try:
                    subprocess.Popen(["nmcli", "dev", "wifi", "connect", ssid], stderr=subprocess.DEVNULL)
                except Exception:
                    pass

    def disconnect_wifi(self):
        self.connected_ssid = ""
        self._update_wireless_buttons()

    def refresh_wifi_networks(self):
        real_nets = []
        # Query real Wi-Fi networks via nmcli
        try:
            out = safe_check_output(["nmcli", "-t", "-f", "SSID,SIGNAL", "dev", "wifi", "list"], timeout=1.0)
            for line in out.splitlines():
                if ":" in line:
                    s, sig = line.split(":", 1)
                    s = s.strip()
                    if s and (s, f"{sig}%") not in real_nets:
                        real_nets.append((s, f"{sig}%"))
        except Exception:
            pass
            
        # Detect active default route
        try:
            route_out = safe_check_output(["ip", "route", "show", "default"], timeout=0.5)
            if "dev " in route_out:
                dev = route_out.split("dev ")[1].split()[0]
                if not self.connected_ssid:
                    if dev.startswith("wl"):
                        ssid_out = safe_check_output(["iwgetid", "-r"], timeout=0.5).strip()
                        self.connected_ssid = ssid_out if ssid_out else f"Wi-Fi ({dev})"
                    else:
                        self.connected_ssid = f"Wired ({dev})"
                    self.wifi_conn_lbl.setText(f"● {self.connected_ssid}")
        except Exception:
            pass

        if real_nets:
            self.wifi_networks = real_nets
        else:
            self.wifi_networks = [
                ("TinkerHub-Guest", "85%"),
                ("Campus-Makerspace", "75%"),
                ("Overthinkers-Wi-Fi", "60%"),
                ("CoffeeShop_Free_5G", "45%"),
                ("Library-Quiet-Zone", "30%")
            ]
        self.update_wifi_ui()
        self._update_wireless_buttons()

    def connect_selected_bt(self):
        sel = self.bt_list.currentItem()
        if sel:
            dname = sel.data(Qt.ItemDataRole.UserRole if PYQT6 else Qt.UserRole)
            if dname:
                if dname not in self.connected_bt:
                    self.connected_bt.append(dname)
                self.bt_conn_lbl.setText(f"● {dname} (Connected)")
                self._update_wireless_buttons()

    def disconnect_bt(self):
        if self.connected_bt:
            self.connected_bt.pop(0)
        self.bt_conn_lbl.setText(f"● {self.connected_bt[0]}" if self.connected_bt else "No Devices Connected")
        self._update_wireless_buttons()

    def refresh_bt_devices(self):
        real_devs = []
        try:
            out = safe_check_output(["bluetoothctl", "devices"], timeout=0.5)
            for line in out.splitlines():
                parts = line.split()
                if len(parts) >= 3:
                    real_devs.append((" ".join(parts[2:]), "Paired"))
        except Exception:
            pass
            
        if real_devs:
            self.bt_devices = real_devs
        else:
            self.bt_devices = [
                ("Overthinking ANC Headphones", "Discovered"),
                ("Bluetooth Precision Mouse", "Paired"),
                ("Pixel Buds Pro", "Discovered"),
                ("Mechanical Keyboard", "Paired")
            ]
        self.update_bt_ui()
        self._update_wireless_buttons()

    def action_shutdown(self):
        try:
            subprocess.Popen(["sudo", "poweroff"])
        except Exception:
            os.system("systemctl poweroff || sudo poweroff")

    def action_restart(self):
        try:
            subprocess.Popen(["sudo", "reboot"])
        except Exception:
            os.system("systemctl reboot || sudo reboot")

    def toggle_wifi(self):
        self.wifi_state = not self.wifi_state
        self._update_wireless_buttons()
        try:
            state_arg = "on" if self.wifi_state else "off"
            subprocess.Popen(["nmcli", "radio", "wifi", state_arg], stderr=subprocess.DEVNULL)
            subprocess.Popen(["sudo", "rfkill", "unblock" if self.wifi_state else "block", "wifi"], stderr=subprocess.DEVNULL)
        except Exception:
            pass

    def toggle_bluetooth(self):
        self.bt_state = not self.bt_state
        self._update_wireless_buttons()
        try:
            state_arg = "on" if self.bt_state else "off"
            subprocess.Popen(["bluetoothctl", "power", state_arg], stderr=subprocess.DEVNULL)
            subprocess.Popen(["sudo", "rfkill", "unblock" if self.bt_state else "block", "bluetooth"], stderr=subprocess.DEVNULL)
        except Exception:
            pass

    def on_volume_changed(self, val):
        self.sound_lbl.setText(f"Sound Volume: {val}%")
        try:
            subprocess.Popen(["pactl", "set-sink-volume", "@DEFAULT_SINK@", f"{val}%"], stderr=subprocess.DEVNULL)
            subprocess.Popen(["amixer", "set", "Master", f"{val}%"], stderr=subprocess.DEVNULL)
        except Exception:
            pass

    def on_brightness_changed(self, val):
        self.bright_lbl.setText(f"Display Brightness: {val}%")
        b = max(0.2, min(1.0, val / 100.0))
        disp = self.get_display_name()
        env = os.environ.copy()
        env["DISPLAY"] = os.environ.get("DISPLAY", ":0")
        try:
            subprocess.Popen(["xrandr", "--output", disp, "--brightness", f"{b:.2f}"], env=env, stderr=subprocess.DEVNULL)
        except Exception:
            pass

    def get_display_name(self):
        try:
            env = os.environ.copy()
            env["DISPLAY"] = os.environ.get("DISPLAY", ":0")
            out = safe_check_output(["xrandr", "--current"], env=env, timeout=0.5)
            for line in out.splitlines():
                if " connected" in line:
                    return line.split()[0]
        except Exception:
            pass
        return "Virtual1"

    def get_current_volume(self):
        try:
            out = safe_check_output(["pactl", "get-sink-volume", "@DEFAULT_SINK@"], timeout=0.5)
            import re
            m = re.search(r'(\d+)%', out)
            if m:
                return int(m.group(1))
        except Exception:
            pass
        return 80

    def init_hardware_states(self):
        try:
            out = safe_check_output(["rfkill", "list", "wifi"], timeout=0.5)
            if "Soft blocked: yes" in out or "Hard blocked: yes" in out:
                self.wifi_state = False
            else:
                self.wifi_state = True
        except Exception:
            pass
            
        try:
            out = safe_check_output(["rfkill", "list", "bluetooth"], timeout=0.5)
            if "Soft blocked: yes" in out or "Hard blocked: yes" in out:
                self.bt_state = False
            else:
                self.bt_state = True
        except Exception:
            pass
            
        # Detect active default route
        try:
            route_out = safe_check_output(["ip", "route", "show", "default"], timeout=0.5)
            if "dev " in route_out:
                dev = route_out.split("dev ")[1].split()[0]
                if dev.startswith("wl"):
                    ssid_out = safe_check_output(["iwgetid", "-r"], timeout=0.5).strip()
                    self.connected_ssid = ssid_out if ssid_out else f"Wi-Fi ({dev})"
                else:
                    self.connected_ssid = f"Wired ({dev})"
                self.wifi_conn_lbl.setText(f"● {self.connected_ssid}")
        except Exception:
            pass
            
        self._update_wireless_buttons()
        # Defer background network and bluetooth scans so window displays immediately
        QTimer.singleShot(800, self.refresh_wifi_networks)
        QTimer.singleShot(1200, self.refresh_bt_devices)




class LaunchpadDrawer(QFrame):
    """
    macOS Launchpad-style App Drawer in TinkerHub brutalist theme.
    Expansive overlay with live search filtering across all 10 apps and rich cards.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 0.98);
                border: 3px solid #0e0e0d;
                border-radius: 26px;
            }
        """)
        
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(28, 24, 28, 24)
        self.layout.setSpacing(16)
        
        # Header with Search Bar and Close button
        h_box = QHBoxLayout()
        title = QLabel("USELESS APPLICATIONS LAUNCHPAD")
        title.setStyleSheet("font-family: Helvetica; font-size: 15pt; font-weight: 900; color: #0e0e0d; border: none;")
        h_box.addWidget(title)
        h_box.addStretch()
        
        close_btn = QPushButton("✕")
        close_btn.setFixedSize(32, 32)
        close_btn.setCursor(QCursor(PointingHandCursor))
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #0e0e0d;
                color: #ffffff;
                border-radius: 16px;
                font-weight: 900;
                font-size: 11pt;
                border: none;
            }
            QPushButton:hover {
                background-color: #e82803;
            }
        """)
        close_btn.clicked.connect(self.hide)
        h_box.addWidget(close_btn)
        self.layout.addLayout(h_box)
        
        # Live Search Input Bar
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search 10 useless applications (e.g. excuse, dread, terminal)...")
        self.search_input.setStyleSheet("""
            QLineEdit {
                background-color: #f5f4f0;
                color: #0e0e0d;
                border: 2px solid #0e0e0d;
                border-radius: 14px;
                padding: 10px 18px;
                font-family: Helvetica;
                font-size: 11pt;
                font-weight: 600;
            }
            QLineEdit:focus {
                border: 2px solid #ea34df;
                background-color: #ffffff;
            }
        """)
        self.search_input.textChanged.connect(self.filter_apps)
        # Scrollable Grid Container
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.Shape.NoFrame if PYQT6 else QFrame.NoFrame)
        self.scroll_area.setStyleSheet("""
            QScrollArea {
                background: transparent;
                border: none;
            }
            QScrollBar:vertical {
                border: 1.5px solid #0e0e0d;
                background: #f5f4f0;
                width: 10px;
                border-radius: 5px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #0e0e0d;
                border-radius: 3px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: #ea34df;
            }
        """)
        
        self.grid_widget = QWidget()
        self.grid_widget.setStyleSheet("background: transparent; border: none;")
        self.grid = QGridLayout(self.grid_widget)
        self.grid.setSpacing(12)
        self.grid.setContentsMargins(0, 4, 8, 4)
        self.scroll_area.setWidget(self.grid_widget)
        self.layout.addWidget(self.scroll_area)
        
        self.app_cards = []
        self._populate_grid()
        
    def _populate_grid(self):
        for idx, (name, script, icon_name, color, desc) in enumerate(APPS_DATA):
            card = QPushButton()
            card.setCursor(QCursor(PointingHandCursor))
            card.setFixedHeight(68)
            
            card_layout = QHBoxLayout(card)
            card_layout.setContentsMargins(12, 6, 12, 6)
            card_layout.setSpacing(14)
            
            # Icon
            icon_lbl = QLabel()
            icon_path = get_icon_path(icon_name)
            if icon_path and os.path.exists(icon_path):
                pix = QPixmap(icon_path).scaled(48, 48, Qt.AspectRatioMode.KeepAspectRatio if PYQT6 else Qt.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation if PYQT6 else Qt.SmoothTransformation)
                icon_lbl.setPixmap(pix)
            icon_lbl.setFixedSize(48, 48)
            icon_lbl.setStyleSheet("background: transparent; border: none;")
            card_layout.addWidget(icon_lbl)
            
            # Text block
            v_text = QVBoxLayout()
            v_text.setSpacing(2)
            title_lbl = QLabel(name)
            title_lbl.setStyleSheet("font-family: Helvetica; font-size: 11pt; font-weight: 900; color: #0e0e0d; border: none; background: transparent;")
            desc_lbl = QLabel(desc)
            desc_lbl.setStyleSheet("font-size: 8.5pt; font-weight: 600; color: #716f64; border: none; background: transparent;")
            v_text.addWidget(title_lbl)
            v_text.addWidget(desc_lbl)
            card_layout.addLayout(v_text)
            card_layout.addStretch()
            card.setToolTip(f"""
                <div style='background-color: #ffffff; color: #0e0e0d; padding: 2px;'>
                    <b style='font-size: 10.5pt; color: #0e0e0d;'>{name}</b><br/>
                    <span style='color: {color}; font-weight: 800; font-size: 8pt;'>● USELESS PROJECTS 3.0</span><br/>
                    <span style='color: #555550; font-size: 8.5pt;'>{desc}</span>
                </div>
            """)
            
            card.setStyleSheet(f"""
                QPushButton {{
                    background-color: #ffffff;
                    border: 2px solid #0e0e0d;
                    border-radius: 16px;
                    text-align: left;
                }}
                QPushButton:hover {{
                    background-color: #f5f4f0;
                    border: 3px solid {color};
                }}
            """)
            card.clicked.connect(lambda checked, s=script: self.launch_and_close(s))
            
            self.app_cards.append((card, name, desc, idx))
            row = idx // 2
            col = idx % 2
            self.grid.addWidget(card, row, col)
            
    def filter_apps(self, query):
        query = query.strip().lower()
        visible_idx = 0
        for card, name, desc, idx in self.app_cards:
            match = query in name.lower() or query in desc.lower()
            card.setVisible(match)
            if match:
                self.grid.removeWidget(card)
                row = visible_idx // 2
                col = visible_idx % 2
                self.grid.addWidget(card, row, col)
                visible_idx += 1
                
    def launch_and_close(self, script):
        launch_app(script)
        self.hide()


class TopBar(QFrame):
    """macOS-style top bar with menus, Useless status, Control Center, and clock."""
    def __init__(self, parent=None, shell=None):
        super().__init__(parent)
        self.shell = shell
        self.setObjectName("TopBarFrame")
        self.setFixedHeight(44)
        self.setStyleSheet("""
            #TopBarFrame {
                background-color: rgba(255, 255, 255, 0.98);
                border-bottom: 2px solid #0e0e0d;
            }
        """)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 0, 12, 0)
        layout.setSpacing(6)
        layout.setAlignment(Qt.AlignmentFlag.AlignVCenter if PYQT6 else Qt.AlignVCenter)
        
        # Mascot button (macOS Apple System Menu)
        logo_btn = QPushButton()
        logo_btn.setCursor(QCursor(PointingHandCursor))
        mascot_icon_path = get_icon_path("mascot.png")
        if mascot_icon_path and os.path.exists(mascot_icon_path):
            logo_btn.setIcon(QIcon(mascot_icon_path))
            logo_btn.setIconSize(QSize(22, 22))
        logo_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                padding: 2px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background: #f5f4f0;
                border: 1px solid #0e0e0d;
            }
            QPushButton::menu-indicator {
                image: none;
                width: 0px;
            }
        """)
        
        # macOS Apple-Style System Menu
        self.apple_menu = QMenu(self)
        self.apple_menu.setStyleSheet(self._menu_dropdown_style())
        
        act_about = QAction("About UselessOS 3.0", self)
        act_about.triggered.connect(self.show_about_dialog)
        self.apple_menu.addAction(act_about)
        
        self.apple_menu.addSeparator()
        
        act_settings = QAction("System Settings...", self)
        act_settings.triggered.connect(lambda: launch_app("useless_settings.py"))
        self.apple_menu.addAction(act_settings)
        
        act_launchpad = QAction("Launchpad / App Drawer", self)
        act_launchpad.triggered.connect(lambda: self.shell.toggle_launchpad() if self.shell else None)
        self.apple_menu.addAction(act_launchpad)
        
        act_force_quit = QAction("Force Quit Applications...", self)
        act_force_quit.triggered.connect(self.show_force_quit_dialog)
        self.apple_menu.addAction(act_force_quit)
        
        self.apple_menu.addSeparator()
        
        act_sleep = QAction("Sleep / Screen Lock", self)
        act_sleep.triggered.connect(self.action_sleep)
        self.apple_menu.addAction(act_sleep)
        
        act_restart = QAction("Restart...", self)
        act_restart.triggered.connect(self.action_restart_prompt)
        self.apple_menu.addAction(act_restart)
        
        act_shutdown = QAction("Shut Down...", self)
        act_shutdown.triggered.connect(self.action_shutdown_prompt)
        self.apple_menu.addAction(act_shutdown)
        
        self.apple_menu.addSeparator()
        
        act_logout = QAction("Log Out vagrant...", self)
        act_logout.triggered.connect(self.action_logout_prompt)
        self.apple_menu.addAction(act_logout)
        
        logo_btn.setMenu(self.apple_menu)
        layout.addWidget(logo_btn)
        
        # OS Title (Explicit transparent background so it never paints over border)
        os_lbl = QLabel("UselessOS 3.0")
        os_lbl.setStyleSheet("font-weight: 900; font-family: Helvetica; font-size: 11pt; color: #0e0e0d; background: transparent; border: none;")
        layout.addWidget(os_lbl)
        
        # Applications Menu directly in top bar
        apps_btn = QPushButton("Apps")
        apps_btn.setCursor(QCursor(PointingHandCursor))
        apps_btn.setStyleSheet(self._menu_btn_style())
        apps_menu = QMenu(self)
        apps_menu.setStyleSheet(self._menu_dropdown_style())
        for name, script, icon_name, color, desc in APPS_DATA:
            act = QAction(f"{name} — {desc}", self)
            icon_path = get_icon_path(icon_name)
            if icon_path and os.path.exists(icon_path):
                act.setIcon(QIcon(icon_path))
            act.triggered.connect(lambda checked, s=script: launch_app(s))
            apps_menu.addAction(act)
        apps_btn.setMenu(apps_menu)
        layout.addWidget(apps_btn)
        
        # Standard Menus
        system_menus = [
            ("File", ["New Procrastination Session", "Save Nothing", "Exit to Reality (Access Denied)"]),
            ("Edit", ["Undo Regret", "Redo Mistake", "Cut Corners", "Copy Fake Work"]),
            ("Overthink", ["Simulate 3 AM Panic", "Analyze Hypothetical Worst Case", "Ruminate on 2017 Conversation"]),
            ("Curiosity", ["Why Does This OS Exist?", "Calibrate Sarcasm Matrix", "Test Impracticality Limit"]),
            ("Help", ["No Help Available", "Submit Complaint to /dev/null", "Embrace The Absurdity"])
        ]
        
        for menu_title, actions in system_menus:
            btn = QPushButton(menu_title)
            btn.setCursor(QCursor(PointingHandCursor))
            btn.setStyleSheet(self._menu_btn_style())
            menu = QMenu(self)
            menu.setStyleSheet(self._menu_dropdown_style())
            for a in actions:
                act = QAction(a, self)
                act.triggered.connect(lambda checked, text=a: self.handle_menu_action(text))
                menu.addAction(act)
            btn.setMenu(menu)
            layout.addWidget(btn)
            
        layout.addStretch()
        
        # Impracticality Status Indicator (Brutalist Useless Projects Pill Badge)
        status_lbl = QLabel()
        status_lbl.setText("<span style='color: #00ff66;'>●</span> <span style='color: #ffffff;'>Impracticality: 100% (Nominal)</span>")
        status_lbl.setFixedHeight(26)
        status_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter if PYQT6 else Qt.AlignCenter)
        status_lbl.setStyleSheet("""
            QLabel {
                background-color: #244638;
                font-weight: 800;
                font-family: Helvetica;
                font-size: 9pt;
                padding-left: 14px;
                padding-right: 14px;
                border-radius: 13px;
                border: 2px solid #0e0e0d;
            }
        """)
        layout.addWidget(status_lbl)
        
        # Control Center Button
        self.cc_btn = QPushButton("Control Center")
        self.cc_btn.setCursor(QCursor(PointingHandCursor))
        self.cc_btn.setFixedHeight(28)
        cc_icon_path = get_icon_path("control_center.png")
        if cc_icon_path and os.path.exists(cc_icon_path):
            self.cc_btn.setIcon(QIcon(cc_icon_path))
            self.cc_btn.setIconSize(QSize(18, 18))
        self.cc_btn.setStyleSheet("""
            QPushButton {
                background-color: #f5f4f0;
                color: #0e0e0d;
                font-weight: 800;
                font-family: Helvetica;
                font-size: 9pt;
                padding: 3px 12px;
                border: 2px solid #0e0e0d;
                border-radius: 14px;
            }
            QPushButton:hover {
                background-color: #ea34df;
                color: #ffffff;
            }
        """)
        self.cc_btn.clicked.connect(self.toggle_control_center)
        layout.addWidget(self.cc_btn)
        
        # Real-time Clock (Explicit transparent background)
        self.clock_lbl = QLabel()
        self.clock_lbl.setStyleSheet("font-weight: 900; font-family: Helvetica; font-size: 11pt; color: #0e0e0d; background: transparent; border: none;")
        layout.addWidget(self.clock_lbl)
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_clock)
        self.timer.start(1000)
        self.update_clock()
        
    def _menu_btn_style(self):
        arrow_path = get_asset_path("menu_arrow.svg")
        arrow_url = arrow_path.replace("\\", "/") if arrow_path else ""
        return f"""
            QPushButton {{
                background: transparent;
                border: none;
                font-weight: 800;
                font-family: Helvetica;
                font-size: 10pt;
                color: #0e0e0d;
                padding-top: 4px;
                padding-bottom: 4px;
                padding-left: 8px;
                padding-right: 20px;
            }}
            QPushButton:hover {{
                background: #f5f4f0;
                border: 1px solid #0e0e0d;
                border-radius: 6px;
            }}
            QPushButton::menu-indicator {{
                subcontrol-origin: padding;
                subcontrol-position: center right;
                right: 6px;
                width: 8px;
                height: 5px;
                image: url("{arrow_url}");
            }}
        """
        
    def _menu_dropdown_style(self):
        return """
            QMenu {
                background-color: #ffffff;
                border: 2px solid #0e0e0d;
                border-radius: 8px;
                padding: 6px;
                font-family: Helvetica;
                font-weight: 600;
            }
            QMenu::item {
                padding: 8px 24px;
                border-radius: 6px;
                color: #0e0e0d;
            }
            QMenu::item:selected {
                background-color: #ea34df;
                color: #ffffff;
            }
        """
        
    def update_clock(self):
        self.clock_lbl.setText(QTime.currentTime().toString("hh:mm A"))
        
    def toggle_control_center(self):
        if self.shell:
            self.shell.toggle_control_center()

    def show_about_dialog(self):
        dlg = QDialog(self)
        dlg.setWindowTitle("About UselessOS & Useless Projects 3.0")
        dlg.setFixedSize(500, 570)
        dlg.setWindowFlags((Qt.WindowType.Dialog if PYQT6 else Qt.Dialog) | (Qt.WindowType.FramelessWindowHint if PYQT6 else Qt.FramelessWindowHint))
        dlg.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground if PYQT6 else Qt.WA_TranslucentBackground)
        if hasattr(Qt, 'WindowModality') and hasattr(Qt.WindowModality, 'ApplicationModal'):
            dlg.setWindowModality(Qt.WindowModality.ApplicationModal)
        elif hasattr(Qt, 'ApplicationModal'):
            dlg.setWindowModality(Qt.ApplicationModal)

        frame = QFrame(dlg)
        frame.setObjectName("AboutModalFrame")
        frame.setStyleSheet("""
            QFrame#AboutModalFrame {
                background-color: #ffffff;
                border: 2.5px solid #0e0e0d;
                border-radius: 20px;
            }
        """)
        f_lay = QVBoxLayout(frame)
        f_lay.setContentsMargins(24, 20, 24, 20)
        f_lay.setSpacing(10)
        
        # Mascot icon
        m_lbl = QLabel()
        m_path = get_icon_path("mascot.png")
        if m_path and os.path.exists(m_path):
            pix = QPixmap(m_path).scaled(56, 56, Qt.AspectRatioMode.KeepAspectRatio if PYQT6 else Qt.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation if PYQT6 else Qt.SmoothTransformation)
            m_lbl.setPixmap(pix)
        m_lbl.setAlignment(AlignCenter)
        m_lbl.setStyleSheet("background: transparent; border: none;")
        f_lay.addWidget(m_lbl)
        
        # Title
        t_lbl = QLabel("Useless Projects 3.0")
        t_lbl.setStyleSheet("font-family: 'Drowner', 'Helvetica', sans-serif; font-size: 20pt; font-weight: 900; color: #0e0e0d; background: transparent; border: none;")
        t_lbl.setAlignment(AlignCenter)
        f_lay.addWidget(t_lbl)
        
        # Tagline
        sub_lbl = QLabel("exclusive to TinkerHub campus community <3")
        sub_lbl.setStyleSheet("font-family: 'NanumPenScript', cursive; font-size: 13pt; color: #e82803; background: transparent; border: none;")
        sub_lbl.setAlignment(AlignCenter)
        f_lay.addWidget(sub_lbl)
        
        # 1. Developer Credits Card
        dev_card = QWidget()
        dev_card.setStyleSheet("background-color: #f5f4f0; border: 2px solid #0e0e0d; border-radius: 12px; padding: 6px 10px;")
        d_lay = QVBoxLayout(dev_card)
        d_lay.setSpacing(4)
        
        dev_hdr = QLabel("CORE ARCHITECTS & DEVELOPERS")
        dev_hdr.setStyleSheet("font-size: 8pt; font-weight: 900; color: #716f64; font-family: Helvetica; border: none; background: transparent;")
        d_lay.addWidget(dev_hdr)
        
        # Edwin Joseph
        d1 = QVBoxLayout()
        d1.setSpacing(1)
        r1_name = QLabel("Edwin Joseph")
        r1_name.setStyleSheet("font-weight: 900; font-family: Helvetica; font-size: 10pt; color: #0e0e0d; border: none; background: transparent;")
        r1_role = QLabel("Lead Creator & Visionary Architect")
        r1_role.setStyleSheet("font-weight: 700; font-family: Helvetica; font-size: 8.5pt; color: #ea34df; border: none; background: transparent;")
        d1.addWidget(r1_name)
        d1.addWidget(r1_role)
        d_lay.addLayout(d1)
        
        d_lay.addSpacing(6)
        
        # Antigravity (Google DeepMind)
        d2 = QVBoxLayout()
        d2.setSpacing(1)
        r2_name = QLabel("Antigravity (Google DeepMind)")
        r2_name.setStyleSheet("font-weight: 900; font-family: Helvetica; font-size: 10pt; color: #0e0e0d; border: none; background: transparent;")
        r2_role = QLabel("AI Systems Pair Programmer & Core Engineer")
        r2_role.setStyleSheet("font-weight: 700; font-family: Helvetica; font-size: 8.5pt; color: #00c2cb; border: none; background: transparent;")
        d2.addWidget(r2_name)
        d2.addWidget(r2_role)
        d_lay.addLayout(d2)
        f_lay.addWidget(dev_card)
        
        # 2. System Specs Card
        card = QWidget()
        card.setStyleSheet("background-color: #ffffff; border: 2px solid #0e0e0d; border-radius: 12px; padding: 6px 10px;")
        c_lay = QVBoxLayout(card)
        c_lay.setSpacing(4)
        
        specs = [
            ("Base OS:", "UselessOS 3.0 (Debian Bookworm x86_64)"),
            ("Cognitive Engine:", "Qwen 3.5 (0.8B Instruct)"),
            ("Desktop Environment:", "Native PyQt6 on Openbox + Picom"),
            ("Impracticality Index:", "100% Certified Nominal")
        ]
        for k, v in specs:
            h = QHBoxLayout()
            kl = QLabel(k)
            kl.setStyleSheet("font-weight: 700; font-family: Helvetica; font-size: 8.5pt; border: none; background: transparent;")
            vl = QLabel(v)
            vl.setStyleSheet("font-weight: 900; font-family: Helvetica; font-size: 8.5pt; color: #244638; border: none; background: transparent;")
            h.addWidget(kl)
            h.addStretch()
            h.addWidget(vl)
            c_lay.addLayout(h)
        f_lay.addWidget(card)
        
        f_lay.addStretch()

        btn = QPushButton("Acknowledge Uselessness (Close)")
        btn.setCursor(QCursor(PointingHandCursor))
        btn.setFixedHeight(38)
        btn.setStyleSheet("""
            QPushButton {
                background-color: #0e0e0d;
                color: #ffffff;
                border: 2px solid #0e0e0d;
                border-radius: 19px;
                font-family: Helvetica;
                font-weight: 800;
                font-size: 9.5pt;
            }
            QPushButton:hover {
                background-color: #ea34df;
            }
        """)
        btn.clicked.connect(dlg.accept)
        f_lay.addWidget(btn)

        main_lay = QVBoxLayout(dlg)
        main_lay.setContentsMargins(0, 0, 0, 0)
        main_lay.addWidget(frame)

        # Center on screen
        screen = QApplication.primaryScreen()
        if screen:
            s_geo = screen.availableGeometry()
            dlg.move(s_geo.x() + (s_geo.width() - 500) // 2, s_geo.y() + max(44, (s_geo.height() - 570) // 2))

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

        frame.mousePressEvent = mouse_press
        frame.mouseMoveEvent = mouse_move
        frame.mouseReleaseEvent = mouse_release
        
        dlg.exec()

    def show_force_quit_dialog(self):
        dlg = QDialog(self)
        dlg.setWindowTitle("Force Quit Applications")
        dlg.setFixedSize(420, 380)
        dlg.setWindowFlags((Qt.WindowType.Dialog if PYQT6 else Qt.Dialog) | (Qt.WindowType.FramelessWindowHint if PYQT6 else Qt.FramelessWindowHint))
        dlg.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground if PYQT6 else Qt.WA_TranslucentBackground)
        if hasattr(Qt, 'WindowModality') and hasattr(Qt.WindowModality, 'ApplicationModal'):
            dlg.setWindowModality(Qt.WindowModality.ApplicationModal)
        elif hasattr(Qt, 'ApplicationModal'):
            dlg.setWindowModality(Qt.ApplicationModal)
        
        frame = QFrame(dlg)
        frame.setObjectName("ForceQuitModalFrame")
        frame.setStyleSheet("""
            QFrame#ForceQuitModalFrame {
                background-color: #ffffff;
                border: 2.5px solid #0e0e0d;
                border-radius: 20px;
            }
        """)
        f_lay = QVBoxLayout(frame)
        f_lay.setContentsMargins(20, 18, 20, 20)
        f_lay.setSpacing(10)
        
        t_lbl = QLabel("Force Quit Applications")
        t_lbl.setStyleSheet("font-family: Helvetica; font-size: 13pt; font-weight: 900; color: #0e0e0d; border: none; background: transparent;")
        f_lay.addWidget(t_lbl)
        
        sub = QLabel("If an application is unresponsive or needlessly useful, select it and force quit.")
        sub.setStyleSheet("font-size: 8.5pt; color: #716f64; border: none; background: transparent;")
        sub.setWordWrap(True)
        f_lay.addWidget(sub)
        
        app_list = QListWidget()
        app_list.setStyleSheet("""
            QListWidget {
                background-color: #f5f4f0;
                border: 2px solid #0e0e0d;
                border-radius: 10px;
                padding: 4px;
            }
            QListWidget::item {
                padding: 6px 8px;
                border-radius: 6px;
            }
            QListWidget::item:selected {
                background-color: #e82803;
                color: #ffffff;
            }
        """)
        
        # Discover running apps
        try:
            out = safe_check_output(["wmctrl", "-l", "-p", "-x"], timeout=0.5)
            for line in out.splitlines():
                parts = line.split()
                if len(parts) >= 5:
                    pid = parts[2]
                    cls = parts[3]
                    title = " ".join(parts[4:])
                    if ("useless" in cls.lower() or "overthinking" in cls.lower() or "excuse" in cls.lower() or "screen" in cls.lower() or "emotional" in cls.lower() or "existential" in cls.lower() or "alarm" in cls.lower()) and "useless_shell" not in cls.lower():
                        item = QListWidgetItem(f"⚡ {title} (PID {pid})")
                        item.setData(Qt.ItemDataRole.UserRole if PYQT6 else Qt.UserRole, pid)
                        app_list.addItem(item)
        except Exception:
            pass
            
        if app_list.count() == 0:
            item = QListWidgetItem("No running child applications detected")
            item.setFlags(item.flags() & ~(Qt.ItemFlag.ItemIsEnabled if PYQT6 else Qt.ItemIsEnabled))
            app_list.addItem(item)
            
        f_lay.addWidget(app_list)
        
        b_box = QHBoxLayout()
        b_cancel = QPushButton("Cancel")
        b_cancel.setFixedHeight(34)
        b_cancel.setStyleSheet("""
            QPushButton {
                background-color: #ffffff;
                color: #0e0e0d;
                border: 2px solid #0e0e0d;
                border-radius: 14px;
                font-weight: 800;
            }
            QPushButton:hover {
                background-color: #f5f4f0;
            }
        """)
        b_cancel.clicked.connect(dlg.reject)
        b_box.addWidget(b_cancel)
        
        b_kill = QPushButton("Force Quit")
        b_kill.setFixedHeight(34)
        b_kill.setStyleSheet("""
            QPushButton {
                background-color: #e82803;
                color: #ffffff;
                border: 2px solid #0e0e0d;
                border-radius: 14px;
                font-weight: 800;
            }
            QPushButton:hover {
                background-color: #0e0e0d;
            }
        """)
        def do_kill():
            sel = app_list.currentItem()
            if sel:
                pid = sel.data(Qt.ItemDataRole.UserRole if PYQT6 else Qt.UserRole)
                if pid:
                    subprocess.Popen(["kill", "-9", str(pid)])
            dlg.accept()
        b_kill.clicked.connect(do_kill)
        b_box.addWidget(b_kill)
        f_lay.addLayout(b_box)
        
        main_lay = QVBoxLayout(dlg)
        main_lay.setContentsMargins(0, 0, 0, 0)
        main_lay.addWidget(frame)

        screen = QApplication.primaryScreen()
        if screen:
            s_geo = screen.availableGeometry()
            dlg.move(s_geo.x() + (s_geo.width() - 420) // 2, s_geo.y() + max(44, (s_geo.height() - 380) // 2))

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

        frame.mousePressEvent = mouse_press
        frame.mouseMoveEvent = mouse_move
        frame.mouseReleaseEvent = mouse_release

        dlg.exec()

    def action_restart_prompt(self):
        reply = QMessageBox.question(self, "Restart UselessOS", "Are you sure you want to restart your non-productive session?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No if PYQT6 else QMessageBox.Yes | QMessageBox.No)
        if reply == (QMessageBox.StandardButton.Yes if PYQT6 else QMessageBox.Yes):
            subprocess.Popen(["sudo", "reboot"])

    def action_shutdown_prompt(self):
        reply = QMessageBox.question(self, "Shut Down UselessOS", "Are you sure you want to shut down UselessOS?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No if PYQT6 else QMessageBox.Yes | QMessageBox.No)
        if reply == (QMessageBox.StandardButton.Yes if PYQT6 else QMessageBox.Yes):
            subprocess.Popen(["sudo", "poweroff"])

    def action_logout_prompt(self):
        reply = QMessageBox.question(self, "Log Out", "Are you sure you want to log out of vagrant?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No if PYQT6 else QMessageBox.Yes | QMessageBox.No)
        if reply == (QMessageBox.StandardButton.Yes if PYQT6 else QMessageBox.Yes):
            subprocess.Popen(["killall", "-u", "vagrant"])

    def action_sleep(self):
        env = os.environ.copy()
        env["DISPLAY"] = os.environ.get("DISPLAY", ":0")
        subprocess.Popen(["xset", "dpms", "force", "off"], env=env)

    def _create_modal_dialog(self, title, width=460, height=380, accent_color="#ea34df"):
        dlg = QDialog(self)
        dlg.setWindowTitle(title)
        dlg.setFixedSize(width, height)
        dlg.setWindowFlags((Qt.WindowType.Dialog if PYQT6 else Qt.Dialog) | (Qt.WindowType.FramelessWindowHint if PYQT6 else Qt.FramelessWindowHint))
        dlg.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground if PYQT6 else Qt.WA_TranslucentBackground)
        if hasattr(Qt, 'WindowModality') and hasattr(Qt.WindowModality, 'ApplicationModal'):
            dlg.setWindowModality(Qt.WindowModality.ApplicationModal)
        elif hasattr(Qt, 'ApplicationModal'):
            dlg.setWindowModality(Qt.ApplicationModal)

        frame = QFrame(dlg)
        frame.setObjectName("ShellModalFrame")
        frame.setStyleSheet("""
            QFrame#ShellModalFrame {
                background-color: #ffffff;
                border: 2.5px solid #0e0e0d;
                border-radius: 20px;
            }
        """)
        lay = QVBoxLayout(frame)
        lay.setContentsMargins(22, 18, 22, 18)
        lay.setSpacing(10)
        
        hdr = QHBoxLayout()
        t_lbl = QLabel(title)
        t_lbl.setStyleSheet("font-family: Helvetica; font-size: 13pt; font-weight: 900; color: #0e0e0d; border: none; background: transparent;")
        hdr.addWidget(t_lbl)
        hdr.addStretch()
        
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
        c_btn.clicked.connect(dlg.accept)
        hdr.addWidget(c_btn)
        lay.addLayout(hdr)
        
        main_lay = QVBoxLayout(dlg)
        main_lay.setContentsMargins(0, 0, 0, 0)
        main_lay.addWidget(frame)

        screen = QApplication.primaryScreen()
        if screen:
            s_geo = screen.availableGeometry()
            dlg.move(s_geo.x() + (s_geo.width() - width) // 2, s_geo.y() + max(44, (s_geo.height() - height) // 2))

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

        frame.mousePressEvent = mouse_press
        frame.mouseMoveEvent = mouse_move
        frame.mouseReleaseEvent = mouse_release
        
        return dlg, frame, lay

    def handle_menu_action(self, action_text):
        if action_text == "New Procrastination Session":
            self.show_procrastination_session_dialog()
        elif action_text == "Save Nothing":
            self.show_save_nothing_dialog()
        elif action_text == "Exit to Reality (Access Denied)":
            self.show_exit_reality_dialog()
        elif action_text == "Undo Regret":
            self.show_undo_regret_dialog()
        elif action_text == "Redo Mistake":
            self.show_redo_mistake_dialog()
        elif action_text == "Cut Corners":
            self.show_cut_corners_dialog()
        elif action_text == "Copy Fake Work":
            self.action_copy_fake_work()
        elif action_text == "Simulate 3 AM Panic":
            self.show_panic_simulation_dialog()
        elif action_text == "Analyze Hypothetical Worst Case":
            self.show_worst_case_dialog()
        elif action_text == "Ruminate on 2017 Conversation":
            self.show_rumination_dialog()
        elif action_text == "Why Does This OS Exist?":
            self.show_curiosity_exist_dialog()
        elif action_text == "Calibrate Sarcasm Matrix":
            self.show_sarcasm_matrix_dialog()
        elif action_text == "Test Impracticality Limit":
            self.show_impracticality_stress_dialog()
        elif action_text == "No Help Available":
            self.show_no_help_dialog()
        elif action_text == "Submit Complaint to /dev/null":
            self.show_complaint_dialog()
        elif action_text == "Embrace The Absurdity":
            self.show_absurdity_dialog()
        else:
            print(f"[TopBar] Action: {action_text}")

    def show_procrastination_session_dialog(self):
        dlg, frame, lay = self._create_modal_dialog("Procrastination Session 3.0", 460, 360)
        
        badge = QLabel("● SESSION IN PROGRESS: 100% UNPRODUCTIVE")
        badge.setStyleSheet("font-weight: 800; font-size: 8pt; color: #244638; background: #e8f5e9; border: 1.5px solid #244638; border-radius: 8px; padding: 4px 8px;")
        lay.addWidget(badge)
        
        timer_lbl = QLabel("Time Successfully Wasted: 00:00")
        timer_lbl.setStyleSheet("font-family: Helvetica; font-size: 14pt; font-weight: 900; color: #0e0e0d; background: transparent; border: none;")
        lay.addWidget(timer_lbl)
        
        seconds = [0]
        t = QTimer(dlg)
        def tick():
            seconds[0] += 1
            m = seconds[0] // 60
            s = seconds[0] % 60
            timer_lbl.setText(f"Time Successfully Wasted: {m:02d}:{s:02d}")
        t.timeout.connect(tick)
        t.start(1000)
        
        quote = QLabel("“Hard work pays off in the future, but procrastination pays off right now.”")
        quote.setStyleSheet("font-style: italic; font-size: 9pt; color: #716f64; background: transparent; border: none;")
        quote.setWordWrap(True)
        lay.addWidget(quote)
        
        pbar = QProgressBar()
        pbar.setRange(0, 100)
        pbar.setValue(100)
        pbar.setFormat("Guilt Deflected: 100%")
        pbar.setStyleSheet("QProgressBar { border: 2px solid #0e0e0d; border-radius: 10px; text-align: center; font-weight: 800; } QProgressBar::chunk { background: #244638; border-radius: 6px; }")
        lay.addWidget(pbar)
        
        lay.addStretch()
        
        btn_row = QHBoxLayout()
        btn_distract = QPushButton("Spawn Distraction App")
        btn_distract.setFixedHeight(36)
        btn_distract.setStyleSheet("QPushButton { background-color: #ea34df; color: #ffffff; border: 2px solid #0e0e0d; border-radius: 12px; font-weight: 900; } QPushButton:hover { background-color: #0e0e0d; }")
        btn_distract.clicked.connect(lambda: launch_app(random.choice(APPS_DATA)[1]))
        btn_row.addWidget(btn_distract)
        
        btn_close = QPushButton("Continue Slacking")
        btn_close.setFixedHeight(36)
        btn_close.setStyleSheet("QPushButton { background-color: #f5f4f0; color: #0e0e0d; border: 2px solid #0e0e0d; border-radius: 12px; font-weight: 900; } QPushButton:hover { background-color: #0e0e0d; color: #ffffff; }")
        btn_close.clicked.connect(dlg.accept)
        btn_row.addWidget(btn_close)
        lay.addLayout(btn_row)
        
        dlg.exec()

    def show_save_nothing_dialog(self):
        dlg, frame, lay = self._create_modal_dialog("Save Nothing Engine", 440, 320)
        
        msg = QLabel("Writing non-existent data to persistent nothingness...")
        msg.setStyleSheet("font-weight: 700; color: #0e0e0d; border: none; background: transparent;")
        lay.addWidget(msg)
        
        pbar = QProgressBar()
        pbar.setRange(0, 100)
        pbar.setValue(0)
        pbar.setStyleSheet("QProgressBar { border: 2px solid #0e0e0d; border-radius: 10px; text-align: center; font-weight: 800; } QProgressBar::chunk { background: #ea34df; border-radius: 6px; }")
        lay.addWidget(pbar)
        
        status = QLabel("Target: /dev/null • Status: In Progress")
        status.setStyleSheet("font-size: 8.5pt; color: #716f64; border: none; background: transparent;")
        lay.addWidget(status)
        
        prog = [0]
        t = QTimer(dlg)
        def step():
            prog[0] += 20
            pbar.setValue(min(100, prog[0]))
            if prog[0] >= 100:
                t.stop()
                status.setText("✓ 0 bytes successfully committed to void. Your non-work is safe.")
                status.setStyleSheet("font-size: 9pt; font-weight: 800; color: #244638; border: none; background: transparent;")
        t.timeout.connect(step)
        t.start(100)
        
        lay.addStretch()
        btn = QPushButton("Acknowledge Zero Bytes")
        btn.setFixedHeight(36)
        btn.setStyleSheet("QPushButton { background-color: #0e0e0d; color: #ffffff; border: 2px solid #0e0e0d; border-radius: 12px; font-weight: 800; } QPushButton:hover { background-color: #ea34df; }")
        btn.clicked.connect(dlg.accept)
        lay.addWidget(btn)
        dlg.exec()

    def show_exit_reality_dialog(self):
        dlg, frame, lay = self._create_modal_dialog("Security Alert: Reality Unsafe", 450, 360)
        
        alert = QLabel("⚠️ ACCESS DENIED: REALITY PROTOCOL")
        alert.setStyleSheet("font-weight: 900; font-size: 10pt; color: #e82803; border: none; background: transparent;")
        lay.addWidget(alert)
        
        body = QLabel("Connection to 'Reality' was terminated by Existential Safety Protocol.\n\nKnown vulnerabilities detected in Reality:\n• Unscheduled meetings\n• Inflation and tax obligations\n• No Command+Z / Undo for awkward conversations\n• Lack of dark mode\n\nFor your mental preservation, you must remain in UselessOS.")
        body.setStyleSheet("font-size: 8.5pt; color: #0e0e0d; border: none; background: transparent; line-height: 1.4;")
        body.setWordWrap(True)
        lay.addWidget(body)
        
        lay.addStretch()
        btn = QPushButton("Stay Safely Unproductive")
        btn.setFixedHeight(36)
        btn.setStyleSheet("QPushButton { background-color: #244638; color: #ffffff; border: 2px solid #0e0e0d; border-radius: 12px; font-weight: 900; } QPushButton:hover { background-color: #0e0e0d; }")
        btn.clicked.connect(dlg.accept)
        lay.addWidget(btn)
        dlg.exec()

    def show_undo_regret_dialog(self):
        dlg, frame, lay = self._create_modal_dialog("Spatiotemporal Rollback Engine", 460, 420)
        
        desc = QLabel("Select historical regret to rollback via quantum inversion:")
        desc.setStyleSheet("font-size: 8.5pt; color: #716f64; border: none; background: transparent;")
        lay.addWidget(desc)
        
        lw = QListWidget()
        lw.setStyleSheet("QListWidget { background: #f5f4f0; border: 2px solid #0e0e0d; border-radius: 10px; padding: 4px; }")
        regrets = [
            "Said 'You too' when waiter said 'Enjoy your meal' (2018)",
            "Sent email saying 'Attached is the file' without attaching anything (2021)",
            "Bought gym membership on Jan 1 and never stepped inside (2023)",
            "Agreed to an 8:30 AM Monday morning alignment sync (Last week)",
            "Overthought a one-word text message for 45 minutes (Today)"
        ]
        for r in regrets:
            item = QListWidgetItem(f"☐  {r}")
            lw.addItem(item)
        lay.addWidget(lw)
        
        status = QLabel("Ready for temporal inversion.")
        status.setStyleSheet("font-size: 8pt; color: #716f64; border: none; background: transparent;")
        lay.addWidget(status)
        
        def attempt_undo():
            sel = lw.currentItem()
            if sel:
                status.setText("⚠️ Error 503: Thermodynamics law prevents time travel. Regret converted to character development.")
                status.setStyleSheet("font-size: 8pt; font-weight: 800; color: #e82803; border: none; background: transparent;")
            else:
                status.setText("Please select a regret to attempt rollback.")
                
        btn_undo = QPushButton("Attempt Quantum Rollback")
        btn_undo.setFixedHeight(36)
        btn_undo.setStyleSheet("QPushButton { background-color: #00c2cb; color: #0e0e0d; border: 2px solid #0e0e0d; border-radius: 12px; font-weight: 900; } QPushButton:hover { background-color: #0e0e0d; color: #ffffff; }")
        btn_undo.clicked.connect(attempt_undo)
        lay.addWidget(btn_undo)
        dlg.exec()

    def show_redo_mistake_dialog(self):
        dlg, frame, lay = self._create_modal_dialog("Mistake Acceleration Unit", 440, 320)
        
        body = QLabel("Would you like to repeat your previous lapse of judgment with 200% higher confidence?\n\nStudies show that repeating mistakes builds resilience, humility, and memorable stories for future standups.")
        body.setStyleSheet("font-size: 9pt; color: #0e0e0d; border: none; background: transparent; line-height: 1.4;")
        body.setWordWrap(True)
        lay.addWidget(body)
        
        status = QLabel("Status: Awaiting poor decision...")
        status.setStyleSheet("font-size: 8.5pt; color: #716f64; border: none; background: transparent;")
        lay.addWidget(status)
        
        def commit_again():
            status.setText("✓ Mistake recommitted! Zero lessons learned. Confidence at maximum.")
            status.setStyleSheet("font-size: 8.5pt; font-weight: 900; color: #ea34df; border: none; background: transparent;")
            
        btn = QPushButton("Commit Exact Same Mistake Again")
        btn.setFixedHeight(38)
        btn.setStyleSheet("QPushButton { background-color: #ea34df; color: #ffffff; border: 2px solid #0e0e0d; border-radius: 12px; font-weight: 900; } QPushButton:hover { background-color: #0e0e0d; }")
        btn.clicked.connect(commit_again)
        lay.addWidget(btn)
        dlg.exec()

    def show_cut_corners_dialog(self):
        dlg, frame, lay = self._create_modal_dialog("Corner Cutting Engine", 460, 340)
        
        info = QLabel("Adjust the aggressive laziness quotient of your workflow:")
        info.setStyleSheet("font-size: 8.5pt; color: #716f64; border: none; background: transparent;")
        lay.addWidget(info)
        
        lbl_val = QLabel("Corner Cutting Quotient: 50%")
        lbl_val.setStyleSheet("font-weight: 800; font-size: 9pt; color: #0e0e0d; border: none; background: transparent;")
        lay.addWidget(lbl_val)
        
        slider = QSlider(Horizontal)
        slider.setRange(0, 100)
        slider.setValue(50)
        slider.setStyleSheet(self._slider_style("#e82803"))
        lay.addWidget(slider)
        
        preview = QLabel("Bypassing unit tests and hardcoding configuration.")
        preview.setStyleSheet("font-style: italic; font-size: 8.5pt; color: #e82803; border: none; background: transparent;")
        preview.setWordWrap(True)
        lay.addWidget(preview)
        
        def on_val(v):
            lbl_val.setText(f"Corner Cutting Quotient: {v}%")
            if v < 25:
                preview.setText("Meticulous craftsmanship. (Warning: Not aligned with Useless philosophy)")
            elif v < 50:
                preview.setText("Skipping documentation and descriptive variable names.")
            elif v < 75:
                preview.setText("Copying StackOverflow snippets from 2011 directly into production.")
            else:
                preview.setText("Pushing straight to main branch on Friday at 4:59 PM. Structural integrity: Optimistic.")
        slider.valueChanged.connect(on_val)
        
        lay.addStretch()
        btn = QPushButton("Apply Corner Cutting")
        btn.setFixedHeight(36)
        btn.setStyleSheet("QPushButton { background-color: #0e0e0d; color: #ffffff; border: 2px solid #0e0e0d; border-radius: 12px; font-weight: 900; } QPushButton:hover { background-color: #e82803; }")
        btn.clicked.connect(dlg.accept)
        lay.addWidget(btn)
        dlg.exec()

    def _slider_style(self, color):
        return f"""
            QSlider::groove:horizontal {{
                border: 2px solid #0e0e0d;
                height: 10px;
                background: #f5f4f0;
                border-radius: 5px;
            }}
            QSlider::sub-page:horizontal {{
                background: {color};
                border: 2px solid #0e0e0d;
                border-radius: 5px;
            }}
            QSlider::handle:horizontal {{
                background: #ffffff;
                border: 2px solid #0e0e0d;
                width: 22px;
                margin-top: -6px;
                margin-bottom: -6px;
                border-radius: 11px;
            }}
        """

    def action_copy_fake_work(self):
        fake_code = (
            "// CORE SYNERGY & PARADIGM ALIGNMENT ENGINE v3.4.1\n"
            "// Lead Architects: Edwin Joseph & Antigravity (Google DeepMind)\n"
            "class CrossFunctionalDeliverableOptimizer {\n"
            "    constructor(options = {}) {\n"
            "        this.kpiThreshold = options.kpiThreshold || 1.6180339887;\n"
            "        this.synergyBandwidth = new Map();\n"
            "        this.circuitBreaker = false;\n"
            "    }\n"
            "    async executeStrategicRoadmap(paradigmShift) {\n"
            "        const latency = await this.synthesizeStakeholderConsensus();\n"
            "        return paradigmShift.map(deliverable => ({\n"
            "            actionableInsight: deliverable.pivotWithoutWarning(),\n"
            "            scalabilityConfidence: 0.9998,\n"
            "            unplannedOverhead: Math.log2(latency)\n"
            "        }));\n"
            "    }\n"
            "    synthesizeStakeholderConsensus() {\n"
            "        return new Promise(resolve => setTimeout(resolve, 42));\n"
            "    }\n"
            "}\n"
        )
        try:
            cb = QApplication.clipboard()
            if cb:
                cb.setText(fake_code)
        except Exception:
            pass
            
        dlg, frame, lay = self._create_modal_dialog("Clipboard Copied", 420, 260)
        lbl = QLabel("✓ 500 lines of fake enterprise synergy pseudocode copied to your system clipboard!\n\nPaste into your code editor or Slack to look furiously productive.")
        lbl.setStyleSheet("font-weight: 800; font-size: 9pt; color: #244638; border: none; background: transparent; line-height: 1.4;")
        lbl.setWordWrap(True)
        lay.addWidget(lbl)
        lay.addStretch()
        btn = QPushButton("Understood")
        btn.setFixedHeight(34)
        btn.setStyleSheet("QPushButton { background-color: #0e0e0d; color: #ffffff; border: 2px solid #0e0e0d; border-radius: 12px; font-weight: 800; }")
        btn.clicked.connect(dlg.accept)
        lay.addWidget(btn)
        dlg.exec()

    def show_panic_simulation_dialog(self):
        dlg, frame, lay = self._create_modal_dialog("3:17 AM Panic Simulation", 450, 360)
        
        bpm_row = QHBoxLayout()
        bpm_lbl = QLabel("SIMULATED HEART RATE: 142 BPM")
        bpm_lbl.setStyleSheet("font-weight: 900; font-size: 9pt; color: #e82803; background: #ffebee; border: 1.5px solid #e82803; border-radius: 8px; padding: 4px 8px;")
        bpm_row.addWidget(bpm_lbl)
        bpm_row.addStretch()
        lay.addLayout(bpm_row)
        
        panics = [
            "“Did I sound passive-aggressive when I replied 'Sounds good.' with a period in 2022?”",
            "“What if everyone at work realizes I just Google basic syntax every 15 minutes?”",
            "“Where do all the pigeons go at night and why don't we see baby pigeons?”",
            "“What if I left the stove on in an apartment I moved out of three years ago?”"
        ]
        
        quote = QLabel(random.choice(panics))
        quote.setStyleSheet("font-family: Helvetica; font-size: 11pt; font-weight: 800; color: #0e0e0d; border: 2px solid #0e0e0d; border-radius: 12px; padding: 12px; background: #f5f4f0;")
        quote.setWordWrap(True)
        lay.addWidget(quote)
        
        tip = QLabel("Remedy: Stare blankly at ceiling, hydrate, and realize nothing matters.")
        tip.setStyleSheet("font-size: 8pt; color: #716f64; border: none; background: transparent;")
        lay.addWidget(tip)
        
        lay.addStretch()
        btn_next = QPushButton("Simulate Another 3 AM Thought")
        btn_next.setFixedHeight(36)
        btn_next.setStyleSheet("QPushButton { background-color: #ea34df; color: #ffffff; border: 2px solid #0e0e0d; border-radius: 12px; font-weight: 900; } QPushButton:hover { background-color: #0e0e0d; }")
        btn_next.clicked.connect(lambda: quote.setText(random.choice(panics)))
        lay.addWidget(btn_next)
        dlg.exec()

    def show_worst_case_dialog(self):
        dlg, frame, lay = self._create_modal_dialog("Hypothetical Worst-Case Extrapolator", 460, 420)
        
        info = QLabel("Enter any minor everyday event:")
        info.setStyleSheet("font-size: 8.5pt; color: #716f64; border: none; background: transparent;")
        lay.addWidget(info)
        
        inp = QLineEdit("I sent an email with a typo in the greeting.")
        inp.setStyleSheet("QLineEdit { background: #f5f4f0; border: 2px solid #0e0e0d; border-radius: 10px; padding: 6px 10px; font-weight: 600; }")
        lay.addWidget(inp)
        
        res = QLabel("Calculated Doom Probability: 99.8%\n\nExtrapolation Cascade:\n1. Recipient notes typo.\n2. Recipient questions your attention to detail.\n3. Contract canceled.\n4. Global macroeconomic collapse.\n5. Heat death of the universe.")
        res.setStyleSheet("font-size: 8.5pt; color: #0e0e0d; border: 2px solid #0e0e0d; border-radius: 10px; padding: 8px; background: #ffffff; line-height: 1.3;")
        res.setWordWrap(True)
        lay.addWidget(res)
        
        def calculate():
            text = inp.text()
            res.setText(f"Event: “{text}”\nCatastrophe Probability: 99.9%\nCascade: Minor lapse -> Deep existential dread -> Total timeline unraveling.\nRecommendation: Continue spiraling.")
            
        btn = QPushButton("Recalculate Doom Cascade")
        btn.setFixedHeight(36)
        btn.setStyleSheet("QPushButton { background-color: #e82803; color: #ffffff; border: 2px solid #0e0e0d; border-radius: 12px; font-weight: 900; } QPushButton:hover { background-color: #0e0e0d; }")
        btn.clicked.connect(calculate)
        lay.addWidget(btn)
        dlg.exec()

    def show_rumination_dialog(self):
        dlg, frame, lay = self._create_modal_dialog("2017 Conversation Rumination", 460, 420)
        
        transcript = QLabel("TRANSCRIPT: OCT 14, 2017 — 2:41 PM\n\nCashier: “Enjoy your coffee!”\nYou: “Thanks, you too!”\nCashier: “...”\nYou: [Disappears into floorboards]")
        transcript.setStyleSheet("font-family: monospace; font-size: 8.5pt; color: #0e0e0d; background: #f5f4f0; border: 2px solid #0e0e0d; border-radius: 10px; padding: 10px;")
        lay.addWidget(transcript)
        
        h_lbl = QLabel("10 Better Comebacks Thought of 7 Years Later in the Shower:")
        h_lbl.setStyleSheet("font-weight: 800; font-size: 8.5pt; color: #ea34df; border: none; background: transparent;")
        lay.addWidget(h_lbl)
        
        lw = QListWidget()
        lw.setStyleSheet("QListWidget { background: #ffffff; border: 2px solid #0e0e0d; border-radius: 8px; padding: 4px; font-size: 8pt; }")
        comebacks = [
            "“I will, and may your next customer be as polite as me.”",
            "“Actually, coffee is an illusion, but thanks.”",
            "“Take a sip with me in spirit.”",
            "“Only if the coffee enjoys me back.”"
        ]
        for c in comebacks:
            lw.addItem(c)
        lay.addWidget(lw)
        
        lay.addStretch()
        btn = QPushButton("Close & Ruminate Silently")
        btn.setFixedHeight(34)
        btn.setStyleSheet("QPushButton { background-color: #0e0e0d; color: #ffffff; border: 2px solid #0e0e0d; border-radius: 12px; font-weight: 800; }")
        btn.clicked.connect(dlg.accept)
        lay.addWidget(btn)
        dlg.exec()

    def show_curiosity_exist_dialog(self):
        dlg, frame, lay = self._create_modal_dialog("Why Does UselessOS Exist?", 500, 470)
        
        sub = QLabel("A Manifesto on Intentional Impracticality")
        sub.setStyleSheet("font-size: 9pt; font-weight: 800; color: #ea34df; border: none; background: transparent;")
        lay.addWidget(sub)
        
        body = QLabel(
            "Every modern operating system is designed to extract your labor, measure your key performance indicators, bombard you with push notifications, and optimize every second of your waking life.\n\n"
            "UselessOS 3.0 was conceived by Edwin Joseph and Antigravity (Google DeepMind) as an interactive art sanctuary for the TinkerHub community.\n\n"
            "It is an operating system where technology performs no corporate duties. It does not synchronize calendars. It does not file reports.\n\n"
            "Instead, it exists solely to spark curiosity, make you smile, and remind us of the playful soul of personal computing."
        )
        body.setStyleSheet("font-size: 8.5pt; color: #0e0e0d; border: none; background: transparent; line-height: 1.45;")
        body.setWordWrap(True)
        lay.addWidget(body)
        
        creds = QLabel("Crafted with <3 by Edwin Joseph & Antigravity (Google DeepMind)")
        creds.setStyleSheet("font-family: 'NanumPenScript', cursive; font-size: 13.5pt; color: #e82803; border: none; background: transparent;")
        creds.setAlignment(AlignCenter)
        creds.setWordWrap(True)
        lay.addWidget(creds)
        
        lay.addStretch()
        btn = QPushButton("Celebrate Uselessness")
        btn.setFixedHeight(36)
        btn.setStyleSheet("QPushButton { background-color: #244638; color: #ffffff; border: 2px solid #0e0e0d; border-radius: 12px; font-weight: 900; } QPushButton:hover { background-color: #0e0e0d; }")
        btn.clicked.connect(dlg.accept)
        lay.addWidget(btn)
        dlg.exec()

    def show_sarcasm_matrix_dialog(self):
        dlg, frame, lay = self._create_modal_dialog("Sarcasm Matrix Calibration", 460, 360)
        
        hdr = QLabel("Adjust Cognitive Sarcasm Threshold:")
        hdr.setStyleSheet("font-size: 8.5pt; color: #716f64; border: none; background: transparent;")
        lay.addWidget(hdr)
        
        s_lbl = QLabel("Sarcasm Intensity: 75% (Severe)")
        s_lbl.setStyleSheet("font-weight: 800; font-size: 9.5pt; color: #0e0e0d; border: none; background: transparent;")
        lay.addWidget(s_lbl)
        
        slider = QSlider(Horizontal)
        slider.setRange(0, 100)
        slider.setValue(75)
        slider.setStyleSheet(self._slider_style("#00c2cb"))
        lay.addWidget(slider)
        
        preview = QLabel("“Groundbreaking productivity happening right here. The shareholders will weep with joy.”")
        preview.setStyleSheet("font-style: italic; font-size: 9pt; color: #00838f; border: 2px solid #0e0e0d; border-radius: 10px; padding: 10px; background: #e0f7fa;")
        preview.setWordWrap(True)
        lay.addWidget(preview)
        
        def on_v(v):
            s_lbl.setText(f"Sarcasm Intensity: {v}%")
            if v < 25:
                preview.setText("“Oh, you clicked that? That was very polite and thoughtful.”")
            elif v < 50:
                preview.setText("“Another masterclass in modern digital navigation.”")
            elif v < 80:
                preview.setText("“Groundbreaking productivity happening right here. The shareholders will weep with joy.”")
            else:
                preview.setText("“I would explain the logic to you, but neither of us has the cognitive bandwidth.”")
        slider.valueChanged.connect(on_v)
        
        lay.addStretch()
        btn = QPushButton("Lock Sarcasm Level")
        btn.setFixedHeight(36)
        btn.setStyleSheet("QPushButton { background-color: #0e0e0d; color: #ffffff; border: 2px solid #0e0e0d; border-radius: 12px; font-weight: 900; } QPushButton:hover { background-color: #00c2cb; color: #0e0e0d; }")
        btn.clicked.connect(dlg.accept)
        lay.addWidget(btn)
        dlg.exec()

    def show_impracticality_stress_dialog(self):
        dlg, frame, lay = self._create_modal_dialog("Impracticality Limit Stress Test", 460, 360)
        
        sub = QLabel("Measuring system adherence to non-functional specifications:")
        sub.setStyleSheet("font-size: 8.5pt; color: #716f64; border: none; background: transparent;")
        lay.addWidget(sub)
        
        bars = [
            ("Nonsense Generation Core", 100, "#ea34df"),
            ("Productivity Neutralization", 100, "#244638"),
            ("Cognitive Overload Suppression", 99, "#00c2cb")
        ]
        for name, val, col in bars:
            lay.addWidget(QLabel(f"{name}: {val}%"))
            pb = QProgressBar()
            pb.setRange(0, 100)
            pb.setValue(val)
            pb.setStyleSheet(f"QProgressBar {{ border: 2px solid #0e0e0d; border-radius: 8px; text-align: center; font-weight: 800; height: 16px; }} QProgressBar::chunk {{ background: {col}; border-radius: 4px; }}")
            lay.addWidget(pb)
            
        status = QLabel("✓ RESULT: System is operating at certified 100% impractical capacity.")
        status.setStyleSheet("font-weight: 900; font-size: 9pt; color: #244638; border: none; background: transparent;")
        lay.addWidget(status)
        
        lay.addStretch()
        btn = QPushButton("Acknowledge Peak Impracticality")
        btn.setFixedHeight(36)
        btn.setStyleSheet("QPushButton { background-color: #0e0e0d; color: #ffffff; border: 2px solid #0e0e0d; border-radius: 12px; font-weight: 800; }")
        btn.clicked.connect(dlg.accept)
        lay.addWidget(btn)
        dlg.exec()

    def show_no_help_dialog(self):
        dlg, frame, lay = self._create_modal_dialog("No Help Available", 420, 280)
        
        body = QLabel("In strict alignment with UselessOS design guidelines, helpfulness has been permanently deprecated.\n\nIf you are experiencing confusion, please:\n1. Ask a nearby rubber duck\n2. Drink a glass of water\n3. Accept that computers are essentially glowing sand")
        body.setStyleSheet("font-size: 8.5pt; color: #0e0e0d; border: none; background: transparent; line-height: 1.4;")
        body.setWordWrap(True)
        lay.addWidget(body)
        
        lay.addStretch()
        btn = QPushButton("Accept Helplessness")
        btn.setFixedHeight(36)
        btn.setStyleSheet("QPushButton { background-color: #0e0e0d; color: #ffffff; border: 2px solid #0e0e0d; border-radius: 12px; font-weight: 800; } QPushButton:hover { background-color: #ea34df; }")
        btn.clicked.connect(dlg.accept)
        lay.addWidget(btn)
        dlg.exec()

    def show_complaint_dialog(self):
        dlg, frame, lay = self._create_modal_dialog("Submit Complaint to /dev/null", 460, 360)
        
        info = QLabel("Please describe your grievances, bugs, or existential complaints:")
        info.setStyleSheet("font-size: 8.5pt; color: #716f64; border: none; background: transparent;")
        lay.addWidget(info)
        
        te = QTextEdit()
        te.setPlaceholderText("e.g. The apps are too useless, the clock is too existential, my cat won't stop judging me...")
        te.setStyleSheet("QTextEdit { background: #f5f4f0; border: 2px solid #0e0e0d; border-radius: 10px; padding: 8px; font-weight: 600; }")
        lay.addWidget(te)
        
        status = QLabel("Target: /dev/null • Retention: 0.00 seconds")
        status.setStyleSheet("font-size: 8pt; color: #716f64; border: none; background: transparent;")
        lay.addWidget(status)
        
        def send_void():
            te.clear()
            status.setText("✓ Complaint successfully vaporized into the cosmos. No one will ever read it.")
            status.setStyleSheet("font-size: 8.5pt; font-weight: 900; color: #244638; border: none; background: transparent;")
            
        btn = QPushButton("Transmit Complaint to /dev/null")
        btn.setFixedHeight(36)
        btn.setStyleSheet("QPushButton { background-color: #e82803; color: #ffffff; border: 2px solid #0e0e0d; border-radius: 12px; font-weight: 900; } QPushButton:hover { background-color: #0e0e0d; }")
        btn.clicked.connect(send_void)
        lay.addWidget(btn)
        dlg.exec()

    def show_absurdity_dialog(self):
        dlg, frame, lay = self._create_modal_dialog("Embrace The Absurdity", 460, 360)
        
        quote = QLabel("“The absurd is born of this confrontation between the human need and the unreasonable silence of the world.”\n\n— Albert Camus, The Myth of Sisyphus")
        quote.setStyleSheet("font-style: italic; font-size: 9.5pt; color: #0e0e0d; border: 2px solid #0e0e0d; border-radius: 12px; padding: 12px; background: #f5f4f0; line-height: 1.4;")
        quote.setWordWrap(True)
        lay.addWidget(quote)
        
        expl = QLabel("You cannot defeat the absurdity of existence, but you can launch an absurd app:")
        expl.setStyleSheet("font-size: 8.5pt; color: #716f64; border: none; background: transparent;")
        lay.addWidget(expl)
        
        row = QHBoxLayout()
        b1 = QPushButton("Existential Clock")
        b1.setFixedHeight(36)
        b1.setStyleSheet("QPushButton { background-color: #00c2cb; color: #0e0e0d; border: 2px solid #0e0e0d; border-radius: 12px; font-weight: 800; }")
        b1.clicked.connect(lambda: launch_app("existential_clock.py"))
        row.addWidget(b1)
        
        b2 = QPushButton("Excuse Generator")
        b2.setFixedHeight(36)
        b2.setStyleSheet("QPushButton { background-color: #ea34df; color: #ffffff; border: 2px solid #0e0e0d; border-radius: 12px; font-weight: 800; }")
        b2.clicked.connect(lambda: launch_app("excuse_generator.py"))
        row.addWidget(b2)
        lay.addLayout(row)
        
        lay.addStretch()
        btn = QPushButton("I Am Sisyphus and I Am Happy")
        btn.setFixedHeight(36)
        btn.setStyleSheet("QPushButton { background-color: #0e0e0d; color: #ffffff; border: 2px solid #0e0e0d; border-radius: 12px; font-weight: 800; }")
        btn.clicked.connect(dlg.accept)
        lay.addWidget(btn)
        dlg.exec()


class DockItem(QWidget):
    """
    Individual dock tile representing an application.
    Displays bespoke squircle icon and active running indicator dot.
    Clicking acts like an iPad-style app switcher (unminimizing/raising window).
    """
    def __init__(self, name, script, icon_name, color, desc, parent=None):
        super().__init__(parent)
        self.name = name
        self.script = script
        self.color = color
        self.desc = desc
        self.win_id = None
        self.is_running = False
        
        self.setFixedSize(56, 68)
        
        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 2)
        lay.setSpacing(2)
        lay.setAlignment(Qt.AlignmentFlag.AlignCenter if PYQT6 else Qt.AlignCenter)
        
        self.btn = QPushButton(self)
        self.btn.setToolTip(f"""
            <div style='background-color: #ffffff; color: #0e0e0d; padding: 2px;'>
                <b style='font-size: 10.5pt; color: #0e0e0d;'>{name}</b><br/>
                <span style='color: {color}; font-weight: 800; font-size: 8pt;'>● USELESS PROJECTS 3.0</span><br/>
                <span style='color: #555550; font-size: 8.5pt;'>{desc}</span>
            </div>
        """)
        self.btn.setFixedSize(52, 52)
        self.btn.setCursor(QCursor(PointingHandCursor))
        
        icon_path = get_icon_path(icon_name)
        if icon_path and os.path.exists(icon_path):
            pix = QPixmap(icon_path).scaled(44, 44, Qt.AspectRatioMode.KeepAspectRatio if PYQT6 else Qt.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation if PYQT6 else Qt.SmoothTransformation)
            self.btn.setIcon(QIcon(pix))
            self.btn.setIconSize(QSize(44, 44))
        else:
            self.btn.setText(name[:3])
            
        self.btn.setStyleSheet(f"""
            QPushButton {{
                background-color: #ffffff;
                border: 2px solid #0e0e0d;
                border-radius: 14px;
                padding: 2px;
            }}
            QPushButton:hover {{
                background-color: {color};
                border: 3px solid #0e0e0d;
            }}
        """)
        self.btn.clicked.connect(self.on_clicked)
        lay.addWidget(self.btn)
        
        # Running status indicator dot (iPad/macOS style)
        self.dot = QLabel(self)
        self.dot.setFixedSize(6, 6)
        self.dot.setStyleSheet("""
            background-color: #0e0e0d;
            border-radius: 3px;
            border: none;
        """)
        self.dot.hide()
        lay.addWidget(self.dot, alignment=Qt.AlignmentFlag.AlignCenter if PYQT6 else Qt.AlignCenter)
        
    def set_running_state(self, is_running, win_id=None):
        self.is_running = is_running
        self.win_id = win_id
        if is_running:
            self.dot.show()
            self.btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: #ffffff;
                    border: 2.5px solid {self.color};
                    border-radius: 14px;
                    padding: 2px;
                }}
                QPushButton:hover {{
                    background-color: {self.color};
                    border: 3px solid #0e0e0d;
                }}
            """)
        else:
            self.dot.hide()
            self.btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: #ffffff;
                    border: 2px solid #0e0e0d;
                    border-radius: 14px;
                    padding: 2px;
                }}
                QPushButton:hover {{
                    background-color: {self.color};
                    border: 3px solid #0e0e0d;
                }}
            """)
            
    def on_clicked(self):
        if self.is_running and self.win_id:
            # iPad-style App Switcher: Bring window to foreground & focus
            try:
                env = os.environ.copy()
                env["DISPLAY"] = os.environ.get("DISPLAY", ":0")
                subprocess.Popen(["wmctrl", "-i", "-a", self.win_id], env=env)
            except Exception as e:
                print(f"[DockItem] wmctrl raise error: {e}")
                launch_app(self.script)
        else:
            # Launch application
            launch_app(self.script)


class Dock(QFrame):
    """
    macOS/iPad-style floating dock and active app switcher.
    Queries active X11 windows in real time, displays running status indicators,
    and switches to open windows on click.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 0.96);
                border: 2px solid #0e0e0d;
                border-radius: 26px;
            }
        """)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 5, 12, 3)
        layout.setSpacing(8)
        
        self.items = []
        for name, script, icon_name, color, desc in APPS_DATA:
            item = DockItem(name, script, icon_name, color, desc, self)
            self.items.append(item)
            layout.addWidget(item)
            
        # Real-time window tracker timer (throttled to 3.0s to reduce process fork overhead)
        self.poll_timer = QTimer(self)
        self.poll_timer.timeout.connect(self.poll_windows)
        self.poll_timer.start(3000)
        self.poll_windows()
        
    def poll_windows(self):
        env = os.environ.copy()
        env["DISPLAY"] = os.environ.get("DISPLAY", ":0")
        try:
            out = safe_check_output(["wmctrl", "-l", "-p", "-x"], env=env, timeout=0.5)
            lines = out.splitlines()
        except Exception:
            lines = []
            
        for item in self.items:
            found_win = None
            for line in lines:
                # Exclude desktop shell itself
                if "Useless Shell" in line:
                    continue
                # Match by script name or class or app title
                script_stem = item.script.replace(".py", "")
                if (script_stem in line.lower() or 
                    item.name.lower() in line.lower() or 
                    item.script in line):
                    found_win = line.split()[0]
                    break
            item.set_running_state(found_win is not None, found_win)



class UselessDesktopShell(QMainWindow):
    """
    Unified, High-Performance Desktop Shell for UselessOS.
    Brings together macOS UI architecture (Top Bar, Control Center, Launchpad App Drawer, Dock)
    with 100% faithful TinkerHub Useless Projects aesthetic.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Useless Shell")
        self.setWindowFlags(FramelessWindowHint)
        self.setStyleSheet("background-color: #ffffff;")
        
        central = QWidget(self)
        self.setCentralWidget(central)
        
        # 1. Top Bar
        self.topbar = TopBar(central, shell=self)
        
        # 2. Hero Centerpiece Container
        self.hero_container = QWidget(central)
        
        # Decorative SVGs positioned in safe outer perimeter (never colliding with center)
        self.svg_widgets = []
        svg_items = [
            # Top perimeter
            ("tetris-green-a.svg", -480, -180, 80, 80),
            ("tetris-magenta-a.svg", 400, -170, 80, 80),
            # Flanking mid perimeter
            ("ele-monster-green.svg", -450, -30, 90, 90),
            ("ele-monster-purple.svg", 380, -20, 90, 90),
            # Bottom perimeter
            ("tetris-cyan.svg", -470, 120, 75, 75),
            ("tetris-orange-a.svg", 410, 110, 75, 75),
            ("tetris-red.svg", 280, 175, 60, 60),
            ("tetris-yellow.svg", -280, 175, 60, 60),
            # Subtle accent dots
            ("hero-dot-1.svg", -260, -170, 26, 26),
            ("hero-dot-2.svg", 260, -160, 24, 24)
        ]
        
        for fname, rx, ry, w, h in svg_items:
            path = get_asset_path(fname)
            if path and QSvgWidget is not None:
                svg = QSvgWidget(path, self.hero_container)
                self.svg_widgets.append((svg, rx, ry, w, h))
                
        # Giant Hero Title ("Useless" & "Projects") with dedicated non-clipping labels
        self.title_useless = QLabel("Useless", self.hero_container)
        self.title_useless.setAlignment(AlignCenter)
        self.title_useless.setStyleSheet("""
            QLabel {
                color: #0e0e0d;
                font-family: "Drowner", "Helvetica-Bold", "Arial Black", sans-serif;
                font-size: 70pt;
                font-weight: 900;
                background: transparent;
            }
        """)
        
        self.title_projects = QLabel("Projects", self.hero_container)
        self.title_projects.setAlignment(AlignCenter)
        self.title_projects.setStyleSheet("""
            QLabel {
                color: #0e0e0d;
                font-family: "Drowner", "Helvetica-Bold", "Arial Black", sans-serif;
                font-size: 70pt;
                font-weight: 900;
                background: transparent;
            }
        """)
        
        # "3.0" Badge with comfortable padding and clear font
        self.badge = QLabel("3.0", self.hero_container)
        self.badge.setAlignment(AlignCenter)
        self.badge.setStyleSheet("""
            QLabel {
                background-color: #ea34df;
                color: #ffffff;
                border: 2px solid #0e0e0d;
                border-radius: 20px;
                font-family: "JRK", "Helvetica", sans-serif;
                font-size: 16pt;
                font-weight: 900;
                padding-bottom: 2px;
            }
        """)
        
        # Handwritten Tagline
        self.tagline = QLabel("exclusive to Tinkerhub campus community <3", self.hero_container)
        self.tagline.setAlignment(AlignCenter)
        self.tagline.setStyleSheet("""
            QLabel {
                color: #100f0f;
                font-family: "NanumPenScript", "Nanum Pen Script", cursive;
                font-size: 22pt;
                background: transparent;
            }
        """)
        
        # Centerpiece Buttons Container
        self.btn_box = QWidget(self.hero_container)
        btn_layout = QHBoxLayout(self.btn_box)
        btn_layout.setContentsMargins(0, 0, 0, 0)
        btn_layout.setSpacing(16)
        
        # Main Impracticality Button (Launchpad trigger)
        self.reveal_btn = QPushButton("Explore All Applications")
        self.reveal_btn.setCursor(QCursor(PointingHandCursor))
        self.reveal_btn.setFixedHeight(52)
        self.reveal_btn.setStyleSheet("""
            QPushButton {
                background-color: #0e0e0d;
                color: #ffffff;
                border: 2px solid #0e0e0d;
                border-radius: 26px;
                font-family: Helvetica;
                font-weight: 900;
                font-size: 11pt;
                padding: 10px 30px;
            }
            QPushButton:hover {
                background-color: #ea34df;
                color: #ffffff;
                border: 2px solid #0e0e0d;
            }
        """)
        self.reveal_btn.clicked.connect(self.toggle_launchpad)
        btn_layout.addWidget(self.reveal_btn)
        
        # Companion Button (Instant Launch)
        self.random_btn = QPushButton("Launch Random App")
        self.random_btn.setCursor(QCursor(PointingHandCursor))
        self.random_btn.setFixedHeight(52)
        self.random_btn.setStyleSheet("""
            QPushButton {
                background-color: #ffffff;
                color: #0e0e0d;
                border: 2px solid #0e0e0d;
                border-radius: 26px;
                font-family: Helvetica;
                font-weight: 900;
                font-size: 11pt;
                padding: 10px 24px;
            }
            QPushButton:hover {
                background-color: #e82803;
                color: #ffffff;
            }
        """)
        self.random_btn.clicked.connect(self.launch_random_app)
        btn_layout.addWidget(self.random_btn)
        
        # Dynamic feedback ticker
        self.feedback_lbl = QLabel(self.hero_container)
        self.feedback_lbl.setAlignment(AlignCenter)
        self.feedback_lbl.setStyleSheet("""
            QLabel {
                color: #244638;
                font-family: Helvetica;
                font-size: 10pt;
                font-weight: 700;
                background: transparent;
            }
        """)
        self.feedback_lbl.setText("Click above to explore applications or click any dock icon below.")
        
        # 3. macOS-style Launchpad Drawer (Modal overlay)
        self.launchpad = LaunchpadDrawer(central)
        self.launchpad.hide()
        
        # 4. macOS-style Control Center Drawer
        self.control_center = ControlCenterDrawer(central)
        self.control_center.hide()
        
        # 5. macOS-style Bottom Dock with Squircle PNG Icons
        self.dock = Dock(central)
        
        # Floating Animation Loop (optimized at 80ms for smooth 12.5fps rendering without CPU waste)
        self.float_tick = 0
        self.anim_timer = QTimer(self)
        self.anim_timer.timeout.connect(self.animate_floating)
        self.anim_timer.start(80)
        
        # Connect to screen geometry changes for dynamic resolution adaptation
        app = QApplication.instance()
        if app and app.primaryScreen():
            app.primaryScreen().geometryChanged.connect(self._handle_screen_change)
            if hasattr(app.primaryScreen(), 'virtualGeometryChanged'):
                app.primaryScreen().virtualGeometryChanged.connect(self._handle_screen_change)

    def _handle_screen_change(self, geo):
        self.setGeometry(geo)
        self.update()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        w = self.width()
        h = self.height()
        
        # 1. Top Bar spans full screen width
        self.topbar.setGeometry(0, 0, w, 44)
        
        # 2. Bottom Dock centered horizontally
        dock_w = min(w - 20, len(APPS_DATA) * 64 + 28)
        dock_h = 80
        dock_y = max(50, h - dock_h - 12)
        self.dock.setGeometry((w - dock_w) // 2, dock_y, dock_w, dock_h)
        
        # 3. Available space between topbar and dock
        avail_h = max(200, dock_y - 44)
        hero_w = min(1140, w - 20)
        hero_h = min(470, max(260, avail_h - 10))
        hero_x = (w - hero_w) // 2
        hero_y = 44 + max(5, (avail_h - hero_h) // 2)
        self.hero_container.setGeometry(hero_x, hero_y, hero_w, hero_h)
        
        cx = hero_w // 2
        cy = hero_h // 2
        
        # Responsive typography scale factor for different display resolutions
        scale = min(1.0, max(0.6, min(w / 1140.0, hero_h / 460.0)))
        f_size = int(70 * scale)
        t_height = int(115 * scale)
        t_w = int(880 * scale)
        
        self.title_useless.setStyleSheet(f"""
            QLabel {{
                color: #0e0e0d;
                font-family: 'Drowner', sans-serif;
                font-size: {f_size}pt;
                font-weight: 900;
                background: transparent;
                border: none;
                margin: 0px;
                padding: 0px;
            }}
        """)
        self.title_projects.setStyleSheet(f"""
            QLabel {{
                color: #0e0e0d;
                font-family: 'Drowner', sans-serif;
                font-size: {f_size}pt;
                font-weight: 900;
                background: transparent;
                border: none;
                margin: 0px;
                padding: 0px;
            }}
        """)
        
        offset_y = int(95 * scale)
        self.title_useless.setGeometry(cx - t_w // 2, cy - offset_y * 2, t_w, t_height)
        self.title_projects.setGeometry(cx - t_w // 2, cy - offset_y, t_w, t_height)
        self.badge.setGeometry(min(hero_w - 90, cx + int(240 * scale)), cy - int(170 * scale), 84, 42)
        self.tagline.setGeometry(cx - 350, min(hero_h - 100, cy + int(35 * scale)), 700, 36)
        self.btn_box.setGeometry(cx - 280, min(hero_h - 60, cy + int(85 * scale)), 560, 52)
        self.feedback_lbl.setGeometry(cx - 420, min(hero_h - 25, cy + int(145 * scale)), 840, 26)
        
        # Position decorative SVGs safely
        for svg, rx, ry, sw, sh in self.svg_widgets:
            s_sw = int(sw * scale)
            s_sh = int(sh * scale)
            svg.setGeometry(cx + int(rx * scale), cy + int(ry * scale), s_sw, s_sh)
            
        # 4. Launchpad Drawer centered
        lp_w = min(880, w - 40)
        lp_h = min(520, max(280, h - 80))
        self.launchpad.setGeometry((w - lp_w) // 2, max(46, (h - lp_h) // 2), lp_w, lp_h)
        
        # 5. Control Center positioned top-right
        cc_w = min(self.control_center.width(), w - 20)
        cc_h = min(self.control_center.height(), h - 60)
        self.control_center.setGeometry(max(10, w - cc_w - 20), 48, cc_w, cc_h)
        
    def animate_floating(self):
        if not self.isVisible() or self.isMinimized():
            return
        import math
        self.float_tick += 0.06
        offset = int(math.sin(self.float_tick) * 5)
        
        hero_h = self.hero_container.height()
        cy = hero_h // 2
        cx = self.hero_container.width() // 2
        
        # Relative scale
        w = self.width()
        scale = min(1.0, max(0.6, min(w / 1140.0, hero_h / 460.0)))
        t_w = int(880 * scale)
        offset_y = int(95 * scale)
        
        self.title_useless.move(cx - t_w // 2, cy - offset_y * 2 + offset)
        self.title_projects.move(cx - t_w // 2, cy - offset_y + offset)
        self.badge.move(min(self.hero_container.width() - 90, cx + int(240 * scale)), cy - int(170 * scale) + offset)
        
        for i, (svg, rx, ry, sw, sh) in enumerate(self.svg_widgets):
            svg_offset = int(math.sin(self.float_tick + i) * 4)
            svg.move(cx + int(rx * scale), cy + int(ry * scale) + svg_offset)

    def toggle_launchpad(self):
        if self.control_center.isVisible():
            self.control_center.hide()
        if self.launchpad.isVisible():
            self.launchpad.hide()
        else:
            self.launchpad.show()
            self.launchpad.raise_()
            self.launchpad.search_input.setFocus()
            
    def toggle_control_center(self):
        if self.launchpad.isVisible():
            self.launchpad.hide()
        if self.control_center.isVisible():
            self.control_center.hide()
        else:
            self.control_center.show()
            self.control_center.raise_()
            
    def launch_random_app(self):
        app = random.choice(APPS_DATA)
        name, script, icon_name, color, desc = app
        launch_app(script)
        self.feedback_lbl.setText(f"Launched {name} ({desc})!")


def main():
    app = QApplication(sys.argv)
    useless_style.apply_corporate_style(app)
    
    screen = app.primaryScreen()
    screen_rect = screen.geometry()
    
    shell = UselessDesktopShell()
    shell.setGeometry(screen_rect)
    shell.show()
    shell.lower()
    
    def on_screen_changed(geo):
        shell.setGeometry(geo)
        shell.update()
        
    screen.geometryChanged.connect(on_screen_changed)
    if hasattr(screen, 'virtualGeometryChanged'):
        screen.virtualGeometryChanged.connect(on_screen_changed)
    
    run_app(app)


if __name__ == "__main__":
    main()
