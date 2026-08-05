########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/@SpinnTV
# WEBSITE: customwidgets.org
########################################################################

########################################################################
## QCustomRangeBarChart - a painted floating-bar / range chart.
##
## Each bar spans a low-to-high pair rather than sitting on a baseline: a
## temperature min/max, a salary band, a project window, a confidence
## interval. A normal bar chart cannot express "from X to Y".
##
## QPainter only, NO QtCharts (see docs/design/mui-charts-gap.md). Axis ticks
## come from the shared _chart_axis so this agrees with Scatter about where
## round numbers fall.
##
## Data goes in with setRanges([...]) in code, or rangesCsv in Qt Designer:
##
##     rangesCsv    = "Mon=4,12;Tue=6,15;Wed=3,9"
##     categoriesCsv overrides the labels if you prefer them separate
##
## Emits barHovered(int) and barClicked(int); -1 means "nothing".
########################################################################
from qtpy.QtCore import Qt, Signal, Property, QRectF, QSize, QPointF
from qtpy.QtGui import QColor, QPainter, QPen, QBrush, QFontMetrics
from qtpy.QtWidgets import QWidget, QSizePolicy

from ._chart_axis import formatTick, niceTicks, tickValues


class QCustomRangeBarChart(QWidget):
    barHovered = Signal(int)
    barClicked = Signal(int)

    WIDGET_ICON = "components/icons/bar_chart.png"
    WIDGET_TOOLTIP = "A painted floating-bar / range chart"
    WIDGET_MODULE = "Custom_Widgets.QCustomRangeBarChart"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomRangeBarChart' name='customRangeBarChart'>
            <property name='geometry'><rect><x>0</x><y>0</y><width>420</width><height>280</height></rect></property>
            <property name='rangesCsv'><string>Mon=4,12;Tue=6,15;Wed=3,9;Thu=8,17;Fri=5,11</string></property>
        </widget>
    </ui>
    """
    __catalog__ = {
        "name": "QCustomRangeBarChart",
        "props": {"rangesCsv": {"type": "string", "default": ""},
                  "categoriesCsv": {"type": "string", "default": ""},
                  "orientation": {"type": "enum", "values": ["vertical", "horizontal"],
                                  "default": "vertical"},
                  "barWidthRatio": {"type": "float", "default": 0.55},
                  "cornerRadius": {"type": "int", "default": 4},
                  "tickCount": {"type": "int", "default": 5},
                  "showGrid": {"type": "bool", "default": True},
                  "showAxis": {"type": "bool", "default": True},
                  "showLabels": {"type": "bool", "default": True},
                  "showBounds": {"type": "bool", "default": False},
                  "barColor": {"type": "color", "default": "#2563eb"},
                  "gridColor": {"type": "color", "default": "#e2e8f0"},
                  "labelColor": {"type": "color", "default": "#64748b"},
                  "boundsColor": {"type": "color", "default": "#0f172a"}},
        "signals": ["barHovered", "barClicked"],
        "tokens_used": ["accent", "outline", "on-surface", "surface-muted"],
    }

    _PAD = 10.0

    def __init__(self, parent=None, ranges=None):
        super().__init__(parent)
        self.setObjectName("QCustomRangeBarChart")
        self._ranges = []           # list of (label, low, high)
        self._orientation = "vertical"
        self._widthRatio = 0.55
        self._radius = 4
        self._tickCount = 5
        self._showGrid = True
        self._showAxis = True
        self._showLabels = True
        self._showBounds = False
        self._hover = -1
        self._rects = []

        self._barColor = QColor("#2563eb")
        self._gridColor = QColor("#e2e8f0")
        self._labelColor = QColor("#64748b")
        self._boundsColor = QColor("#0f172a")

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMouseTracking(True)
        if ranges:
            self.setRanges(ranges)

    # ------------------------------------------------------------------ #
    ## Data
    # ------------------------------------------------------------------ #
    @staticmethod
    def _coerce(item):
        if isinstance(item, dict):
            label = item.get("label", "")
            low, high = item.get("low"), item.get("high")
        elif isinstance(item, (tuple, list)) and len(item) >= 3:
            label, low, high = item[0], item[1], item[2]
        elif isinstance(item, (tuple, list)) and len(item) == 2:
            label, (low, high) = "", (item[0], item[1])
        else:
            return None
        try:
            low, high = float(low), float(high)
        except (TypeError, ValueError):
            return None
        # A reversed pair is a data-entry slip, not a reason to drop the bar.
        if high < low:
            low, high = high, low
        return (str(label), low, high)

    def setRanges(self, ranges):
        self._ranges = [r for r in (self._coerce(x) for x in (ranges or [])) if r]
        self._hover = -1
        self.update()

    def ranges(self):
        return list(self._ranges)

    def barCount(self):
        return len(self._ranges)

    def clearRanges(self):
        self._ranges = []
        self._hover = -1
        self.update()

    def dataBounds(self):
        if not self._ranges:
            return (0.0, 1.0)
        return (min(r[1] for r in self._ranges), max(r[2] for r in self._ranges))

    def valueRange(self):
        low, high = self.dataBounds()
        start, stop, _step = niceTicks(low, high, self._tickCount)
        return (start, stop)

    # ------------------------------------------------------------------ #
    ## Geometry
    # ------------------------------------------------------------------ #
    def sizeHint(self):
        return QSize(420, 280)

    def minimumSizeHint(self):
        return QSize(140, 110)

    def _plotRect(self):
        fm = QFontMetrics(self.font())
        left, bottom = self._PAD, self._PAD
        horizontal = self._orientation == "horizontal"
        if self._showAxis:
            low, high = self.valueRange()
            _s, _e, step = niceTicks(*self.dataBounds(), count=self._tickCount)
            widest = max(fm.horizontalAdvance(formatTick(v, step))
                         for v in (low, high))
            if horizontal:
                bottom += fm.height() + 4
                left += widest
            else:
                left += widest + 8
        if self._showLabels:
            if horizontal:
                left += max((fm.horizontalAdvance(r[0]) for r in self._ranges),
                            default=0) + 8
            else:
                bottom += fm.height() + 4
        return QRectF(left, self._PAD,
                      max(1.0, self.width() - left - self._PAD),
                      max(1.0, self.height() - self._PAD - bottom))

    def valueToPixel(self, value):
        """Value -> pixel along the value axis."""
        rect = self._plotRect()
        low, high = self.valueRange()
        span = (high - low) or 1.0
        fraction = (value - low) / span
        if self._orientation == "horizontal":
            return rect.left() + fraction * rect.width()
        return rect.bottom() - fraction * rect.height()

    def _computeRects(self):
        self._rects = []
        count = len(self._ranges)
        if not count:
            return
        rect = self._plotRect()
        horizontal = self._orientation == "horizontal"
        axis = rect.height() if horizontal else rect.width()
        slot = axis / count
        thickness = max(1.0, slot * max(0.05, min(1.0, self._widthRatio)))

        for index, (_label, low, high) in enumerate(self._ranges):
            near = self.valueToPixel(low)
            far = self.valueToPixel(high)
            centre = (rect.top() if horizontal else rect.left()) + slot * (index + 0.5)
            if horizontal:
                self._rects.append(QRectF(min(near, far), centre - thickness / 2.0,
                                          max(1.0, abs(far - near)), thickness))
            else:
                self._rects.append(QRectF(centre - thickness / 2.0, min(near, far),
                                          thickness, max(1.0, abs(far - near))))

    def barRects(self):
        if not self._rects:
            self._computeRects()
        return list(self._rects)

    # ------------------------------------------------------------------ #
    ## Painting
    # ------------------------------------------------------------------ #
    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.setFont(self.font())
        rect = self._plotRect()
        self._computeRects()

        if self._showGrid or self._showAxis:
            self._paintGrid(p, rect)
        if not self._ranges:
            return

        for index, bar in enumerate(self._rects):
            colour = self._barColor.lighter(115) if index == self._hover else self._barColor
            p.setPen(Qt.NoPen)
            p.setBrush(QBrush(colour))
            radius = min(float(self._radius),
                         min(bar.width(), bar.height()) / 2.0)
            p.drawRoundedRect(bar, radius, radius)

        if self._showLabels:
            self._paintCategoryLabels(p, rect)
        if self._showBounds:
            self._paintBounds(p)

    def _paintGrid(self, p, rect):
        fm = QFontMetrics(self.font())
        low, high = self.dataBounds()
        _s, _e, step = niceTicks(low, high, self._tickCount)
        horizontal = self._orientation == "horizontal"
        for value in tickValues(low, high, self._tickCount):
            pixel = self.valueToPixel(value)
            if self._showGrid:
                p.setPen(QPen(self._gridColor, 1))
                if horizontal:
                    p.drawLine(QPointF(pixel, rect.top()), QPointF(pixel, rect.bottom()))
                else:
                    p.drawLine(QPointF(rect.left(), pixel), QPointF(rect.right(), pixel))
            if self._showAxis:
                p.setPen(QPen(self._labelColor))
                text = formatTick(value, step)
                if horizontal:
                    width = fm.horizontalAdvance(text) + 8
                    p.drawText(QRectF(pixel - width / 2.0, rect.bottom() + 3,
                                      width, fm.height()),
                               int(Qt.AlignHCenter | Qt.AlignVCenter), text)
                else:
                    p.drawText(QRectF(0, pixel - fm.height() / 2.0,
                                      rect.left() - 6, fm.height()),
                               int(Qt.AlignRight | Qt.AlignVCenter), text)

    def _paintCategoryLabels(self, p, rect):
        fm = QFontMetrics(self.font())
        p.setPen(QPen(self._labelColor))
        horizontal = self._orientation == "horizontal"
        for index, (label, _low, _high) in enumerate(self._ranges):
            if not label or index >= len(self._rects):
                continue
            bar = self._rects[index]
            if horizontal:
                p.drawText(QRectF(0, bar.center().y() - fm.height() / 2.0,
                                  rect.left() - 6, fm.height()),
                           int(Qt.AlignRight | Qt.AlignVCenter), label)
            else:
                width = max(fm.horizontalAdvance(label) + 8, bar.width())
                p.drawText(QRectF(bar.center().x() - width / 2.0,
                                  rect.bottom() + 3, width, fm.height()),
                           int(Qt.AlignHCenter | Qt.AlignVCenter), label)

    def _paintBounds(self, p):
        fm = QFontMetrics(self.font())
        p.setPen(QPen(self._boundsColor))
        horizontal = self._orientation == "horizontal"
        for index, (_label, low, high) in enumerate(self._ranges):
            if index >= len(self._rects):
                continue
            bar = self._rects[index]
            lowText, highText = "%g" % low, "%g" % high
            if horizontal:
                p.drawText(QRectF(bar.left() - fm.horizontalAdvance(lowText) - 4,
                                  bar.center().y() - fm.height() / 2.0,
                                  fm.horizontalAdvance(lowText), fm.height()),
                           int(Qt.AlignRight | Qt.AlignVCenter), lowText)
                p.drawText(QRectF(bar.right() + 4,
                                  bar.center().y() - fm.height() / 2.0,
                                  fm.horizontalAdvance(highText) + 2, fm.height()),
                           int(Qt.AlignLeft | Qt.AlignVCenter), highText)
            else:
                p.drawText(QRectF(bar.center().x() - 30, bar.top() - fm.height() - 2,
                                  60, fm.height()),
                           int(Qt.AlignCenter), highText)
                p.drawText(QRectF(bar.center().x() - 30, bar.bottom() + 2,
                                  60, fm.height()),
                           int(Qt.AlignCenter), lowText)

    # ------------------------------------------------------------------ #
    ## Interaction
    # ------------------------------------------------------------------ #
    def barAt(self, pos):
        point = QPointF(pos)
        for index, bar in enumerate(self.barRects()):
            # Widen the hit area on the thin axis so a slim bar is still
            # grabbable without aiming precisely.
            padded = bar.adjusted(-3, -3, 3, 3)
            if padded.contains(point):
                return index
        return -1

    def mouseMoveEvent(self, e):
        index = self.barAt(e.pos())
        if index != self._hover:
            self._hover = index
            self.barHovered.emit(index)
            self.update()
        super().mouseMoveEvent(e)

    def leaveEvent(self, e):
        if self._hover != -1:
            self._hover = -1
            self.barHovered.emit(-1)
            self.update()
        super().leaveEvent(e)

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.LeftButton:
            index = self.barAt(e.pos())
            if index >= 0:
                self.barClicked.emit(index)
        super().mouseReleaseEvent(e)

    # ------------------------------------------------------------------ #
    ## Designer properties
    # ------------------------------------------------------------------ #
    @Property(str)
    def rangesCsv(self):
        return ";".join("%s=%g,%g" % (label, low, high)
                        for label, low, high in self._ranges)

    @rangesCsv.setter
    def rangesCsv(self, text):
        ranges = []
        for chunk in str(text).replace("|", ";").split(";"):
            chunk = chunk.strip()
            if not chunk:
                continue
            if "=" in chunk:
                label, _, raw = chunk.partition("=")
                label = label.strip()
            else:
                label, raw = "", chunk
            parts = [t.strip() for t in raw.split(",") if t.strip()]
            if len(parts) < 2:
                continue
            coerced = self._coerce((label, parts[0], parts[1]))
            if coerced:
                ranges.append(coerced)
        self.setRanges(ranges)

    @Property(str)
    def categoriesCsv(self):
        return ",".join(label for label, _l, _h in self._ranges)

    @categoriesCsv.setter
    def categoriesCsv(self, text):
        labels = [t.strip() for t in str(text).replace(";", ",").split(",")
                  if t.strip()]
        self._ranges = [(labels[i] if i < len(labels) else label, low, high)
                        for i, (label, low, high) in enumerate(self._ranges)]
        self.update()

    @Property(str)
    def orientation(self):
        return self._orientation

    @orientation.setter
    def orientation(self, value):
        self._orientation = "horizontal" if str(value) == "horizontal" else "vertical"
        self.update()

    @Property(float)
    def barWidthRatio(self):
        return self._widthRatio

    @barWidthRatio.setter
    def barWidthRatio(self, value):
        self._widthRatio = max(0.05, min(1.0, float(value))); self.update()

    @Property(int)
    def cornerRadius(self):
        return self._radius

    @cornerRadius.setter
    def cornerRadius(self, value):
        self._radius = max(0, int(value)); self.update()

    @Property(int)
    def tickCount(self):
        return self._tickCount

    @tickCount.setter
    def tickCount(self, value):
        self._tickCount = max(1, int(value)); self.update()

    @Property(bool)
    def showGrid(self):
        return self._showGrid

    @showGrid.setter
    def showGrid(self, value):
        self._showGrid = bool(value); self.update()

    @Property(bool)
    def showAxis(self):
        return self._showAxis

    @showAxis.setter
    def showAxis(self, value):
        self._showAxis = bool(value); self.update()

    @Property(bool)
    def showLabels(self):
        return self._showLabels

    @showLabels.setter
    def showLabels(self, value):
        self._showLabels = bool(value); self.update()

    @Property(bool)
    def showBounds(self):
        return self._showBounds

    @showBounds.setter
    def showBounds(self, value):
        self._showBounds = bool(value); self.update()

    # -- colours (from tokens via qproperty) --
    @Property(QColor)
    def barColor(self):
        return self._barColor

    @barColor.setter
    def barColor(self, c):
        self._barColor = QColor(c); self.update()

    @Property(QColor)
    def gridColor(self):
        return self._gridColor

    @gridColor.setter
    def gridColor(self, c):
        self._gridColor = QColor(c); self.update()

    @Property(QColor)
    def labelColor(self):
        return self._labelColor

    @labelColor.setter
    def labelColor(self, c):
        self._labelColor = QColor(c); self.update()

    @Property(QColor)
    def boundsColor(self):
        return self._boundsColor

    @boundsColor.setter
    def boundsColor(self, c):
        self._boundsColor = QColor(c); self.update()
