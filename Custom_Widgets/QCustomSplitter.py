########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/spinnTv
# WEBSITE: spinncode.com
########################################################################

########################################################################
## QCustomSplitter - a QSplitter with a tokenized, grippable handle.
##
## A drop-in QSplitter whose handle colour follows the design tokens (subtle
## by default, accent on hover) and is comfortable to grab. Everything else is
## standard QSplitter (addWidget, setSizes, saveState, splitterMoved, ...).
########################################################################
from qtpy.QtCore import Property, Qt
from qtpy.QtWidgets import QSplitter


class QCustomSplitter(QSplitter):

    WIDGET_ICON = "components/icons/vertical_split.png"
    WIDGET_TOOLTIP = "A splitter with a tokenized handle"
    WIDGET_MODULE = "Custom_Widgets.QCustomSplitter"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomSplitter' name='customSplitter'>
            <property name='geometry'><rect><x>0</x><y>0</y><width>320</width><height>200</height></rect></property>
            <property name='orientation'><enum>Qt::Horizontal</enum></property>
        </widget>
    </ui>
    """
    __catalog__ = {
        "name": "QCustomSplitter",
        "props": {"orientation": {"type": "enum",
                                  "values": ["horizontal", "vertical"],
                                  "default": "horizontal"}},
        "signals": ["splitterMoved"],
        "tokens_used": ["outline", "accent", "surface"],
    }

    def __init__(self, orientation=Qt.Horizontal, parent=None):
        super().__init__(orientation, parent)
        self.setObjectName("QCustomSplitter")
        self.setHandleWidth(6)
        self.setChildrenCollapsible(False)

    # ------------------------------------------------------------------ #
    ## Designer-friendly string orientation
    # ------------------------------------------------------------------ #
    @Property(str)
    def orientationName(self):
        return "vertical" if self.orientation() == Qt.Vertical else "horizontal"

    @orientationName.setter
    def orientationName(self, value):
        self.setOrientation(
            Qt.Vertical if str(value).lower().startswith("v") else Qt.Horizontal)
