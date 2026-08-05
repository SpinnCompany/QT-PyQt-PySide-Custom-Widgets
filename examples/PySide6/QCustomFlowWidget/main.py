"""QCustomFlowWidget — complete test suite.

Add / remove / reorder tiles of many kinds inside an animated
QCustomFlowWidget, tune the animation (duration + easing), the layout
(margin + spacing), run performance / stress scenarios, and toggle
data-driven ordering (orderJsonPath -> style.json QCustomFlowLayoutOrder).

All chrome lives in json-styles/style.json + Qss/scss/defaultStyle.scss;
tiles are tagged with dynamic properties (tileKind / tileRole / flash)
and painted purely from the stylesheet. This file only boots the app,
creates data-driven tiles and wires signals.
"""

import os
import random
import sys

# Force PySide6 to match compiled ui files
os.environ.setdefault("QT_API", "pyside6")

from Custom_Widgets.Project import setProjectRoot
setProjectRoot(__file__)

from Custom_Widgets import *
from Custom_Widgets.QCustomQLabel import QCustomQLabel
from qtpy.QtCore import QCoreApplication, QSettings, Qt, QTimer
from qtpy.QtWidgets import (
    QApplication, QFrame, QLabel, QMessageBox, QPushButton, QVBoxLayout,
)

APP_DIR = os.path.dirname(os.path.abspath(__file__))

TILE_ROLES = ["tile1", "tile2", "tile3", "tile4",
              "tile5", "tile6", "tile7", "tile8"]
NUMBER_ROLES = ["num1", "num2", "num3", "num4", "num5"]
ICON_NAMES = ["star", "heart", "feather", "send", "award",
              "sun", "target", "zap", "gift", "coffee"]


def repolish(widget):
    """Re-evaluate the stylesheet after a dynamic-property change."""
    widget.style().unpolish(widget)
    widget.style().polish(widget)


