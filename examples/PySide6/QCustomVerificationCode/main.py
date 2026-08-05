"""QCustomVerificationCode demo — confirm-your-email screen with three variants.

Try pasting "123 456" into any of them - the formatting is ignored.
"""

import os, sys

# Force PySide6 to match compiled ui files
os.environ.setdefault("QT_API", "pyside6")

from Custom_Widgets.Project import setProjectRoot
setProjectRoot(__file__)

from Custom_Widgets import *
from qtpy.QtCore import QCoreApplication, QSettings
from qtpy.QtWidgets import QApplication

EXPECTED = "123456"


class MainWindow(QCustomMainWindow):
    def __init__(self, parent=None):
        QCustomMainWindow.__init__(self)
        # Set BEFORE loadJsonStyle: the theme engine reads QSettings() while
        # parsing the json — without these names it reads the interpreter-wide
        # settings file and the app's own THEME/default theme never resolve.
        QCoreApplication.setOrganizationName("CustomWidgets")
        QCoreApplication.setApplicationName("QCustomVerificationCode Demo")

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
            for t in themeEngine.themes:
                if getattr(t, "defaultTheme", False) and (init_set is None or not init_set):
                    s.setValue("THEME", t.name)
                    s.setValue("INIT-THEME-SET", True)
        s.setValue("THEMES-LIST", themeEngine.themes)
        themeEngine.reloadJsonStyles(update=False)
        themeEngine.applyCompiledSass(generateIcons=False, paintEntireApp=True)

        from Custom_Widgets.AppControl import maybe_start_app_control
        try:
            maybe_start_app_control()
        except Exception:
            pass

        self._wireDemo()

    def _wireDemo(self):
        ui = self.ui
        ui.codeInput.completed.connect(self._onCompleted)
        ui.codeInput.codeChanged.connect(self._onChanged)
        ui.clearButton.clicked.connect(lambda: ui.codeInput.clear())
        ui.pasteButton.clicked.connect(self._pasteFormatted)
        ui.themeButton.clicked.connect(self._toggleTheme)

    def _onChanged(self, code):
        if self.ui.codeInput.state == "error" and len(code) < 6:
            self.ui.codeInput.state = "default"
        self.ui.statusLabel.setText("Entered %d/6" % len(code))

    def _onCompleted(self, code):
        if code == EXPECTED:
            self.ui.codeInput.state = "default"
            self.ui.statusLabel.setText("Code accepted")
        else:
            self.ui.codeInput.state = "error"
            self.ui.statusLabel.setText("That code is not correct")

    def _pasteFormatted(self):
        # Demonstrates that separators and spaces are stripped on the way in.
        self.ui.codeInput.setCodeText("123 456")

    def _toggleTheme(self):
        current = str(getattr(self.themeEngine, "theme", "") or "")
        target = "Verify-Day" if current == "Verify-Night" else "Verify-Night"
        self.themeEngine.setTheme(target)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
