########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/spinnTv
# WEBSITE: spinncode.com
########################################################################

########################################################################
## QCustomHeatmap - a painted colour-intensity grid.
##
## Two modes (`mode`):
##   "grid" (default) - a rows x cols matrix (e.g. hours x weekdays, the
##       "Activity by time" heatmap): each cell's colour is its value mapped on a
##       low->high ramp, with row/col labels and an optional Less->More legend.
##   "calendar" - a GitHub-style contributions calendar: a flat list of daily
##       values wrapped into 7 rows (weekdays) x N columns (weeks).
##
## Values come in via setValues(list[list[float]]) / a flat list (calendar), or
## the `valuesCsv` Designer property (rows separated by ';', cells by ','). Cells
## auto-normalise across the data (min->max) unless you setRange(...). Painted
## with QPainter so it stays crisp at any size; the grid FLEX-fits the box left
## after labels + legend, so nothing clips when the widget grows or shrinks.
##
## Signals: cellClicked(row, col, value); a per-cell tooltip on hover.
########################################################################
import math

from qtpy.QtCore import Qt, Property, Signal, QRectF, QPointF
from qtpy.QtGui import QColor, QPainter, QPen, QBrush, QFont, QFontMetrics
from qtpy.QtWidgets import QWidget, QSizePolicy


