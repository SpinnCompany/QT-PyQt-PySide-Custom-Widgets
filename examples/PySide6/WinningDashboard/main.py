"""WINNING — E-commerce Analytics Dashboard
============================================

A dense, chart-heavy showcase for the QT-PyQt-PySide Custom Widgets library,
rebuilt pixel-for-intent from a modern Dribbble dashboard reference. It stages
a fictional fashion store's command center: KPI cards with live sparklines,
a grouped online/offline sales bar chart, a sales-distribution donut, a recent
orders feed and a customers area/line chart — with a live Light / Dark toggle.

Custom widgets used: QCustomBarChart (online/offline sales), QCustomAreaChart
(customers), QCustomBadge (order status + nav count) and QCustomSegmentedControl
(theme switch) — plus recolored feather icons, a painted donut and sparklines,
and a token-derived chrome (applyDesignTokens) that flips with the theme.

Run:
    python main.py                 # interactive
    python main.py --shots DIR     # render dark+light PNGs to DIR, keep open
"""

import os
import sys
import math
import argparse

from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtCore import Qt, QMargins, QByteArray
from PySide6.QtGui import QColor, QPainter, QPixmap, QBrush
from PySide6.QtSvg import QSvgRenderer

from Custom_Widgets.JSonStyles.tokens import applyDesignTokens, DesignTokens
from Custom_Widgets.QCustomBadge import QCustomBadge
from Custom_Widgets.QCustomSegmentedControl import QCustomSegmentedControl
from Custom_Widgets.QCustomCharts.QCustomBarChart import QCustomBarChart
from Custom_Widgets.QCustomCharts.QCustomAreaChart import QCustomAreaChart

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
ICON_DIR = os.path.join(REPO, "Custom_Widgets", "Qss", "icons", "feather")


# --------------------------------------------------------------------------- #
# Palette — a neutral near-black + violet scheme to match the reference,
# rather than the token blue-slate. Both themes share the accent hues.
# --------------------------------------------------------------------------- #
PALETTES = {
    "dark": {
        "bg": "#0d0e12", "panel": "#15171d", "card": "#1b1e26", "card2": "#232733",
        "text": "#e9ebf1", "muted": "#8b909e", "faint": "#5b6070",
        "line": "rgba(255,255,255,0.06)", "hover": "rgba(255,255,255,0.05)",
        "violet": "#7b6cf6", "violet_soft": "rgba(123,108,246,0.16)",
        "orange": "#f2794b", "yellow": "#f4c44e", "green": "#3ddc97", "red": "#f5678a",
        "active_card": "#ffffff", "active_text": "#12141a", "active_sub": "#6b7080",
        "nav_active": "#232733", "nav_text": "#c2c6d2", "nav_icon": "#8b909e",
        "chart_grid": "rgba(255,255,255,0.05)", "chart_axis": "#767c8b",
    },
    "light": {
        "bg": "#eceff5", "panel": "#ffffff", "card": "#f6f8fc", "card2": "#eceff5",
        "text": "#161a24", "muted": "#6c7280", "faint": "#a2a8b4",
        "line": "rgba(16,20,35,0.08)", "hover": "rgba(16,20,35,0.04)",
        "violet": "#6c5ce7", "violet_soft": "rgba(108,92,231,0.12)",
        "orange": "#f2794b", "yellow": "#e6a51c", "green": "#17b26a", "red": "#e14d6e",
        "active_card": "#6c5ce7", "active_text": "#ffffff", "active_sub": "rgba(255,255,255,0.75)",
        "nav_active": "#eceff5", "nav_text": "#3b4150", "nav_icon": "#6c7280",
        "chart_grid": "rgba(16,20,35,0.06)", "chart_axis": "#98a1af",
    },
}


# --------------------------------------------------------------------------- #
# Fictional data model
# --------------------------------------------------------------------------- #
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul",
          "Aug", "Sep", "Oct", "Nov", "Dec"]
ONLINE = [22, 19, 26, 23, 21, 25, 23, 17, 19, 19, 24, 26]     # in $k
OFFLINE = [6.2, 4.6, 6.8, 5.8, 8.9, 5.6, 4.9, 4.2, 5.8, 6.4, 6.8, 2.2]

DISTRIBUTION = [("Online sales", 52, "violet"),
                ("Offline sales", 33, "orange"),
                ("Returns", 15, "yellow")]

LOYAL = [1.1, 1.9, 1.5, 2.3, 1.8, 2.0, 1.9, 2.2, 2.0, 2.4, 2.3, 2.9]
NEWC = [0.9, 1.4, 2.1, 1.6, 1.5, 1.9, 1.5, 1.7, 1.6, 2.0, 1.7, 2.5]

