########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/@SpinnTV
# WEBSITE: customwidgets.org
########################################################################

########################################################################
## QCustomTreeWidget - a tokenized hierarchical tree.
##
## Built on QTreeWidget with a convenient nested setItems() API and
## tokenized styling (selection, hover, branches). variant/sizeVariant.
########################################################################
from qtpy.QtCore import Qt, Property
from qtpy.QtWidgets import QTreeWidget, QTreeWidgetItem


class QCustomTreeWidget(QTreeWidget):
    WIDGET_ICON = "components/icons/tree.png"
    WIDGET_TOOLTIP = "A hierarchical tree"
    WIDGET_MODULE = "Custom_Widgets.QCustomTreeWidget"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomTreeWidget' name='customTreeWidget'>
            <property name='geometry'><rect><x>0</x><y>0</y><width>240</width><height>300</height></rect></property>
        </widget>
    </ui>
    """
    DESIGNER_CUSTOM_PROPS = [
        {"name": "variant", "kind": "str", "group": "Appearance"},
        {"name": "sizeVariant", "kind": "str", "group": "Appearance"},
    ]
    __catalog__ = {
        "name": "QCustomTreeWidget",
        "props": {
            "variant": {"type": "enum",
                        "values": ["primary", "secondary", "outline", "ghost"],
                        "default": "outline"},
            "sizeVariant": {"type": "enum", "values": ["sm", "md", "lg"], "default": "md"},
        },
        "signals": ["itemSelectionChanged", "itemExpanded", "itemCollapsed"],
        "tokens_used": ["surface", "on-surface", "surface-muted", "outline",
                        "accent", "on-primary"],
    }

    def __init__(self, parent=None):
        super().__init__(parent)
        self._variant = "outline"
        self._sizeVariant = "md"
        self.setObjectName("QCustomTreeWidget")
        self.setHeaderHidden(True)
        self.setColumnCount(1)

    def setItems(self, items, headers=None):
        """Build the tree from nested data. Each item is a string, or a dict
        with text / data / children / expanded keys."""
        self.clear()
        if headers:
            self.setHeaderHidden(False)
            self.setColumnCount(len(headers))
            self.setHeaderLabels(list(headers))
        for spec in items or []:
            self._addItem(spec, self.invisibleRootItem())

    def _addItem(self, spec, parent):
        if isinstance(spec, dict):
            text = spec.get("text", "")
            data = spec.get("data")
            children = spec.get("children", [])
            expanded = spec.get("expanded", False)
        else:
            text, data, children, expanded = str(spec), spec, [], False
        item = QTreeWidgetItem([text])
        item.setData(0, Qt.UserRole, data)
        parent.addChild(item)
        for child in children:
            self._addItem(child, item)
        item.setExpanded(expanded)
        return item

    def _repolish(self):
        self.style().unpolish(self)
        self.style().polish(self)
        self.update()

    @Property(str)
    def variant(self):
        return self._variant

    @variant.setter
    def variant(self, value):
        self._variant = str(value)
        self._repolish()

    @Property(str)
    def sizeVariant(self):
        return self._sizeVariant

    @sizeVariant.setter
    def sizeVariant(self, value):
        self._sizeVariant = str(value)
        self._repolish()
