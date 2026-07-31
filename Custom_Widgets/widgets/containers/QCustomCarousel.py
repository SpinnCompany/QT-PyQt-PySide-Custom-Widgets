########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/spinnTv
# WEBSITE: spinncode.com
########################################################################

########################################################################
## QCustomCarousel - one slide at a time, with prev/next nav + dot indicators.
##
## Add any widgets as slides; the carousel shows one at a time with previous /
## next buttons and a row of clickable dots. Optional wrap-around and auto
## advance. Emits currentChanged(index). Tokenized (nav buttons + active dot).
########################################################################
from qtpy.QtCore import Property, Qt, Signal, QTimer
from qtpy.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QStackedWidget,
                            QPushButton)

_DOT = 10   # dot diameter (px); the QSS radius is half this -> a circle


class QCustomCarousel(QWidget):
    currentChanged = Signal(int)

    WIDGET_ICON = "components/icons/view_carousel.png"
    WIDGET_TOOLTIP = "A slideshow carousel with nav + dots"
    WIDGET_MODULE = "Custom_Widgets.QCustomCarousel"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomCarousel' name='customCarousel'>
            <property name='geometry'><rect><x>0</x><y>0</y><width>360</width><height>220</height></rect></property>
        </widget>
    </ui>
    """
    __catalog__ = {
        "name": "QCustomCarousel",
        "props": {"currentIndex": {"type": "int", "default": 0},
                  "wrap": {"type": "bool", "default": True}},
        "signals": ["currentChanged"],
        "tokens_used": ["surface", "surface-muted", "on-surface", "outline",
                        "accent"],
    }

    def __init__(self, parent=None, wrap=True):
        super().__init__(parent)
        self.setObjectName("QCustomCarousel")
        self._wrap = bool(wrap)
        self._dots = []
        self._autoMs = 0
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._autoNext)

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(8)

        # slide row: prev | stack | next
        row = QHBoxLayout()
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(6)
        self._prev = QPushButton("‹", self)      # ‹
        self._prev.setObjectName("carouselNav")
        self._prev.setFixedWidth(28)
        self._prev.setCursor(Qt.PointingHandCursor)
        self._prev.clicked.connect(self.previous)
        self._stack = QStackedWidget(self)
        self._next = QPushButton("›", self)      # ›
        self._next.setObjectName("carouselNav")
        self._next.setFixedWidth(28)
        self._next.setCursor(Qt.PointingHandCursor)
        self._next.clicked.connect(self.next)
        row.addWidget(self._prev)
        row.addWidget(self._stack, 1)
        row.addWidget(self._next)
        root.addLayout(row, 1)

        # dots
        self._dotRow = QHBoxLayout()
        self._dotRow.setContentsMargins(0, 0, 0, 0)
        self._dotRow.setSpacing(6)
        self._dotRow.setAlignment(Qt.AlignCenter)
        root.addLayout(self._dotRow)

        self._stack.currentChanged.connect(self._onStackChanged)
        self._updateNav()

    # ------------------------------------------------------------------ #
    ## Slides
    # ------------------------------------------------------------------ #
    def addSlide(self, widget):
        """Append a widget as a slide. Returns its index."""
        idx = self._stack.addWidget(widget)
        self._rebuildDots()
        self._updateNav()
        return idx

    def insertSlide(self, index, widget):
        idx = self._stack.insertWidget(index, widget)
        self._rebuildDots()
        self._updateNav()
        return idx

    def removeSlide(self, index):
        w = self._stack.widget(index)
        if w is not None:
            self._stack.removeWidget(w)
            w.deleteLater()
            self._rebuildDots()
            self._updateNav()

    def clear(self):
        while self._stack.count():
            w = self._stack.widget(0)
            self._stack.removeWidget(w)
            w.deleteLater()
        self._rebuildDots()
        self._updateNav()

    def count(self):
        return self._stack.count()

    # ------------------------------------------------------------------ #
    ## Navigation
    # ------------------------------------------------------------------ #
    def currentIndex(self):
        return self._stack.currentIndex()

    def setCurrentIndex(self, index):
        n = self._stack.count()
        if n == 0:
            return
        if self._wrap:
            index = index % n
        else:
            index = max(0, min(int(index), n - 1))
        self._stack.setCurrentIndex(index)

    def next(self):
        if self._stack.count():
            self.setCurrentIndex(self.currentIndex() + 1)

    def previous(self):
        if self._stack.count():
            self.setCurrentIndex(self.currentIndex() - 1)

    def setWrap(self, wrap):
        self._wrap = bool(wrap)
        self._updateNav()

    def wrapsAround(self):
        return self._wrap

    def setAutoAdvance(self, milliseconds):
        """Advance automatically every N ms (0 stops the timer)."""
        self._autoMs = max(0, int(milliseconds))
        if self._autoMs and self._stack.count() > 1:
            self._timer.start(self._autoMs)
        else:
            self._timer.stop()

    # ------------------------------------------------------------------ #
    ## Internals
    # ------------------------------------------------------------------ #
    def _autoNext(self):
        if self._stack.count() > 1:
            self.next()

    def _onStackChanged(self, index):
        for i, dot in enumerate(self._dots):
            dot.setProperty("active", i == index)
            dot.style().unpolish(dot)
            dot.style().polish(dot)
        self._updateNav()
        self.currentChanged.emit(index)

    def _updateNav(self):
        n = self._stack.count()
        cur = self._stack.currentIndex()
        multi = n > 1
        self._prev.setVisible(multi)
        self._next.setVisible(multi)
        if not self._wrap:
            self._prev.setEnabled(cur > 0)
            self._next.setEnabled(cur < n - 1)
        else:
            self._prev.setEnabled(multi)
            self._next.setEnabled(multi)

    def _rebuildDots(self):
        while self._dotRow.count():
            item = self._dotRow.takeAt(0)
            w = item.widget()
            if w is not None:
                w.setParent(None)
                w.deleteLater()
        self._dots = []
        n = self._stack.count()
        if n <= 1:
            return
        cur = self._stack.currentIndex()
        for i in range(n):
            dot = QPushButton(self)
            dot.setObjectName("carouselDot")
            dot.setCursor(Qt.PointingHandCursor)
            dot.setFixedSize(_DOT, _DOT)
            dot.setProperty("active", i == cur)
            dot.clicked.connect(lambda _c=False, idx=i: self.setCurrentIndex(idx))
            self._dotRow.addWidget(dot)
            self._dots.append(dot)

    # ------------------------------------------------------------------ #
    ## Declarative properties
    # ------------------------------------------------------------------ #
    @Property(int)
    def currentIndex_(self):
        return self.currentIndex()

    @Property(bool)
    def wrap(self):
        return self._wrap

    @wrap.setter
    def wrap(self, value):
        self.setWrap(value)
