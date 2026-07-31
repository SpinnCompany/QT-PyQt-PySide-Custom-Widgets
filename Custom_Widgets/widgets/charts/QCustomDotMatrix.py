########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/spinnTv
# WEBSITE: spinncode.com
########################################################################

########################################################################
## QCustomDotMatrix - a density / category dot grid.
##
## A grid of small dots where each cell carries a STATE (0..N). State 0 is
## the "empty" slot (drawn faintly with `emptyColor`); states 1..N pick a
## colour from `colorsCsv`. Use it for the dot-matrix density panels seen on
## modern dashboards (e.g. a "product" activity grid: valid / invalid / idle
## dots that thicken toward one corner). Painted (no QtCharts) so it is crisp
## at any size and needs no legend/toolbar.
##
## Give the grid in code with setData([[0,1,2,...], ...]) (row-major 2-D list
## of state ints), or in Qt Designer with the `dataCsv` property (rows joined
## by ';', cells by ','). `rows`/`cols` size an empty grid. Colours are
## qproperties so a theme/manager can tokenise them and they flip on theme
## switch.
########################################################################
from qtpy.QtCore import Qt, Property, QRectF
from qtpy.QtGui import QColor, QPainter, QBrush
from qtpy.QtWidgets import QWidget, QSizePolicy


