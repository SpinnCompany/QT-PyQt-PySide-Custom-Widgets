"""Aurora Jobs — GUI orchestration (the CORRECT architecture).

A single GuiFunctions orchestrator owns nav + theming and holds one Manager per
page. The JobsManager reaches its embedded component via ``container.component``
and configures the library widgets that Designer cannot set (DataTable columns,
Toolbar statuses) IN CODE — exactly like charts. Data lives in gui/data.py; the
rows arrive from a background Worker->Signal->GUI loader.

ICONS ARE NOT SET FROM PYTHON. Every icon is declared in Qss/scss/chrome.scss
(``qproperty-icon: url(theme-icons:icons/feather/<name>.svg)``) and recolours to
the theme's Icons-color automatically. On a theme switch Python only RE-POLISHES
(``style().unpolish``/``polish``) so the widgets reload their recoloured icons —
never ``setIcon``/``setPixmap``. Theme switching goes BY NAME (Aurora Light/Dark).
"""

from qtpy.QtCore import QObject, Qt, QThread, QTimer
from qtpy.QtWidgets import QApplication

from Custom_Widgets.QCustomDataTable import DataTableColumn

from gui import theme as T
from gui import data as D
from gui.workers import JobsLoaderWorker

# Rail nav buttons (icons are assigned in chrome.scss by objectName).
NAV_NAMES = ["navWork", "navCalendar", "navClock", "navUsers", "navInvoice",
             "navNote", "navBox", "navChart", "navSettings"]


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
    # These are PAINT colours (like chart series), not icons/pixmaps — read from
    # the theme roles and re-applied on theme switch.
    def _applyThemeColors(self):
        r = T.roles(self._theme_name())
        self.table.setCellAccentColor(r["accent"])
        self.table.setCellMutedColor(r["muted"])
        self.table.setActionsColor(r["muted"])
        self.table.setHeaderGlyphColor(r["muted"])
        self.table.setHeaderAccentColor(r["accent"])
        self.table.setRowSeparatorColor(r["outline"])   # uniform under ALL cells
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
        # The rail starts collapsed (72px icons); the sidebarToggle expands it to
        # 240px to reveal labels. NOTE: the width animation is SKIPPED when
        # collapsedWidth == expandedWidth, so they must differ for collapse/expand
        # to resize at all. defaultWidth=72 makes it start collapsed.
        rail = ui.railBar
        rail.customizeQCustomSlideMenu(defaultWidth=72, collapsedWidth=72, expandedWidth=240)
        ui.sidebarToggle.clicked.connect(rail.toggleMenu)

        self.pages = {"jobs": ui.jobsContainer}
        self.railButtons = {name: getattr(ui, name) for name in NAV_NAMES}
        self.managers = {"jobs": JobsManager(self.win, ui.jobsContainer)}

        for name, btn in self.railButtons.items():
            btn.clicked.connect(lambda _=False, n=name: self.navigateTo(n))

        # avatar doubles as the light/dark toggle
        self.themeEngine = getattr(self.win, "themeEngine", None)
        ui.avatar.clicked.connect(self.toggleTheme)
        if self.themeEngine is not None:
            try:
                self.themeEngine.onThemeChangeComplete.connect(self._onThemeReady)
            except Exception:
                pass

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
        # Async icon regen finished: RE-POLISH so the QSS qproperty-icons reload
        # in their new theme colour (no setIcon here), then refresh delegate paint.
        self._repolishChrome()
        for mgr in self.managers.values():
            try:
                mgr.recolor()
            except Exception:
                pass

    def _repolishChrome(self):
        widgets = list(self.railButtons.values())
        for obj in ("sidebarToggle", "searchIcon", "helpIcon", "bellIcon",
                    "avatarCaret", "avatar", "railLogo"):
            w = getattr(self.ui, obj, None)
            if w is not None:
                widgets.append(w)
        for w in widgets:
            w.style().unpolish(w)
            w.style().polish(w)

    # -- navigation -------------------------------------------------------- #
    def navigateTo(self, name):
        page = self.pages.get("jobs")               # single page in this example
        if page is not None:
            self.ui.pageStack.setCurrentWidget(page)
        # keep Work highlighted as the active section (rail is otherwise inert);
        # setChecked makes Qt re-apply the :checked QSS automatically.
        active = name if name in self.railButtons else "navWork"
        # autoExclusive ignores setChecked(False), so toggle it off per-button to
        # force exactly one active pill.
        for n, btn in self.railButtons.items():
            btn.setAutoExclusive(False)
            btn.setChecked(n == active)
            btn.setAutoExclusive(True)
        self.managers["jobs"].onShown()
