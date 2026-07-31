########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/spinnTv
# WEBSITE: spinncode.com
########################################################################

########################################################################
## QCustomPageDots - a carousel / pager page indicator.
##
## A row (or column) of dots where the active page is drawn as an elongated
## pill. Painted with QPainter so it stays crisp at any size and needs no child
## widgets. Optionally clickable: clicking a dot sets it active and emits
## `pageChanged(index)`, so it can drive a QStackedWidget / carousel directly.
########################################################################
from qtpy.QtCore import Qt, Property, Signal, QRectF, QSize
from qtpy.QtGui import QColor, QPainter, QBrush
from qtpy.QtWidgets import QWidget, QSizePolicy


class QCustomPageDots(QWidget):

    pageChanged = Signal(int)

    WIDGET_ICON = "components/icons/dots.png"
    WIDGET_TOOLTIP = "A carousel / pager page indicator (dots + active pill)"
    WIDGET_MODULE = "Custom_Widgets.QCustomPageDots"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomPageDots' name='customPageDots'>
            <property name='geometry'><rect><x>0</x><y>0</y><width>60</width><height>16</height></rect></property>
        </widget>
    </ui>
    """
    __catalog__ = {
        "name": "QCustomPageDots",
        "props": {"count": {"type": "int", "default": 3},
                  "activeIndex": {"type": "int", "default": 0},
                  "dotColor": {"type": "color", "default": "#d7dbe6"},
                  "activeColor": {"type": "color", "default": "#3355e8"},
                  "dotDiameter": {"type": "int", "default": 8},
                  "activePillLength": {"type": "int", "default": 22},
                  "spacing": {"type": "int", "default": 6},
                  "orientation": {"type": "enum", "values": ["horizontal", "vertical"], "default": "horizontal"},
                  "clickable": {"type": "bool", "default": True}},
        "signals": ["pageChanged"],
        "tokens_used": ["accent"],
    }

    def __init__(self, parent=None, count=3, active=0):
        super().__init__(parent)
        self.setObjectName("QCustomPageDots")
        self._count = max(0, int(count))
        self._active = int(active)
        self._dot = QColor("#d7dbe6")
        self._active_color = QColor("#3355e8")
        self._d = 8
        self._pill = 22
        self._spacing = 6
        self._orientation = "horizontal"
        self._clickable = True
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.setCursor(Qt.PointingHandCursor)

    # ------------------------------------------------------------------ #
    ## API
    # ------------------------------------------------------------------ #
    def setCount(self, n):
        self._count = max(0, int(n))
        self._active = min(self._active, self._count - 1) if self._count else 0
        self.updateGeometry()
        self.update()

    def setActiveIndex(self, i):
        i = int(i)
        if 0 <= i < self._count and i != self._active:
            self._active = i
            self.updateGeometry()
            self.update()

    def bindTo(self, control):
        """Two-way bind the dots to any paged control (QCustomSegmentedControl,
        QStackedWidget, a carousel…): the control's ``currentChanged(int)``
        drives the active dot, clicking a dot calls ``setCurrentIndex``. Also
        adopts the control's ``count()`` when available. One declarative line
        instead of two lambdas per app."""
        count = getattr(control, "count", None)
        if callable(count):
            try:
                self.setCount(int(count()))
            except Exception:
                pass
        sig = getattr(control, "currentChanged", None)
        if sig is not None:
            sig.connect(self.setActiveIndex)
        setter = getattr(control, "setCurrentIndex", None)
        if callable(setter):
            self.pageChanged.connect(setter)
        return self

    def setColors(self, dot=None, active=None):
        if dot is not None:
            self._dot = QColor(dot)
        if active is not None:
            self._active_color = QColor(active)
        self.update()

    # ------------------------------------------------------------------ #
    ## Geometry
    # ------------------------------------------------------------------ #
    def _length_of(self, i):
        return self._pill if i == self._active else self._d

    def _extent(self):
        """Total length along the layout axis for all dots + gaps."""
        if self._count <= 0:
            return 0
        return sum(self._length_of(i) for i in range(self._count)) \
            + self._spacing * (self._count - 1)

    def sizeHint(self):
        ext = self._extent()
        if self._orientation == "vertical":
            return QSize(self._d, ext)
        return QSize(ext, self._d)

    def minimumSizeHint(self):
        return self.sizeHint()

    def _rects(self):
        """Yield (index, QRectF) for each dot, centred on the cross axis."""
        vert = self._orientation == "vertical"
        thick = self._d
        cross = (self.width() if vert else self.height())
        cyoff = (cross - thick) / 2.0
        pos = 0.0
        for i in range(self._count):
            ln = self._length_of(i)
            if vert:
                r = QRectF(cyoff, pos, thick, ln)
            else:
                r = QRectF(pos, cyoff, ln, thick)
            yield i, r
            pos += ln + self._spacing

    # ------------------------------------------------------------------ #
    ## Painting
    # ------------------------------------------------------------------ #
    def paintEvent(self, e):
        if self._count <= 0:
            return
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, True)
        p.setPen(Qt.NoPen)
        r = self._d / 2.0
        for i, rect in self._rects():
            p.setBrush(QBrush(self._active_color if i == self._active else self._dot))
            p.drawRoundedRect(rect, r, r)
        p.end()

    def mousePressEvent(self, e):
        if self._clickable and e.button() == Qt.LeftButton:
            pt = e.position() if hasattr(e, "position") else e.pos()
            for i, rect in self._rects():
                if rect.adjusted(-3, -6, 3, 6).contains(pt):
                    if i != self._active:
                        self.setActiveIndex(i)
                        self.pageChanged.emit(i)
                    e.accept()
                    return
        super().mousePressEvent(e)

    # ------------------------------------------------------------------ #
    ## Designer properties
    # ------------------------------------------------------------------ #
    @Property(int)
    def count(self):
        return self._count

    @count.setter
    def count(self, v):
        self.setCount(v)

    @Property(int)
    def activeIndex(self):
        return self._active

    @activeIndex.setter
    def activeIndex(self, v):
        self.setActiveIndex(v)

    @Property(QColor)
    def dotColor(self):
        return self._dot

    @dotColor.setter
    def dotColor(self, c):
        self._dot = QColor(c)
        self.update()

    @Property(QColor)
    def activeColor(self):
        return self._active_color

    @activeColor.setter
    def activeColor(self, c):
        self._active_color = QColor(c)
        self.update()

    @Property(int)
    def dotDiameter(self):
        return self._d

    @dotDiameter.setter
    def dotDiameter(self, v):
        self._d = max(2, int(v))
        self.updateGeometry()
        self.update()

    @Property(int)
    def activePillLength(self):
        return self._pill

    @activePillLength.setter
    def activePillLength(self, v):
        self._pill = max(self._d, int(v))
        self.updateGeometry()
        self.update()

    @Property(int)
    def spacing(self):
        return self._spacing

    @spacing.setter
    def spacing(self, v):
        self._spacing = max(0, int(v))
        self.updateGeometry()
        self.update()

    @Property(str)
    def orientation(self):
        return self._orientation

    @orientation.setter
    def orientation(self, v):
        self._orientation = "vertical" if str(v) == "vertical" else "horizontal"
        self.updateGeometry()
        self.update()

    @Property(bool)
    def clickable(self):
        return self._clickable

    @clickable.setter
    def clickable(self, v):
        self._clickable = bool(v)
