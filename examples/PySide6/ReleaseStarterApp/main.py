"""Release starter app — the minimal template to copy when starting a project.

Structure and chrome live in ui/MainWindow.ui + Qss/scss (compiled to
src/ui_MainWindow.py); themes live in json-styles/style.json; only form
fields (data) and signal wiring live here.
"""

import os, sys

# Force PySide6 to match compiled ui files
os.environ.setdefault("QT_API", "pyside6")

from Custom_Widgets.Project import setProjectRoot
setProjectRoot(__file__)

from Custom_Widgets import *
from Custom_Widgets.QCustomButtonGroup import QCustomButtonGroup
from Custom_Widgets.QCustomComboBox import QCustomComboBox
from Custom_Widgets.QCustomForm import QCustomFormField
from Custom_Widgets.QCustomInput import QCustomInput
from Custom_Widgets.QCustomToast import QCustomToast
from qtpy.QtCore import QCoreApplication, QSettings
from qtpy.QtWidgets import QApplication


class MainWindow(QCustomMainWindow):
    def __init__(self, parent=None):
        QCustomMainWindow.__init__(self)
        # Set BEFORE loadJsonStyle: the theme engine reads QSettings() while
        # parsing the json — without these names it reads the interpreter-wide
        # settings file and the app's own THEME/default theme never resolve.
        QCoreApplication.setOrganizationName("CustomWidgets")
        QCoreApplication.setApplicationName("ReleaseStarterApp")

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

        self._buildForm()
        self._wireDemo()

    def _buildForm(self):
        """Form fields are data-driven, so they are added here in code."""
        form = self.ui.signupForm

        nameInput = QCustomInput(self)
        nameInput.setPlaceholderText("Enter your name")
        nameInput.variant = "outline"
        nameInput.sizeVariant = "md"
        nameField = QCustomFormField("Name", widget=nameInput)
        nameField.set_required(True)
        form.add_field(nameField)

        emailInput = QCustomInput(self)
        emailInput.setPlaceholderText("Enter your email")
        emailInput.variant = "outline"
        emailField = QCustomFormField("Email", widget=emailInput)
        emailField.set_validator(lambda value: "@" in value)
        form.add_field(emailField)

        region = QCustomComboBox(self, editable=True)
        region.setPlaceholderText("Choose a region")
        region.setItems(["North America", "Europe", "Asia Pacific", "Latin America"])
        region.setCurrentIndex(0)
        regionField = QCustomFormField("Region", widget=region)
        form.add_field(regionField)

        # QCustomButtonGroup's layout direction is fixed at construction time
        # (the orientation property does not rebuild the layout), so the
        # horizontal group is created here and dropped into the .ui holder.
        self.prefsGroup = QCustomButtonGroup(self, exclusive=True,
                                             orientation="horizontal")
        self.prefsGroup.setButtons(["Light Mode", "Dark Mode", "Auto"])
        self.prefsGroup.setSelectedId(2)
        self.ui.prefsHolder.addWidget(self.prefsGroup)

    def _wireDemo(self):
        self.ui.signupForm.submitted.connect(self._handleSubmit)
        self.ui.submitButton.clicked.connect(
            lambda: QCustomToast.success(self, "Starter app ready", title="Success"))

    def _handleSubmit(self, payload):
        QCustomToast.success(self, f"Submitted {payload['Name']}", title="Form")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
