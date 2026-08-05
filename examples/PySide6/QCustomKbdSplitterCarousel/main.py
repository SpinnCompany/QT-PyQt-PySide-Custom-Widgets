"""QCustomKbd + QCustomSplitter + QCustomCarousel showcase — keyboard-shortcut
keycaps, a tokenized splitter, and a slideshow carousel with auto-advance."""

import os, sys

# Force PySide6 to match compiled ui files
os.environ.setdefault("QT_API", "pyside6")

from Custom_Widgets.Project import setProjectRoot
setProjectRoot(__file__)

from Custom_Widgets import *
from qtpy.QtCore import QCoreApplication, QSettings, Qt
from qtpy.QtWidgets import QApplication, QFrame, QLabel, QVBoxLayout


def _slideCard(title, body):
    """A carousel slide: same card structure as the splitter panels; all
    styling comes from defaultStyle.scss via the objectNames."""
    frame = QFrame()
    frame.setObjectName("slideCard")
    lay = QVBoxLayout(frame)
    lay.setContentsMargins(16, 16, 16, 16)
    t = QLabel(title)
    t.setObjectName("slideTitle")
    b = QLabel(body)
    b.setObjectName("slideBody")
    b.setWordWrap(True)
    b.setAlignment(Qt.AlignTop)
    lay.addWidget(t)
    lay.addWidget(b, 1)
    return frame


class MainWindow(QCustomMainWindow):
    def __init__(self, parent=None):
        QCustomMainWindow.__init__(self)
        from src.ui_MainWindow import Ui_MainWindow
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Name the app BEFORE loadJsonStyle: theme parsing checks QSettings for
        # an existing THEME, and without these names QSettings resolves to the
        # shared "Unknown Organization/main.py.conf" — whose stale THEME would
        # cancel this app's Default-Theme flag on every first run.
        QCoreApplication.setOrganizationName("CustomWidgets")
        QCoreApplication.setApplicationName("QCustomKbdSplitterCarousel Example")

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

        self._seedDemo()

    def _seedDemo(self):
        # splitter proportions
        self.ui.splitter.setSizes([160, 320, 220])

        # carousel slides + auto-advance
        carousel = self.ui.carousel
        for title, body in (
                ("Welcome", "QCustomCarousel shows one slide at a time."),
                ("Navigate", "Use the arrows or click a dot below."),
                ("Automate", "setAutoAdvance(ms) cycles the slides for you.")):
            carousel.addSlide(_slideCard(title, body))
        carousel.setAutoAdvance(2500)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
