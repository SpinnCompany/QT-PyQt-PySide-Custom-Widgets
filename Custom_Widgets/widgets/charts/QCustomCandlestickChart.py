########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/spinnTv
# WEBSITE: spinncode.com
########################################################################

########################################################################
## QCustomCandlestickChart - a painted OHLC / candlestick price chart.
##
## Each candle is one period: a filled body spanning open->close and a wick
## spanning low->high. Candles are coloured by direction - up when close >= open,
## down otherwise - which is the whole point of the form.
##
## Rendered entirely with QPainter and NO QtCharts dependency. That is
## deliberate and load-bearing: Qt Charts is GPLv3-or-commercial with no LGPL
## option, so anything built on it cannot ship inside a proprietary wheel. This
## widget stays clean.
##
## Data goes in with setData([(open, high, low, close), ...]) in code, or the
## ohlcCsv property in Qt Designer ("o,h,l,c;o,h,l,c;..."), following the
## valuesCsv convention used by the other painted charts.
##
## Emits candleHovered(int) and candleClicked(int); -1 means "nothing".
########################################################################
from qtpy.QtCore import Qt, Signal, Property, QRectF, QSize, QPointF
from qtpy.QtGui import QColor, QPainter, QPen, QBrush, QFontMetrics
from qtpy.QtWidgets import QWidget, QSizePolicy