class QCustomDotMatrix(QWidget):

    WIDGET_ICON = "components/icons/bar_chart.png"
    WIDGET_TOOLTIP = "A density / category dot grid (valid / invalid / idle dots)"
    WIDGET_MODULE = "Custom_Widgets.QCustomDotMatrix"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomDotMatrix' name='customDotMatrix'>
            <property name='geometry'><rect><x>0</x><y>0</y><width>260</width><height>120</height></rect></property>
        </widget>
    </ui>
    """
    __catalog__ = {
        "name": "QCustomDotMatrix",
        "props": {"dataCsv": {"type": "string", "default": ""},
                  "rows": {"type": "int", "default": 6},
                  "cols": {"type": "int", "default": 14},
                  "colorsCsv": {"type": "string", "default": "#8fe36b,#ffffff,#f6912b"},
                  "emptyColor": {"type": "color", "default": "#2c2c30"},
                  "dotDiameter": {"type": "int", "default": 0},
                  "gapRatio": {"type": "float", "default": 0.55},
                  "emptyOpacity": {"type": "float", "default": 0.6},
                  "square": {"type": "bool", "default": False}},
        "signals": [],
        "tokens_used": ["accent"],
    }

    # a deterministic demo pattern (density thickens toward the bottom-right)
    _DEMO = [
        [0, 0, 0, 0, 0, 0, 1, 0, 2, 0, 1, 2, 1, 2],
        [0, 0, 0, 1, 0, 2, 1, 2, 1, 1, 2, 1, 2, 1],
        [0, 1, 0, 2, 1, 1, 2, 1, 2, 2, 1, 2, 1, 2],
        [1, 2, 1, 1, 2, 2, 1, 2, 1, 1, 2, 1, 2, 3],
        [2, 1, 2, 2, 1, 1, 2, 1, 3, 2, 1, 2, 3, 2],
        [1, 2, 1, 2, 3, 2, 1, 3, 2, 1, 3, 2, 1, 3],
    ]

    def __init__(self, parent=None, data=None):
        super().__init__(parent)
        self.setObjectName("QCustomDotMatrix")
        self._data = [list(r) for r in data] if data else []
        self._rows = 6
        self._cols = 14
        self._colors = [QColor("#8fe36b"), QColor("#ffffff"), QColor("#f6912b")]
        self._empty = QColor("#2c2c30")
        self._dot_d = 0            # 0 = auto-fit
        self._gap_ratio = 0.55     # gap as a fraction of the dot diameter
        self._empty_opacity = 0.6
        self._square = False
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMinimumSize(80, 48)
        if not self._data:
            self._data = [list(r) for r in self._DEMO]
            self._rows = len(self._DEMO)
            self._cols = len(self._DEMO[0])

    # ------------------------------------------------------------------ #
    ## Data API
    # ------------------------------------------------------------------ #
    def setData(self, data):
        """2-D row-major list of state ints (0 = empty, 1..N = colour index)."""
        self._data = [list(r) for r in (data or [])]
        if self._data:
            self._rows = len(self._data)
            self._cols = max(len(r) for r in self._data)
        self.update()

    def data(self):
        return [list(r) for r in self._data]

    def setColors(self, colors):
        self._colors = [QColor(c) for c in colors if c]
        self.update()

    def _grid(self):
        """Normalised rows×cols grid (pads short rows with 0)."""
        rows = self._data if self._data else [[0] * self._cols for _ in range(self._rows)]
        cols = max((len(r) for r in rows), default=self._cols)
        return [[(r[c] if c < len(r) else 0) for c in range(cols)] for r in rows], len(rows), cols

    # ------------------------------------------------------------------ #
    ## Painting
    # ------------------------------------------------------------------ #
    def paintEvent(self, e):
        grid, nrows, ncols = self._grid()
        if nrows == 0 or ncols == 0:
            return
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, True)
        w, h = self.width(), self.height()

        # cell pitch that fits both axes; dot = pitch / (1 + gapRatio)
        g = max(0.0, float(self._gap_ratio))
        pitch_x = w / ncols
        pitch_y = h / nrows
        pitch = min(pitch_x, pitch_y)
        d = self._dot_d if self._dot_d > 0 else pitch / (1.0 + g)
        d = max(2.0, d)
        gap = pitch - d

        grid_w = ncols * pitch
        grid_h = nrows * pitch
        ox = (w - grid_w) / 2.0
        oy = (h - grid_h) / 2.0

        p.setPen(Qt.NoPen)
        for r in range(nrows):
            for c in range(ncols):
                state = grid[r][c]
                if state <= 0:
                    col = QColor(self._empty)
                    col.setAlphaF(max(0.0, min(1.0, self._empty_opacity)))
                else:
                    idx = (state - 1) % len(self._colors) if self._colors else 0
                    col = QColor(self._colors[idx]) if self._colors else QColor("#ffffff")
                x = ox + c * pitch + gap / 2.0
                y = oy + r * pitch + gap / 2.0
                p.setBrush(QBrush(col))
                rect = QRectF(x, y, d, d)
                if self._square:
                    p.drawRoundedRect(rect, d * 0.28, d * 0.28)
                else:
                    p.drawEllipse(rect)
        p.end()

    # ------------------------------------------------------------------ #
    ## Designer properties
    # ------------------------------------------------------------------ #
    @Property(str)
    def dataCsv(self):
        return ";".join(",".join(str(int(v)) for v in row) for row in self._grid()[0])

    @dataCsv.setter
    def dataCsv(self, text):
        rows = []
        for line in str(text).replace("|", ";").split(";"):
            line = line.strip()
            if not line:
                continue
            row = []
            for tok in line.split(","):
                tok = tok.strip()
                if not tok:
                    continue
                try:
                    row.append(int(float(tok)))
                except ValueError:
                    row.append(0)
            rows.append(row)
        if rows:
            self.setData(rows)

    @Property(int)
    def rows(self):
        return self._rows

    @rows.setter
    def rows(self, v):
        self._rows = max(1, int(v))
        if not self._data or len(self._data) != self._rows:
            self.update()

    @Property(int)
    def cols(self):
        return self._cols

    @cols.setter
    def cols(self, v):
        self._cols = max(1, int(v))
        self.update()

    @Property(str)
    def colorsCsv(self):
        return ",".join(c.name() for c in self._colors)

    @colorsCsv.setter
    def colorsCsv(self, text):
        cols = [t.strip() for t in str(text).replace(";", ",").split(",") if t.strip()]
        if cols:
            self.setColors(cols)

    @Property(QColor)
    def emptyColor(self):
        return self._empty

    @emptyColor.setter
    def emptyColor(self, c):
        self._empty = QColor(c)
        self.update()

    @Property(int)
    def dotDiameter(self):
        return self._dot_d

    @dotDiameter.setter
    def dotDiameter(self, v):
        self._dot_d = max(0, int(v))
        self.update()

    @Property(float)
    def gapRatio(self):
        return self._gap_ratio

    @gapRatio.setter
    def gapRatio(self, v):
        self._gap_ratio = max(0.0, float(v))
        self.update()

    @Property(float)
    def emptyOpacity(self):
        return self._empty_opacity

    @emptyOpacity.setter
    def emptyOpacity(self, v):
        self._empty_opacity = max(0.0, min(1.0, float(v)))
        self.update()

    @Property(bool)
    def square(self):
        return self._square

    @square.setter
    def square(self, v):
        self._square = bool(v)
        self.update()
