########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/@SpinnTV
# WEBSITE: customwidgets.org
########################################################################

########################################################################
## QCustomColorPicker - a colour selector.
##
## A colour swatch + hex field. Clicking the swatch opens a popup of preset
## swatches with a "Custom..." button (QColorDialog). Emits colorChanged.
########################################################################
from qtpy.QtCore import Qt, Signal, QPoint
from qtpy.QtGui import QColor
from qtpy.QtWidgets import (QWidget, QHBoxLayout, QGridLayout, QVBoxLayout,
                            QPushButton, QLineEdit, QFrame, QColorDialog)


_PRESETS = [
    "#ef4444", "#f97316", "#f59e0b", "#eab308", "#84cc16", "#22c55e",
    "#10b981", "#14b8a6", "#06b6d4", "#3b82f6", "#6366f1", "#8b5cf6",
    "#a855f7", "#d946ef", "#ec4899", "#f43f5e", "#64748b", "#0f172a",
    "#94a3b8", "#ffffff",
]


class QCustomColorPicker(QWidget):
    colorChanged = Signal(QColor)

    WIDGET_ICON = "components/icons/colorpicker.png"
    WIDGET_TOOLTIP = "A colour selector with presets and a custom dialog"
    WIDGET_MODULE = "Custom_Widgets.QCustomColorPicker"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomColorPicker' name='customColorPicker'>
            <property name='geometry'><rect><x>0</x><y>0</y><width>160</width><height>32</height></rect></property>
        </widget>
    </ui>
    """
    __catalog__ = {
        "name": "QCustomColorPicker",
        "props": {},
        "signals": ["colorChanged"],
        "tokens_used": ["surface", "on-surface", "surface-muted", "outline", "accent"],
    }

    def __init__(self, parent=None, color="#3b82f6"):
        super().__init__(parent)
        self.setObjectName("QCustomColorPicker")
        self._color = QColor(color)

        row = QHBoxLayout(self)
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(6)

        self._swatch = QPushButton(self)
        self._swatch.setObjectName("colorSwatch")
        self._swatch.setFixedSize(28, 28)
        self._swatch.setCursor(Qt.PointingHandCursor)
        self._swatch.clicked.connect(self._openPopup)
        row.addWidget(self._swatch)

        self._hex = QLineEdit(self)
        self._hex.setObjectName("colorHex")
        self._hex.setMaxLength(7)
        self._hex.editingFinished.connect(self._onHexEdited)
        row.addWidget(self._hex, 1)

        self._popup = QFrame(self, Qt.Popup)
        self._popup.setObjectName("colorPopup")
        grid = QGridLayout(self._popup)
        grid.setContentsMargins(8, 8, 8, 8)
        grid.setSpacing(4)
        for i, hexc in enumerate(_PRESETS):
            b = QPushButton(self._popup)
            b.setObjectName("colorPreset")
            b.setFixedSize(22, 22)
            b.setCursor(Qt.PointingHandCursor)
            b.setStyleSheet("background-color: %s; border: 1px solid rgba(0,0,0,40);"
                            " border-radius: 4px;" % hexc)
            b.clicked.connect(lambda _c=False, h=hexc: self._pick(QColor(h)))
            grid.addWidget(b, i // 5, i % 5)
        custom = QPushButton("Custom...", self._popup)
        custom.setObjectName("colorCustomBtn")
        custom.clicked.connect(self._openDialog)
        grid.addWidget(custom, (len(_PRESETS) + 4) // 5, 0, 1, 5)

        self._refresh()

    # ------------------------------------------------------------------ #
    ## Selection
    # ------------------------------------------------------------------ #
    def _openPopup(self):
        below = self.mapToGlobal(QPoint(0, self.height()))
        self._popup.move(below)
        self._popup.show()

    def _openDialog(self):
        self._popup.hide()
        col = QColorDialog.getColor(self._color, self, "Select colour")
        if col.isValid():
            self._pick(col)

    def _pick(self, color):
        self._popup.hide()
        self.setColor(color)

    def _onHexEdited(self):
        col = QColor(self._hex.text().strip())
        if col.isValid():
            self.setColor(col)
        else:
            self._hex.setText(self._color.name())      # revert invalid input

    def _refresh(self):
        self._hex.setText(self._color.name())
        self._swatch.setStyleSheet(
            "#colorSwatch { background-color: %s; border: 1px solid rgba(0,0,0,60);"
            " border-radius: 6px; }" % self._color.name())

    # ------------------------------------------------------------------ #
    ## API
    # ------------------------------------------------------------------ #
    def color(self):
        return QColor(self._color)

    def colorName(self):
        return self._color.name()

    def setColor(self, color):
        col = QColor(color)
        if not col.isValid() or col == self._color:
            if col.isValid():
                self._refresh()
            return
        self._color = col
        self._refresh()
        self.colorChanged.emit(QColor(col))
