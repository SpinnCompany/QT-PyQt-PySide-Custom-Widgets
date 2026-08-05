"""QCustomEmbeddedWindow example.

Click "Add embedded window" to drop a movable, closable, collapsible child
window into the scroll area (one is added at startup so the demo is visible
immediately). Chrome comes from Qss/scss + json-styles."""

import os, sys

# Force PySide6 to match compiled ui files
os.environ.setdefault("QT_API", "pyside6")

from Custom_Widgets.Project import setProjectRoot
setProjectRoot(__file__)

from Custom_Widgets import *
from Custom_Widgets.QCustomEmbeddedWindow import QCustomEmbeddedWindow
from qtpy.QtCore import QCoreApplication, QSettings
from qtpy.QtGui import QIcon
from qtpy.QtWidgets import QApplication, QLabel, QStyle


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
            for t in themeEngine.themes:
                if getattr(t, "defaultTheme", False) and (init_set is None or not init_set):
                    s.setValue("THEME", t.name)
                    s.setValue("INIT-THEME-SET", True)
        if s.value("THEME") is None:
            # A stray QSettings file (written before QApplication got its real
            # names) strips every theme's default flag — seed explicitly.
            s.setValue("THEME", "Obsidian")
            s.setValue("INIT-THEME-SET", True)
        s.setValue("THEMES-LIST", themeEngine.themes)
        themeEngine.reloadJsonStyles(update=False)
        themeEngine.applyCompiledSass(generateIcons=False, paintEntireApp=True)

        from Custom_Widgets.AppControl import maybe_start_app_control
        try:
            maybe_start_app_control()
        except Exception:
            pass

        self.ui.addWindowBtn.clicked.connect(self.addEmbeddedWindow)
        # Show one embedded window immediately so the demo is visible.
        self.addEmbeddedWindow()

    def addEmbeddedWindow(self):
        label = QLabel("My parent is the top-level widget so I can move anywhere")
        label.setWordWrap(True)
        self.embeddedWindow = QCustomEmbeddedWindow(
            self.ui.scrollAreaWidgetContents,
            icon=QIcon(self.style().standardIcon(QStyle.SP_TitleBarMenuButton)))
        self.embeddedWindow.addWidget(label)
        self.embeddedWindow.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
