########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/spinnTv
# WEBSITE: spinncode.com
########################################################################

########################################################################
## QCustomTabWidget - a tokenized tab container.
##
## Built on QTabWidget (correct tab management + keyboard) with three
## token-styled looks via the `tabStyle` property: "underline" (default),
## "pills", "enclosed". Density follows `sizeVariant`.
########################################################################
from qtpy.QtCore import Property
from qtpy.QtWidgets import QTabWidget


class QCustomTabWidget(QTabWidget):
    WIDGET_ICON = "components/icons/tabs.png"
    WIDGET_TOOLTIP = "A tokenized tab container (underline / pills / enclosed)"
    WIDGET_MODULE = "Custom_Widgets.QCustomTabWidget"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomTabWidget' name='customTabWidget'>
            <property name='geometry'><rect><x>0</x><y>0</y><width>400</width><height>300</height></rect></property>
            <widget class='QWidget' name='tab1'><attribute name='title'><string>Tab 1</string></attribute></widget>
            <widget class='QWidget' name='tab2'><attribute name='title'><string>Tab 2</string></attribute></widget>
        </widget>
    </ui>
    """
    DESIGNER_CUSTOM_PROPS = [
        {"name": "tabStyle", "kind": "str", "group": "Tabs"},
        {"name": "sizeVariant", "kind": "str", "group": "Appearance"},
    ]
    __catalog__ = {
        "name": "QCustomTabWidget",
        "props": {
            "tabStyle": {"type": "enum", "values": ["underline", "pills", "enclosed"],
                         "default": "underline"},
            "sizeVariant": {"type": "enum", "values": ["sm", "md", "lg"], "default": "md"},
        },
        "signals": ["currentChanged", "tabCloseRequested"],
        "tokens_used": ["surface", "on-surface", "surface-muted", "outline",
                        "accent", "on-primary"],
    }

    def __init__(self, parent=None):
        super().__init__(parent)
        self._tabStyle = "underline"
        self._sizeVariant = "md"
        self.setObjectName("QCustomTabWidget")

    def _repolish(self):
        self.style().unpolish(self)
        self.style().polish(self)
        self.tabBar().update()
        self.update()

    @Property(str)
    def tabStyle(self):
        return self._tabStyle

    @tabStyle.setter
    def tabStyle(self, value):
        self._tabStyle = str(value)
        self._repolish()

    @Property(str)
    def sizeVariant(self):
        return self._sizeVariant

    @sizeVariant.setter
    def sizeVariant(self, value):
        self._sizeVariant = str(value)
        self._repolish()
