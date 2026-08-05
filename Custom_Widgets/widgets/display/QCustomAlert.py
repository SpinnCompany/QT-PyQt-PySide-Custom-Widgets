########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/@SpinnTV
# WEBSITE: customwidgets.org
########################################################################

########################################################################
## QCustomAlert - an inline callout / banner.
##
## A static, non-transient message block (unlike the auto-dismiss QCustomToast):
## a leading glyph, an optional bold title, the message text, and an optional
## close button. Four semantic variants drive the colour via the `variant`
## dynamic property + QSS attribute selectors: info / success / warning /
## destructive. Emits closed when dismissed.
########################################################################
from qtpy.QtCore import Qt, Signal, Property
from qtpy.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QLabel,
                            QPushButton, QSizePolicy)


class QCustomAlert(QWidget):
    closed = Signal()

    WIDGET_ICON = "components/icons/alert.png"
    WIDGET_TOOLTIP = "An inline alert / callout banner"
    WIDGET_MODULE = "Custom_Widgets.QCustomAlert"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomAlert' name='customAlert'>
            <property name='geometry'><rect><x>0</x><y>0</y><width>320</width><height>60</height></rect></property>
        </widget>
    </ui>
    """
    __catalog__ = {
        "name": "QCustomAlert",
        "props": {"variant": {"type": "enum",
                              "values": ["info", "success", "warning", "destructive"],
                              "default": "info"},
                  "title": {"type": "string", "default": ""},
                  "text": {"type": "string", "default": ""},
                  "dismissible": {"type": "bool", "default": False}},
        "signals": ["closed"],
        "tokens_used": ["surface", "on-surface", "info", "success", "warning",
                        "destructive", "outline"],
    }

    _GLYPHS = {"info": "ℹ", "success": "✓", "warning": "⚠", "destructive": "✕"}

    def __init__(self, parent=None, title="", text="", variant="info",
                 dismissible=False):
        super().__init__(parent)
        self.setObjectName("QCustomAlert")
        self.setAttribute(Qt.WA_StyledBackground, True)
        self._variant = variant if variant in self._GLYPHS else "info"
        self._dismissible = bool(dismissible)

        row = QHBoxLayout(self)
        row.setContentsMargins(12, 10, 10, 10)
        row.setSpacing(10)

        self._icon = QLabel(self)
        self._icon.setObjectName("alertIcon")
        self._icon.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        row.addWidget(self._icon, 0, Qt.AlignTop)

        body = QVBoxLayout()
        body.setContentsMargins(0, 0, 0, 0)
        body.setSpacing(2)
        self._title = QLabel(self)
        self._title.setObjectName("alertTitle")
        self._title.setWordWrap(True)
        self._text = QLabel(self)
        self._text.setObjectName("alertText")
        self._text.setWordWrap(True)
        self._text.setTextInteractionFlags(Qt.TextSelectableByMouse)
        body.addWidget(self._title)
        body.addWidget(self._text)
        row.addLayout(body, 1)

        self._close = QPushButton("✕", self)
        self._close.setObjectName("alertClose")
        self._close.setCursor(Qt.PointingHandCursor)
        self._close.setFocusPolicy(Qt.NoFocus)
        self._close.setFixedSize(20, 20)
        self._close.clicked.connect(self._onClose)
        row.addWidget(self._close, 0, Qt.AlignTop)

        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        self.setTitle(title)
        self.setText(text)
        self._applyVariant()
        self.setDismissible(dismissible)

    # ------------------------------------------------------------------ #
    ## Behaviour
    # ------------------------------------------------------------------ #
    def _onClose(self):
        self.hide()
        self.closed.emit()

    def _applyVariant(self):
        self._icon.setText(self._GLYPHS.get(self._variant, "ℹ"))
        self._repolish()

    def _repolish(self):
        for w in (self, self._icon, self._title, self._text):
            w.style().unpolish(w)
            w.style().polish(w)

    # ------------------------------------------------------------------ #
    ## Public API
    # ------------------------------------------------------------------ #
    def setTitle(self, title):
        title = title or ""
        self._title.setText(title)
        self._title.setVisible(bool(title))

    def setText(self, text):
        text = text or ""
        self._text.setText(text)
        self._text.setVisible(bool(text))

    def setDismissible(self, dismissible):
        self._dismissible = bool(dismissible)
        self._close.setVisible(self._dismissible)

    def isDismissible(self):
        return self._dismissible

    def closeButton(self):
        return self._close

    @Property(str)
    def variant(self):
        return self._variant

    @variant.setter
    def variant(self, value):
        value = str(value)
        self._variant = value if value in self._GLYPHS else "info"
        self._applyVariant()

    @Property(str)
    def title(self):
        return self._title.text()

    @title.setter
    def title(self, value):
        self.setTitle(value)

    @Property(str)
    def text(self):
        return self._text.text()

    @text.setter
    def text(self, value):
        self.setText(value)

    @Property(bool)
    def dismissible(self):
        return self._dismissible

    @dismissible.setter
    def dismissible(self, value):
        self.setDismissible(value)