ORDERS = [
    ("RL", "Rust Linen Blazer", "Jan 25, 2025", "$149.99", "Shipping", "warning"),
    ("CT", "Crop Tank", "Jan 25, 2025", "$49.99", "Received", "success"),
    ("OB", "Oversized Blazer", "Jan 24, 2025", "$185.99", "Received", "success"),
    ("SD", "Silk Slip Dress", "Jan 24, 2025", "$129.00", "Shipping", "warning"),
    ("WT", "Wide-Leg Trouser", "Jan 23, 2025", "$89.50", "Received", "success"),
]
AVATAR_COLORS = ["#f2794b", "#7b6cf6", "#f4c44e", "#3ddc97", "#f5678a"]

SPARK_KPI = [
    ("Total orders", "947", "+5%", "up", ONLINE, "violet", True),
    ("Total sales", "$28,407", "+3%", "up", [12, 15, 13, 18, 16, 22, 20, 24], "orange", False),
    ("Online sessions", "54,778", "+2%", "up", [30, 28, 33, 31, 36, 34, 40, 44], "yellow", False),
    ("Average order", "$89.99", "-1%", "down", [22, 20, 24, 19, 23, 18, 21, 17], "red", False),
]

NAV = [
    ("GENERAL", [("grid", "Dashboard", None), ("package", "Products", None),
                 ("shopping-cart", "Orders", "5"), ("users", "Customers", None)]),
    ("OTHER", [("award", "Marketing", None), ("folder", "Documents", None),
               ("mail", "Emails", None), ("credit-card", "Billing", None),
               ("zap", "Integrations", None), ("bar-chart-2", "Analytics", None)]),
    ("SUPPORT", [("settings", "Settings", None), ("help-circle", "Help", None)]),
]


# --------------------------------------------------------------------------- #
# Icon helper — load a feather svg, recolor its stroke, render to a pixmap.
# --------------------------------------------------------------------------- #
_ICON_CACHE = {}


def feather_pixmap(name, color, size=20):
    key = (name, color, size)
    if key in _ICON_CACHE:
        return _ICON_CACHE[key]
    path = os.path.join(ICON_DIR, name + ".svg")
    pm = QPixmap(size, size)
    pm.fill(Qt.transparent)
    if os.path.exists(path):
        data = open(path, "r", encoding="utf-8").read()
        data = data.replace('stroke="#ffffff"', 'stroke="%s"' % color)
        data = data.replace('stroke="#000000"', 'stroke="%s"' % color)
        renderer = QSvgRenderer(QByteArray(data.encode("utf-8")))
        p = QPainter(pm)
        p.setRenderHint(QPainter.Antialiasing, True)
        renderer.render(p)
        p.end()
    _ICON_CACHE[key] = pm
    return pm


def feather_icon(name, color, size=20):
    return QtGui.QIcon(feather_pixmap(name, color, size))


# --------------------------------------------------------------------------- #
# Small custom widgets
# --------------------------------------------------------------------------- #
class Sparkline(QtWidgets.QWidget):
    """Tiny smooth line + soft gradient fill, painted from a value series."""

    def __init__(self, values, color, parent=None):
        super().__init__(parent)
        self._values = values
        self._color = QColor(color)
        self.setMinimumSize(96, 44)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding,
                           QtWidgets.QSizePolicy.Preferred)

    def setColor(self, color):
        self._color = QColor(color)
        self.update()

    def paintEvent(self, _):
        vals = self._values
        if len(vals) < 2:
            return
        w, h = self.width(), self.height()
        pad = 4.0
        lo, hi = min(vals), max(vals)
        rng = (hi - lo) or 1.0
        step = (w - 2 * pad) / (len(vals) - 1)
        pts = [QtCore.QPointF(pad + i * step,
                              h - pad - (v - lo) / rng * (h - 2 * pad))
               for i, v in enumerate(vals)]

        path = QtGui.QPainterPath(pts[0])
        for i in range(1, len(pts)):
            a, b = pts[i - 1], pts[i]
            mx = (a.x() + b.x()) / 2.0
            path.cubicTo(mx, a.y(), mx, b.y(), b.x(), b.y())

        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, True)

        fill = QtGui.QPainterPath(path)
        fill.lineTo(pts[-1].x(), h)
        fill.lineTo(pts[0].x(), h)
        fill.closeSubpath()
        grad = QtGui.QLinearGradient(0, 0, 0, h)
        c = QColor(self._color)
        c.setAlpha(90)
        grad.setColorAt(0.0, c)
        c2 = QColor(self._color)
        c2.setAlpha(0)
        grad.setColorAt(1.0, c2)
        p.fillPath(fill, grad)

        pen = QtGui.QPen(self._color, 2.2)
        pen.setJoinStyle(Qt.RoundJoin)
        pen.setCapStyle(Qt.RoundCap)
        p.setPen(pen)
        p.drawPath(path)
        p.end()


