"""Aurora Jobs — GUI orchestration (the CORRECT architecture).

A single GuiFunctions orchestrator owns nav + theming and holds one Manager per
page. The JobsManager reaches its embedded component via ``container.component``
and configures the library widgets that Designer cannot set (DataTable columns,
Toolbar statuses) IN CODE — exactly like charts. All colours come from
json-styles/style.json (theme roles + StatusPalette + Brand), never hard-coded,
and are re-applied on ``themeEngine.onThemeChangeComplete`` so a theme switch
recolours the delegate/toolbar too. Data lives in gui/data.py; the rows arrive
from a background Worker->Signal->GUI loader.
"""

import os

from qtpy.QtCore import QObject, Qt, QByteArray, QThread, QTimer
from qtpy.QtGui import QColor, QPainter, QPixmap, QIcon
from qtpy.QtWidgets import QApplication
from qtpy.QtSvg import QSvgRenderer

import Custom_Widgets
from Custom_Widgets.QCustomDataTable import DataTableColumn

from gui import theme as T
from gui import data as D
from gui.workers import JobsLoaderWorker

_ICON_DIR = os.path.join(os.path.dirname(Custom_Widgets.__file__), "Qss", "icons", "feather")
_PM_CACHE = {}

RAIL_ICONS = [
    ("navWork", "briefcase"), ("navCalendar", "calendar"), ("navClock", "clock"),
    ("navUsers", "users"), ("navInvoice", "file-text"), ("navNote", "edit-3"),
    ("navBox", "archive"), ("navChart", "bar-chart-2"), ("navSettings", "settings"),
]


def feather_pixmap(name, color, size=20):
    key = (name, color, size)
    if key in _PM_CACHE:
        return _PM_CACHE[key]
    path = os.path.join(_ICON_DIR, name + ".svg")
    pm = QPixmap(int(size * 2), int(size * 2))
    pm.setDevicePixelRatio(2)
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


def _rgba(color, alpha):
    c = QColor(color)
    return "rgba(%d,%d,%d,%.3f)" % (c.red(), c.green(), c.blue(), alpha)


