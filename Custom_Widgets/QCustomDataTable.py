########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/spinnTv
# WEBSITE: spinncode.com
########################################################################

########################################################################
## QCustomDataTable - free core basic data table.
##
## This is the first model/view widget in the library. It provides a
## read-only, client-side sortable/filterable table that the commercial
## QCustomDataTablePro extends. See:
##     docs/design/datatable-free-impl-spec.md
##
## Layers in this module:
##   DataTableColumn / QCustomDataTableModel   - the model
##   _PaginationProxy                          - row-windowing pagination
##   QCustomDataTable                          - the QWidget (view + footer)
########################################################################
from enum import IntEnum

from qtpy.QtCore import (
    Qt, QModelIndex, QAbstractTableModel, QAbstractProxyModel,
    QSortFilterProxyModel, Signal, Property, QSize, QRect, QRectF,
)
from qtpy.QtGui import QColor, QFont, QPainter, QPen
from qtpy.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableView, QAbstractItemView,
    QLabel, QPushButton, QStyledItemDelegate, QStyle, QHeaderView,
    QStyleOptionButton, QMenu,
)


########################################################################
## Default per-type cell alignment
########################################################################
_TYPE_ALIGN = {
    "number": Qt.AlignRight | Qt.AlignVCenter,
    "bool":   Qt.AlignCenter,
    "date":   Qt.AlignLeft | Qt.AlignVCenter,
    "text":   Qt.AlignLeft | Qt.AlignVCenter,
}

########################################################################
## Rich-cell model roles (read by QCustomDataTableDelegate)
##
## These extra roles ride the model/proxy chain, so the delegate on the view
## receives them through the sort/filter/pagination proxies unchanged. They
## describe HOW a cell should be drawn (renderer), plus the auxiliary bits a
## rich cell needs (a second line, an explicit colour).
########################################################################
RendererRole = Qt.UserRole + 1     # str: "" | status | link | colored | twoline | badge | currency
SubtitleRole = Qt.UserRole + 2     # str: the second line for the twoline renderer
CellColorRole = Qt.UserRole + 3    # str: an explicit dot/text/badge colour (hex or name)

# The renderers the delegate understands (also the allowed `renderer=` values).
CELL_RENDERERS = ("status", "link", "colored", "twoline", "badge", "currency")

# Synthetic renderer for the trailing row-actions (kebab ⋮) column. Not a valid
# user `renderer=` value - the model advertises it for its own actions column.
ACTIONS_RENDERER = "actions"


class DataTableColumn(object):
    """Lightweight column descriptor for QCustomDataTable.

    key        row-dict key this column reads.
    title      header text (defaults to key).
    type       "text" | "number" | "date" | "bool" - drives default
               alignment and (via the sort proxy) sort comparison.
    width      column width in pixels, or None for automatic.
    align      Qt alignment flag, or None to use the type default.
    formatter  optional callable(value) -> str for display.
    sortable   whether this column may be sorted.

    Rich-cell rendering (drawn by QCustomDataTableDelegate):
    renderer   one of CELL_RENDERERS, or None for a plain text cell:
                 "status"   coloured status dot + link-coloured text
                 "link"     accent/link-coloured text
                 "colored"  text painted in the resolved cell colour
                 "twoline"  bold title (the value) over a muted subtitle
                 "badge"    rounded pill filled with the resolved colour
                 "currency" right-aligned money, optionally coloured
    color      a fixed colour (hex like '#22c55e' or a Qt colour name) used as
               the dot/text/badge colour for this column.
    colorMap   dict {cell value -> colour} - per-value colouring (e.g. a
               status label to its colour). Wins over `color`.
    colorKey   a row-dict key whose value IS the colour for that cell (fully
               per-row). Wins over colorMap/color.
    subtitleKey  row-dict key for the second line of a "twoline" cell.
    """

    def __init__(self, key, title=None, type="text", width=None,
                 align=None, formatter=None, sortable=True,
                 renderer=None, color=None, colorMap=None, colorKey=None,
                 subtitleKey=None):
        self.key = key
        self.title = key if title is None else title
        self.type = type
        self.width = width
        self.align = align
        self.formatter = formatter
        self.sortable = sortable
        self.renderer = renderer
        self.color = color
        self.colorMap = colorMap
        self.colorKey = colorKey
        self.subtitleKey = subtitleKey

    @classmethod
    def ensure(cls, column):
        """Coerce a DataTableColumn, dict, or bare key into a DataTableColumn."""
        if isinstance(column, cls):
            return column
        if isinstance(column, dict):
            return cls(**column)
        return cls(str(column))

    def defaultAlign(self):
        return _TYPE_ALIGN.get(self.type, _TYPE_ALIGN["text"])

    def resolveColor(self, value, row):
        """The explicit colour for a cell, from colorKey > colorMap > color,
        or "" when the column carries no colour rule."""
        if self.colorKey and isinstance(row, dict):
            got = row.get(self.colorKey)
            if got:
                return str(got)
        if self.colorMap and value in self.colorMap:
            return str(self.colorMap[value])
        return str(self.color) if self.color else ""

    def subtitle(self, row):
        """The second-line text for a twoline cell (or "")."""
        if self.subtitleKey and isinstance(row, dict):
            val = row.get(self.subtitleKey)
            return "" if val is None else str(val)
        return ""