class DonutChart(QtWidgets.QWidget):
    """A rounded-segment donut, painted directly for pixel control."""

    def __init__(self, values, colors, gap_color="#1b1e26", parent=None):
        super().__init__(parent)
        self._values = values
        self._colors = [QColor(c) for c in colors]
        self._gap = QColor(gap_color)
        self.setMinimumHeight(190)

    def setColors(self, colors):
        self._colors = [QColor(c) for c in colors]
        self.update()

    def setGapColor(self, c):
        self._gap = QColor(c)
        self.update()

    def paintEvent(self, _):
        total = float(sum(self._values)) or 1.0
        w, h = self.width(), self.height()
        side = min(w, h)
        thickness = side * 0.16
        margin = thickness / 2.0 + 6
        rect = QtCore.QRectF((w - side) / 2.0 + margin, (h - side) / 2.0 + margin,
                             side - 2 * margin, side - 2 * margin)
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, True)
        gap = 4.0                       # degrees of visual separation
        start = 90.0                    # start at top, sweep clockwise
        for val, color in zip(self._values, self._colors):
            span = val / total * 360.0
            pen = QtGui.QPen(color, thickness)
            pen.setCapStyle(Qt.RoundCap)
            p.setPen(pen)
            p.drawArc(rect, int((start - gap / 2.0) * 16),
                      int(-(span - gap) * 16))
            start -= span
        p.end()


class InitialsAvatar(QtWidgets.QLabel):
    def __init__(self, initials, color, size=34, parent=None):
        super().__init__(initials, parent)
        self.setFixedSize(size, size)
        self.setAlignment(Qt.AlignCenter)
        r = size // 2
        self.setStyleSheet(
            "background:%s; color:#ffffff; border-radius:%dpx; "
            "font-weight:700; font-size:12px;" % (color, r))


class NavButton(QtWidgets.QPushButton):
    def __init__(self, icon_name, text, badge=None, parent=None):
        super().__init__(parent)
        self.icon_name = icon_name
        self.setObjectName("navBtn")
        self.setCheckable(True)
        self.setCursor(Qt.PointingHandCursor)
        self.setFixedHeight(42)
        lay = QtWidgets.QHBoxLayout(self)
        lay.setContentsMargins(14, 0, 12, 0)
        lay.setSpacing(12)
        self.iconLbl = QtWidgets.QLabel()
        self.iconLbl.setFixedSize(20, 20)
        self.textLbl = QtWidgets.QLabel(text)
        self.textLbl.setObjectName("navText")
        lay.addWidget(self.iconLbl)
        lay.addWidget(self.textLbl)
        lay.addStretch(1)
        if badge:
            self.badge = QCustomBadge(badge, variant="warning")
            self.badge.sizeVariant = "sm"
            lay.addWidget(self.badge)

    def paint_icon(self, color):
        self.iconLbl.setPixmap(feather_pixmap(self.icon_name, color, 20))


# --------------------------------------------------------------------------- #
# Chart styling — background transparent, palette-driven axes/grid. No setTheme
# (we control every colour) so it is fully theme-independent and re-stylable.
# --------------------------------------------------------------------------- #
def style_chart(cw, P, hide_axes=False, xlabels=True, ylabels=True):
    # strip the built-in toolbar and default titles — we supply our own chrome
    for meth in ("setToolbarVisible",):
        try:
            getattr(cw, meth)(False)
        except Exception:
            pass
    for meth in ("setChartTitle", "setXAxisTitle", "setYAxisTitle"):
        if hasattr(cw, meth):
            try:
                getattr(cw, meth)("")
            except Exception:
                pass
    ch = cw.getChart()
    ch.setBackgroundVisible(False)
    ch.setBackgroundBrush(QBrush(Qt.transparent))
    try:
        ch.setPlotAreaBackgroundVisible(False)
    except Exception:
        pass
    ch.setMargins(QMargins(0, 0, 0, 0))
    try:
        ch.legend().setVisible(False)
    except Exception:
        pass
    view = cw.getChartView()
    view.setStyleSheet("background: transparent; border: 0;")
    view.setBackgroundBrush(QBrush(Qt.transparent))

    axis_col = QColor(P["chart_axis"])
    grid_col = QColor(P["chart_grid"])
    axes = ch.axes()
    for ax in axes:
        try:
            ax.setLineVisible(False)
            ax.setGridLineColor(grid_col)
            ax.setLabelsColor(axis_col)
            f = ax.labelsFont()
            f.setPointSizeF(9.0)
            ax.setLabelsFont(f)
        except Exception:
            pass
    if hide_axes:
        for ax in axes:
            ax.setVisible(False)
    else:
        for ax in axes:
            try:
                if ax.orientation() == Qt.Horizontal:
                    ax.setGridLineVisible(False)
                    ax.setLabelsVisible(xlabels)
                else:
                    ax.setGridLineVisible(True)
                    ax.setLabelsVisible(ylabels)
            except Exception:
                pass


