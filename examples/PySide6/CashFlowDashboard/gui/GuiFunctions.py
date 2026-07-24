"""Cash Flow dashboard — GUI orchestration (the CORRECT Custom_Widgets way).

A single GuiFunctions orchestrator holds one Manager per page. The manager
reaches its embedded component via ``container.component`` and wires child
widgets by objectName. Runtime data + painted data-viz (the teal balance
banner, the diverging cash-flow bar chart, income/expense/KPI deltas, activity
rows, the credit card) live here (and in a background worker), never in the .ui.

Colours come from the token-driven ChartPalette in style.json, so they flip
when the theme switches. Theme switching goes through the icon pipeline BY NAME
(Cashflow Light / Cashflow Dark).
"""

import os

from qtpy.QtCore import QObject, QTimer, QByteArray, Qt, QThread
from qtpy.QtGui import QColor, QPainter, QPixmap, QIcon, QBrush, QPen
from qtpy.QtWidgets import (QApplication, QFrame, QLabel, QWidget,
                            QVBoxLayout, QHBoxLayout, QSizePolicy)
from qtpy.QtSvg import QSvgRenderer

import Custom_Widgets
from Custom_Widgets.QCustomMenu import QCustomMenu
from Custom_Widgets.QCustomModal import QCustomModal

from gui import theme as T
from gui import data as D
from gui.workers import ClockWorker

_ICON_DIR = os.path.join(os.path.dirname(Custom_Widgets.__file__), "Qss", "icons", "feather")
_PM_CACHE = {}

