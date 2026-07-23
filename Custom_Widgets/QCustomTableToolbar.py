########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/spinnTv
# WEBSITE: spinncode.com
########################################################################

########################################################################
## QCustomTableToolbar - a rich filter/search bar for data tables.
##
## The companion chrome above a QCustomDataTable, modelled on modern SaaS
## "Jobs / Records" screens (search + Filters button + removable filter chips +
## Clear filters, and a second row of colour-coded status pills with counts and
## a Show-statuses switch). It owns no data - it just emits intent:
##
##   searchChanged(str)          the search text changed (debounced by typing)
##   filtersClicked()            the Filters button was pressed
##   filterChipRemoved(str)      a filter chip's x was clicked (its key)
##   clearFiltersClicked()       the Clear filters link was pressed
##   statusSelected(str)         a status pill was picked ("" == the All pill)
##   showStatusesToggled(bool)   the Show-statuses switch flipped
##
## Colours track the active theme through setThemeColors(...) (call it after
## applyDesignTokens); each status keeps its own semantic hue for its pill.
########################################################################
from qtpy.QtCore import Qt, Signal, QSize, QRectF, QPointF
from qtpy.QtGui import QColor, QPainter, QPen, QPixmap, QIcon, QFont
from qtpy.QtWidgets import (
    QWidget, QFrame, QLabel, QLineEdit, QPushButton, QToolButton,
    QHBoxLayout, QVBoxLayout, QSizePolicy,
)

from Custom_Widgets.QCustomSwitch import QCustomSwitch


# --------------------------------------------------------------------------- #
## Painted glyphs (crisp, theme-recolourable, no asset dependency)
# --------------------------------------------------------------------------- #
def _glyph_pixmap(kind, color, size=16, ratio=2):
    """A small monochrome UI glyph rendered to a QPixmap in `color`."""
    px = QPixmap(size * ratio, size * ratio)
    px.setDevicePixelRatio(ratio)
    px.fill(Qt.transparent)
    p = QPainter(px)
    p.setRenderHint(QPainter.Antialiasing, True)
    pen = QPen(QColor(color))
    pen.setWidthF(1.6)
    pen.setCapStyle(Qt.RoundCap)
    p.setPen(pen)
    if kind == "search":
        r = size * 0.42
        cx, cy = size * 0.42, size * 0.42
        p.drawEllipse(QRectF(cx - r / 2, cy - r / 2, r, r))
        p.drawLine(QPointF(cx + r / 2 - 0.5, cy + r / 2 - 0.5),
                   QPointF(size * 0.86, size * 0.86))
    elif kind == "sliders":
        # three horizontal rails with offset knobs (a "filters" icon)
        p.setBrush(QColor(color))
        ys = (size * 0.28, size * 0.5, size * 0.72)
        knobx = (size * 0.66, size * 0.36, size * 0.6)
        for y, kx in zip(ys, knobx):
            p.drawLine(QPointF(size * 0.16, y), QPointF(size * 0.84, y))
            p.drawEllipse(QRectF(kx - 2.2, y - 2.2, 4.4, 4.4))
    p.end()
    return px


def _rgba(color, alpha):
    c = QColor(color)
    return "rgba(%d,%d,%d,%.3f)" % (c.red(), c.green(), c.blue(), alpha)


# --------------------------------------------------------------------------- #
## Removable filter chip  ("Status: Pending  x")
# --------------------------------------------------------------------------- #
class _FilterChip(QFrame):
    removed = Signal(str)

    def __init__(self, key, label, value=None, parent=None):
        super().__init__(parent)
        self._key = str(key)
        self.setObjectName("tableFilterChip")
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        lay = QHBoxLayout(self)
        lay.setContentsMargins(12, 4, 8, 4)
        lay.setSpacing(6)
        self._prefix = QLabel(self)
        self._prefix.setObjectName("tableFilterChipPrefix")
        self._value = QLabel(self)
        self._value.setObjectName("tableFilterChipValue")
        lay.addWidget(self._prefix)
        lay.addWidget(self._value)
        self._close = QToolButton(self)
        self._close.setObjectName("tableFilterChipClose")
        self._close.setText("✕")
        self._close.setCursor(Qt.PointingHandCursor)
        self._close.setAutoRaise(True)
        self._close.clicked.connect(lambda: self.removed.emit(self._key))
        lay.addWidget(self._close)
        self.setText(label, value)

    def key(self):
        return self._key

    def setText(self, label, value=None):
        if value is None or value == "":
            self._prefix.setText("")
            self._prefix.setVisible(False)
            self._value.setText(str(label))
        else:
            self._prefix.setText("%s:" % label)
            self._prefix.setVisible(True)
            self._value.setText(str(value))


