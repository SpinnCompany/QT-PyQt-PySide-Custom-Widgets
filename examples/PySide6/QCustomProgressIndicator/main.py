########################################################################
## QCustomProgressIndicator example — SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/spinnTv
# WEBSITE: spinncode.com
##
## Three form-progress indicators: a self-restyling download simulation,
## a 10-step form and a 5-step form, each driven from the buttons below
## it. Chrome comes from Qss/scss/defaultStyle.scss + json-styles.
## Run:
##     python main.py
########################################################################
import os
import random
import sys

# Force PySide6 to match compiled ui files
os.environ.setdefault("QT_API", "pyside6")

from Custom_Widgets.Project import setProjectRoot
setProjectRoot(__file__)

from Custom_Widgets import *
from Custom_Widgets.QAppSettings import QAppSettings
from qtpy.QtCore import QCoreApplication, QSettings, QTimer
from qtpy.QtWidgets import QApplication


class MainWindow(QCustomMainWindow):
    def __init__(self, parent=None):
        QCustomMainWindow.__init__(self)
        from src.ui_MainWindow import Ui_MainWindow
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Name the QSettings scope BEFORE loadJsonStyle: the theme loader
        # checks QSettings("THEME") while registering CustomThemes, and an
        # unnamed app reads a shared fallback file whose stale THEME key
        # strips the Default-Theme flag.
        QCoreApplication.setOrganizationName("CustomWidgets")
        QCoreApplication.setApplicationName("QCustomProgressIndicator Showcase")

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

        self._wireIndicators()

    # ------------------------------------------------------------------ #
    ## Wiring + data seeding (no styling here — see Qss/scss)
    # ------------------------------------------------------------------ #
    def _wireIndicators(self):
        ui = self.ui

        # 5-STEP FORM INDICATOR
        ui.formIndicator5.updateFormProgressIndicator(
            formProgressAnimationEasingCurve="InOutQuint",
            height=80,
            width=500,
        )

        # 10-STEP FORM INDICATOR
        ui.formIndicator10.updateFormProgressIndicator(
            formProgressCount=10,
            formProgressAnimationDuration=2000,  # 2 seconds
            height=80,
        )

        ui.formIndicator5.selectFormProgressIndicatorTheme(4)
        ui.formIndicator10.selectFormProgressIndicatorTheme(2)
        ui.formIndicator10.animateFormProgress(60)  # 60 percent

        # DOWNLOAD SIMULATION INDICATOR
        ui.downloadIndicator.updateFormProgressIndicator(
            formProgressCount=10,
            formProgressAnimationDuration=2000,
            height=80,
            width=500,
        )
        ui.downloadIndicator.selectFormProgressIndicatorTheme(3)
        ui.downloadIndicator.animateFormProgress(60)

        # NAVIGATE THROUGH THE 10-STEP FORM
        ui.btnPct20.clicked.connect(lambda: ui.formIndicator10.animateFormProgress(20))
        ui.btnPct40.clicked.connect(lambda: ui.formIndicator10.animateFormProgress(40))
        ui.btnPct60.clicked.connect(lambda: ui.formIndicator10.animateFormProgress(60))
        ui.btnPct80.clicked.connect(lambda: ui.formIndicator10.animateFormProgress(80))
        ui.btnPct100.clicked.connect(lambda: ui.formIndicator10.animateFormProgress(100))

        # PROGRESS STEP STATUSES
        ui.formIndicator10.setStepStatus(
            step_5_error=True,
            step_3_warning=True,
            step_8_success=True,
        )
        ui.formIndicator5.setStepStatus(
            step_5_error=True,
            step_2_warning=True,
            step_3_success=True,
        )

        # NAVIGATE THROUGH THE 5-STEP FORM
        ui.btnStep1.clicked.connect(lambda: ui.formIndicator5.animateFormProgress(20))
        ui.btnStep2.clicked.connect(lambda: ui.formIndicator5.animateFormProgress(40))
        ui.btnStep3.clicked.connect(lambda: ui.formIndicator5.animateFormProgress(60))
        ui.btnStep4.clicked.connect(lambda: ui.formIndicator5.animateFormProgress(80))
        ui.btnStep5.clicked.connect(lambda: ui.formIndicator5.animateFormProgress(100))

        # ANIMATE THE DOWNLOAD SIMULATION
        self.download = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.downloadProgress)
        self.timer.start(100)

    # Simulate download process
    def downloadProgress(self):
        ui = self.ui
        statuses = ["warning", "error", "success"]
        if self.download < 101:
            self.download += 1
        else:
            self.download = 0
            # Reset step statuses
            for x in range(1, 11):
                for y in statuses:
                    ui.downloadIndicator.setStepStatus(
                        step=int(x),
                        status=y,
                        value=False,
                    )

            # Apply a new random style
            formProgressCount = random.choice([10, 5, 3, 7, 15])
            height = random.choice([20, 40, 50, 60])
            theme = random.choice([1, 2, 3, 4, 5])
            ui.downloadIndicator.updateFormProgressIndicator(
                formProgressCount=formProgressCount,
                height=height,
            )
            ui.downloadIndicator.selectFormProgressIndicatorTheme(theme)

            # Update UI labels
            ui.themeValue.setText(str(theme))
            ui.heightValue.setText(str(height))
            ui.stepsValue.setText(str(formProgressCount))

        # Animate progress
        ui.downloadIndicator.animateFormProgress(self.download)

        # Apply a random progress step status
        randStatus = random.choice(statuses)
        if self.download % ui.downloadIndicator.formProgressCount == 0:
            ui.downloadIndicator.setStepStatus(
                step=int(self.download / ui.downloadIndicator.formProgressCount),
                status=randStatus,
                value=True,
            )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
