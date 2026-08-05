"""QCustomSocialButton showcase — brand-coloured sign-in buttons.

The foreground contrast is chosen automatically from the brand colour; the
controls flip every button's variant and shape.
"""

import os
import sys

# Force PySide6 to match compiled ui files
os.environ.setdefault("QT_API", "pyside6")

from Custom_Widgets.Project import setProjectRoot
setProjectRoot(__file__)

from Custom_Widgets import *
from qtpy.QtCore import QCoreApplication, QSettings
from qtpy.QtWidgets import QApplication


class MainWindow(QCustomMainWindow):
    def __init__(self, parent=None):
        QCustomMainWindow.__init__(self)
        from src.ui_MainWindow import Ui_MainWindow
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Set the app identity BEFORE loadJsonStyle: the theme loader consults
        # QSettings while parsing CustomThemes, and without these names it
        # reads the shared unnamed settings file (polluted by other example
        # apps), which silently cancels this app's Default-Theme flag.
        QCoreApplication.setOrganizationName("CustomWidgets")
        QCoreApplication.setApplicationName("QCustomSocialButton Showcase")

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

        self._wire()

    def _wire(self):
        self.buttons = [
            self.ui.btnGithub, self.ui.btnGoogle, self.ui.btnX,
            self.ui.btnFacebook, self.ui.btnLinkedin, self.ui.btnDiscord,
            self.ui.btnSlack, self.ui.btnApple, self.ui.btnWhatsapp,
        ]
        for widget in self.buttons:
            widget.clicked.connect(
                lambda b=widget.brand: self.ui.statusLabel.setText(
                    "clicked %s" % b))
        self.ui.variantCombo.currentTextChanged.connect(self._setVariant)
        self.ui.shapeCombo.currentTextChanged.connect(self._setShape)
        self.ui.themeBtn.clicked.connect(self._toggleTheme)

    def _setVariant(self, value):
        for widget in self.buttons:
            widget.variant = value

    def _setShape(self, value):
        for widget in self.buttons:
            widget.shape = value

    def _toggleTheme(self):
        self.themeEngine.toggleTheme(dark="Social Night", light="Social Day")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