# --------------------------------------------------------------------------- #
## Status pill  ("Pending  1235") with a semantic outline colour
# --------------------------------------------------------------------------- #
class _StatusPill(QFrame):
    clicked = Signal(str)

    def __init__(self, key, label, count=None, color="#3b82f6", parent=None):
        super().__init__(parent)
        self._key = str(key)
        self._color = color
        self._checked = False
        self._text = QColor("#0f172a")
        self._muted = QColor("#64748b")
        self._surface = QColor("#ffffff")
        self.setObjectName("tableStatusPill")
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setCursor(Qt.PointingHandCursor)
        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        lay = QHBoxLayout(self)
        lay.setContentsMargins(14, 5, 14, 5)
        lay.setSpacing(9)
        self._name = QLabel(label, self)
        self._name.setObjectName("tableStatusPillName")
        self._count = QLabel("" if count is None else str(count), self)
        self._count.setObjectName("tableStatusPillCount")
        self._count.setVisible(count is not None)
        lay.addWidget(self._name)
        lay.addWidget(self._count)
        self._restyle()

    def key(self):
        return self._key

    def isChecked(self):
        return self._checked

    def setChecked(self, on):
        on = bool(on)
        if on != self._checked:
            self._checked = on
            self._restyle()

    def setCount(self, count):
        self._count.setText("" if count is None else str(count))
        self._count.setVisible(count is not None)

    def setColor(self, color):
        self._color = color
        self._restyle()

    def applyThemeColors(self, text, muted, surface):
        self._text = QColor(text)
        self._muted = QColor(muted)
        self._surface = QColor(surface)
        self._restyle()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.rect().contains(event.pos()):
            self.clicked.emit(self._key)
        super().mouseReleaseEvent(event)

    def _restyle(self):
        # neutral pills (the "All" pill uses the muted colour as its hue)
        hue = self._color
        h = self.sizeHint().height() or 30
        radius = 15
        border = hue if self._checked else _rgba(hue, 0.55)
        bg = _rgba(hue, 0.14) if self._checked else self._surface.name()
        name_col = (QColor(hue).name() if self._checked else self._text.name())
        self.setStyleSheet(
            "#tableStatusPill { border: 1.4px solid %s; border-radius: %dpx;"
            " background: %s; }"
            "#tableStatusPillName { color: %s; font-weight: 600; background: transparent; }"
            "#tableStatusPillCount { color: %s; font-weight: 700; background: transparent; }"
            % (border, radius, bg, name_col, QColor(hue).name()))


