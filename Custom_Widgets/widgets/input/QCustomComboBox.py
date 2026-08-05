########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/@SpinnTV
# WEBSITE: customwidgets.org
########################################################################

########################################################################
## QCustomComboBox - a searchable / autocomplete select.
##
## Built on QComboBox + QCompleter so keyboard navigation, popup filtering
## and focus handling are correct, with a tokenized look and a convenient
## items API. Editable mode gives type-to-filter (substring) autocomplete;
## the arrow still shows the full list.
##
##     c = QCustomComboBox()
##     c.setItems(["Apple", "Banana", ("Grape", 3), {"label": "Kiwi", "value": 9}])
##     c.currentData(); c.currentText()
########################################################################
from qtpy.QtCore import Qt, Property
from qtpy.QtWidgets import QComboBox, QCompleter


class QCustomComboBox(QComboBox):
    # Designer registration
    WIDGET_ICON = "components/icons/combobox.png"
    WIDGET_TOOLTIP = "A searchable / autocomplete select"
    WIDGET_MODULE = "Custom_Widgets.QCustomComboBox"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomComboBox' name='customComboBox'>
            <property name='geometry'>
                <rect><x>0</x><y>0</y><width>200</width><height>32</height></rect>
            </property>
        </widget>
    </ui>
    """

    DESIGNER_CUSTOM_PROPS = [
        {"name": "editable", "kind": "bool", "group": "Combo Box"},
        {"name": "variant", "kind": "str", "group": "Appearance"},
        {"name": "sizeVariant", "kind": "str", "group": "Appearance"},
    ]

    __catalog__ = {
        "name": "QCustomComboBox",
        "props": {
            "editable": {"type": "bool", "default": True},
            "variant": {"type": "enum",
                        "values": ["primary", "secondary", "outline", "ghost"],
                        "default": "outline"},
            "sizeVariant": {"type": "enum", "values": ["sm", "md", "lg"],
                            "default": "md"},
        },
        "signals": ["currentIndexChanged", "currentTextChanged", "activated"],
        "tokens_used": ["surface", "on-surface", "surface-muted", "outline",
                        "accent", "on-primary", "focus-ring"],
    }

    def __init__(self, parent=None, editable=True):
        super().__init__(parent)
        self._variant = "outline"
        self._sizeVariant = "md"
        self.setObjectName("QCustomComboBox")
        self.view().setObjectName("comboDropdown")     # the arrow popup list
        self.setEditable(editable)

    # ------------------------------------------------------------------ #
    ## Editable + autocomplete
    # ------------------------------------------------------------------ #
    def setEditable(self, editable):
        super().setEditable(editable)
        if not editable:
            return
        # don't turn typed text into a new item; keep known-item selection clean
        self.setInsertPolicy(QComboBox.NoInsert)
        comp = self.completer()
        if comp is not None:
            comp.setCompletionMode(QCompleter.PopupCompletion)
            comp.setFilterMode(Qt.MatchContains)          # substring, not just prefix
            comp.setCaseSensitivity(Qt.CaseInsensitive)
            popup = comp.popup()
            if popup is not None:
                popup.setObjectName("comboCompleterPopup")

    def placeholderText(self):
        le = self.lineEdit()
        return le.placeholderText() if le is not None else ""

    def setPlaceholderText(self, text):
        le = self.lineEdit()
        if le is not None:
            le.setPlaceholderText(text)

    # ------------------------------------------------------------------ #
    ## Items API
    # ------------------------------------------------------------------ #
    def setItems(self, items):
        """Replace all items. Each item may be a string, a (label, data) pair,
        or a dict with label/text and value/data keys."""
        self.clear()
        for item in items or []:
            if isinstance(item, dict):
                label = item.get("label", item.get("text", ""))
                data = item.get("value", item.get("data"))
            elif isinstance(item, (tuple, list)) and len(item) >= 2:
                label, data = item[0], item[1]
            else:
                label, data = item, item
            self.addItem(str(label), data)

    def currentValue(self):
        """Alias for currentData()."""
        return self.currentData()

    def _repolish(self):
        self.style().unpolish(self)
        self.style().polish(self)
        self.update()

    # ------------------------------------------------------------------ #
    ## Properties (declared; QSS attribute selectors read them via the getter)
    # ------------------------------------------------------------------ #
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
