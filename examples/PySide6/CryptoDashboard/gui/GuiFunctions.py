"""Crypto dashboard — GUI orchestration (the CORRECT Custom_Widgets way).

A single GuiFunctions orchestrator holds one Manager per page. The manager
reaches its embedded component via ``container.component`` and configures the
library widgets Designer cannot set (segmented controls, the area chart, the
DataTable columns/rows, avatars) IN CODE — like charts. Runtime data lives in
gui/data.py; the market rows arrive from a background Worker->Signal->GUI.

Colours for data-viz + dark chrome come from the token-driven ChartPalette in
style.json, so they flip when the theme switches. Coin brand colours live in a
Coins section of the same file. Theme switching goes BY NAME (Crypto Light/Dark).

Icons are painted per-widget (feather SVG -> recoloured pixmap): this UI mixes a
DARK sidebar rail and LIGHT cards, so a single global QSS Icons-color can't serve
both surfaces — each icon is tinted for the surface it sits on (rail vs card),
exactly like the canonical FinanceDashboard reference.
"""

import os

from qtpy.QtCore import QObject, Qt, QByteArray, QThread, QTimer
from qtpy.QtGui import QColor, QPainter, QPixmap, QIcon, QBrush
from qtpy.QtWidgets import QApplication, QLabel
from qtpy.QtSvg import QSvgRenderer

import Custom_Widgets
from Custom_Widgets.QCustomDataTable import DataTableColumn

from gui import theme as T
from gui import data as D
from gui.workers import MarketWorker

_ICON_DIR = os.path.join(os.path.dirname(Custom_Widgets.__file__), "Qss", "icons", "feather")
_PM_CACHE = {}


def feather_pixmap(name, color, size=22, stroke=2.1):
    key = (name, color, size, stroke)
    if key in _PM_CACHE:
        return _PM_CACHE[key]
    path = os.path.join(_ICON_DIR, name + ".svg")
    pm = QPixmap(int(size * 2), int(size * 2))
    pm.fill(QColor(0, 0, 0, 0))
    if os.path.exists(path):
        svg = open(path, "r", encoding="utf-8").read()
        svg = svg.replace('stroke="#ffffff"', 'stroke="%s"' % color)  # noqa: hardcoded-hex (SVG source token, not a chrome colour)
        svg = svg.replace('stroke="#000000"', 'stroke="%s"' % color)  # noqa: hardcoded-hex (SVG source token, not a chrome colour)
        svg = svg.replace('stroke-width="3"', 'stroke-width="%s"' % stroke)
        r = QSvgRenderer(QByteArray(svg.encode("utf-8")))
        p = QPainter(pm)
        p.setRenderHint(QPainter.Antialiasing, True)
        r.render(p)
        p.end()
    pm.setDevicePixelRatio(2.0)
    _PM_CACHE[key] = pm
    return pm


def feather_icon(name, color, size=22, stroke=2.1):
    return QIcon(feather_pixmap(name, color, size, stroke))


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
            QTimer.singleShot(80, self.onShown)     # container loads async on first show
            return
        try:
            self.setup(comp)
            self._loaded = True
        except Exception:
            import traceback
            traceback.print_exc()

    def setup(self, comp):
        pass

    def recolor(self, pal):
        pass

    def _theme_name(self):
        eng = getattr(self.win, "themeEngine", None)
        return str(getattr(eng, "theme", "") or T.THEME_LIGHT)

    def _palette(self):
        return T.chart_palette(self._theme_name())


