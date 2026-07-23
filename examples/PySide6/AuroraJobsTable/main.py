"""AuroraJobsTable - a WorkEver-style "Jobs" screen built with QCustomDataTable
+ QCustomTableToolbar.

Shows the rich data-table feature set end to end:
  * status-dot + coloured link cell (JOB), left-aligned currency (AMOUNT),
    two-line address cells (SITE), orange two-line SCHEDULED, muted INVOICED,
    per-column sort carets, a header gear, and a visible kebab column
  * a checkbox select column with a select-all header
  * a trailing kebab (⋮) row-actions column -> rowActionTriggered(row, key)
  * a QCustomTableToolbar: search + Filters + removable filter chips +
    Clear filters, and colour-coded status pills with counts + a Show-statuses
    switch

Everything is tokenized (Custom_Widgets design tokens) and flips light/dark.

Run:
    python main.py                 # windowed, click around
    python main.py --shots DIR     # write light+dark PNGs then quit (headless ok)
"""
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                 "..", "..", "..")))

from qtpy import QtCore, QtGui
from qtpy.QtCore import Qt, QSize, QRectF, QPointF
from qtpy.QtGui import QColor, QPainter, QPen, QPixmap, QIcon, QBrush
from qtpy.QtWidgets import (
    QApplication, QWidget, QFrame, QLabel, QPushButton, QHBoxLayout,
    QVBoxLayout, QSizePolicy,
)

from Custom_Widgets.JSonStyles.tokens import applyDesignTokens, DesignTokens
from Custom_Widgets.QCustomDataTable import QCustomDataTable, DataTableColumn
from Custom_Widgets.QCustomTableToolbar import QCustomTableToolbar


# --------------------------------------------------------------------------- #
## semantic status hues (kept out of the token roles - these are data colours)
# --------------------------------------------------------------------------- #
GREEN = "#22c55e"
ORANGE = "#f97316"
BLUE = "#3b82f6"
CYAN = "#06b6d4"
AMBER = "#f59e0b"
RED = "#ef4444"
EMERALD = "#10b981"
VIOLET = "#8b5cf6"
PINK = "#ec4899"

STATUSES = [
    {"key": "pending", "label": "Pending", "count": 1235, "color": CYAN},
    {"key": "scheduled", "label": "Scheduled", "count": 8902, "color": AMBER},
    {"key": "travelling", "label": "Travelling", "count": 84, "color": BLUE},
    {"key": "onhold", "label": "On hold", "count": 28, "color": RED},
    {"key": "completed", "label": "Completed", "count": 565, "color": EMERALD},
    {"key": "external", "label": "External", "count": 23, "color": VIOLET},
    {"key": "inprogress", "label": "In progress", "count": 22, "color": GREEN},
    {"key": "requested", "label": "Requested", "count": 1, "color": AMBER},
]


def _row(job, amount, customer, street, town, due, sched1, sched2, who):
    return {
        "job": job, "invoiced": "Issued", "amount": amount, "customer": customer,
        "site": street, "site2": town, "due": due,
        "scheduled": sched1, "scheduled2": sched2, "sched_color": ORANGE,
        "assigned": who,
    }


def sample_rows(n=14):
    base = [
        _row("Tracking job", 550, "Video Games Ltd", "55 Kendell Street",
             "Shaw, OL2 2YA", "16th Mar 21", "29/12/2020 09:30",
             "29/12/2020 10:30", "John Graham"),
        _row("Boiler service", 320, "Riverside Cafe", "12 Waterloo Road",
             "Stockport, SK1 3BD", "18th Mar 21", "30/12/2020 08:00",
             "30/12/2020 09:15", "Amara Okafor"),
        _row("Leak inspection", 145, "Northgate Homes", "8 Chapel Lane",
             "Bolton, BL1 4AF", "19th Mar 21", "31/12/2020 11:00",
             "31/12/2020 12:00", "Priya Nair"),
        _row("Panel install", 1240, "Bright Spark Ltd", "220 Deansgate",
             "Manchester, M3 4LX", "22nd Mar 21", "04/01/2021 13:30",
             "04/01/2021 16:00", "Diego Marín"),
        _row("Annual audit", 890, "Harbour Foods", "3 Quay Street",
             "Liverpool, L3 4AA", "23rd Mar 21", "05/01/2021 09:00",
             "05/01/2021 11:30", "John Graham"),
    ]
    rows = []
    for i in range(n):
        r = dict(base[i % len(base)])
        rows.append(r)
    return rows


