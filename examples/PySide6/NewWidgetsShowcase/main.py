"""
New Widgets Showcase — QCustomInput, QCustomButtonGroup, and modern data viz.
Demonstrates the release-ready input layer plus high-value chart/gauge widgets,
styled by the json-styles + Qss/scss theme pipeline (no inline styles).
"""
import os
import sys

# Force PySide6 to match compiled ui files
os.environ.setdefault("QT_API", "pyside6")

from Custom_Widgets.Project import setProjectRoot
setProjectRoot(__file__)

from Custom_Widgets import *
from Custom_Widgets.QAppSettings import QAppSettings
from Custom_Widgets.QCustomInput import QCustomInput
from Custom_Widgets.QCustomButtonGroup import QCustomButtonGroup
from Custom_Widgets.QCustomForm import QCustomFormField
from Custom_Widgets.QCustomToast import QCustomToast
from qtpy.QtCore import QCoreApplication, QSettings
from qtpy.QtWidgets import QApplication, QLabel


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
        QCoreApplication.setApplicationName("New Widgets Showcase")
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
            # Name the app's default theme explicitly: a stale THEME key in the
            # pre-appName fallback QSettings file makes the json loader drop
            # every Default-Theme flag, so relying on the flag alone can leave
            # the app with no theme selected at all.
            target = "Showcase-Dark"
            for t in themeEngine.themes:
                if getattr(t, "defaultTheme", False):
                    target = t.name
                    break
            s.setValue("THEME", target)
            s.setValue("INIT-THEME-SET", True)
        s.setValue("THEMES-LIST", themeEngine.themes)
        themeEngine.reloadJsonStyles(update=False)
        themeEngine.applyCompiledSass(generateIcons=False, paintEntireApp=True)

        from Custom_Widgets.AppControl import maybe_start_app_control
        try:
            maybe_start_app_control()
        except Exception:
            pass

        self._buildFormFields()
        self._buildButtonGroups()
        self._seedDataViz()
        self.ui.submitBtn.clicked.connect(lambda: QCustomToast.success(
            self, "Form submitted successfully!", title="Success"
        ))

    # ------------------------------------------------------------------ #
    ## Input layer (data-driven wiring — styling stays in Qss/scss)
    # ------------------------------------------------------------------ #
    def _buildFormFields(self):
        form = self.ui.showcaseForm
        for variant in ["outline", "primary", "secondary"]:
            inp = QCustomInput()
            inp.variant = variant
            inp.sizeVariant = "md"
            inp.setPlaceholderText("Enter text (%s)" % variant)

            field = QCustomFormField("Field (%s)" % variant, widget=inp)
            if variant == "primary":
                field.set_required(True)
            form.add_field(field)

        form.submitted.connect(self._onFormSubmit)

    def _buildButtonGroups(self):
        host = self.ui.groupsCard
        layout = self.ui.groupsHostLayout
        for variant in ["outline", "primary", "secondary"]:
            caption = QLabel("%s:" % variant.title(), host)
            caption.setObjectName("groupCaption%s" % variant.title())
            layout.addWidget(caption)

            group = QCustomButtonGroup(host, exclusive=True,
                                       orientation="horizontal")
            group.setObjectName("group%s" % variant.title())
            group.setButtons(["Option 1", "Option 2", "Option 3"])
            group.variant = variant
            group.setSelectedId(0)
            layout.addWidget(group)

    def _seedDataViz(self):
        # Data AFTER the widgets exist: setData() is the (restored) heatmap
        # data API — an alias of setValues().
        self.ui.heatmap.mode = "grid"
        self.ui.heatmap.setData([
            [1, 2, 3, 4, 5],
            [2, 3, 4, 5, 6],
            [3, 4, 5, 6, 7],
        ])
        # Heat ramp colours come from the ACTIVE theme so they flip with it.
        low = self.themeEngine.themeColor("HEAT_LOW", "")
        high = self.themeEngine.themeColor("HEAT_HIGH", "")
        if low and high:
            self.ui.heatmap.setColors(low, high)

    def _onFormSubmit(self, payload):
        QCustomToast.success(
            self,
            "Submitted %d fields" % len(payload),
            title="Form Valid"
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
