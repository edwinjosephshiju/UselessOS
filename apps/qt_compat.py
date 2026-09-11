import sys

HAS_QT = False
PYQT6 = False
PYQT5 = False
PYSIDE6 = False
PYSIDE2 = False
QSvgWidget = None

try:
    from PyQt6.QtWidgets import *
    from PyQt6.QtCore import *
    from PyQt6.QtGui import *
    try:
        from PyQt6.QtSvgWidgets import QSvgWidget
    except ImportError:
        QSvgWidget = None
    PYQT6 = True
    HAS_QT = True
except ImportError:
    try:
        from PyQt5.QtWidgets import *
        from PyQt5.QtCore import *
        from PyQt5.QtGui import *
        try:
            from PyQt5.QtSvg import QSvgWidget
        except ImportError:
            QSvgWidget = None
        PYQT5 = True
        HAS_QT = True
    except ImportError:
        try:
            from PySide6.QtWidgets import *
            from PySide6.QtCore import *
            from PySide6.QtGui import *
            try:
                from PySide6.QtSvgWidgets import QSvgWidget
            except ImportError:
                QSvgWidget = None
            PYSIDE6 = True
            PYQT6 = True
            HAS_QT = True
        except ImportError:
            try:
                from PySide2.QtWidgets import *
                from PySide2.QtCore import *
                from PySide2.QtGui import *
                try:
                    from PySide2.QtSvg import QSvgWidget
                except ImportError:
                    QSvgWidget = None
                PYSIDE2 = True
                PYQT5 = True
                HAS_QT = True
            except ImportError:
                HAS_QT = False

# Scoped Enum compatibility or headless mock fallbacks
if HAS_QT:
    if PYQT6:
        AlignLeft = Qt.AlignmentFlag.AlignLeft
        AlignRight = Qt.AlignmentFlag.AlignRight
        AlignCenter = Qt.AlignmentFlag.AlignCenter
        Horizontal = Qt.Orientation.Horizontal
        Vertical = Qt.Orientation.Vertical
        FramelessWindowHint = Qt.WindowType.FramelessWindowHint
        FRAMELESS = FramelessWindowHint
        Dialog = Qt.WindowType.Dialog
        Window = Qt.WindowType.Window
        WindowStaysOnTopHint = Qt.WindowType.WindowStaysOnTopHint
        Tool = Qt.WindowType.Tool
        WA_TranslucentBackground = Qt.WidgetAttribute.WA_TranslucentBackground
        ApplicationModal = Qt.WindowModality.ApplicationModal
        PointingHandCursor = Qt.CursorShape.PointingHandCursor
        SizeHorCursor = Qt.CursorShape.SizeHorCursor
        SizeVerCursor = Qt.CursorShape.SizeVerCursor
        SizeFDiagCursor = Qt.CursorShape.SizeFDiagCursor
        SizeBDiagCursor = Qt.CursorShape.SizeBDiagCursor
        ArrowCursor = Qt.CursorShape.ArrowCursor
        LeftButton = Qt.MouseButton.LeftButton
    else:
        AlignLeft = Qt.AlignLeft
        AlignRight = Qt.AlignRight
        AlignCenter = Qt.AlignCenter
        Horizontal = Qt.Horizontal
        Vertical = Qt.Vertical
        FramelessWindowHint = Qt.FramelessWindowHint
        FRAMELESS = FramelessWindowHint
        Dialog = Qt.Dialog
        Window = Qt.Window
        WindowStaysOnTopHint = Qt.WindowStaysOnTopHint
        Tool = Qt.Tool
        WA_TranslucentBackground = Qt.WA_TranslucentBackground
        ApplicationModal = Qt.ApplicationModal
        PointingHandCursor = Qt.PointingHandCursor
        SizeHorCursor = Qt.SizeHorCursor
        SizeVerCursor = Qt.SizeVerCursor
        SizeFDiagCursor = Qt.SizeFDiagCursor
        SizeBDiagCursor = Qt.SizeBDiagCursor
        ArrowCursor = Qt.ArrowCursor
        LeftButton = Qt.LeftButton
else:
    # Fallback placeholders when running in minimal test/CI environments without Qt
    class _MockBase:
        def __init__(self, *args, **kwargs): pass
        def setStyleSheet(self, *args): pass
        def setObjectName(self, *args): pass
        def addWidget(self, *args, **kwargs): pass
        def addLayout(self, *args, **kwargs): pass
        def addStretch(self, *args): pass
        def setContentsMargins(self, *args): pass
        def setSpacing(self, *args): pass
        def show(self): pass
        def hide(self): pass
        def close(self): pass

    class _MockQt:
        class WindowType:
            FramelessWindowHint = 0
            Dialog = 0
            Window = 0
        class WindowModality:
            ApplicationModal = 0
        class WidgetAttribute:
            WA_TranslucentBackground = 0
        class AspectRatioMode:
            KeepAspectRatio = 0
        class TransformationMode:
            SmoothTransformation = 0
        FramelessWindowHint = 0
        Dialog = 0
        Window = 0
        ApplicationModal = 0
        WA_TranslucentBackground = 0
        KeepAspectRatio = 0
        SmoothTransformation = 0

    Qt = _MockQt
    QWidget = _MockBase
    QDialog = _MockBase
    QMainWindow = _MockBase
    QFrame = _MockBase
    QLabel = _MockBase
    QPushButton = _MockBase
    QScrollArea = _MockBase
    QTextEdit = _MockBase
    QLineEdit = _MockBase
    QSlider = _MockBase
    QProgressBar = _MockBase
    QHBoxLayout = _MockBase
    QVBoxLayout = _MockBase
    QGridLayout = _MockBase
    QGroupBox = _MockBase
    QApplication = _MockBase
    QTimer = _MockBase
    class _MockThread(_MockBase):
        def start(self):
            import threading
            t = threading.Thread(target=self.run, daemon=True)
            t.start()

    QThread = _MockThread
    QCursor = _MockBase
    QFontDatabase = _MockBase
    QPixmap = _MockBase
    QComboBox = _MockBase
    QRegion = _MockBase
    QPainterPath = _MockBase

    def pyqtSignal(*args, **kwargs):
        class _Signal:
            def __init__(self):
                self._callbacks = []
            def connect(self, cb):
                self._callbacks.append(cb)
            def emit(self, *a):
                for cb in list(self._callbacks):
                    try:
                        cb(*a)
                    except Exception:
                        pass
        return _Signal()

    AlignLeft = 1
    AlignRight = 2
    AlignCenter = 4
    Horizontal = 1
    Vertical = 2
    FramelessWindowHint = 0
    FRAMELESS = 0
    Dialog = 0
    Window = 0
    ApplicationModal = 0
    WindowStaysOnTopHint = 0
    Tool = 0
    WA_TranslucentBackground = 0
    PointingHandCursor = 0
    SizeHorCursor = 0
    SizeVerCursor = 0
    SizeFDiagCursor = 0
    SizeBDiagCursor = 0
    ArrowCursor = 0
    LeftButton = 1

def require_qt():
    if not HAS_QT:
        raise RuntimeError(
            "UselessOS requires PyQt6, PyQt5, or PySide6 to display graphical windows.\n"
            "Inside Debian / UselessOS VM: python3-pyqt6 is pre-installed.\n"
            "On host Windows / dev machines: install via `pip install PyQt6`."
        )

def run_app(app):
    require_qt()
    if PYQT6:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())