class QCustomHeatmap(QWidget):

    cellClicked = Signal(int, int, float)

    WIDGET_ICON = "components/icons/heatmap.png"
    WIDGET_TOOLTIP = "A painted colour-intensity grid (activity / calendar heatmap)"
    WIDGET_MODULE = "Custom_Widgets.QCustomHeatmap"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomHeatmap' name='customHeatmap'>
            <property name='geometry'><rect><x>0</x><y>0</y><width>340</width><height>230</height></rect></property>
        </widget>
    </ui>
    """
    __catalog__ = {
        "name": "QCustomHeatmap",
        "props": {
            "mode": {"type": "enum", "values": ["grid", "calendar"], "default": "grid"},
            "valuesCsv": {"type": "string", "default": ""},
            "lowColor": {"type": "color", "default": "#1e1b3a"},
            "highColor": {"type": "color", "default": "#b3a4ff"},
            "emptyColor": {"type": "color", "default": "#17152b"},
            "rowLabelsCsv": {"type": "string", "default": ""},
            "colLabelsCsv": {"type": "string", "default": ""},
            "cellSize": {"type": "int", "default": 0},
            "cellGap": {"type": "int", "default": 4},
            "cornerRadius": {"type": "int", "default": 4},
            "showLabels": {"type": "bool", "default": True},
            "showLegend": {"type": "bool", "default": True},
            "labelColor": {"type": "color", "default": "#8b90a0"},
            "autoNormalize": {"type": "bool", "default": True},
            "minValue": {"type": "float", "default": 0.0},
            "maxValue": {"type": "float", "default": 1.0},
        },
        "signals": ["cellClicked"],
        "tokens_used": ["accent"],
    }

    def __init__(self, parent=None, values=None, mode="grid"):
        super().__init__(parent)
        self.setObjectName("QCustomHeatmap")
        self._mode = "calendar" if str(mode) == "calendar" else "grid"
        self._values = self._coerce(values) if values is not None else self._seed()
        self._low = QColor("#1e1b3a")
        self._high = QColor("#b3a4ff")
        self._empty = QColor("#17152b")
        self._row_labels = ["1pm", "2pm", "3pm", "4pm", "5pm", "6pm"]
        self._col_labels = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        self._cell_size = 0            # 0 -> auto flex-fit
        self._cell_gap = 4
        self._radius = 4
        self._show_labels = True
        self._show_legend = True
        self._label_color = QColor("#8b90a0")
        self._auto = True
        self._min = 0.0
        self._max = 1.0
        self._hover = (-1, -1)
        self._rects = {}               # (r,c) -> QRectF  (last layout, for hit-test)
        self.setMouseTracking(True)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMinimumSize(120, 90)

    # ------------------------------------------------------------------ #
    ## Data
    # ------------------------------------------------------------------ #
    @staticmethod
    def _seed():
        # a small activity-by-time grid so it previews in Designer / render_widget
        import itertools
        rng = [3, 8, 2, 6, 9, 1, 4, 7, 5, 2, 8, 6, 3, 9, 4, 1, 7, 5, 6, 2, 8]
        it = itertools.cycle(rng)
        return [[float(next(it)) for _ in range(7)] for _ in range(6)]

    @staticmethod
    def _coerce(values):
        """Accept list[list] or a flat list (wrapped later for calendar)."""
        if not values:
            return []
        if isinstance(values[0], (list, tuple)):
            return [[(None if v is None else float(v)) for v in row] for row in values]
        return [float(v) for v in values]     # flat -> arranged per mode

    def setValues(self, values):
        self._values = self._coerce(values)
        self.update()

    def setRange(self, minimum, maximum):
        self._auto = False
        self._min, self._max = float(minimum), float(maximum)
        self.update()

    def setColors(self, low, high, empty=None):
        self._low, self._high = QColor(low), QColor(high)
        if empty is not None:
            self._empty = QColor(empty)
        self.update()

    def setLabels(self, row_labels=None, col_labels=None):
        if row_labels is not None:
            self._row_labels = [str(s) for s in row_labels]
        if col_labels is not None:
            self._col_labels = [str(s) for s in col_labels]
        self.update()

    def setMode(self, mode):
        self._mode = "calendar" if str(mode) == "calendar" else "grid"
        self.update()

    def values(self):
        return self._values

    # ------------------------------------------------------------------ #
    ## Grid shape (mode-aware): returns (rows, cols, get(r,c)->value|None)
    # ------------------------------------------------------------------ #
    def _matrix(self):
        vals = self._values
        if not vals:
            return 0, 0, (lambda r, c: None)
        if self._mode == "calendar":
            flat = vals
            if flat and isinstance(flat[0], (list, tuple)):
                flat = [v for row in flat for v in row]
            weeks = max(1, math.ceil(len(flat) / 7.0))

            def get(r, c):
                i = c * 7 + r
                return flat[i] if 0 <= i < len(flat) else None
            return 7, weeks, get
        # grid
        rows = len(vals)
        cols = max((len(row) for row in vals), default=0)

        def get(r, c):
            row = vals[r]
            return row[c] if c < len(row) else None
        return rows, cols, get

    def _norm_range(self):
        if not self._auto:
            return self._min, self._max
        lo, hi = None, None
        for row in self._values:
            row = row if isinstance(row, (list, tuple)) else [row]
            for v in row:
                if v is None:
                    continue
                lo = v if lo is None else min(lo, v)
                hi = v if hi is None else max(hi, v)
        if lo is None:
            return 0.0, 1.0
        return lo, hi

    def _cell_color(self, v, lo, hi):
        if v is None:
            return QColor(self._empty)
        t = 0.5 if hi <= lo else (v - lo) / (hi - lo)
        t = max(0.0, min(1.0, t))
        return self._lerp(self._low, self._high, t)

    @staticmethod
    def _lerp(c0, c1, t):
        return QColor(
            int(c0.red() + (c1.red() - c0.red()) * t),
            int(c0.green() + (c1.green() - c0.green()) * t),
            int(c0.blue() + (c1.blue() - c0.blue()) * t),
        )

    # ------------------------------------------------------------------ #
    ## Flex layout — size the cells to the box left after labels + legend
    # ------------------------------------------------------------------ #
    def _label_font(self):
        """One label font used for BOTH measuring the gutters and painting the
        labels — a size mismatch here clips the row labels."""
        f = QFont(self.font())
        side = min(self.width(), self.height())
        f.setPointSizeF(max(7.5, min(11.0, side * 0.034)))
        return f

    def _layout(self, rows, cols):
        w, h = self.width(), self.height()
        m = 8.0
        fm = QFontMetrics(self._label_font())
        show_lab = self._show_labels
        # left gutter for row labels, top strip for column labels
        left = 0.0
        if show_lab and self._row_labels and self._mode == "grid":
            left = max((fm.horizontalAdvance(s) for s in self._row_labels), default=0) + 12.0
        top = 0.0
        if show_lab and self._col_labels and self._mode == "grid":
            top = fm.height() + 4.0
        legend_h = (fm.height() + 10.0) if self._show_legend else 0.0

        avail_w = max(1.0, w - 2 * m - left)
        avail_h = max(1.0, h - 2 * m - top - legend_h)
        gap = float(self._cell_gap)
        if self._cell_size > 0:
            cell = float(self._cell_size)
        else:
            cell = min((avail_w - (cols - 1) * gap) / max(cols, 1),
                       (avail_h - (rows - 1) * gap) / max(rows, 1))
        cell = max(cell, 2.0)
        grid_w = cols * cell + (cols - 1) * gap
        grid_h = rows * cell + (rows - 1) * gap
        x0 = m + left + max(0.0, (avail_w - grid_w) / 2.0)
        y0 = m + top + max(0.0, (avail_h - grid_h) / 2.0)
        return x0, y0, cell, gap, left, top, legend_h

    # ------------------------------------------------------------------ #
    ## Painting
    # ------------------------------------------------------------------ #
    def paintEvent(self, e):
        rows, cols, get = self._matrix()
        if rows == 0 or cols == 0:
            return
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, True)
        lo, hi = self._norm_range()
        x0, y0, cell, gap, left, top, legend_h = self._layout(rows, cols)
        self._rects = {}

        # labels (grid mode) — same font used to measure the gutters
        if self._show_labels and self._mode == "grid":
            p.setFont(self._label_font())
            p.setPen(QPen(self._label_color))
            if top:
                for c in range(cols):
                    if c < len(self._col_labels):
                        cx = x0 + c * (cell + gap)
                        p.drawText(QRectF(cx, y0 - top, cell, top - 2),
                                   Qt.AlignCenter, self._col_labels[c])
            if left:
                for r in range(rows):
                    if r < len(self._row_labels):
                        ry = y0 + r * (cell + gap)
                        p.drawText(QRectF(4, ry, left - 8, cell),
                                   Qt.AlignVCenter | Qt.AlignRight, self._row_labels[r])

        # cells
        for r in range(rows):
            for c in range(cols):
                v = get(r, c)
                rect = QRectF(x0 + c * (cell + gap), y0 + r * (cell + gap), cell, cell)
                self._rects[(r, c)] = rect
                p.setPen(Qt.NoPen)
                p.setBrush(QBrush(self._cell_color(v, lo, hi)))
                p.drawRoundedRect(rect, self._radius, self._radius)
                if (r, c) == self._hover and v is not None:
                    pen = QPen(QColor(255, 255, 255, 150), max(1.0, cell * 0.06))
                    p.setPen(pen)
                    p.setBrush(Qt.NoBrush)
                    p.drawRoundedRect(rect, self._radius, self._radius)

        if self._show_legend:
            self._paint_legend(p, x0, self.height() - 8.0 - (legend_h - 10.0),
                               x0 + cols * (cell + gap) - gap)
        p.end()

    def _paint_legend(self, p, x_left, y, x_right):
        fm = p.fontMetrics()
        f = QFont(self.font())
        f.setPointSizeF(max(7.0, self.font().pointSizeF()))
        p.setFont(f)
        sw = max(9.0, fm.height() - 2)          # swatch size
        gap = 3.0
        steps = 4
        block = steps * sw + (steps - 1) * gap
        more_w = fm.horizontalAdvance("More") + 3
        less_w = fm.horizontalAdvance("Less") + 3
        total = less_w + 6 + block + 6 + more_w
        x = max(x_left, x_right - total)
        p.setPen(QPen(self._label_color))
        p.drawText(QRectF(x, y - fm.height() / 2.0 + sw / 2.0, less_w, fm.height()),
                   Qt.AlignVCenter | Qt.AlignLeft, "Less")
        x += less_w + 6
        for i in range(steps):
            t = i / (steps - 1)
            p.setPen(Qt.NoPen)
            p.setBrush(QBrush(self._lerp(self._low, self._high, t)))
            p.drawRoundedRect(QRectF(x, y, sw, sw), 2, 2)
            x += sw + gap
        x += 6 - gap
        p.setPen(QPen(self._label_color))
        p.drawText(QRectF(x, y - fm.height() / 2.0 + sw / 2.0, more_w, fm.height()),
                   Qt.AlignVCenter | Qt.AlignLeft, "More")

    # ------------------------------------------------------------------ #
    ## Interaction
    # ------------------------------------------------------------------ #
    def _cell_at(self, pos):
        for (r, c), rect in self._rects.items():
            if rect.contains(pos):
                return r, c
        return -1, -1

    def mouseMoveEvent(self, e):
        pos = e.position() if hasattr(e, "position") else QPointF(e.pos())
        rc = self._cell_at(pos)
        if rc != self._hover:
            self._hover = rc
            r, c = rc
            if r >= 0:
                _, _, get = self._matrix()
                v = get(r, c)
                if v is not None:
                    rl = self._row_labels[r] if r < len(self._row_labels) else "%d" % r
                    cl = self._col_labels[c] if c < len(self._col_labels) else "%d" % c
                    self.setToolTip("%s · %s: %g" % (cl, rl, v))
                else:
                    self.setToolTip("")
            else:
                self.setToolTip("")
            self.update()
        super().mouseMoveEvent(e)

    def leaveEvent(self, e):
        if self._hover != (-1, -1):
            self._hover = (-1, -1)
            self.update()
        super().leaveEvent(e)

    def mousePressEvent(self, e):
        pos = e.position() if hasattr(e, "position") else QPointF(e.pos())
        r, c = self._cell_at(pos)
        if r >= 0:
            _, _, get = self._matrix()
            v = get(r, c)
            self.cellClicked.emit(r, c, float(v) if v is not None else float("nan"))
        super().mousePressEvent(e)

    # ------------------------------------------------------------------ #
    ## Designer properties
    # ------------------------------------------------------------------ #
    @Property(str)
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, m):
        self.setMode(m)

    @Property(str)
    def valuesCsv(self):
        rows = self._values if self._values and isinstance(self._values[0], (list, tuple)) \
            else [self._values]
        return ";".join(",".join("" if v is None else "%g" % v for v in row) for row in rows)

    @valuesCsv.setter
    def valuesCsv(self, text):
        out = []
        for rowtok in str(text).split(";"):
            rowtok = rowtok.strip()
            if not rowtok:
                continue
            row = []
            for tok in rowtok.split(","):
                tok = tok.strip()
                row.append(None if tok == "" else float(tok) if _isnum(tok) else None)
            out.append(row)
        if out:
            self.setValues(out)

    @Property(str)
    def rowLabelsCsv(self):
        return ",".join(self._row_labels)

    @rowLabelsCsv.setter
    def rowLabelsCsv(self, text):
        self.setLabels(row_labels=[s.strip() for s in str(text).split(",") if s.strip()])

    @Property(str)
    def colLabelsCsv(self):
        return ",".join(self._col_labels)

    @colLabelsCsv.setter
    def colLabelsCsv(self, text):
        self.setLabels(col_labels=[s.strip() for s in str(text).split(",") if s.strip()])

    @Property(QColor)
    def lowColor(self):
        return self._low

    @lowColor.setter
    def lowColor(self, c):
        self._low = QColor(c)
        self.update()

    @Property(QColor)
    def highColor(self):
        return self._high

    @highColor.setter
    def highColor(self, c):
        self._high = QColor(c)
        self.update()

    @Property(QColor)
    def emptyColor(self):
        return self._empty

    @emptyColor.setter
    def emptyColor(self, c):
        self._empty = QColor(c)
        self.update()

    @Property(int)
    def cellSize(self):
        return self._cell_size

    @cellSize.setter
    def cellSize(self, v):
        self._cell_size = max(0, int(v))
        self.update()

    @Property(int)
    def cellGap(self):
        return self._cell_gap

    @cellGap.setter
    def cellGap(self, v):
        self._cell_gap = max(0, int(v))
        self.update()

    @Property(int)
    def cornerRadius(self):
        return self._radius

    @cornerRadius.setter
    def cornerRadius(self, v):
        self._radius = max(0, int(v))
        self.update()

    @Property(bool)
    def showLabels(self):
        return self._show_labels

    @showLabels.setter
    def showLabels(self, v):
        self._show_labels = bool(v)
        self.update()

    @Property(bool)
    def showLegend(self):
        return self._show_legend

    @showLegend.setter
    def showLegend(self, v):
        self._show_legend = bool(v)
        self.update()

    @Property(QColor)
    def labelColor(self):
        return self._label_color

    @labelColor.setter
    def labelColor(self, c):
        self._label_color = QColor(c)
        self.update()

    @Property(bool)
    def autoNormalize(self):
        return self._auto

    @autoNormalize.setter
    def autoNormalize(self, v):
        self._auto = bool(v)
        self.update()

    @Property(float)
    def minValue(self):
        return self._min

    @minValue.setter
    def minValue(self, v):
        self._min = float(v)
        self._auto = False
        self.update()

    @Property(float)
    def maxValue(self):
        return self._max

    @maxValue.setter
    def maxValue(self, v):
        self._max = float(v)
        self._auto = False
        self.update()


def _isnum(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
