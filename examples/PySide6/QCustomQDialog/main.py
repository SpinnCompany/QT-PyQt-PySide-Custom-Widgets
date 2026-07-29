"""QCustomQDialog showcase — professional dialog/modal patterns."""

import os, sys

os.environ.setdefault("QT_API", "pyside6")

from Custom_Widgets.Project import setProjectRoot
setProjectRoot(__file__)

from Custom_Widgets import *
from Custom_Widgets.QCustomQDialog import QCustomQDialog
from Custom_Widgets.QAppSettings import QAppSettings
from qtpy.QtCore import QCoreApplication, QSettings
from qtpy.QtWidgets import QApplication


class MainWindow(QCustomMainWindow):
    def __init__(self, parent=None):
        QCustomMainWindow.__init__(self)
        self._build()

    def _build(self):
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
        # applyCompiledSass starts a background icon thread that can deadlock
        # when the main thread is in the constructor + QSettings path; skip the
        # thread and compile synchronously instead.
        generateIcons = False
        paintEntireApp = True
        themeEngine.applyCompiledSass(
            generateIcons=generateIcons, paintEntireApp=paintEntireApp)

        from Custom_Widgets.AppControl import maybe_start_app_control
        try:
            maybe_start_app_control()
        except Exception:
            pass

        self._wire_buttons()

    def _show_dialog(self, title, description, show_cancel=True):
        dialog = QCustomQDialog(
            parent=self,
            title=title,
            description=description,
            yesButtonText="Confirm",
            cancelButtonText="Cancel",
            showYesButton=True,
            showCancelButton=show_cancel,
            setModal=False,
            frameless=True,
            windowMovable=True,
            animationDuration=400,
            position="center",
        )
        dialog.accepted.connect(
            lambda: self.ui.statusLabel.setText(f"Accepted: {title}")
        )
        dialog.rejected.connect(
            lambda: self.ui.statusLabel.setText(f"Cancelled: {title}")
        )
        dialog.show()
        return dialog

    def _wire_buttons(self):
        self.ui.infoBtn.clicked.connect(
            lambda: self._show_dialog("Information", "Informational message. No action required.", show_cancel=False)
        )
        self.ui.confirmBtn.clicked.connect(
            lambda: self._show_dialog("Confirm Action", "Are you sure? This cannot be undone.")
        )
        self.ui.warningBtn.clicked.connect(
            lambda: self._show_dialog("Warning", "This may have unintended consequences.")
        )
        self.ui.errorBtn.clicked.connect(
            lambda: self._show_dialog("Error", "Something went wrong. Please try again.")
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