class FlowTile(QFrame):
    """A flow tile painted entirely by the app stylesheet (tileKind /
    tileRole dynamic properties). Reports clicks and flashes a border
    via the `flash` property + repolish (no inline styles)."""

    def __init__(self, text, kind, role="", size=(120, 100), parent=None):
        super().__init__(parent)
        self.setFixedSize(size[0], size[1])
        self.text = text
        self.setProperty("tileKind", kind)
        if role:
            self.setProperty("tileRole", role)
        self.clickCallback = None

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        self.label = QLabel(text)
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)
        if not text:
            self.label.hide()  # icon tiles carry a QCustomQLabel instead

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self.clickCallback:
            self.clickCallback(self)

    def setText(self, text):
        self.text = text
        self.label.setText(text)

    def flash(self, durationMs=200):
        self.setProperty("flash", True)
        repolish(self)
        QTimer.singleShot(durationMs, self._unflash)

    def _unflash(self):
        self.setProperty("flash", False)
        repolish(self)


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
        QCoreApplication.setApplicationName("QCustomFlowWidget Test Suite")
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
        if s.value("THEME") not in ("Flow Suite Night", "Flow Suite Day"):
            # A stray pre-identity QSettings file strips every Default-Theme
            # flag at parse time — name this app's default explicitly.
            s.setValue("THEME", "Flow Suite Night")
            s.setValue("INIT-THEME-SET", True)
        s.setValue("THEMES-LIST", themeEngine.themes)
        themeEngine.reloadJsonStyles(update=False)
        themeEngine.applyCompiledSass(generateIcons=False, paintEntireApp=True)

        from Custom_Widgets.AppControl import maybe_start_app_control
        try:
            maybe_start_app_control()
        except Exception:
            pass

        self.flowWidget = self.ui.flowWidget
        self.ui.mainSplitter.setSizes([400, 500])
        self._tileSerial = 0
        self._wire()
        self._addSampleWidgets()
        self._updateCounter()
        self.status().showMessage(
            "Ready - Test the flow widget with various controls!")

    def status(self):
        return self.ui.statusbar

    # ------------------------------------------------------------------ #
    ## Wiring (signals only — chrome stays in scss)
    # ------------------------------------------------------------------ #
    def _wire(self):
        ui = self.ui
        ui.easingCombo.addItems([
            "Linear", "InQuad", "OutQuad", "InOutQuad",
            "InCubic", "OutCubic", "InOutCubic",
            "InQuart", "OutQuart", "InOutQuart",
            "InQuint", "OutQuint", "InOutQuint",
            "InSine", "OutSine", "InOutSine",
            "InExpo", "OutExpo", "InOutExpo",
            "InCirc", "OutCirc", "InOutCirc",
            "InBack", "OutBack", "InOutBack",
            "InBounce", "OutBounce", "InOutBounce",
        ])
        ui.easingCombo.setCurrentText("OutCubic")

        ui.addBtn.clicked.connect(self.addWidget)
        ui.add5Btn.clicked.connect(lambda: self.addBatchWidgets(5))
        ui.add10Btn.clicked.connect(lambda: self.addBatchWidgets(10))
        ui.add20Btn.clicked.connect(lambda: self.addBatchWidgets(20))
        ui.add50Btn.clicked.connect(lambda: self.addBatchWidgets(50))
        ui.removeLastBtn.clicked.connect(self.removeLastWidget)
        ui.removeRandomBtn.clicked.connect(self.removeRandomWidget)
        ui.clearAllBtn.clicked.connect(self.clearAll)
        ui.useJsonOrderCheck.toggled.connect(self.toggleJsonOrder)

        ui.animateCb.toggled.connect(self.toggleAnimations)
        ui.durationSlider.valueChanged.connect(self.changeDuration)
        ui.easingCombo.currentTextChanged.connect(self.changeEasing)

        ui.marginSlider.valueChanged.connect(self.changeMargin)
        ui.spacingSlider.valueChanged.connect(self.changeSpacing)
        ui.applySpacingBtn.clicked.connect(self.applySeparateSpacing)

        ui.perfBtn.clicked.connect(self.performanceTest)
        ui.extremeBtn.clicked.connect(self.extremeTest)
        ui.shuffleBtn.clicked.connect(self.shuffleWidgets)
        ui.reverseBtn.clicked.connect(self.reverseOrder)
        ui.sortBtn.clicked.connect(self.sortBySize)
        ui.resizeStressBtn.clicked.connect(self.stressTest)
        ui.rapidAddBtn.clicked.connect(self.rapidAddRemove)

        flowLayout = self.ui.flowWidget.getFlowLayout()
        if flowLayout:
            flowLayout.animationStarted.connect(
                lambda: self.status().showMessage("Layout animation started..."))
            flowLayout.animationFinished.connect(
                lambda: self.status().showMessage("Animation complete!", 2000))

        self.statusTimer = QTimer(self)
        self.statusTimer.timeout.connect(self.updateAnimationStatus)
        self.statusTimer.start(100)

    # ------------------------------------------------------------------ #
    ## Tile factories (data-driven; painted by the stylesheet)
    # ------------------------------------------------------------------ #
    def _nextTileName(self):
        self._tileSerial += 1
        return "flowTile%d" % self._tileSerial

    def createColoredWidget(self, text, role, size=(120, 100)):
        tile = FlowTile(text, "color", role, size)
        tile.setObjectName(self._nextTileName())
        tile.clickCallback = self.onWidgetClicked
        return tile

    def createGradientWidget(self, text):
        tile = FlowTile(text, "gradient", size=(140, 100))
        tile.setObjectName(self._nextTileName())
        return tile

    def createNumberWidget(self, number):
        role = NUMBER_ROLES[number % len(NUMBER_ROLES)]
        tile = FlowTile(str(number), "number", role, size=(100, 80))
        tile.setObjectName(self._nextTileName())
        return tile

    def createLetterWidget(self, letter):
        tile = FlowTile(letter, "letter", size=(90, 90))
        tile.setObjectName(self._nextTileName())
        return tile

    def createIconWidget(self, iconName):
        tile = FlowTile("", "icon", size=(100, 100))
        tile.setObjectName(self._nextTileName())
        icon = QCustomQLabel(tile)
        icon.setProperty("flowIcon", iconName)
        icon.setAlignment(Qt.AlignCenter)
        icon.setFixedSize(56, 56)
        tile.layout().addWidget(icon)
        return tile

    def createCustomSizeWidget(self):
        width = random.randint(80, 200)
        height = random.randint(60, 150)
        tile = FlowTile("%dx%d" % (width, height), "custom",
                        size=(width, height))
        tile.setObjectName(self._nextTileName())
        return tile

    # ------------------------------------------------------------------ #
    ## Widget management
    # ------------------------------------------------------------------ #
    def _addSampleWidgets(self):
        for i in range(12):
            role = TILE_ROLES[i % len(TILE_ROLES)]
            self.flowWidget.addWidget(
                self.createColoredWidget("Item %d" % (i + 1), role))

    def addWidget(self):
        widgetType = self.ui.widgetType.currentText()
        count = self.flowWidget.getFlowLayout().count()

        if widgetType == "Color Box":
            role = TILE_ROLES[count % 6]
            widget = self.createColoredWidget("Item %d" % (count + 1), role)
        elif widgetType == "Number Box":
            widget = self.createNumberWidget(count + 1)
        elif widgetType == "Letter Box":
            letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            widget = self.createLetterWidget(letters[count % len(letters)])
        elif widgetType == "Icon Box":
            widget = self.createIconWidget(ICON_NAMES[count % len(ICON_NAMES)])
        elif widgetType == "Button":
            widget = QPushButton("Button %d" % (count + 1))
            widget.setObjectName(self._nextTileName())
            widget.setProperty("role", "tileButton")
            widget.setFixedSize(120, 60)
            widget.clicked.connect(
                lambda checked=False, btn=widget:
                self.showMessage("Button %s clicked!" % btn.text()))
        elif widgetType == "Custom Size":
            widget = self.createCustomSizeWidget()
        elif widgetType == "Gradient Box":
            widget = self.createGradientWidget("Grad %d" % (count + 1))
        else:  # Random Color — random pick from the theme tile palette
            role = random.choice(TILE_ROLES)
            widget = self.createColoredWidget("Random %d" % (count + 1), role)

        self.flowWidget.addWidget(widget)
        self._updateCounter()

    def addBatchWidgets(self, count):
        animationsEnabled = self.ui.animateCb.isChecked()
        if animationsEnabled:
            self.flowWidget.animationEnabled = False

        for _ in range(count):
            self.addWidget()

        if animationsEnabled:
            self.flowWidget.animationEnabled = True

        self.status().showMessage("Added %d widgets" % count, 2000)

    def removeLastWidget(self):
        flowLayout = self.flowWidget.getFlowLayout()
        if flowLayout.count() > 0:
            item = flowLayout.takeAt(flowLayout.count() - 1)
            if item and item.widget():
                item.widget().deleteLater()
            self._updateCounter()

    def removeRandomWidget(self):
        flowLayout = self.flowWidget.getFlowLayout()
        count = flowLayout.count()
        if count > 0:
            index = random.randint(0, count - 1)
            item = flowLayout.takeAt(index)
            if item and item.widget():
                item.widget().deleteLater()
            self._updateCounter()
            self.status().showMessage(
                "Removed widget at position %d" % index, 2000)

    def clearAll(self):
        reply = QMessageBox.question(
            self, "Clear All",
            "Are you sure you want to clear all widgets?",
            QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.flowWidget.stopAllAnimations()
            self.flowWidget.clear()
            self._updateCounter()
            self.status().showMessage("Cleared all widgets", 2000)

    # ------------------------------------------------------------------ #
    ## Data-driven order (orderJsonPath -> style.json QCustomFlowLayoutOrder)
    # ------------------------------------------------------------------ #
    def toggleJsonOrder(self, enabled):
        if enabled:
            self.flowWidget.orderJsonPath = os.path.join(
                APP_DIR, "json-styles", "style.json")
            self.status().showMessage(
                "Seed tiles now follow style.json QCustomFlowLayoutOrder", 3000)
        else:
            self.flowWidget.orderJsonPath = ""
            self.status().showMessage(
                "Back to insertion order (shuffle/reverse/sort act on it)",
                3000)
        self.flowWidget.refreshLayout()

    # ------------------------------------------------------------------ #
    ## Reorder tests
    # ------------------------------------------------------------------ #
    def _takeAllWidgets(self):
        flowLayout = self.flowWidget.getFlowLayout()
        widgets = []
        for _ in range(flowLayout.count()):
            item = flowLayout.takeAt(0)
            if item and item.widget():
                widgets.append(item.widget())
        return flowLayout, widgets

    def shuffleWidgets(self):
        flowLayout, widgets = self._takeAllWidgets()
        random.shuffle(widgets)
        for widget in widgets:
            flowLayout.addWidget(widget)
        self._updateCounter()
        self.status().showMessage("Widgets shuffled!", 2000)

    def reverseOrder(self):
        flowLayout, widgets = self._takeAllWidgets()
        widgets.reverse()
        for widget in widgets:
            flowLayout.addWidget(widget)
        self._updateCounter()
        self.status().showMessage("Widget order reversed!", 2000)

    def sortBySize(self):
        flowLayout, widgets = self._takeAllWidgets()
        widgets.sort(key=lambda w: w.width() * w.height())
        for widget in widgets:
            flowLayout.addWidget(widget)
        self._updateCounter()
        self.status().showMessage("Widgets sorted by size!", 2000)

    # ------------------------------------------------------------------ #
    ## Performance / stress tests
    # ------------------------------------------------------------------ #
    def performanceTest(self):
        reply = QMessageBox.question(
            self, "Performance Test",
            "This will add 100 widgets. Continue?",
            QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.flowWidget.stopAllAnimations()
            self.flowWidget.clear()
            animationsEnabled = self.ui.animateCb.isChecked()
            self.flowWidget.animationEnabled = False
            for i in range(100):
                self.flowWidget.addWidget(self.createNumberWidget(i + 1))
            self.flowWidget.animationEnabled = animationsEnabled
            self._updateCounter()
            self.status().showMessage(
                "Performance test: 100 widgets added!", 3000)

    def extremeTest(self):
        reply = QMessageBox.question(
            self, "Extreme Test",
            "This will add 500 widgets. Continue?\n(This may take a moment)",
            QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.flowWidget.stopAllAnimations()
            self.flowWidget.clear()
            animationsEnabled = self.ui.animateCb.isChecked()
            self.flowWidget.animationEnabled = False
            for i in range(500):
                if i % 50 == 0:
                    QApplication.processEvents()  # Keep UI responsive
                self.flowWidget.addWidget(self.createNumberWidget(i + 1))
            self.flowWidget.animationEnabled = animationsEnabled
            self._updateCounter()
            self.status().showMessage("Extreme test: 500 widgets added!", 3000)

    def stressTest(self):
        self.status().showMessage("Starting stress test...", 2000)
        originalWidth = self.width()

        def resizeLoop(iteration=0):
            if iteration < 30:
                width = originalWidth + (100 if iteration % 2 == 0 else -100)
                self.resize(width, self.height())
                QTimer.singleShot(30, lambda: resizeLoop(iteration + 1))
            else:
                self.resize(originalWidth, self.height())
                self.status().showMessage("Stress test completed!", 2000)

        resizeLoop()

    def rapidAddRemove(self):
        self.status().showMessage("Starting rapid add/remove test...", 2000)

        def rapidLoop(iteration=0):
            if iteration < 50:
                if iteration % 2 == 0:
                    self.flowWidget.addWidget(
                        self.createNumberWidget(iteration))
                else:
                    flowLayout = self.flowWidget.getFlowLayout()
                    if flowLayout.count() > 0:
                        item = flowLayout.takeAt(0)
                        if item and item.widget():
                            item.widget().deleteLater()
                self._updateCounter()
                QTimer.singleShot(50, lambda: rapidLoop(iteration + 1))
            else:
                self.status().showMessage(
                    "Rapid add/remove test completed!", 2000)

        rapidLoop()

    # ------------------------------------------------------------------ #
    ## Animation / layout properties
    # ------------------------------------------------------------------ #
    def toggleAnimations(self, enabled):
        self.flowWidget.animationEnabled = enabled
        self.status().showMessage(
            "Animations %s" % ("enabled" if enabled else "disabled"), 2000)

    def changeDuration(self, value):
        self.flowWidget.animationDuration = value
        self.ui.durationLabel.setText("%dms" % value)

    def changeEasing(self, curve):
        self.flowWidget.animationEasingCurve = curve
        self.status().showMessage("Easing: %s" % curve, 2000)

    def changeMargin(self, value):
        self.flowWidget.margin = value
        self.ui.marginLabel.setText("%dpx" % value)

    def changeSpacing(self, value):
        self.flowWidget.spacing = value
        self.ui.spacingLabel.setText("%dpx" % value)

    def applySeparateSpacing(self):
        self.flowWidget.horizontalSpacing = self.ui.hSpin.value()
        self.flowWidget.verticalSpacing = self.ui.vSpin.value()
        self.status().showMessage(
            "Applied H:%dpx V:%dpx" % (self.ui.hSpin.value(),
                                       self.ui.vSpin.value()), 2000)

    # ------------------------------------------------------------------ #
    ## Status displays (colours flip via [state] rules in the stylesheet)
    # ------------------------------------------------------------------ #
    def _updateCounter(self):
        flowLayout = self.flowWidget.getFlowLayout()
        count = flowLayout.count() if flowLayout else 0
        label = self.ui.counterLabel
        label.setText("Widgets: %d" % count)
        state = "empty" if count == 0 else "filled"
        if label.property("state") != state:
            label.setProperty("state", state)
            repolish(label)

    def updateAnimationStatus(self):
        label = self.ui.animStatus
        if self.flowWidget.isAnimating():
            text, state = "Animating...", "busy"
        else:
            text, state = "Idle", "idle"
        if label.text() != text:
            label.setText(text)
            label.setProperty("state", state)
            repolish(label)

    def onWidgetClicked(self, widget):
        text = getattr(widget, "text", "widget")
        self.status().showMessage("Clicked: %s" % text, 2000)
        widget.flash()

    def showMessage(self, message):
        QMessageBox.information(self, "Info", message)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
