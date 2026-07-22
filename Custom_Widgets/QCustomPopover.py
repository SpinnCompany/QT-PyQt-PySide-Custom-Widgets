########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/spinnTv
# WEBSITE: spinncode.com
########################################################################

########################################################################
## QCustomPopover - a rich popover anchored to a widget.
##
## Unlike a text tooltip, a popover holds arbitrary widgets and points at its
## anchor with an arrow. Opens on demand (or wire it to a trigger via
## attach()); closes on outside click. Tokenized colours via qproperty.
########################################################################
from qtpy.QtCore import Qt, QPoint, QRectF, Property, Signal
from qtpy.QtGui import QColor, QPainter, QPainterPath, QPen, QPolygonF
from qtpy.QtCore import QPointF
from qtpy.QtWidgets import QWidget, QVBoxLayout


_PLACEMENTS = ("top", "bottom", "left", "right")


class QCustomPopover(QWidget):
    opened = Signal()
    closed = Signal()
    ARROW = 8
    RADIUS = 8

    __catalog__ = {
        "name": "QCustomPopover",
        "props": {"placement": {"type": "enum",
                                "values": ["top", "bottom", "left", "right"],
                                "default": "bottom"}},
        "signals": ["opened", "closed"],
        "tokens_used": ["surface", "on-surface", "outline"],
    }

    def __init__(self, anchor=None, placement="bottom"):
        super().__init__(anchor.window() if anchor is not None else None,
                         Qt.Popup | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)
        self.setObjectName("QCustomPopover")
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self._anchor = anchor
        self._placement = placement if placement in _PLACEMENTS else "bottom"
        self._panel = QColor("#ffffff")
        self._border = QColor("#cbd5e1")

        self._content = QVBoxLayout(self)
        self._applyContentMargins()
        self._content.setSpacing(6)

    def _applyContentMargins(self):
        a = self.ARROW
        m = 12
        self._content.setContentsMargins(
            m + (a if self._placement == "left" else 0),
            m + (a if self._placement == "top" else 0),
            m + (a if self._placement == "right" else 0),
            m + (a if self._placement == "bottom" else 0))

    # ------------------------------------------------------------------ #
    ## Content
    # ------------------------------------------------------------------ #
    def contentLayout(self):
        return self._content

    def addWidget(self, widget):
        self._content.addWidget(widget)

    def setPlacement(self, placement):
        if placement in _PLACEMENTS:
            self._placement = placement
            self._applyContentMargins()

    # ------------------------------------------------------------------ #
    ## Show / position
    # ------------------------------------------------------------------ #
    def showPopover(self):
        self.adjustSize()
        if self._anchor is not None:
            self.move(self._computePos())
        self.show()
        self.raise_()
        self.opened.emit()

    def _computePos(self):
        a = self._anchor
        tl = a.mapToGlobal(QPoint(0, 0))
        aw, ah = a.width(), a.height()
        w, h = self.width(), self.height()
        if self._placement == "bottom":
            return QPoint(tl.x() + aw // 2 - w // 2, tl.y() + ah)
        if self._placement == "top":
            return QPoint(tl.x() + aw // 2 - w // 2, tl.y() - h)
        if self._placement == "right":
            return QPoint(tl.x() + aw, tl.y() + ah // 2 - h // 2)
        return QPoint(tl.x() - w, tl.y() + ah // 2 - h // 2)   # left

    def hideEvent(self, e):
        super().hideEvent(e)
        self.closed.emit()

    # ------------------------------------------------------------------ #
    ## Painting (panel + arrow)
    # ------------------------------------------------------------------ #
    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        a = self.ARROW
        rect = QRectF(self.rect()).adjusted(
            (a if self._placement == "left" else 0) + 0.5,
            (a if self._placement == "top" else 0) + 0.5,
            -((a if self._placement == "right" else 0) + 0.5),
            -((a if self._placement == "bottom" else 0) + 0.5))
        path = QPainterPath()
        path.addRoundedRect(rect, self.RADIUS, self.RADIUS)

        # arrow triangle pointing to the anchor
        cx = self.width() / 2.0
        cy = self.height() / 2.0
        arrow = QPolygonF()
        if self._placement == "bottom":
            arrow = QPolygonF([QPointF(cx - a, rect.top()), QPointF(cx + a, rect.top()),
                               QPointF(cx, rect.top() - a)])
        elif self._placement == "top":
            arrow = QPolygonF([QPointF(cx - a, rect.bottom()), QPointF(cx + a, rect.bottom()),
                               QPointF(cx, rect.bottom() + a)])
        elif self._placement == "right":
            arrow = QPolygonF([QPointF(rect.left(), cy - a), QPointF(rect.left(), cy + a),
                               QPointF(rect.left() - a, cy)])
        else:  # left
            arrow = QPolygonF([QPointF(rect.right(), cy - a), QPointF(rect.right(), cy + a),
                               QPointF(rect.right() + a, cy)])
        path.addPolygon(arrow)
        path = path.simplified()

        p.setPen(QPen(self._border, 1))
        p.setBrush(self._panel)
        p.drawPath(path)

    # ------------------------------------------------------------------ #
    ## Colours (from tokens via qproperty)
    # ------------------------------------------------------------------ #
    @Property(QColor)
    def panelColor(self):
        return self._panel

    @panelColor.setter
    def panelColor(self, color):
        self._panel = QColor(color)
        self.update()

    @Property(QColor)
    def borderColor(self):
        return self._border

    @borderColor.setter
    def borderColor(self, color):
        self._border = QColor(color)
        self.update()

    # ------------------------------------------------------------------ #
    ## Trigger helper
    # ------------------------------------------------------------------ #
    @staticmethod
    def attach(trigger, placement="bottom"):
        """Create a popover anchored to `trigger` and open it on click."""
        pop = QCustomPopover(trigger, placement=placement)
        trigger.clicked.connect(pop.showPopover)
        return pop