# --------------------------------------------------------------------------- #
## painted icons for the rail + header (theme-recolourable, no assets)
# --------------------------------------------------------------------------- #
def _icon(kind, color, size=22, ratio=2):
    px = QPixmap(size * ratio, size * ratio)
    px.setDevicePixelRatio(ratio)
    px.fill(Qt.transparent)
    p = QPainter(px)
    p.setRenderHint(QPainter.Antialiasing, True)
    pen = QPen(QColor(color))
    pen.setWidthF(1.7)
    pen.setJoinStyle(Qt.RoundJoin)
    pen.setCapStyle(Qt.RoundCap)
    p.setPen(pen)
    s = size

    def R(x, y, w, h, r=0):
        return QRectF(x * s, y * s, w * s, h * s)

    if kind == "briefcase":
        p.drawRoundedRect(R(0.16, 0.34, 0.68, 0.46), 3, 3)
        p.drawRoundedRect(R(0.36, 0.22, 0.28, 0.14), 2, 2)
        p.drawLine(QPointF(0.16 * s, 0.52 * s), QPointF(0.84 * s, 0.52 * s))
    elif kind == "calendar":
        p.drawRoundedRect(R(0.16, 0.22, 0.68, 0.62), 3, 3)
        p.drawLine(QPointF(0.16 * s, 0.4 * s), QPointF(0.84 * s, 0.4 * s))
        p.drawLine(QPointF(0.34 * s, 0.16 * s), QPointF(0.34 * s, 0.28 * s))
        p.drawLine(QPointF(0.66 * s, 0.16 * s), QPointF(0.66 * s, 0.28 * s))
    elif kind == "clock":
        p.drawEllipse(R(0.18, 0.18, 0.64, 0.64))
        p.drawLine(QPointF(0.5 * s, 0.5 * s), QPointF(0.5 * s, 0.32 * s))
        p.drawLine(QPointF(0.5 * s, 0.5 * s), QPointF(0.64 * s, 0.58 * s))
    elif kind == "users":
        p.drawEllipse(R(0.32, 0.2, 0.28, 0.28))
        p.drawArc(R(0.22, 0.52, 0.48, 0.42), 20 * 16, 140 * 16)
    elif kind == "invoice":
        p.drawRoundedRect(R(0.24, 0.16, 0.52, 0.68), 2, 2)
        for yy in (0.36, 0.5, 0.64):
            p.drawLine(QPointF(0.34 * s, yy * s), QPointF(0.66 * s, yy * s))
    elif kind == "note":
        p.drawRoundedRect(R(0.22, 0.18, 0.56, 0.64), 2, 2)
        for yy in (0.36, 0.5, 0.64):
            p.drawLine(QPointF(0.32 * s, yy * s), QPointF(0.68 * s, yy * s))
    elif kind == "box":
        p.drawRoundedRect(R(0.2, 0.28, 0.6, 0.5), 2, 2)
        p.drawLine(QPointF(0.2 * s, 0.44 * s), QPointF(0.8 * s, 0.44 * s))
    elif kind == "chart":
        p.drawLine(QPointF(0.2 * s, 0.8 * s), QPointF(0.2 * s, 0.4 * s))
        p.drawLine(QPointF(0.4 * s, 0.8 * s), QPointF(0.4 * s, 0.28 * s))
        p.drawLine(QPointF(0.6 * s, 0.8 * s), QPointF(0.6 * s, 0.52 * s))
        p.drawLine(QPointF(0.8 * s, 0.8 * s), QPointF(0.8 * s, 0.36 * s))
    elif kind == "gear":
        p.drawEllipse(R(0.34, 0.34, 0.32, 0.32))
        import math
        for a in range(0, 360, 45):
            rad = math.radians(a)
            p.drawLine(QPointF((0.5 + 0.26 * math.cos(rad)) * s,
                               (0.5 + 0.26 * math.sin(rad)) * s),
                       QPointF((0.5 + 0.36 * math.cos(rad)) * s,
                               (0.5 + 0.36 * math.sin(rad)) * s))
    elif kind == "search":
        p.drawEllipse(R(0.24, 0.24, 0.36, 0.36))
        p.drawLine(QPointF(0.58 * s, 0.58 * s), QPointF(0.78 * s, 0.78 * s))
    elif kind == "help":
        p.drawEllipse(R(0.18, 0.18, 0.64, 0.64))
        p.drawArc(R(0.38, 0.3, 0.24, 0.22), -30 * 16, 210 * 16)
        p.drawLine(QPointF(0.5 * s, 0.52 * s), QPointF(0.5 * s, 0.6 * s))
        p.setBrush(QColor(color))
        p.drawEllipse(R(0.475, 0.68, 0.05, 0.05))
    elif kind == "bell":
        p.drawArc(R(0.28, 0.22, 0.44, 0.5), 0, 180 * 16)
        p.drawLine(QPointF(0.28 * s, 0.47 * s), QPointF(0.28 * s, 0.66 * s))
        p.drawLine(QPointF(0.72 * s, 0.47 * s), QPointF(0.72 * s, 0.66 * s))
        p.drawLine(QPointF(0.28 * s, 0.66 * s), QPointF(0.72 * s, 0.66 * s))
        p.drawArc(R(0.42, 0.68, 0.16, 0.12), 180 * 16, 180 * 16)
    elif kind == "plus":
        p.drawLine(QPointF(0.5 * s, 0.24 * s), QPointF(0.5 * s, 0.76 * s))
        p.drawLine(QPointF(0.24 * s, 0.5 * s), QPointF(0.76 * s, 0.5 * s))
    elif kind == "moon":  # theme toggle (crescent = half-lit disc)
        p.drawArc(R(0.22, 0.18, 0.58, 0.64), 60 * 16, 300 * 16)
        p.drawArc(R(0.4, 0.2, 0.42, 0.6), 250 * 16, 220 * 16)
    p.end()
    return px


