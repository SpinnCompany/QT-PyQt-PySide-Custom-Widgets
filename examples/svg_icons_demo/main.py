########################################################################
## SVG THEME ICONS - INTERACTIVE TEST APP (real project layout)
##
## ui/          - .ui files designed in Qt Designer (icons from _icons.qrc)
## src/         - generated Python (ui_*.py), created by the converter
## json-styles/ - style.json (themes, icon color)
##
## One-time convert (or after pulling changes):
##     Custom_Widgets --convert-ui ui --src-output-dir src
##
## Live development - regenerate on every Designer save:
##     Custom_Widgets --monitor-ui ui --src-output-dir src
##
## Run:
##     python main.py
########################################################################
import os
import sys
import time

# Keep all generated files (Qss/, generated-files/) inside this example folder
DEMO_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(DEMO_DIR)
sys.path.insert(0, DEMO_DIR)

from qtpy.QtCore import QSize
from qtpy.QtGui import QIcon
from qtpy.QtWidgets import QApplication, QMainWindow, QListWidgetItem

from Custom_Widgets import loadJsonStyle
from Custom_Widgets.QAppSettings import QAppSettings
from Custom_Widgets.QCustomTheme import QCustomTheme

try:
    from src.ui_mainwindow import Ui_MainWindow
except ImportError:
    sys.exit("Generated UI not found. Run first:\n"
             "    Custom_Widgets --convert-ui ui --src-output-dir src")

MAX_VISIBLE_ICONS = 300


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self._theme_switch_started = None

        self.ui.sampleSlider.valueChanged.connect(self.ui.sampleProgress.setValue)
        self.ui.themeSelector.activated.connect(self._switchTheme)
        self.ui.packSelector.activated.connect(lambda *_: self._populateIconList())
        self.ui.filterEdit.textChanged.connect(lambda *_: self._populateIconList())
        for btn in (self.ui.saveBtn, self.ui.settingsBtn, self.ui.deleteBtn, self.ui.materialBtn):
            btn.setIconSize(QSize(20, 20))

        # A QCustomQMainWindow attaches the theme engine itself; a plain
        # QMainWindow attaches it explicitly.
        self.themeEngine = QCustomTheme(self)
        loadJsonStyle(self, jsonFiles={"json-styles/style.json"})

    def start(self):
        self.show()
        # All UI population happens in _onThemeReady, driven by the
        # onThemeChangeComplete signal (icon generation runs on a worker).
        self.themeEngine.onThemeChangeComplete.connect(self._onThemeReady)
        QAppSettings.updateAppSettings(self)

    ####################################################################
    ## THEME SWITCHING
    ####################################################################
    def _populateThemeSelector(self):
        selector = self.ui.themeSelector
        selector.clear()
        current = self.themeEngine.theme
        for theme in self.themeEngine.themes:
            selector.addItem(theme.name)
            if theme.name == current:
                selector.setCurrentIndex(selector.count() - 1)

    def _switchTheme(self, index):
        name = self.ui.themeSelector.itemText(index)
        self.ui.timingLabel.setText(f"Generating icons for '{name}' ...")
        self._theme_switch_started = time.monotonic()
        self.themeEngine.setTheme(name)

    def _onThemeReady(self):
        if self._theme_switch_started is not None:
            elapsed = (time.monotonic() - self._theme_switch_started) * 1000
            self.ui.timingLabel.setText(f"Icons ready in {elapsed:.0f} ms (SVG pipeline)")
            self._theme_switch_started = None
        # Re-point the .ui icons (from generated-files/json) at the shared set
        self.themeEngine.applyIcons(self.ui, ui_file_name="mainwindow")
        self._populateThemeSelector()
        self._refreshPackSelector()
        self._populateIconList()

    def _activeIconsDir(self):
        # Single shared icon set - recolored in place on theme/color change
        return os.path.join(os.getcwd(), "Qss", "icons", "icons")

    ####################################################################
    ## ICON BROWSER
    ####################################################################
    def _refreshPackSelector(self):
        icons_dir = self._activeIconsDir()
        packs = []
        for root, dirs, files in os.walk(icons_dir):
            if any(f.endswith(".svg") for f in files):
                packs.append(os.path.relpath(root, icons_dir))
        selector = self.ui.packSelector
        selected = selector.currentText()
        selector.blockSignals(True)
        selector.clear()
        selector.addItems(sorted(packs))
        if selected in packs:
            selector.setCurrentText(selected)
        selector.blockSignals(False)

    def _populateIconList(self):
        icon_list = self.ui.iconList
        icon_list.clear()
        pack_dir = os.path.join(self._activeIconsDir(), self.ui.packSelector.currentText())
        if not os.path.isdir(pack_dir):
            self.ui.iconCountLabel.setText("Icons not generated yet ...")
            return

        needle = self.ui.filterEdit.text().lower()
        names = sorted(f for f in os.listdir(pack_dir)
                       if f.endswith(".svg") and needle in f.lower())

        for name in names[:MAX_VISIBLE_ICONS]:
            item = QListWidgetItem(QIcon(os.path.join(pack_dir, name)), name.replace(".svg", ""))
            item.setToolTip(name)
            icon_list.addItem(item)

        shown = min(len(names), MAX_VISIBLE_ICONS)
        suffix = f" (showing first {MAX_VISIBLE_ICONS})" if len(names) > shown else ""
        self.ui.iconCountLabel.setText(f"{len(names)} icons match{suffix}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.start()
    sys.exit(app.exec())
