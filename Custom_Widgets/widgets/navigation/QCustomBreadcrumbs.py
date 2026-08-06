########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/@SpinnTV
# WEBSITE: customwidgets.org
########################################################################

########################################################################
## QCustomBreadcrumbs - a clickable path navigation.
##
## Home / Section / Page ... - all but the last segment are clickable
## links; the last is the current location. Tokenized.
########################################################################
from qtpy.QtCore import Qt, Signal
from qtpy.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLabel


class QCustomBreadcrumbs(QWidget):
    itemClicked = Signal(int, object)      # index, data

    WIDGET_ICON = "components/icons/last_page.png"
    WIDGET_TOOLTIP = "A clickable path navigation"
    WIDGET_MODULE = "Custom_Widgets.QCustomBreadcrumbs"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomBreadcrumbs' name='customBreadcrumbs'>
            <property name='geometry'><rect><x>0</x><y>0</y><width>320</width><height>28</height></rect></property>
        </widget>
    </ui>
    """
    __catalog__ = {
        "name": "QCustomBreadcrumbs",
        "props": {},
        "signals": ["itemClicked"],
        "tokens_used": ["on-surface", "surface-muted", "accent"],
    }

    def __init__(self, parent=None, separator="/"):
        super().__init__(parent)
        self.setObjectName("QCustomBreadcrumbs")
        self._separator = separator
        self._items = []
        self._row = QHBoxLayout(self)
        self._row.setContentsMargins(0, 0, 0, 0)
        self._row.setSpacing(6)
        self._row.addStretch(1)

    def setItems(self, items):
        """Set the trail. Each item is a string, (label, data) pair, or a dict
        with label/text and data/value keys."""
        self._clear()
        self._items = []
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

        last = len(norm) - 1
        for i, (label, data) in enumerate(norm):
            if i < last:
                link = QPushButton(str(label), self)
                link.setObjectName("breadcrumbLink")
                link.setFlat(True)
                link.setCursor(Qt.PointingHandCursor)
                link.clicked.connect(lambda _c=False, idx=i, d=data: self.itemClicked.emit(idx, d))
                self._row.insertWidget(self._row.count() - 1, link)
                sep = QLabel(self._separator, self)
                sep.setObjectName("breadcrumbSep")
                self._row.insertWidget(self._row.count() - 1, sep)
            else:
                current = QLabel(str(label), self)
                current.setObjectName("breadcrumbCurrent")
                self._row.insertWidget(self._row.count() - 1, current)

    def items(self):
        return list(self._items)

    def _clear(self):
        while self._row.count() > 1:               # keep the trailing stretch
            item = self._row.takeAt(0)
            w = item.widget()
            if w is not None:
                w.deleteLater()
