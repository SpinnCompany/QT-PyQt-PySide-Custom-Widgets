"""QCustomTypewriterText demo — a rotating headline that types, holds, erases and moves on."""

import os, sys

# Force PySide6 to match compiled ui files
os.environ.setdefault("QT_API", "pyside6")

from Custom_Widgets.Project import setProjectRoot
setProjectRoot(__file__)

from Custom_Widgets import *
from qtpy.QtCore import QCoreApplication, QSettings
from qtpy.QtWidgets import QApplication

PHRASES = ["Build faster.", "Ship sooner.", "Sleep better."]


class MainWindow(QCustomMainWindow):
    def __init__(self, parent=None):
        QCustomMainWindow.__init__(self)
        # Set BEFORE loadJsonStyle: the theme engine reads QSettings() while
        # parsing the json — without these names it reads the interpreter-wide
        # settings file and the app's own THEME/default theme never resolve.
        QCoreApplication.setOrganizationName("CustomWidgets")
        QCoreApplication.setApplicationName("QCustomTypewriterText Demo")

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
        # Demo data: the rotating phrases.
        ui.typewriterText.setPhrases(PHRASES)
        ui.typewriterText.phraseFinished.connect(
            lambda phrase: ui.statusLabel.setText("finished: %s" % phrase))

        ui.speedSlider.valueChanged.connect(
            lambda v: setattr(ui.typewriterText, "typeSpeed", v))
        ui.startButton.clicked.connect(lambda: ui.typewriterText.start())
        ui.stopButton.clicked.connect(lambda: ui.typewriterText.stop())
        ui.skipButton.clicked.connect(lambda: ui.typewriterText.skip())
        ui.caretButton.clicked.connect(self._toggleCaret)
        ui.themeButton.clicked.connect(self._toggleTheme)

    def _toggleCaret(self):
        typer = self.ui.typewriterText
        typer.showCaret = not typer.showCaret

    def _toggleTheme(self):
        current = str(getattr(self.themeEngine, "theme", "") or "")
        target = "Typewriter-Day" if current == "Typewriter-Night" else "Typewriter-Night"
        self.themeEngine.setTheme(target)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
