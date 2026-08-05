"""Winning dashboard — GUI orchestration.

A single GuiFunctions orchestrator holds one Manager per page. navigateTo(name)
switches the animated pageStack by *widget* (never by index) and marks the active
sidebar button. Each manager reaches its embedded component via
``container.component`` and wires child widgets by objectName. Runtime data +
interactions live here (and in background workers), never in the .ui.

Theme switching goes through the icon pipeline BY NAME (Winning Dark / Light),
so the custom themes' icon sets recolour correctly. Chart hues come from the
token-driven ChartPalette in style.json, so they flip with the theme too.

ZERO inline stylesheets: data-coloured chrome (legend dots, initials avatars,
status badges, delta pills) is styled ONLY in Qss/scss/chrome.scss via enumerable
dynamic props ([chartKey=...], [avatarKey=...], [trend=...], [variant=...])
whose hues are each theme's Other-variables from json-styles/style.json.
Painted colours (chart series, sparklines) use typed Qt properties/APIs fed
from the ChartPalette section of the same file.
"""

import os

from qtpy.QtCore import QObject, QTimer, QByteArray, Qt, QThread, QMargins
from qtpy.QtGui import QColor, QPainter, QPixmap, QIcon, QBrush
from qtpy.QtWidgets import (QApplication, QFrame, QLabel, QWidget,
                            QVBoxLayout, QHBoxLayout)
from qtpy.QtSvg import QSvgRenderer

import Custom_Widgets
from Custom_Widgets.QCustomSparkline import QCustomSparkline
from Custom_Widgets.QCustomBadge import QCustomBadge

from gui import theme as T
from gui import data as D
from gui.workers import LiveMetricsWorker

# Shared feather icon set that ships with the library.
_ICON_DIR = os.path.join(os.path.dirname(Custom_Widgets.__file__), "Qss", "icons", "feather")
_PM_CACHE = {}

NAV_ICONS = {
    "dashboard": "grid", "products": "package", "orders": "shopping-cart",
    "customers": "users", "marketing": "award", "analytics": "bar-chart-2",
    "settings": "settings", "help": "help-circle",
}


def feather_pixmap(name, color, size=20):
    key = (name, color, size)
    if key in _PM_CACHE:
        return _PM_CACHE[key]
    path = os.path.join(_ICON_DIR, name + ".svg")
    pm = QPixmap(size, size)
    pm.fill(QColor(0, 0, 0, 0))
    if os.path.exists(path):
        svg = open(path, "r", encoding="utf-8").read()
        svg = svg.replace('stroke="#ffffff"', 'stroke="%s"' % color)
        svg = svg.replace('stroke="#000000"', 'stroke="%s"' % color)
        r = QSvgRenderer(QByteArray(svg.encode("utf-8")))
        p = QPainter(pm)
        p.setRenderHint(QPainter.Antialiasing, True)
        r.render(p)
        p.end()
    _PM_CACHE[key] = pm
    return pm


def feather_icon(name, color, size=20):
    return QIcon(feather_pixmap(name, color, size))


# --------------------------------------------------------------------------- #
# Base page manager
# --------------------------------------------------------------------------- #
class PageManager(QObject):
    def __init__(self, win, container):
        super().__init__(win)
        self.win = win
        self.container = container
        self._loaded = False

    @property
    def component(self):
        return getattr(self.container, "component", None)

    def onShown(self):
        if self._loaded:
            return
        comp = self.component
        if comp is None:
            QTimer.singleShot(80, self.onShown)   # container loads async on first show
            return
        try:
            self.setup(comp)
            self._loaded = True
        except Exception as e:
            import traceback
            print("[winning] %s setup failed: %s" % (type(self).__name__, e))
            traceback.print_exc()

    def setup(self, comp):
        pass

    def recolor(self, palette):
        pass

    def teardown(self):
        pass

    # theme helpers shared by managers ------------------------------------- #
    def _theme_name(self):
        eng = getattr(self.win, "themeEngine", None)
        return str(getattr(eng, "theme", "") or T.THEME_DARK)

    def _palette(self):
        return T.chart_palette(self._theme_name())

    def _accent_hex(self):
        return "#6c5ce7" if T.is_light(self._theme_name()) else "#7b6cf6"


