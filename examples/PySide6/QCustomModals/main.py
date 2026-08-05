"""QCustomModals showcase — every modal type (Information / Success / Warning /
Error / Custom) in every anchor position. Click a button to pop the matching
modal; a welcome modal is shown on launch."""

import os, sys
from functools import partial

# Force PySide6 to match compiled ui files
os.environ.setdefault("QT_API", "pyside6")

from Custom_Widgets.Project import setProjectRoot
setProjectRoot(__file__)

from Custom_Widgets import *
from Custom_Widgets.QCustomModals import QCustomModals
from qtpy.QtCore import QCoreApplication, QSettings, QSize
from qtpy.QtWidgets import QApplication, QPushButton, QStyle

MODAL_TYPES = ["Information", "Success", "Warning", "Error", "Custom"]
POSITIONS = ["top-left", "top-center", "top-right", "center-left",
             "center-center", "center-right", "bottom-left", "bottom-center",
             "bottom-right"]


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
        QCoreApplication.setApplicationName("QCustomModals Example")

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

        self.createButtons()
        # A persistent welcome modal so the demo shows one immediately.
        self.showModal("Information", "top-right", duration=0)

    def createButtons(self):
        layout = self.ui.buttonsLayout
        for modalType in MODAL_TYPES:
            for position in POSITIONS:
                button = QPushButton("%s Modal (%s)" % (modalType, position))
                button.setObjectName("%s_%s_button"
                                     % (modalType.lower(),
                                        position.replace("-", "_")))
                # scss tints the button per modal type via [kind="..."]
                button.setProperty("kind", modalType.lower())
                button.clicked.connect(partial(self.showModal, modalType,
                                               position))
                layout.addWidget(button)

    def showModal(self, modalType, position, duration=3000):
        kwargs = {
            "title": "%s Title" % modalType,
            "description": "This is a %s modal in position: %s"
                           % (modalType.lower(), position),
            "position": position,
            "parent": self,
            # set to zero if you want your modal to not auto-close
            "animationDuration": duration,
        }

        if modalType == "Information":
            modal = QCustomModals.InformationModal(**kwargs)
        elif modalType == "Success":
            modal = QCustomModals.SuccessModal(**kwargs)
        elif modalType == "Warning":
            modal = QCustomModals.WarningModal(**kwargs)
        elif modalType == "Error":
            modal = QCustomModals.ErrorModal(**kwargs)
        else:
            kwargs["modalIcon"] = self.style().standardIcon(
                QStyle.SP_MessageBoxQuestion).pixmap(QSize(32, 32))
            kwargs["description"] += ("\n\nCustom modals are transparent by "
                                      "default; this one is styled from "
                                      "defaultStyle.scss.")
            modal = QCustomModals.CustomModal(**kwargs)

        modal.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
