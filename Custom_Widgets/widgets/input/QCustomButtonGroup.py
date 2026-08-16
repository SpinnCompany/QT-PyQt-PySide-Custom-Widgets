from qtpy.QtCore import Qt, Property, Signal
from qtpy.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QButtonGroup, QPushButton


from Custom_Widgets.accessibility import set_accessibility, QAccessible


class QCustomButtonGroup(QWidget):
    """An accessible button group (radio-style or checkbox-style selection).
    
    Wraps QButtonGroup with a tokenized, variant-aware presentation:
    - variant: "primary" | "secondary" | "outline" (default)
    - sizeVariant: "sm" | "md" (default) | "lg"
    - exclusive: True (radio) or False (checkbox)
    - orientation: "horizontal" | "vertical" (default)
    
    Each button carries the same variant/size as the group, with a 
    "selected" state that's driven by the button group's selection.
    """

    WIDGET_ICON = "components/icons/smart_button.png"
    WIDGET_TOOLTIP = "A tokenized, accessible button group"
    WIDGET_MODULE = "Custom_Widgets.QCustomButtonGroup"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomButtonGroup' name='customButtonGroup'>
            <property name='geometry'><rect><x>0</x><y>0</y><width>300</width><height>40</height></rect></property>
        </widget>
    </ui>
    """

    selectionChanged = Signal(int, str)  # button_id, button_text

    __catalog__ = {
        "name": "QCustomButtonGroup",
        "props": {
            "variant": {"type": "enum",
                        "values": ["primary", "secondary", "outline"],
                        "default": "outline"},
            "sizeVariant": {"type": "enum", "values": ["sm", "md", "lg"],
                            "default": "md"},
            "exclusive": {"type": "bool", "default": True},
            "orientation": {"type": "enum", "values": ["horizontal", "vertical"],
                            "default": "vertical"},
        },
        "signals": ["selectionChanged"],
        "tokens_used": ["surface", "on-surface", "accent", "primary", "outline"],
    }

    def __init__(self, parent=None, exclusive=True, orientation="vertical"):
        super().__init__(parent)
        self.setObjectName("QCustomButtonGroup")
        self._variant = "outline"
        self._sizeVariant = "md"
        self._exclusive = bool(exclusive)
        self._orientation = orientation
        self._group = QButtonGroup(self)
        self._group.setExclusive(self._exclusive)
        self._group.buttonClicked.connect(self._onSelectionChanged)

        # Container layout
        if orientation == "horizontal":
            self._layout = QHBoxLayout(self)
        else:
            self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(4)
        set_accessibility(self, QAccessible.Grouping, self.toolTip() or "Button group")

    def _onSelectionChanged(self, btn):
        """Emit selectionChanged signal when a button is clicked."""
        btn_id = self._group.id(btn)
        self.selectionChanged.emit(btn_id, btn.text())

    def addButton(self, text, button_id=None):
        """Add a button to the group."""
        btn = QPushButton(text, self)
        btn.setProperty("variant", self._variant)
        btn.setProperty("sizeVariant", self._sizeVariant)
        btn.setCheckable(True)
        if button_id is None:
            button_id = len(self._group.buttons())
        self._group.addButton(btn, button_id)
        self._layout.addWidget(btn)
        return btn

    def setButtons(self, items):
        """Replace all buttons. Items may be strings or (text, id) pairs."""
        # Clear existing
        for btn in self._group.buttons():
            self._layout.removeWidget(btn)
            btn.deleteLater()
        self._group = QButtonGroup(self)
        self._group.setExclusive(self._exclusive)
        self._group.buttonClicked.connect(self._onSelectionChanged)

        # Add new
        for idx, item in enumerate(items or []):
            if isinstance(item, (tuple, list)):
                text, bid = item[0], item[1]
            else:
                text, bid = item, idx
            self.addButton(text, bid)

    def selectedId(self):
        """Return the ID of the selected button, or -1 if none."""
        return self._group.checkedId()

    def selectedText(self):
        """Return the text of the selected button, or empty string if none."""
        btn = self._group.checkedButton()
        return btn.text() if btn else ""

    def setSelectedId(self, button_id):
        """Set the selected button by ID."""
        btn = self._group.button(button_id)
        if btn:
            btn.setChecked(True)

    def _repolish(self):
        """Re-apply variant/size to all buttons."""
        for btn in self._group.buttons():
            btn.setProperty("variant", self._variant)
            btn.setProperty("sizeVariant", self._sizeVariant)
            btn.style().unpolish(btn)
            btn.style().polish(btn)
            btn.update()

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

    @Property(bool)
    def exclusive(self):
        return self._exclusive

    @exclusive.setter
    def exclusive(self, value):
        self._exclusive = bool(value)
        self._group.setExclusive(self._exclusive)

    @Property(str)
    def orientation(self):
        return self._orientation

    @orientation.setter
    def orientation(self, value):
        value = "horizontal" if str(value).lower() == "horizontal" else "vertical"
        if value == self._orientation:
            return
        self._orientation = value
        self._rebuildLayout()

    def _rebuildLayout(self):
        """Swap the container layout to match the orientation, keeping the
        buttons (in order), margins, spacing and the current selection."""
        wanted = QHBoxLayout if self._orientation == "horizontal" else QVBoxLayout
        old = self._layout
        if type(old) is wanted:
            return
        new = wanted()
        new.setContentsMargins(old.contentsMargins())
        new.setSpacing(old.spacing())
        while old.count():
            item = old.takeAt(0)
            widget = item.widget()
            if widget is not None:
                new.addWidget(widget)
        # A widget refuses a second layout while the old one is installed:
        # hand the empty husk to a throwaway parent, then install the new one.
        QWidget().setLayout(old)
        self._layout = new
        self.setLayout(new)
