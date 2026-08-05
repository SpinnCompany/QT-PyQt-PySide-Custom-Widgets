"""QCustomImagePicker showcase — an avatar-and-cover form: a circular avatar
picker, a wide cover picker in cover mode, and the same image in contain mode
so the difference is visible. Drag an image file onto any of them, or click to
browse. The status line shows the rejection reason when a file is refused."""

import os, sys

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

        # Name the app BEFORE loadJsonStyle: theme parsing checks QSettings for
        # an existing THEME, and without these names QSettings resolves to the
        # shared "Unknown Organization/main.py.conf" — whose stale THEME would
        # cancel this app's Default-Theme flag on every first run.
        QCoreApplication.setOrganizationName("CustomWidgets")
        QCoreApplication.setApplicationName("QCustomImagePicker Example")

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

        self._wireControls()

    def _wireControls(self):
        ui = self.ui
        # Mirror whatever the cover picker accepts into the contain one, so the
        # two fit modes can be compared on the same file.
        ui.coverPicker.imageSelected.connect(ui.containPicker.setImagePath)
        ui.coverPicker.imageCleared.connect(ui.containPicker.clearImage)

        status = ui.statusLabel
        for picker, name in ((ui.avatarPicker, "avatar"),
                             (ui.coverPicker, "cover")):
            picker.imageSelected.connect(
                lambda path, n=name: status.setText("%s: %s" % (n, path)))
            picker.selectionRejected.connect(
                lambda why, n=name: status.setText("%s rejected — %s" % (n, why)))
            picker.imageCleared.connect(
                lambda n=name: status.setText("%s cleared" % n))

        ui.browseButton.clicked.connect(ui.avatarPicker.browse)
        ui.clearButton.clicked.connect(self._clearAll)
        ui.themeButton.clicked.connect(
            lambda: self.themeEngine.toggleTheme(dark="DarkroomTeal",
                                                 light="SeafoamLight"))

    def _clearAll(self):
        for picker in (self.ui.avatarPicker, self.ui.coverPicker,
                       self.ui.containPicker):
            picker.clearImage()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