# --------------------------------------------------------------------------- #
# Small builders — no inline stylesheets. Colour comes from Qss/scss/chrome.scss:
# enumerable dynamic props (avatarKey / chartKey / trend) select rules whose
# hues are the theme's Other-variables, so everything flips on theme switch.
# --------------------------------------------------------------------------- #
def _round_avatar(text, idx, size=32):
    a = QLabel(text)
    a.setFixedSize(size, size)
    a.setAlignment(Qt.AlignCenter)
    a.setProperty("role", "avatar")
    a.setProperty("avatarKey", str(idx % 5))    # -> scss [avatarKey="0..4"]
    return a


def _dot(key, d=9):
    lbl = QLabel()
    lbl.setFixedSize(d, d)
    lbl.setProperty("role", "dot")
    lbl.setProperty("chartKey", key)            # -> scss [chartKey="online"...]
    return lbl


def _legend(key, text):
    w = QWidget()
    lay = QHBoxLayout(w)
    lay.setContentsMargins(0, 0, 0, 0)
    lay.setSpacing(7)
    lay.addWidget(_dot(key))
    lab = QLabel(text)
    lab.setProperty("role", "legend")
    lay.addWidget(lab)
    return w


# --------------------------------------------------------------------------- #
# Dashboard
# --------------------------------------------------------------------------- #
class DashboardManager(PageManager):
    def setup(self, comp):
        self.comp = comp
        self._kpi = {}          # key -> {value,spark,active,delta,trend}
        pal = self._palette()

        self._build_header(comp)
        self._build_kpis(comp, pal)
        self._build_sales(comp, pal)
        self._build_dist(comp, pal)
        self._build_orders(comp, pal)
        self._build_customers(comp, pal)

        # Background worker: Worker -> Signal -> GUI (queued to the GUI thread).
        self._thread = QThread(self.win)
        self._worker = LiveMetricsWorker(interval=2.0)
        self._worker.moveToThread(self._thread)
        self._thread.started.connect(self._worker.run)
        self._worker.tick.connect(self._on_tick)
        self._thread.start()
        QApplication.instance().aboutToQuit.connect(self.teardown)

    # -- chart chrome ------------------------------------------------------ #
    def _strip(self, cw, pal, hide_axes=False, xlabels=True):
        try:
            cw.setToolbarVisible(False)
        except Exception:
            pass
        for m in ("setChartTitle", "setXAxisTitle", "setYAxisTitle"):
            if hasattr(cw, m):
                try:
                    getattr(cw, m)("")
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
        v = cw.getChartView()
        # transparent native holder: attribute + scss rule, no inline stylesheet
        v.setAttribute(Qt.WA_TranslucentBackground, True)
        v.setBackgroundBrush(QBrush(Qt.transparent))
        axis = QColor(pal.get("axis", "#888888"))
        grid = QColor(pal.get("grid", "#ffffff22"))
        for ax in ch.axes():
            try:
                ax.setLineVisible(False)
                ax.setLabelsColor(axis)
                f = ax.labelsFont()
                f.setPointSizeF(9.0)
                ax.setLabelsFont(f)
            except Exception:
                pass
        if hide_axes:
            for ax in ch.axes():
                ax.setVisible(False)
        else:
            for ax in ch.axes():
                try:
                    if ax.orientation() == Qt.Horizontal:
                        ax.setGridLineVisible(False)
                        ax.setLabelsVisible(xlabels)
                    else:
                        ax.setGridLineVisible(True)
                        ax.setLabelsVisible(True)
                        ax.setGridLineColor(grid)
                except Exception:
                    pass

    # -- header ------------------------------------------------------------ #
    # headerAvatar chrome lives in scss (#headerAvatar, accent token) — only
    # the painted feather pixmaps are (re)tinted here.
    def _build_header(self, comp):
        col = T.icon_color(self._theme_name())
        comp.searchIcon.setPixmap(feather_pixmap("search", col, 18))
        comp.bellIcon.setPixmap(feather_pixmap("bell", col, 18))

    # -- KPI cards --------------------------------------------------------- #
    def _build_kpis(self, comp, pal):
        row = comp.kpiRow.layout()
        for key, label, series, ckey, active in D.KPIS:
            card = QFrame()
            card.setProperty("role", "kpiActive" if active else "kpi")
            card.setMinimumHeight(120)
            cl = QHBoxLayout(card)
            cl.setContentsMargins(18, 16, 18, 16)
            cl.setSpacing(8)

            left = QVBoxLayout()
            left.setSpacing(6)
            lab = QLabel(label)
            lab.setProperty("role", "kpiLabel")
            val = QLabel("—")
            val.setProperty("role", "kpiValue")
            left.addWidget(lab)
            left.addWidget(val)
            left.addStretch(1)
            delta = QLabel("")
            delta.setProperty("role", "delta")
            # enumerable trend prop -> scss [trend="up"/"down"/"onAccent"]
            delta.setProperty("trend", "onAccent" if active else
                              ("down" if ckey == "down" else "up"))
            drow = QHBoxLayout()
            drow.addWidget(delta)
            drow.addStretch(1)
            left.addLayout(drow)
            cl.addLayout(left, 0)

            spark = QCustomSparkline(values=list(series))
            spark.setFixedWidth(114)
            cl.addWidget(spark, 1, Qt.AlignVCenter)

            row.addWidget(card, 1)
            trend = "down" if ckey == "down" else "up"
            self._kpi[key] = {"value": val, "spark": spark, "active": active,
                              "delta": delta, "trend": trend, "ckey": ckey}
        self._style_kpis(pal)

    # Pill styling is pure scss ([role="delta"][trend=...]); Python only feeds
    # the sparkline's TYPED lineColor property from the theme's ChartPalette.
    def _style_kpis(self, pal):
        for key, ref in self._kpi.items():
            if ref["active"]:
                ref["spark"].lineColor = QColor("#ffffff")
            else:
                ref["spark"].lineColor = QColor(pal[ref["ckey"]])
            ref["delta"].setText(("↗  +5%" if key == "orders" else
                                  "↗  +3%" if key == "sales" else
                                  "↗  +2%" if key == "sessions" else "↘  -1%"))

    # -- sales bar chart --------------------------------------------------- #
    def _build_sales(self, comp, pal):
        c = comp.salesChart
        c.setStacked(False)
        c.setCategories(D.MONTHS)
        c.addSeries("Online sales", D.ONLINE, color=QColor(pal["online"]))
        c.addSeries("Offline sales", D.OFFLINE, color=QColor(pal["offline"]))
        c.setYAxisRange(0, 30)
        c.setShowValueLabels(False)
        try:
            c.setBarWidth(0.55)
        except Exception:
            pass
        c.setBarCornerRadius(6)
        c.setGridLineColor(QColor(pal["grid"]))
        self._strip(c, pal)
        for key, label in (("online", "Online sales"), ("offline", "Offline sales")):
            comp.salesLegend.layout().addWidget(_legend(key, label))

    # -- distribution donut ------------------------------------------------ #
    def _build_dist(self, comp, pal):
        c = comp.distChart      # QCustomDonut — painted concentric rings (mode=rings)
        vals = [v for _n, v, _k in D.DISTRIBUTION]
        cols = [pal[k] for _n, _v, k in D.DISTRIBUTION]
        c.setData(vals, cols)
        c.setTrackColor(QColor(pal["donutTrack"]))    # QColor hex is #AARRGGBB
        for n, v, k in D.DISTRIBUTION:
            roww = QWidget()
            rl = QHBoxLayout(roww)
            rl.setContentsMargins(0, 0, 0, 0)
            rl.setSpacing(9)
            rl.addWidget(_dot(k))
            nm = QLabel(n)
            nm.setProperty("role", "legend")
            rl.addWidget(nm)
            rl.addStretch(1)
            pv = QLabel("%d%%" % v)
            pv.setProperty("role", "legendVal")
            rl.addWidget(pv)
            comp.distLegend.layout().addWidget(roww)

    # -- orders feed ------------------------------------------------------- #
    def _build_orders(self, comp, pal):
        for i, (ini, name, date, price, status, variant) in enumerate(D.ORDERS):
            row = QFrame()
            row.setProperty("role", "orderRow")
            rl = QHBoxLayout(row)
            rl.setContentsMargins(0, 6, 0, 6)
            rl.setSpacing(8)

            namecell = QWidget()
            ncl = QHBoxLayout(namecell)
            ncl.setContentsMargins(0, 0, 0, 0)
            ncl.setSpacing(11)
            ncl.addWidget(_round_avatar(ini, i))
            nm = QLabel(name)
            nm.setProperty("role", "orderName")
            ncl.addWidget(nm)
            ncl.addStretch(1)
            rl.addWidget(namecell, 3)

            d = QLabel(date)
            d.setProperty("role", "orderMeta")
            rl.addWidget(d, 2)
            pr = QLabel(price)
            pr.setProperty("role", "orderPrice")
            rl.addWidget(pr, 1)

            # variant is a typed Qt property -> scss QCustomBadge[variant=...]
            badge = QCustomBadge(status, variant=variant)
            badge.sizeVariant = "sm"
            bw = QWidget()
            bl = QHBoxLayout(bw)
            bl.setContentsMargins(0, 0, 0, 0)
            bl.addStretch(1)
            bl.addWidget(badge)
            rl.addWidget(bw, 1)

            comp.ordersBody.layout().addWidget(row)

    # -- customers area chart ---------------------------------------------- #
    def _build_customers(self, comp, pal):
        c = comp.customersChart
        xs = list(range(len(D.MONTHS)))
        c.addSeries("Loyal customers", list(zip(xs, D.LOYAL)),
                    color=QColor(pal["loyal"]), line_width=3.0)
        c.addSeries("New customers", list(zip(xs, D.NEWC)),
                    color=QColor(pal["new"]), line_width=3.0)
        try:
            c.setGradientFill(True)
            c.setFillOpacity(0.18)
        except Exception:
            pass
        c.setYAxisRange(0, 4)
        c.setXAxisRange(0, len(D.MONTHS) - 1)
        self._strip(c, pal, hide_axes=False, xlabels=False)
        for key, label in (("loyal", "Loyal customers"), ("new", "New customers")):
            comp.custLegend.layout().addWidget(_legend(key, label))
        for m in ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]:
            ml = QLabel(m)
            ml.setProperty("role", "axis")
            ml.setAlignment(Qt.AlignCenter)
            comp.monthRow.layout().addWidget(ml, 1)

    # -- live updates from the worker -------------------------------------- #
    def _on_tick(self, payload):
        vals = payload.get("values", {})
        spark = payload.get("spark", {})
        for key, ref in self._kpi.items():
            if key in vals:
                ref["value"].setText(D.fmt_kpi(key, vals[key]))
            if key in spark and not ref["active"]:
                ref["spark"].setValues(spark[key])
            elif key in spark and ref["active"]:
                ref["spark"].setValues(spark[key])

    # -- theme recolour ---------------------------------------------------- #
    def recolor(self, pal):
        comp = self.comp
        # charts
        try:
            comp.salesChart.setSeriesColor("Online sales", QColor(pal["online"]))
            comp.salesChart.setSeriesColor("Offline sales", QColor(pal["offline"]))
            comp.salesChart.setGridLineColor(QColor(pal["grid"]))
            self._strip(comp.salesChart, pal)
        except Exception:
            pass
        try:
            comp.distChart.setColors([pal[k] for _n, _v, k in D.DISTRIBUTION])
            comp.distChart.setTrackColor(QColor(pal["donutTrack"]))
        except Exception:
            pass
        try:
            comp.customersChart.setSeriesColor("Loyal customers", QColor(pal["loyal"]))
            comp.customersChart.setSeriesColor("New customers", QColor(pal["new"]))
            self._strip(comp.customersChart, pal, hide_axes=False, xlabels=False)
        except Exception:
            pass
        # Dots / avatars / badges / delta pills need NOTHING here: their scss
        # rules reference the theme's Other-variables, so the theme engine's
        # recompiled stylesheet restyles them on its own. Only painted things
        # (sparkline lines, feather pixmaps) are re-fed.
        self._style_kpis(pal)
        self._build_header(comp)

    def teardown(self):
        try:
            self._worker.stop()
            self._thread.quit()
            self._thread.wait(1500)
        except Exception:
            pass


