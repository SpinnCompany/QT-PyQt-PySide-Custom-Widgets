"""QCustomFlowLayout showcase.

Ten buttons flowing and re-wrapping with the window width. The layout itself
is the custom widget being demonstrated, so it is created in code (Qt Designer
cannot author custom layouts); everything else lives in the .ui + scss.
"""

import os
import sys

# Force PySide6 to match compiled ui files
os.environ.setdefault("QT_API", "pyside6")

from Custom_Widgets.Project import setProjectRoot
setProjectRoot(__file__)

from Custom_Widgets import *
from Custom_Widgets.QCustomFlowLayout import QCustomFlowLayout
from qtpy.QtCore import QCoreApplication, QSettings
from qtpy.QtWidgets import QApplication, QPushButton


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

        self._seedButtons()

    def _seedButtons(self):
        """The demo content: ten buttons in a QCustomFlowLayout."""
        self.flowLayout = QCustomFlowLayout(parent=self.ui.flowHost,
                                            margin=10, spacing=5)
        for i in range(10):
            button = QPushButton("Button %d" % (i + 1), self.ui.flowHost)
            button.setObjectName("flowButton%d" % (i + 1))
            self.flowLayout.addWidget(button)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