class QCustomCandlestickChart(QWidget):
    candleHovered = Signal(int)
    candleClicked = Signal(int)

    WIDGET_ICON = "components/icons/candlestick_chart.png"
    WIDGET_TOOLTIP = "A painted OHLC / candlestick price chart"
    WIDGET_MODULE = "Custom_Widgets.QCustomCandlestickChart"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomCandlestickChart' name='customCandlestickChart'>
            <property name='geometry'><rect><x>0</x><y>0</y><width>520</width><height>280</height></rect></property>
            <property name='ohlcCsv'><string>26,28,25,27;27,30,26,29;29,29.5,27,27.5;27.5,31,27,30.5;30.5,32,30,31</string></property>
        </widget>
    </ui>
    """
    __catalog__ = {
        "name": "QCustomCandlestickChart",
        "props": {"ohlcCsv": {"type": "string", "default": ""},
                  "labelsCsv": {"type": "string", "default": ""},
                  "upColor": {"type": "color", "default": "#16a34a"},
                  "downColor": {"type": "color", "default": "#dc2626"},
                  "wickColor": {"type": "color", "default": "#64748b"},
                  "gridColor": {"type": "color", "default": "#e2e8f0"},
                  "axisTextColor": {"type": "color", "default": "#64748b"},
                  "showGrid": {"type": "bool", "default": True},
                  "showPriceAxis": {"type": "bool", "default": True},
                  "showLabels": {"type": "bool", "default": True},
                  "showTooltip": {"type": "bool", "default": True},
                  "hollowUpCandles": {"type": "bool", "default": False},
                  "candleWidthRatio": {"type": "float", "default": 0.62},
                  "gridLines": {"type": "int", "default": 4},
                  "pricePrecision": {"type": "int", "default": 2}},
        "signals": ["candleHovered", "candleClicked"],
        "tokens_used": ["success", "destructive", "outline", "on-surface"],
    }

    _PAD_L_NO_AXIS = 8
    _PAD_R = 8
    _PAD_T = 10
    _PAD_B_NO_LABELS = 8

    def __init__(self, parent=None, data=None, labels=None):
        super().__init__(parent)
        self.setObjectName("QCustomCandlestickChart")
        self._data = []            # list of (open, high, low, close)
        self._labels = []
        self._rects = []           # per-candle hit rect, parallel to _data
        self._hover = -1

        self._up = QColor("#16a34a")
        self._down = QColor("#dc2626")
        self._wick = QColor("#64748b")
        self._grid = QColor("#e2e8f0")
        self._axisText = QColor("#64748b")
        self._tooltipBg = QColor("#0f172a")
        self._tooltipText = QColor("#f8fafc")

        self._showGrid = True
        self._showPriceAxis = True
        self._showLabels = True
        self._showTooltip = True
        self._hollowUp = False
        self._widthRatio = 0.62
        self._gridLines = 4
        self._precision = 2

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMouseTracking(True)
        self.setCursor(Qt.CrossCursor)
        if data:
            self.setData(data, labels)
        elif labels:
            self._labels = [str(x) for x in labels]

    # ------------------------------------------------------------------ #
    ## Data
    # ------------------------------------------------------------------ #
    @staticmethod
    def _coerce(candle):
        """Accept (o,h,l,c), [o,h,l,c] or a dict with those keys."""
        if isinstance(candle, dict):
            vals = (candle.get("open"), candle.get("high"),
                    candle.get("low"), candle.get("close"))
        else:
            try:
                vals = tuple(candle)[:4]
            except TypeError:          # None, a bare number, any non-iterable
                return None
        if len(vals) != 4 or any(v is None for v in vals):
            return None
        try:
            o, h, l, c = (float(v) for v in vals)
        except (TypeError, ValueError):
            return None
        # Tolerate high/low that do not actually bound the body rather than
        # dropping the candle: a feed that swaps them should still render.
        hi = max(o, h, l, c)
        lo = min(o, h, l, c)
        return (o, hi, lo, c)

    def setData(self, data, labels=None):
        """Replace every candle. Each item is (open, high, low, close)."""
        out = []
        for candle in data or []:
            coerced = self._coerce(candle)
            if coerced is not None:
                out.append(coerced)
        self._data = out
        if labels is not None:
            self._labels = [str(x) for x in labels]
        self._hover = -1
        self.updateGeometry()
        self.update()

    def data(self):
        return list(self._data)

    def count(self):
        return len(self._data)

    def setLabels(self, labels):
        self._labels = [str(x) for x in (labels or [])]
        self.update()

    def labels(self):
        return list(self._labels)

    def priceRange(self):
        """(low, high) across every candle, or (0.0, 1.0) when empty."""
        if not self._data:
            return (0.0, 1.0)
        lo = min(c[2] for c in self._data)
        hi = max(c[1] for c in self._data)
        if hi == lo:                       # flat series: give it room to draw
            return (lo - 0.5, hi + 0.5)
        return (lo, hi)

    # ------------------------------------------------------------------ #
    ## Geometry
    # ------------------------------------------------------------------ #
    def sizeHint(self):
        return QSize(520, 280)

    def minimumSizeHint(self):
        return QSize(160, 90)

    def _priceAxisWidth(self):
        if not self._showPriceAxis:
            return self._PAD_L_NO_AXIS
        lo, hi = self.priceRange()
        fm = QFontMetrics(self.font())
        widest = max(fm.horizontalAdvance(self._fmtPrice(v)) for v in (lo, hi))
        return widest + 12

    def _labelStripHeight(self):
        if not (self._showLabels and self._labels):
            return self._PAD_B_NO_LABELS
        return QFontMetrics(self.font()).height() + 6

    def _plotRect(self):
        left = self._priceAxisWidth()
        bottom = self._labelStripHeight()
        return QRectF(left, self._PAD_T,
                      max(1.0, self.width() - left - self._PAD_R),
                      max(1.0, self.height() - self._PAD_T - bottom))

    def _fmtPrice(self, v):
        return "%.*f" % (self._precision, v)

    # ------------------------------------------------------------------ #
    ## Painting
    # ------------------------------------------------------------------ #
    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        plot = self._plotRect()
        lo, hi = self.priceRange()
        span = (hi - lo) or 1.0

        def y_for(price):
            return plot.bottom() - (price - lo) / span * plot.height()

        if self._showGrid or self._showPriceAxis:
            self._paintGrid(p, plot, lo, span, y_for)

        self._rects = []
        if not self._data:
            return

        slot = plot.width() / len(self._data)
        body_w = max(1.0, slot * self._widthRatio)

        for i, (o, h, l, c) in enumerate(self._data):
            cx = plot.left() + slot * (i + 0.5)
            up = c >= o
            colour = self._up if up else self._down

            # wick first so the body paints over it
            p.setPen(QPen(self._wick, 1))
            p.drawLine(QPointF(cx, y_for(h)), QPointF(cx, y_for(l)))

            top, bottom = y_for(max(o, c)), y_for(min(o, c))
            # A doji (open == close) has zero height; give it a visible line.
            if bottom - top < 1.0:
                bottom = top + 1.0
            body = QRectF(cx - body_w / 2.0, top, body_w, bottom - top)

            if i == self._hover:
                p.setPen(Qt.NoPen)
                p.setBrush(QBrush(QColor(colour.red(), colour.green(),
                                         colour.blue(), 38)))
                p.drawRect(QRectF(cx - slot / 2.0, plot.top(), slot, plot.height()))

            if self._hollowUp and up:
                p.setPen(QPen(colour, 1.4))
                p.setBrush(Qt.NoBrush)
            else:
                p.setPen(QPen(colour, 1))
                p.setBrush(QBrush(colour))
            p.drawRect(body)

            self._rects.append(QRectF(cx - slot / 2.0, plot.top(),
                                      slot, plot.height()))

        if self._showLabels and self._labels:
            self._paintLabels(p, plot, slot)

        if self._showTooltip and 0 <= self._hover < len(self._data):
            self._paintTooltip(p, plot, slot)

    def _paintGrid(self, p, plot, lo, span, y_for):
        lines = max(1, self._gridLines)
        fm = QFontMetrics(self.font())
        p.setFont(self.font())
        for i in range(lines + 1):
            price = lo + span * i / lines
            y = y_for(price)
            if self._showGrid:
                p.setPen(QPen(self._grid, 1))
                p.drawLine(QPointF(plot.left(), y), QPointF(plot.right(), y))
            if self._showPriceAxis:
                p.setPen(QPen(self._axisText))
                text = self._fmtPrice(price)
                p.drawText(QRectF(0, y - fm.height() / 2.0,
                                  plot.left() - 6, fm.height()),
                           int(Qt.AlignRight | Qt.AlignVCenter), text)

    def _paintLabels(self, p, plot, slot):
        fm = QFontMetrics(self.font())
        p.setPen(QPen(self._axisText))
        p.setFont(self.font())
        # Thin the labels out so they never overlap: draw every nth that fits.
        widest = max((fm.horizontalAdvance(s) for s in self._labels), default=1)
        step = max(1, int((widest + 10) // max(1.0, slot)) + (0 if slot >= widest + 10 else 1))
        for i, text in enumerate(self._labels[:len(self._data)]):
            if i % step:
                continue
            cx = plot.left() + slot * (i + 0.5)
            p.drawText(QRectF(cx - slot, plot.bottom() + 2, slot * 2, fm.height()),
                       int(Qt.AlignHCenter | Qt.AlignVCenter), text)

    def _paintTooltip(self, p, plot, slot):
        o, h, l, c = self._data[self._hover]
        label = (self._labels[self._hover]
                 if self._hover < len(self._labels) else "#%d" % self._hover)
        rows = ["%s" % label,
                "O %s   H %s" % (self._fmtPrice(o), self._fmtPrice(h)),
                "L %s   C %s" % (self._fmtPrice(l), self._fmtPrice(c))]
        fm = QFontMetrics(self.font())
        w = max(fm.horizontalAdvance(r) for r in rows) + 16
        row_h = fm.height()
        box_h = row_h * len(rows) + 12

        cx = plot.left() + slot * (self._hover + 0.5)
        x = cx + 10
        if x + w > plot.right():           # flip to the left near the edge
            x = cx - 10 - w
        x = max(plot.left(), min(x, plot.right() - w))
        y = max(plot.top(), plot.top() + 6)

        p.setPen(Qt.NoPen)
        p.setBrush(QBrush(QColor(self._tooltipBg.red(), self._tooltipBg.green(),
                                 self._tooltipBg.blue(), 235)))
        p.drawRoundedRect(QRectF(x, y, w, box_h), 6, 6)
        p.setPen(QPen(self._tooltipText))
        p.setFont(self.font())
        for i, text in enumerate(rows):
            p.drawText(QRectF(x + 8, y + 6 + i * row_h, w - 16, row_h),
                       int(Qt.AlignLeft | Qt.AlignVCenter), text)

    # ------------------------------------------------------------------ #
    ## Interaction
    # ------------------------------------------------------------------ #
    def candleAt(self, pos):
        """Index of the candle under a point, or -1."""
        for i, rect in enumerate(self._rects):
            if rect.contains(QPointF(pos)):
                return i
        return -1

    def mouseMoveEvent(self, e):
        i = self.candleAt(e.pos())
        if i != self._hover:
            self._hover = i
            self.candleHovered.emit(i)
            self.update()
        super().mouseMoveEvent(e)

    def leaveEvent(self, e):
        if self._hover != -1:
            self._hover = -1
            self.candleHovered.emit(-1)
            self.update()
        super().leaveEvent(e)

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.LeftButton:
            i = self.candleAt(e.pos())
            if i >= 0:
                self.candleClicked.emit(i)
        super().mouseReleaseEvent(e)

    # ------------------------------------------------------------------ #
    ## Designer properties
    # ------------------------------------------------------------------ #
    @Property(str)
    def ohlcCsv(self):
        return ";".join(",".join("%g" % v for v in candle) for candle in self._data)

    @ohlcCsv.setter
    def ohlcCsv(self, text):
        candles = []
        for chunk in str(text).split(";"):
            parts = [tok.strip() for tok in chunk.split(",") if tok.strip()]
            if len(parts) < 4:
                continue
            try:
                candles.append(tuple(float(v) for v in parts[:4]))
            except ValueError:
                continue
        self.setData(candles)

    @Property(str)
    def labelsCsv(self):
        return ",".join(self._labels)

    @labelsCsv.setter
    def labelsCsv(self, text):
        self.setLabels([tok.strip() for tok in str(text).replace(";", ",").split(",")
                        if tok.strip()])

    @Property(bool)
    def showGrid(self):
        return self._showGrid

    @showGrid.setter
    def showGrid(self, v):
        self._showGrid = bool(v); self.update()

    @Property(bool)
    def showPriceAxis(self):
        return self._showPriceAxis

    @showPriceAxis.setter
    def showPriceAxis(self, v):
        self._showPriceAxis = bool(v); self.update()

    @Property(bool)
    def showLabels(self):
        return self._showLabels

    @showLabels.setter
    def showLabels(self, v):
        self._showLabels = bool(v); self.update()

    @Property(bool)
    def showTooltip(self):
        return self._showTooltip

    @showTooltip.setter
    def showTooltip(self, v):
        self._showTooltip = bool(v); self.update()

    @Property(bool)
    def hollowUpCandles(self):
        return self._hollowUp

    @hollowUpCandles.setter
    def hollowUpCandles(self, v):
        self._hollowUp = bool(v); self.update()

    @Property(float)
    def candleWidthRatio(self):
        return self._widthRatio

    @candleWidthRatio.setter
    def candleWidthRatio(self, v):
        self._widthRatio = max(0.05, min(1.0, float(v))); self.update()

    @Property(int)
    def gridLines(self):
        return self._gridLines

    @gridLines.setter
    def gridLines(self, v):
        self._gridLines = max(1, int(v)); self.update()

    @Property(int)
    def pricePrecision(self):
        return self._precision

    @pricePrecision.setter
    def pricePrecision(self, v):
        self._precision = max(0, int(v)); self.update()

    # -- colours (from tokens via qproperty) --
    @Property(QColor)
    def upColor(self):
        return self._up

    @upColor.setter
    def upColor(self, c):
        self._up = QColor(c); self.update()

    @Property(QColor)
    def downColor(self):
        return self._down

    @downColor.setter
    def downColor(self, c):
        self._down = QColor(c); self.update()

    @Property(QColor)
    def wickColor(self):
        return self._wick

    @wickColor.setter
    def wickColor(self, c):
        self._wick = QColor(c); self.update()

    @Property(QColor)
    def gridColor(self):
        return self._grid

    @gridColor.setter
    def gridColor(self, c):
        self._grid = QColor(c); self.update()

    @Property(QColor)
    def axisTextColor(self):
        return self._axisText

    @axisTextColor.setter
    def axisTextColor(self, c):
        self._axisText = QColor(c); self.update()

    @Property(QColor)
    def tooltipBackgroundColor(self):
        return self._tooltipBg

    @tooltipBackgroundColor.setter
    def tooltipBackgroundColor(self, c):
        self._tooltipBg = QColor(c); self.update()

    @Property(QColor)
    def tooltipTextColor(self):
        return self._tooltipText

    @tooltipTextColor.setter
    def tooltipTextColor(self, c):
        self._tooltipText = QColor(c); self.update()