# --------------------------------------------------------------------------- #
## The toolbar
# --------------------------------------------------------------------------- #
class QCustomTableToolbar(QWidget):

    # -- Designer registration constants --
    WIDGET_ICON = "components/icons/table.png"
    WIDGET_TOOLTIP = "A search / filter / status-pill toolbar for data tables"
    WIDGET_MODULE = "Custom_Widgets.QCustomTableToolbar"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomTableToolbar' name='tableToolbar'>
            <property name='geometry'>
                <rect><x>0</x><y>0</y><width>720</width><height>110</height></rect>
            </property>
        </widget>
    </ui>
    """

    __catalog__ = {
        "name": "QCustomTableToolbar",
        "props": {
            "searchPlaceholder": {"type": "string", "default": "Search"},
            "showStatuses": {"type": "bool", "default": True},
        },
        "signals": ["searchChanged", "filtersClicked", "filterChipRemoved",
                    "clearFiltersClicked", "statusSelected", "showStatusesToggled"],
        "tokens_used": ["surface", "surface-muted", "on-surface", "outline",
                        "primary", "accent"],
    }

    ALL_KEY = ""     # the built-in "All" status pill

    searchChanged = Signal(str)
    filtersClicked = Signal()
    filterChipRemoved = Signal(str)
    clearFiltersClicked = Signal()
    statusSelected = Signal(str)
    showStatusesToggled = Signal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("tableToolbar")
        self.setAttribute(Qt.WA_StyledBackground, True)
        self._chips = {}          # key -> _FilterChip
        self._pills = {}          # key -> _StatusPill
        self._activeStatus = self.ALL_KEY
        # theme colours (sensible light defaults until setThemeColors is called)
        self._c = dict(surface="#ffffff", on_surface="#0f172a",
                       muted="#64748b", outline="#e2e8f0", accent="#2563eb")
        self._buildUi()
        self._applyChrome()

    # ------------------------------------------------------------------ #
    ## UI
    # ------------------------------------------------------------------ #
    def _buildUi(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(14)

        # -- row 1: search + Filters + chips + Clear filters -------------
        row1 = QHBoxLayout()
        row1.setSpacing(10)

        self._search = QFrame(self)
        self._search.setObjectName("tableSearch")
        self._search.setAttribute(Qt.WA_StyledBackground, True)
        slay = QHBoxLayout(self._search)
        slay.setContentsMargins(12, 0, 12, 0)
        slay.setSpacing(8)
        self._searchIcon = QLabel(self._search)
        self._searchIcon.setObjectName("tableSearchIcon")
        self._input = QLineEdit(self._search)
        self._input.setObjectName("tableSearchInput")
        self._input.setPlaceholderText("Search")
        self._input.setFrame(False)
        self._input.textChanged.connect(self.searchChanged.emit)
        slay.addWidget(self._searchIcon)
        slay.addWidget(self._input)
        self._search.setFixedHeight(40)
        self._search.setMinimumWidth(240)
        row1.addWidget(self._search)

        self._filtersBtn = QPushButton("Filters", self)
        self._filtersBtn.setObjectName("tableFiltersBtn")
        self._filtersBtn.setCursor(Qt.PointingHandCursor)
        self._filtersBtn.clicked.connect(self.filtersClicked.emit)
        row1.addWidget(self._filtersBtn)

        self._chipBox = QWidget(self)
        self._chipBox.setObjectName("tableChips")
        self._chipLay = QHBoxLayout(self._chipBox)
        self._chipLay.setContentsMargins(0, 0, 0, 0)
        self._chipLay.setSpacing(8)
        row1.addWidget(self._chipBox)

        row1.addStretch(1)

        self._clearBtn = QPushButton("Clear filters", self)
        self._clearBtn.setObjectName("tableClearBtn")
        self._clearBtn.setCursor(Qt.PointingHandCursor)
        self._clearBtn.setFlat(True)
        self._clearBtn.clicked.connect(self.clearFiltersClicked.emit)
        row1.addWidget(self._clearBtn)
        root.addLayout(row1)

        # -- row 2: Show-statuses switch + All + status pills ------------
        row2 = QHBoxLayout()
        row2.setSpacing(10)
        self._switch = QCustomSwitch(self, checked=True)
        self._switch.toggled.connect(self._onShowStatusesToggled)
        row2.addWidget(self._switch)
        self._switchLabel = QLabel("Show statuses", self)
        self._switchLabel.setObjectName("tableShowStatusesLabel")
        row2.addWidget(self._switchLabel)
        row2.addSpacing(6)

        self._pillBox = QWidget(self)
        self._pillBox.setObjectName("tableStatusPills")
        self._pillLay = QHBoxLayout(self._pillBox)
        self._pillLay.setContentsMargins(0, 0, 0, 0)
        self._pillLay.setSpacing(9)
        row2.addWidget(self._pillBox)
        row2.addStretch(1)
        root.addLayout(row2)

        # the built-in "All" pill (neutral hue, selected by default)
        self._allPill = _StatusPill(self.ALL_KEY, "All", None, self._c["muted"],
                                    self._pillBox)
        self._allPill.setChecked(True)
        self._allPill.clicked.connect(self._onStatusClicked)
        self._pillLay.addWidget(self._allPill)
        self._pills[self.ALL_KEY] = self._allPill

    # ------------------------------------------------------------------ #
    ## Search API
    # ------------------------------------------------------------------ #
    def searchInput(self):
        return self._input

    def setSearchPlaceholder(self, text):
        self._input.setPlaceholderText(text or "")

    def searchText(self):
        return self._input.text()

    def setSearchText(self, text):
        self._input.setText(text or "")

    # ------------------------------------------------------------------ #
    ## Filter chips
    # ------------------------------------------------------------------ #
    def setFilterChips(self, items):
        """Replace all filter chips. Each item is (key, label[, value]) or a
        dict {"key":, "label":, "value":}."""
        self.clearFilterChips()
        for it in (items or []):
            if isinstance(it, dict):
                self.addFilterChip(it.get("key"), it.get("label"), it.get("value"))
            elif isinstance(it, (tuple, list)):
                self.addFilterChip(*it)
            else:
                self.addFilterChip(it, it)

    def addFilterChip(self, key, label, value=None):
        key = str(key)
        if key in self._chips:
            self._chips[key].setText(label, value)
            return
        chip = _FilterChip(key, label, value, self._chipBox)
        chip.removed.connect(self._onChipRemoved)
        self._chipLay.addWidget(chip)
        self._chips[key] = chip
        self._styleChip(chip)

    def removeFilterChip(self, key):
        chip = self._chips.pop(str(key), None)
        if chip is not None:
            self._chipLay.removeWidget(chip)
            chip.deleteLater()

    def clearFilterChips(self):
        for key in list(self._chips.keys()):
            self.removeFilterChip(key)

    def filterChipKeys(self):
        return list(self._chips.keys())

    def _onChipRemoved(self, key):
        self.removeFilterChip(key)
        self.filterChipRemoved.emit(key)

    # ------------------------------------------------------------------ #
    ## Status pills
    # ------------------------------------------------------------------ #
    def setStatuses(self, items):
        """Rebuild the status pills (the built-in All pill is kept first).
        Each item is a dict {"key":, "label":, "count":, "color":}."""
        for key in list(self._pills.keys()):
            if key == self.ALL_KEY:
                continue
            pill = self._pills.pop(key)
            self._pillLay.removeWidget(pill)
            pill.deleteLater()
        for it in (items or []):
            key = str(it.get("key"))
            pill = _StatusPill(key, it.get("label", key), it.get("count"),
                               it.get("color", self._c["accent"]), self._pillBox)
            pill.applyThemeColors(self._c["on_surface"], self._c["muted"],
                                  self._c["surface"])
            pill.clicked.connect(self._onStatusClicked)
            self._pillLay.addWidget(pill)
            self._pills[key] = pill
        self.setActiveStatus(self._activeStatus if self._activeStatus in self._pills
                             else self.ALL_KEY)

    def setStatusCount(self, key, count):
        pill = self._pills.get(str(key))
        if pill is not None:
            pill.setCount(count)

    def setActiveStatus(self, key):
        key = str(key)
        if key not in self._pills:
            key = self.ALL_KEY
        self._activeStatus = key
        for k, pill in self._pills.items():
            pill.setChecked(k == key)

    def activeStatus(self):
        return self._activeStatus

    def _onStatusClicked(self, key):
        self.setActiveStatus(key)
        self.statusSelected.emit(key)

    # ------------------------------------------------------------------ #
    ## Show-statuses switch
    # ------------------------------------------------------------------ #
    def showStatuses(self):
        return self._switch.isChecked()

    def setShowStatuses(self, on):
        self._switch.setChecked(bool(on))

    def _onShowStatusesToggled(self, on):
        self._pillBox.setVisible(on)
        self.showStatusesToggled.emit(on)

    # ------------------------------------------------------------------ #
    ## Theme
    # ------------------------------------------------------------------ #
    def setThemeColors(self, surface=None, on_surface=None, muted=None,
                       outline=None, accent=None):
        """Track the active theme. Pass token role values (call after
        applyDesignTokens). Any omitted colour keeps its current value."""
        for name, val in (("surface", surface), ("on_surface", on_surface),
                          ("muted", muted), ("outline", outline),
                          ("accent", accent)):
            if val:
                self._c[name] = val
        self._applyChrome()

    def _applyChrome(self):
        c = self._c
        # recolour painted glyphs
        self._searchIcon.setPixmap(_glyph_pixmap("search", c["muted"], 16))
        self._filtersBtn.setIcon(QIcon(_glyph_pixmap("sliders", c["on_surface"], 16)))
        self._filtersBtn.setIconSize(QSize(16, 16))
        # the "All" pill borrows the muted hue so it reads as neutral
        self._allPill.setColor(c["muted"])
        for pill in self._pills.values():
            pill.applyThemeColors(c["on_surface"], c["muted"], c["surface"])
        for chip in self._chips.values():
            self._styleChip(chip)
        self.setStyleSheet(self._chromeQss())

    def _styleChip(self, chip):
        c = self._c
        chip.setStyleSheet(
            "#tableFilterChip { background: %s; border: 1px solid %s;"
            " border-radius: 15px; }"
            "#tableFilterChipPrefix { color: %s; background: transparent; }"
            "#tableFilterChipValue { color: %s; font-weight: 600; background: transparent; }"
            "#tableFilterChipClose { color: %s; border: none; font-size: 12px;"
            " padding: 0 2px; background: transparent; }"
            "#tableFilterChipClose:hover { color: %s; }"
            % (_rgba(c["muted"], 0.10), c["outline"], c["muted"],
               c["on_surface"], c["muted"], c["on_surface"]))

    def _chromeQss(self):
        c = self._c
        return (
            "#tableToolbar { background: transparent; }"
            "#tableSearch { background: %(surface)s; border: 1px solid %(outline)s;"
            " border-radius: 20px; }"
            "#tableSearchInput { border: none; background: transparent;"
            " color: %(on_surface)s; font-size: 14px; }"
            "#tableFiltersBtn { background: %(surface)s; color: %(on_surface)s;"
            " border: 1px solid %(outline)s; border-radius: 20px; padding: 8px 16px;"
            " font-weight: 600; }"
            "#tableFiltersBtn:hover { border-color: %(accent)s; color: %(accent)s; }"
            "#tableClearBtn { border: none; background: transparent; color: %(accent)s;"
            " font-weight: 600; padding: 6px 4px; }"
            "#tableClearBtn:hover { text-decoration: underline; }"
            "#tableShowStatusesLabel { color: %(on_surface)s; font-weight: 500; }"
            % c)
