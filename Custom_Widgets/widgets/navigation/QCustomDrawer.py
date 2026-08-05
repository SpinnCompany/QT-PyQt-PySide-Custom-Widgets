########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/@SpinnTV
# WEBSITE: customwidgets.org
########################################################################

########################################################################
## QCustomDrawer - a slide-in side panel / sheet.
##
## A dimmed overlay with a panel that slides in from an edge (left / right /
## top / bottom). Backdrop-click or Esc closes it. Tokenized.
##
##     drawer = QCustomDrawer(window, side="left", size=280)
##     drawer.contentLayout().addWidget(nav)
##     drawer.open()
########################################################################
from qtpy.QtCore import Qt, Signal, QPoint, QPropertyAnimation, QEasingCurve
from qtpy.QtWidgets import QWidget, QFrame, QVBoxLayout, QGraphicsOpacityEffect


_SIDES = ("left", "right", "top", "bottom")


class QCustomDrawer(QWidget):
    opened = Signal()
    closed = Signal()
    SLIDE_MS = 220

    __catalog__ = {
        "name": "QCustomDrawer",
        "props": {"side": {"type": "enum",
                           "values": ["left", "right", "top", "bottom"],
                           "default": "left"}},
        "signals": ["opened", "closed"],
        "tokens_used": ["surface", "on-surface", "outline"],
    }

    def __init__(self, parent, side="left", size=300):
        super().__init__(parent)
        self.setObjectName("QCustomDrawer")            # dim backdrop
        self.setAttribute(Qt.WA_StyledBackground, True)
        self._side = side if side in _SIDES else "left"
        self._size = size
        self._open = False
        self.hide()

        self._panel = QFrame(self)
        self._panel.setObjectName("drawerPanel")
        self._content = QVBoxLayout(self._panel)
        self._content.setContentsMargins(16, 16, 16, 16)

        self._opacity = QGraphicsOpacityEffect(self)
        self._opacity.setOpacity(0.0)
        self.setGraphicsEffect(self._opacity)
        self._fade = QPropertyAnimation(self._opacity, b"opacity", self)
        self._fade.setDuration(self.SLIDE_MS)
        self._slide = QPropertyAnimation(self._panel, b"pos", self)
        self._slide.setDuration(self.SLIDE_MS)
        self._slide.setEasingCurve(QEasingCurve.OutCubic)
        self._closing = False
        self._fade.finished.connect(self._onFadeFinished)

    # ------------------------------------------------------------------ #
    ## Content
    # ------------------------------------------------------------------ #
    def contentLayout(self):
        return self._content

    def addWidget(self, widget):
        self._content.addWidget(widget)

    # ------------------------------------------------------------------ #
    ## Geometry
    # ------------------------------------------------------------------ #
    def _layoutPanel(self):
        pw, ph = self.width(), self.height()
        if self._side in ("left", "right"):
            w = min(self._size, max(200, pw - 40))
            self._panel.resize(w, ph)
        else:
            h = min(self._size, max(160, ph - 40))
            self._panel.resize(pw, h)

    def _shownPos(self):
        pw, ph = self.width(), self.height()
        w, h = self._panel.width(), self._panel.height()
        return {"left": QPoint(0, 0), "right": QPoint(pw - w, 0),
                "top": QPoint(0, 0), "bottom": QPoint(0, ph - h)}[self._side]

    def _hiddenPos(self):
        pw, ph = self.width(), self.height()
        w, h = self._panel.width(), self._panel.height()
        return {"left": QPoint(-w, 0), "right": QPoint(pw, 0),
                "top": QPoint(0, -h), "bottom": QPoint(0, ph)}[self._side]

    # ------------------------------------------------------------------ #
    ## Open / close
    # ------------------------------------------------------------------ #
    def open(self):
        p = self.parentWidget()
        if p is not None:
            self.setGeometry(p.rect())
        self._layoutPanel()
        self._panel.move(self._hiddenPos())
        self.show()
        self.raise_()
        self._open = True
        self._closing = False
        self._fade.stop(); self._fade.setStartValue(0.0); self._fade.setEndValue(1.0); self._fade.start()
        self._slide.stop(); self._slide.setStartValue(self._hiddenPos()); self._slide.setEndValue(self._shownPos()); self._slide.start()
        self.opened.emit()

    def close(self):
        self._open = False
        self._closing = True
        self._fade.stop(); self._fade.setStartValue(self._opacity.opacity()); self._fade.setEndValue(0.0); self._fade.start()
        self._slide.stop(); self._slide.setStartValue(self._panel.pos()); self._slide.setEndValue(self._hiddenPos()); self._slide.start()
        return True

    def isOpen(self):
        return self._open

    def _onFadeFinished(self):
        if self._closing:
            self._closing = False
            self.hide()
            self.closed.emit()

    def mousePressEvent(self, e):
        if not self._panel.geometry().contains(e.pos()):
            self.close()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()
        else:
            super().keyPressEvent(e)
