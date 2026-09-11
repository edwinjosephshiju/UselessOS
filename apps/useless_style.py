import os
import sys
import functools
from qt_compat import *

_fonts_loaded = False

def load_custom_fonts():
    global _fonts_loaded
    if _fonts_loaded:
        return
    
    fonts_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts")
    if os.path.exists(fonts_dir):
        for font_file in os.listdir(fonts_dir):
            if font_file.endswith((".otf", ".ttf")):
                full_path = os.path.join(fonts_dir, font_file)
                QFontDatabase.addApplicationFont(full_path)
    _fonts_loaded = True

@functools.lru_cache(maxsize=128)
def get_icon_path(filename):
    if not filename:
        return None
    script_dir = os.path.dirname(os.path.abspath(__file__))
    candidates = [
        os.path.join(script_dir, "assets", "icons", filename),
        os.path.join(script_dir, "assets", filename),
        os.path.join("/opt", "uselessos", "assets", "icons", filename),
        os.path.join("/opt", "uselessos", "assets", filename),
    ]
    for c in candidates:
        if os.path.exists(c):
            return c
    return None

@functools.lru_cache(maxsize=128)
def get_asset_path(filename):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    candidates = [
        os.path.join(script_dir, "assets", filename),
        os.path.join("/opt", "uselessos", "assets", filename),
    ]
    for c in candidates:
        if os.path.exists(c):
            return c
    return None

APP_GUIDES = {
    "Excuse Generator™": {
        "how_to_use": [
            "Select an excuse archetype (e.g. Spatiotemporal Anomalies, Sentient Infrastructure).",
            "Pick the intended recipient (e.g. Direct Line Manager, Team Slack Channel).",
            "Adjust the Absurdity Calibration slider to tune believability vs chaos.",
            "Click 'GENERATE BINDING CORPORATE EXCUSE' to produce a bullet-proof mitigation excuse."
        ],
        "philosophy": "In hyper-productive corporate environments, honesty creates meetings. A sufficiently convoluted spatiotemporal anomaly creates profound silence and automatic PTO approval."
    },
    "Overthinking Engine™": {
        "how_to_use": [
            "Enter any mundane everyday decision (e.g. 'Should I reply to this email now?').",
            "Click 'SIMULATE 14,000,605 SCENARIOS' to calculate catastrophic branch probabilities.",
            "Review the Catastrophe Confidence Index and paralysis telemetry."
        ],
        "philosophy": "Why make a simple decision in 5 seconds when you can calculate 14 million catastrophic timelines for 4 hours and conclude that taking no action is safest?"
    },
    "AI That Says Hmm™": {
        "how_to_use": [
            "Type any deep existential dilemma, moral question, or technical query into the input.",
            "Click 'Ask AI' or press Enter to invoke the Qwen 3.5 0.8B cognitive backend.",
            "Observe the token streaming and telemetry as it engages in profound deliberation."
        ],
        "philosophy": "Modern LLMs hallucinate false certainty. Qwen 3.5 0.8B in UselessOS respects cosmic ambiguity: when faced with reality, the only truly honest answer is 'Hmm...'."
    },
    "Uselessness Analytics™": {
        "how_to_use": [
            "Observe live enterprise procrastination throughput and dopamine decay metrics.",
            "Review the Spatiotemporal Drift and Circular Logic coefficients.",
            "Click 'Run Audit' to re-certify that zero tangible value was created."
        ],
        "philosophy": "Corporate dashboards measure output regardless of utility. Here, we measure lack of utility with enterprise rigor, proving that idleness is quantifiable science."
    },
    "Screen Time™": {
        "how_to_use": [
            "Monitor real-time consumption of glowing rectangle photons.",
            "Toggle between 'Existential Despair' and 'Digital Dissociation' telemetry.",
            "Click 'Log More Screen Time' to deepen your dedication to the void."
        ],
        "philosophy": "Other screen time apps shame you into touching grass. Screen Time celebrates your loyal commitment to the phosphor glow of digital delusion."
    },
    "Existential Crisis Tracker™": {
        "how_to_use": [
            "Inspect telemetry: Sense of Purpose, Monday Motivation, Bloodstream Caffeine.",
            "Consult the System Recommendation (e.g. 'Have some water').",
            "Increment the 'Why am I doing this?' counter whenever dread peaks."
        ],
        "philosophy": "Awareness of one's cosmic insignificance is the first step toward enjoying a pointless cup of tea. We track the void so the void doesn't sneak up on you."
    },
    "Emotional Bin™": {
        "how_to_use": [
            "Type negative emotions, imposter syndrome, or annoying thoughts into the incinerator.",
            "Click 'DISCARD & SHRED' to watch them vanish forever into the digital incinerator."
        ],
        "philosophy": "Closure is overrated and therapy takes time. Emotional Bin offers an unceremonious byte-level /dev/null deletion for all psychological baggage."
    },
    "Useless Alarm™": {
        "how_to_use": [
            "Select your desired wake-up hour (or sleep procrastination window).",
            "Set the Snooze Permissiveness slider to maximum.",
            "Click 'Arm Alarm' — when it rings, it will politely suggest going back to sleep."
        ],
        "philosophy": "Waking up early is a social construct. Useless Alarm believes in honoring your circadian rebellion by actively encouraging naps."
    },
    "System Settings": {
        "how_to_use": [
            "Navigate the macOS-style sidebar: General, Desktop, Display, Sound, Impracticality.",
            "Toggle placebos such as 'Hyper-Threading Coffee Machine' and 'Dark Mode Sarcasm'.",
            "Adjust sliders that change absolutely nothing with high precision."
        ],
        "philosophy": "The illusion of control is the foundation of modern operating systems. Here, you have total control over settings that intentionally effect zero changes."
    },
    "Useless Terminal™": {
        "how_to_use": [
            "Type standard UNIX commands like 'help', 'status', 'why', 'overthink', 'sudo', or 'matrix'.",
            "Experience a terminal environment engineered to answer everything with philosophical absurdity."
        ],
        "philosophy": "UNIX was designed for deterministic computing. Useless Terminal restores poetry to the shell prompt, proving that not all pipelines need an exit code of 0."
    }
}

