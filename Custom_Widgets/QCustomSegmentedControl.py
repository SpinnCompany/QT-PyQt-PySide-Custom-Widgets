########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/spinnTv
# WEBSITE: spinncode.com
########################################################################

########################################################################
## QCustomSegmentedControl - a single-select connected button group.
##
## A row of joined segments; exactly one is selected. Tokenized, with rounded
## ends via a `seg` position property (first / middle / last / only). Emits
## currentChanged.
########################################################################
from qtpy.QtCore import Signal
from qtpy.QtWidgets import QWidget, QHBoxLayout, QPushButton, QButtonGroup


class QCustomSegmentedControl(QWidget):
    currentChanged = Signal(int)

    WIDGET_ICON = "components/icons/segmented.png"
    WIDGET_TOOLTIP = "A single-select segmented control"
    WIDGET_MODULE = "Custom_Widgets.QCustomSegmentedControl"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomSegmentedControl' name='customSegmentedControl'>
            <property name='geometry'><rect><x>0</x><y>0</y><width>260</width><height>32</height></rect></property>
        </widget>
    </ui>
    """
    __catalog__ = {
        "name": "QCustomSegmentedControl",
        "props": {"currentIndex": {"type": "int", "default": 0}},
        "signals": ["currentChanged"],
        "tokens_used": ["surface", "on-surface", "surface-muted", "outline",
                        "accent", "on-primary"],
    }

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("QCustomSegmentedControl")
        self._items = []               # (label, data)
        self._current = 0
        self._buttons = []
        self._group = QButtonGroup(self)
        self._group.setExclusive(True)
        self._group.idClicked.connect(self._onClicked)
        self._row = QHBoxLayout(self)
        self._row.setContentsMargins(0, 0, 0, 0)
        self._row.setSpacing(0)

    def setSegments(self, items):
        """Each item is a string, (label, data) pair, or a dict with
        label/text and data/value keys."""
        self._clear()
        norm = []
        for it in items or []:
            if isinstance(it, dict):
                norm.append((it.get("label", it.get("text", "")),
                             it.get("data", it.get("value"))))
            elif isinstance(it, (tuple, list)) and len(it) >= 2:
                norm.append((it[0], it[1]))
            else:
                norm.append((str(it), it))
        self._items = norm

        n = len(norm)
        for i, (label, _data) in enumerate(norm):
            b = QPushButton(str(label), self)
            b.setObjectName("segmentButton")
            b.setCheckable(True)
            b.setProperty("seg", self._segPos(i, n))
            self._group.addButton(b, i)
            self._row.addWidget(b)
            self._buttons.append(b)
        if n:
            self.setCurrentIndex(min(self._current, n - 1))

    @staticmethod
    def _segPos(i, n):
        if n == 1:
            return "only"
        if i == 0:
            return "first"
        if i == n - 1:
            return "last"
        return "middle"

    def _clear(self):
        for b in self._buttons:
            self._group.removeButton(b)
            b.deleteLater()
        self._buttons = []
        self._items = []

    def _onClicked(self, index):
        self.setCurrentIndex(index)

    # -- API --
    def count(self):
        return len(self._items)

    def currentIndex(self):
        return self._current

    def currentData(self):
        if 0 <= self._current < len(self._items):
            return self._items[self._current][1]
        return None

    def setCurrentIndex(self, index):
        if not self._buttons:
            self._current = index
            return
        index = max(0, min(int(index), len(self._buttons) - 1))
        changed = index != self._current or not self._buttons[index].isChecked()
        self._current = index
        self._buttons[index].setChecked(True)
        if changed:
            self.currentChanged.emit(index)
