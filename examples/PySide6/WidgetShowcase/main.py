"""Widget Showcase — the complete Custom Widgets library tour.

Four tabs demonstrate form inputs + validation, data visualization (stat
cards, progress rings, rating, badges), feedback (alerts + toasts) and
advanced containers (card, accordion), with a runtime theme switcher.
All styling lives in json-styles/style.json + Qss/scss/defaultStyle.scss;
this file only boots the app, seeds data and wires signals.
"""

import os
import sys

# Force PySide6 to match compiled ui files
os.environ.setdefault("QT_API", "pyside6")

from Custom_Widgets.Project import setProjectRoot
setProjectRoot(__file__)

from Custom_Widgets import *
from Custom_Widgets.QCustomInput import QCustomInput
from Custom_Widgets.QCustomComboBox import QCustomComboBox
from Custom_Widgets.QCustomButtonGroup import QCustomButtonGroup
from Custom_Widgets.QCustomForm import QCustomFormField
from Custom_Widgets.QCustomToast import QCustomToast
from qtpy.QtCore import QCoreApplication, QSettings
from qtpy.QtWidgets import QApplication, QLabel

THEMES = {"Night": "Showcase Night", "Day": "Showcase Day"}

TOAST_MESSAGES = {
    "info": ("Information", "This is an info message."),
    "success": ("Success", "Operation completed!"),
    "warning": ("Warning", "Please check this."),
    "error": ("Error", "Something went wrong."),
}


class MainWindow(QCustomMainWindow):
    def __init__(self, parent=None):
        QCustomMainWindow.__init__(self)
        from src.ui_MainWindow import Ui_MainWindow
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Point QSettings at THIS app BEFORE loadJsonStyle: the loader reads
        # THEME during parse, and a stale value in the shared pre-identity
        # store strips every Default-Theme flag (wrong theme wins).
        QCoreApplication.setOrganizationName("CustomWidgets")
        QCoreApplication.setApplicationName("Widget Showcase")
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
        if s.value("THEME") not in THEMES.values():
            # A stray pre-identity QSettings file strips every Default-Theme
            # flag at parse time — name this app's default explicitly.
            s.setValue("THEME", "Showcase Night")
            s.setValue("INIT-THEME-SET", True)
        s.setValue("THEMES-LIST", themeEngine.themes)
        themeEngine.reloadJsonStyles(update=False)
        themeEngine.applyCompiledSass(generateIcons=False, paintEntireApp=True)

        from Custom_Widgets.AppControl import maybe_start_app_control
        try:
            maybe_start_app_control()
        except Exception:
            pass

        self._buildThemeSwitcher()
        self._buildForm()
        self._buildPrefGroup()
        self._seedData()
        self._wireToasts()

    # ------------------------------------------------------------------ #
    ## Theme switcher (runtime theme flip — QSS only, no inline styles)
    # ------------------------------------------------------------------ #
    def _buildThemeSwitcher(self):
        group = QCustomButtonGroup(self.ui.themeGroupHost, exclusive=True,
                                   orientation="horizontal")
        group.setObjectName("themeGroup")
        group.setButtons(list(THEMES.keys()))
        current = QSettings().value("THEME")
        group.setSelectedId(1 if current == THEMES["Day"] else 0)
        group.selectionChanged.connect(self._onThemeChanged)
        self.ui.themeGroupHostLayout.addWidget(group)

    def _onThemeChanged(self, buttonId, text):
        name = THEMES.get(text)
        if not name:
            return
        s = QSettings()
        s.setValue("THEME", name)
        s.setValue("INIT-THEME-SET", True)
        # applyCompiledSass re-reads THEME; setTheme() would regenerate the
        # icon set (deadlock path under the offscreen platform).
        self.themeEngine.applyCompiledSass(generateIcons=False,
                                           paintEntireApp=True)

    # ------------------------------------------------------------------ #
    ## Forms & validation (field wiring is data, chrome stays in scss)
    # ------------------------------------------------------------------ #
    def _buildForm(self):
        form = self.ui.showcaseForm

        nameInput = QCustomInput(form)
        nameInput.setPlaceholderText("Enter your name")
        nameField = QCustomFormField("Name", widget=nameInput)
        nameField.set_required(True)
        form.add_field(nameField)

        emailInput = QCustomInput(form)
        emailInput.setPlaceholderText("user@example.com")
        emailField = QCustomFormField("Email", widget=emailInput)
        emailField.set_validator(lambda v: "@" in v if v else False)
        form.add_field(emailField)

        combo = QCustomComboBox(form, editable=True)
        combo.setItems(["Option A", "Option B", "Option C"])
        comboField = QCustomFormField("Selection", widget=combo)
        form.add_field(comboField)

        form.submitted.connect(self._onFormSubmitted)

    def _onFormSubmitted(self, payload):
        QCustomToast.success(self, "Submitted %d fields" % len(payload),
                             title="Form Valid")

    def _buildPrefGroup(self):
        group = QCustomButtonGroup(self.ui.prefGroupHost, exclusive=True,
                                   orientation="horizontal")
        group.setObjectName("prefGroup")
        group.setButtons(["Monthly", "Quarterly", "Annual"])
        group.setSelectedId(0)
        self.ui.prefGroupHostLayout.addWidget(group)
        self.ui.prefGroupHostLayout.addStretch()

    # ------------------------------------------------------------------ #
    ## Data seeding (deltas / ring values are data, not chrome)
    # ------------------------------------------------------------------ #
    def _seedData(self):
        self.ui.statRevenue.setDelta("+8.2%", "up")
        self.ui.statUsers.setDelta("+12%", "up")
        self.ui.statRetention.setDelta("-2%", "down")

        self.ui.ringCpu.setValue(65)
        self.ui.ringMemory.setValue(42)
        self.ui.ringDisk.setValue(88)

        card = self.ui.featureCard
        card.addWidget(self.ui.cardContentHolder)

        accordion = self.ui.accordion
        for title in ["Section 1", "Section 2", "Section 3"]:
            accordion.addSection(title, QLabel("Content for %s" % title))
        accordion.setExpanded(0, True)

    # ------------------------------------------------------------------ #
    ## Toasts
    # ------------------------------------------------------------------ #
    def _wireToasts(self):
        pairs = [
            (self.ui.toastInfoBtn, "info"),
            (self.ui.toastSuccessBtn, "success"),
            (self.ui.toastWarningBtn, "warning"),
            (self.ui.toastErrorBtn, "error"),
        ]
        for button, variant in pairs:
            button.clicked.connect(
                lambda _=False, v=variant: self._showToast(v))

    def _showToast(self, variant):
        title, message = TOAST_MESSAGES[variant]
        QCustomToast.show_toast(self, message, variant=variant, title=title)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
