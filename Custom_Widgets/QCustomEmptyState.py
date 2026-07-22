########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/spinnTv
# WEBSITE: spinncode.com
########################################################################

########################################################################
## QCustomEmptyState - a centered "nothing here yet" placeholder.
##
## A large glyph (or pixmap) + title + description + an optional action
## button. Tokenized. Emits actionClicked.
########################################################################
from qtpy.QtCore import Qt, Signal
from qtpy.QtWidgets import QWidget, QVBoxLayout, QLabel

from Custom_Widgets.QCustomQPushButton import QCustomQPushButton


class QCustomEmptyState(QWidget):
    actionClicked = Signal()

    WIDGET_ICON = "components/icons/emptystate.png"
    WIDGET_TOOLTIP = "An empty-state placeholder"
    WIDGET_MODULE = "Custom_Widgets.QCustomEmptyState"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomEmptyState' name='customEmptyState'>
            <property name='geometry'><rect><x>0</x><y>0</y><width>280</width><height>220</height></rect></property>
        </widget>
    </ui>
    """
    __catalog__ = {
        "name": "QCustomEmptyState",
        "props": {},
        "signals": ["actionClicked"],
        "tokens_used": ["on-surface", "outline", "surface-muted", "accent"],
    }

    def __init__(self, parent=None, icon="📭", title="Nothing here yet",
                 description=""):
        super().__init__(parent)
        self.setObjectName("QCustomEmptyState")
        col = QVBoxLayout(self)
        col.setAlignment(Qt.AlignCenter)
        col.setSpacing(8)

        self._icon = QLabel(icon, self)
        self._icon.setObjectName("emptyIcon")
        self._icon.setAlignment(Qt.AlignCenter)
        col.addWidget(self._icon, 0, Qt.AlignHCenter)

        self._title = QLabel(title, self)
        self._title.setObjectName("emptyTitle")
        self._title.setAlignment(Qt.AlignCenter)
        col.addWidget(self._title)

        self._desc = QLabel(description, self)
        self._desc.setObjectName("emptyDesc")
        self._desc.setAlignment(Qt.AlignCenter)
        self._desc.setWordWrap(True)
        self._desc.setVisible(bool(description))
        col.addWidget(self._desc)

        self._action = QCustomQPushButton(self)
        self._action.variant = "primary"
        self._action.setVisible(False)
        self._action.clicked.connect(self.actionClicked)
        col.addWidget(self._action, 0, Qt.AlignHCenter)

    # -- API --
    def setIcon(self, glyph_or_pixmap):
        if isinstance(glyph_or_pixmap, str):
            self._icon.setText(glyph_or_pixmap)
        else:
            self._icon.setPixmap(glyph_or_pixmap)

    def setTitle(self, title):
        self._title.setText(title)

    def setDescription(self, description):
        self._desc.setText(description)
        self._desc.setVisible(bool(description))

    def setActionText(self, text):
        self._action.setText(text)
        self._action.setVisible(bool(text))

    def actionButton(self):
        return self._action