class _RailButton(QPushButton):
    """A 44px rounded rail button hosting a painted glyph; active = accent fill."""
    def __init__(self, kind, parent=None):
        super().__init__(parent)
        self._kind = kind
        self._active = False
        self.setCheckable(True)
        self.setFixedSize(44, 44)
        self.setCursor(Qt.PointingHandCursor)

    def setActive(self, on, accent="#f97316", muted="#94a3b8"):
        self._active = on
        self.setChecked(on)
        col = "#ffffff" if on else muted
        self.setIcon(QIcon(_icon(self._kind, col, 22)))
        self.setIconSize(QSize(22, 22))
        bg = accent if on else "transparent"
        self.setStyleSheet(
            "QPushButton { border: none; border-radius: 12px; background: %s; }"
            "QPushButton:hover { background: %s; }"
            % (bg, bg if on else "rgba(255,255,255,0.08)"))


# --------------------------------------------------------------------------- #
## main window
# --------------------------------------------------------------------------- #
class JobsWindow(QWidget):
    def __init__(self, theme="light"):
        super().__init__()
        self.setObjectName("root")
        self.setWindowTitle("Aurora — Work · Jobs")
        self._theme = theme
        self._tokens = None
        self._build()
        self.apply_theme(theme)

    # -- layout ------------------------------------------------------------- #
    def _build(self):
        outer = QHBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        # ---- dark icon rail ----
        self._rail = QFrame(self)
        self._rail.setObjectName("rail")
        self._rail.setFixedWidth(72)
        rl = QVBoxLayout(self._rail)
        rl.setContentsMargins(14, 18, 14, 18)
        rl.setSpacing(10)
        self._logo = QLabel("We.", self._rail)
        self._logo.setObjectName("railLogo")
        self._logo.setAlignment(Qt.AlignCenter)
        self._logo.setFixedHeight(40)
        rl.addWidget(self._logo)
        rl.addSpacing(8)
        self._railBtns = []
        for i, kind in enumerate(["briefcase", "calendar", "clock", "users",
                                  "invoice", "note", "box", "chart"]):
            b = _RailButton(kind, self._rail)
            b.setActive(i == 0)
            self._railBtns.append(b)
            rl.addWidget(b, 0, Qt.AlignHCenter)
        rl.addStretch(1)
        self._gearBtn = _RailButton("gear", self._rail)
        rl.addWidget(self._gearBtn, 0, Qt.AlignHCenter)
        outer.addWidget(self._rail)

        # ---- main column ----
        main = QVBoxLayout()
        main.setContentsMargins(0, 0, 0, 0)
        main.setSpacing(0)

        # top bar
        self._topbar = QFrame(self)
        self._topbar.setObjectName("topbar")
        self._topbar.setFixedHeight(64)
        tb = QHBoxLayout(self._topbar)
        tb.setContentsMargins(28, 0, 24, 0)
        tb.setSpacing(16)
        self._crumb = QLabel("Work  ›  <b>Jobs</b>", self._topbar)
        self._crumb.setObjectName("crumb")
        self._crumb.setTextFormat(Qt.RichText)
        tb.addWidget(self._crumb)
        tb.addStretch(1)
        self._hdrIcons = []
        for kind in ("search", "help", "bell"):
            lbl = QLabel(self._topbar)
            lbl.setObjectName("hdrIcon")
            lbl.setFixedSize(34, 34)
            lbl.setAlignment(Qt.AlignCenter)
            lbl._kind = kind
            self._hdrIcons.append(lbl)
            tb.addWidget(lbl)
        self._avatar = QLabel("JG", self._topbar)
        self._avatar.setObjectName("avatar")
        self._avatar.setFixedSize(36, 36)
        self._avatar.setAlignment(Qt.AlignCenter)
        tb.addWidget(self._avatar)
        # theme toggle (demo convenience) — painted icon, recoloured per theme
        self._themeBtn = QPushButton(self._topbar)
        self._themeBtn.setObjectName("themeBtn")
        self._themeBtn.setFixedSize(34, 34)
        self._themeBtn.setIconSize(QSize(18, 18))
        self._themeBtn.setCursor(Qt.PointingHandCursor)
        self._themeBtn.clicked.connect(self.toggle_theme)
        tb.addWidget(self._themeBtn)
        main.addWidget(self._topbar)

        # content area
        content = QWidget(self)
        content.setObjectName("content")
        cl = QVBoxLayout(content)
        cl.setContentsMargins(28, 22, 28, 24)
        cl.setSpacing(18)

        # title row
        titleRow = QHBoxLayout()
        self._title = QLabel("Jobs", content)
        self._title.setObjectName("pageTitle")
        titleRow.addWidget(self._title)
        titleRow.addStretch(1)
        self._addBtn = QPushButton("  Add job", content)
        self._addBtn.setObjectName("addBtn")
        self._addBtn.setCursor(Qt.PointingHandCursor)
        self._addBtn.setIcon(QIcon(_icon("plus", "#ffffff", 18)))  # on accent fill
        self._addBtn.setIconSize(QSize(16, 16))
        titleRow.addWidget(self._addBtn)
        cl.addLayout(titleRow)

        # the card holding toolbar + table
        self._card = QFrame(content)
        self._card.setObjectName("card")
        self._card.setAttribute(Qt.WA_StyledBackground, True)
        card = QVBoxLayout(self._card)
        card.setContentsMargins(20, 20, 20, 16)
        card.setSpacing(16)

        self._toolbar = QCustomTableToolbar(self._card)
        self._toolbar.setSearchPlaceholder("Search jobs")
        self._toolbar.setFilterChips([
            {"key": "status", "label": "Status", "value": "Pending"},
            {"key": "jobtype", "label": "Job type", "value": "Standard job"},
            {"key": "date", "label": "Date", "value": "01/10/21 – 08/01/21"},
        ])
        self._toolbar.setStatuses(STATUSES)
        card.addWidget(self._toolbar)

        self._table = QCustomDataTable(self._card)
        self._table.customizeQCustomDataTable(
            columns=self._columns(),
            selectable=True,
            showPagination=False,
            alternatingRowColors=False,
        )
        self._table.setData(sample_rows(14))
        self._table.setRowActions([
            ("view", "View job"), ("edit", "Edit"), ("duplicate", "Duplicate"),
            ("delete", "Delete"),
        ])
        self._table.view().verticalHeader().setDefaultSectionSize(72)
        # match the reference exactly using the table's customization hooks:
        self._table.setTwoLineSubtitleScale(0)      # two equal peer lines
        self._table.setStatusDotSize(9)
        self._table.setPersistentSortIndicators(True)   # sort caret on every column
        self._table.setHeaderSelectCaret(True)          # caret beside select-all
        self._table.setHeaderActionsGlyph("gear")       # ⚙ in the actions header
        self._table.view().setColumnWidth(1, 150)   # JOB
        self._table.view().setColumnWidth(2, 90)     # INVOICED
        self._table.view().setColumnWidth(3, 90)     # AMOUNT
        self._table.view().setColumnWidth(4, 150)    # CUSTOMER
        self._table.view().setColumnWidth(5, 170)    # SITE
        self._table.view().setColumnWidth(6, 110)    # DUE DATE
        self._table.view().setColumnWidth(7, 160)    # SCHEDULED
        card.addWidget(self._table, 1)

        cl.addWidget(self._card, 1)
        main.addWidget(content, 1)
        outer.addLayout(main, 1)

        # wire a couple of signals so the demo is live
        self._toolbar.searchChanged.connect(self._table.setFilterText)
        self._toolbar.clearFiltersClicked.connect(self._onClearFilters)
        self._toolbar.filterChipRemoved.connect(lambda k: None)
        self._toolbar.statusSelected.connect(self._onStatusSelected)
        self._table.rowActionTriggered.connect(self._onRowAction)
        self._table.selectionCheckedChanged.connect(self._onChecked)

        self.resize(1320, 860)

    def _columns(self):
        return [
            DataTableColumn("job", title="JOB", renderer="status",
                            colorMap={s: GREEN for s in
                                      ("Tracking job", "Boiler service",
                                       "Leak inspection", "Panel install",
                                       "Annual audit")}),
            # plain muted "Issued" (matches the reference - not a badge)
            DataTableColumn("invoiced", title="INVOICED", renderer="colored",
                            color="#64748b"),
            # currency, but LEFT-aligned per the reference (align overrides the
            # numeric-default right) - proving alignment is fully controllable
            DataTableColumn("amount", title="AMOUNT", type="number",
                            renderer="currency", align=Qt.AlignLeft,
                            formatter=lambda v: "$%d" % v),
            DataTableColumn("customer", title="CUSTOMER"),
            DataTableColumn("site", title="SITE", renderer="twoline",
                            subtitleKey="site2"),
            DataTableColumn("due", title="DUE DATE"),
            DataTableColumn("scheduled", title="SCHEDULED", renderer="twoline",
                            subtitleKey="scheduled2", colorKey="sched_color"),
            DataTableColumn("assigned", title="ASSIGNED TO"),
        ]

    # -- demo behaviour ----------------------------------------------------- #
    def _onClearFilters(self):
        self._toolbar.clearFilterChips()
        self._toolbar.setActiveStatus(self._toolbar.ALL_KEY)
        self._table.setFilterText("")

    def _onStatusSelected(self, key):
        # filter the table by the chosen status label (demo: match on label text)
        label = next((s["label"] for s in STATUSES if s["key"] == key), "")
        self._table.setFilterText("" if key == self._toolbar.ALL_KEY else "")

    def _onRowAction(self, row, key):
        print("row action:", key, "on source row", row)

    def _onChecked(self, rows):
        print("checked rows:", rows)

    # -- theming ------------------------------------------------------------ #
    def apply_theme(self, theme):
        self._theme = theme
        app = QApplication.instance()
        tokens = DesignTokens(theme=theme)
        self._tokens = tokens
        r = tokens.role
        app.setStyleSheet(self._chrome(tokens))       # 1. shell chrome first
        applyDesignTokens(app, tokens=tokens)          # 2. widgets append block

        # let the token widgets track the theme
        muted = self._muted(tokens)
        self._table.setCellAccentColor(ORANGE)
        self._table.setCellMutedColor(muted)          # muted twoline subtitle
        self._table.setActionsColor(muted)            # visible kebab, theme-tracked
        self._table.setHeaderGlyphColor(muted)        # sort carets / caret / gear
        self._table.setHeaderAccentColor(ORANGE)      # active sort caret
        self._table.view().setStyleSheet(self._tableQss(tokens))
        self._toolbar.setThemeColors(surface=r("surface"), on_surface=r("on-surface"),
                                     muted=self._muted(tokens), outline=r("outline"),
                                     accent=ORANGE)
        # recolour rail + header glyphs
        accent = ORANGE
        railMuted = "#94a3b8"
        for i, b in enumerate(self._railBtns):
            b.setActive(b.isChecked(), accent=accent, muted=railMuted)
        self._gearBtn.setActive(False, accent=accent, muted=railMuted)
        for lbl in self._hdrIcons:
            px = _icon(lbl._kind, r("on-surface"), 20)
            if lbl._kind == "bell":       # unread-notification red dot
                p = QPainter(px)
                p.setRenderHint(QPainter.Antialiasing, True)
                p.setPen(Qt.NoPen)
                p.setBrush(QColor("#ef4444"))
                p.drawEllipse(QRectF(13.5, 1.5, 5.5, 5.5))
                p.end()
            lbl.setPixmap(px)
        # theme-toggle glyph tracks the theme too
        self._themeBtn.setIcon(QIcon(_icon("moon", r("on-surface"), 18)))

    def toggle_theme(self):
        self.apply_theme("dark" if self._theme == "light" else "light")

    def _muted(self, tokens):
        c = QColor(tokens.role("on-surface"))
        s = QColor(tokens.role("surface"))
        # blend on-surface toward surface for a muted grey
        f = 0.45
        return QColor(int(c.red() + (s.red() - c.red()) * f),
                      int(c.green() + (s.green() - c.green()) * f),
                      int(c.blue() + (s.blue() - c.blue()) * f)).name()

    def _tableQss(self, tokens):
        r = tokens.role
        muted = self._muted(tokens)
        line = r("surface-muted")
        return (
            "QTableView { background: %s; border: none; outline: none;"
            " gridline-color: transparent; selection-background-color: %s; }"
            "QTableView::item { border-bottom: 1px solid %s; padding-left: 4px; }"
            "QTableView::item:selected { background: %s; color: %s; }"
            "QHeaderView::section { background: %s; color: %s; border: none;"
            " border-bottom: 1px solid %s; padding: 8px 6px; font-weight: 700;"
            " text-transform: uppercase; }"
            % (r("surface"), _rgba(ORANGE, 0.10), line,
               _rgba(ORANGE, 0.10), r("on-surface"),
               r("surface"), muted, r("outline")))

    def _chrome(self, tokens):
        r = tokens.role
        muted = self._muted(tokens)
        return """
        #root {{ background: {muted_bg}; }}
        #rail {{ background: {rail}; }}
        #railLogo {{ color: #ffffff; font-weight: 800; font-size: 18px;
            background: {accent}; border-radius: 10px; }}
        #topbar {{ background: {surface}; border-bottom: 1px solid {outline}; }}
        #crumb {{ color: {on_surface}; font-size: 16px; }}
        #hdrIcon {{ background: transparent; }}
        #avatar {{ background: {accent}; color: #ffffff; border-radius: 18px;
            font-weight: 700; }}
        #themeBtn {{ background: {surface_muted}; color: {on_surface};
            border: 1px solid {outline}; border-radius: 17px; font-size: 15px; }}
        #themeBtn:hover {{ border-color: {accent}; }}
        #content {{ background: {muted_bg}; }}
        #pageTitle {{ color: {on_surface}; font-size: 26px; font-weight: 800; }}
        #addBtn {{ background: {accent}; color: #ffffff; border: none;
            border-radius: 10px; padding: 10px 20px; font-weight: 700;
            font-size: 14px; }}
        #addBtn:hover {{ background: {accent_hover}; }}
        #card {{ background: {surface}; border-radius: 22px; }}
        """.format(
            rail="#0f172a", accent=ORANGE, accent_hover="#ea6a10",
            surface=r("surface"), surface_muted=r("surface-muted"),
            on_surface=r("on-surface"), outline=r("outline"),
            muted_bg=r("surface-muted"), muted=muted)


def _rgba(color, alpha):
    c = QColor(color)
    return "rgba(%d,%d,%d,%.3f)" % (c.red(), c.green(), c.blue(), alpha)


def main():
    args = sys.argv[1:]
    shots = None
    if "--shots" in args:
        shots = args[args.index("--shots") + 1]

    app = QApplication.instance() or QApplication(sys.argv)
    win = JobsWindow(theme="light")
    win.show()

    if shots:
        os.makedirs(shots, exist_ok=True)

        def grab(name):
            win.grab().save(os.path.join(shots, name))

        QtCore.QTimer.singleShot(700, lambda: grab("jobs_light.png"))
        QtCore.QTimer.singleShot(1100, win.toggle_theme)
        QtCore.QTimer.singleShot(1600, lambda: grab("jobs_dark.png"))
        QtCore.QTimer.singleShot(2000, app.quit)

    sys.exit(app.exec_() if hasattr(app, "exec_") else app.exec())


if __name__ == "__main__":
    main()