class CustomTitleBar(QWidget):
    """
    macOS-inspired brutalist window title bar with traffic light controls,
    bespoke squircle app icon, bold typography, and smooth mouse window dragging.
    """
    def __init__(self, parent=None, title="Application", subtitle="", icon_name="", accent_color="#ea34df"):
        super().__init__(parent)
        self.parent_window = parent
        self.setFixedHeight(42)
        self.setObjectName("CustomTitleBar")
        self.setStyleSheet("""
            #CustomTitleBar {
                background-color: #f5f4f0;
                border-bottom: 2px solid #0e0e0d;
                border-top-left-radius: 14px;
                border-top-right-radius: 14px;
            }
        """)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(14, 0, 14, 0)
        layout.setSpacing(10)
        layout.setAlignment(Qt.AlignmentFlag.AlignVCenter if PYQT6 else Qt.AlignVCenter)
        
        # 1. macOS Traffic Light Window Controls
        lights = QHBoxLayout()
        lights.setSpacing(8)
        lights.setContentsMargins(0, 0, 8, 0)
        
        # Close (Red)
        self.btn_close = QPushButton("✕", self)
        self.btn_close.setToolTip("Close")
        self.btn_close.setFixedSize(14, 14)
        self.btn_close.setCursor(QCursor(PointingHandCursor))
        self.btn_close.setStyleSheet("""
            QPushButton {
                background-color: #ff5f56;
                color: transparent;
                border: 1.5px solid #0e0e0d;
                border-radius: 7px;
                font-size: 8px;
                font-weight: 900;
                padding: 0px;
            }
            QPushButton:hover {
                color: #5c0000;
                background-color: #ff5f56;
            }
        """)
        self.btn_close.clicked.connect(self.parent_window.close)
        lights.addWidget(self.btn_close)
        
        # Minimize (Yellow)
        self.btn_min = QPushButton("—", self)
        self.btn_min.setToolTip("Minimize")
        self.btn_min.setFixedSize(14, 14)
        self.btn_min.setCursor(QCursor(PointingHandCursor))
        self.btn_min.setStyleSheet("""
            QPushButton {
                background-color: #ffbd2e;
                color: transparent;
                border: 1.5px solid #0e0e0d;
                border-radius: 7px;
                font-size: 8px;
                font-weight: 900;
                padding: 0px;
            }
            QPushButton:hover {
                color: #5c3b00;
                background-color: #ffbd2e;
            }
        """)
        self.btn_min.clicked.connect(self.parent_window.showMinimized)
        lights.addWidget(self.btn_min)
        
        # Maximize / Restore (Green)
        self.btn_max = QPushButton("+", self)
        self.btn_max.setToolTip("Maximize / Restore")
        self.btn_max.setFixedSize(14, 14)
        self.btn_max.setCursor(QCursor(PointingHandCursor))
        self.btn_max.setStyleSheet("""
            QPushButton {
                background-color: #27c93f;
                color: transparent;
                border: 1.5px solid #0e0e0d;
                border-radius: 7px;
                font-size: 8px;
                font-weight: 900;
                padding: 0px;
            }
            QPushButton:hover {
                color: #004d10;
                background-color: #27c93f;
            }
        """)
        self.btn_max.clicked.connect(self.parent_window.toggle_maximized)
        lights.addWidget(self.btn_max)
        
        layout.addLayout(lights)
        
        # 2. Bespoke Squircle App Icon
        icon_path = get_icon_path(icon_name)
        if icon_path and os.path.exists(icon_path):
            icon_lbl = QLabel()
            pix = QPixmap(icon_path).scaled(22, 22, Qt.AspectRatioMode.KeepAspectRatio if PYQT6 else Qt.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation if PYQT6 else Qt.SmoothTransformation)
            icon_lbl.setPixmap(pix)
            icon_lbl.setFixedSize(22, 22)
            icon_lbl.setStyleSheet("background: transparent; border: none;")
            layout.addWidget(icon_lbl)
            
        # 3. App Title (Helvetica Bold)
        title_lbl = QLabel(title)
        title_lbl.setStyleSheet("font-family: Helvetica; font-size: 11pt; font-weight: 900; color: #0e0e0d; background: transparent; border: none;")
        layout.addWidget(title_lbl)
        
        # 4. Whimsical Handwritten Tagline (NanumPenScript)
        if subtitle:
            sub_lbl = QLabel(f"•  {subtitle}")
            sub_lbl.setStyleSheet(f"font-family: 'NanumPenScript', 'Nanum Pen Script', cursive; font-size: 13pt; font-weight: bold; color: {accent_color}; background: transparent; border: none;")
            layout.addWidget(sub_lbl)
            
        layout.addStretch()
        
        # 5. OS Badge Pill
        pill = QLabel("UselessOS 3.0")
        pill.setStyleSheet("""
            QLabel {
                background-color: #ffffff;
                color: #0e0e0d;
                border: 1.5px solid #0e0e0d;
                border-radius: 10px;
                font-family: Helvetica;
                font-size: 8pt;
                font-weight: 800;
                padding: 2px 8px;
            }
        """)
        layout.addWidget(pill)
        
        # 6. Question Mark Button for App Instructions & Logic
        self.btn_help = QPushButton("?", self)
        self.btn_help.setToolTip("Application Instructions & Philosophical Logic")
        self.btn_help.setCursor(QCursor(PointingHandCursor))
        self.btn_help.setFixedSize(22, 22)
        self.btn_help.setStyleSheet("""
            QPushButton {
                background-color: #ffffff;
                color: #0e0e0d;
                border: 1.5px solid #0e0e0d;
                border-radius: 11px;
                font-family: Helvetica;
                font-size: 9pt;
                font-weight: 900;
                padding: 0px;
            }
            QPushButton:hover {
                background-color: #00c2cb;
                color: #ffffff;
                border: 1.5px solid #0e0e0d;
            }
        """)
        self.btn_help.clicked.connect(self.parent_window.show_instructions_dialog)
        layout.addWidget(self.btn_help)
        
        # Mouse dragging state
        self._drag_pos = None

    def mouseDoubleClickEvent(self, event):
        if event.button() == (Qt.MouseButton.LeftButton if PYQT6 else Qt.LeftButton):
            self.parent_window.toggle_maximized()
            event.accept()

    def mousePressEvent(self, event):
        if event.button() == (Qt.MouseButton.LeftButton if PYQT6 else Qt.LeftButton):
            if self.parent_window._is_maximized:
                self.parent_window.toggle_maximized()
            pos = event.globalPosition().toPoint() if hasattr(event, 'globalPosition') else event.globalPos()
            self._drag_pos = pos - self.parent_window.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if self._drag_pos is not None and (event.buttons() & (Qt.MouseButton.LeftButton if PYQT6 else Qt.LeftButton)):
            pos = event.globalPosition().toPoint() if hasattr(event, 'globalPosition') else event.globalPos()
            target_pos = pos - self._drag_pos
            screen_geo = QApplication.primaryScreen().availableGeometry()
            # Strict macOS top-bar boundary: never allow titlebar above y=40
            clamped_y = max(screen_geo.y() + 40, target_pos.y())
            clamped_x = max(screen_geo.x() - self.parent_window.width() + 80, min(screen_geo.right() - 80, target_pos.x()))
            self.parent_window.move(clamped_x, clamped_y)
            event.accept()

    def mouseReleaseEvent(self, event):
        self._drag_pos = None