class QCustomDataTableModel(QAbstractTableModel):
    """Simple in-memory table model backed by a list of row dicts.

    Columns are DataTableColumn descriptors; rows are dicts keyed by
    ``column.key``. The model is read-only in the free tier (editing lives
    in QCustomDataTablePro).

    The raw, unformatted cell value is exposed through ``Qt.UserRole`` so a
    QSortFilterProxyModel configured with ``setSortRole(Qt.UserRole)`` sorts
    by real Python types instead of the display string. This raw-value seam
    is part of the stable contract the Pro model relies on.

    Two optional synthetic columns bracket the data columns:
      * a leading **select** column (``selectable``) - a per-row checkbox via
        ``Qt.CheckStateRole``; checked source rows live in ``_checked``.
      * a trailing **actions** column (``rowActions``) - advertises the
        ``ACTIONS_RENDERER`` so the delegate paints a kebab (⋮); the widget
        turns a click into a menu + ``rowActionTriggered``.
    Both keep the data columns' meaning intact - view/model column indices are
    translated back to a ``DataTableColumn`` through the select offset.
    """

    # emitted whenever the set of checked rows changes (toggle / select-all)
    checkedChanged = Signal()

    def __init__(self, columns=None, rows=None, parent=None,
                 selectable=False, rowActions=None):
        super().__init__(parent)
        self._columns = [DataTableColumn.ensure(c) for c in (columns or [])]
        self._rows = list(rows or [])
        self._selectable = bool(selectable)
        self._rowActions = self._normalizeActions(rowActions)
        self._checked = set()          # source-row indices that are checked

    # ------------------------------------------------------------------ #
    ## Qt model interface
    # ------------------------------------------------------------------ #
    def rowCount(self, parent=QModelIndex()):
        return 0 if parent.isValid() else len(self._rows)

    def columnCount(self, parent=QModelIndex()):
        if parent.isValid():
            return 0
        extra = (1 if self._selectable else 0) + (1 if self._rowActions else 0)
        return len(self._columns) + extra

    # -- synthetic-column geometry -------------------------------------- #
    def _selOffset(self):
        return 1 if self._selectable else 0

    def _columnKind(self, col):
        """'select' | 'actions' | 'data' for a view/model column index."""
        if self._selectable and col == 0:
            return "select"
        if self._rowActions and col == self.columnCount() - 1:
            return "actions"
        return "data"

    def _dataColumnAt(self, col):
        """The DataTableColumn behind a view/model column, or None if the
        column is a synthetic select/actions column or out of range."""
        if self._columnKind(col) != "data":
            return None
        idx = col - self._selOffset()
        return self._columns[idx] if 0 <= idx < len(self._columns) else None

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None
        row, col = index.row(), index.column()
        if not (0 <= row < len(self._rows)) or not (0 <= col < self.columnCount()):
            return None
        kind = self._columnKind(col)
        if kind == "select":
            if role == Qt.CheckStateRole:
                return Qt.Checked if row in self._checked else Qt.Unchecked
            if role == Qt.TextAlignmentRole:
                return int(Qt.AlignCenter)
            return None
        if kind == "actions":
            if role == RendererRole:
                return ACTIONS_RENDERER
            if role == Qt.TextAlignmentRole:
                return int(Qt.AlignCenter)
            return None

        column = self._dataColumnAt(col)
        if column is None:
            return None
        value = self._rows[row].get(column.key)

        if role == Qt.DisplayRole or role == Qt.EditRole:
            return self._display(column, value)
        if role == Qt.TextAlignmentRole:
            align = column.align if column.align is not None else column.defaultAlign()
            return int(align)
        if role == Qt.UserRole:
            return value
        if role == RendererRole:
            return column.renderer or ""
        if role == SubtitleRole:
            return column.subtitle(self._rows[row])
        if role == CellColorRole:
            return column.resolveColor(value, self._rows[row])
        return None

    def setData(self, index, value, role=Qt.EditRole):
        """Only the select column is writable (its checkbox) in the free tier."""
        if not index.isValid():
            return False
        if role == Qt.CheckStateRole and self._columnKind(index.column()) == "select":
            # value may arrive as an int or a Qt.CheckState enum (PySide6 6.x)
            checked = Qt.CheckState(value) == Qt.CheckState.Checked
            if self._applyChecked(index.row(), checked):
                self.dataChanged.emit(index, index, [Qt.CheckStateRole])
                self.checkedChanged.emit()
            return True
        return False

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            kind = self._columnKind(section)
            if kind != "data":
                return ""  # select/actions headers are painted, not labelled
            column = self._dataColumnAt(section)
            return column.title if column is not None else None
        return section + 1  # 1-based row numbers on the vertical header

    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags
        base = Qt.ItemIsEnabled | Qt.ItemIsSelectable
        if self._columnKind(index.column()) == "select":
            return base | Qt.ItemIsUserCheckable
        return base

    def removeRows(self, row, count, parent=QModelIndex()):
        if parent.isValid() or count <= 0 or row < 0 or row + count > len(self._rows):
            return False
        self.beginRemoveRows(QModelIndex(), row, row + count - 1)
        del self._rows[row:row + count]
        self._shiftCheckedAfterRemoval(row, count)
        self.endRemoveRows()
        return True

    # ------------------------------------------------------------------ #
    ## Data API
    # ------------------------------------------------------------------ #
    def columns(self):
        return list(self._columns)

    def setColumns(self, columns):
        self.beginResetModel()
        self._columns = [DataTableColumn.ensure(c) for c in (columns or [])]
        self.endResetModel()

    def rows(self):
        return list(self._rows)

    def setRows(self, rows):
        self.beginResetModel()
        self._rows = list(rows or [])
        self._checked.clear()
        self.endResetModel()
        self.checkedChanged.emit()

    def addRow(self, row):
        pos = len(self._rows)
        self.beginInsertRows(QModelIndex(), pos, pos)
        self._rows.append(dict(row))
        self.endInsertRows()

    def addRows(self, rows):
        rows = list(rows or [])
        if not rows:
            return
        pos = len(self._rows)
        self.beginInsertRows(QModelIndex(), pos, pos + len(rows) - 1)
        self._rows.extend(dict(r) for r in rows)
        self.endInsertRows()

    def clear(self):
        if not self._rows:
            return
        self.beginResetModel()
        self._rows = []
        self._checked.clear()
        self.endResetModel()
        self.checkedChanged.emit()

    def rawValue(self, row, col):
        """Unformatted cell value at (row, col) in source coordinates.

        ``col`` indexes the DATA columns (0-based, ignoring any synthetic
        select/actions columns), matching the stable Pro contract."""
        if 0 <= row < len(self._rows) and 0 <= col < len(self._columns):
            return self._rows[row].get(self._columns[col].key)
        return None

    # ------------------------------------------------------------------ #
    ## Selection (checkbox) column + row-actions (kebab) column
    # ------------------------------------------------------------------ #
    @staticmethod
    def _normalizeActions(actions):
        """Coerce a row-actions spec into a list of (key, label) tuples.
        Accepts (key, label) pairs, {"key":, "label":} dicts, or bare strings."""
        out = []
        for a in (actions or []):
            if isinstance(a, dict):
                key = a.get("key", a.get("label"))
                label = a.get("label", a.get("key"))
                if key is not None:
                    out.append((str(key), str(label)))
            elif isinstance(a, (tuple, list)) and len(a) >= 2:
                out.append((str(a[0]), str(a[1])))
            elif a is not None:
                out.append((str(a), str(a)))
        return out

    def _applyChecked(self, row, checked):
        """Add/remove a source row from the checked set. Returns True if the
        set actually changed."""
        if not (0 <= row < len(self._rows)):
            return False
        if checked and row not in self._checked:
            self._checked.add(row)
            return True
        if not checked and row in self._checked:
            self._checked.discard(row)
            return True
        return False

    def _shiftCheckedAfterRemoval(self, row, count):
        shifted = set()
        for r in self._checked:
            if r < row:
                shifted.add(r)
            elif r >= row + count:
                shifted.add(r - count)
            # rows inside [row, row+count) were removed -> dropped
        self._checked = shifted

    def isSelectable(self):
        return self._selectable

    def setSelectable(self, on):
        on = bool(on)
        if on == self._selectable:
            return
        self.beginResetModel()
        self._selectable = on
        if not on:
            self._checked.clear()
        self.endResetModel()
        self.checkedChanged.emit()

    def rowActions(self):
        return list(self._rowActions)

    def setRowActions(self, actions):
        self.beginResetModel()
        self._rowActions = self._normalizeActions(actions)
        self.endResetModel()

    def checkedRows(self):
        """Sorted source-row indices whose checkbox is ticked."""
        return sorted(self._checked)

    def setRowChecked(self, row, checked=True):
        if self._applyChecked(row, bool(checked)):
            if self._selectable:
                idx = self.index(row, 0)
                self.dataChanged.emit(idx, idx, [Qt.CheckStateRole])
            self.checkedChanged.emit()

    def setAllChecked(self, checked):
        target = set(range(len(self._rows))) if checked else set()
        if target == self._checked:
            return
        self._checked = target
        if self._selectable and self._rows:
            self.dataChanged.emit(self.index(0, 0),
                                  self.index(len(self._rows) - 1, 0),
                                  [Qt.CheckStateRole])
        self.checkedChanged.emit()

    def headerCheckState(self):
        """Tri-state for the select-all header: 0 none, 1 some, 2 all."""
        n = len(self._checked)
        if n == 0:
            return 0
        return 2 if n >= len(self._rows) else 1

    # ------------------------------------------------------------------ #
    ## Formatting helpers
    # ------------------------------------------------------------------ #
    def _display(self, column, value):
        if column.formatter is not None:
            try:
                return column.formatter(value)
            except Exception:
                pass  # fall back to the default formatting on a bad formatter
        return self._format(column, value)

    @staticmethod
    def _format(column, value):
        if value is None:
            return ""
        if column.type == "bool":
            return "Yes" if value else "No"
        return str(value)


