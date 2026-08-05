########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/@SpinnTV
# WEBSITE: customwidgets.org
########################################################################

########################################################################
## QCustomBeeswarm - a column beeswarm / bubble-stack chart.
##
## Each COLUMN is a thin vertical guide line carrying a vertical stack of
## rounded "pill" bubbles. Every bubble shows a VALUE (its number) and a
## CATEGORY (a colour from `colorsCsv`); the pill's height scales with the
## value between `minSize`..`maxSize`. This is the "check-box product" viz:
## numbered capsules in columns, coloured by Resources / Valid / Invalid.
## Painted (no QtCharts) so it stays crisp and needs no external axis.
##
## Give data in code with setData(columns) where `columns` is a list of
## columns and each column is a list of (value, category) pairs, or in Qt
## Designer with `dataCsv` (columns separated by ';', items by ',', each item
## "value:category" — category is the 1-based colour index, default 1).
## Colours / the number-text colour rules are qproperties so a theme flips
## them on switch. The legend + total are best drawn as sibling labels in the
## card (reuse), not by this widget.
########################################################################
from qtpy.QtCore import Qt, Property, QRectF
from qtpy.QtGui import QColor, QPainter, QBrush, QPen, QFont, QFontMetrics
from qtpy.QtWidgets import QWidget, QSizePolicy


