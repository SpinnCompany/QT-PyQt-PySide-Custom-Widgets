########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/spinnTv
# WEBSITE: spinncode.com
########################################################################

########################################################################
## QCustomMiniBarChart - a compact, axis-less bar chart.
##
## The painted sibling of QCustomSparkline: a row of bottom-aligned bars with
## rounded tops, PER-BAR colours, an optional highlighted bar, and optional
## labels underneath (e.g. day numbers). Unlike the QtCharts QCustomBarChart it
## carries no axes/grid/legend/toolbar and stays crisp at any size - perfect for
## a dashboard panel where each bar wants its own colour (idle / accent / a
## single highlighted value). Give data via setData([...]) in code, or the
## valuesCsv / colorsCsv / labelsCsv properties in Qt Designer.
########################################################################
from qtpy.QtCore import Qt, Property, QRectF
from qtpy.QtGui import QColor, QPainter, QBrush, QPainterPath, QFont, QFontMetrics
from qtpy.QtWidgets import QWidget, QSizePolicy


class QCustomMiniBarChart(QWidget):

    WIDGET_ICON = "components/icons/bar_chart.png"
    WIDGET_TOOLTIP = "A compact axis-less bar chart (per-bar colours, labels)"
    WIDGET_MODULE = "Custom_Widgets.QCustomMiniBarChart"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomMiniBarChart' name='customMiniBarChart'>
            <property name='geometry'><rect><x>0</x><y>0</y><width>320</width><height>150</height></rect></property>
        </widget>
    </ui>
    """
    __catalog__ = {
        "name": "QCustomMiniBarChart",
        "props": {"valuesCsv": {"type": "string", "default": "6,12,10,7,14,18,7,13,19,22,14"},
                  "colorsCsv": {"type": "string", "default": ""},
                  "labelsCsv": {"type": "string", "default": ""},
                  "barColor": {"type": "color", "default": "#3355e8"},
                  "idleColor": {"type": "color", "default": "#d7dbe6"},
                  "highlightColor": {"type": "color", "default": "#2fce80"},
                  "highlightIndex": {"type": "int", "default": -1},
                  "barWidth": {"type": "int", "default": 9},
                  "cornerRadius": {"type": "int", "default": 4},
                  "showLabels": {"type": "bool", "default": True},
                  "calloutText": {"type": "string", "default": ""},
                  "calloutBg": {"type": "color", "default": "#ffffff"},
                  "calloutTextColor": {"type": "color", "default": "#1a1e2c"},
                  "yLabelsCsv": {"type": "string", "default": ""},
                  "yLabelColor": {"type": "color", "default": "#8b909e"}},
        "signals": [],
        "tokens_used": ["accent"],
    }

    def __init__(self, parent=None, values=None, colors=None, labels=None):
        super().__init__(parent)
        self.setObjectName("QCustomMiniBarChart")
        self._values = [float(v) for v in (values or [])]
        self._colors = [QColor(c) for c in colors] if colors else []   # per-bar override
        self._labels = list(labels) if labels else []
        self._bar_color = QColor("#3355e8")     # default bar colour
        self._idle_color = QColor("#d7dbe6")    # unset/idle bars (see idleAtOrBelow)
        self._highlight_color = QColor("#2fce80")
        self._highlight_index = -1
        self._idle_at_or_below = None           # values <= this render idle (optional)
        self._bar_width = 9
        self._corner_radius = 4
        self._spacing = 10
        self._show_labels = True
        self._label_color = QColor("#8b909e")
        self._label_size = 11
        self._baseline_gap = 10                 # gap between bars and labels
        # Opt-in reference-style extras (all default OFF / empty):
        self._callout_text = ""                 # bubble above the highlighted bar
        self._callout_bg = QColor("#ffffff")
        self._callout_text_color = QColor("#1a1e2c")
        self._y_labels = []                     # [(value, text)] left-edge scale
        self._y_label_color = QColor("#8b909e")
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMinimumSize(60, 60)

    # ------------------------------------------------------------------ #
    ## Data API
    # ------------------------------------------------------------------ #
    def setData(self, values, colors=None, labels=None):
        self._values = [float(v) for v in (values or [])]
        if colors is not None:
            self._colors = [QColor(c) for c in colors]
        if labels is not None:
            self._labels = list(labels)
        self.update()

    def setValues(self, values):
        self._values = [float(v) for v in (values or [])]
        self.update()

    def setBarColors(self, colors):
        """Give each bar its own colour (list parallel to values)."""
        self._colors = [QColor(c) for c in (colors or [])]
        self.update()

    def setLabels(self, labels):
        self._labels = list(labels or [])
        self.update()

    def highlightIndex(self, index, color=None):
        """Highlight a single bar (in highlightColor, or the given colour)."""
        self._highlight_index = int(index)
        if color is not None:
            self._highlight_color = QColor(color)
        self.update()

    def clearHighlight(self):
        self._highlight_index = -1
        self.update()

    def setIdleThreshold(self, value):
        """Bars whose value is <= value paint in idleColor (e.g. weekends)."""
        self._idle_at_or_below = None if value is None else float(value)
        self.update()

    def values(self):
        return list(self._values)

    # ------------------------------------------------------------------ #
    ## Painting
    # ------------------------------------------------------------------ #
    def _bar_color_for(self, i, val):
        if i == self._highlight_index:
            return self._highlight_color
        if self._colors and i < len(self._colors):
            return self._colors[i]
        if self._idle_at_or_below is not None and val <= self._idle_at_or_below:
            return self._idle_color
        return self._bar_color

    @staticmethod
    def _top_rounded_path(x, y, w, h, r):
        r = max(0.0, min(r, w / 2.0, h))
        p = QPainterPath()
        p.moveTo(x, y + h)
        p.lineTo(x, y + r)
        p.quadTo(x, y, x + r, y)
        p.lineTo(x + w - r, y)
        p.quadTo(x + w, y, x + w, y + r)
        p.lineTo(x + w, y + h)
        p.closeSubpath()
        return p

    def paintEvent(self, e):
        if not self._values:
            return
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, True)

        w, h = self.width(), self.height()
        show_labels = bool(self._show_labels and self._labels)
        # Reserve the real text height (not the point size) + the gap, so labels
        # never clip at the widget's bottom edge.
        lbl_font = QFont(self.font())
        lbl_font.setPointSize(self._label_size)
        lbl_h = QFontMetrics(lbl_font).height() if show_labels else 0
        label_room = (lbl_h + self._baseline_gap) if show_labels else 0

        fm = QFontMetrics(lbl_font)
        # Left gutter for the optional y-scale (measured, not guessed).
        show_scale = bool(self._y_labels)
        gutter = (max(fm.horizontalAdvance(t) for _, t in self._y_labels) + 10) if show_scale else 0
        # Headroom for the optional callout bubble above the highlighted bar.
        callout = self._callout_text if (self._callout_text and 0 <= self._highlight_index < len(self._values)) else ""
        callout_room = (fm.height() + 12 + 6 + 4) if callout else 0  # pad + pointer + gap

        chart_top = float(callout_room)
        chart_h = max(1.0, h - label_room)
        maxv = max(self._values) or 1.0
        if show_scale:
            maxv = max([maxv] + [v for v, _ in self._y_labels]) or 1.0
        n = len(self._values)

        def bar_geo(i, val):
            col_w = (w - gutter) / n
            cx = gutter + col_w * (i + 0.5)
            bh = max(3.0, (val / maxv) * (chart_h - 4 - chart_top))
            return cx, chart_h - bh, bh, col_w

        if show_scale:
            p.setFont(lbl_font)
            p.setPen(self._y_label_color)
            for v, t in self._y_labels:
                yy = chart_h - (v / maxv) * (chart_h - 4 - chart_top)
                rect = QRectF(0, yy - fm.height() / 2.0, gutter - 8, fm.height())
                p.drawText(rect, Qt.AlignRight | Qt.AlignVCenter, t)

        p.setPen(Qt.NoPen)
        for i, val in enumerate(self._values):
            cx, y, bh, _ = bar_geo(i, val)
            x = cx - self._bar_width / 2.0
            p.setBrush(QBrush(self._bar_color_for(i, val)))
            p.drawPath(self._top_rounded_path(x, y, float(self._bar_width), bh, float(self._corner_radius)))

        if show_labels:
            p.setFont(lbl_font)
            p.setPen(self._label_color)
            ly = chart_h + self._baseline_gap
            for i in range(n):
                if i >= len(self._labels):
                    break
                cx, _, _, col_w = bar_geo(i, self._values[i])
                rect = QRectF(cx - col_w / 2.0, ly, col_w, lbl_h)
                p.drawText(rect, Qt.AlignHCenter | Qt.AlignVCenter, str(self._labels[i]))

        if callout:
            cx, bar_y, _, _ = bar_geo(self._highlight_index, self._values[self._highlight_index])
            bw = fm.horizontalAdvance(callout) + 20
            bh_c = fm.height() + 10
            bx = min(max(cx - bw / 2.0, 2.0), w - bw - 2.0)
            by = max(2.0, bar_y - bh_c - 8)
            bubble = QPainterPath()
            bubble.addRoundedRect(QRectF(bx, by, bw, bh_c), bh_c / 2.0, bh_c / 2.0)
            # small pointer under the bubble, centred on the bar
            bubble.moveTo(cx - 5, by + bh_c - 1)
            bubble.lineTo(cx, by + bh_c + 5)
            bubble.lineTo(cx + 5, by + bh_c - 1)
            bubble.closeSubpath()
            p.setPen(Qt.NoPen)
            p.setBrush(QBrush(self._callout_bg))
            p.drawPath(bubble)
            p.setPen(self._callout_text_color)
            p.setFont(lbl_font)
            p.drawText(QRectF(bx, by, bw, bh_c), Qt.AlignCenter, callout)
        p.end()

    # ------------------------------------------------------------------ #
    ## Designer properties
    # ------------------------------------------------------------------ #
    @Property(str)
    def valuesCsv(self):
        return ",".join("%g" % v for v in self._values)

    @valuesCsv.setter
    def valuesCsv(self, text):
        out = []
        for tok in str(text).replace(";", ",").split(","):
            tok = tok.strip()
            if tok:
                try:
                    out.append(float(tok))
                except ValueError:
                    pass
        self.setValues(out)

    @Property(str)
    def colorsCsv(self):
        return ",".join(c.name() for c in self._colors)

    @colorsCsv.setter
    def colorsCsv(self, text):
        cols = [t.strip() for t in str(text).replace(";", ",").split(",") if t.strip()]
        self.setBarColors(cols)

    @Property(str)
    def labelsCsv(self):
        return ",".join(str(x) for x in self._labels)

    @labelsCsv.setter
    def labelsCsv(self, text):
        self.setLabels([t.strip() for t in str(text).replace(";", ",").split(",") if t.strip()])

    @Property(QColor)
    def barColor(self):
        return self._bar_color

    @barColor.setter
    def barColor(self, c):
        self._bar_color = QColor(c)
        self.update()

    @Property(QColor)
    def idleColor(self):
        return self._idle_color

    @idleColor.setter
    def idleColor(self, c):
        self._idle_color = QColor(c)
        self.update()

    @Property(QColor)
    def highlightColor(self):
        return self._highlight_color

    @highlightColor.setter
    def highlightColor(self, c):
        self._highlight_color = QColor(c)
        self.update()

    @Property(int)
    def highlightIndexProp(self):
        return self._highlight_index

    @highlightIndexProp.setter
    def highlightIndexProp(self, i):
        self._highlight_index = int(i)
        self.update()

    @Property(int)
    def barWidth(self):
        return self._bar_width

    @barWidth.setter
    def barWidth(self, v):
        self._bar_width = max(1, int(v))
        self.update()

    @Property(int)
    def cornerRadius(self):
        return self._corner_radius

    @cornerRadius.setter
    def cornerRadius(self, v):
        self._corner_radius = max(0, int(v))
        self.update()

    @Property(bool)
    def showLabels(self):
        return self._show_labels

    @showLabels.setter
    def showLabels(self, v):
        self._show_labels = bool(v)
        self.update()

    @Property(QColor)
    def labelColor(self):
        return self._label_color

    @labelColor.setter
    def labelColor(self, c):
        self._label_color = QColor(c)
        self.update()

    @Property(str)
    def calloutText(self):
        return self._callout_text

    @calloutText.setter
    def calloutText(self, text):
        self._callout_text = str(text)
        self.update()

    @Property(QColor)
    def calloutBg(self):
        return self._callout_bg

    @calloutBg.setter
    def calloutBg(self, c):
        self._callout_bg = QColor(c)
        self.update()

    @Property(QColor)
    def calloutTextColor(self):
        return self._callout_text_color

    @calloutTextColor.setter
    def calloutTextColor(self, c):
        self._callout_text_color = QColor(c)
        self.update()

    @Property(str)
    def yLabelsCsv(self):
        return ",".join(t for _, t in self._y_labels)

    @yLabelsCsv.setter
    def yLabelsCsv(self, text):
        out = []
        for tok in str(text).replace(";", ",").split(","):
            tok = tok.strip()
            if tok:
                try:
                    out.append((float(tok), tok))
                except ValueError:
                    pass
        self._y_labels = out
        self.update()

    @Property(QColor)
    def yLabelColor(self):
        return self._y_label_color

    @yLabelColor.setter
    def yLabelColor(self, c):
        self._y_label_color = QColor(c)
        self.update()