class UselessWindow(QMainWindow):
    """
    Standard window framework for all UselessOS applications.
    Renders a unified macOS-inspired brutalist frame with custom traffic lights,
    crisp 2px solid #0e0e0d borders, 16px radius, dedicated content area,
    and a robust core-level 8-directional frameless resizing engine.
    """
    RESIZE_MARGIN = 8

    def __init__(self, title="Useless Application", subtitle="", icon_name="", accent_color="#ea34df", width=620, height=520, parent=None):
        super().__init__(parent)
        self.app_title = title
        self.app_subtitle = subtitle
        self.app_icon = icon_name
        self.app_accent = accent_color

        self.setWindowTitle(f"{title} - UselessOS")
        self.resize(width, height)
        
        # Responsive minimum size
        min_w = max(340, min(width, 400))
        min_h = max(240, min(height, 300))
        self.setMinimumSize(min_w, min_h)
        
        # Frameless window with custom rounded corners
        self.setWindowFlags(FramelessWindowHint)
        self.setAttribute(WA_TranslucentBackground)
        self.setMouseTracking(True)
        
        # Center window on screen
        screen = QApplication.primaryScreen().availableGeometry()
        self.move(screen.x() + max(20, (screen.width() - width) // 2), screen.y() + max(50, (screen.height() - height) // 2 - 20))
        
        # Main root frame with 2px solid border and rounded corners
        self.root_frame = QFrame(self)
        self.root_frame.setObjectName("UselessRootFrame")
        self.root_frame.setMouseTracking(True)
        self.root_frame.setStyleSheet("""
            #UselessRootFrame {
                background-color: #ffffff;
                border: 2px solid #0e0e0d;
                border-radius: 16px;
            }
        """)
        self.setCentralWidget(self.root_frame)
        
        self.main_layout = QVBoxLayout(self.root_frame)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        # macOS Custom Title Bar
        self.title_bar = CustomTitleBar(self, title=title, subtitle=subtitle, icon_name=icon_name, accent_color=accent_color)
        self.main_layout.addWidget(self.title_bar)
        
        # Scroll area for robust scaling on low-resolution displays
        self.scroll_area = QScrollArea(self.root_frame)
        self.scroll_area.setObjectName("UselessScrollArea")
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.Shape.NoFrame if PYQT6 else QFrame.NoFrame)
        self.scroll_area.setStyleSheet("""
            #UselessScrollArea {
                background-color: transparent;
                border: none;
            }
            QScrollBar:vertical {
                border: 1.5px solid #0e0e0d;
                background: #f5f4f0;
                width: 10px;
                border-radius: 5px;
                margin: 4px 6px 6px 0px;
            }
            QScrollBar::handle:vertical {
                background: #0e0e0d;
                border-radius: 3px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: #ea34df;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QScrollBar:horizontal {
                height: 0px;
            }
        """)
        
        # Content Container
        self.content_widget = QWidget(self.scroll_area)
        self.content_widget.setObjectName("UselessContentWidget")
        self.content_widget.setStyleSheet("""
            #UselessContentWidget {
                background-color: #ffffff;
                border: none;
                border-bottom-left-radius: 14px;
                border-bottom-right-radius: 14px;
            }
        """)
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(20, 16, 20, 20)
        self.content_layout.setSpacing(14)
        
        self.scroll_area.setWidget(self.content_widget)
        self.main_layout.addWidget(self.scroll_area)
        
        self._is_maximized = False
        self._normal_geo = None
        
        # Resizing state
        self._resizing = False
        self._resize_edges = (False, False, False, False)
        self._press_pos = None
        self._press_geo = None
        
        # Install event filter to capture mouse events on root frame for edge resizing
        self.root_frame.installEventFilter(self)
        
        # Screen geometry listener for adaptive scaling
        app = QApplication.instance()
        if app and app.primaryScreen():
            app.primaryScreen().geometryChanged.connect(self._on_screen_changed)
            
        self._update_window_mask()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._update_window_mask()

    def _update_window_mask(self):
        """Shape masking: cuts transparent corners cleanly so raw X11 never renders black triangles."""
        try:
            path = QPainterPath()
            path.addRoundedRect(0.0, 0.0, float(self.width()), float(self.height()), 16.0, 16.0)
            self.setMask(QRegion(path.toFillPolygon().toPolygon()))
        except Exception:
            pass

    def show_instructions_dialog(self):
        """Displays in-app operation manual and philosophical satirical logic."""
        info = APP_GUIDES.get(self.app_title, None)
        if not info:
            for k in APP_GUIDES:
                if k.lower() in self.app_title.lower() or self.app_title.lower() in k.lower():
                    info = APP_GUIDES[k]
                    break
        if not info:
            info = {
                "how_to_use": [
                    "Interact with the controls, buttons, and inputs on screen.",
                    "Enjoy the complete lack of measurable productivity.",
                    "Observe how peaceful idleness feels in an over-engineered world."
                ],
                "philosophy": "Every application in UselessOS is an aesthetic celebration of digital futility, challenging the assumption that all software must generate shareholder value."
            }

        dlg = QDialog(self)
        dlg.setWindowTitle(f"About {self.app_title}")
        dlg_w = 560
        dlg_h = 560
        dlg.setFixedSize(dlg_w, dlg_h)
        dlg.setWindowFlags((Qt.WindowType.Dialog if PYQT6 else Qt.Dialog) | (Qt.WindowType.FramelessWindowHint if PYQT6 else Qt.FramelessWindowHint))
        dlg.setAttribute(WA_TranslucentBackground)
        if hasattr(Qt, 'WindowModality') and hasattr(Qt.WindowModality, 'ApplicationModal'):
            dlg.setWindowModality(Qt.WindowModality.ApplicationModal)
        elif hasattr(Qt, 'ApplicationModal'):
            dlg.setWindowModality(Qt.ApplicationModal)

        d_frame = QFrame(dlg)
        d_frame.setObjectName("InstructionsModalFrame")
        d_frame.setStyleSheet("""
            QFrame#InstructionsModalFrame {
                background-color: #ffffff;
                border: 2.5px solid #0e0e0d;
                border-radius: 20px;
            }
        """)

        d_root_lay = QVBoxLayout(dlg)
        d_root_lay.setContentsMargins(0, 0, 0, 0)
        d_root_lay.addWidget(d_frame)

        d_lay = QVBoxLayout(d_frame)
        d_lay.setContentsMargins(22, 18, 22, 18)
        d_lay.setSpacing(10)

        # Top Header (Row 1: Icon, Title, Badge)
        top_h = QHBoxLayout()
        top_h.setSpacing(10)
        icon_path = get_icon_path(self.app_icon)
        if icon_path and os.path.exists(icon_path):
            icon_lbl = QLabel()
            pix = QPixmap(icon_path).scaled(34, 34, Qt.AspectRatioMode.KeepAspectRatio if PYQT6 else Qt.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation if PYQT6 else Qt.SmoothTransformation)
            icon_lbl.setPixmap(pix)
            icon_lbl.setStyleSheet("background: transparent; border: none;")
            top_h.addWidget(icon_lbl)

        t_label = QLabel(self.app_title)
        t_label.setStyleSheet("font-family: Helvetica; font-size: 14pt; font-weight: 900; color: #0e0e0d; background: transparent; border: none;")
        top_h.addWidget(t_label)
        top_h.addStretch()

        badge = QLabel("Useless Guide")
        badge.setStyleSheet("background: #0e0e0d; color: #ffffff; border-radius: 8px; font-size: 8pt; font-weight: 800; padding: 4px 10px; font-family: Helvetica;")
        top_h.addWidget(badge)
        d_lay.addLayout(top_h)

        # Row 2: Subtitle (Full width, wrapped if necessary, completely avoiding badge collision)
        if self.app_subtitle:
            st_label = QLabel(f"•  {self.app_subtitle}")
            st_label.setWordWrap(True)
            st_label.setStyleSheet(f"font-family: 'NanumPenScript', cursive; font-size: 13pt; color: {self.app_accent}; background: transparent; border: none; margin-top: -2px;")
            d_lay.addWidget(st_label)

        # 1. How To Use GroupBox
        box_use = QGroupBox("HOW TO OPERATE THIS APPLICATION")
        box_use.setStyleSheet("""
            QGroupBox {
                border: 2px solid #0e0e0d;
                border-radius: 12px;
                margin-top: 14px;
                background-color: #f5f4f0;
                font-family: Helvetica;
                font-weight: 800;
                font-size: 8.5pt;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 2px 10px;
                background: #0e0e0d;
                color: #ffffff;
                border-radius: 6px;
                font-size: 8pt;
                font-weight: 900;
                left: 14px;
            }
        """)
        u_lay = QVBoxLayout(box_use)
        u_lay.setContentsMargins(14, 16, 14, 12)
        u_lay.setSpacing(6)
        for idx, step in enumerate(info["how_to_use"], 1):
            lbl = QLabel(f"<b>{idx}.</b> {step}")
            lbl.setWordWrap(True)
            lbl.setStyleSheet("font-family: Helvetica; font-size: 8.5pt; color: #0e0e0d; background: transparent; border: none; line-height: 130%;")
            u_lay.addWidget(lbl)
        d_lay.addWidget(box_use)

        # 2. Philosophical Logic GroupBox
        box_phil = QGroupBox("THE IMPRACTICAL PHILOSOPHY & LOGIC")
        box_phil.setStyleSheet("""
            QGroupBox {
                border: 2px solid #0e0e0d;
                border-radius: 12px;
                margin-top: 14px;
                background-color: #ffffff;
                font-family: Helvetica;
                font-weight: 800;
                font-size: 8.5pt;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 2px 10px;
                background: #ea34df;
                color: #ffffff;
                border-radius: 6px;
                font-size: 8pt;
                font-weight: 900;
                left: 14px;
            }
        """)
        p_lay = QVBoxLayout(box_phil)
        p_lay.setContentsMargins(14, 16, 14, 12)
        phil_lbl = QLabel(f"<i>\"{info['philosophy']}\"</i>")
        phil_lbl.setWordWrap(True)
        phil_lbl.setStyleSheet("font-family: Helvetica; font-size: 8.5pt; color: #244638; background: transparent; border: none; line-height: 135%;")
        p_lay.addWidget(phil_lbl)
        d_lay.addWidget(box_phil)

        d_lay.addStretch()

        # Close Button
        btn_close = QPushButton("Understood (Carry On)")
        btn_close.setCursor(QCursor(PointingHandCursor))
        btn_close.setFixedHeight(38)
        btn_close.setStyleSheet("""
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
                background-color: #00c2cb;
                color: #0e0e0d;
            }
        """)
        btn_close.clicked.connect(dlg.accept)
        d_lay.addWidget(btn_close)

        # Center dialog over parent window, clamped within screen bounds
        p_geo = self.geometry()
        center_x = p_geo.x() + (p_geo.width() - dlg_w) // 2
        center_y = p_geo.y() + (p_geo.height() - dlg_h) // 2
        screen = QApplication.primaryScreen()
        if screen:
            s_geo = screen.availableGeometry()
            center_x = max(s_geo.x() + 10, min(center_x, s_geo.right() - dlg_w - 10))
            center_y = max(s_geo.y() + 44, min(center_y, s_geo.bottom() - dlg_h - 10))
        dlg.move(center_x, center_y)

        # Enable mouse dragging for the dialog
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

    def _on_screen_changed(self, geo):
        if self._is_maximized:
            top_y = geo.y() + 46
            self.setGeometry(geo.x() + 8, top_y, geo.width() - 16, max(300, geo.height() - 46 - 94))

    def toggle_maximized(self):
        if self._is_maximized:
            if self._normal_geo:
                self.setGeometry(self._normal_geo)
            else:
                self.showNormal()
            self._is_maximized = False
        else:
            self._normal_geo = self.geometry()
            screen = QApplication.primaryScreen().availableGeometry()
            top_y = screen.y() + 46
            self.setGeometry(screen.x() + 8, top_y, screen.width() - 16, max(300, screen.height() - 46 - 94))
            self._is_maximized = True

    def _get_active_edges(self, pos):
        if self._is_maximized:
            return (False, False, False, False)
        m = self.RESIZE_MARGIN
        w = self.width()
        h = self.height()
        top = pos.y() < m
        bottom = pos.y() >= h - m
        left = pos.x() < m
        right = pos.x() >= w - m
        return (top, bottom, left, right)

    def _update_cursor_shape(self, edges):
        top, bottom, left, right = edges
        if (top and left) or (bottom and right):
            self.setCursor(QCursor(SizeFDiagCursor))
            self.root_frame.setCursor(QCursor(SizeFDiagCursor))
        elif (top and right) or (bottom and left):
            self.setCursor(QCursor(SizeBDiagCursor))
            self.root_frame.setCursor(QCursor(SizeBDiagCursor))
        elif left or right:
            self.setCursor(QCursor(SizeHorCursor))
            self.root_frame.setCursor(QCursor(SizeHorCursor))
        elif top or bottom:
            self.setCursor(QCursor(SizeVerCursor))
            self.root_frame.setCursor(QCursor(SizeVerCursor))
        else:
            self.unsetCursor()
            self.root_frame.unsetCursor()

    def eventFilter(self, obj, event):
        if obj is self.root_frame or obj is self:
            t = event.type()
            
            # 1. Mouse Move: Update cursor or resize window
            if t == QEvent.Type.MouseMove if PYQT6 else QEvent.MouseMove:
                g_pos = event.globalPosition().toPoint() if hasattr(event, 'globalPosition') else event.globalPos()
                if self._resizing and self._press_pos and self._press_geo:
                    dx = g_pos.x() - self._press_pos.x()
                    dy = g_pos.y() - self._press_pos.y()
                    top, bottom, left, right = self._resize_edges
                    
                    geo = QRect(self._press_geo)
                    min_w = self.minimumWidth()
                    min_h = self.minimumHeight()
                    
                    if left:
                        new_w = max(min_w, geo.width() - dx)
                        new_x = geo.right() - new_w + 1
                        geo.setLeft(new_x)
                    elif right:
                        geo.setWidth(max(min_w, geo.width() + dx))
                        
                    if top:
                        new_h = max(min_h, geo.height() - dy)
                        new_y = geo.bottom() - new_h + 1
                        screen_geo = QApplication.primaryScreen().availableGeometry()
                        if new_y < screen_geo.y() + 40:
                            new_y = screen_geo.y() + 40
                            new_h = geo.bottom() - new_y + 1
                        geo.setTop(new_y)
                    elif bottom:
                        geo.setHeight(max(min_h, geo.height() + dy))
                        
                    self.setGeometry(geo)
                    return True
                else:
                    local_pos = self.mapFromGlobal(g_pos)
                    edges = self._get_active_edges(local_pos)
                    self._update_cursor_shape(edges)
                    
            # 2. Mouse Press: Begin resize if on edge
            elif t == QEvent.Type.MouseButtonPress if PYQT6 else QEvent.MouseButtonPress:
                btn = event.button()
                if btn == (Qt.MouseButton.LeftButton if PYQT6 else Qt.LeftButton):
                    g_pos = event.globalPosition().toPoint() if hasattr(event, 'globalPosition') else event.globalPos()
                    local_pos = self.mapFromGlobal(g_pos)
                    edges = self._get_active_edges(local_pos)
                    if any(edges):
                        self._resizing = True
                        self._resize_edges = edges
                        self._press_pos = g_pos
                        self._press_geo = self.geometry()
                        return True
                        
            # 3. Mouse Release: End resize
            elif t == QEvent.Type.MouseButtonRelease if PYQT6 else QEvent.MouseButtonRelease:
                if self._resizing:
                    self._resizing = False
                    self._press_pos = None
                    self._press_geo = None
                    self.unsetCursor()
                    self.root_frame.unsetCursor()
                    return True
                    
            # 4. Leave event: Reset cursor
            elif t == QEvent.Type.Leave if PYQT6 else QEvent.Leave:
                if not self._resizing:
                    self.unsetCursor()
                    self.root_frame.unsetCursor()
                    
        return super().eventFilter(obj, event)


def apply_corporate_style(app: QApplication):
    load_custom_fonts()
    
    try:
        if hasattr(Qt.ApplicationAttribute, 'AA_EnableHighDpiScaling'):
            app.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)
        if hasattr(Qt.ApplicationAttribute, 'AA_UseHighDpiPixmaps'):
            app.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps, True)
        if hasattr(Qt, 'HighDpiScaleFactorRoundingPolicy'):
            app.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    except Exception:
        pass
        
    app.setStyle("Fusion")
    
    font = QFont("Helvetica", 11)
    app.setFont(font)
    
    stylesheet = """
    QWidget {
        color: #0e0e0d;
        font-family: "Helvetica", -apple-system, BlinkMacSystemFont, "Segoe UI", Arial, sans-serif;
    }
    QMainWindow, QDialog {
        background-color: #ffffff;
    }
    
    /* Hover Windows / Tooltips matching TinkerHub Brutalist Theme */
    QToolTip {
        background-color: #ffffff;
        color: #0e0e0d;
        border: 2px solid #0e0e0d;
        border-radius: 8px;
        padding: 6px 12px;
        font-family: "Helvetica", sans-serif;
        font-size: 9pt;
        font-weight: 800;
    }
    
    /* Brutalist Cards */
    QGroupBox {
        border: 2px solid #0e0e0d;
        border-radius: 14px;
        margin-top: 20px;
        background-color: #ffffff;
        font-weight: 700;
    }
    QGroupBox::title {
        subcontrol-origin: margin;
        subcontrol-position: top center;
        padding: 3px 14px;
        color: #0e0e0d;
        font-weight: 800;
        font-size: 10pt;
        background-color: #f5f4f0;
        border: 2px solid #0e0e0d;
        border-radius: 10px;
    }
    
    /* Pill Buttons matching the desktop hero buttons */
    QPushButton {
        background-color: #0e0e0d;
        color: #ffffff;
        border: 2px solid #0e0e0d;
        border-radius: 20px;
        padding: 10px 22px;
        font-weight: 800;
        font-size: 10.5pt;
        font-family: "Helvetica";
    }
    QPushButton:hover {
        background-color: #ea34df;
        color: #ffffff;
        border: 2px solid #0e0e0d;
    }
    QPushButton:pressed {
        background-color: #c0326b;
    }
    QPushButton:disabled {
        background-color: #e5e5e0;
        color: #888880;
        border: 2px solid #b5b5b0;
    }
    
    /* Inputs */
    QLineEdit, QTextEdit, QTimeEdit, QSpinBox {
        background-color: #ffffff;
        color: #0e0e0d;
        border: 2px solid #0e0e0d;
        border-radius: 12px;
        padding: 8px 12px;
        font-size: 10.5pt;
    }
    QComboBox {
        background-color: #ffffff;
        color: #0e0e0d;
        border: 2px solid #0e0e0d;
        border-radius: 12px;
        padding: 4px 10px;
        font-size: 10pt;
        font-weight: 700;
        min-height: 28px;
    }
    QLineEdit:focus, QTextEdit:focus, QComboBox:focus, QTimeEdit:focus, QSpinBox:focus {
        border: 2px solid #ea34df;
    }
    QComboBox::drop-down {
        border: none;
        width: 26px;
    }
    QComboBox QAbstractItemView {
        border: 2px solid #0e0e0d;
        border-radius: 8px;
        background-color: #ffffff;
        color: #0e0e0d;
        selection-background-color: #ea34df;
        selection-color: #ffffff;
        padding: 4px;
    }
    
    /* Custom Sliders */
    QSlider::groove:horizontal {
        border: 2px solid #0e0e0d;
        height: 10px;
        background: #f5f4f0;
        border-radius: 5px;
    }
    QSlider::sub-page:horizontal {
        background: #ea34df;
        border: 2px solid #0e0e0d;
        border-radius: 5px;
    }
    QSlider::handle:horizontal {
        background: #ffffff;
        border: 2px solid #0e0e0d;
        width: 22px;
        margin-top: -6px;
        margin-bottom: -6px;
        border-radius: 11px;
    }
    QSlider::handle:horizontal:hover {
        background: #0e0e0d;
    }
    
    /* Progress Bars */
    QProgressBar {
        border: 2px solid #0e0e0d;
        border-radius: 12px;
        text-align: center;
        background-color: #ffffff;
        color: #0e0e0d;
        font-weight: 800;
        height: 22px;
    }
    QProgressBar::chunk {
        background-color: #244638;
        border-radius: 8px;
        margin: 2px;
    }
    
    /* Typography */
    QLabel#corp_title {
        color: #0e0e0d;
        font-family: "Drowner", "Helvetica", sans-serif;
        font-size: 20pt;
        font-weight: 900;
    }
    QLabel#corp_subtitle {
        color: #e82803;
        font-family: "NanumPenScript", "Nanum Pen Script", cursive;
        font-size: 14pt;
        font-weight: bold;
    }
    
    /* Lists */
    QListWidget {
        background-color: #ffffff;
        border: 2px solid #0e0e0d;
        border-radius: 12px;
        padding: 6px;
    }
    QListWidget::item {
        border-radius: 8px;
        padding: 6px 10px;
    }
    QListWidget::item:selected {
        background-color: #ea34df;
        color: #ffffff;
    }
    
    /* Scrollbars */
    QScrollBar:vertical {
        border: 1px solid #0e0e0d;
        background: #f5f4f0;
        width: 12px;
        border-radius: 6px;
        margin: 0px;
    }
    QScrollBar::handle:vertical {
        background: #0e0e0d;
        border-radius: 5px;
        min-height: 20px;
    }
    /* Tooltips matching Useless Projects 3.0 Brutalist Aesthetic */
    QToolTip {
        background-color: #ffffff;
        color: #0e0e0d;
        border: 2px solid #0e0e0d;
        border-radius: 10px;
        padding: 8px 12px;
        font-family: "Helvetica", sans-serif;
        font-size: 9pt;
        font-weight: 700;
    }
    """
    app.setStyleSheet(stylesheet)
