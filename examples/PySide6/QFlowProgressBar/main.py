"""QFlowProgressBar demo — Circular, Flat and Square step bars with clickable steps."""

import json
import os, sys

# Force PySide6 to match compiled ui files
os.environ.setdefault("QT_API", "pyside6")

from Custom_Widgets.Project import setProjectRoot
setProjectRoot(__file__)

from Custom_Widgets import *
from Custom_Widgets.QFlowProgressBar import QFlowProgressBar
from qtpy.QtCore import QCoreApplication, QSettings, Qt
from qtpy.QtGui import QColor
from qtpy.QtWidgets import QApplication

STEPS = ["Start: Step 1", "Step 2", "Step 3", "Final step: Step 4"]


class MainWindow(QCustomMainWindow):
    def __init__(self, parent=None):
        QCustomMainWindow.__init__(self)
        # Set BEFORE loadJsonStyle: the theme engine reads QSettings() while
        # parsing the json — without these names it reads the interpreter-wide
        # settings file and the app's own THEME/default theme never resolve.
        QCoreApplication.setOrganizationName("CustomWidgets")
        QCoreApplication.setApplicationName("QFlowProgressBar Demo")

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

        self._buildBars()
        self._wireDemo()

    def _chartPalette(self):
        """ChartPalette section for the active theme (falls back to the first)."""
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "json-styles", "style.json")
        with open(path) as fh:
            palettes = json.load(fh)["ChartPalette"]
        theme = str(getattr(self.themeEngine, "theme", "") or "")
        return palettes.get(theme) or next(iter(palettes.values()))

    def _buildBars(self):
        """The bars take their steps + colours in the constructor, so they are
        created here (data first) and dropped into the .ui holder layouts."""
        pal = self._chartPalette()
        variants = [
            (QFlowProgressBar.Styles.Circular, self.ui.circularHolder,
             pal["circularFinished"], pal["circularUnfinished"]),
            (QFlowProgressBar.Styles.Flat, self.ui.flatHolder,
             pal["flatFinished"], pal["flatUnfinished"]),
            (QFlowProgressBar.Styles.Square, self.ui.squareHolder,
             pal["squareFinished"], pal["squareUnfinished"]),
        ]
        finishedNumber = QColor(pal["finishedNumber"])

        self.flowProgressBars = []
        for style, holder, finished, unfinished in variants:
            bar = QFlowProgressBar(
                STEPS,
                style,
                finishedBackgroundColor=QColor(finished),
                unfinishedBackgroundColor=QColor(unfinished),
                finishedNumberColor=finishedNumber,
                numberFontSize=12,
                textFontSize=10,
                pointerDirection=QFlowProgressBar.Direction.Down,
                animationDuration=1000,
                stepsClickable=True,
            )
            bar.setMaximumHeight(100)
            bar.setMinimumHeight(70)
            bar.setAttribute(Qt.WA_TranslucentBackground, True)
            bar.onStepClicked.connect(self.onStepClicked)
            holder.addWidget(bar)
            self.flowProgressBars.append(bar)

    def _wireDemo(self):
        self.ui.nextButton.clicked.connect(self.nextStep)
        self.ui.prevButton.clicked.connect(self.prevStep)

    def nextStep(self):
        for bar in self.flowProgressBars:
            bar.changeCurrentStep(bar.getCurrentStep() + 1)

    def prevStep(self):
        for bar in self.flowProgressBars:
            bar.changeCurrentStep(bar.getCurrentStep() - 1)

    def onStepClicked(self, step: int):
        print(f"Step {step + 1} clicked")
        for bar in self.flowProgressBars:
            bar.changeCurrentStep(step + 1)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
