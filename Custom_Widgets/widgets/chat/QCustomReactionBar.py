########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/@SpinnTV
# WEBSITE: customwidgets.org
########################################################################

########################################################################
## QCustomReactionBar - a row of emoji reaction chips.
##
## The little pills under a chat message showing who reacted: each chip is an
## emoji + a count, and an optional trailing "add reaction" button. Feed it data
## with setReactions([("👍", 3), ("❤️", 1)]) or the `reactions` Designer
## property ("👍:3,❤️:1"). Clicking a chip emits reactionClicked(emoji);
## clicking the add button emits addRequested(). Chips are styled entirely from
## the app QSS (objectName selectors) so they flip with the theme; the add
## button's "+" is painted (no glyph/asset).
########################################################################
from qtpy.QtCore import Qt, Property, Signal, QRectF
from qtpy.QtGui import QColor, QPainter, QPen
from qtpy.QtCore import QPointF
from qtpy.QtWidgets import (QWidget, QLabel, QFrame, QHBoxLayout, QSizePolicy)


class _Chip(QFrame):
    clicked = Signal(str)

    def __init__(self, emoji, count, parent=None):
        super().__init__(parent)
        self.setObjectName("reactionChip")
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setCursor(Qt.PointingHandCursor)
        self._emoji = emoji
        lay = QHBoxLayout(self)
        lay.setContentsMargins(8, 3, 9, 3)
        lay.setSpacing(4)
        self._emojiLbl = QLabel(emoji)
        self._emojiLbl.setObjectName("reactionEmoji")
        self._countLbl = QLabel(str(count))
        self._countLbl.setObjectName("reactionCount")
        lay.addWidget(self._emojiLbl)
        lay.addWidget(self._countLbl)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

    def setCount(self, count):
        self._countLbl.setText(str(count))
        self._countLbl.setVisible(int(count) > 1 if str(count).isdigit() else True)

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.clicked.emit(self._emoji)
        super().mousePressEvent(e)


class _AddButton(QFrame):
    clicked = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("reactionAdd")
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setCursor(Qt.PointingHandCursor)
        self._fg = QColor("#8a93a6")
        self.setFixedSize(26, 24)

    def setColor(self, c):
        self._fg = QColor(c)
        self.update()

    def paintEvent(self, e):
        super().paintEvent(e)     # let QSS paint the chip background first
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, True)
        pen = QPen(self._fg, 1.7)
        pen.setCapStyle(Qt.RoundCap)
        p.setPen(pen)
        c = self.rect().center()
        cx, cy = c.x() + 0.5, c.y() + 0.5
        r = 3.4
        p.drawLine(QPointF(cx - r, cy), QPointF(cx + r, cy))
        p.drawLine(QPointF(cx, cy - r), QPointF(cx, cy + r))
        p.end()

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(e)


class QCustomReactionBar(QWidget):

    reactionClicked = Signal(str)
    addRequested = Signal()

    WIDGET_ICON = "components/icons/emoji_emotions.png"
    WIDGET_TOOLTIP = "A row of emoji reaction chips"
    WIDGET_MODULE = "Custom_Widgets.QCustomReactionBar"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomReactionBar' name='customReactionBar'>
            <property name='geometry'><rect><x>0</x><y>0</y><width>160</width><height>28</height></rect></property>
        </widget>
    </ui>
    """
    __catalog__ = {
        "name": "QCustomReactionBar",
        "props": {
            "reactions": {"type": "string", "default": ""},
            "showAdd": {"type": "bool", "default": True},
            "addColor": {"type": "color", "default": "#8a93a6"},
        },
        "signals": ["reactionClicked", "addRequested"],
        "tokens_used": [],
    }

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("QCustomReactionBar")
        self._show_add = True
        self._add_color = QColor("#8a93a6")
        self._pairs = []
        self._row = QHBoxLayout(self)
        self._row.setContentsMargins(0, 0, 0, 0)
        self._row.setSpacing(5)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self._rebuild()

    # ------------------------------------------------------------------ #
    ## Data API
    # ------------------------------------------------------------------ #
    def setReactions(self, reactions):
        pairs = []
        for r in (reactions or []):
            if isinstance(r, (tuple, list)) and len(r) >= 2:
                pairs.append((str(r[0]), int(r[1])))
            elif isinstance(r, dict):
                pairs.append((str(r.get("emoji", "")), int(r.get("count", 1))))
            else:
                pairs.append((str(r), 1))
        self._pairs = [p for p in pairs if p[0]]
        self._rebuild()

    def _rebuild(self):
        while self._row.count():
            it = self._row.takeAt(0)
            w = it.widget()
            if w is not None:
                w.setParent(None)
                w.deleteLater()
        for emoji, count in self._pairs:
            chip = _Chip(emoji, count, self)
            chip.setCount(count)
            chip.clicked.connect(self.reactionClicked)
            self._row.addWidget(chip, 0)
        if self._show_add:
            add = _AddButton(self)
            add.setColor(self._add_color)
            add.clicked.connect(self.addRequested)
            self._row.addWidget(add, 0)
        self._row.addStretch(1)

    # ------------------------------------------------------------------ #
    ## Designer properties
    # ------------------------------------------------------------------ #
    @Property(str)
    def reactions(self):
        return ",".join("%s:%d" % (e, c) for e, c in self._pairs)

    @reactions.setter
    def reactions(self, text):
        pairs = []
        for tok in str(text).replace(";", ",").split(","):
            tok = tok.strip()
            if not tok:
                continue
            if ":" in tok:
                emoji, _, cnt = tok.rpartition(":")
                try:
                    pairs.append((emoji.strip(), int(cnt)))
                except ValueError:
                    pairs.append((tok, 1))
            else:
                pairs.append((tok, 1))
        self.setReactions(pairs)

    @Property(bool)
    def showAdd(self):
        return self._show_add

    @showAdd.setter
    def showAdd(self, v):
        self._show_add = bool(v)
        self._rebuild()

    @Property(QColor)
    def addColor(self):
        return self._add_color

    @addColor.setter
    def addColor(self, c):
        self._add_color = QColor(c)
        self._rebuild()