NAV_ICONS = {
    "dashboard": "grid", "activity": "list",
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


def _clear_layout(lay):
    if lay is None:
        return
    while lay.count():
        it = lay.takeAt(0)
        w = it.widget()
        if w is not None:
            w.setParent(None)
            w.deleteLater()


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
            print("[cashflow] %s setup failed: %s" % (type(self).__name__, e))
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
# Dashboard manager
# --------------------------------------------------------------------------- #
class DashboardManager(PageManager):
    def setup(self, comp):
        self.comp = comp
        pal = self._palette()
        self._build_banner(comp, pal)
        self._build_chart(comp, pal)
        self._build_side(comp, pal)
        self._build_kpis(comp, pal)
        self._build_activity(comp, pal)
        self._build_card(comp, pal)
        self._build_headicons(comp, pal)
        self._build_popups(comp, pal)

        # Background worker: Worker -> Signal -> GUI (queued to the GUI thread).
        self._thread = QThread(self.win)
        self._worker = ClockWorker()
        self._worker.moveToThread(self._thread)
        self._thread.started.connect(self._worker.run)
        self._worker.tick.connect(self._on_clock)
        self._thread.start()
        QApplication.instance().aboutToQuit.connect(self.teardown)

    # -- small painted helpers -------------------------------------------- #
    def _icon_tile(self, label, bg, fg, icon_name, glyph=20, radius=12):
        label.setStyleSheet("background:%s; border-radius:%dpx;" % (bg, radius))
        label.setPixmap(feather_pixmap(icon_name, fg, glyph, 2.2))
        label.setAlignment(Qt.AlignCenter)

    def _delta(self, holder, pct, direction, color):
        """Fill a placeholder QWidget with 'NN% ↗' — coloured %+arrow icon."""
        # the holder is a native QWidget (paints the palette bg = a white/dark
        # box); force it transparent so only the coloured text+arrow show
        # (matters on the teal banner where a white box would be visible).
        holder.setStyleSheet("background: transparent;")
        holder.setAttribute(Qt.WA_TranslucentBackground, True)
        lay = holder.layout()
        _clear_layout(lay)
        val = QLabel(pct)
        val.setStyleSheet("background:transparent; color:%s; font-size:13px; "
                          "font-weight:700;" % color)
        arrow = QLabel()
        arrow.setFixedSize(14, 14)
        arrow.setAlignment(Qt.AlignCenter)
        arrow.setPixmap(feather_pixmap(
            "arrow-up-right" if direction == "up" else "arrow-down-right",
            color, 13, 2.6))
        lay.addWidget(val)
        lay.addWidget(arrow)

    # -- teal balance banner (painted gradient + light-on-teal buttons) --- #
    def _build_banner(self, comp, pal):
        comp.banner.setStyleSheet(
            "QFrame#banner{ background: qlineargradient(x1:0,y1:0,x2:1,y2:0,"
            " stop:0 %s, stop:1 %s); border-radius:20px; }" % (pal["bannerTop"], pal["bannerBottom"]))
        comp.bannerTitle.setStyleSheet(
            "background:transparent; color:%s; font-size:13px; font-weight:600;" % pal["bannerMuted"])
        comp.bannerValue.setStyleSheet(
            "background:transparent; color:%s; font-size:34px; font-weight:800;" % pal["bannerText"])
        self._delta(comp.bannerDelta, D.BALANCE["delta"], D.BALANCE["dir"], pal["cardStrip"])
        comp.bannerValue.setText(D.BALANCE["value"])

        # action buttons — light-on-teal (painted here, not in scss)
        prim = ("QPushButton{ background:%s; color:%s; border:0; border-radius:12px;"
                " font-size:14px; font-weight:700; padding:0 16px; }"
                "QPushButton:hover{ background:%s; }") % (
                    pal["accent"], pal["accentText"], pal["cardStrip"])
        ghost = ("QPushButton{ background:rgba(255,255,255,0.10); color:#ffffff;"
                 " border:0; border-radius:12px; font-size:14px; font-weight:600;"
                 " padding:0 14px; } QPushButton:hover{ background:rgba(255,255,255,0.20); }")
        comp.addBtn.setStyleSheet(prim)
        comp.addBtn.setIcon(feather_icon("plus", pal["accentText"], 16, 2.6))
        for btn, ic in ((comp.sendBtn, "arrow-up-right"),
                        (comp.requestBtn, "refresh-cw"),
                        (comp.moreBtn, "more-horizontal")):
            btn.setStyleSheet(ghost)
            btn.setIcon(feather_icon(ic, "#ffffff", 16, 2.2))

    # -- diverging cash-flow chart (QCustomDivergingBarChart) -------------- #
    def _build_chart(self, comp, pal):
        # One painted widget: income up (dark teal), expense down (green),
        # split across a zero axis with a gap between + and - bars. Values are
        # in €K; the widget draws the faint grid + €K axis labels itself.
        ch = comp.cashChart
        ch.setData(D.CASHFLOW_INCOME, D.CASHFLOW_EXPENSE, D.CASHFLOW_LABELS)
        ch.setColors(pal["barIncome"], pal["barExpense"])
        ch.gridColor = QColor(pal["gridLine"])
        ch.axisTextColor = QColor(pal["muted"])
        ch.axisPrefix = "€"
        ch.axisSuffix = "K"

    # -- income / expense side panel -------------------------------------- #
    def _build_side(self, comp, pal):
        self._icon_tile(comp.incIcon, pal["kpiIconBg"], pal["kpiIconFg"], "arrow-down-left")
        self._icon_tile(comp.expIcon, pal["kpiIconBg"], pal["kpiIconFg"], "arrow-up-right")
        for key, label, value, pct, direction, _ic in D.CASHFLOW_SIDE:
            if key == "income":
                comp.incValue.setText(value)
                self._delta(comp.incDelta, pct, direction, pal["pos"])
            else:
                comp.expValue.setText(value)
                self._delta(comp.expDelta, pct, direction, pal["neg"])

    # -- KPI cards -------------------------------------------------------- #
    def _build_kpis(self, comp, pal):
        tiles = [comp.kpiIcon0, comp.kpiIcon1, comp.kpiIcon2]
        titles = [comp.kpiTitle0, comp.kpiTitle1, comp.kpiTitle2]
        values = [comp.kpiValue0, comp.kpiValue1, comp.kpiValue2]
        deltas = [comp.kpiDelta0, comp.kpiDelta1, comp.kpiDelta2]
        subs = [comp.kpiSub0, comp.kpiSub1, comp.kpiSub2]
        for i, (icon, title, value, pct, direction, sub) in enumerate(D.KPIS):
            self._icon_tile(tiles[i], pal["kpiIconBg"], pal["kpiIconFg"], icon)
            titles[i].setText(title)
            values[i].setText(value)
            subs[i].setText(sub)
            self._delta(deltas[i], pct, direction, pal["pos"] if direction == "up" else pal["neg"])

    # -- recent-activity rows (built in code) ----------------------------- #
    def _build_activity(self, comp, pal):
        body = comp.activityBody.layout()
        _clear_layout(body)
        for icon, name, typ, date, amount, sub, status, method, last4, sign in D.ACTIVITY:
            body.addWidget(self._activity_row(pal, icon, name, typ, date, amount,
                                              sub, status, method, last4, sign))

    def _activity_row(self, pal, icon, name, typ, date, amount, sub, status, method, last4, sign):
        row = QWidget()
        lay = QHBoxLayout(row)
        lay.setContentsMargins(4, 8, 4, 8)
        lay.setSpacing(12)

        tile = QLabel()
        tile.setFixedSize(40, 40)
        self._icon_tile(tile, pal["kpiIconBg"], pal["kpiIconFg"], icon)
        lay.addWidget(tile)

        who = QVBoxLayout(); who.setSpacing(2)
        who.addWidget(self._rlbl(name, "rowStrong"))
        who.addWidget(self._rlbl("%s · %s" % (typ, date), "rowMuted"))
        lay.addLayout(who)
        lay.addStretch(1)

        amt = QVBoxLayout(); amt.setSpacing(2)
        amt.addWidget(self._rlbl(amount, "rowStrong"))
        amt.addWidget(self._rlbl(sub, "rowMuted"))
        lay.addWidget(self._wrap(amt, 150))

        pill = self._rlbl(status, "pillSuccess" if status.lower() == "success" else "pillPending")
        pill.setAlignment(Qt.AlignCenter)
        pillw = QWidget(); pl = QHBoxLayout(pillw); pl.setContentsMargins(0, 0, 0, 0)
        pl.addWidget(pill); pl.addStretch(1)
        pillw.setFixedWidth(110)
        lay.addWidget(pillw)

        meth = QVBoxLayout(); meth.setSpacing(2)
        meth.addWidget(self._rlbl(method, "rowMethod"))
        meth.addWidget(self._rlbl("**** %s" % last4, "rowMuted"))
        lay.addWidget(self._wrap(meth, 150))
        return row

    def _rlbl(self, text, role):
        """Label coloured by an app-QSS role (auto-flips with the theme)."""
        w = QLabel(text)
        w.setProperty("role", role)
        return w

    def _wrap(self, layout, width):
        w = QWidget(); w.setFixedWidth(width)
        layout.setContentsMargins(0, 0, 0, 0)
        w.setLayout(layout)
        return w

    # -- credit cards (interactive stack) --------------------------------- #
    def _build_card(self, comp, pal):
        stack = comp.cardStack
        grads = pal.get("cardGradients") or [[pal["cardTop"], pal["cardBottom"]]]
        if getattr(self, "_cards_built", False):
            stack.setCardColorsList(grads)                          # recolour, keep index
            return
        else:
            self._cards_built = True
            stack.setCards([
                dict(brand=c["brand"], amount=c["amount"], number=c["number"],
                     top=grads[i % len(grads)][0], bottom=grads[i % len(grads)][1],
                     fullNumber=c["fullNumber"])
                for i, c in enumerate(D.MY_CARDS)
            ])

    # -- popup menu (…/more buttons) + modal ------------------------------ #
    def _build_popups(self, comp, pal):
        if not hasattr(self, "_menu"):
            self._menu = QCustomMenu(self.win)
            self._menu.triggered.connect(self._on_menu)
            self._activityMenu = QCustomMenu(self.win)
            self._activityMenu.triggered.connect(self._on_menu)
            self._modal = QCustomModal(self.win)
            self._modal.triggered.connect(self._on_modal)
            # wire the …/more/Send buttons ONCE
            comp.moreBtn.clicked.connect(lambda: self._menu.popupAt(comp.moreBtn, "right"))
            comp.activityMore.clicked.connect(lambda: self._activityMenu.popupAt(comp.activityMore, "right"))
            comp.sendBtn.clicked.connect(self._open_send_modal)
        self._theme_popups(pal)

    def _theme_popups(self, pal):
        icol = T.icon_color(self._theme_name())
        for m in (self._menu, self._activityMenu):
            m.applyColors(bg=pal["popupBg"], text=pal["text"], muted=pal["muted"],
                          hover=pal["popupHover"], border=pal["popupBorder"],
                          accent=pal["accent"], danger=pal["neg"])
        self._menu.clear()
        for icon, label, key, danger in D.MORE_MENU:
            if icon == "__sep__":
                self._menu.addSeparator()
            else:
                self._menu.addAction(label, key, feather_icon(icon, pal["neg"] if danger else icol, 17), danger=danger)
        self._activityMenu.clear()
        for icon, label, key, _d in D.ACTIVITY_MENU:
            self._activityMenu.addAction(label, key, feather_icon(icon, icol, 17))
        self._modal.applyColors(bg=pal["popupBg"], text=pal["text"], muted=pal["muted"],
                                border=pal["popupBorder"], accent=pal["accent"],
                                accentText=pal["accentText"], hover=pal["popupHover"])

    def _modal_line(self, label, value, pal):
        w = QWidget()
        h = QHBoxLayout(w); h.setContentsMargins(0, 0, 0, 0)
        h.addWidget(self._lbl(label, pal["muted"], 13, 500))
        h.addStretch(1)
        h.addWidget(self._lbl(value, pal["text"], 14, 700))
        return w

    def _lbl(self, text, color, size, weight):
        w = QLabel(text)
        w.setStyleSheet("background:transparent; color:%s; font-size:%dpx; font-weight:%d;"
                        % (color, size, weight))
        return w

    def _open_send_modal(self):
        pal = self._palette()
        m = self._modal
        m.clearContent(); m.clearActions()       # drop the seeded demo defaults
        m.setTitle("Send money")
        m.setSubtitle("Transfer to a saved payee")
        m.addContent(self._modal_line("Payee", "Isabella Garcia · **** 6120", pal))
        m.addContent(self._modal_line("From", "VISA · **** 2104", pal))
        m.addContent(self._modal_line("Amount", "€ 1.250,00", pal))
        m.addAction("Cancel", "cancel")
        m.addAction("Send now", "send", primary=True)
        m.showModal()

    def _on_menu(self, key):
        # a real app would route here; keep the demo visible via the clock line
        try:
            self.comp.clockLabel.setText("Menu action: %s" % key)
        except Exception:
            pass

    def _on_modal(self, key):
        try:
            self.comp.clockLabel.setText("Modal action: %s" % key)
        except Exception:
            pass

    # -- header glyph icons ----------------------------------------------- #
    def _build_headicons(self, comp, pal):
        col = pal["accent"]
        comp.cashIcon.setPixmap(feather_pixmap("bar-chart-2", col, 18, 2.4))
        comp.activityIcon.setPixmap(feather_pixmap("activity", col, 18, 2.4))
        comp.cardsIcon.setPixmap(feather_pixmap("credit-card", col, 18, 2.4))
        icol = T.icon_color(self._theme_name())
        comp.moreBtn.setText("")
        comp.activityMore.setIcon(feather_icon("more-horizontal", icol, 18))
        comp.filterBtn.setIcon(feather_icon("filter", icol, 15))
        comp.sortBtn.setIcon(feather_icon("bar-chart", icol, 15))

    # -- live clock ------------------------------------------------------- #
    def _on_clock(self, text):
        try:
            self.comp.clockLabel.setText(text)
        except Exception:
            pass

    # -- theme recolour --------------------------------------------------- #
    def recolor(self, pal):
        comp = self.comp
        self._build_banner(comp, pal)
        self._build_chart(comp, pal)
        self._build_side(comp, pal)
        self._build_kpis(comp, pal)
        self._build_activity(comp, pal)
        self._build_card(comp, pal)
        self._build_headicons(comp, pal)
        self._theme_popups(pal)

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

        ui.sidebarToggle.clicked.connect(ui.sidebar.toggleMenu)
        try:
            ui.sidebar.onCollapsed.connect(lambda: ui.avatarName.hide())
            ui.sidebar.onExpanded.connect(lambda: ui.avatarName.show())
            ui.avatarName.hide()
        except Exception:
            pass

        ui.themeToggle.clicked.connect(self.toggleTheme)

        self.themeEngine = getattr(self.win, "themeEngine", None)
        if self.themeEngine is not None:
            try:
                self.themeEngine.onThemeChangeComplete.connect(self._onThemeReady)
            except Exception:
                pass
        self.win.toggleTheme = self.toggleTheme

        self._paintChrome()
        self.navigateTo("dashboard")

    # -- theme ------------------------------------------------------------ #
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
                import traceback
                traceback.print_exc()

    def _accent(self):
        return T.chart_palette(self._currentTheme()).get("accent", "#16a34a")

    def _paintChrome(self):
        theme = self._currentTheme()
        col = T.icon_color(theme)
        accent = self._accent()
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
        try:
            light = T.is_light(theme)
            self.ui.themeToggle.setIcon(feather_icon("moon" if light else "sun", col, 20))
            self.ui.themeToggle.labelText = "Dark mode" if light else "Light mode"
        except Exception:
            pass
        try:
            av = self.ui.sidebarAvatar
            av.bgColor = QColor(accent)
            av.statusColor = QColor(T.chart_palette(theme).get("neg", "#e5484d"))
            av.statusBorderColor = QColor(T.shell_bg(theme))
            self.ui.avatarName.setStyleSheet(
                "color:%s; background:transparent; font-size:13px; font-weight:600;" % col)
        except Exception:
            pass

    # -- navigation ------------------------------------------------------- #
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