# --------------------------------------------------------------------------- #
# Orchestrator
# --------------------------------------------------------------------------- #
class GuiFunctions:
    def __init__(self, win):
        self.win = win
        self.ui = win.ui

    def initialize(self):
        ui = self.ui
        self.pages = {"dashboard": ui.dashboardContainer}
        self.navButtons = {
            "dashboard": ui.navDashboard, "products": ui.navProducts,
            "orders": ui.navOrders, "customers": ui.navCustomers,
            "marketing": ui.navMarketing, "analytics": ui.navAnalytics,
            "settings": ui.navSettings, "help": ui.navHelp,
        }
        self.managers = {"dashboard": DashboardManager(self.win, ui.dashboardContainer)}

        for name, btn in self.navButtons.items():
            btn.clicked.connect(lambda _=False, n=name: self.navigateTo(n))

        # Collapse/expand the sidebar — wired ONCE here (deterministic).
        ui.sidebarToggle.clicked.connect(ui.sidebar.toggleMenu)

        # Theme switching BY NAME through the icon pipeline (see the comment: the
        # generic Light/Dark toggle never matches a CUSTOM theme name, so icon
        # recolour would fall back to the default theme).
        self.themeEngine = getattr(self.win, "themeEngine", None)
        ui.themeToggle.clicked.connect(self.toggleTheme)
        if self.themeEngine is not None:
            try:
                self.themeEngine.onThemeChangeComplete.connect(self._onThemeReady)
            except Exception:
                pass

        self._paintChrome()
        self.navigateTo("dashboard")

    # -- theme ------------------------------------------------------------- #
    def _currentTheme(self):
        return str(getattr(self.themeEngine, "theme", "") or T.THEME_DARK)

    def toggleTheme(self):
        if self.themeEngine is None:
            return
        target = T.THEME_DARK if T.is_light(self._currentTheme()) else T.THEME_LIGHT
        self.themeEngine.setTheme(target)     # async icon regen on a worker thread
        self._updateThemeButton(target)

    def _onThemeReady(self):
        self._paintChrome()
        pal = T.chart_palette(self._currentTheme())
        for mgr in self.managers.values():
            try:
                mgr.recolor(pal)
            except Exception:
                pass

    def _updateThemeButton(self, theme_name):
        light = T.is_light(theme_name)
        try:
            self.ui.themeToggle.setText("  Dark theme" if light else "  Light theme")
            self.ui.themeToggle.setIcon(feather_icon("sun" if light else "moon",
                                                     T.icon_color(theme_name), 18))
        except Exception:
            pass

    def _paintChrome(self):
        theme = self._currentTheme()
        col = T.icon_color(theme)
        for name, btn in self.navButtons.items():
            icon_col = self._accent() if btn.isChecked() else col
            btn.setIcon(feather_icon(NAV_ICONS.get(name, "circle"), icon_col, 20))
        try:
            self.ui.brandLabel.setIcon(feather_icon("award", self._accent(), 24))
        except Exception:
            pass
        try:
            self.ui.sidebarToggle.setIcon(feather_icon("sidebar", col, 18))
        except Exception:
            pass
        self._updateThemeButton(theme)

    def _accent(self):
        return "#6c5ce7" if T.is_light(self._currentTheme()) else "#7b6cf6"

    # -- navigation -------------------------------------------------------- #
    def navigateTo(self, name):
        page = self.pages.get(name)
        if page is not None:
            self.ui.pageStack.setCurrentWidget(page)
        for n, btn in self.navButtons.items():
            btn.setChecked(n == name)
        self._paintChrome()
        mgr = self.managers.get(name)
        if mgr is not None:
            mgr.onShown()
