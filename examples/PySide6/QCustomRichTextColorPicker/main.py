########################################################################
## QCustomRichTextEditor + QCustomColorPicker example
##
## A rich-text editor and a colour picker whose choice tints a preview
## swatch. Themed through the Custom_Widgets pipeline (ui/ + Qss scss +
## json-styles); the preview colour is data-driven, set through the
## swatch widget's typed colour property.
## Run:
##     python main.py
########################################################################
import os, sys

# Force PySide6 to match compiled ui files
os.environ.setdefault("QT_API", "pyside6")

from Custom_Widgets.Project import setProjectRoot
setProjectRoot(__file__)

from Custom_Widgets import *
from qtpy.QtCore import QCoreApplication, QSettings
from qtpy.QtGui import QColor
from qtpy.QtWidgets import QApplication


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
            # Default-Theme is ignored by the json parser when ANY QSettings
            # file already holds a THEME, so pin this app's default explicitly.
            if not s.value("INIT-THEME-SET"):
                s.setValue("THEME", "RichText-Dark")
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
        # Data seeding: the document content and the starting accent colour.
        ui.editor.setHtml("<h2>Release notes</h2>"
                          "<p>Type here. Use the toolbar for <b>bold</b>, "
                          "<i>italics</i>, headings and lists.</p>")
        ui.picker.colorChanged.connect(self._tint)
        # Seed the picker with the active theme's accent (the tokenised green).
        ui.picker.setColor(QColor(str(self.themeEngine.COLOR_ACCENT_1)))
        self._tint(ui.picker.color())

    def _tint(self, color):
        # Data-driven colour on a custom widget: typed Qt property, not QSS.
        self.ui.preview.setProperty("bgColor", QColor(color))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
