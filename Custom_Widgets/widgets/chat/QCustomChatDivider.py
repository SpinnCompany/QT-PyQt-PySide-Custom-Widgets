########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/@SpinnTV
# WEBSITE: customwidgets.org
########################################################################

########################################################################
## QCustomChatDivider - a thread separator with a centered label.
##
## The "YESTERDAY" / "Today" date pill (and the coloured "Unread messages"
## marker) that separates runs of chat bubbles. Three variants: `pill` (a
## rounded chip centred on transparent space), `line` (label between two hair
## rules), and `unread` (an accent rule + label). Painted-free (a QLabel + a
## painted rule), themeable via qproperties, Designer-droppable so the thread is
## composed in the form.
########################################################################
from qtpy.QtCore import Qt, Property, QRectF
from qtpy.QtGui import QColor, QPainter
from qtpy.QtWidgets import QFrame, QLabel, QHBoxLayout, QWidget, QSizePolicy


class _Rule(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._color = QColor("#e6e9ef")
        self.setFixedHeight(2)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

    def setColor(self, c):
        self._color = QColor(c)
        self.update()

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, True)
        p.setPen(Qt.NoPen)
        p.setBrush(self._color)
        y = self.height() / 2.0 - 0.5
        p.drawRoundedRect(QRectF(0, y, self.width(), 1.4), 0.7, 0.7)
        p.end()


class QCustomChatDivider(QFrame):

    WIDGET_ICON = "components/icons/horizontal_rule.png"
    WIDGET_TOOLTIP = "A chat thread date / unread divider"
    WIDGET_MODULE = "Custom_Widgets.QCustomChatDivider"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomChatDivider' name='customChatDivider'>
            <property name='geometry'><rect><x>0</x><y>0</y><width>420</width><height>28</height></rect></property>
        </widget>
    </ui>
    """
    __catalog__ = {
        "name": "QCustomChatDivider",
        "props": {"text": {"type": "string", "default": "YESTERDAY"},
                  "variant": {"type": "enum", "values": ["pill", "line", "unread"], "default": "pill"},
                  "pillColor": {"type": "color", "default": "#eef1f5"},
                  "textColor": {"type": "color", "default": "#8a93a6"},
                  "lineColor": {"type": "color", "default": "#e6e9ef"},
                  "accentColor": {"type": "color", "default": "#1b74e4"}},
        "signals": [],
        "tokens_used": ["accent"],
    }

    def __init__(self, parent=None, text="", variant="pill"):
        super().__init__(parent)
        self.setObjectName("QCustomChatDivider")
        self._variant = variant if variant in ("pill", "line", "unread") else "pill"
        self._pill = QColor("#eef1f5")
        self._text_color = QColor("#8a93a6")
        self._line_color = QColor("#e6e9ef")
        self._accent = QColor("#1b74e4")

        self._lay = QHBoxLayout(self)
        self._lay.setContentsMargins(0, 6, 0, 6)
        self._lay.setSpacing(10)
        self._leftRule = _Rule(self)
        self._rightRule = _Rule(self)
        self._label = QLabel(text, self)
        self._label.setObjectName("chatDividerLabel")
        self._label.setAlignment(Qt.AlignCenter)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self._rebuild()

    def _rebuild(self):
        while self._lay.count():
            it = self._lay.takeAt(0)
            w = it.widget()
            if w is not None:
                w.setParent(self)
        if self._variant == "pill":
            self._lay.addStretch(1)
            self._lay.addWidget(self._label, 0)
            self._lay.addStretch(1)
            self._leftRule.hide()
            self._rightRule.hide()
        else:
            self._leftRule.show()
            self._rightRule.show()
            self._lay.addWidget(self._leftRule, 1)
            self._lay.addWidget(self._label, 0)
            self._lay.addWidget(self._rightRule, 1)
        self._restyle()

    def _restyle(self):
        # `variant` is a Qt property the app QSS targets
        # (QCustomChatDivider[variant="pill"] #chatDividerLabel {…}); the painted
        # rules read their colour from qproperties the QSS sets. No per-widget
        # stylesheet — only a re-polish so the theme engine re-evaluates us.
        if self._variant == "unread":
            self._leftRule.setColor(self._accent)
            self._rightRule.setColor(self._accent)
        elif self._variant == "line":
            self._leftRule.setColor(self._line_color)
            self._rightRule.setColor(self._line_color)
        self.style().unpolish(self)
        self.style().polish(self)
        self._label.style().unpolish(self._label)
        self._label.style().polish(self._label)

    # ------------------------------------------------------------------ #
    ## Designer properties
    # ------------------------------------------------------------------ #
    @Property(str)
    def text(self):
        return self._label.text()

    @text.setter
    def text(self, v):
        self._label.setText(str(v))

    @Property(str)
    def variant(self):
        return self._variant

    @variant.setter
    def variant(self, v):
        v = str(v)
        if v in ("pill", "line", "unread"):
            self._variant = v
            self._rebuild()

    @Property(QColor)
    def pillColor(self):
        return self._pill

    @pillColor.setter
    def pillColor(self, c):
        self._pill = QColor(c)
        self._restyle()

    @Property(QColor)
    def textColor(self):
        return self._text_color

    @textColor.setter
    def textColor(self, c):
        self._text_color = QColor(c)
        self._restyle()

    @Property(QColor)
    def lineColor(self):
        return self._line_color

    @lineColor.setter
    def lineColor(self, c):
        self._line_color = QColor(c)
        self._restyle()

    @Property(QColor)
    def accentColor(self):
        return self._accent

    @accentColor.setter
    def accentColor(self, c):
        self._accent = QColor(c)
        self._restyle()
