########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/@SpinnTV
# WEBSITE: customwidgets.org
########################################################################

########################################################################
## QCustomKbd - render a keyboard shortcut as styled keycaps.
##
## The HTML <kbd> equivalent: pass a shortcut string ("Ctrl+K", "Cmd+Shift+P")
## or a list of keys and each is drawn as a small tokenized keycap joined by
## "+" separators. Read-only / display only.
########################################################################
from qtpy.QtCore import Property, Qt
from qtpy.QtWidgets import QWidget, QHBoxLayout, QLabel


class QCustomKbd(QWidget):

    WIDGET_ICON = "components/icons/keyboard.png"
    WIDGET_TOOLTIP = "Render a keyboard shortcut as keycaps"
    WIDGET_MODULE = "Custom_Widgets.QCustomKbd"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomKbd' name='customKbd'>
            <property name='geometry'><rect><x>0</x><y>0</y><width>110</width><height>28</height></rect></property>
            <property name='keys'><string>Ctrl+K</string></property>
        </widget>
    </ui>
    """
    __catalog__ = {
        "name": "QCustomKbd",
        "props": {"keys": {"type": "string", "default": "Ctrl+K"},
                  "separator": {"type": "string", "default": "+"}},
        "signals": [],
        "tokens_used": ["surface-muted", "on-surface", "outline"],
    }

    def __init__(self, keys="Ctrl+K", parent=None, separator="+"):
        # Qt Designer / uic instantiate custom widgets as ``Widget(parent)``.
        # ``keys`` is the first positional arg, so a parent passed positionally
        # would be mistaken for the shortcut string. Detect a QWidget here and
        # treat it as the parent so promoted .ui forms load correctly.
        if isinstance(keys, QWidget) and parent is None:
            keys, parent = "Ctrl+K", keys
        super().__init__(parent)
        self.setObjectName("QCustomKbd")
        self._separator = separator or "+"
        self._keys = []
        self._row = QHBoxLayout(self)
        self._row.setContentsMargins(0, 0, 0, 0)
        self._row.setSpacing(4)
        self._row.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.setKeys(keys)

    # ------------------------------------------------------------------ #
    ## API
    # ------------------------------------------------------------------ #
    def setKeys(self, keys):
        """Accept a shortcut string ("Ctrl+K") split on the separator, or an
        explicit list of key labels."""
        if isinstance(keys, str):
            parts = [k.strip() for k in keys.split(self._separator) if k.strip()]
        else:
            parts = [str(k).strip() for k in (keys or []) if str(k).strip()]
        self._keys = parts
        self._rebuild()

    def keysList(self):
        return list(self._keys)

    def _clear(self):
        while self._row.count():
            item = self._row.takeAt(0)
            w = item.widget()
            if w is not None:
                w.setParent(None)
                w.deleteLater()

    def _rebuild(self):
        self._clear()
        for i, key in enumerate(self._keys):
            if i > 0:
                plus = QLabel(self._separator, self)
                plus.setObjectName("kbdPlus")
                self._row.addWidget(plus)
            cap = QLabel(key, self)
            cap.setObjectName("kbdKey")
            cap.setAlignment(Qt.AlignCenter)
            self._row.addWidget(cap)

    # ------------------------------------------------------------------ #
    ## Designer / declarative properties
    # ------------------------------------------------------------------ #
    @Property(str)
    def keys(self):
        return self._separator.join(self._keys)

    @keys.setter
    def keys(self, value):
        self.setKeys(value if value is not None else "")

    @Property(str)
    def separator(self):
        return self._separator

    @separator.setter
    def separator(self, value):
        current = self.keys
        self._separator = value or "+"
        self.setKeys(current)
