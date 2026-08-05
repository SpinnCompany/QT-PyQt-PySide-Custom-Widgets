########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/spinnTv
# WEBSITE: spinncode.com
########################################################################

########################################################################
## QCustomRadialBars - a painted radial bar chart.
##
## Concentric arcs, one per category, each sweeping in proportion to its
## value. The "activity rings" form: compact, reads at a glance, and unlike a
## pie it compares values that do NOT sum to a whole.
##
## QPainter only, NO QtCharts (see docs/design/mui-charts-gap.md). Angles come
## from the shared _chart_axis polar helpers, so this winds the same way as
## QCustomRadarChart and QCustomRadialLines.
##
## Data goes in with setBars([...]) in code, or barsCsv in Qt Designer:
##
##     barsCsv = "Move=82,Exercise=64,Stand=95"
##
## Emits barHovered(int) and barClicked(int); -1 means "nothing".
########################################################################
import math

from qtpy.QtCore import Qt, Signal, Property, QRectF, QSize, QPointF
from qtpy.QtGui import QColor, QPainter, QPen, QBrush, QFontMetrics
from qtpy.QtWidgets import QWidget, QSizePolicy


class QCustomRadialBars(QWidget):
    barHovered = Signal(int)
    barClicked = Signal(int)

    WIDGET_ICON = "components/icons/donut_large.png"
    WIDGET_TOOLTIP = "A painted radial bar chart (activity rings)"
    WIDGET_MODULE = "Custom_Widgets.QCustomRadialBars"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomRadialBars' name='customRadialBars'>
            <property name='geometry'><rect><x>0</x><y>0</y><width>300</width><height>300</height></rect></property>
            <property name='barsCsv'><string>Move=82,Exercise=64,Stand=95</string></property>
        </widget>
    </ui>
    """
    __catalog__ = {
        "name": "QCustomRadialBars",
        "props": {"barsCsv": {"type": "string", "default": ""},
                  "colorsCsv": {"type": "string", "default": ""},
                  "maxValue": {"type": "float", "default": 100.0},
                  "startAngle": {"type": "int", "default": 90},
                  "clockwise": {"type": "bool", "default": True},
                  "thickness": {"type": "int", "default": 18},
                  "spacing": {"type": "int", "default": 6},
                  "holeRatio": {"type": "float", "default": 0.35},
                  "rounded": {"type": "bool", "default": True},
                  "showTrack": {"type": "bool", "default": True},
                  "showLabels": {"type": "bool", "default": True},
                  "showValues": {"type": "bool", "default": True},
                  "trackColor": {"type": "color", "default": "#e2e8f0"},
                  "labelColor": {"type": "color", "default": "#0f172a"}},
        "signals": ["barHovered", "barClicked"],
        "tokens_used": ["accent", "surface-muted", "on-surface"],
    }

    _DEFAULT_COLORS = ["#2563eb", "#16a34a", "#f59e0b", "#dc2626", "#7c3aed",
                       "#0891b2"]

    def __init__(self, parent=None, bars=None):
        super().__init__(parent)
        self.setObjectName("QCustomRadialBars")
        self._bars = []             # list of (label, value)
        self._colors = []
        self._maxValue = 100.0
        self._startAngle = 90
        self._clockwise = True
        self._thickness = 18
        self._spacing = 6
        self._holeRatio = 0.35
        self._rounded = True
        self._showTrack = True
        self._showLabels = True
        self._showValues = True
        self._hover = -1

        self._trackColor = QColor("#e2e8f0")
        self._labelColor = QColor("#0f172a")

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMouseTracking(True)
        if bars:
            self.setBars(bars)

    # ------------------------------------------------------------------ #
    ## Data
    # ------------------------------------------------------------------ #
    @staticmethod
    def _coerce(bar):
        if isinstance(bar, dict):
            label, value = bar.get("label"), bar.get("value")
        elif isinstance(bar, (tuple, list)) and len(bar) >= 2:
            label, value = bar[0], bar[1]
        else:
            return None
        try:
            return (str(label), max(0.0, float(value)))
        except (TypeError, ValueError):
            return None

    def setBars(self, bars):
        self._bars = [b for b in (self._coerce(x) for x in (bars or [])) if b]
        self._hover = -1
        self.update()

    def bars(self):
        return list(self._bars)

    def barCount(self):
        return len(self._bars)

    def clearBars(self):
        self._bars = []
        self._hover = -1
        self.update()

    def maximum(self):
        if self._maxValue > 0:
            return self._maxValue
        return max((v for _l, v in self._bars), default=0.0) or 1.0

    def barColor(self, index):
        if 0 <= index < len(self._colors) and self._colors[index] is not None:
            return QColor(self._colors[index])
        return QColor(self._DEFAULT_COLORS[index % len(self._DEFAULT_COLORS)])

    def fractionFor(self, index):
        """0..1 of the maximum. Values above the maximum are clamped so a bar
        cannot wrap past its own start and read as a smaller number."""
        if not (0 <= index < len(self._bars)):
            return 0.0
        return max(0.0, min(1.0, self._bars[index][1] / self.maximum()))

    # ------------------------------------------------------------------ #
    ## Geometry
    # ------------------------------------------------------------------ #
    def sizeHint(self):
        return QSize(300, 300)

    def minimumSizeHint(self):
        return QSize(110, 110)

    def _legendHeight(self):
        if not (self._showLabels or self._showValues) or not self._bars:
            return 0.0
        return QFontMetrics(self.font()).height() + 8

    def _plotRect(self):
        bottom = self._legendHeight()
        side = max(10.0, min(self.width(), self.height() - bottom) - 16)
        return QRectF((self.width() - side) / 2.0,
                      (self.height() - bottom - side) / 2.0, side, side)

    def ringRect(self, index):
        """Bounding rect of ring `index`, outermost first."""
        rect = self._plotRect()
        inset = index * (self._thickness + self._spacing) + self._thickness / 2.0
        limit = rect.width() / 2.0 * (1.0 - max(0.0, min(0.95, self._holeRatio)))
        inset = min(inset, max(1.0, limit))
        return rect.adjusted(inset, inset, -inset, -inset)

    def _sweepFor(self, index):
        """(startAngle, spanAngle) in Qt's 1/16-degree units."""
        span = self.fractionFor(index) * 360.0
        if self._clockwise:
            span = -span
        return int(self._startAngle * 16), int(span * 16)

    # ------------------------------------------------------------------ #
    ## Painting
    # ------------------------------------------------------------------ #
    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.setFont(self.font())
        if not self._bars:
            return

        cap = Qt.RoundCap if self._rounded else Qt.FlatCap
        for index in range(len(self._bars)):
            ring = self.ringRect(index)
            if self._showTrack:
                pen = QPen(self._trackColor, self._thickness)
                pen.setCapStyle(Qt.FlatCap)
                p.setPen(pen)
                p.setBrush(Qt.NoBrush)
                p.drawArc(ring, 0, 360 * 16)

            colour = self.barColor(index)
            if index == self._hover:
                colour = colour.lighter(115)
            pen = QPen(colour, self._thickness)
            pen.setCapStyle(cap)
            p.setPen(pen)
            start, span = self._sweepFor(index)
            if span:
                p.drawArc(ring, start, span)

        if self._showLabels or self._showValues:
            self._paintLabels(p)

    def _paintLabels(self, p):
        """A legend strip below the rings.

        Anchoring each label to its own ring's start angle put the text
        straight over the arcs — every ring starts at the same angle, so the
        labels stacked on top of each other and on the bars underneath. A
        legend also matches the other charts in the family.
        """
        fm = QFontMetrics(self.font())
        swatch, gap = 9.0, 14.0
        entries = []
        for index, (label, value) in enumerate(self._bars):
            parts = []
            if self._showLabels:
                parts.append(label)
            if self._showValues:
                parts.append("%g" % value)
            text = "  ".join(parts)
            if text:
                entries.append((index, text))
        if not entries:
            return

        widths = [swatch + 5 + fm.horizontalAdvance(text) for _i, text in entries]
        x = (self.width() - (sum(widths) + gap * (len(widths) - 1))) / 2.0
        y = self.height() - self._legendHeight() + 4
        for slot, (index, text) in enumerate(entries):
            p.setPen(Qt.NoPen)
            p.setBrush(QBrush(self.barColor(index)))
            p.drawEllipse(QRectF(x, y + (fm.height() - swatch) / 2.0,
                                 swatch, swatch))
            p.setPen(QPen(self._labelColor))
            p.drawText(QRectF(x + swatch + 5, y, widths[slot], fm.height()),
                       int(Qt.AlignLeft | Qt.AlignVCenter), text)
            x += widths[slot] + gap

    # ------------------------------------------------------------------ #
    ## Interaction
    # ------------------------------------------------------------------ #
    def barAt(self, pos):
        """Index of the ring under a point, or -1.

        Tests the radius band only: a point anywhere on the ring counts, filled
        or not, so hovering the empty part of a track still identifies it.
        """
        point = QPointF(pos)
        for index in range(len(self._bars)):
            ring = self.ringRect(index)
            centre = ring.center()
            distance = math.hypot(point.x() - centre.x(), point.y() - centre.y())
            radius = ring.width() / 2.0
            if abs(distance - radius) <= self._thickness / 2.0:
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
    def barsCsv(self):
        return ",".join("%s=%g" % (label, value) for label, value in self._bars)

    @barsCsv.setter
    def barsCsv(self, text):
        bars = []
        for chunk in str(text).replace(";", ",").split(","):
            chunk = chunk.strip()
            if not chunk:
                continue
            if "=" in chunk:
                label, _, raw = chunk.partition("=")
            else:
                label, raw = "Bar %d" % (len(bars) + 1), chunk
            try:
                bars.append((label.strip() or "Bar %d" % (len(bars) + 1),
                             max(0.0, float(raw.strip()))))
            except ValueError:
                continue
        self.setBars(bars)

    @Property(str)
    def colorsCsv(self):
        return ",".join(c.name() if c is not None else "" for c in self._colors)

    @colorsCsv.setter
    def colorsCsv(self, text):
        colors = []
        for token in str(text).replace(";", ",").split(","):
            token = token.strip()
            colour = QColor(token) if token else QColor()
            colors.append(colour if colour.isValid() else None)
        self._colors = colors
        self.update()

    @Property(float)
    def maxValue(self):
        return self._maxValue

    @maxValue.setter
    def maxValue(self, value):
        self._maxValue = max(0.0, float(value)); self.update()

    @Property(int)
    def startAngle(self):
        return self._startAngle

    @startAngle.setter
    def startAngle(self, value):
        self._startAngle = int(value) % 360; self.update()

    @Property(bool)
    def clockwise(self):
        return self._clockwise

    @clockwise.setter
    def clockwise(self, value):
        self._clockwise = bool(value); self.update()

    @Property(int)
    def thickness(self):
        return self._thickness

    @thickness.setter
    def thickness(self, value):
        self._thickness = max(1, int(value)); self.update()

    @Property(int)
    def spacing(self):
        return self._spacing

    @spacing.setter
    def spacing(self, value):
        self._spacing = max(0, int(value)); self.update()

    @Property(float)
    def holeRatio(self):
        return self._holeRatio

    @holeRatio.setter
    def holeRatio(self, value):
        self._holeRatio = max(0.0, min(0.95, float(value))); self.update()

    @Property(bool)
    def rounded(self):
        return self._rounded

    @rounded.setter
    def rounded(self, value):
        self._rounded = bool(value); self.update()

    @Property(bool)
    def showTrack(self):
        return self._showTrack

    @showTrack.setter
    def showTrack(self, value):
        self._showTrack = bool(value); self.update()

    @Property(bool)
    def showLabels(self):
        return self._showLabels

    @showLabels.setter
    def showLabels(self, value):
        self._showLabels = bool(value); self.update()

    @Property(bool)
    def showValues(self):
        return self._showValues

    @showValues.setter
    def showValues(self, value):
        self._showValues = bool(value); self.update()

    # -- colours (from tokens via qproperty) --
    @Property(QColor)
    def trackColor(self):
        return self._trackColor

    @trackColor.setter
    def trackColor(self, c):
        self._trackColor = QColor(c); self.update()

    @Property(QColor)
    def labelColor(self):
        return self._labelColor

    @labelColor.setter
    def labelColor(self, c):
        self._labelColor = QColor(c); self.update()
