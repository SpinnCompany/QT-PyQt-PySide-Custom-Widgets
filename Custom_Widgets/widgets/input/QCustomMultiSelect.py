########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/@SpinnTV
# WEBSITE: customwidgets.org
########################################################################

########################################################################
## QCustomMultiSelect - a multiple-choice field with chips.
##
## A closed field that paints the current selection as removable chips, and a
## checkable popup list to change it. QComboBox cannot do this: it is
## single-selection by design, and the usual workaround (a QComboBox with
## checkable model items) leaves the closed field showing one entry while the
## model holds several.
##
## Options are authored in code with setOptions([...]) or in Qt Designer with
## the optionsCsv property, following the valuesCsv convention used elsewhere:
##
##     optionsCsv = "Red,Green,Blue"                 labels double as values
##     optionsCsv = "r=Red,g=Green,b=Blue"           explicit value=label
##
## Emits selectionChanged(list) and optionToggled(str, bool).
########################################################################
from qtpy.QtCore import Qt, Signal, Property, QRectF, QSize, QPoint
from qtpy.QtGui import QColor, QPainter, QPen, QBrush, QFontMetrics
from qtpy.QtWidgets import (QWidget, QSizePolicy, QListWidget, QListWidgetItem,
                            QVBoxLayout, QFrame, QLineEdit)


