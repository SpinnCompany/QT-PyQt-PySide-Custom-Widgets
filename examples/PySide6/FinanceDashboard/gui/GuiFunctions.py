"""Finance dashboard — GUI orchestration (the CORRECT Custom_Widgets way).

A single GuiFunctions orchestrator holds one Manager per page. The manager
reaches its embedded component via ``container.component`` and wires child
widgets by objectName. Runtime data, painted data-viz (credit cards, the
monthly bars, transaction rows, income/expense chips) and interactions live
here (and in a background worker), never in the .ui.

Colours for data-viz come from the token-driven ChartPalette in style.json, so
they flip when the theme switches. Theme switching goes through the icon
pipeline BY NAME (Finance Light / Finance Dark).
"""

import os

from qtpy.QtCore import QObject, QTimer, QByteArray, Qt, QThread
from qtpy.QtGui import QColor, QPainter, QPixmap, QIcon
from qtpy.QtWidgets import (QApplication, QFrame, QLabel, QWidget,
                            QVBoxLayout, QHBoxLayout)
from qtpy.QtSvg import QSvgRenderer

import Custom_Widgets
from Custom_Widgets.QCustomListRow import QCustomListRow

from gui import theme as T
from gui import data as D
from gui.workers import ClockWorker

_ICON_DIR = os.path.join(os.path.dirname(Custom_Widgets.__file__), "Qss", "icons", "feather")
_PM_CACHE = {}

NAV_ICONS = {
    "dashboard": "home", "activity": "list",
    "cards": "credit-card", "settings": "settings",
}


def feather_pixmap(name, color, size=22, stroke=2.2):
    key = (name, color, size, stroke)
    if key in _PM_CACHE:
        return _PM_CACHE[key]
    path = os.path.join(_ICON_DIR, name + ".svg")
    pm = QPixmap(int(size * 2), int(size * 2))
    pm.fill(QColor(0, 0, 0, 0))
    if os.path.exists(path):
        svg = open(path, "r", encoding="utf-8").read()
        svg = svg.replace('stroke="#ffffff"', 'stroke="%s"' % color)
        svg = svg.replace('stroke="#000000"', 'stroke="%s"' % color)
        svg = svg.replace('stroke-width="3"', 'stroke-width="%s"' % stroke)
        r = QSvgRenderer(QByteArray(svg.encode("utf-8")))
        p = QPainter(pm)
        p.setRenderHint(QPainter.Antialiasing, True)
        r.render(p)
        p.end()
    pm.setDevicePixelRatio(2.0)
    _PM_CACHE[key] = pm
    return pm


def feather_icon(name, color, size=22, stroke=2.2):
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
            QTimer.singleShot(80, self.onShown)   # container loads async on first show
            return
        try:
            self.setup(comp)
            self._loaded = True
        except Exception as e:
            import traceback
            print("[finance] %s setup failed: %s" % (type(self).__name__, e))
            traceback.print_exc()

    def setup(self, comp):
        pass

    def recolor(self, palette):
        pass

    def _theme_name(self):
        eng = getattr(self.win, "themeEngine", None)
        return str(getattr(eng, "theme", "") or T.THEME_LIGHT)

    def _palette(self):
        return T.chart_palette(self._theme_name())


