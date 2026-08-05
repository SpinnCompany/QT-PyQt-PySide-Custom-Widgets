########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/@SpinnTV
# WEBSITE: customwidgets.org
########################################################################

########################################################################
## QCustomFunnelChart - a painted funnel / pyramid chart.
##
## Stacked trapezoid stages narrowing toward the end: a conversion funnel, a
## sales pipeline, a drop-off analysis. Each stage's width encodes its value
## and the taper between stages is the loss.
##
## Pyramid is the SAME chart inverted, so it is a `shape` property rather than
## a second widget - MUI ships them as two components, which duplicates every
## property for one flipped polygon.
##
## QPainter only, NO QtCharts (see docs/design/mui-charts-gap.md).
##
## Data goes in with setStages([...]) in code, or stagesCsv in Qt Designer:
##
##     stagesCsv = "Visits=1000,Signups=420,Trials=180,Paid=64"
##
## Emits stageHovered(int) and stageClicked(int); -1 means "nothing".
########################################################################
from qtpy.QtCore import Qt, Signal, Property, QRectF, QSize, QPointF
from qtpy.QtGui import QColor, QPainter, QPen, QBrush, QPolygonF, QFontMetrics
from qtpy.QtWidgets import QWidget, QSizePolicy


class QCustomFunnelChart(QWidget):
    stageHovered = Signal(int)
    stageClicked = Signal(int)

    WIDGET_ICON = "components/icons/filter_alt.png"
    WIDGET_TOOLTIP = "A painted funnel / pyramid chart"
    WIDGET_MODULE = "Custom_Widgets.QCustomFunnelChart"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomFunnelChart' name='customFunnelChart'>
            <property name='geometry'><rect><x>0</x><y>0</y><width>360</width><height>300</height></rect></property>
            <property name='stagesCsv'><string>Visits=1000,Signups=420,Trials=180,Paid=64</string></property>
        </widget>
    </ui>
    """
    __catalog__ = {
        "name": "QCustomFunnelChart",
        "props": {"stagesCsv": {"type": "string", "default": ""},
                  "colorsCsv": {"type": "string", "default": ""},
                  "shape": {"type": "enum", "values": ["funnel", "pyramid"],
                            "default": "funnel"},
                  "orientation": {"type": "enum", "values": ["vertical", "horizontal"],
                                  "default": "vertical"},
                  "gapPx": {"type": "int", "default": 3},
                  "neckRatio": {"type": "float", "default": 0.0},
                  "showLabels": {"type": "bool", "default": True},
                  "showValues": {"type": "bool", "default": True},
                  "showPercent": {"type": "bool", "default": False},
                  "percentOf": {"type": "enum", "values": ["first", "previous"],
                                "default": "first"},
                  "labelColor": {"type": "color", "default": "#ffffff"},
                  "outsideLabelColor": {"type": "color", "default": "#0f172a"}},
        "signals": ["stageHovered", "stageClicked"],
        "tokens_used": ["accent", "on-surface", "surface"],
    }

    _DEFAULT_COLORS = ["#2563eb", "#3b82f6", "#60a5fa", "#93c5fd", "#bfdbfe",
                       "#dbeafe"]

    def __init__(self, parent=None, stages=None):
        super().__init__(parent)
        self.setObjectName("QCustomFunnelChart")
        self._stages = []           # list of (label, value)
        self._colors = []
        self._shape = "funnel"
        self._orientation = "vertical"
        self._gap = 3
        self._neckRatio = 0.0       # 0 = taper to a point at the last stage
        self._showLabels = True
        self._showValues = True
        self._showPercent = False
        self._percentOf = "first"
        self._hover = -1
        self._bands = []            # per-stage polygon, parallel to _stages

        self._labelColor = QColor("#ffffff")
        self._outsideLabelColor = QColor("#0f172a")

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMouseTracking(True)
        if stages:
            self.setStages(stages)

    # ------------------------------------------------------------------ #
    ## Data
    # ------------------------------------------------------------------ #
    @staticmethod
    def _coerce(stage):
        if isinstance(stage, dict):
            label, value = stage.get("label"), stage.get("value")
        elif isinstance(stage, (tuple, list)) and len(stage) >= 2:
            label, value = stage[0], stage[1]
        else:
            return None
        try:
            return (str(label), max(0.0, float(value)))
        except (TypeError, ValueError):
            return None

    def setStages(self, stages):
        self._stages = [s for s in (self._coerce(x) for x in (stages or [])) if s]
        self._hover = -1
        self.update()

    def stages(self):
        return list(self._stages)

    def stageCount(self):
        return len(self._stages)

    def clearStages(self):
        self._stages = []
        self._hover = -1
        self.update()

    def maximum(self):
        """The value the widest band represents; never zero."""
        return max((v for _l, v in self._stages), default=0.0) or 1.0

    def stageColor(self, index):
        if 0 <= index < len(self._colors) and self._colors[index] is not None:
            return QColor(self._colors[index])
        return QColor(self._DEFAULT_COLORS[index % len(self._DEFAULT_COLORS)])

    def percentFor(self, index):
        """Conversion percentage for a stage, per `percentOf`."""
        if not (0 <= index < len(self._stages)):
            return 0.0
        value = self._stages[index][1]
        if self._percentOf == "previous" and index > 0:
            base = self._stages[index - 1][1]
        else:
            base = self._stages[0][1]
        return (value / base * 100.0) if base else 0.0

    # ------------------------------------------------------------------ #
    ## Geometry
    # ------------------------------------------------------------------ #
    def sizeHint(self):
        return QSize(360, 300)

    def minimumSizeHint(self):
        return QSize(120, 100)

    def _plotRect(self):
        return QRectF(8, 8, max(1.0, self.width() - 16),
                      max(1.0, self.height() - 16))

    def _halfWidthAt(self, value):
        """Half-extent of a band, as a fraction of the plot's half-width."""
        peak = self.maximum()
        fraction = value / peak if peak else 0.0
        # neckRatio floors the taper so a funnel can end in a spout rather
        # than a point; 0 keeps the classic full taper.
        floor = max(0.0, min(1.0, self._neckRatio))
        return (floor + (1.0 - floor) * fraction) / 2.0

    def _computeBands(self):
        """Trapezoid per stage. Each band's far edge matches the next band's
        near edge, so the funnel reads as one continuous shape."""
        self._bands = []
        count = len(self._stages)
        if not count:
            return
        rect = self._plotRect()
        horizontal = self._orientation == "horizontal"
        length = rect.width() if horizontal else rect.height()
        extent = rect.height() if horizontal else rect.width()
        gap = float(self._gap)
        band = (length - gap * (count - 1)) / count

        for index, (_label, value) in enumerate(self._stages):
            nearValue = value
            nextValue = self._stages[index + 1][1] if index + 1 < count else (
                value if self._neckRatio > 0 else 0.0)
            nearHalf = self._halfWidthAt(nearValue) * extent
            farHalf = self._halfWidthAt(nextValue) * extent

            start = (rect.top() if not horizontal else rect.left()) + index * (band + gap)
            stop = start + band
            centre = rect.center().y() if horizontal else rect.center().x()

            if horizontal:
                poly = QPolygonF([QPointF(start, centre - nearHalf),
                                  QPointF(stop, centre - farHalf),
                                  QPointF(stop, centre + farHalf),
                                  QPointF(start, centre + nearHalf)])
            else:
                poly = QPolygonF([QPointF(centre - nearHalf, start),
                                  QPointF(centre + nearHalf, start),
                                  QPointF(centre + farHalf, stop),
                                  QPointF(centre - farHalf, stop)])
            self._bands.append(poly)

        if self._shape == "pyramid":
            # Mirror the finished chain rather than swapping each band's own
            # edges: swapping per band leaves band i's far edge no longer
            # matching band i+1's near edge, so the shape comes apart at every
            # seam. Mirroring keeps it continuous by construction.
            self._bands = [self._mirror(poly, rect, horizontal)
                           for poly in self._bands]

    @staticmethod
    def _mirror(poly, rect, horizontal):
        """Flip a polygon across the plot's centre line, along the flow axis."""
        out = QPolygonF()
        for point in poly:
            if horizontal:
                out.append(QPointF(rect.left() + rect.right() - point.x(),
                                   point.y()))
            else:
                out.append(QPointF(point.x(),
                                   rect.top() + rect.bottom() - point.y()))
        return out

    def bands(self):
        if not self._bands:
            self._computeBands()
        return list(self._bands)

    # ------------------------------------------------------------------ #
    ## Painting
    # ------------------------------------------------------------------ #
    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.setFont(self.font())
        self._computeBands()
        if not self._stages:
            return

        for index, poly in enumerate(self._bands):
            colour = self.stageColor(index)
            if index == self._hover:
                colour = colour.lighter(112)
            p.setPen(Qt.NoPen)
            p.setBrush(QBrush(colour))
            p.drawPolygon(poly)

        if self._showLabels or self._showValues or self._showPercent:
            self._paintLabels(p)

    def _labelFor(self, index):
        label, value = self._stages[index]
        parts = []
        if self._showLabels:
            parts.append(label)
        if self._showValues:
            parts.append("%g" % value)
        if self._showPercent:
            parts.append("%.0f%%" % self.percentFor(index))
        return "  ".join(parts)

    def _paintLabels(self, p):
        fm = QFontMetrics(self.font())
        for index, poly in enumerate(self._bands):
            text = self._labelFor(index)
            if not text:
                continue
            box = poly.boundingRect()
            width = fm.horizontalAdvance(text)
            # Narrow bands cannot hold their label: put it outside and use the
            # on-surface colour, or the text disappears into the background.
            inside = width + 12 <= box.width() and box.height() >= fm.height()
            if inside:
                p.setPen(QPen(self._labelColor))
                p.drawText(box, int(Qt.AlignCenter), text)
                continue

            p.setPen(QPen(self._outsideLabelColor))
            # Outside labels go PERPENDICULAR to the flow. Pushing them along
            # it (right, on a horizontal funnel) lands them inside the next
            # band, so every label piles up on top of the others.
            if self._orientation == "horizontal":
                target = QRectF(box.center().x() - width / 2.0,
                                max(0.0, box.top() - fm.height() - 2),
                                width, fm.height())
                if target.top() < 0:
                    target.moveTop(min(self.height() - fm.height(),
                                       box.bottom() + 2))
                p.drawText(target, int(Qt.AlignCenter), text)
                continue

            target = QRectF(box.right() + 6, box.center().y() - fm.height() / 2.0,
                            max(0.0, self.width() - box.right() - 8), fm.height())
            if target.width() < width:
                target = QRectF(max(0.0, box.left() - width - 6),
                                box.center().y() - fm.height() / 2.0,
                                width, fm.height())
                p.drawText(target, int(Qt.AlignRight | Qt.AlignVCenter), text)
            else:
                p.drawText(target, int(Qt.AlignLeft | Qt.AlignVCenter), text)

    # ------------------------------------------------------------------ #
    ## Interaction
    # ------------------------------------------------------------------ #
    def stageAt(self, pos):
        point = QPointF(pos)
        for index, poly in enumerate(self.bands()):
            if poly.containsPoint(point, Qt.OddEvenFill):
                return index
        return -1

    def mouseMoveEvent(self, e):
        index = self.stageAt(e.pos())
        if index != self._hover:
            self._hover = index
            self.stageHovered.emit(index)
            self.update()
        super().mouseMoveEvent(e)

    def leaveEvent(self, e):
        if self._hover != -1:
            self._hover = -1
            self.stageHovered.emit(-1)
            self.update()
        super().leaveEvent(e)

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.LeftButton:
            index = self.stageAt(e.pos())
            if index >= 0:
                self.stageClicked.emit(index)
        super().mouseReleaseEvent(e)

    # ------------------------------------------------------------------ #
    ## Designer properties
    # ------------------------------------------------------------------ #
    @Property(str)
    def stagesCsv(self):
        return ",".join("%s=%g" % (label, value) for label, value in self._stages)

    @stagesCsv.setter
    def stagesCsv(self, text):
        stages = []
        for chunk in str(text).replace(";", ",").split(","):
            chunk = chunk.strip()
            if not chunk:
                continue
            if "=" in chunk:
                label, _, raw = chunk.partition("=")
            else:
                label, raw = "Stage %d" % (len(stages) + 1), chunk
            try:
                stages.append((label.strip() or "Stage %d" % (len(stages) + 1),
                               max(0.0, float(raw.strip()))))
            except ValueError:
                continue
        self.setStages(stages)

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

    @Property(str)
    def shape(self):
        return self._shape

    @shape.setter
    def shape(self, value):
        self._shape = "pyramid" if str(value) == "pyramid" else "funnel"
        self.update()

    @Property(str)
    def orientation(self):
        return self._orientation

    @orientation.setter
    def orientation(self, value):
        self._orientation = "horizontal" if str(value) == "horizontal" else "vertical"
        self.update()

    @Property(int)
    def gapPx(self):
        return self._gap

    @gapPx.setter
    def gapPx(self, value):
        self._gap = max(0, int(value)); self.update()

    @Property(float)
    def neckRatio(self):
        return self._neckRatio

    @neckRatio.setter
    def neckRatio(self, value):
        self._neckRatio = max(0.0, min(1.0, float(value))); self.update()

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

    @Property(bool)
    def showPercent(self):
        return self._showPercent

    @showPercent.setter
    def showPercent(self, value):
        self._showPercent = bool(value); self.update()

    @Property(str)
    def percentOf(self):
        return self._percentOf

    @percentOf.setter
    def percentOf(self, value):
        self._percentOf = "previous" if str(value) == "previous" else "first"
        self.update()

    # -- colours (from tokens via qproperty) --
    @Property(QColor)
    def labelColor(self):
        return self._labelColor

    @labelColor.setter
    def labelColor(self, c):
        self._labelColor = QColor(c); self.update()

    @Property(QColor)
    def outsideLabelColor(self):
        return self._outsideLabelColor

    @outsideLabelColor.setter
    def outsideLabelColor(self, c):
        self._outsideLabelColor = QColor(c); self.update()