# --------------------------------------------------------------------------- #
# Dashboard manager
# --------------------------------------------------------------------------- #
class DashboardManager(PageManager):
    def setup(self, comp):
        self.comp = comp
        pal = self._palette()
        self._segments(comp)
        self._build_overview(comp, pal)
        self._build_market(comp, pal)
        self._build_promo(comp, pal)
        self._build_trade(comp, pal)
        self._wire(comp)

        # Background worker: Worker -> Signal -> GUI (queued to the GUI thread).
        self._thread = QThread(self.win)
        self._worker = MarketWorker()
        self._worker.moveToThread(self._thread)
        self._thread.started.connect(self._worker.run)
        self._worker.rowsReady.connect(self._on_rows)
        self._thread.start()
        QApplication.instance().aboutToQuit.connect(self.teardown)

    # -- segmented controls ------------------------------------------------- #
    def _segments(self, comp):
        for ctrl, items in ((comp.rangeControl, D.RANGE_SEGMENTS),
                            (comp.marketTabs, D.MARKET_TABS),
                            (comp.tradeTabs, D.TRADE_TABS)):
            ctrl.setSegments(items)
            ctrl.setCurrentIndex(0)                    # index-dependent: set AFTER segments
            # custom QWidget needs this so the QSS track background actually paints
            ctrl.setAttribute(Qt.WA_StyledBackground, True)

    # -- overview: value + trend chip + area chart + time axis -------------- #
    def _build_overview(self, comp, pal):
        card = T.card_icon_color(self._theme_name())
        comp.changeChip.upColor = QColor(pal["up"])
        comp.changeChip.setDirection("up")
        comp.changeValue.setStyleSheet(
            "color:%s; background:transparent; font-size:14px; font-weight:800;" % pal["up"])
        comp.coinPick.setIcon(feather_icon("chevron-down", card, 15, stroke=2.4))
        self._build_chart(comp, pal)
        # time-axis labels painted under the chart (chart's own x-labels hidden)
        row = comp.timeRow.layout()
        while row.count():
            it = row.takeAt(0)
            if it.widget():
                it.widget().deleteLater()
        for i, t in enumerate(D.OVERVIEW_TIMES):
            lbl = QLabel(t)
            lbl.setProperty("role", "axis")
            if i == 0:
                lbl.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            elif i == len(D.OVERVIEW_TIMES) - 1:
                lbl.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            else:
                lbl.setAlignment(Qt.AlignCenter)
            row.addWidget(lbl, 1)

    def _build_chart(self, comp, pal):
        c = comp.overviewChart
        xs = list(range(len(D.OVERVIEW_SERIES)))
        try:
            c.addSeries("Wallet", list(zip(xs, D.OVERVIEW_SERIES)),
                        color=QColor(pal["chartLine"]), line_width=2.6)
        except TypeError:
            c.addSeries("Wallet", list(zip(xs, D.OVERVIEW_SERIES)))
        try:
            c.setAreaBorderEdges(False)   # no vertical closing walls; crisp top line only
            c.setGradientFill(True)
            c.setFillOpacity(0.22)
        except Exception:
            pass
        lo, hi = min(D.OVERVIEW_SERIES), max(D.OVERVIEW_SERIES)
        pad = (hi - lo) * 0.35 or 1.0
        c.setYAxisRange(lo - pad, hi + pad)
        c.setXAxisRange(0, len(D.OVERVIEW_SERIES) - 1)
        self._strip_chart(c, pal)

    def _strip_chart(self, c, pal):
        getattr(c, "setToolbarVisible", lambda *a: None)(False)   # no interactive toolbar
        for m in ("setChartTitle", "setXAxisTitle", "setYAxisTitle"):
            getattr(c, m, lambda *a: None)("")
        try:
            ch = c.getChart()
            ch.setBackgroundVisible(False)
            ch.setBackgroundBrush(QBrush(Qt.transparent))
            ch.setPlotAreaBackgroundVisible(False)
            ch.legend().setVisible(False)
            v = c.getChartView()
            v.setStyleSheet("background: transparent; border: 0;")
            v.setBackgroundBrush(QBrush(Qt.transparent))
            axis = QColor(pal["axis"])
            grid = QColor(pal["grid"])
            for ax in ch.axes():
                ax.setLineVisible(False)
                ax.setLabelsColor(axis)
                f = ax.labelsFont()
                f.setPointSizeF(9.0)
                ax.setLabelsFont(f)
                if ax.orientation() == Qt.Horizontal:
                    ax.setGridLineVisible(False)
                    ax.setLabelsVisible(False)          # times are painted in timeRow
                else:
                    ax.setGridLineVisible(True)
                    ax.setLabelsVisible(True)
                    ax.setGridLineColor(grid)
        except Exception:
            pass

    # -- market DataTable --------------------------------------------------- #
    def _market_rows(self, pal):
        coins = T.coins()
        rows = []
        for tk, name, amount, price, change, sign in D.MARKET:
            rows.append({
                "dot": "", "dotColor": coins.get(tk, pal["muted"]),
                "name": tk, "name2": name,
                "amount": amount, "price": price,
                "change": change,
                "changeColor": pal["up"] if sign == "up" else pal["down"],
                "trade": "Trade",
            })
        return rows

    def _market_columns(self, pal):
        return [
            DataTableColumn("dot", title="", renderer="status",
                            colorKey="dotColor", sortable=False),
            DataTableColumn("name", title="Name", renderer="twoline",
                            subtitleKey="name2", subtitleScale=-1),
            DataTableColumn("amount", title="Amount"),
            DataTableColumn("price", title="Price"),
            DataTableColumn("change", title="24 Change", renderer="colored",
                            colorKey="changeColor"),
            DataTableColumn("trade", title="", renderer="badge",
                            color=pal["accent"], align=Qt.AlignCenter, sortable=False),
        ]

    def _build_market(self, comp, pal):
        t = comp.marketTable
        t.customizeQCustomDataTable(columns=self._market_columns(pal),
                                    selectable=False, showPagination=False,
                                    alternatingRowColors=False)
        t.view().verticalHeader().setDefaultSectionSize(54)
        t.setStatusDotSize(14)
        t.setPersistentSortIndicators(True)
        t.setFlexColumn(1)                             # Name column stretches
        t.setFlexMinWidth(120)
        for i, w in ((0, 36), (2, 108), (3, 108), (4, 96), (5, 92)):
            t.view().setColumnWidth(i, w)
        self._market_theme(t, pal)
        t.setData(self._market_rows(pal))
        try:
            t.cellClicked.connect(self._on_cell)
        except Exception:
            pass

    def _market_theme(self, t, pal):
        t.setCellAccentColor(QColor(pal["accent"]))
        t.setCellMutedColor(QColor(pal["muted"]))
        t.setHeaderGlyphColor(QColor(pal["muted"]))
        t.setHeaderAccentColor(QColor(pal["accent"]))
        t.setRowSeparatorColor(QColor(pal["fieldBorder"]))

    def _on_cell(self, row, col):
        if col == 5:                                   # the "Trade" badge column
            print("[crypto] trade row", row)

    # -- promo card --------------------------------------------------------- #
    def _build_promo(self, comp, pal):
        comp.promoCard.setStyleSheet(
            "#promoCard{border-radius:22px; background:qlineargradient("
            "x1:0,y1:0,x2:1,y2:1, stop:0 %s, stop:0.55 %s, stop:1 %s);}"
            % (pal["promoTop"], pal["promoMid"], pal["promoBottom"]))
        comp.promoTitle.setStyleSheet(
            "color:%s; background:transparent; font-size:21px; font-weight:800;"
            % pal["promoText"])
        comp.promoSub.setStyleSheet(
            "color:%s; background:transparent; font-size:12px;" % pal["promoSubText"])
        comp.promoCoins.ringColor = QColor(pal["promoMid"])
        comp.promoCoins.setAvatars(D.PROMO_COINS)

    # -- trade card --------------------------------------------------------- #
    def _build_trade(self, comp, pal):
        coins = T.coins()
        card = T.card_icon_color(self._theme_name())
        comp.coinAvatar.bgColor = QColor(coins.get(D.TRADE_COIN_TICKER, pal["accent"]))
        comp.coinAvatar.setText("E")
        comp.amountBadge.bgColor = QColor(pal["accent"])
        comp.amountBadge.setText("$")
        comp.coinFieldChevron.setIcon(feather_icon("chevron-down", card, 16, stroke=2.4))
        comp.amountChevron.setIcon(feather_icon("chevron-down", card, 16, stroke=2.4))
        comp.promoCodeBtn.setIcon(feather_icon("chevron-right", pal["accent"], 15, stroke=2.4))
        comp.receivedValue.setStyleSheet(
            "color:%s; background:transparent; font-size:18px; font-weight:800;" % pal["accent"])
        comp.buyBtn.setStyleSheet(
            "QCustomQPushButton#buyBtn{background-color:%s; color:%s; border:0;"
            "border-radius:14px; font-size:15px; font-weight:800;}"
            "QCustomQPushButton#buyBtn:hover{background-color:%s;}"
            % (pal["accent"], pal["onAccent"], pal["accentHover"]))

    # -- interactions ------------------------------------------------------- #
    def _wire(self, comp):
        comp.tradeTabs.currentChanged.connect(self._on_trade_tab)

    def _on_trade_tab(self, idx):
        verb = D.TRADE_TABS[idx] if 0 <= idx < len(D.TRADE_TABS) else "Buy"
        self.comp.buyBtn.setText("%s %s" % (verb, D.TRADE_COIN_TICKER))

    def _on_rows(self, rows):
        # background loader delivered the market snapshot; merge colours + render
        pal = self._palette()
        merged = self._market_rows(pal)
        self.comp.marketTable.setData(merged)

    # -- theme recolour ----------------------------------------------------- #
    def recolor(self, pal):
        comp = self.comp
        self._build_overview(comp, pal)
        self._market_theme(comp.marketTable, pal)
        comp.marketTable.setColumns(self._market_columns(pal))
        comp.marketTable.setData(self._market_rows(pal))
        self._build_promo(comp, pal)
        self._build_trade(comp, pal)

    def teardown(self):
        try:
            self._worker.stop()
            self._thread.quit()
            self._thread.wait(1200)
        except Exception:
            pass