# --------------------------------------------------------------------------- #
# Jobs page manager
# --------------------------------------------------------------------------- #
class JobsManager(QObject):
    def __init__(self, win, container):
        super().__init__(win)
        self.win = win
        self.container = container
        self._loaded = False
        self._thread = None
        self._worker = None

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

    # -- build ------------------------------------------------------------- #
    def setup(self, comp):
        self.comp = comp
        self.toolbar = comp.tableToolbar
        self.table = comp.jobsTable
        pal = T.status_palette()

        # Add-job button: white plus glyph on the accent fill (styled in chrome.scss)
        comp.addJobBtn.setIcon(feather_icon("plus", T.brand().get("railText", "#ffffff"), 16))

        # -- toolbar (statuses + chips come from data.py; hues from StatusPalette)
        self.toolbar.setSearchPlaceholder("Search jobs")
        self.toolbar.setFilterChips(
            [{"key": k, "label": l, "value": v} for k, l, v in D.FILTER_CHIPS])
        self.toolbar.setStatuses(
            [{"key": k, "label": l, "count": c, "color": pal.get(k, "#888888")}
             for k, l, c in D.STATUSES])

        # -- data table: configure columns IN CODE (Designer can't set these) --
        self.table.customizeQCustomDataTable(
            columns=self._columns(pal), selectable=True,
            showPagination=False, alternatingRowColors=False)
        self.table.setRowActions(D.ROW_ACTIONS)
        self.table.view().verticalHeader().setDefaultSectionSize(72)
        self.table.setStatusDotSize(9)
        self.table.setPersistentSortIndicators(True)
        self.table.setHeaderSelectCaret(True)
        self.table.setHeaderActionsGlyph("gear")
        self.table.setFlexMinWidth(150)                 # ASSIGNED TO never collapses
        for i, w in enumerate((168, 90, 90, 168, 192, 132, 160), start=1):
            self.table.view().setColumnWidth(i, w)

        # -- wire intent -------------------------------------------------- #
        self.toolbar.searchChanged.connect(self.table.setFilterText)
        self.toolbar.clearFiltersClicked.connect(self._onClearFilters)
        self.table.rowActionTriggered.connect(
            lambda row, key: print("[aurora] row action:", key, "row", row))

        self._applyThemeColors()

        # -- rows arrive from a background loader (Worker -> Signal -> GUI) --
        self._thread = QThread(self.win)
        self._worker = JobsLoaderWorker(count=14)
        self._worker.moveToThread(self._thread)
        self._thread.started.connect(self._worker.run)
        self._worker.rowsLoaded.connect(self._onRowsLoaded)
        self._thread.start()
        QApplication.instance().aboutToQuit.connect(self.teardown)

    def _columns(self, pal):
        green = pal.get("jobLink", "#22c55e")
        sched = pal.get("scheduleTime", "#f97316")
        return [
            DataTableColumn("job", title="JOB", renderer="status",
                            colorMap={j: green for j in D.GREEN_JOBS}),
            DataTableColumn("invoiced", title="INVOICED"),
            DataTableColumn("amount", title="AMOUNT", type="number",
                            renderer="currency", align=Qt.AlignLeft,
                            formatter=lambda v: "$%d" % v),
            DataTableColumn("customer", title="CUSTOMER"),
            DataTableColumn("site", title="SITE", renderer="twoline",
                            subtitleKey="site2", subtitleScale=-1),
            DataTableColumn("due", title="DUE DATE"),
            DataTableColumn("scheduled", title="SCHEDULED", renderer="twoline",
                            subtitleKey="scheduled2", color=sched, subtitleScale=0),
            DataTableColumn("assigned", title="ASSIGNED TO"),
        ]

    def _onRowsLoaded(self, rows):
        self.table.setData(rows)

    def _onClearFilters(self):
        self.toolbar.clearFilterChips()
        self.toolbar.setActiveStatus(self.toolbar.ALL_KEY)
        self.table.setFilterText("")

    # -- theme colours (delegate + toolbar track the active theme) --------- #
    def _applyThemeColors(self):
        r = T.roles(self._theme_name())
        self.table.setCellAccentColor(r["accent"])
        self.table.setCellMutedColor(r["muted"])
        self.table.setActionsColor(r["muted"])
        self.table.setHeaderGlyphColor(r["muted"])
        self.table.setHeaderAccentColor(r["accent"])
        self.toolbar.setThemeColors(surface=r["surface"], on_surface=r["text"],
                                    muted=r["muted"], outline=r["outline"],
                                    accent=r["accent"])

    def recolor(self):
        if self._loaded:
            self._applyThemeColors()

    def _theme_name(self):
        eng = getattr(self.win, "themeEngine", None)
        return str(getattr(eng, "theme", "") or T.THEME_LIGHT)

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
        # Pin the icon rail to 72px. QCustomSidebar starts at its 300px default;
        # collapse it to 72. NOTE: the width animation is SKIPPED when
        # collapsedWidth == expandedWidth, so expandedWidth must differ (240) for
        # the collapse to actually resize. defaultWidth=72 makes it start collapsed.
        rail = ui.railBar
        rail.customizeQCustomSlideMenu(defaultWidth=72, collapsedWidth=72, expandedWidth=240)

        def _pin_rail():
            rail.setMinimumWidth(72)
            rail.setMaximumWidth(72)
        QTimer.singleShot(600, _pin_rail)

        self.pages = {"jobs": ui.jobsContainer}
        self.railButtons = {name: getattr(ui, name) for name, _ in RAIL_ICONS}
        self.managers = {"jobs": JobsManager(self.win, ui.jobsContainer)}

        for name, btn in self.railButtons.items():
            btn.clicked.connect(lambda _=False, n=name: self.navigateTo(n))

        # avatar doubles as the light/dark toggle (matches the reference chrome)
        self.themeEngine = getattr(self.win, "themeEngine", None)
        ui.avatar.clicked.connect(self.toggleTheme)
        if self.themeEngine is not None:
            try:
                self.themeEngine.onThemeChangeComplete.connect(self._onThemeReady)
            except Exception:
                pass

        self._paintChrome()
        self.navigateTo("jobs")

    # -- theme ------------------------------------------------------------- #
    def _currentTheme(self):
        return str(getattr(self.themeEngine, "theme", "") or T.THEME_LIGHT)

    def toggleTheme(self):
        if self.themeEngine is None:
            return
        target = T.THEME_LIGHT if not T.is_light(self._currentTheme()) else T.THEME_DARK
        self.themeEngine.setTheme(target)          # async icon regen, by NAME

    def _onThemeReady(self):
        self._paintChrome()
        for mgr in self.managers.values():
            try:
                mgr.recolor()
            except Exception:
                pass

    # -- chrome (icons + brand-constant dark rail) ------------------------- #
    def _paintChrome(self):
        theme = self._currentTheme()
        brand = T.brand()
        icon_col = T.roles(theme)["iconStrong"]     # crisp topbar glyphs (tracks theme)
        rail_text = brand.get("railText", "#ffffff")
        rail_muted = brand.get("railMuted", "#8a94a8")

        # dark rail is INTENTIONALLY theme-independent: styled from the Brand
        # palette (read from style.json), not from the flipping theme tokens.
        self._styleRail(brand)
        for name, icon in RAIL_ICONS:
            btn = self.railButtons.get(name)
            if btn is None:
                continue
            on = btn.isChecked()
            btn.setIcon(feather_icon(icon, rail_text if on else rail_muted, 22))

        # topbar glyphs track the theme icon colour
        for obj, icon in (("searchIcon", "search"), ("helpIcon", "help-circle"),
                          ("bellIcon", "bell")):
            lbl = getattr(self.ui, obj, None)
            if lbl is not None:
                lbl.setPixmap(feather_pixmap(icon, icon_col, 19))
        if hasattr(self.ui, "avatarCaret"):
            self.ui.avatarCaret.setPixmap(feather_pixmap("chevron-down", icon_col, 14))

    def _styleRail(self, brand):
        # brand-constant dark rail — colours read from style.json's Brand section
        # (not the theme tokens), because the rail stays dark in the light UI too.
        rail = brand.get("rail", "#0f172a")
        accent = brand.get("accent", "#f97316")
        text = brand.get("railText", "#ffffff")
        hover = _rgba(text, 0.08)
        self.ui.railLogo.setStyleSheet(
            "QLabel{background:%s; color:%s; border-radius:10px;"
            " font-weight:800; font-size:18px;}" % (accent, text))
        self.ui.railBar.setStyleSheet(
            "#railBar{background:%s;}"
            "QCustomSidebarButton{background:transparent; border:0; border-radius:12px;}"
            "QCustomSidebarButton:hover{background:%s;}"
            "QCustomSidebarButton:checked{background:%s;}" % (rail, hover, accent))

    # -- navigation -------------------------------------------------------- #
    def navigateTo(self, name):
        page = self.pages.get("jobs")               # single page in this example
        if page is not None:
            self.ui.pageStack.setCurrentWidget(page)
        # keep Work highlighted as the active section (rail is otherwise inert)
        active = name if name in self.railButtons else "navWork"
        for n, btn in self.railButtons.items():
            btn.setChecked(n == active)
        self._paintChrome()
        self.managers["jobs"].onShown()
