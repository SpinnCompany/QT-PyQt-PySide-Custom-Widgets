########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/@SpinnTV
# WEBSITE: customwidgets.org
########################################################################

########################################################################
## QCustomPagination - page navigation with prev/next and ellipsis.
##
## [<] [1] ... [4] [5] [6] ... [20] [>]  - first/last always shown, a window
## around the current page, ellipsis for gaps. Tokenized. Emits pageChanged.
########################################################################
from qtpy.QtCore import Signal
from qtpy.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLabel


def pages_to_show(current, total, window=1):
    """Return the page tokens to render: ints and '...' gaps."""
    if total <= 0:
        return []
    if total <= 2 * window + 5:            # small enough to show every page
        return list(range(1, total + 1))
    keep = {1, total}
    for p in range(current - window, current + window + 1):
        if 1 <= p <= total:
            keep.add(p)
    ordered = sorted(keep)
    out = []
    prev = 0
    for p in ordered:
        if p - prev > 1:
            out.append("...")
        out.append(p)
        prev = p
    return out


from Custom_Widgets.accessibility import set_accessibility, QAccessible


class QCustomPagination(QWidget):
    pageChanged = Signal(int)      # 1-based current page

    WIDGET_ICON = "components/icons/more_horiz.png"
    WIDGET_TOOLTIP = "Page navigation"
    WIDGET_MODULE = "Custom_Widgets.QCustomPagination"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomPagination' name='customPagination'>
            <property name='geometry'><rect><x>0</x><y>0</y><width>320</width><height>32</height></rect></property>
        </widget>
    </ui>
    """
    __catalog__ = {
        "name": "QCustomPagination",
        "props": {"pageCount": {"type": "int", "default": 1},
                  "currentPage": {"type": "int", "default": 1}},
        "signals": ["pageChanged"],
        "tokens_used": ["surface", "on-surface", "surface-muted", "outline",
                        "accent", "on-primary"],
    }

    def __init__(self, parent=None, pageCount=1):
        super().__init__(parent)
        self.setObjectName("QCustomPagination")
        self._count = max(1, int(pageCount))
        self._current = 1
        self._window = 1
        self._row = QHBoxLayout(self)
        self._row.setContentsMargins(0, 0, 0, 0)
        self._row.setSpacing(4)
        self._row.addStretch(1)
        self._rebuild()
        set_accessibility(self, QAccessible.Grouping, "Pagination")

    def _rebuild(self):
        while self._row.count() > 1:
            w = self._row.takeAt(0).widget()
            if w is not None:
                w.setParent(None)          # detach now so it isn't a lingering child
                w.deleteLater()

        prev = QPushButton("‹", self)
        prev.setObjectName("pageNav")
        prev.setEnabled(self._current > 1)
        prev.clicked.connect(lambda: self.setCurrentPage(self._current - 1))
        self._row.insertWidget(self._row.count() - 1, prev)

        for tok in pages_to_show(self._current, self._count, self._window):
            if tok == "...":
                lbl = QLabel("…", self)
                lbl.setObjectName("pageEllipsis")
                self._row.insertWidget(self._row.count() - 1, lbl)
            else:
                b = QPushButton(str(tok), self)
                b.setObjectName("pageBtn")
                b.setProperty("current", tok == self._current)
                b.clicked.connect(lambda _c=False, p=tok: self.setCurrentPage(p))
                self._row.insertWidget(self._row.count() - 1, b)

        nxt = QPushButton("›", self)
        nxt.setObjectName("pageNav")
        nxt.setEnabled(self._current < self._count)
        nxt.clicked.connect(lambda: self.setCurrentPage(self._current + 1))
        self._row.insertWidget(self._row.count() - 1, nxt)

    # -- API --
    def pageCount(self):
        return self._count

    def setPageCount(self, count):
        self._count = max(1, int(count))
        self._current = min(self._current, self._count)
        self._rebuild()

    def currentPage(self):
        return self._current

    def setCurrentPage(self, page):
        page = max(1, min(int(page), self._count))
        changed = page != self._current
        self._current = page
        self._rebuild()
        if changed:
            self.pageChanged.emit(page)