# --------------------------------------------------------------------------- #
# Orchestrator
# --------------------------------------------------------------------------- #
NAV_BUTTONS = list(D.NAV_ICONS.keys())


class GuiFunctions:
    def __init__(self, win):
        self.win = win
        self.ui = win.ui

    def initialize(self):
        ui = self.ui
        self.pages = {"navDashboard": ui.dashboardContainer}
        self.navButtons = {n: getattr(ui, n) for n in NAV_BUTTONS}
        self.managers = {"navDashboard": DashboardManager(self.win, ui.dashboardContainer)}

        for name, btn in self.navButtons.items():
            btn.clicked.connect(lambda _=False, n=name: self.navigateTo(n))

        # Collapsible rail: collapsedWidth must DIFFER from expandedWidth or the
        # slide animation is skipped. Starts collapsed (icon-only), toggles to
        # 230px to reveal the labels (QCustomSidebarButton shows labelText on
        # expand automatically). Wire the toggle ONCE.
        try:
            ui.sidebar.customizeQCustomSlideMenu(defaultWidth=84, collapsedWidth=84,
                                                 expandedWidth=230)
        except Exception:
            pass
        ui.sidebarToggle.clicked.connect(ui.sidebar.toggleMenu)
        # the brand wordmark is a plain QLabel, so hide it with the rail
        try:
            ui.sidebar.onCollapsed.connect(ui.brandName.hide)
            ui.sidebar.onExpanded.connect(ui.brandName.show)
            ui.brandName.hide()
        except Exception:
            pass

        ui.themeToggle.clicked.connect(self.toggleTheme)

        self.themeEngine = getattr(self.win, "themeEngine", None)
        if self.themeEngine is not None:
            try:
                self.themeEngine.onThemeChangeComplete.connect(self._onThemeReady)
            except Exception:
                pass
        self.win.toggleTheme = self.toggleTheme      # headless verification slot

        self._active = "navDashboard"
        self._paintChrome()
        self.navigateTo("navDashboard")

    # -- theme -------------------------------------------------------------- #
    def _currentTheme(self):
        return str(getattr(self.themeEngine, "theme", "") or T.THEME_LIGHT)

    def toggleTheme(self):
        if self.themeEngine is None:
            return
        target = T.THEME_DARK if T.is_light(self._currentTheme()) else T.THEME_LIGHT
        self.themeEngine.setTheme(target)            # by NAME; async icon regen

    def _onThemeReady(self):
        self._paintChrome()
        pal = T.chart_palette(self._currentTheme())
        for mgr in self.managers.values():
            try:
                mgr.recolor(pal)
            except Exception:
                pass

    def _paintChrome(self):
        theme = self._currentTheme()
        pal = T.chart_palette(theme)
        rail = T.rail_icon_color(theme)
        card = T.card_icon_color(theme)
        accent = pal["accent"]

        # dark floating rail (bg + label colours from palette — dark in BOTH themes)
        self.ui.sidebar.setStyleSheet(
            "#sidebar{background-color:%s; border-radius:26px;}"
            "#sidebar QCustomSidebarButton{color:%s;}"
            "#sidebar QCustomSidebarButton:checked{color:%s;}"
            "#sidebar #sidebarToggle{color:%s;}"
            "#sidebar #brandName{color:%s; background:transparent; font-size:17px; font-weight:800;}"
            % (pal["sidebarBg"], pal["sidebarText"], pal["onAccent"],
               pal["sidebarText"], pal["onAccent"]))
        self.ui.logoBtn.setStyleSheet(
            "#logoBtn{background-color:%s; border:0; border-radius:15px;}" % accent)
        self.ui.logoBtn.setIcon(feather_icon("trending-up", pal["onAccent"], 24, stroke=2.4))
        self.ui.sidebarToggle.setIcon(feather_icon("menu", rail, 20))

        # nav icons: idle = rail grey, active = white on the accent pill
        active = getattr(self, "_active", "navDashboard")
        for name, btn in self.navButtons.items():
            is_active = (name == active)
            if btn.isChecked() != is_active:
                btn.setChecked(is_active)              # re-assert (autoExclusive steals it)
            col = pal["onAccent"] if is_active else rail
            btn.setIcon(feather_icon(D.NAV_ICONS.get(name, "circle"), col, 22))

        # bottom rail utilities
        self.ui.themeToggle.setIcon(
            feather_icon("moon" if T.is_light(theme) else "sun", rail, 20))
        try:
            self.ui.themeToggle.labelText = "Dark mode" if T.is_light(theme) else "Light mode"
        except Exception:
            pass
        for obj in ("navDocs", "navSettings"):
            w = getattr(self.ui, obj, None)
            if w is not None:
                w.setIcon(feather_icon(D.NAV_ICONS.get(obj, "circle"), rail, 20))

        # top-bar user chip
        try:
            av = self.ui.dashboardContainer.component.userAvatar
            av.bgColor = QColor(accent)
            av.statusColor = QColor(pal["avatarNote"])
            self.ui.dashboardContainer.component.userChevron.setIcon(
                feather_icon("chevron-down", card, 16, stroke=2.4))
        except Exception:
            pass

    # -- navigation --------------------------------------------------------- #
    def navigateTo(self, name):
        self._active = name if name in self.pages else self._active
        page = self.pages.get(name)
        if page is not None:
            self.ui.pageStack.setCurrentWidget(page)
        # force exactly one active pill (autoExclusive ignores setChecked(False))
        for n, btn in self.navButtons.items():
            btn.setAutoExclusive(False)
            btn.setChecked(n == self._active)
            btn.setAutoExclusive(True)
        self._paintChrome()
        mgr = self.managers.get(self._active)
        if mgr is not None:
            mgr.onShown()