# --------------------------------------------------------------------------- #
# small painted helpers
# --------------------------------------------------------------------------- #
def _dot(color, active, d=8):
    lbl = QLabel()
    w = 22 if active else d
    lbl.setFixedSize(w, d)
    lbl.setStyleSheet("background:%s; border-radius:%dpx;" % (color, d // 2))
    return lbl


# --------------------------------------------------------------------------- #
# Dashboard manager
# --------------------------------------------------------------------------- #
class DashboardManager(PageManager):
    def setup(self, comp):
        self.comp = comp
        pal = self._palette()
        self._build_cards(comp, pal)
        self._build_balance(comp, pal)
        self._build_summary(comp, pal)
        self._build_bars(comp, pal)
        self._build_transactions(comp, pal)
        self._build_dots(comp, pal)
        self._style_buttons(comp, pal)

        # Background worker: Worker -> Signal -> GUI (queued to the GUI thread).
        self._thread = QThread(self.win)
        self._worker = ClockWorker()
        self._worker.moveToThread(self._thread)
        self._thread.started.connect(self._worker.run)
        self._worker.tick.connect(self._on_clock)
        self._thread.start()
        QApplication.instance().aboutToQuit.connect(self.teardown)

    # -- credit cards (QCustomPaymentCard) --------------------------------- #
    def _build_cards(self, comp, pal):
        comp.blueCard.setVariant("gradient")
        comp.blueCard.setColors(pal["cardTop"], pal["cardBottom"])
        comp.blueCard.textColor = QColor("#ffffff")
        comp.greyCard.setVariant("flat")
        comp.greyCard.flatColor = QColor(pal["greyCard"])
        comp.greyCard.textColor = QColor(pal["greyCardText"])
        comp.addCardBtn.setIcon(feather_icon("plus", pal["accent"], 20))

    # -- balance income / expense chips (QCustomTrendChip) ----------------- #
    def _build_balance(self, comp, pal):
        comp.incomeChip.upColor = QColor(pal["up"])
        comp.incomeChip.setDirection("up")
        comp.expenseChip.downColor = QColor(pal["down"])
        comp.expenseChip.setDirection("down")
        comp.lastMonthBtn.setIcon(feather_icon("chevron-down", pal["accent"], 16, stroke=2.6))

    # -- monthly summary money --------------------------------------------- #
    def _build_summary(self, comp, pal):
        comp.sumIncomeValue.setStyleSheet("color:%s; background:transparent; font-size:19px; font-weight:800;" % pal["up"])
        comp.sumExpenseValue.setStyleSheet("color:%s; background:transparent; font-size:19px; font-weight:800;" % pal["down"])
        comp.generateReportBtn.setProperty("role", "link")

    # -- bar chart (QCustomMiniBarChart, per-bar colour + highlight) ------- #
    def _build_bars(self, comp, pal):
        vals = [frac * 100 for _d, frac, _k in D.MONTH_BARS]
        labels = [day for day, _f, _k in D.MONTH_BARS]
        colors = [pal[key] for _d, _f, key in D.MONTH_BARS]
        comp.barsChart.setData(vals, colors, labels)
        comp.barsChart.labelColor = QColor("#8b909e")
        # exercise the highlight API on the one "active" (green) bar
        for i, (_d, _f, key) in enumerate(D.MONTH_BARS):
            if key == "barActive":
                comp.barsChart.highlightIndex(i, pal["barActive"])

    # -- transaction rows (QCustomListRow) --------------------------------- #
    def _build_transactions(self, comp, pal):
        self._rows = []
        body = comp.txnBody.layout()
        col = T.icon_color(self._theme_name())
        for icon, name, cat, amount, date, sign in D.TRANSACTIONS:
            row = QCustomListRow(title=name, subtitle=cat, value=amount, meta=date)
            row.chipColor = QColor(pal["chipBg"])
            row.chipTextColor = QColor(pal["accent"])
            row.subtitleColor = QColor(pal["accent"])
            if sign == "pos":
                row.valueColor = QColor(pal["up"])
            row.setIcon(feather_pixmap(icon, col, 18, stroke=2.2))
            self._rows.append((row, icon, sign))
            body.addWidget(row)

    # -- carousel dots (QCustomPageDots) ----------------------------------- #
    def _build_dots(self, comp, pal):
        for dots, (count, active) in ((comp.cardsDots, D.CARD_DOTS),
                                      (comp.summaryDots, D.SUMMARY_DOTS)):
            dots.setCount(count)
            dots.setActiveIndex(active)
            dots.setColors(pal["barIdle"], pal["accent"])

    # -- action buttons ---------------------------------------------------- #
    def _style_buttons(self, comp, pal):
        # QCustomQPushButton variant QSS is styled by objectName in chrome.scss;
        # nothing token-specific needed here.
        pass

    # -- live clock -------------------------------------------------------- #
    def _on_clock(self, text):
        try:
            self.comp.clockLabel.setText(text)
        except Exception:
            pass

    # -- theme recolour ---------------------------------------------------- #
    def recolor(self, pal):
        comp = self.comp
        self._build_cards(comp, pal)
        self._build_balance(comp, pal)
        self._build_summary(comp, pal)
        # mini bar chart re-hues from the palette
        comp.barsChart.setBarColors([pal[key] for _d, _f, key in D.MONTH_BARS])
        # page dots
        for dots in (comp.cardsDots, comp.summaryDots):
            dots.setColors(pal["barIdle"], pal["accent"])
        # transaction rows
        col = T.icon_color(self._theme_name())
        for row, icon, sign in getattr(self, "_rows", []):
            row.chipColor = QColor(pal["chipBg"])
            row.chipTextColor = QColor(pal["accent"])
            row.subtitleColor = QColor(pal["accent"])
            if sign == "pos":
                row.valueColor = QColor(pal["up"])
            row.setIcon(feather_pixmap(icon, col, 18, stroke=2.2))

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
class GuiFunctions:
    def __init__(self, win):
        self.win = win
        self.ui = win.ui

    def initialize(self):
        ui = self.ui
        self.pages = {"dashboard": ui.dashboardContainer}
        self.navButtons = {
            "dashboard": ui.navDashboard, "activity": ui.navActivity,
            "cards": ui.navCards, "settings": ui.navSettings,
        }
        self.managers = {"dashboard": DashboardManager(self.win, ui.dashboardContainer)}

        for name, btn in self.navButtons.items():
            btn.clicked.connect(lambda _=False, n=name: self.navigateTo(n))

        # Collapse/expand the sidebar — wired ONCE (deterministic).
        ui.sidebarToggle.clicked.connect(ui.sidebar.toggleMenu)
        # Hide the avatar name when the sidebar is collapsed (icon-only).
        try:
            ui.sidebar.onCollapsed.connect(lambda: ui.avatarName.hide())
            ui.sidebar.onExpanded.connect(lambda: ui.avatarName.show())
            ui.avatarName.hide()   # start collapsed
        except Exception:
            pass

        # Theme toggle button in the sidebar.
        ui.themeToggle.clicked.connect(self.toggleTheme)

        self.themeEngine = getattr(self.win, "themeEngine", None)
        if self.themeEngine is not None:
            try:
                self.themeEngine.onThemeChangeComplete.connect(self._onThemeReady)
            except Exception:
                pass
        # expose a slot for headless theme-flip verification
        self.win.toggleTheme = self.toggleTheme

        self._paintChrome()
        self.navigateTo("dashboard")

    # -- theme ------------------------------------------------------------- #
    def _currentTheme(self):
        return str(getattr(self.themeEngine, "theme", "") or T.THEME_LIGHT)

    def toggleTheme(self):
        if self.themeEngine is None:
            return
        target = T.THEME_DARK if T.is_light(self._currentTheme()) else T.THEME_LIGHT
        self.themeEngine.setTheme(target)

    def _onThemeReady(self):
        self._paintChrome()
        pal = T.chart_palette(self._currentTheme())
        for mgr in self.managers.values():
            try:
                mgr.recolor(pal)
            except Exception:
                pass

    def _accent(self):
        return T.chart_palette(self._currentTheme()).get("accent", "#3355e8")

    def _paintChrome(self):
        theme = self._currentTheme()
        col = T.icon_color(theme)
        accent = self._accent()
        # Re-assert the active nav (theme/sidebar toggles can steal the checked
        # state); keeps the indicator on the current page.
        active = getattr(self, "_active", "dashboard")
        for name, btn in self.navButtons.items():
            is_active = (name == active)
            if btn.isChecked() != is_active:
                btn.setChecked(is_active)
            icon_col = accent if is_active else col
            btn.setIcon(feather_icon(NAV_ICONS.get(name, "circle"), icon_col, 22))
        try:
            self.ui.sidebarToggle.setIcon(feather_icon("menu", col, 22))
            self.ui.navAdd.setIcon(feather_icon("plus", col, 20))
        except Exception:
            pass
        # theme-toggle button (moon in light / sun in dark)
        try:
            light = T.is_light(theme)
            self.ui.themeToggle.setIcon(feather_icon("moon" if light else "sun", col, 20))
            self.ui.themeToggle.labelText = "Dark mode" if light else "Light mode"
        except Exception:
            pass
        # avatar widget (accent circle + notification dot ringed by the sidebar bg)
        try:
            av = self.ui.sidebarAvatar
            av.bgColor = QColor(accent)
            av.statusColor = QColor(T.chart_palette(theme).get("avatarNote", "#f2704e"))
            av.statusBorderColor = QColor(self._sidebar_bg(theme))
            self.ui.avatarName.setStyleSheet(
                "color:%s; background:transparent; font-size:13px; font-weight:600;"
                % col)
        except Exception:
            pass

    def _sidebar_bg(self, theme):
        return "#ffffff" if T.is_light(theme) else "#12141c"

    # -- navigation -------------------------------------------------------- #
    def navigateTo(self, name):
        self._active = name
        page = self.pages.get(name)
        if page is not None:
            self.ui.pageStack.setCurrentWidget(page)
        for n, btn in self.navButtons.items():
            btn.setChecked(n == name)
        self._paintChrome()
        mgr = self.managers.get(name)
        if mgr is not None:
            mgr.onShown()
