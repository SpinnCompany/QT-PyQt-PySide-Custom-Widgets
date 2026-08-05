########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/@SpinnTV
# WEBSITE: customwidgets.org
########################################################################

########################################################################
## QCustomToast - non-blocking, auto-dismissing, corner-stacked
## notifications (success / error / warning / info).
##
## Unlike QCustomModals, toasts STACK in a corner and reflow as they
## close, managed by QCustomToastManager. Styled entirely from design
## tokens (see Custom_Widgets/JSonStyles/tokens.py); no bundled assets.
##
##     QCustomToast.success(window, "Saved!")
##     QCustomToast.error(window, "Failed", title="Upload", position="bottom-right")
########################################################################
from qtpy.QtCore import Qt, QTimer, QPropertyAnimation, Property, Signal
from qtpy.QtGui import QFont
from qtpy.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QLabel,
                            QPushButton, QGraphicsOpacityEffect)


_GLYPHS = {"success": "✓", "error": "✕", "warning": "!", "info": "i"}
_POSITIONS = ("top-right", "top-left", "bottom-right", "bottom-left",
              "top-center", "bottom-center")


class QCustomToastManager(object):
    """Singleton that stacks toasts per (parent, position) and reflows them as
    they appear and dismiss."""
    _instance = None
    MARGIN = 16
    GAP = 8

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        self._stacks = {}      # (parent, position) -> [toast, ...]

    def add(self, toast):
        parent = toast.parentWidget()
        if parent is None:
            return
        key = (parent, toast.position)
        self._stacks.setdefault(key, []).append(toast)
        toast.show()
        self.reflow(parent, toast.position)
        toast._fadeIn()
        if toast.duration and toast.duration > 0:
            QTimer.singleShot(int(toast.duration), toast.dismiss)

    def remove(self, toast):
        key = (toast.parentWidget(), toast.position)
        stack = self._stacks.get(key)
        if stack and toast in stack:
            stack.remove(toast)
            if stack:
                self.reflow(*key)
            else:
                self._stacks.pop(key, None)

    def stackFor(self, parent, position):
        return list(self._stacks.get((parent, position), []))

    def reflow(self, parent, position):
        if parent is None:
            return
        stack = self._stacks.get((parent, position), [])
        pw, ph = parent.width(), parent.height()
        offset = 0
        for toast in stack:
            toast.adjustSize()
            w, h = toast.width(), toast.height()
            if position.endswith("right"):
                x = pw - w - self.MARGIN
            elif position.endswith("left"):
                x = self.MARGIN
            else:                                  # center
                x = max(self.MARGIN, (pw - w) // 2)
            if position.startswith("top"):
                y = self.MARGIN + offset
            else:                                  # bottom: stack upward
                y = ph - self.MARGIN - h - offset
            toast.move(x, y)
            toast.raise_()
            offset += h + self.GAP


class QCustomToast(QWidget):
    """A single toast notification. Prefer the classmethods
    (success/error/warning/info/show_toast) which also register it with the
    manager for stacking."""

    closed = Signal()

    WIDTH = 340
    FADE_MS = 160

    __catalog__ = {
        "name": "QCustomToast",
        "props": {
            "variant": {"type": "enum",
                        "values": ["success", "error", "warning", "info"],
                        "default": "info"},
        },
        "signals": ["closed"],
        "tokens_used": ["surface", "on-surface", "surface-muted", "outline",
                        "success", "destructive", "warning", "info"],
    }

    def __init__(self, parent, message, variant="info", title=None,
                 duration=4000, closable=True, position="top-right"):
        super().__init__(parent)
        self._variant = variant if variant in _GLYPHS else "info"
        self.duration = duration
        self.position = position if position in _POSITIONS else "top-right"
        self._dismissing = False

        self.setObjectName("QCustomToast")
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setFixedWidth(self.WIDTH)

        row = QHBoxLayout(self)
        row.setContentsMargins(14, 12, 10, 12)
        row.setSpacing(10)

        self._icon = QLabel(_GLYPHS[self._variant], self)
        self._icon.setObjectName("toastIcon")
        f = QFont(); f.setBold(True); f.setPointSize(f.pointSize() + 2)
        self._icon.setFont(f)
        self._icon.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        self._icon.setFixedWidth(18)
        row.addWidget(self._icon)

        text = QVBoxLayout()
        text.setContentsMargins(0, 0, 0, 0)
        text.setSpacing(2)
        if title:
            self._title = QLabel(title, self)
            self._title.setObjectName("toastTitle")
            self._title.setWordWrap(True)
            text.addWidget(self._title)
        self._message = QLabel(message, self)
        self._message.setObjectName("toastMessage")
        self._message.setWordWrap(True)
        text.addWidget(self._message)
        row.addLayout(text, 1)

        self._close = QPushButton("✕", self)
        self._close.setObjectName("toastClose")
        self._close.setFixedSize(20, 20)
        self._close.setCursor(Qt.PointingHandCursor)
        self._close.clicked.connect(self.dismiss)
        self._close.setVisible(closable)
        row.addWidget(self._close, 0, Qt.AlignTop)

        self._opacity = QGraphicsOpacityEffect(self)
        self._opacity.setOpacity(0.0)
        self.setGraphicsEffect(self._opacity)
        self._fade = QPropertyAnimation(self._opacity, b"opacity", self)
        self._fade.setDuration(self.FADE_MS)

    # ------------------------------------------------------------------ #
    ## variant (declared Qt property; QSS reads it via the getter)
    # ------------------------------------------------------------------ #
    @Property(str)
    def variant(self):
        return self._variant

    @variant.setter
    def variant(self, value):
        self._variant = value if value in _GLYPHS else "info"
        self._icon.setText(_GLYPHS[self._variant])
        self.style().unpolish(self)
        self.style().polish(self)
        self.update()

    # ------------------------------------------------------------------ #
    ## Show / dismiss
    # ------------------------------------------------------------------ #
    def showToast(self):
        QCustomToastManager.instance().add(self)
        return self

    def _fadeIn(self):
        self._fade.stop()
        self._fade.setStartValue(self._opacity.opacity())
        self._fade.setEndValue(1.0)
        self._fade.start()

    def dismiss(self):
        if self._dismissing:
            return
        self._dismissing = True
        self._fade.stop()
        self._fade.setStartValue(self._opacity.opacity())
        self._fade.setEndValue(0.0)
        self._fade.finished.connect(self._afterFadeOut)
        self._fade.start()

    def _afterFadeOut(self):
        QCustomToastManager.instance().remove(self)
        self.closed.emit()
        self.deleteLater()

    # ------------------------------------------------------------------ #
    ## Convenience constructors
    # ------------------------------------------------------------------ #
    @classmethod
    def show_toast(cls, parent, message, variant="info", **kw):
        return cls(parent, message, variant=variant, **kw).showToast()

    @classmethod
    def success(cls, parent, message, **kw):
        return cls.show_toast(parent, message, variant="success", **kw)

    @classmethod
    def error(cls, parent, message, **kw):
        return cls.show_toast(parent, message, variant="error", **kw)

    @classmethod
    def warning(cls, parent, message, **kw):
        return cls.show_toast(parent, message, variant="warning", **kw)

    @classmethod
    def info(cls, parent, message, **kw):
        return cls.show_toast(parent, message, variant="info", **kw)