# --------------------------------------------------------------------------- #
# Panels / building blocks
# --------------------------------------------------------------------------- #
def hline_dot(color, d=8):
    dot = QtWidgets.QLabel()
    dot.setFixedSize(d, d)
    dot.setStyleSheet("background:%s; border-radius:%dpx;" % (color, d // 2))
    return dot


def legend_item(color, text):
    w = QtWidgets.QWidget()
    lay = QtWidgets.QHBoxLayout(w)
    lay.setContentsMargins(0, 0, 0, 0)
    lay.setSpacing(7)
    lay.addWidget(hline_dot(color))
    lbl = QtWidgets.QLabel(text)
    lbl.setObjectName("legendText")
    lay.addWidget(lbl)
    return w


class Dashboard(QtWidgets.QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.theme = "dark"
        self.setWindowTitle("Winning · Analytics")
        self._nav_buttons = []
        self._charts = []          # (widget, style_kwargs)
        self._spark_widgets = []   # (Sparkline, palette_key)
        self._tick = 0

        root = QtWidgets.QWidget()
        root.setObjectName("root")
        self.setCentralWidget(root)
        outer = QtWidgets.QHBoxLayout(root)
        outer.setContentsMargins(14, 14, 14, 14)
        outer.setSpacing(14)

        outer.addWidget(self._build_sidebar())
        outer.addWidget(self._build_main(), 1)

        self.resize(1360, 880)

        self._timer = QtCore.QTimer(self)
        self._timer.timeout.connect(self._pulse)
        self._timer.start(2500)

    # ---- sidebar --------------------------------------------------------- #
    def _build_sidebar(self):
        bar = QtWidgets.QFrame()
        bar.setObjectName("sidebar")
        bar.setFixedWidth(248)
        lay = QtWidgets.QVBoxLayout(bar)
        lay.setContentsMargins(16, 20, 16, 18)
        lay.setSpacing(4)

        # logo row
        logo_row = QtWidgets.QHBoxLayout()
        logo_row.setSpacing(11)
        mark = QtWidgets.QLabel()
        mark.setObjectName("logoMark")
        mark.setFixedSize(34, 34)
        mark.setAlignment(Qt.AlignCenter)
        mark.setPixmap(feather_pixmap("award", "#ffffff", 19))
        name = QtWidgets.QLabel("Winning")
        name.setObjectName("logoText")
        self.collapseBtn = QtWidgets.QLabel()
        self.collapseBtn.setFixedSize(20, 20)
        logo_row.addWidget(mark)
        logo_row.addWidget(name)
        logo_row.addStretch(1)
        logo_row.addWidget(self.collapseBtn)
        lay.addLayout(logo_row)
        lay.addSpacing(18)

        # nav sections
        for section, items in NAV:
            sec = QtWidgets.QLabel(section)
            sec.setObjectName("navSection")
            lay.addWidget(sec)
            lay.addSpacing(2)
            for icon_name, text, badge in items:
                btn = NavButton(icon_name, text, badge)
                btn.clicked.connect(lambda _=False, b=btn: self._select_nav(b))
                self._nav_buttons.append(btn)
                lay.addWidget(btn)
            lay.addSpacing(14)

        lay.addStretch(1)

        # theme toggle
        self.themeToggle = QCustomSegmentedControl()
        self.themeToggle.setSegments([("Light", "light"), ("Dark", "dark")])
        self.themeToggle.setCurrentIndex(1)
        self.themeToggle.currentChanged.connect(self._on_theme_seg)
        lay.addWidget(self.themeToggle)

        self._nav_buttons[0].setChecked(True)
        return bar

    def _select_nav(self, btn):
        for b in self._nav_buttons:
            b.setChecked(b is btn)
        self._repaint_nav()

    def _repaint_nav(self):
        P = PALETTES[self.theme]
        for b in self._nav_buttons:
            b.paint_icon(P["violet"] if b.isChecked() else P["nav_icon"])

    # ---- main ------------------------------------------------------------ #
    def _build_main(self):
        main = QtWidgets.QFrame()
        main.setObjectName("main")
        lay = QtWidgets.QVBoxLayout(main)
        lay.setContentsMargins(26, 22, 26, 22)
        lay.setSpacing(18)

        lay.addLayout(self._build_header())
        lay.addLayout(self._build_kpis())
        lay.addLayout(self._build_mid_row(), 1)
        lay.addLayout(self._build_bottom_row(), 1)
        return main

    def _build_header(self):
        row = QtWidgets.QHBoxLayout()
        row.setSpacing(12)
        col = QtWidgets.QVBoxLayout()
        col.setSpacing(3)
        title = QtWidgets.QLabel("Welcome back")
        title.setObjectName("pageTitle")
        sub = QtWidgets.QLabel("Check your last activity today")
        sub.setObjectName("pageSub")
        col.addWidget(title)
        col.addWidget(sub)
        row.addLayout(col)
        row.addStretch(1)

        self.searchBtn = self._icon_chip("search")
        self.bellBtn = self._icon_chip("bell", dot=True)
        row.addWidget(self.searchBtn)
        row.addWidget(self.bellBtn)
        av = InitialsAvatar("AK", "#7b6cf6", 40)
        av.setObjectName("headerAvatar")
        row.addWidget(av)
        return row

    def _icon_chip(self, icon_name, dot=False):
        holder = QtWidgets.QFrame()
        holder.setObjectName("iconChip")
        holder.setFixedSize(40, 40)
        hl = QtWidgets.QHBoxLayout(holder)
        hl.setContentsMargins(0, 0, 0, 0)
        lbl = QtWidgets.QLabel()
        lbl.setAlignment(Qt.AlignCenter)
        lbl.setProperty("iconName", icon_name)
        hl.addWidget(lbl)
        holder._iconLabel = lbl
        if dot:
            d = QtWidgets.QLabel(holder)
            d.setObjectName("bellDot")
            d.setFixedSize(8, 8)
            d.move(25, 8)
        return holder

    # ---- KPI cards ------------------------------------------------------- #
    def _build_kpis(self):
        row = QtWidgets.QHBoxLayout()
        row.setSpacing(16)
        self._kpi_cards = []
        for label, value, delta, trend, series, color_key, active in SPARK_KPI:
            card = QtWidgets.QFrame()
            card.setObjectName("kpiCardActive" if active else "kpiCard")
            card.setMinimumHeight(122)
            cl = QtWidgets.QHBoxLayout(card)
            cl.setContentsMargins(18, 16, 18, 16)
            cl.setSpacing(8)

            left = QtWidgets.QVBoxLayout()
            left.setSpacing(6)
            lab = QtWidgets.QLabel(label)
            lab.setObjectName("kpiLabelActive" if active else "kpiLabel")
            val = QtWidgets.QLabel(value)
            val.setObjectName("kpiValueActive" if active else "kpiValue")
            left.addWidget(lab)
            left.addWidget(val)
            left.addStretch(1)

            pill = QtWidgets.QLabel(("↗  " if trend == "up" else "↘  ") + delta)
            if active:
                pill.setObjectName("deltaActive")
                self._active_delta = pill
            else:
                pill.setObjectName("deltaUp" if trend == "up" else "deltaDown")
            prow = QtWidgets.QHBoxLayout()
            prow.addWidget(pill)
            prow.addStretch(1)
            left.addLayout(prow)
            cl.addLayout(left, 0)

            # active card flips its background per theme, so its sparkline must
            # use the contrasting on-card colour, not a fixed accent.
            spark_key = "active_text" if active else color_key
            spark = Sparkline(series, PALETTES[self.theme][spark_key])
            spark.setFixedWidth(118)
            self._spark_widgets.append((spark, spark_key))
            cl.addWidget(spark, 1, Qt.AlignVCenter)

            self._kpi_cards.append(card)
            row.addWidget(card, 1)
        return row

    # ---- middle row: bar chart + donut ----------------------------------- #
    def _build_mid_row(self):
        row = QtWidgets.QHBoxLayout()
        row.setSpacing(16)
        row.addWidget(self._build_sales_panel(), 2)
        row.addWidget(self._build_distribution_panel(), 1)
        return row

    def _panel(self, title):
        panel = QtWidgets.QFrame()
        panel.setObjectName("panel")
        lay = QtWidgets.QVBoxLayout(panel)
        lay.setContentsMargins(20, 18, 20, 18)
        lay.setSpacing(14)
        head = QtWidgets.QHBoxLayout()
        t = QtWidgets.QLabel(title)
        t.setObjectName("panelTitle")
        head.addWidget(t)
        head.addStretch(1)
        return panel, lay, head

    def _build_sales_panel(self):
        P = PALETTES[self.theme]
        panel, lay, head = self._panel("Total sales")
        head.addWidget(legend_item(P["violet"], "Online sales"))
        head.addSpacing(14)
        head.addWidget(legend_item(P["orange"], "Offline sales"))
        lay.addLayout(head)

        bar = QCustomBarChart()
        bar.setStacked(False)
        bar.setCategories(MONTHS)
        bar.addSeries("Online sales", ONLINE, color=QColor(P["violet"]))
        bar.addSeries("Offline sales", OFFLINE, color=QColor(P["orange"]))
        bar.setYAxisRange(0, 30)
        bar.setShowValueLabels(False)
        try:
            bar.setBarWidth(0.55)
        except Exception:
            pass
        bar.setMinimumHeight(300)
        self._charts.append((bar, dict(hide_axes=False)))
        lay.addWidget(bar, 1)
        return panel

    def _build_distribution_panel(self):
        P = PALETTES[self.theme]
        panel, lay, head = self._panel("Sales distribution")
        lay.addLayout(head)

        vals = [v for _n, v, _c in DISTRIBUTION]
        cols = [P[c] for _n, _v, c in DISTRIBUTION]
        self._donut = DonutChart(vals, cols, gap_color=P["card"])
        self._donut.setMinimumHeight(220)
        lay.addWidget(self._donut, 1)

        # custom legend with values
        for name, val, ck in DISTRIBUTION:
            r = QtWidgets.QHBoxLayout()
            r.setSpacing(9)
            r.addWidget(hline_dot(P[ck]))
            nm = QtWidgets.QLabel(name)
            nm.setObjectName("legendText")
            r.addWidget(nm)
            r.addStretch(1)
            pv = QtWidgets.QLabel("%d%%" % val)
            pv.setObjectName("legendValue")
            r.addWidget(pv)
            lay.addLayout(r)
        return panel

    # ---- bottom row: orders feed + customers chart ----------------------- #
    def _build_bottom_row(self):
        row = QtWidgets.QHBoxLayout()
        row.setSpacing(16)
        row.addWidget(self._build_orders_panel(), 1)
        row.addWidget(self._build_customers_panel(), 1)
        return row

    def _build_orders_panel(self):
        panel, lay, head = self._panel("Recent orders")
        lay.addLayout(head)

        header = QtWidgets.QHBoxLayout()
        header.setContentsMargins(0, 0, 0, 0)
        for text, stretch, align in (("Product name", 3, Qt.AlignLeft),
                                     ("Date", 2, Qt.AlignLeft),
                                     ("Price", 1, Qt.AlignLeft),
                                     ("Status", 1, Qt.AlignRight)):
            h = QtWidgets.QLabel(text)
            h.setObjectName("colHead")
            h.setAlignment(align | Qt.AlignVCenter)
            header.addWidget(h, stretch)
        lay.addLayout(header)

        for i, (ini, name, date, price, status, variant) in enumerate(ORDERS):
            r = QtWidgets.QFrame()
            r.setObjectName("orderRow")
            rl = QtWidgets.QHBoxLayout(r)
            rl.setContentsMargins(0, 6, 0, 6)
            rl.setSpacing(8)

            namecell = QtWidgets.QHBoxLayout()
            namecell.setSpacing(11)
            namecell.addWidget(InitialsAvatar(ini, AVATAR_COLORS[i % len(AVATAR_COLORS)], 32))
            nm = QtWidgets.QLabel(name)
            nm.setObjectName("orderName")
            namecell.addWidget(nm)
            namecell.addStretch(1)
            wrap = QtWidgets.QWidget()
            wrap.setLayout(namecell)
            rl.addWidget(wrap, 3)

            d = QtWidgets.QLabel(date)
            d.setObjectName("orderMeta")
            rl.addWidget(d, 2)
            pr = QtWidgets.QLabel(price)
            pr.setObjectName("orderPrice")
            rl.addWidget(pr, 1)

            badge = QCustomBadge(status, variant=variant)
            badge.sizeVariant = "sm"
            bc = QtWidgets.QHBoxLayout()
            bc.setContentsMargins(0, 0, 0, 0)
            bc.addStretch(1)
            bc.addWidget(badge)
            bw = QtWidgets.QWidget()
            bw.setLayout(bc)
            rl.addWidget(bw, 1)

            lay.addWidget(r)
        lay.addStretch(1)
        return panel

    def _build_customers_panel(self):
        P = PALETTES[self.theme]
        panel, lay, head = self._panel("Customers")
        head.addWidget(legend_item(P["violet"], "Loyal customers"))
        head.addSpacing(14)
        head.addWidget(legend_item(P["orange"], "New customers"))
        lay.addLayout(head)

        area = QCustomAreaChart()
        xs = list(range(len(MONTHS)))
        area.addSeries("Loyal customers",
                       list(zip(xs, LOYAL)), color=QColor(P["violet"]), line_width=3.0)
        area.addSeries("New customers",
                       list(zip(xs, NEWC)), color=QColor(P["orange"]), line_width=3.0)
        try:
            area.setGradientFill(True)
            area.setFillOpacity(0.18)
        except Exception:
            pass
        area.setYAxisRange(0, 4)
        area.setXAxisRange(0, len(MONTHS) - 1)
        area.setMinimumHeight(210)
        self._charts.append((area, dict(hide_axes=False, xlabels=False)))
        lay.addWidget(area, 1)

        # month labels row (x axis labels hidden on the chart itself)
        labels = QtWidgets.QHBoxLayout()
        labels.setContentsMargins(6, 0, 6, 0)
        for m in ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]:
            ml = QtWidgets.QLabel(m)
            ml.setObjectName("axisLabel")
            ml.setAlignment(Qt.AlignCenter)
            labels.addWidget(ml, 1)
        lay.addLayout(labels)
        return panel

    # ---- theming --------------------------------------------------------- #
    def _on_theme_seg(self, _idx):
        data = self.themeToggle.currentData()
        self.set_theme(data or "dark")

    def toggle_theme(self):
        self.set_theme("light" if self.theme == "dark" else "dark")
        self.themeToggle.setCurrentIndex(0 if self.theme == "light" else 1)

    def set_theme(self, theme):
        self.theme = theme
        P = PALETTES[theme]
        self.app.setStyleSheet(base_chrome(P))
        applyDesignTokens(self.app, tokens=DesignTokens(theme=theme))
        # re-apply the parts QSS can't reach
        self._repaint_nav()
        for spark, ck in self._spark_widgets:
            spark.setColor(P[ck])
        for holder in self.findChildren(QtWidgets.QFrame, "iconChip"):
            lbl = getattr(holder, "_iconLabel", None)
            if lbl is not None:
                lbl.setPixmap(feather_pixmap(lbl.property("iconName"), P["muted"], 18))
        self.collapseBtn.setPixmap(feather_pixmap("sidebar", P["muted"], 18))
        # charts
        for cw, kw in self._charts:
            style_chart(cw, P, **kw)
        # donut (custom-painted) tracks the theme too
        donut = getattr(self, "_donut", None)
        if donut is not None:
            donut.setColors([P[c] for _n, _v, c in DISTRIBUTION])
            donut.setGapColor(P["card"])
        # active KPI pill: the card flips colour, so style the pill for contrast
        pill = getattr(self, "_active_delta", None)
        if pill is not None:
            if theme == "dark":     # white card
                css = "color:#1f9d63; background:rgba(31,157,99,0.14);"
            else:                   # violet card
                css = "color:#ffffff; background:rgba(255,255,255,0.22);"
            pill.setStyleSheet(css + " border-radius:8px; padding:3px 9px;"
                               " font-weight:700; font-size:11px;")

    # ---- live pulse ------------------------------------------------------ #
    def _pulse(self):
        self._tick += 1
        for spark, _ck in self._spark_widgets:
            vals = spark._values
            nudged = [max(0.0, v + math.sin(self._tick / 2.0 + i) * (max(vals) * 0.03))
                      for i, v in enumerate(vals)]
            spark._values = nudged
            spark.update()


# --------------------------------------------------------------------------- #
# Chrome QSS — objectName-scoped so it wins over the token block appended after.
# --------------------------------------------------------------------------- #
def base_chrome(P):
    return """
    QWidget {{ color: {text}; font-family: 'Inter', 'Segoe UI', sans-serif; font-size: 13px; }}
    QToolTip {{ color: {text}; background: {card}; border: 1px solid {line}; }}
    #root {{ background: {bg}; }}

    #sidebar {{ background: {panel}; border-radius: 22px; }}
    #main    {{ background: {panel}; border-radius: 22px; }}

    #logoMark {{ background: qlineargradient(x1:0,y1:0,x2:1,y2:1,
                 stop:0 {violet}, stop:1 {orange}); border-radius: 10px; }}
    #logoText {{ font-size: 18px; font-weight: 800; letter-spacing: .3px; }}
    #navSection {{ color: {faint}; font-size: 10px; font-weight: 700;
                   letter-spacing: 1.6px; padding: 2px 6px; }}

    QPushButton#navBtn {{ background: transparent; border: 0; border-radius: 11px; text-align: left; }}
    QPushButton#navBtn:hover {{ background: {hover}; }}
    QPushButton#navBtn:checked {{ background: {nav_active}; }}
    QPushButton#navBtn #navText {{ color: {nav_text}; font-size: 13.5px; }}
    QPushButton#navBtn:checked #navText {{ color: {text}; font-weight: 600; }}

    #pageTitle {{ font-size: 27px; font-weight: 800; letter-spacing: .2px; }}
    #pageSub {{ color: {muted}; font-size: 13px; }}

    #iconChip {{ background: {card}; border: 1px solid {line}; border-radius: 13px; }}
    #iconChip:hover {{ background: {card2}; }}
    #bellDot {{ background: {orange}; border-radius: 4px; }}

    #kpiCard {{ background: {card}; border: 1px solid {line}; border-radius: 20px; }}
    #kpiCardActive {{ background: {active_card}; border-radius: 20px; }}
    #kpiLabel {{ color: {muted}; font-size: 13px; }}
    #kpiLabelActive {{ color: {active_sub}; font-size: 13px; }}
    #kpiValue {{ color: {text}; font-size: 30px; font-weight: 800; }}
    #kpiValueActive {{ color: {active_text}; font-size: 30px; font-weight: 800; }}
    #deltaUp {{ color: {green}; background: rgba(61,220,151,0.14);
               border-radius: 8px; padding: 3px 9px; font-weight: 700; font-size: 11px; }}
    #deltaDown {{ color: {red}; background: rgba(245,103,138,0.14);
                 border-radius: 8px; padding: 3px 9px; font-weight: 700; font-size: 11px; }}

    #panel {{ background: {card}; border: 1px solid {line}; border-radius: 20px; }}
    #panelTitle {{ font-size: 16.5px; font-weight: 700; }}
    #legendText {{ color: {muted}; font-size: 12px; }}
    #legendValue {{ color: {text}; font-size: 12.5px; font-weight: 700; }}
    #axisLabel {{ color: {chart_axis}; font-size: 11px; }}

    #colHead {{ color: {faint}; font-size: 11.5px; font-weight: 600; }}
    #orderRow {{ background: transparent; border: 0; border-bottom: 1px solid {line}; }}
    #orderName {{ font-size: 13.5px; font-weight: 600; }}
    #orderMeta {{ color: {muted}; font-size: 12.5px; }}
    #orderPrice {{ font-size: 13px; font-weight: 700; }}

    QLineEdit {{ background: {card2}; color: {text}; border: 1px solid {line};
                 border-radius: 10px; padding: 7px 11px; selection-background-color: {violet}; }}
    QLineEdit:focus {{ border: 1px solid {violet}; }}
    """.format(**P)


# --------------------------------------------------------------------------- #
# Screenshot driver
# --------------------------------------------------------------------------- #
def _shoot(win, app, out_dir):
    os.makedirs(out_dir, exist_ok=True)

    def grab(path):
        app.processEvents()
        win.grab().save(path)
        print("[shot] wrote", path, flush=True)

    QtCore.QTimer.singleShot(1000, lambda: grab(os.path.join(out_dir, "winning_dark.png")))
    QtCore.QTimer.singleShot(1500, win.toggle_theme)
    QtCore.QTimer.singleShot(2100, lambda: grab(os.path.join(out_dir, "winning_light.png")))
    QtCore.QTimer.singleShot(2500, win.toggle_theme)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--shots", metavar="DIR", default=None)
    parser.add_argument("--exit-after", type=float, default=0)
    args = parser.parse_args()

    app = QtWidgets.QApplication(sys.argv)
    win = Dashboard(app)
    win.set_theme("dark")
    win.show()

    if args.shots:
        _shoot(win, app, args.shots)
    if args.exit_after:
        QtCore.QTimer.singleShot(int(args.exit_after * 1000), app.quit)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
