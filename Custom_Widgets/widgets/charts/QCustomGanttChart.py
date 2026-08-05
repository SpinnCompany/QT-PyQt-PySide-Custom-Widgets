########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/@SpinnTV
# WEBSITE: customwidgets.org
########################################################################

########################################################################
## QCustomGanttChart - a horizontal timeline / gantt of rounded pill bars.
##
## Every ROW is one rounded "pill" bar placed on a shared numeric x-axis by
## its `start` and `length`; the row LABEL (e.g. a date) sits on the left,
## the row VALUE is printed at the right end of the bar, and an optional
## leading circular ICON (a QPixmap clipped to a circle) or coloured dot marks
## the bar's start. Bars are coloured by CATEGORY (`colorsCsv`). A light x-grid
## with tick labels runs underneath. This is the "projects timeline" viz.
## Painted (no QtCharts) so it is crisp and self-contained.
##
## Give rows in code with setData([...]) — each row a dict
## {"label","start","length","category","value","icon"} (icon = a path or
## QPixmap, optional) — or in Qt Designer with `dataCsv` (rows by ';', fields
## "label,start,length,category,value"). `xMax`/`gridStep` set the axis;
## colours are qproperties so a theme flips them on switch.
########################################################################
import os
from qtpy.QtCore import Qt, Property, QRectF, QPointF
from qtpy.QtGui import (QColor, QPainter, QBrush, QPen, QFont, QFontMetrics,
                        QPixmap, QPainterPath)
from qtpy.QtWidgets import QWidget, QSizePolicy


