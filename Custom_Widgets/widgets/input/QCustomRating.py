########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/@SpinnTV
# WEBSITE: customwidgets.org
########################################################################

########################################################################
## QCustomRating - a clickable star rating.
##
## A row of stars; click to set the value, hover to preview. Read-only mode
## for display. Tokenized via a `filled` dynamic property on each star.
########################################################################
from qtpy.QtCore import Qt, Signal, Property
from qtpy.QtWidgets import QWidget, QHBoxLayout, QLabel


class QCustomRating(QWidget):
    valueChanged = Signal(int)

    WIDGET_ICON = "components/icons/rating.png"
    WIDGET_TOOLTIP = "A star rating"
    WIDGET_MODULE = "Custom_Widgets.QCustomRating"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomRating' name='customRating'>
            <property name='geometry'><rect><x>0</x><y>0</y><width>160</width><height>28</height></rect></property>
        </widget>
    </ui>
    """
    __catalog__ = {
        "name": "QCustomRating",
        "props": {"maximum": {"type": "int", "default": 5},
                  "value": {"type": "int", "default": 0},
                  "readOnly": {"type": "bool", "default": False}},
        "signals": ["valueChanged"],
        "tokens_used": ["warning", "outline"],
    }

    def __init__(self, parent=None, maximum=5):
        super().__init__(parent)
        self.setObjectName("QCustomRating")
        self._max = max(1, int(maximum))
        self._value = 0
        self._readOnly = False
        self._stars = []
        self.setMouseTracking(True)
        self._row = QHBoxLayout(self)
        self._row.setContentsMargins(0, 0, 0, 0)
        self._row.setSpacing(2)
        self._build()

    def _build(self):
        while self._row.count():
            w = self._row.takeAt(0).widget()
            if w is not None:
                w.deleteLater()
        self._stars = []
        for _i in range(self._max):
            star = QLabel(self)
            star.setObjectName("ratingStar")
            star.setAlignment(Qt.AlignCenter)
            star.setFixedSize(24, 24)
            star.setMouseTracking(True)
            self._stars.append(star)
            self._row.addWidget(star)
        self._row.addStretch(1)
        self._paint(self._value)

    def _paint(self, filledCount):
        for i, star in enumerate(self._stars):
            filled = i < filledCount
            star.setText("★" if filled else "☆")
            star.setProperty("filled", filled)
            star.style().unpolish(star)
            star.style().polish(star)

    def _starAt(self, pos):
        for i, star in enumerate(self._stars):
            if star.geometry().contains(pos):
                return i
        return -1

    # -- interaction --
    def mouseMoveEvent(self, e):
        if not self._readOnly:
            i = self._starAt(e.pos())
            self._paint(i + 1 if i >= 0 else self._value)

    def mousePressEvent(self, e):
        if not self._readOnly and e.button() == Qt.LeftButton:
            i = self._starAt(e.pos())
            if i >= 0:
                new = i + 1
                # click the only lit star again to clear
                self.setValue(0 if new == self._value else new)

    def leaveEvent(self, e):
        self._paint(self._value)

    # -- API --
    @Property(int)
    def maximum(self):
        return self._max

    @maximum.setter
    def maximum(self, value):
        self._max = max(1, int(value))
        self._value = min(self._value, self._max)
        self._build()

    @Property(int)
    def value(self):
        return self._value

    @value.setter
    def value(self, v):
        self.setValue(v)

    def setValue(self, v):
        v = max(0, min(int(v), self._max))
        changed = v != self._value
        self._value = v
        self._paint(v)
        if changed:
            self.valueChanged.emit(v)

    @Property(bool)
    def readOnly(self):
        return self._readOnly

    @readOnly.setter
    def readOnly(self, ro):
        self._readOnly = bool(ro)
        self.setCursor(Qt.ArrowCursor if self._readOnly else Qt.PointingHandCursor)