class _PaginationProxy(QAbstractProxyModel):
    """Row-windowing proxy exposing only the current page of its source.

    Sits on top of the sort/filter proxy: proxy row r maps to source row
    ``r + page * pageSize``. Columns pass through unchanged. Page count and
    clamping track the (already sorted/filtered) source row count, so sorting
    and filtering upstream automatically reshape the visible page.

    The free tier uses this for classic pagination; Pro replaces the whole
    chain with a virtualized model and drops pagination entirely.
    """

    paginationChanged = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._pageSize = 25
        self._page = 0

    # ------------------------------------------------------------------ #
    ## Pagination state
    # ------------------------------------------------------------------ #
    def _offset(self):
        return self._page * self._pageSize if self._pageSize > 0 else 0

    def pageSize(self):
        return self._pageSize

    def setPageSize(self, size):
        size = max(0, int(size))
        if size == self._pageSize:
            return
        self.beginResetModel()
        self._pageSize = size
        self._clampPage()
        self.endResetModel()
        self.paginationChanged.emit()

    def page(self):
        return self._page

    def setPage(self, page):
        page = self._clampValue(page)
        if page == self._page:
            return
        self.beginResetModel()
        self._page = page
        self.endResetModel()
        self.paginationChanged.emit()

    def pageCount(self):
        src = self.sourceModel()
        if src is None or self._pageSize <= 0:
            return 1
        total = src.rowCount()
        return max(1, (total + self._pageSize - 1) // self._pageSize)

    def _clampValue(self, page):
        return max(0, min(int(page), self.pageCount() - 1))

    def _clampPage(self):
        self._page = self._clampValue(self._page)

    # ------------------------------------------------------------------ #
    ## Source model tracking (QAbstractProxyModel does not auto-connect)
    # ------------------------------------------------------------------ #
    def setSourceModel(self, source):
        prev = self.sourceModel()
        if prev is not None:
            for sig in (prev.modelReset, prev.layoutChanged, prev.rowsInserted,
                        prev.rowsRemoved, prev.columnsInserted, prev.columnsRemoved):
                try:
                    sig.disconnect(self._sourceReshaped)
                except (TypeError, RuntimeError):
                    pass
            try:
                prev.dataChanged.disconnect(self._sourceDataChanged)
            except (TypeError, RuntimeError):
                pass
        super().setSourceModel(source)
        if source is not None:
            source.modelReset.connect(self._sourceReshaped)
            source.layoutChanged.connect(self._sourceReshaped)
            source.rowsInserted.connect(self._sourceReshaped)
            source.rowsRemoved.connect(self._sourceReshaped)
            source.columnsInserted.connect(self._sourceReshaped)
            source.columnsRemoved.connect(self._sourceReshaped)
            source.dataChanged.connect(self._sourceDataChanged)
        self._sourceReshaped()

    def _sourceReshaped(self, *args):
        self.beginResetModel()
        self._clampPage()
        self.endResetModel()
        self.paginationChanged.emit()

    def _sourceDataChanged(self, topLeft, bottomRight, roles=None):
        rows, cols = self.rowCount(), self.columnCount()
        if rows > 0 and cols > 0:
            self.dataChanged.emit(self.index(0, 0), self.index(rows - 1, cols - 1),
                                  roles or [])

    # ------------------------------------------------------------------ #
    ## QAbstractProxyModel interface
    # ------------------------------------------------------------------ #
    def rowCount(self, parent=QModelIndex()):
        src = self.sourceModel()
        if parent.isValid() or src is None:
            return 0
        total = src.rowCount()
        if self._pageSize <= 0:
            return total
        return max(0, min(self._pageSize, total - self._offset()))

    def columnCount(self, parent=QModelIndex()):
        src = self.sourceModel()
        if parent.isValid() or src is None:
            return 0
        return src.columnCount()

    def index(self, row, column, parent=QModelIndex()):
        if parent.isValid():
            return QModelIndex()
        if 0 <= row < self.rowCount() and 0 <= column < self.columnCount():
            return self.createIndex(row, column)
        return QModelIndex()

    def parent(self, index=QModelIndex()):
        return QModelIndex()

    def mapToSource(self, proxyIndex):
        src = self.sourceModel()
        if src is None or not proxyIndex.isValid():
            return QModelIndex()
        return src.index(proxyIndex.row() + self._offset(), proxyIndex.column())

    def mapFromSource(self, sourceIndex):
        if not sourceIndex.isValid():
            return QModelIndex()
        row = sourceIndex.row() - self._offset()
        if 0 <= row < self.rowCount():
            return self.createIndex(row, sourceIndex.column())
        return QModelIndex()

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        src = self.sourceModel()
        if src is None:
            return None
        if orientation == Qt.Vertical:
            return src.headerData(section + self._offset(), orientation, role)
        return src.headerData(section, orientation, role)

    def sort(self, column, order=Qt.AscendingOrder):
        src = self.sourceModel()
        if src is not None:
            src.sort(column, order)


class QCustomDataTableDelegate(QStyledItemDelegate):
    """Paints rich cells for QCustomDataTable from the model's RendererRole /
    SubtitleRole / CellColorRole. Plain cells (no renderer) fall through to the
    default QStyledItemDelegate, so ordinary columns are untouched.

    Colours come from the column rules (hex or Qt colour names). The link/status
    accent and the muted subtitle colour default to the view's palette (so they
    track the active theme) and can be overridden with setAccentColor /
    setMutedColor.
    """

    _PAD = 10       # horizontal text inset (matches the spacing token scale)
    _DOT = 8        # status-dot diameter
    _GAP = 8        # gap after the status dot

    def __init__(self, parent=None):
        super().__init__(parent)
        self._accent = None
        self._muted = None

    def setAccentColor(self, color):
        """Colour for link text and (by default) status text. None -> palette."""
        self._accent = QColor(color) if color else None

    def setMutedColor(self, color):
        """Colour for the muted second line of twoline cells. None -> palette."""
        self._muted = QColor(color) if color else None

    # ------------------------------------------------------------------ #
    ## colour helpers
    # ------------------------------------------------------------------ #
    def _accentColor(self, option):
        return QColor(self._accent) if self._accent else option.palette.link().color()

    def _mutedColor(self, option):
        if self._muted:
            return QColor(self._muted)
        c = QColor(option.palette.text().color())
        c.setAlpha(150)
        return c

    def _onSelection(self, option):
        return bool(option.state & QStyle.State_Selected)

    def _textColor(self, option, explicit, fallback=None):
        if self._onSelection(option):
            return option.palette.highlightedText().color()
        if explicit:
            return QColor(explicit)
        return fallback if fallback is not None else option.palette.text().color()

    def _elide(self, option, text, width):
        return option.fontMetrics.elidedText(text, Qt.ElideRight, max(0, int(width)))

    # ------------------------------------------------------------------ #
    ## paint
    # ------------------------------------------------------------------ #
    def paint(self, painter, option, index):
        renderer = index.data(RendererRole) or ""
        if renderer == ACTIONS_RENDERER:
            return self._paintActions(painter, option, index)
        if renderer not in CELL_RENDERERS:
            return super().paint(painter, option, index)

        self.initStyleOption(option, index)
        text = str(index.data(Qt.DisplayRole) or "")
        color = index.data(CellColorRole) or ""
        rect = option.rect.adjusted(self._PAD, 0, -self._PAD, 0)

        painter.save()
        painter.setRenderHint(QPainter.Antialiasing, True)
        if self._onSelection(option):
            painter.fillRect(option.rect, option.palette.highlight())
        try:
            if renderer == "twoline":
                self._paintTwoLine(painter, option, rect, text,
                                   str(index.data(SubtitleRole) or ""), color)
            elif renderer == "badge":
                self._paintBadge(painter, option, rect, text, color)
            elif renderer == "status":
                self._paintStatus(painter, option, rect, text, color)
            else:  # link | colored | currency
                self._paintText(painter, option, rect, text, renderer, color)
        finally:
            painter.restore()

    def _paintText(self, painter, option, rect, text, renderer, color):
        if renderer == "link":
            col = (option.palette.highlightedText().color()
                   if self._onSelection(option)
                   else (QColor(color) if color else self._accentColor(option)))
        else:  # colored | currency
            col = self._textColor(option, color)
        align = Qt.AlignVCenter | (Qt.AlignRight if renderer == "currency"
                                   else Qt.AlignLeft)
        painter.setPen(QPen(col))
        painter.drawText(rect, int(align), self._elide(option, text, rect.width()))

    def _paintStatus(self, painter, option, rect, text, color):
        cy = rect.center().y()
        dot = QColor(color) if color else self._accentColor(option)
        painter.setPen(Qt.NoPen)
        painter.setBrush(dot)
        painter.drawEllipse(QRectF(rect.left(), cy - self._DOT / 2.0,
                                   self._DOT, self._DOT))
        text_rect = rect.adjusted(self._DOT + self._GAP, 0, 0, 0)
        col = (option.palette.highlightedText().color()
               if self._onSelection(option) else self._accentColor(option))
        painter.setPen(QPen(col))
        painter.drawText(text_rect, int(Qt.AlignVCenter | Qt.AlignLeft),
                         self._elide(option, text, text_rect.width()))

    def _paintBadge(self, painter, option, rect, text, color):
        base = QColor(color) if color else self._accentColor(option)
        fm = option.fontMetrics
        tw = fm.horizontalAdvance(text)
        h = min(rect.height() - 8, fm.height() + 8)
        w = tw + 20
        pill = QRectF(rect.left(), rect.center().y() - h / 2.0, w, h)
        bg = QColor(base)
        bg.setAlpha(38)                      # soft tinted fill
        painter.setPen(Qt.NoPen)
        painter.setBrush(bg)
        painter.drawRoundedRect(pill, h / 2.0, h / 2.0)
        painter.setPen(QPen(base))
        painter.drawText(pill, int(Qt.AlignCenter), text)

    def _paintActions(self, painter, option, index):
        """Trailing row-actions cell: a centred kebab (vertical ellipsis)."""
        self.initStyleOption(option, index)
        painter.save()
        painter.setRenderHint(QPainter.Antialiasing, True)
        selected = self._onSelection(option)
        if selected:
            painter.fillRect(option.rect, option.palette.highlight())
        hovered = bool(option.state & QStyle.State_MouseOver)
        col = (option.palette.highlightedText().color() if selected
               else (self._accentColor(option) if hovered
                     else self._mutedColor(option)))
        f = QFont(option.font)
        f.setPointSizeF(option.font.pointSizeF() + 3)
        f.setBold(True)
        painter.setFont(f)
        painter.setPen(QPen(col))
        painter.drawText(option.rect, int(Qt.AlignCenter), "⋮")  # ⋮
        painter.restore()

    def _paintTwoLine(self, painter, option, rect, title, subtitle, color):
        fm = option.fontMetrics
        line = fm.height()
        block = line * 2
        top = rect.top() + max(0, (rect.height() - block) // 2)
        title_rect = QRectF(rect.left(), top, rect.width(), line)
        sub_rect = QRectF(rect.left(), top + line, rect.width(), line)
        title_col = self._textColor(option, color)
        if color:
            sub_col = self._textColor(option, color)
        else:
            sub_col = (option.palette.highlightedText().color()
                       if self._onSelection(option) else self._mutedColor(option))
        painter.setPen(QPen(title_col))
        painter.drawText(title_rect, int(Qt.AlignVCenter | Qt.AlignLeft),
                         self._elide(option, title, rect.width()))
        if subtitle:
            f = QFont(option.font)
            f.setPointSizeF(max(1.0, option.font.pointSizeF() - 1))
            painter.setFont(f)
            painter.setPen(QPen(sub_col))
            painter.drawText(sub_rect, int(Qt.AlignVCenter | Qt.AlignLeft),
                             self._elide(option, subtitle, rect.width()))

    def sizeHint(self, option, index):
        base = super().sizeHint(option, index)
        renderer = index.data(RendererRole) or ""
        rich = renderer in CELL_RENDERERS or renderer == ACTIONS_RENDERER
        min_h = 44 if rich else base.height()
        if renderer == "twoline":
            self.initStyleOption(option, index)
            min_h = max(min_h, option.fontMetrics.height() * 2 + 16)
        return QSize(base.width(), max(base.height(), min_h))


class _SelectAllHeader(QHeaderView):
    """Horizontal header that paints a tri-state select-all checkbox in the
    select column and turns a click there into ``selectAllToggled`` instead of
    a sort. All other sections behave like a normal sortable header.
    """

    selectAllToggled = Signal(bool)

    def __init__(self, orientation=Qt.Horizontal, parent=None):
        super().__init__(orientation, parent)
        self._checkCol = -1
        self._state = 0                 # 0 none, 1 some, 2 all
        self.setSectionsClickable(True)
        self.setHighlightSections(False)

    def setCheckColumn(self, col):
        if col == self._checkCol:
            return
        old = self._checkCol
        self._checkCol = col
        for c in (old, col):
            if c is not None and c >= 0:
                self.updateSection(c)

    def setCheckState(self, state):
        state = int(state)
        if state != self._state:
            self._state = state
            if self._checkCol >= 0:
                self.updateSection(self._checkCol)

    def paintSection(self, painter, rect, logicalIndex):
        super().paintSection(painter, rect, logicalIndex)
        if logicalIndex != self._checkCol:
            return
        opt = QStyleOptionButton()
        sz = 16
        opt.rect = QRect(rect.center().x() - sz // 2,
                         rect.center().y() - sz // 2, sz, sz)
        if self._state == 2:
            opt.state = QStyle.State_On | QStyle.State_Enabled
        elif self._state == 1:
            opt.state = QStyle.State_NoChange | QStyle.State_Enabled
        else:
            opt.state = QStyle.State_Off | QStyle.State_Enabled
        self.style().drawPrimitive(QStyle.PE_IndicatorCheckBox, opt, painter, self)

    def mouseReleaseEvent(self, event):
        if (self._checkCol >= 0
                and self.logicalIndexAt(event.pos()) == self._checkCol):
            # not all -> select all; already all -> clear. Swallow the event so
            # the section does not also emit a sort click.
            self.selectAllToggled.emit(self._state != 2)
            return
        super().mouseReleaseEvent(event)


class QCustomDataTable(QWidget):
    """Modern, read-only data table with client-side sort, filter and
    optional pagination. Styled through the theme/token system.

    This is the free-core base that QCustomDataTablePro extends. The
    ``_createModel`` / ``_createView`` factories and the model's
    ``Qt.UserRole`` raw-value seam are the stable Pro extension contract.
    """

    # -- Designer registration constants --
    WIDGET_ICON = "components/icons/table.png"
    WIDGET_TOOLTIP = "A modern data table with sort, filter and pagination"
    WIDGET_MODULE = "Custom_Widgets.QCustomDataTable"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomDataTable' name='customDataTable'>
            <property name='geometry'>
                <rect>
                    <x>0</x>
                    <y>0</y>
                    <width>480</width>
                    <height>320</height>
                </rect>
            </property>
        </widget>
    </ui>
    """

    # -- Rich editors for the Designer "Custom Properties" dock --
    DESIGNER_CUSTOM_PROPS = [
        {"name": "pageSize", "kind": "int", "group": "Data Table"},
        {"name": "showPagination", "kind": "bool", "group": "Data Table"},
        {"name": "selectionMode", "kind": "choice", "enum": "SelectionMode",
         "group": "Data Table"},
        {"name": "selectable", "kind": "bool", "group": "Data Table"},
        {"name": "sortable", "kind": "bool", "group": "Data Table"},
        {"name": "filterable", "kind": "bool", "group": "Data Table"},
        {"name": "alternatingRowColors", "kind": "bool", "group": "Appearance"},
        {"name": "showGrid", "kind": "bool", "group": "Appearance"},
        {"name": "showHeader", "kind": "bool", "group": "Appearance"},
        {"name": "variant", "kind": "str", "group": "Appearance"},
        {"name": "sizeVariant", "kind": "str", "group": "Appearance"},
    ]

    # -- Machine-readable catalog (MCP / agent introspection) --
    __catalog__ = {
        "name": "QCustomDataTable",
        "props": {
            "pageSize": {"type": "int", "default": 25},
            "selectionMode": {"type": "enum",
                              "values": ["NoSelection", "SingleRow", "MultiRow", "Cell"],
                              "default": "SingleRow"},
            "variant": {"type": "enum",
                        "values": ["primary", "secondary", "outline", "ghost"],
                        "default": "outline"},
            "sizeVariant": {"type": "enum", "values": ["sm", "md", "lg"],
                            "default": "md"},
        },
        "signals": ["rowSelected", "cellClicked", "sortChanged", "pageChanged",
                    "rowActionTriggered", "selectionCheckedChanged"],
        "tokens_used": ["surface", "on-surface", "surface-muted", "outline",
                        "accent", "focus-ring"],
    }

    class SelectionMode(IntEnum):
        NoSelection = 0
        SingleRow = 1
        MultiRow = 2
        Cell = 3

    # -- signals (all row indices are SOURCE-model coordinates) --
    rowSelected = Signal(int)
    cellClicked = Signal(int, int)
    sortChanged = Signal(int, object)
    pageChanged = Signal(int)
    rowActionTriggered = Signal(int, str)      # (source row, action key) from the ⋮ menu
    selectionCheckedChanged = Signal(list)     # checked source rows (checkbox column)

    def __init__(self, parent=None):
        super().__init__(parent)
        # defaults
        self._pageSize = 25
        self._showPagination = True
        self._selectionMode = QCustomDataTable.SelectionMode.SingleRow
        self._sortable = True
        self._filterable = True
        self._alternatingRowColors = True
        self._showGrid = False
        self._showHeader = True
        self._variant = "outline"
        self._sizeVariant = "md"
        self._pageProxy = None
        self._selModel = None
        self._lastPage = -1

        # model chain: model -> sort/filter -> (pagination) -> view
        self._model = self._createModel()
        # keep the select-all header + listeners in sync with checkbox state
        self._model.checkedChanged.connect(self._onModelCheckedChanged)
        self._sortFilter = QSortFilterProxyModel(self)
        self._sortFilter.setSourceModel(self._model)
        self._sortFilter.setSortRole(Qt.UserRole)
        self._sortFilter.setFilterKeyColumn(-1)
        self._sortFilter.setFilterCaseSensitivity(Qt.CaseInsensitive)

        self._view = self._createView()
        self._buildUi()
        self._installModel()
        self._applyViewProps()

    # ------------------------------------------------------------------ #
    ## Overridable factories (Pro overrides these)
    # ------------------------------------------------------------------ #
    def _createModel(self):
        return QCustomDataTableModel(parent=self)

    def _createView(self):
        return QTableView(self)

    def _createDelegate(self):
        return QCustomDataTableDelegate(self._view)

    # ------------------------------------------------------------------ #
    ## UI
    # ------------------------------------------------------------------ #
    def _buildUi(self):
        self.setObjectName("QCustomDataTable")
        # let QSS background-color paint on these plain QWidget containers
        self.setAttribute(Qt.WA_StyledBackground, True)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self._view.setObjectName("dataTableView")
        self._view.verticalHeader().setVisible(False)
        self._view.setEditTriggers(QAbstractItemView.NoEditTriggers)  # read-only in free tier
        self._view.setWordWrap(False)
        # select-all-aware header (paints the header checkbox for the select column)
        self._hheader = _SelectAllHeader(Qt.Horizontal, self._view)
        self._view.setHorizontalHeader(self._hheader)
        self._hheader.setStretchLastSection(True)
        self._hheader.selectAllToggled.connect(self._onSelectAllToggled)
        # rich-cell painting (status dots, links, badges, two-line, currency);
        # plain columns fall through to default rendering.
        self._delegate = self._createDelegate()
        self._view.setItemDelegate(self._delegate)
        self._view.setMouseTracking(True)   # so the ⋮ cell can react to hover
        layout.addWidget(self._view)

        self._footer = QWidget(self)
        self._footer.setObjectName("dataTableFooter")
        self._footer.setAttribute(Qt.WA_StyledBackground, True)
        foot = QHBoxLayout(self._footer)
        foot.setContentsMargins(8, 4, 8, 4)
        self._prevBtn = QPushButton("Previous", self._footer)
        self._prevBtn.setObjectName("dataTablePrev")
        self._nextBtn = QPushButton("Next", self._footer)
        self._nextBtn.setObjectName("dataTableNext")
        self._pageLabel = QLabel("", self._footer)
        self._pageLabel.setObjectName("dataTablePageLabel")
        self._pageLabel.setAlignment(Qt.AlignCenter)
        foot.addWidget(self._prevBtn)
        foot.addStretch(1)
        foot.addWidget(self._pageLabel)
        foot.addStretch(1)
        foot.addWidget(self._nextBtn)
        layout.addWidget(self._footer)

        self._prevBtn.clicked.connect(self.prevPage)
        self._nextBtn.clicked.connect(self.nextPage)
        self._view.clicked.connect(self._onCellClicked)
        self._view.horizontalHeader().sortIndicatorChanged.connect(self._onSortIndicatorChanged)

    def _installModel(self):
        """(Re)build the view's model chain based on pagination settings."""
        paginate = self._showPagination and self._pageSize > 0
        if paginate:
            if self._pageProxy is None:
                self._pageProxy = _PaginationProxy(self)
                self._pageProxy.paginationChanged.connect(self._onPaginationChanged)
            self._pageProxy.setPageSize(self._pageSize)
            self._pageProxy.setSourceModel(self._sortFilter)
            self._setViewModel(self._pageProxy)
        else:
            self._setViewModel(self._sortFilter)
        self._footer.setVisible(paginate)
        self._configureColumns()
        self._onPaginationChanged()

    def _setViewModel(self, model):
        if self._selModel is not None:
            try:
                self._selModel.currentRowChanged.disconnect(self._onCurrentRowChanged)
            except (TypeError, RuntimeError):
                pass
        self._view.setModel(model)
        self._selModel = self._view.selectionModel()
        if self._selModel is not None:
            self._selModel.currentRowChanged.connect(self._onCurrentRowChanged)

    def _applyViewProps(self):
        self._view.setAlternatingRowColors(self._alternatingRowColors)
        self._view.setShowGrid(self._showGrid)
        self._view.horizontalHeader().setVisible(self._showHeader)
        self._view.setSortingEnabled(self._sortable)
        if self._sortable:
            # setSortingEnabled(True) otherwise auto-sorts by column 0; start
            # unsorted so rows show in insertion order until a header is clicked.
            self._view.horizontalHeader().setSortIndicator(-1, Qt.AscendingOrder)
        self._applySelectionMode()

    def _applySelectionMode(self):
        mode = self._selectionMode
        SM = QCustomDataTable.SelectionMode
        if mode == SM.NoSelection:
            self._view.setSelectionMode(QAbstractItemView.NoSelection)
        elif mode == SM.MultiRow:
            self._view.setSelectionBehavior(QAbstractItemView.SelectRows)
            self._view.setSelectionMode(QAbstractItemView.ExtendedSelection)
        elif mode == SM.Cell:
            self._view.setSelectionBehavior(QAbstractItemView.SelectItems)
            self._view.setSelectionMode(QAbstractItemView.SingleSelection)
        else:  # SingleRow
            self._view.setSelectionBehavior(QAbstractItemView.SelectRows)
            self._view.setSelectionMode(QAbstractItemView.SingleSelection)

    # -- column width unit for the synthetic select/actions columns --
    _SYNTH_COL_WIDTH = 46

    def _applyColumnWidths(self):
        """Apply DataTableColumn.width values, offset past the select column."""
        off = self._model._selOffset()
        for i, col in enumerate(self._model.columns()):
            if col.width:
                self._view.setColumnWidth(i + off, int(col.width))

    def _configureColumns(self):
        """Size + resize-mode the columns, including the synthetic select/actions
        columns (fixed & narrow), and tell the header which column carries the
        select-all checkbox."""
        header = self._hheader
        vm = self._view.model()
        n = vm.columnCount() if vm is not None else 0
        selCol = 0 if self._model.isSelectable() else -1
        actCol = n - 1 if self._model.rowActions() else -1

        header.setCheckColumn(selCol)
        # a trailing actions column must stay narrow, so don't stretch the last
        # section; otherwise let the last data column fill the width.
        header.setStretchLastSection(actCol < 0)
        for i in range(n):
            if i in (selCol, actCol):
                header.setSectionResizeMode(i, QHeaderView.Fixed)
                self._view.setColumnWidth(i, self._SYNTH_COL_WIDTH)
            else:
                header.setSectionResizeMode(i, QHeaderView.Interactive)
        self._applyColumnWidths()
        # with an actions column pinned last, stretch the final DATA column so
        # the table still fills its width.
        if actCol > 0:
            stretch = actCol - 1
            if stretch != selCol and stretch >= 0:
                header.setSectionResizeMode(stretch, QHeaderView.Stretch)
        self._syncHeaderCheckState()

    def _repolish(self):
        self.style().unpolish(self)
        self.style().polish(self)
        self.update()

    # ------------------------------------------------------------------ #
    ## Data API
    # ------------------------------------------------------------------ #
    def setColumns(self, columns):
        self._model.setColumns(columns)
        self._configureColumns()

    def setData(self, rows):
        self._model.setRows(rows)
        self.setPage(0)

    setRows = setData

    def addRow(self, row):
        self._model.addRow(row)

    def clear(self):
        self._model.clear()

    def model(self):
        return self._model

    def view(self):
        return self._view

    def delegate(self):
        return self._delegate

    def setCellAccentColor(self, color):
        """Colour used for link/status cell text (blank/None -> palette link)."""
        self._delegate.setAccentColor(color)

    def setCellMutedColor(self, color):
        """Colour used for the muted second line of twoline cells."""
        self._delegate.setMutedColor(color)

    # ------------------------------------------------------------------ #
    ## Selection column (checkboxes) + row-actions (kebab)
    # ------------------------------------------------------------------ #
    def isSelectable(self):
        return self._model.isSelectable()

    def setSelectable(self, on):
        """Show/hide the leading checkbox column (with a select-all header)."""
        self._model.setSelectable(bool(on))
        self._configureColumns()

    def setRowActions(self, actions):
        """Enable the trailing ⋮ column. ``actions`` is a list of (key, label)
        pairs, {"key":, "label":} dicts, or bare strings; picking one emits
        ``rowActionTriggered(sourceRow, key)``."""
        self._model.setRowActions(actions)
        self._configureColumns()

    def rowActions(self):
        return self._model.rowActions()

    def checkedRows(self):
        """Sorted SOURCE-model row indices whose checkbox is ticked."""
        return self._model.checkedRows()

    def setRowChecked(self, row, checked=True):
        self._model.setRowChecked(row, checked)

    def setAllChecked(self, checked=True):
        self._model.setAllChecked(checked)

    def clearChecked(self):
        self._model.setAllChecked(False)

    # -- internal wiring -------------------------------------------------- #
    def _onSelectAllToggled(self, checked):
        self._model.setAllChecked(checked)

    def _onModelCheckedChanged(self):
        self._syncHeaderCheckState()
        self.selectionCheckedChanged.emit(self._model.checkedRows())

    def _syncHeaderCheckState(self):
        if getattr(self, "_hheader", None) is not None:
            self._hheader.setCheckState(self._model.headerCheckState())

    def _actionsColumn(self):
        """The view/model column index of the ⋮ column, or -1 when disabled."""
        vm = self._view.model()
        if vm is None or not self._model.rowActions():
            return -1
        return vm.columnCount() - 1

    def buildRowActionsMenu(self, srcRow):
        """A QMenu of the configured row actions; each entry emits
        ``rowActionTriggered(srcRow, key)`` when triggered. Exposed (not just
        used by the popup) so the wiring is unit-testable without a modal exec."""
        menu = QMenu(self)
        menu.setObjectName("dataTableRowMenu")
        for key, label in self._model.rowActions():
            act = menu.addAction(label)
            act.triggered.connect(
                lambda _checked=False, k=key, r=srcRow:
                self.rowActionTriggered.emit(r, k))
        return menu

    def _showRowActionsMenu(self, srcRow, viewIndex):
        menu = self.buildRowActionsMenu(srcRow)
        rect = self._view.visualRect(viewIndex)
        pos = self._view.viewport().mapToGlobal(rect.center())
        menu.exec_(pos)

    # ------------------------------------------------------------------ #
    ## Sorting / filtering
    # ------------------------------------------------------------------ #
    def setFilterText(self, text):
        if not self._filterable:
            return
        self._sortFilter.setFilterFixedString(text or "")
        self.setPage(0)

    def sortBy(self, column, order=Qt.AscendingOrder):
        self._sortFilter.sort(column, order)
        self._view.horizontalHeader().setSortIndicator(column, order)

    # ------------------------------------------------------------------ #
    ## Pagination
    # ------------------------------------------------------------------ #
    def _paginationActive(self):
        # the pagination proxy lingers once created; it only governs the view
        # when it is actually the view's model (pagination on + pageSize > 0).
        return self._pageProxy is not None and self._view.model() is self._pageProxy

    def pageCount(self):
        return self._pageProxy.pageCount() if self._paginationActive() else 1

    def currentPage(self):
        return self._pageProxy.page() if self._paginationActive() else 0

    def setPage(self, index):
        if self._pageProxy is not None:
            self._pageProxy.setPage(index)

    def nextPage(self):
        if self._pageProxy is not None:
            self._pageProxy.setPage(self._pageProxy.page() + 1)

    def prevPage(self):
        if self._pageProxy is not None:
            self._pageProxy.setPage(self._pageProxy.page() - 1)

    def _onPaginationChanged(self):
        if self._pageProxy is None or not self._footer.isVisible():
            return
        page = self._pageProxy.page()
        pages = self._pageProxy.pageCount()
        self._pageLabel.setText("Page %d of %d" % (page + 1, pages))
        self._prevBtn.setEnabled(page > 0)
        self._nextBtn.setEnabled(page < pages - 1)
        if page != self._lastPage:
            self._lastPage = page
            self.pageChanged.emit(page)

    # ------------------------------------------------------------------ #
    ## Selection
    # ------------------------------------------------------------------ #
    def selectedRows(self):
        """Return the selected SOURCE-model row indices (sorted, unique)."""
        rows = set()
        if self._selModel is not None:
            for idx in self._selModel.selectedIndexes():
                r = self._toSourceRow(idx)
                if r >= 0:
                    rows.add(r)
        return sorted(rows)

    def _toSourceRow(self, viewIndex):
        if not viewIndex.isValid():
            return -1
        idx = viewIndex
        if self._pageProxy is not None and self._view.model() is self._pageProxy:
            idx = self._pageProxy.mapToSource(idx)
        src = self._sortFilter.mapToSource(idx)
        return src.row()

    def _onCurrentRowChanged(self, current, previous):
        row = self._toSourceRow(current)
        if row >= 0:
            self.rowSelected.emit(row)

    def _onCellClicked(self, viewIndex):
        row = self._toSourceRow(viewIndex)
        if row < 0:
            return
        if viewIndex.column() == self._actionsColumn():
            self._showRowActionsMenu(row, viewIndex)
            return
        self.cellClicked.emit(row, viewIndex.column())

    def _onSortIndicatorChanged(self, column, order):
        self.sortChanged.emit(column, order)

    # ------------------------------------------------------------------ #
    ## Bulk config
    # ------------------------------------------------------------------ #
    def customizeQCustomDataTable(self, **customValues):
        if "columns" in customValues:
            self.setColumns(customValues["columns"])
        if "selectable" in customValues:
            self.setSelectable(customValues["selectable"])
        if "rowActions" in customValues:
            self.setRowActions(customValues["rowActions"])
        if "data" in customValues:
            self.setData(customValues["data"])
        elif "rows" in customValues:
            self.setData(customValues["rows"])
        for name in ("pageSize", "showPagination", "selectionMode", "sortable",
                     "filterable", "alternatingRowColors", "showGrid", "showHeader",
                     "variant", "sizeVariant"):
            if name in customValues:
                setattr(self, name, customValues[name])
        if "filterText" in customValues:
            self.setFilterText(customValues["filterText"])
        self.update()

    # ------------------------------------------------------------------ #
    ## Properties (Designer)
    # ------------------------------------------------------------------ #
    @Property(int)
    def pageSize(self):
        return self._pageSize

    @pageSize.setter
    def pageSize(self, value):
        self._pageSize = max(0, int(value))
        self._installModel()

    @Property(bool)
    def showPagination(self):
        return self._showPagination

    @showPagination.setter
    def showPagination(self, value):
        self._showPagination = bool(value)
        self._installModel()

    @Property(int)
    def selectionMode(self):
        return int(self._selectionMode)

    @selectionMode.setter
    def selectionMode(self, value):
        self._selectionMode = QCustomDataTable.SelectionMode(int(value))
        self._applySelectionMode()

    @Property(bool)
    def selectable(self):
        return self._model.isSelectable()

    @selectable.setter
    def selectable(self, value):
        self.setSelectable(bool(value))

    @Property(bool)
    def sortable(self):
        return self._sortable

    @sortable.setter
    def sortable(self, value):
        self._sortable = bool(value)
        self._view.setSortingEnabled(self._sortable)

    @Property(bool)
    def filterable(self):
        return self._filterable

    @filterable.setter
    def filterable(self, value):
        self._filterable = bool(value)

    @Property(bool)
    def alternatingRowColors(self):
        return self._alternatingRowColors

    @alternatingRowColors.setter
    def alternatingRowColors(self, value):
        self._alternatingRowColors = bool(value)
        self._view.setAlternatingRowColors(self._alternatingRowColors)

    @Property(bool)
    def showGrid(self):
        return self._showGrid

    @showGrid.setter
    def showGrid(self, value):
        self._showGrid = bool(value)
        self._view.setShowGrid(self._showGrid)

    @Property(bool)
    def showHeader(self):
        return self._showHeader

    @showHeader.setter
    def showHeader(self, value):
        self._showHeader = bool(value)
        self._view.horizontalHeader().setVisible(self._showHeader)

    @Property(str)
    def variant(self):
        return self._variant

    @variant.setter
    def variant(self, value):
        # declared Qt property: QSS [variant="..."] reads the getter directly,
        # so we must NOT call setProperty("variant") here (it would recurse).
        self._variant = str(value)
        self._repolish()

    @Property(str)
    def sizeVariant(self):
        return self._sizeVariant

    @sizeVariant.setter
    def sizeVariant(self, value):
        self._sizeVariant = str(value)
        self._repolish()
