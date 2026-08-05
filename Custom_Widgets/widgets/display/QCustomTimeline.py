########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/@SpinnTV
# WEBSITE: customwidgets.org
########################################################################

########################################################################
## QCustomTimeline - a vertical event timeline.
##
## Each item has a marker dot on a connecting rail plus a title, optional
## time and description. Rail colours come from tokens (qproperty lineColor);
## per-item dot colour can be overridden. Tokenized.
########################################################################
from qtpy.QtCore import Qt, Property, QRectF
from qtpy.QtGui import QColor, QPainter, QPen, QBrush
from qtpy.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel


class _Rail(QWidget):
    """The left column: a vertical connector line + a dot for one item."""

    def __init__(self, isFirst, isLast, dotColor, lineColor, parent=None):
        super().__init__(parent)
        self._isFirst = isFirst
        self._isLast = isLast
        self._dot = QColor(dotColor)
        self._line = QColor(lineColor)
        self.setFixedWidth(24)

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        cx = self.width() / 2.0
        cy = 14.0                       # dot centre near the title baseline
        h = self.height()
        p.setPen(QPen(self._line, 2))
        if not self._isFirst:
            p.drawLine(int(cx), 0, int(cx), int(cy))
        if not self._isLast:
            p.drawLine(int(cx), int(cy), int(cx), int(h))
        p.setPen(Qt.NoPen)
        p.setBrush(QBrush(self._dot))
        p.drawEllipse(QRectF(cx - 5, cy - 5, 10, 10))


class QCustomTimeline(QWidget):
    WIDGET_ICON = "components/icons/timeline.png"
    WIDGET_TOOLTIP = "A vertical event timeline"
    WIDGET_MODULE = "Custom_Widgets.QCustomTimeline"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomTimeline' name='customTimeline'>
            <property name='geometry'><rect><x>0</x><y>0</y><width>320</width><height>260</height></rect></property>
        </widget>
    </ui>
    """
    __catalog__ = {
        "name": "QCustomTimeline",
        "props": {},
        "signals": [],
        "tokens_used": ["on-surface", "surface-muted", "outline", "accent"],
    }

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("QCustomTimeline")
        self._items = []               # (title, time, desc, color)
        self._line = QColor("#cbd5e1")
        self._defaultDot = QColor("#2563eb")
        self._box = QVBoxLayout(self)
        self._box.setContentsMargins(0, 0, 0, 0)
        self._box.setSpacing(0)
        self._box.addStretch(1)

    def addItem(self, title, time=None, description=None, color=None):
        self._items.append((title, time, description, color))
        self._rebuild()

    def setItems(self, items):
        self._items = []
        for it in items or []:
            if isinstance(it, dict):
                self._items.append((it.get("title", ""), it.get("time"),
                                    it.get("description"), it.get("color")))
            elif isinstance(it, (tuple, list)):
                self._items.append(tuple(list(it) + [None] * (4 - len(it)))[:4])
            else:
                self._items.append((str(it), None, None, None))
        self._rebuild()

    def _rebuild(self):
        while self._box.count() > 1:
            w = self._box.takeAt(0).widget()
            if w is not None:
                w.deleteLater()
        n = len(self._items)
        for i, (title, time, desc, color) in enumerate(self._items):
            row = QWidget(self)
            h = QHBoxLayout(row)
            h.setContentsMargins(0, 0, 0, 8)
            h.setSpacing(10)
            rail = _Rail(i == 0, i == n - 1, color or self._defaultDot, self._line, row)
            h.addWidget(rail, 0)
            content = QVBoxLayout()
            content.setContentsMargins(0, 4, 0, 0)
            content.setSpacing(1)
            t = QLabel(str(title), row)
            t.setObjectName("timelineTitle")
            content.addWidget(t)
            if time:
                tm = QLabel(str(time), row)
                tm.setObjectName("timelineTime")
                content.addWidget(tm)
            if desc:
                d = QLabel(str(desc), row)
                d.setObjectName("timelineDesc")
                d.setWordWrap(True)
                content.addWidget(d)
            h.addLayout(content, 1)
            self._box.insertWidget(self._box.count() - 1, row)

    def count(self):
        return len(self._items)

    # -- properties (rail colours from tokens) --
    @Property(QColor)
    def lineColor(self):
        return self._line

    @lineColor.setter
    def lineColor(self, color):
        self._line = QColor(color)
        self._rebuild()

    @Property(QColor)
    def dotColor(self):
        return self._defaultDot

    @dotColor.setter
    def dotColor(self, color):
        self._defaultDot = QColor(color)
        self._rebuild()
