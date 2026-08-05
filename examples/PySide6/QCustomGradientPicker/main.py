"""QCustomGradientPicker showcase.

An editor plus a live preview: click the bar to add a stop, drag a handle to
move it, double-click a handle (or press Return) to recolour it, Delete to
remove it. The preview panel paints the same gradient at full size so the
angle and type controls have something to act on. Full project structure:
ui/ + compiled src/ + json-styles themes + Qss scss tokens (zero inline
styling).
"""

import os
import sys

# Force PySide6 to match compiled ui files
os.environ.setdefault("QT_API", "pyside6")

from Custom_Widgets.Project import setProjectRoot
setProjectRoot(__file__)

from Custom_Widgets import *
from qtpy.QtCore import QCoreApplication, QRectF, QSettings
from qtpy.QtGui import QBrush, QPainter, QPen
from qtpy.QtWidgets import QApplication, QFrame

THEME_DARK = "Picker Dark"
THEME_LIGHT = "Picker Light"

SEED_STOPS = "0:#2563eb,0.5:#a855f7,1:#16a34a"


class Preview(QFrame):
    """Paints whatever gradient the picker currently describes.

    Demo-local painting helper: its frame colour comes from the picker's
    themed borderColor property, so it follows the active theme.
    """

    def __init__(self, picker, parent=None):
        super().__init__(parent)
        self._picker = picker

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = QRectF(self.rect()).adjusted(1, 1, -1, -1)
        painter.setBrush(QBrush(self._picker.gradient(rect)))
        painter.setPen(QPen(self._picker.borderColor))
        painter.drawRoundedRect(rect, 10, 10)


class MainWindow(QCustomMainWindow):
    def __init__(self, parent=None):
        QCustomMainWindow.__init__(self)
        from src.ui_MainWindow import Ui_MainWindow
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        loadJsonStyle(self, self.ui, jsonFiles={"json-styles/style.json"})

        self.show()
        themeEngine = self.themeEngine
        org = getattr(themeEngine, "organizationName", "")
        if org:
            QCoreApplication.setOrganizationName(str(org))
        appn = getattr(themeEngine, "applicationName", "")
        if appn:
            QCoreApplication.setApplicationName(str(appn))
        orgd = getattr(themeEngine, "organizationDomain", "")
        if orgd:
            QCoreApplication.setOrganizationDomain(str(orgd))
        s = QSettings()
        init_set = s.value("INIT-THEME-SET")
        if s.value("THEME") is None or not init_set:
            # Prefer the json default; a stale THEME in the pre-boot QSettings
            # scope strips Default-Theme flags, so fall back to the first
            # custom (non-predefined) theme rather than silently keeping the
            # engine's built-in Light palette.
            chosen = None
            for t in themeEngine.themes:
                if getattr(t, "defaultTheme", False):
                    chosen = t.name
                    break
            if chosen is None:
                for t in themeEngine.themes:
                    if not getattr(t, "predefined", False):
                        chosen = t.name
                        break
            if chosen is not None:
                s.setValue("THEME", chosen)
                s.setValue("INIT-THEME-SET", True)
        s.setValue("THEMES-LIST", themeEngine.themes)
        themeEngine.reloadJsonStyles(update=False)
        themeEngine.applyCompiledSass(generateIcons=False, paintEntireApp=True)

        from Custom_Widgets.AppControl import maybe_start_app_control
        try:
            maybe_start_app_control()
        except Exception:
            pass

        self._seedGradient()
        self._wire()

    def _seedGradient(self):
        """Demo data: the initial three-stop gradient + the live preview."""
        self.ui.gradientPicker.stopsCsv = SEED_STOPS
        self.preview = Preview(self.ui.gradientPicker, self.ui.previewHolder)
        self.ui.previewLayout.addWidget(self.preview)
        self.ui.statusLabel.setText(self.ui.gradientPicker.stopsCsv)

    def _wire(self):
        picker = self.ui.gradientPicker
        picker.gradientChanged.connect(self._onChanged)
        picker.stopSelected.connect(
            lambda i: self.ui.statusLabel.setText(
                "stop %d selected — %s" % (i, picker.stopColor(i).name())))
        self.ui.typeBox.currentTextChanged.connect(self._setType)
        self.ui.angleSlider.valueChanged.connect(self._setAngle)
        self.ui.editStopBtn.clicked.connect(picker.editStopColor)
        self.ui.themeBtn.clicked.connect(
            lambda: self.themeEngine.toggleTheme(dark=THEME_DARK,
                                                 light=THEME_LIGHT))
        for button, csv in (
                (self.ui.presetSunset, "0:#f59e0b,0.5:#ef4444,1:#7c3aed"),
                (self.ui.presetOcean, "0:#0ea5e9,1:#065f46"),
                (self.ui.presetFade, "0:#002563eb,1:#2563eb")):
            button.clicked.connect(lambda _=False, c=csv: self._applyPreset(c))

    def _onChanged(self, csv):
        self.ui.statusLabel.setText(csv)
        self.preview.update()

    def _setType(self, value):
        self.ui.gradientPicker.gradientType = value
        self.ui.angleSlider.setEnabled(value == "linear")
        self.preview.update()

    def _setAngle(self, value):
        self.ui.gradientPicker.angle = value
        self.preview.update()

    def _applyPreset(self, csv):
        self.ui.gradientPicker.stopsCsv = csv
        self.preview.update()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
