########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/@SpinnTV
# WEBSITE: customwidgets.org
########################################################################

########################################################################
## QCustomCard - a surface container with an optional header.
##
## A rounded, bordered panel: an optional header (title + subtitle) above a body
## content area you fill with your own widgets (addWidget / contentLayout).
## The base other cards compose. Tokenized; a Designer container so widgets drop
## straight into the body.
########################################################################
from qtpy.QtCore import Qt, Property
from qtpy.QtWidgets import QWidget, QVBoxLayout, QLabel


class QCustomCard(QWidget):
    WIDGET_ICON = "components/icons/web_asset.png"
    WIDGET_TOOLTIP = "A card / surface container"
    WIDGET_MODULE = "Custom_Widgets.QCustomCard"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomCard' name='customCard'>
            <property name='geometry'><rect><x>0</x><y>0</y><width>260</width><height>160</height></rect></property>
        </widget>
    </ui>
    """
    __catalog__ = {
        "name": "QCustomCard",
        "props": {"title": {"type": "string", "default": ""},
                  "subtitle": {"type": "string", "default": ""}},
        "signals": [],
        "tokens_used": ["surface", "on-surface", "outline", "surface-muted"],
    }

    def __init__(self, parent=None, title="", subtitle=""):
        super().__init__(parent)
        self.setObjectName("QCustomCard")
        self.setAttribute(Qt.WA_StyledBackground, True)

        self._root = QVBoxLayout(self)
        self._root.setContentsMargins(16, 14, 16, 16)
        self._root.setSpacing(4)

        self._title = QLabel(self)
        self._title.setObjectName("cardTitle")
        self._title.setWordWrap(True)
        self._root.addWidget(self._title)

        self._subtitle = QLabel(self)
        self._subtitle.setObjectName("cardSubtitle")
        self._subtitle.setWordWrap(True)
        self._root.addWidget(self._subtitle)

        # body: the content area callers fill
        self._body = QWidget(self)
        self._body.setObjectName("cardBody")
        self._bodyLayout = QVBoxLayout(self._body)
        self._bodyLayout.setContentsMargins(0, 0, 0, 0)
        self._bodyLayout.setSpacing(8)
        self._root.addWidget(self._body, 1)

        self.setTitle(title)
        self.setSubtitle(subtitle)

    # ------------------------------------------------------------------ #
    ## Content API
    # ------------------------------------------------------------------ #
    def contentLayout(self):
        """The body QVBoxLayout - add rows/widgets here."""
        return self._bodyLayout

    def body(self):
        return self._body

    def addWidget(self, widget):
        self._bodyLayout.addWidget(widget)

    def addLayout(self, layout):
        self._bodyLayout.addLayout(layout)

    def _syncHeader(self):
        has_header = bool(self._title.text()) or bool(self._subtitle.text())
        self._root.setSpacing(4 if has_header else 0)

    # ------------------------------------------------------------------ #
    ## Header API / Designer properties
    # ------------------------------------------------------------------ #
    def setTitle(self, text):
        text = text or ""
        self._title.setText(text)
        self._title.setVisible(bool(text))
        self._syncHeader()

    def setSubtitle(self, text):
        text = text or ""
        self._subtitle.setText(text)
        self._subtitle.setVisible(bool(text))
        self._syncHeader()

    @Property(str)
    def title(self):
        return self._title.text()

    @title.setter
    def title(self, value):
        self.setTitle(value)

    @Property(str)
    def subtitle(self):
        return self._subtitle.text()

    @subtitle.setter
    def subtitle(self, value):
        self.setSubtitle(value)