class QCustomMultiSelect(QWidget):
    selectionChanged = Signal(list)
    optionToggled = Signal(str, bool)

    WIDGET_ICON = "components/icons/checklist.png"
    WIDGET_TOOLTIP = "A multiple-choice field with removable chips"
    WIDGET_MODULE = "Custom_Widgets.QCustomMultiSelect"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomMultiSelect' name='customMultiSelect'>
            <property name='geometry'><rect><x>0</x><y>0</y><width>280</width><height>40</height></rect></property>
            <property name='optionsCsv'><string>Option one,Option two,Option three</string></property>
        </widget>
    </ui>
    """
    __catalog__ = {
        "name": "QCustomMultiSelect",
        "props": {"optionsCsv": {"type": "string",
                                 "default": "Option one,Option two,Option three"},
                  "selectedCsv": {"type": "string", "default": ""},
                  "placeholderText": {"type": "string", "default": "Select..."},
                  "maxChips": {"type": "int", "default": 0},
                  "searchable": {"type": "bool", "default": False},
                  "maxSelection": {"type": "int", "default": 0},
                  "sizeVariant": {"type": "enum", "values": ["sm", "md", "lg"],
                                  "default": "md"},
                  "state": {"type": "enum", "values": ["default", "error"],
                            "default": "default"}},
        "signals": ["selectionChanged", "optionToggled"],
        "tokens_used": ["surface", "on-surface", "outline", "focus-ring",
                        "accent", "destructive"],
    }

    _HEIGHTS = {"sm": 32, "md": 40, "lg": 48}

    def __init__(self, parent=None, options=None, selected=None,
                 placeholder="Select..."):
        super().__init__(parent)
        self.setObjectName("QCustomMultiSelect")
        self._options = []          # list of (value, label)
        self._selected = []         # ordered list of values
        self._placeholder = str(placeholder)
        self._maxChips = 0          # 0 = show them all
        self._maxSelection = 0      # 0 = unlimited
        self._searchable = False
        self._sizeVariant = "md"
        self._state = "default"
        self._chipRects = []        # (value, chip rect, close rect)
        self._popup = None
        self._search = None

        self._fieldBg = QColor("#ffffff")
        self._fieldBorder = QColor("#cbd5e1")
        self._fieldBorderActive = QColor("#2563eb")
        self._fieldBorderError = QColor("#dc2626")
        self._chipBg = QColor("#e2e8f0")
        self._chipText = QColor("#0f172a")
        self._textColor = QColor("#0f172a")
        self._placeholderColor = QColor("#94a3b8")

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setFocusPolicy(Qt.StrongFocus)
        self.setCursor(Qt.PointingHandCursor)
        self.setOptions(options if options is not None
                        else ["Option one", "Option two", "Option three"])
        if selected:
            self.setSelected(selected)

    # ------------------------------------------------------------------ #
    ## Options / selection
    # ------------------------------------------------------------------ #
    @staticmethod
    def _normalise(options):
        out = []
        for opt in options or []:
            if isinstance(opt, dict):
                label = str(opt.get("label", opt.get("value", "")))
                value = str(opt.get("value", label))
            elif isinstance(opt, (tuple, list)) and len(opt) >= 2:
                value, label = str(opt[0]), str(opt[1])
            else:
                text = str(opt)
                if "=" in text:
                    value, label = text.split("=", 1)
                    value, label = value.strip(), label.strip()
                else:
                    value = label = text.strip()
            if label:
                out.append((value, label))
        return out

    def setOptions(self, options):
        """Replace the option set, dropping any selection that no longer exists."""
        self._options = self._normalise(options)
        valid = {v for v, _ in self._options}
        kept = [v for v in self._selected if v in valid]
        changed = kept != self._selected
        self._selected = kept
        self._syncPopup()
        self.updateGeometry()
        self.update()
        if changed:
            self.selectionChanged.emit(list(self._selected))

    def options(self):
        return list(self._options)

    def labelFor(self, value):
        for v, label in self._options:
            if v == value:
                return label
        return str(value)

    def selected(self):
        return list(self._selected)

    def selectedLabels(self):
        return [self.labelFor(v) for v in self._selected]

    def setSelected(self, values):
        valid = {v for v, _ in self._options}
        # preserve the caller's order, drop unknowns and duplicates
        seen, kept = set(), []
        for v in values or []:
            v = str(v)
            if v in valid and v not in seen:
                seen.add(v)
                kept.append(v)
        if self._maxSelection > 0:
            kept = kept[:self._maxSelection]
        if kept == self._selected:
            return
        self._selected = kept
        self._syncPopup()
        self.update()
        self.selectionChanged.emit(list(self._selected))

    def isSelected(self, value):
        return str(value) in self._selected

    def selectOption(self, value, on=True):
        value = str(value)
        if value not in {v for v, _ in self._options}:
            return
        if on and value not in self._selected:
            if self._maxSelection > 0 and len(self._selected) >= self._maxSelection:
                return
            self._selected.append(value)
        elif not on and value in self._selected:
            self._selected.remove(value)
        else:
            return
        self._syncPopup()
        self.update()
        self.optionToggled.emit(value, on)
        self.selectionChanged.emit(list(self._selected))

    def toggleOption(self, value):
        self.selectOption(value, not self.isSelected(value))

    def clearSelection(self):
        if not self._selected:
            return
        self._selected = []
        self._syncPopup()
        self.update()
        self.selectionChanged.emit([])

    def count(self):
        return len(self._options)

    # ------------------------------------------------------------------ #
    ## Geometry / painting
    # ------------------------------------------------------------------ #
    def _height(self):
        return self._HEIGHTS.get(self._sizeVariant, self._HEIGHTS["md"])

    def sizeHint(self):
        return QSize(280, self._height())

    def minimumSizeHint(self):
        return QSize(120, self._height())

    def _visibleChips(self):
        """(values shown as chips, overflow count)."""
        if self._maxChips > 0 and len(self._selected) > self._maxChips:
            return self._selected[:self._maxChips], len(self._selected) - self._maxChips
        return list(self._selected), 0

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.setFont(self.font())
        fm = QFontMetrics(self.font())

        if self._state == "error":
            border = self._fieldBorderError
        elif self.hasFocus():
            border = self._fieldBorderActive
        else:
            border = self._fieldBorder
        field = QRectF(0.5, 0.5, self.width() - 1, self.height() - 1)
        p.setPen(QPen(border, 2 if self.hasFocus() or self._state == "error" else 1))
        p.setBrush(QBrush(self._fieldBg))
        p.drawRoundedRect(field, 8, 8)

        # chevron
        cx = self.width() - 16
        cy = self.height() / 2.0
        p.setPen(QPen(self._textColor, 1.6))
        p.drawLine(int(cx - 4), int(cy - 2), int(cx), int(cy + 2))
        p.drawLine(int(cx), int(cy + 2), int(cx + 4), int(cy - 2))

        self._chipRects = []
        if not self._selected:
            p.setPen(QPen(self._placeholderColor))
            p.drawText(QRectF(10, 0, self.width() - 34, self.height()),
                       int(Qt.AlignVCenter | Qt.AlignLeft), self._placeholder)
            return

        shown, overflow = self._visibleChips()
        x = 8.0
        limit = self.width() - 28
        chip_h = min(self.height() - 12, fm.height() + 8)
        top = (self.height() - chip_h) / 2.0

        for value in shown:
            label = self.labelFor(value)
            text_w = fm.horizontalAdvance(label)
            chip_w = text_w + 26            # padding + the close glyph
            if x + chip_w > limit:
                overflow += 1
                continue
            chip = QRectF(x, top, chip_w, chip_h)
            p.setPen(Qt.NoPen)
            p.setBrush(QBrush(self._chipBg))
            p.drawRoundedRect(chip, chip_h / 2.0, chip_h / 2.0)
            p.setPen(QPen(self._chipText))
            p.drawText(QRectF(x + 8, top, text_w, chip_h),
                       int(Qt.AlignVCenter | Qt.AlignLeft), label)
            # close cross
            close = QRectF(x + chip_w - 17, top, 14, chip_h)
            ccx, ccy = close.center().x(), close.center().y()
            p.setPen(QPen(self._chipText, 1.4))
            p.drawLine(int(ccx - 3), int(ccy - 3), int(ccx + 3), int(ccy + 3))
            p.drawLine(int(ccx + 3), int(ccy - 3), int(ccx - 3), int(ccy + 3))
            self._chipRects.append((value, chip, close))
            x += chip_w + 6

        if overflow:
            text = "+%d" % overflow
            p.setPen(QPen(self._textColor))
            p.drawText(QRectF(x, top, fm.horizontalAdvance(text) + 8, chip_h),
                       int(Qt.AlignVCenter | Qt.AlignLeft), text)

    # ------------------------------------------------------------------ #
    ## Popup
    # ------------------------------------------------------------------ #
    def _buildPopup(self):
        popup = QFrame(self, Qt.Popup)
        popup.setObjectName("QCustomMultiSelectPopup")
        box = QVBoxLayout(popup)
        box.setContentsMargins(4, 4, 4, 4)
        box.setSpacing(4)

        if self._searchable:
            self._search = QLineEdit(popup)
            self._search.setPlaceholderText("Search...")
            self._search.textChanged.connect(self._filterPopup)
            box.addWidget(self._search)
        else:
            self._search = None

        listing = QListWidget(popup)
        listing.setObjectName("QCustomMultiSelectList")
        listing.itemChanged.connect(self._onItemChanged)
        box.addWidget(listing)
        popup.listing = listing
        return popup

    def _syncPopup(self):
        if self._popup is None:
            return
        listing = self._popup.listing
        listing.blockSignals(True)
        listing.clear()
        for value, label in self._options:
            item = QListWidgetItem(label, listing)
            item.setData(Qt.UserRole, value)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Checked if value in self._selected else Qt.Unchecked)
        listing.blockSignals(False)
        self._filterPopup(self._search.text() if self._search else "")

    def _filterPopup(self, text):
        if self._popup is None:
            return
        needle = str(text).strip().lower()
        listing = self._popup.listing
        for i in range(listing.count()):
            item = listing.item(i)
            item.setHidden(bool(needle) and needle not in item.text().lower())

    def _onItemChanged(self, item):
        value = item.data(Qt.UserRole)
        want = item.checkState() == Qt.Checked
        if want == self.isSelected(value):
            return
        self.selectOption(value, want)
        # A max-selection refusal must not leave the box ticked.
        if want and not self.isSelected(value):
            item.setCheckState(Qt.Unchecked)

    def showPopup(self):
        if self._popup is None:
            self._popup = self._buildPopup()
        self._syncPopup()
        self._popup.setFixedWidth(max(self.width(), 160))
        rows = min(8, max(1, self.count()))
        self._popup.listing.setFixedHeight(rows * 24 + 8)
        self._popup.adjustSize()
        self._popup.move(self.mapToGlobal(QPoint(0, self.height() + 2)))
        self._popup.show()

    def hidePopup(self):
        if self._popup is not None:
            self._popup.hide()

    def isPopupVisible(self):
        return self._popup is not None and self._popup.isVisible()

    # ------------------------------------------------------------------ #
    ## Interaction
    # ------------------------------------------------------------------ #
    def mouseReleaseEvent(self, e):
        if e.button() != Qt.LeftButton:
            super().mouseReleaseEvent(e)
            return
        pos = e.pos()
        for value, _chip, close in self._chipRects:
            if close.contains(pos):
                self.selectOption(value, False)     # the x removes just that chip
                return
        self.showPopup()
        super().mouseReleaseEvent(e)

    def keyPressEvent(self, e):
        if e.key() in (Qt.Key_Space, Qt.Key_Return, Qt.Key_Enter, Qt.Key_Down):
            self.showPopup()
            return
        if e.key() == Qt.Key_Backspace and self._selected:
            self.selectOption(self._selected[-1], False)
            return
        if e.key() == Qt.Key_Escape and self.isPopupVisible():
            self.hidePopup()
            return
        super().keyPressEvent(e)

    # ------------------------------------------------------------------ #
    ## Designer properties
    # ------------------------------------------------------------------ #
    @Property(str)
    def optionsCsv(self):
        return ",".join(lbl if val == lbl else "%s=%s" % (val, lbl)
                        for val, lbl in self._options)

    @optionsCsv.setter
    def optionsCsv(self, text):
        self.setOptions([tok for tok in str(text).replace(";", ",").split(",")
                         if tok.strip()])

    @Property(str)
    def selectedCsv(self):
        return ",".join(self._selected)

    @selectedCsv.setter
    def selectedCsv(self, text):
        self.setSelected([tok.strip() for tok in str(text).replace(";", ",").split(",")
                          if tok.strip()])

    @Property(str)
    def placeholderText(self):
        return self._placeholder

    @placeholderText.setter
    def placeholderText(self, text):
        self._placeholder = str(text); self.update()

    @Property(int)
    def maxChips(self):
        return self._maxChips

    @maxChips.setter
    def maxChips(self, value):
        self._maxChips = max(0, int(value)); self.update()

    @Property(int)
    def maxSelection(self):
        return self._maxSelection

    @maxSelection.setter
    def maxSelection(self, value):
        self._maxSelection = max(0, int(value))
        if self._maxSelection > 0 and len(self._selected) > self._maxSelection:
            self.setSelected(self._selected[:self._maxSelection])

    @Property(bool)
    def searchable(self):
        return self._searchable

    @searchable.setter
    def searchable(self, value):
        value = bool(value)
        if value == self._searchable:
            return
        self._searchable = value
        # rebuild lazily: the popup's contents depend on this
        if self._popup is not None:
            self._popup.deleteLater()
            self._popup = None
            self._search = None

    @Property(str)
    def sizeVariant(self):
        return self._sizeVariant

    @sizeVariant.setter
    def sizeVariant(self, value):
        self._sizeVariant = str(value)
        self.updateGeometry(); self.update()

    @Property(str)
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        self._state = "error" if str(value) == "error" else "default"
        self.update()

    # -- colours (from tokens via qproperty) --
    @Property(QColor)
    def fieldBackgroundColor(self):
        return self._fieldBg

    @fieldBackgroundColor.setter
    def fieldBackgroundColor(self, c):
        self._fieldBg = QColor(c); self.update()

    @Property(QColor)
    def fieldBorderColor(self):
        return self._fieldBorder

    @fieldBorderColor.setter
    def fieldBorderColor(self, c):
        self._fieldBorder = QColor(c); self.update()

    @Property(QColor)
    def fieldBorderActiveColor(self):
        return self._fieldBorderActive

    @fieldBorderActiveColor.setter
    def fieldBorderActiveColor(self, c):
        self._fieldBorderActive = QColor(c); self.update()

    @Property(QColor)
    def fieldBorderErrorColor(self):
        return self._fieldBorderError

    @fieldBorderErrorColor.setter
    def fieldBorderErrorColor(self, c):
        self._fieldBorderError = QColor(c); self.update()

    @Property(QColor)
    def chipBackgroundColor(self):
        return self._chipBg

    @chipBackgroundColor.setter
    def chipBackgroundColor(self, c):
        self._chipBg = QColor(c); self.update()

    @Property(QColor)
    def chipTextColor(self):
        return self._chipText

    @chipTextColor.setter
    def chipTextColor(self, c):
        self._chipText = QColor(c); self.update()

    @Property(QColor)
    def textColor(self):
        return self._textColor

    @textColor.setter
    def textColor(self, c):
        self._textColor = QColor(c); self.update()

    @Property(QColor)
    def placeholderColor(self):
        return self._placeholderColor

    @placeholderColor.setter
    def placeholderColor(self, c):
        self._placeholderColor = QColor(c); self.update()
