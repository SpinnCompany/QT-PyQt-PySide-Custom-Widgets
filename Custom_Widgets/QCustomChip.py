########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/spinnTv
# WEBSITE: spinncode.com
########################################################################

########################################################################
## QCustomChip / QCustomChipGroup - compact tags / filter chips.
##
## A chip is a small rounded label, optionally closable (x) and/or
## selectable (filter/choice chip). QCustomChipGroup lays chips out in a
## wrapping flow with optional single- or multi-select. Tokenized.
########################################################################
from qtpy.QtCore import Qt, Signal
from qtpy.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton

from Custom_Widgets.QCustomFlowLayout import QCustomFlowLayout


class QCustomChip(QWidget):
    removed = Signal()          # close button clicked
    clicked = Signal()          # chip body clicked
    toggled = Signal(bool)      # selection changed (selectable chips)

    def __init__(self, text, closable=False, selectable=False, data=None, parent=None):
        super().__init__(parent)
        self.setObjectName("QCustomChip")
        self.setAttribute(Qt.WA_StyledBackground, True)
        self._text = text
        self._data = data if data is not None else text
        self._selectable = selectable
        self._selected = False
        self.setProperty("selected", False)
        if selectable:
            self.setCursor(Qt.PointingHandCursor)

        row = QHBoxLayout(self)
        row.setContentsMargins(10, 4, 8 if closable else 10, 4)
        row.setSpacing(6)
        self._label = QLabel(text, self)
        self._label.setObjectName("chipLabel")
        row.addWidget(self._label)
        if closable:
            self._close = QPushButton("✕", self)
            self._close.setObjectName("chipClose")
            self._close.setFixedSize(16, 16)
            self._close.setCursor(Qt.PointingHandCursor)
            self._close.clicked.connect(self.removed)
            row.addWidget(self._close)

    def text(self):
        return self._text

    def data(self):
        return self._data

    def isSelected(self):
        return self._selected

    def setSelected(self, selected):
        selected = bool(selected)
        if selected == self._selected:
            return
        self._selected = selected
        self.setProperty("selected", selected)
        self.style().unpolish(self)
        self.style().polish(self)
        self.toggled.emit(selected)

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.clicked.emit()
            if self._selectable:
                self.setSelected(not self._selected)
        super().mousePressEvent(e)


class QCustomChipGroup(QWidget):
    chipRemoved = Signal(object)        # data of removed chip
    selectionChanged = Signal(list)     # list of selected data

    WIDGET_ICON = "components/icons/chips.png"
    WIDGET_TOOLTIP = "A wrapping group of chips / tags"
    WIDGET_MODULE = "Custom_Widgets.QCustomChip"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomChipGroup' name='customChipGroup'>
            <property name='geometry'><rect><x>0</x><y>0</y><width>320</width><height>80</height></rect></property>
        </widget>
    </ui>
    """
    __catalog__ = {
        "name": "QCustomChipGroup",
        "props": {"selectable": {"type": "bool", "default": False},
                  "exclusive": {"type": "bool", "default": False}},
        "signals": ["chipRemoved", "selectionChanged"],
        "tokens_used": ["surface-muted", "on-surface", "accent", "on-primary", "outline"],
    }

    def __init__(self, parent=None, selectable=False, exclusive=False, closable=False):
        super().__init__(parent)
        self.setObjectName("QCustomChipGroup")
        self._selectable = selectable
        self._exclusive = exclusive
        self._closable = closable
        self._chips = []
        self._flow = QCustomFlowLayout(self, margin=0, spacing=6)

    def addChip(self, text, data=None, closable=None, selectable=None):
        chip = QCustomChip(
            text,
            closable=self._closable if closable is None else closable,
            selectable=self._selectable if selectable is None else selectable,
            data=data, parent=self)
        chip.removed.connect(lambda c=chip: self._removeChip(c))
        chip.toggled.connect(lambda _on, c=chip: self._onToggled(c))
        self._chips.append(chip)
        self._flow.addWidget(chip)
        return chip

    def setChips(self, texts):
        for c in list(self._chips):
            self._removeChip(c, emit=False)
        for t in texts or []:
            if isinstance(t, (tuple, list)) and len(t) >= 2:
                self.addChip(t[0], data=t[1])
            else:
                self.addChip(t)

    def _removeChip(self, chip, emit=True):
        if chip in self._chips:
            self._chips.remove(chip)
            self._flow.removeWidget(chip)
            chip.setParent(None)
            chip.deleteLater()
            if emit:
                self.chipRemoved.emit(chip.data())

    def _onToggled(self, chip):
        if chip.isSelected() and self._exclusive:
            for c in self._chips:
                if c is not chip and c.isSelected():
                    c.setSelected(False)
        self.selectionChanged.emit(self.selectedData())

    # -- API --
    def chips(self):
        return list(self._chips)

    def selectedChips(self):
        return [c for c in self._chips if c.isSelected()]

    def selectedData(self):
        return [c.data() for c in self._chips if c.isSelected()]

    def count(self):
        return len(self._chips)
