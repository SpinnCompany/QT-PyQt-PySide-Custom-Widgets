from qtpy.QtCore import Qt, Property, QSize
from qtpy.QtGui import QColor
from qtpy.QtWidgets import QLineEdit, QVBoxLayout, QLabel, QWidget


class QCustomInput(QLineEdit):
    """A modern text input with design-token variants and sizes.
    
    Replaces hand-crafted QLineEdit styling with a tokenized API:
    - variant: "primary" | "secondary" | "outline" (default) | "ghost"
    - sizeVariant: "sm" | "md" (default) | "lg"
    - state: "default" | "focused" | "error" | "disabled"
    
    Works seamlessly with QCustomForm fields.
    """

    WIDGET_ICON = "components/icons/text_input.png"
    WIDGET_TOOLTIP = "A modern text input with variant/size styling"
    WIDGET_MODULE = "Custom_Widgets.QCustomInput"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomInput' name='customInput'>
            <property name='geometry'><rect><x>0</x><y>0</y><width>200</width><height>36</height></rect></property>
            <property name='placeholderText'><string>Enter text...</string></property>
        </widget>
    </ui>
    """

    __catalog__ = {
        "name": "QCustomInput",
        "props": {
            "variant": {"type": "enum",
                        "values": ["primary", "secondary", "outline", "ghost"],
                        "default": "outline"},
            "sizeVariant": {"type": "enum", "values": ["sm", "md", "lg"],
                            "default": "md"},
        },
        "signals": ["textChanged", "returnPressed"],
        "tokens_used": ["surface", "on-surface", "outline", "focus-ring", "accent"],
    }

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("QCustomInput")
        self._variant = "outline"
        self._sizeVariant = "md"
        self._state = "default"
        self._setSizePolicy()

    def _setSizePolicy(self):
        """Apply padding and height based on size variant."""
        if self._sizeVariant == "sm":
            self.setMinimumHeight(28)
            self.setMaximumHeight(28)
        elif self._sizeVariant == "md":
            self.setMinimumHeight(36)
            self.setMaximumHeight(36)
        elif self._sizeVariant == "lg":
            self.setMinimumHeight(44)
            self.setMaximumHeight(44)
        self._repolish()

    def _repolish(self):
        """Re-evaluate QSS attribute selectors after a dynamic property change."""
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
        self._setSizePolicy()

    @Property(str)
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        self._state = str(value)
        self._repolish()

    def setError(self, error_text=None):
        """Set the input to error state and optionally show an error message."""
        if error_text:
            self._state = "error"
            self.setToolTip(error_text)
        else:
            self._state = "default"
            self.setToolTip("")
        self._repolish()

    def focusInEvent(self, event):
        super().focusInEvent(event)
        self._state = "focused"
        self._repolish()

    def focusOutEvent(self, event):
        super().focusOutEvent(event)
        self._state = "default"
        self._repolish()
