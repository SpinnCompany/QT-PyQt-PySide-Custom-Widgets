########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/@SpinnTV
# WEBSITE: customwidgets.org
########################################################################

########################################################################
## QCustomDivergingBarChart - a diverging (bipolar / up-down) bar chart.
##
## Each category is ONE column split across a zero axis: an UPWARD segment
## (e.g. income, `upColor`) and a DOWNWARD segment (e.g. expense/expenditure,
## `downColor`), so a single slot carries two colours and two signs. A
## configurable `zeroGap` leaves clear space between the + and - bars around
## the zero line (as in cash-flow dashboards). Painted (no QtCharts) so it is
## crisp at any size and needs no toolbar/legend.
##
## This is the diverging sibling of QCustomMiniBarChart. Give data via
## setData(up, down, labels) in code, or the upCsv / downCsv / labelsCsv
## properties in Qt Designer. Optional y-axis (gridlines + prefixed/suffixed
## value labels, e.g. "EUR 5K") and x labels underneath.
########################################################################
from qtpy.QtCore import Qt, Property, QRectF
from qtpy.QtGui import QColor, QPainter, QBrush, QPen, QPainterPath, QFont, QFontMetrics
from qtpy.QtWidgets import QWidget, QSizePolicy


class QCustomDivergingBarChart(QWidget):

    WIDGET_ICON = "components/icons/bar_chart.png"
    WIDGET_TOOLTIP = "A diverging (up/down) bar chart: income up, expense down, split across a zero axis"
    WIDGET_MODULE = "Custom_Widgets.QCustomDivergingBarChart"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomDivergingBarChart' name='customDivergingBarChart'>
            <property name='geometry'><rect><x>0</x><y>0</y><width>420</width><height>220</height></rect></property>
        </widget>
    </ui>
    """
    __catalog__ = {
        "name": "QCustomDivergingBarChart",
        "props": {"upCsv": {"type": "string", "default": "1.2,3.1,2.4,0.9,1.1,4.2,3.0,2.0"},
                  "downCsv": {"type": "string", "default": "0.9,1.4,2.6,0.7,0.9,1.7,1.2,1.3"},
                  "labelsCsv": {"type": "string", "default": ""},
                  "upColor": {"type": "color", "default": "#123f39"},
                  "downColor": {"type": "color", "default": "#34d17a"},
                  "barWidth": {"type": "int", "default": 12},
                  "cornerRadius": {"type": "int", "default": 3},
                  "zeroGap": {"type": "int", "default": 8},
                  "showAxis": {"type": "bool", "default": True},
                  "showLabels": {"type": "bool", "default": True},
                  "axisPrefix": {"type": "string", "default": ""},
                  "axisSuffix": {"type": "string", "default": ""},
                  "gridColor": {"type": "color", "default": "#e6e9ec"},
                  "axisTextColor": {"type": "color", "default": "#8b93a1"}},
        "signals": [],
        "tokens_used": ["accent"],
    }

    def __init__(self, parent=None, up=None, down=None, labels=None):
        super().__init__(parent)
        self.setObjectName("QCustomDivergingBarChart")
        self._up = [float(v) for v in (up or [])]
        self._down = [abs(float(v)) for v in (down or [])]     # stored as magnitudes
        self._labels = list(labels) if labels else []
        self._up_color = QColor("#123f39")
        self._down_color = QColor("#34d17a")
        self._bar_width = 12
        self._corner_radius = 3
        self._zero_gap = 8                 # px of clear space between + and - bars
        self._show_axis = True
        self._show_labels = True
        self._axis_prefix = ""
        self._axis_suffix = ""
        self._grid_color = QColor("#e6e9ec")
        self._axis_text_color = QColor("#8b93a1")
        self._label_color = QColor("#8b93a1")
        self._label_size = 11
        self._axis_size = 10
        self._tick_step = 0.0              # 0 = auto
        self._baseline_gap = 10            # gap between chart and x labels
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMinimumSize(120, 100)
        # seed demo data so the widget previews in Designer / render_widget
        # (replaced the moment setData()/upCsv is called).
        if not self._up and not self._down:
            self._up = [1.2, 3.1, 2.4, 0.9, 1.1, 1.3, 4.2, 4.8, 3.0, 1.6, 2.1, 3.4]
            self._down = [0.9, 1.4, 2.6, 0.7, 0.9, 1.1, 1.7, 2.0, 1.2, 1.0, 1.9, 1.5]

    # ------------------------------------------------------------------ #
    ## Data API
    # ------------------------------------------------------------------ #
    def setData(self, up, down, labels=None):
        """Set both series at once. `up` = upward (income) values, `down` =
        downward (expense) values — either sign is accepted for `down`, its
        magnitude is used."""
        self._up = [float(v) for v in (up or [])]
        self._down = [abs(float(v)) for v in (down or [])]
        if labels is not None:
            self._labels = list(labels)
        self.update()

    def setUpValues(self, values):
        self._up = [float(v) for v in (values or [])]
        self.update()

    def setDownValues(self, values):
        self._down = [abs(float(v)) for v in (values or [])]
        self.update()

    def setLabels(self, labels):
        self._labels = list(labels or [])
        self.update()

    def setColors(self, up_color, down_color):
        self._up_color = QColor(up_color)
        self._down_color = QColor(down_color)
        self.update()

    def setTickStep(self, step):
        """Axis gridline/label step in data units (0 = auto)."""
        self._tick_step = max(0.0, float(step))
        self.update()

    def upValues(self):
        return list(self._up)

    def downValues(self):
        return list(self._down)

    # ------------------------------------------------------------------ #
    ## Painting
    # ------------------------------------------------------------------ #
    @staticmethod
    def _rounded_path(x, y, w, h, r, top=True):
        """Rounded on the top edge (top=True) or the bottom edge (top=False)."""
        r = max(0.0, min(r, w / 2.0, h))
        p = QPainterPath()
        if top:
            p.moveTo(x, y + h)
            p.lineTo(x, y + r)
            p.quadTo(x, y, x + r, y)
            p.lineTo(x + w - r, y)
            p.quadTo(x + w, y, x + w, y + r)
            p.lineTo(x + w, y + h)
        else:
            p.moveTo(x, y)
            p.lineTo(x, y + h - r)
            p.quadTo(x, y + h, x + r, y + h)
            p.lineTo(x + w - r, y + h)
            p.quadTo(x + w, y + h, x + w, y + h - r)
            p.lineTo(x + w, y)
        p.closeSubpath()
        return p

    def _nice_step(self, span):
        if self._tick_step > 0:
            return self._tick_step
        if span <= 0:
            return 1.0
        raw = span / 4.0
        import math
        mag = 10 ** math.floor(math.log10(raw))
        for m in (1, 2, 2.5, 5, 10):
            if raw <= m * mag:
                return m * mag
        return 10 * mag

    def _fmt(self, v):
        txt = ("%g" % round(v, 3))
        return "%s%s%s" % (self._axis_prefix, txt, self._axis_suffix)

    def paintEvent(self, e):
        if not self._up and not self._down:
            return
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, True)

        w, h = self.width(), self.height()
        n = max(len(self._up), len(self._down))
        if n == 0:
            p.end(); return

        max_up = max(self._up) if self._up else 0.0
        max_dn = max(self._down) if self._down else 0.0
        if max_up <= 0 and max_dn <= 0:
            p.end(); return

        # x-label room at the bottom
        show_x = bool(self._show_labels and self._labels)
        lbl_font = QFont(self.font()); lbl_font.setPointSize(self._label_size)
        lbl_h = QFontMetrics(lbl_font).height() if show_x else 0
        x_room = (lbl_h + self._baseline_gap) if show_x else 0

        # y-axis room on the left (widest tick label)
        axis_font = QFont(self.font()); axis_font.setPointSize(self._axis_size)
        afm = QFontMetrics(axis_font)
        left_pad = 0
        step = self._nice_step(max_up + max_dn)
        if self._show_axis:
            widest = max(afm.horizontalAdvance(self._fmt(max_up)),
                         afm.horizontalAdvance(self._fmt(-max_dn)),
                         afm.horizontalAdvance(self._fmt(0)))
            left_pad = widest + 10

        chart_x0 = left_pad
        chart_w = max(1.0, w - left_pad)
        chart_h = max(1.0, h - x_room)

        total = (max_up + max_dn) or 1.0
        gap = float(self._zero_gap)
        usable = max(1.0, chart_h - gap)
        up_region = usable * (max_up / total)
        dn_region = usable * (max_dn / total)
        zero_y = up_region + gap / 2.0            # y of the zero axis (from top)
        up_base = zero_y - gap / 2.0              # up bars grow from here, upward
        dn_base = zero_y + gap / 2.0              # down bars grow from here, downward

        # --- axis: gridlines + value labels ------------------------------- #
        if self._show_axis:
            p.setFont(axis_font)
            def y_of(val):
                if val >= 0:
                    return up_base - (val / max_up) * up_region if max_up > 0 else up_base
                return dn_base + (abs(val) / max_dn) * dn_region if max_dn > 0 else dn_base
            # collect tick values from -max_dn..max_up on `step`, plus zero
            ticks = set([0.0])
            v = step
            while v <= max_up + 1e-9:
                ticks.add(v); v += step
            v = -step
            while v >= -max_dn - 1e-9:
                ticks.add(v); v -= step
            for tv in sorted(ticks):
                gy = y_of(tv)
                pen = QPen(QColor(self._grid_color), 1)
                p.setPen(pen)
                p.drawLine(int(chart_x0), int(gy), int(w), int(gy))
                p.setPen(self._axis_text_color)
                rect = QRectF(0, gy - afm.height() / 2.0, left_pad - 8, afm.height())
                p.drawText(rect, Qt.AlignRight | Qt.AlignVCenter, self._fmt(tv))

        # --- bars ---------------------------------------------------------- #
        p.setPen(Qt.NoPen)
        col_w = chart_w / n
        bw = float(min(self._bar_width, col_w * 0.7))
        r = float(self._corner_radius)
        for i in range(n):
            cx = chart_x0 + col_w * (i + 0.5)
            x = cx - bw / 2.0
            if i < len(self._up) and self._up[i] > 0 and max_up > 0:
                uh = max(2.0, (self._up[i] / max_up) * up_region)
                p.setBrush(QBrush(self._up_color))
                p.drawPath(self._rounded_path(x, up_base - uh, bw, uh, r, top=True))
            if i < len(self._down) and self._down[i] > 0 and max_dn > 0:
                dh = max(2.0, (self._down[i] / max_dn) * dn_region)
                p.setBrush(QBrush(self._down_color))
                p.drawPath(self._rounded_path(x, dn_base, bw, dh, r, top=False))

        # --- x labels ------------------------------------------------------ #
        if show_x:
            p.setFont(lbl_font)
            p.setPen(self._label_color)
            ly = chart_h + self._baseline_gap
            for i in range(n):
                if i >= len(self._labels):
                    break
                if not str(self._labels[i]):
                    continue
                cx = chart_x0 + col_w * (i + 0.5)
                rect = QRectF(cx - col_w / 2.0, ly, col_w, lbl_h)
                p.drawText(rect, Qt.AlignHCenter | Qt.AlignVCenter, str(self._labels[i]))
        p.end()

    # ------------------------------------------------------------------ #
    ## Designer properties
    # ------------------------------------------------------------------ #
    @staticmethod
    def _parse_floats(text):
        out = []
        for tok in str(text).replace(";", ",").split(","):
            tok = tok.strip()
            if tok:
                try:
                    out.append(float(tok))
                except ValueError:
                    pass
        return out

    @Property(str)
    def upCsv(self):
        return ",".join("%g" % v for v in self._up)

    @upCsv.setter
    def upCsv(self, text):
        self.setUpValues(self._parse_floats(text))

    @Property(str)
    def downCsv(self):
        return ",".join("%g" % v for v in self._down)

    @downCsv.setter
    def downCsv(self, text):
        self.setDownValues(self._parse_floats(text))

    @Property(str)
    def labelsCsv(self):
        return ",".join(str(x) for x in self._labels)

    @labelsCsv.setter
    def labelsCsv(self, text):
        self.setLabels([t.strip() for t in str(text).replace(";", ",").split(",") if t.strip()])

    @Property(QColor)
    def upColor(self):
        return self._up_color

    @upColor.setter
    def upColor(self, c):
        self._up_color = QColor(c)
        self.update()

    @Property(QColor)
    def downColor(self):
        return self._down_color

    @downColor.setter
    def downColor(self, c):
        self._down_color = QColor(c)
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

    @Property(int)
    def zeroGap(self):
        return self._zero_gap

    @zeroGap.setter
    def zeroGap(self, v):
        self._zero_gap = max(0, int(v))
        self.update()

    @Property(bool)
    def showAxis(self):
        return self._show_axis

    @showAxis.setter
    def showAxis(self, v):
        self._show_axis = bool(v)
        self.update()

    @Property(bool)
    def showLabels(self):
        return self._show_labels

    @showLabels.setter
    def showLabels(self, v):
        self._show_labels = bool(v)
        self.update()

    @Property(str)
    def axisPrefix(self):
        return self._axis_prefix

    @axisPrefix.setter
    def axisPrefix(self, t):
        self._axis_prefix = str(t)
        self.update()

    @Property(str)
    def axisSuffix(self):
        return self._axis_suffix

    @axisSuffix.setter
    def axisSuffix(self, t):
        self._axis_suffix = str(t)
        self.update()

    @Property(QColor)
    def gridColor(self):
        return self._grid_color

    @gridColor.setter
    def gridColor(self, c):
        self._grid_color = QColor(c)
        self.update()

    @Property(QColor)
    def axisTextColor(self):
        return self._axis_text_color

    @axisTextColor.setter
    def axisTextColor(self, c):
        self._axis_text_color = QColor(c)
        self._label_color = QColor(c)
        self.update()