class QCustomBeeswarm(QWidget):

    WIDGET_ICON = "components/icons/bar_chart.png"
    WIDGET_TOOLTIP = "A column beeswarm / numbered bubble-stack chart"
    WIDGET_MODULE = "Custom_Widgets.QCustomBeeswarm"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomBeeswarm' name='customBeeswarm'>
            <property name='geometry'><rect><x>0</x><y>0</y><width>560</width><height>300</height></rect></property>
        </widget>
    </ui>
    """
    __catalog__ = {
        "name": "QCustomBeeswarm",
        "props": {"dataCsv": {"type": "string", "default": ""},
                  "colorsCsv": {"type": "string", "default": "#ffffff,#8fe36b,#f6912b"},
                  "textColorsCsv": {"type": "string", "default": "#1c1c20,#1c1c20,#ffffff"},
                  "lineColor": {"type": "color", "default": "#3a3a40"},
                  "minSize": {"type": "int", "default": 34},
                  "maxSize": {"type": "int", "default": 58},
                  "bubbleWidth": {"type": "int", "default": 42},
                  "gap": {"type": "int", "default": 8},
                  "showValues": {"type": "bool", "default": True},
                  "jitter": {"type": "int", "default": 0}},
        "signals": [],
        "tokens_used": ["accent"],
    }

    # deterministic demo columns: list of (value, category) per column
    _DEMO = [
        [(52, 0), (81, 2)],
        [(96, 1), (25, 0)],
        [(48, 1), (51, 0)],
        [(80, 1), (49, 2)],
        [(34, 2), (67, 1)],
        [(92, 1), (28, 0)],
        [(58, 1), (20, 2)],
        [(84, 2), (39, 1)],
        [(36, 0), (72, 2)],
    ]

    def __init__(self, parent=None, columns=None):
        super().__init__(parent)
        self.setObjectName("QCustomBeeswarm")
        self._cols = [[(float(v), int(c)) for v, c in col] for col in columns] if columns else []
        self._colors = [QColor("#ffffff"), QColor("#8fe36b"), QColor("#f6912b")]
        self._text_colors = [QColor("#1c1c20"), QColor("#1c1c20"), QColor("#ffffff")]
        self._line = QColor("#3a3a40")
        self._min_size = 34
        self._max_size = 58
        self._bubble_w = 42
        self._gap = 8
        self._show_values = True
        self._jitter = 0
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMinimumSize(160, 120)
        if not self._cols:
            self._cols = [[(float(v), int(c)) for v, c in col] for col in self._DEMO]

    # ------------------------------------------------------------------ #
    ## Data API
    # ------------------------------------------------------------------ #
    def setData(self, columns):
        """`columns` = list of columns; each column = list of (value, category)."""
        self._cols = [[(float(v), int(c)) for v, c in col] for col in (columns or [])]
        self.update()

    def data(self):
        return [list(col) for col in self._cols]

    def setColors(self, fills, texts=None):
        self._colors = [QColor(c) for c in fills if c]
        if texts:
            self._text_colors = [QColor(c) for c in texts if c]
        self.update()

    def _value_range(self):
        vals = [v for col in self._cols for (v, _c) in col]
        if not vals:
            return 0.0, 1.0
        return min(vals), max(vals)

    def _fill(self, cat):
        return QColor(self._colors[cat % len(self._colors)]) if self._colors else QColor("#ffffff")

    def _text(self, cat):
        if self._text_colors:
            return QColor(self._text_colors[cat % len(self._text_colors)])
        return QColor("#1c1c20")

    # ------------------------------------------------------------------ #
    ## Painting
    # ------------------------------------------------------------------ #
    def paintEvent(self, e):
        if not self._cols:
            return
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, True)
        w, h = self.width(), self.height()
        n = len(self._cols)
        if n == 0:
            p.end(); return

        lo, hi = self._value_range()
        rng = (hi - lo) or 1.0
        col_w = w / n
        bw = float(min(self._bubble_w, col_w * 0.82))
        gap = float(self._gap)

        vfont = QFont(self.font())
        vfont.setBold(True)

        for i, col in enumerate(self._cols):
            cx = col_w * (i + 0.5)
            if self._jitter:
                # deterministic left/right nudge off the guide line
                cx += (self._jitter if i % 2 else -self._jitter)

            # pill heights for this column
            heights = []
            for (v, _c) in col:
                t = (v - lo) / rng
                heights.append(self._min_size + t * (self._max_size - self._min_size))
            stack_h = sum(heights) + gap * (len(col) - 1)
            # centre the stack vertically with a little breathing room
            top = (h - stack_h) / 2.0

            # guide line spanning the stack
            if len(col) >= 1:
                pen = QPen(self._line, 2)
                pen.setCapStyle(Qt.RoundCap)
                p.setPen(pen)
                p.drawLine(int(cx), int(max(6, top - 8)),
                           int(cx), int(min(h - 6, top + stack_h + 8)))

            y = top
            for (v, c), bh in zip(col, heights):
                fill = self._fill(c)
                rect = QRectF(cx - bw / 2.0, y, bw, bh)
                r = bw / 2.0
                p.setPen(Qt.NoPen)
                p.setBrush(QBrush(fill))
                p.drawRoundedRect(rect, r, r)
                if self._show_values:
                    p.setPen(self._text(c))
                    # fit the number: shrink font for short pills
                    ps = max(8, min(13, int(bh * 0.34)))
                    vfont.setPointSize(ps)
                    p.setFont(vfont)
                    p.drawText(rect, Qt.AlignCenter, ("%g" % v))
                y += bh + gap
        p.end()

    # ------------------------------------------------------------------ #
    ## Designer properties
    # ------------------------------------------------------------------ #
    @Property(str)
    def dataCsv(self):
        return ";".join(
            ",".join("%g:%d" % (v, c) for (v, c) in col) for col in self._cols)

    @dataCsv.setter
    def dataCsv(self, text):
        cols = []
        for chunk in str(text).replace("|", ";").split(";"):
            chunk = chunk.strip()
            if not chunk:
                continue
            col = []
            for tok in chunk.split(","):
                tok = tok.strip()
                if not tok:
                    continue
                if ":" in tok:
                    a, b = tok.split(":", 1)
                    try:
                        col.append((float(a), int(float(b))))
                    except ValueError:
                        pass
                else:
                    try:
                        col.append((float(tok), 0))
                    except ValueError:
                        pass
            if col:
                cols.append(col)
        if cols:
            self.setData(cols)

    @Property(str)
    def colorsCsv(self):
        return ",".join(c.name() for c in self._colors)

    @colorsCsv.setter
    def colorsCsv(self, text):
        cols = [t.strip() for t in str(text).replace(";", ",").split(",") if t.strip()]
        if cols:
            self._colors = [QColor(c) for c in cols]
            self.update()

    @Property(str)
    def textColorsCsv(self):
        return ",".join(c.name() for c in self._text_colors)

    @textColorsCsv.setter
    def textColorsCsv(self, text):
        cols = [t.strip() for t in str(text).replace(";", ",").split(",") if t.strip()]
        if cols:
            self._text_colors = [QColor(c) for c in cols]
            self.update()

    @Property(QColor)
    def lineColor(self):
        return self._line

    @lineColor.setter
    def lineColor(self, c):
        self._line = QColor(c)
        self.update()

    @Property(int)
    def minSize(self):
        return self._min_size

    @minSize.setter
    def minSize(self, v):
        self._min_size = max(6, int(v))
        self.update()

    @Property(int)
    def maxSize(self):
        return self._max_size

    @maxSize.setter
    def maxSize(self, v):
        self._max_size = max(self._min_size, int(v))
        self.update()

    @Property(int)
    def bubbleWidth(self):
        return self._bubble_w

    @bubbleWidth.setter
    def bubbleWidth(self, v):
        self._bubble_w = max(8, int(v))
        self.update()

    @Property(int)
    def gap(self):
        return self._gap

    @gap.setter
    def gap(self, v):
        self._gap = max(0, int(v))
        self.update()

    @Property(bool)
    def showValues(self):
        return self._show_values

    @showValues.setter
    def showValues(self, v):
        self._show_values = bool(v)
        self.update()

    @Property(int)
    def jitter(self):
        return self._jitter

    @jitter.setter
    def jitter(self, v):
        self._jitter = max(0, int(v))
        self.update()