class QCustomGanttChart(QWidget):

    WIDGET_ICON = "components/icons/bar_chart.png"
    WIDGET_TOOLTIP = "A horizontal timeline / gantt of rounded pill bars"
    WIDGET_MODULE = "Custom_Widgets.QCustomGanttChart"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomGanttChart' name='customGanttChart'>
            <property name='geometry'><rect><x>0</x><y>0</y><width>560</width><height>360</height></rect></property>
        </widget>
    </ui>
    """
    __catalog__ = {
        "name": "QCustomGanttChart",
        "props": {"dataCsv": {"type": "string", "default": ""},
                  "colorsCsv": {"type": "string", "default": "#8fe36b,#f6912b,#ffffff"},
                  "textColorsCsv": {"type": "string", "default": "#1c1c20,#1c1c20,#1c1c20"},
                  "xMax": {"type": "float", "default": 30.0},
                  "gridStep": {"type": "float", "default": 5.0},
                  "barHeight": {"type": "int", "default": 30},
                  "labelColor": {"type": "color", "default": "#c7c9cf"},
                  "axisTextColor": {"type": "color", "default": "#7d7f88"},
                  "gridColor": {"type": "color", "default": "#2f2f35"},
                  "showGrid": {"type": "bool", "default": True},
                  "showMarkers": {"type": "bool", "default": True}},
        "signals": [],
        "tokens_used": ["accent"],
    }

    # deterministic demo rows (label, start, length, category, value)
    _DEMO = [
        {"label": "30.09", "start": 2,  "length": 8,  "category": 0, "value": 16},
        {"label": "29.09", "start": 18, "length": 8,  "category": 1, "value": 29},
        {"label": "28.09", "start": 8,  "length": 6,  "category": 2, "value": 15},
        {"label": "27.09", "start": 9,  "length": 9,  "category": 0, "value": 21},
        {"label": "26.09", "start": 6,  "length": 4,  "category": 2, "value": 10},
        {"label": "25.09", "start": 8,  "length": 5,  "category": 1, "value": 15},
        {"label": "25.09", "start": 12, "length": 9,  "category": 0, "value": 19},
        {"label": "24.09", "start": 6,  "length": 4,  "category": 2, "value": 8},
    ]

    def __init__(self, parent=None, rows=None):
        super().__init__(parent)
        self.setObjectName("QCustomGanttChart")
        self._rows = [dict(r) for r in rows] if rows else []
        self._colors = [QColor("#8fe36b"), QColor("#f6912b"), QColor("#ffffff")]
        self._text_colors = [QColor("#1c1c20"), QColor("#1c1c20"), QColor("#1c1c20")]
        self._x_max = 30.0
        self._grid_step = 5.0
        self._bar_h = 30
        self._label_color = QColor("#c7c9cf")
        self._axis_text_color = QColor("#7d7f88")
        self._grid_color = QColor("#2f2f35")
        self._show_grid = True
        self._show_markers = True
        self._label_w = 46          # left gutter for row labels
        self._pix_cache = {}
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMinimumSize(200, 160)
        if not self._rows:
            self._rows = [dict(r) for r in self._DEMO]

    # ------------------------------------------------------------------ #
    ## Data API
    # ------------------------------------------------------------------ #
    def setData(self, rows):
        self._rows = [dict(r) for r in (rows or [])]
        self._pix_cache.clear()
        self.update()

    def data(self):
        return [dict(r) for r in self._rows]

    def setColors(self, fills, texts=None):
        self._colors = [QColor(c) for c in fills if c]
        if texts:
            self._text_colors = [QColor(c) for c in texts if c]
        self.update()

    def _fill(self, cat):
        return QColor(self._colors[int(cat) % len(self._colors)]) if self._colors else QColor("#ffffff")

    def _text(self, cat):
        if self._text_colors:
            return QColor(self._text_colors[int(cat) % len(self._text_colors)])
        return QColor("#1c1c20")

    def _pixmap(self, icon):
        if icon is None or icon == "":
            return None
        if isinstance(icon, QPixmap):
            return icon if not icon.isNull() else None
        key = str(icon)
        if key in self._pix_cache:
            return self._pix_cache[key]
        pm = QPixmap(key) if os.path.exists(key) else QPixmap()
        pm = pm if not pm.isNull() else None
        self._pix_cache[key] = pm
        return pm

    # ------------------------------------------------------------------ #
    ## Painting
    # ------------------------------------------------------------------ #
    def paintEvent(self, e):
        if not self._rows:
            return
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, True)
        p.setRenderHint(QPainter.SmoothPixmapTransform, True)
        w, h = self.width(), self.height()
        n = len(self._rows)

        axis_font = QFont(self.font()); axis_font.setPointSize(9)
        afm = QFontMetrics(axis_font)
        x_room = afm.height() + 8              # bottom band for x tick labels

        left = float(self._label_w)
        plot_x0 = left
        plot_w = max(1.0, w - left - 6)
        plot_h = max(1.0, h - x_room)
        xmax = self._x_max if self._x_max > 0 else 1.0

        def x_of(v):
            return plot_x0 + (float(v) / xmax) * plot_w

        # --- x grid + tick labels ---------------------------------------- #
        if self._show_grid and self._grid_step > 0:
            p.setFont(axis_font)
            t = 0.0
            while t <= xmax + 1e-9:
                gx = x_of(t)
                p.setPen(QPen(self._grid_color, 1, Qt.DashLine))
                p.drawLine(int(gx), 0, int(gx), int(plot_h))
                p.setPen(self._axis_text_color)
                p.drawText(QRectF(gx - 16, plot_h + 4, 32, x_room - 4),
                           Qt.AlignHCenter | Qt.AlignVCenter, ("%g" % t))
                t += self._grid_step

        row_pitch = plot_h / n
        bh = float(min(self._bar_h, row_pitch * 0.8))
        lbl_font = QFont(self.font()); lbl_font.setPointSize(10)
        val_font = QFont(self.font()); val_font.setPointSize(9); val_font.setBold(True)

        for i, row in enumerate(self._rows):
            cy = row_pitch * (i + 0.5)
            start = float(row.get("start", 0))
            length = float(row.get("length", 0))
            cat = row.get("category", 0)
            value = row.get("value", "")
            x0 = x_of(start)
            x1 = x_of(start + length)
            bar_w = max(bh, x1 - x0)          # never thinner than a circle
            rect = QRectF(x0, cy - bh / 2.0, bar_w, bh)
            r = bh / 2.0

            # bar
            p.setPen(Qt.NoPen)
            p.setBrush(QBrush(self._fill(cat)))
            p.drawRoundedRect(rect, r, r)

            # row label (left gutter)
            p.setFont(lbl_font)
            p.setPen(self._label_color)
            p.drawText(QRectF(0, cy - bh / 2.0, left - 8, bh),
                       Qt.AlignRight | Qt.AlignVCenter, str(row.get("label", "")))

            # leading circular marker / icon
            if self._show_markers:
                d = bh - 6
                mrect = QRectF(x0 + 3, cy - d / 2.0, d, d)
                pm = self._pixmap(row.get("icon"))
                if pm is not None:
                    pr = pm.devicePixelRatio() or 1.0
                    aspect = (pm.width() / pr) / max(1.0, (pm.height() / pr))
                    if aspect > 1.3:
                        # a WIDE marker (e.g. an avatar group) — draw it as-is,
                        # left-aligned at bar height, NO circular clip.
                        wrect = QRectF(x0 + 3, cy - d / 2.0, d * aspect, d)
                        p.drawPixmap(wrect, pm, QRectF(0, 0, pm.width(), pm.height()))
                    else:
                        p.save()
                        clip = QPainterPath()
                        clip.addEllipse(mrect)
                        p.setClipPath(clip)
                        scaled = pm.scaled(int(d), int(d), Qt.KeepAspectRatioByExpanding,
                                           Qt.SmoothTransformation)
                        p.drawPixmap(mrect.topLeft(), scaled)
                        p.restore()
                        p.setBrush(Qt.NoBrush)
                        p.setPen(QPen(QColor(0, 0, 0, 40), 1))
                        p.drawEllipse(mrect)
                else:
                    p.setPen(Qt.NoPen)
                    p.setBrush(QBrush(QColor("#ffffff")))
                    p.drawEllipse(mrect)
                    dot = mrect.adjusted(d * 0.28, d * 0.28, -d * 0.28, -d * 0.28)
                    p.setBrush(QBrush(self._text(cat)))
                    p.drawEllipse(dot)

            # trailing value
            if value != "" and value is not None:
                p.setFont(val_font)
                p.setPen(self._text(cat))
                vw = 30.0
                p.drawText(QRectF(rect.right() - vw - 8, cy - bh / 2.0, vw, bh),
                           Qt.AlignRight | Qt.AlignVCenter, str(value))
        p.end()

    # ------------------------------------------------------------------ #
    ## Designer properties
    # ------------------------------------------------------------------ #
    @Property(str)
    def dataCsv(self):
        return ";".join(
            "%s,%g,%g,%d,%s" % (r.get("label", ""), float(r.get("start", 0)),
                                float(r.get("length", 0)), int(r.get("category", 0)),
                                str(r.get("value", "")))
            for r in self._rows)

    @dataCsv.setter
    def dataCsv(self, text):
        rows = []
        for chunk in str(text).replace("|", ";").split(";"):
            chunk = chunk.strip()
            if not chunk:
                continue
            f = [t.strip() for t in chunk.split(",")]
            f += [""] * (5 - len(f))
            try:
                rows.append({"label": f[0], "start": float(f[1] or 0),
                             "length": float(f[2] or 0), "category": int(float(f[3] or 0)),
                             "value": f[4]})
            except ValueError:
                pass
        if rows:
            self.setData(rows)

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

    @Property(float)
    def xMax(self):
        return self._x_max

    @xMax.setter
    def xMax(self, v):
        self._x_max = max(1.0, float(v))
        self.update()

    @Property(float)
    def gridStep(self):
        return self._grid_step

    @gridStep.setter
    def gridStep(self, v):
        self._grid_step = max(0.0, float(v))
        self.update()

    @Property(int)
    def barHeight(self):
        return self._bar_h

    @barHeight.setter
    def barHeight(self, v):
        self._bar_h = max(6, int(v))
        self.update()

    @Property(QColor)
    def labelColor(self):
        return self._label_color

    @labelColor.setter
    def labelColor(self, c):
        self._label_color = QColor(c)
        self.update()

    @Property(QColor)
    def axisTextColor(self):
        return self._axis_text_color

    @axisTextColor.setter
    def axisTextColor(self, c):
        self._axis_text_color = QColor(c)
        self.update()

    @Property(QColor)
    def gridColor(self):
        return self._grid_color

    @gridColor.setter
    def gridColor(self, c):
        self._grid_color = QColor(c)
        self.update()

    @Property(bool)
    def showGrid(self):
        return self._show_grid

    @showGrid.setter
    def showGrid(self, v):
        self._show_grid = bool(v)
        self.update()

    @Property(bool)
    def showMarkers(self):
        return self._show_markers

    @showMarkers.setter
    def showMarkers(self, v):
        self._show_markers = bool(v)
        self.update()
