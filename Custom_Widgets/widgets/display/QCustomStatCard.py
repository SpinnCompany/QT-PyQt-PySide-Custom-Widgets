########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/spinnTv
# WEBSITE: spinncode.com
########################################################################

########################################################################
## QCustomStatCard - a KPI / metric card.
##
## A compact dashboard tile: a small label, a large value, and an optional
## delta with a trend (up / down / flat) coloured from the semantic tokens
## (up=success, down=destructive, flat=muted), plus an optional caption. The
## trend drives colour via the `trend` dynamic property + QSS attribute
## selectors.
########################################################################
from qtpy.QtCore import Qt, Property
from qtpy.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel


class QCustomStatCard(QWidget):
    WIDGET_ICON = "components/icons/statcard.png"
    WIDGET_TOOLTIP = "A KPI / metric card"
    WIDGET_MODULE = "Custom_Widgets.QCustomStatCard"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomStatCard' name='customStatCard'>
            <property name='geometry'><rect><x>0</x><y>0</y><width>200</width><height>110</height></rect></property>
        </widget>
    </ui>
    """
    __catalog__ = {
        "name": "QCustomStatCard",
        "props": {"label": {"type": "string", "default": ""},
                  "value": {"type": "string", "default": ""},
                  "caption": {"type": "string", "default": ""},
                  "trend": {"type": "enum", "values": ["up", "down", "flat"],
                            "default": "flat"}},
        "signals": [],
        "tokens_used": ["surface", "on-surface", "outline", "surface-muted",
                        "success", "destructive"],
    }

    _ARROWS = {"up": "▲", "down": "▼", "flat": ""}

    def __init__(self, parent=None, label="", value="", delta="", trend="flat",
                 caption=""):
        super().__init__(parent)
        self.setObjectName("QCustomStatCard")
        self.setAttribute(Qt.WA_StyledBackground, True)
        self._trend = trend if trend in self._ARROWS else "flat"

        outer = QVBoxLayout(self)
        outer.setContentsMargins(14, 12, 14, 12)
        outer.setSpacing(4)

        self._label = QLabel(self)
        self._label.setObjectName("statLabel")
        outer.addWidget(self._label)

        self._value = QLabel(self)
        self._value.setObjectName("statValue")
        outer.addWidget(self._value)

        deltaRow = QHBoxLayout()
        deltaRow.setContentsMargins(0, 0, 0, 0)
        deltaRow.setSpacing(4)
        self._delta = QLabel(self)
        self._delta.setObjectName("statDelta")
        deltaRow.addWidget(self._delta)
        self._caption = QLabel(self)
        self._caption.setObjectName("statCaption")
        deltaRow.addWidget(self._caption)
        deltaRow.addStretch(1)
        outer.addLayout(deltaRow)

        self.setLabel(label)
        self.setValue(value)
        self.setCaption(caption)
        self.setDelta(delta, trend)

    # ------------------------------------------------------------------ #
    ## Public API
    # ------------------------------------------------------------------ #
    def setLabel(self, text):
        text = text or ""
        self._label.setText(text)
        self._label.setVisible(bool(text))

    def setValue(self, text):
        self._value.setText("" if text is None else str(text))

    def setCaption(self, text):
        text = text or ""
        self._caption.setText(text)
        self._caption.setVisible(bool(text))

    def setDelta(self, text, trend=None):
        """Set the delta text (e.g. "+12.5%") and, optionally, the trend
        (up / down / flat) that colours it."""
        text = text or ""
        if trend is not None:
            self._trend = trend if trend in self._ARROWS else "flat"
        arrow = self._ARROWS.get(self._trend, "")
        shown = ("%s %s" % (arrow, text)).strip() if text else ""
        self._delta.setText(shown)
        self._delta.setVisible(bool(shown))
        self._repolish()

    def setTrend(self, trend):
        self._trend = trend if trend in self._ARROWS else "flat"
        self.setDelta(self._rawDelta(), self._trend)

    def _rawDelta(self):
        # strip a leading arrow glyph back off, for re-rendering on trend change
        txt = self._delta.text()
        for a in self._ARROWS.values():
            if a and txt.startswith(a):
                return txt[len(a):].strip()
        return txt

    def _repolish(self):
        for w in (self, self._delta):
            w.style().unpolish(w)
            w.style().polish(w)

    # ------------------------------------------------------------------ #
    ## Designer properties
    # ------------------------------------------------------------------ #
    @Property(str)
    def label(self):
        return self._label.text()

    @label.setter
    def label(self, value):
        self.setLabel(value)

    @Property(str)
    def value(self):
        return self._value.text()

    @value.setter
    def value(self, v):
        self.setValue(v)

    @Property(str)
    def caption(self):
        return self._caption.text()

    @caption.setter
    def caption(self, v):
        self.setCaption(v)

    @Property(str)
    def trend(self):
        return self._trend

    @trend.setter
    def trend(self, v):
        self.setTrend(v)
