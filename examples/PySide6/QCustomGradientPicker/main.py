########################################################################
## QCustomGradientPicker example
##
## An editor plus a live preview: click the bar to add a stop, drag a handle to
## move it, double-click a handle (or press Return) to recolour it, Delete to
## remove it. The preview panel paints the same gradient at full size so the
## angle and type controls have something to act on.
## Run:
##     python main.py
########################################################################
import sys
from PySide6 import QtWidgets, QtGui, QtCore

from Custom_Widgets.QCustomGradientPicker import QCustomGradientPicker
from Custom_Widgets.JSonStyles.tokens import applyDesignTokens


class Preview(QtWidgets.QFrame):
    """Paints whatever gradient the picker currently describes."""

    def __init__(self, picker, parent=None):
        super().__init__(parent)
        self._picker = picker
        self.setMinimumHeight(160)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        rect = QtCore.QRectF(self.rect()).adjusted(1, 1, -1, -1)
        painter.setBrush(QtGui.QBrush(self._picker.gradient(rect)))
        painter.setPen(QtGui.QPen(QtGui.QColor("#cbd5e1")))
        painter.drawRoundedRect(rect, 10, 10)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QCustomGradientPicker")
        central = QtWidgets.QWidget()
        self.setCentralWidget(central)
        layout = QtWidgets.QVBoxLayout(central)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)
        self._theme = "light"

        layout.addWidget(self._heading("Gradient"))
        self.picker = QCustomGradientPicker(
            stops=[(0.0, "#2563eb"), (0.5, "#a855f7"), (1.0, "#16a34a")])
        layout.addWidget(self.picker)

        self.preview = Preview(self.picker)
        layout.addWidget(self.preview, 1)

        controls = QtWidgets.QHBoxLayout()

        self.typeBox = QtWidgets.QComboBox()
        self.typeBox.addItems(["linear", "radial"])
        self.typeBox.currentTextChanged.connect(self._setType)
        controls.addWidget(QtWidgets.QLabel("Type"))
        controls.addWidget(self.typeBox)

        self.angle = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.angle.setRange(0, 359)
        self.angle.valueChanged.connect(self._setAngle)
        controls.addWidget(QtWidgets.QLabel("Angle"))
        controls.addWidget(self.angle, 1)

        for text, slot in (("Edit selected stop", self.picker.editStopColor),
                           ("Light / dark", self._toggleTheme)):
            btn = QtWidgets.QPushButton(text)
            btn.clicked.connect(slot)
            controls.addWidget(btn)
        layout.addLayout(controls)

        presets = QtWidgets.QHBoxLayout()
        for name, csv in (
                ("Sunset", "0:#f59e0b,0.5:#ef4444,1:#7c3aed"),
                ("Ocean", "0:#0ea5e9,1:#065f46"),
                ("Fade", "0:#002563eb,1:#2563eb")):
            btn = QtWidgets.QPushButton(name)
            btn.clicked.connect(lambda _=False, c=csv: self._applyPreset(c))
            presets.addWidget(btn)
        presets.addStretch(1)
        layout.addLayout(presets)

        self.status = QtWidgets.QLabel(self.picker.stopsCsv)
        layout.addWidget(self.status)

        self.picker.gradientChanged.connect(self._onChanged)
        self.picker.stopSelected.connect(
            lambda i: self.status.setText("stop %d selected — %s"
                                          % (i, self.picker.stopColor(i).name())))
        self.resize(560, 480)

    @staticmethod
    def _heading(text):
        label = QtWidgets.QLabel(text)
        font = label.font()
        font.setBold(True)
        label.setFont(font)
        return label

    def _onChanged(self, csv):
        self.status.setText(csv)
        self.preview.update()

    def _setType(self, value):
        self.picker.gradientType = value
        self.angle.setEnabled(value == "linear")
        self.preview.update()

    def _setAngle(self, value):
        self.picker.angle = value
        self.preview.update()

    def _applyPreset(self, csv):
        self.picker.stopsCsv = csv
        self.preview.update()

    def _toggleTheme(self):
        self._theme = "dark" if self._theme == "light" else "light"
        applyDesignTokens(QtWidgets.QApplication.instance(), theme=self._theme)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    applyDesignTokens(app, theme="light")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
