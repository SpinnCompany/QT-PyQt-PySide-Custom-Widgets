########################################################################
## SVG THEME ICONS - INTERACTIVE TEST APP
##
## Run from this folder (or anywhere - it chdirs itself):
##     python examples/svg_icons_demo/main.py
##
## What to test:
##  - Switch themes from the top bar: icons regenerate as recolored SVGs
##    (the label shows how long generation took - well under a second)
##  - Left panel: standard widgets whose indicator icons come from the
##    theme stylesheet (checkboxes, radios, combo arrows, spinbox arrows)
##  - Right panel: browse/filter every generated SVG icon of the active
##    theme and check color + sharpness (icons render vector-crisp)
##  - After the first run, open designer_test.ui in Qt Designer to verify
##    Designer displays the same SVG icons via Qss/icons/_icons.qrc
########################################################################
import os
import sys
import time

# Keep all generated files (Qss/, generated-files/) inside this example folder
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from qtpy.QtCore import Qt, QSize
from qtpy.QtGui import QIcon
from qtpy.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QGridLayout,
    QLabel, QComboBox, QPushButton, QCheckBox, QRadioButton, QSlider,
    QProgressBar, QSpinBox, QLineEdit, QTabWidget, QListWidget,
    QListWidgetItem, QGroupBox, QListView,
)

from Custom_Widgets import loadJsonStyle
from Custom_Widgets.QAppSettings import QAppSettings
from Custom_Widgets.QCustomTheme import QCustomTheme

MAX_VISIBLE_ICONS = 300


class DemoWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("SVG Theme Icons - Interactive Test")
        self.resize(1100, 700)
        self._theme_switch_started = None

        self._buildUi()

        # Same bootstrap as a real project. A QCustomQMainWindow attaches the
        # theme engine itself; a plain QMainWindow attaches it explicitly.
        self.themeEngine = QCustomTheme(self)
        loadJsonStyle(self, jsonFiles={"json-styles/style.json"})

    def start(self):
        self.show()
        # All UI population happens in _onThemeReady, driven by the
        # onThemeChangeComplete signal: the icon worker thread uses QSettings,
        # and touching QSettings from the main thread while it runs can
        # deadlock both threads on the settings lock file.
        self.themeEngine.onThemeChangeComplete.connect(self._onThemeReady)
        # Run after show; icon generation runs on a worker thread
        QAppSettings.updateAppSettings(self)

    ####################################################################
    ## UI
    ####################################################################
    def _buildUi(self):
        central = QWidget()
        root = QVBoxLayout(central)

        # --- top bar: theme switching + timing ---
        bar = QHBoxLayout()
        bar.addWidget(QLabel("Theme:"))
        self.themeSelector = QComboBox()
        self.themeSelector.activated.connect(self._switchTheme)
        bar.addWidget(self.themeSelector)
        self.timingLabel = QLabel("Icons ready.")
        bar.addWidget(self.timingLabel)
        bar.addStretch()
        root.addLayout(bar)

        body = QHBoxLayout()
        root.addLayout(body)

        # --- left: widgets styled by the theme stylesheet ---
        panel = QGroupBox("Widgets styled with themed SVG icons (QSS)")
        grid = QGridLayout(panel)

        cb1 = QCheckBox("Checked")
        cb1.setChecked(True)
        cb2 = QCheckBox("Unchecked")
        cb3 = QCheckBox("Tristate")
        cb3.setTristate(True)
        cb3.setCheckState(Qt.PartiallyChecked)
        grid.addWidget(cb1, 0, 0)
        grid.addWidget(cb2, 0, 1)
        grid.addWidget(cb3, 0, 2)

        rb1 = QRadioButton("Option A")
        rb1.setChecked(True)
        rb2 = QRadioButton("Option B")
        grid.addWidget(rb1, 1, 0)
        grid.addWidget(rb2, 1, 1)

        combo = QComboBox()
        combo.addItems(["Combo arrow icon", "Item 2", "Item 3"])
        grid.addWidget(combo, 2, 0, 1, 2)
        grid.addWidget(QSpinBox(), 2, 2)

        slider = QSlider(Qt.Horizontal)
        progress = QProgressBar()
        slider.valueChanged.connect(progress.setValue)
        slider.setValue(60)
        grid.addWidget(slider, 3, 0, 1, 3)
        grid.addWidget(progress, 4, 0, 1, 3)

        grid.addWidget(QLineEdit("QLineEdit"), 5, 0, 1, 3)

        # buttons with QIcons taken from the generated theme set
        self.iconButtons = []
        btn_row = QHBoxLayout()
        for name in ("save", "settings", "trash-2", "download"):
            btn = QPushButton(name)
            btn.setIconSize(QSize(20, 20))
            self.iconButtons.append((btn, f"feather/{name}.svg"))
            btn_row.addWidget(btn)
        grid.addLayout(btn_row, 6, 0, 1, 3)

        tabs = QTabWidget()
        self.tabWidget = tabs
        for label in ("Tab one", "Tab two"):
            tabs.addTab(QWidget(), label)
        grid.addWidget(tabs, 7, 0, 1, 3)

        body.addWidget(panel, 1)

        # --- right: icon browser ---
        browser = QGroupBox("Generated SVG icons of the active theme")
        vbox = QVBoxLayout(browser)

        controls = QHBoxLayout()
        self.packSelector = QComboBox()
        controls.addWidget(self.packSelector)
        self.filterEdit = QLineEdit()
        self.filterEdit.setPlaceholderText("Filter icons...")
        controls.addWidget(self.filterEdit)
        vbox.addLayout(controls)

        self.iconList = QListWidget()
        self.iconList.setViewMode(QListView.IconMode)
        self.iconList.setIconSize(QSize(28, 28))
        self.iconList.setResizeMode(QListView.Adjust)
        self.iconList.setUniformItemSizes(True)
        vbox.addWidget(self.iconList)

        self.iconCountLabel = QLabel("")
        vbox.addWidget(self.iconCountLabel)

        body.addWidget(browser, 1)

        self.packSelector.activated.connect(lambda *_: self._populateIconList())
        self.filterEdit.textChanged.connect(lambda *_: self._populateIconList())

        self.setCentralWidget(central)

    ####################################################################
    ## THEME SWITCHING
    ####################################################################
    def _populateThemeSelector(self):
        self.themeSelector.clear()
        current = self.themeEngine.theme
        for theme in self.themeEngine.themes:
            self.themeSelector.addItem(theme.name)
            if theme.name == current:
                self.themeSelector.setCurrentIndex(self.themeSelector.count() - 1)

    def _switchTheme(self, index):
        name = self.themeSelector.itemText(index)
        self.timingLabel.setText(f"Generating icons for '{name}' ...")
        self._theme_switch_started = time.monotonic()
        self.themeEngine.setTheme(name)

    def _onThemeReady(self):
        if self._theme_switch_started is not None:
            elapsed = (time.monotonic() - self._theme_switch_started) * 1000
            self.timingLabel.setText(f"Icons ready in {elapsed:.0f} ms (SVG pipeline)")
            self._theme_switch_started = None
        self._populateThemeSelector()
        self._refreshPackSelector()
        self._refreshWidgetIcons()
        self._populateIconList()

    def _activeIconsDir(self):
        info = self.themeEngine.getCurrentThemeInfo()
        color = info.get("icons-color") or ""
        return os.path.join(os.getcwd(), "Qss", "icons", color.replace("#", ""))

    def _refreshWidgetIcons(self):
        icons_dir = self._activeIconsDir()
        for btn, rel in self.iconButtons:
            path = os.path.join(icons_dir, rel)
            if os.path.exists(path):
                btn.setIcon(QIcon(path))
        for i, name in enumerate(("home.svg", "star.svg")):
            path = os.path.join(icons_dir, "feather", name)
            if i < self.tabWidget.count() and os.path.exists(path):
                self.tabWidget.setTabIcon(i, QIcon(path))

    ####################################################################
    ## ICON BROWSER
    ####################################################################
    def _refreshPackSelector(self):
        icons_dir = self._activeIconsDir()
        packs = []
        for root, dirs, files in os.walk(icons_dir):
            if any(f.endswith(".svg") for f in files):
                packs.append(os.path.relpath(root, icons_dir))
        selected = self.packSelector.currentText()
        self.packSelector.blockSignals(True)
        self.packSelector.clear()
        self.packSelector.addItems(sorted(packs))
        if selected in packs:
            self.packSelector.setCurrentText(selected)
        self.packSelector.blockSignals(False)

    def _populateIconList(self):
        self.iconList.clear()
        pack_dir = os.path.join(self._activeIconsDir(), self.packSelector.currentText())
        if not os.path.isdir(pack_dir):
            self.iconCountLabel.setText("Icons not generated yet ...")
            return

        needle = self.filterEdit.text().lower()
        names = sorted(f for f in os.listdir(pack_dir)
                       if f.endswith(".svg") and needle in f.lower())

        for name in names[:MAX_VISIBLE_ICONS]:
            item = QListWidgetItem(QIcon(os.path.join(pack_dir, name)), name.replace(".svg", ""))
            item.setToolTip(name)
            self.iconList.addItem(item)

        shown = min(len(names), MAX_VISIBLE_ICONS)
        suffix = f" (showing first {MAX_VISIBLE_ICONS})" if len(names) > shown else ""
        self.iconCountLabel.setText(f"{len(names)} icons match{suffix}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DemoWindow()
    window.start()
    sys.exit(app.exec())
