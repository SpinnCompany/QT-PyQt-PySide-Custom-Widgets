"""AnalogGaugeWidget showcase — a live gauge with sliders driving every property."""

import os, sys

# Force PySide6 to match compiled ui files
os.environ.setdefault("QT_API", "pyside6")

from Custom_Widgets.Project import setProjectRoot
setProjectRoot(__file__)

from Custom_Widgets import *
from qtpy.QtCore import QCoreApplication, QSettings
from qtpy.QtGui import QColor
from qtpy.QtWidgets import QApplication

GAUGE_THEME_COUNT = 8  # built-in themes shipped in QAnalogGaugeThemes.json


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
        QCoreApplication.setApplicationName("AnalogGaugeWidget Showcase")
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
            default_theme = next(
                (t.name for t in themeEngine.themes if getattr(t, "defaultTheme", False)),
                "Gauge-Dark",
            )
            s.setValue("THEME", default_theme)
            s.setValue("INIT-THEME-SET", True)
        s.setValue("THEMES-LIST", themeEngine.themes)
        themeEngine.reloadJsonStyles(update=False)
        themeEngine.applyCompiledSass(generateIcons=False, paintEntireApp=True)

        from Custom_Widgets.AppControl import maybe_start_app_control
        try:
            maybe_start_app_control()
        except Exception:
            pass

        self._setup_gauge()
        self._wire_controls()

    # ------------------------------------------------------------------ setup
    def _setup_gauge(self):
        gauge = self.ui.gauge

        # Basic gauge configuration (typed Qt properties)
        gauge.enableBarGraph = True
        gauge.units = "Km/h"
        gauge.minValue = 0
        gauge.maxValue = 100
        gauge.scalaCount = 10

        # Start from the middle value
        gauge.setValue(int((gauge.maxValue - gauge.minValue) / 2))

        # Gauge colours follow the ACTIVE theme (Other-variables in style.json)
        self._apply_theme_gauge_colors()

        # Gauge theme selector (built-in themes 0..N)
        for x in range(GAUGE_THEME_COUNT):
            if self.ui.theme_comboBox.findText(str(x)) < 0:
                self.ui.theme_comboBox.addItem(str(x))

    def _apply_theme_gauge_colors(self):
        te = self.themeEngine
        gauge = self.ui.gauge
        g1 = te.themeColor("GAUGE_1", te.themeColor("ACCENT_2"))
        g2 = te.themeColor("GAUGE_2", te.themeColor("ACCENT_1"))
        g3 = te.themeColor("GAUGE_3", te.themeColor("ACCENT_1"))
        gauge.setCustomGaugeTheme([[0.0, g1], [0.5, g2], [1.0, g3]])
        scale = QColor(te.themeColor("GAUGE_SCALE", te.themeColor("TEXT_2")))
        gauge.setBigScaleColor(scale)
        gauge.setFineScaleColor(scale)

    # ----------------------------------------------------------------- wiring
    def _wire_controls(self):
        ui = self.ui
        gauge = ui.gauge

        # Value slider range mirrors the gauge range
        ui.ActualValueSlider.setMaximum(gauge.maxValue)
        ui.ActualValueSlider.setMinimum(gauge.minValue)
        ui.ActualValueSlider.setValue(gauge.value)

        # Radius sliders (0..1000 mapped to a 0..1 factor by the widget)
        ui.OuterRadiusSlider.setValue(int(gauge.gaugeColorOuterRadiusFactor * 1000))
        ui.lcdOuterRadius.display(int(gauge.gaugeColorOuterRadiusFactor * 1000))
        ui.InnenRadiusSlider.setValue(int(gauge.gaugeColorInnerRadiusFactor * 1000))
        ui.lcdInnerRadius.display(int(gauge.gaugeColorInnerRadiusFactor * 1000))

        # Scale angle sliders
        ui.GaugeStartSlider.setValue(int(gauge.scaleStartAngle))
        ui.lcdGaugeStart.display(int(gauge.scaleStartAngle))
        ui.GaugeSizeSlider.setValue(int(gauge.totalScaleAngleSize))
        ui.lcdGaugeSize.display(int(gauge.totalScaleAngleSize))

        # RGBA needle colour sliders
        for slider in (ui.RedSlider_Needle, ui.GreenSlider_Needle,
                       ui.BlueSlider_Needle, ui.TrancSlider_Needle):
            slider.valueChanged.connect(self.setNeedleColor)
        ui.lcdNumber_Red_Needle.display(ui.RedSlider_Needle.value())
        ui.lcdNumber_Green_Needle.display(ui.GreenSlider_Needle.value())
        ui.lcdNumber_Blue_Needle.display(ui.BlueSlider_Needle.value())
        ui.lcdNumber_Trancparency_Needle.display(ui.TrancSlider_Needle.value())

        # RGBA needle-on-drag colour sliders
        for slider in (ui.RedSlider_NeedleDrag, ui.GreenSlider_NeedleDrag,
                       ui.BlueSlider_NeedleDrag, ui.TrancSlider_NeedleDrag):
            slider.valueChanged.connect(self.setNeedleColorOnDrag)
        ui.lcdNumber_Red_NeedleDrag.display(ui.RedSlider_NeedleDrag.value())
        ui.lcdNumber_Green_NeedleDrag.display(ui.GreenSlider_NeedleDrag.value())
        ui.lcdNumber_Blue_NeedleDrag.display(ui.BlueSlider_NeedleDrag.value())
        ui.lcdNumber_Trancparency_NeedleDrag.display(ui.TrancSlider_NeedleDrag.value())

        # RGBA scale text colour sliders
        for slider in (ui.RedSlider_Scale, ui.GreenSlider_Scale,
                       ui.BlueSlider_Scale, ui.TrancSlider_Scale):
            slider.valueChanged.connect(self.setScaleValueColor)
        ui.lcdNumber_Red_Scale.display(ui.RedSlider_Scale.value())
        ui.lcdNumber_Green_Scale.display(ui.GreenSlider_Scale.value())
        ui.lcdNumber_Blue_Scale.display(ui.BlueSlider_Scale.value())
        ui.lcdNumber_Trancparency_Scale.display(ui.TrancSlider_Scale.value())

        # RGBA value text colour sliders
        for slider in (ui.RedSlider_Display, ui.GreenSlider_Display,
                       ui.BlueSlider_Display, ui.TrancSlider_Display):
            slider.valueChanged.connect(self.setDisplayValueColor)
        ui.lcdNumber_Red_Display.display(ui.RedSlider_Display.value())
        ui.lcdNumber_Green_Display.display(ui.GreenSlider_Display.value())
        ui.lcdNumber_Blue_Display.display(ui.BlueSlider_Display.value())
        ui.lcdNumber_Trancparency_Display.display(ui.TrancSlider_Display.value())

        # Value + geometry sliders
        ui.ActualValueSlider.valueChanged.connect(self.updateGaugeValue)
        gauge.valueChanged.connect(self.updateSliderValue)
        ui.GaugeSizeSlider.valueChanged.connect(self.updateScaleAngleSize)
        ui.GaugeStartSlider.valueChanged.connect(self.updateStartScaleAngle)
        ui.InnenRadiusSlider.valueChanged.connect(self.updateGaugeColorInnerRadius)
        ui.OuterRadiusSlider.valueChanged.connect(self.updateGaugeColorOuterRadius)
        ui.offsetSlider.valueChanged.connect(self.updateAngleOffset)
        ui.MinValueSlider.valueChanged.connect(self.updateMinVal)
        ui.MaxValueSlider.valueChanged.connect(self.updateMaxVal)
        ui.MainGridSlider.valueChanged.connect(self.updateScalaCount)

        # Show/hide checkboxes
        ui.CB_barGraph.stateChanged.connect(self.toggleBarGraphMarker)
        ui.CB_ValueText.stateChanged.connect(self.toggleValueText)
        ui.CB_CenterPoint.stateChanged.connect(self.toggleCenterPoint)
        ui.CB_ScaleText.stateChanged.connect(self.toggleScaleText)
        ui.CB_ShowBarGraph.stateChanged.connect(self.setEnableScalePolygon)
        ui.CB_Grid.stateChanged.connect(self.toggleScaleGrid)
        ui.CB_fineGrid.stateChanged.connect(self.toggleFineScaleGrid)
        ui.CB_Needle.stateChanged.connect(self.toggleNeedle)

        # Built-in gauge theme selector
        ui.theme_comboBox.currentTextChanged.connect(self.changeGaugeTheme)

        self.updateGaugeValue()

    # ------------------------------------------------------------------ slots
    def changeGaugeTheme(self):
        text = self.ui.theme_comboBox.currentText()
        if text.isdigit():
            self.ui.gauge.setGaugeTheme(int(text))

    def updateScalaCount(self):
        self.ui.gauge.setScalaCount(self.ui.MainGridSlider.value())
        self.ui.lcdScalaCount.display(int(self.ui.MainGridSlider.value()))

    def updateMaxVal(self):
        self.ui.gauge.setMaxValue(self.ui.MaxValueSlider.value())
        self.ui.lcdMaxVal.display(int(self.ui.MaxValueSlider.value()))
        self.ui.ActualValueSlider.setMaximum(self.ui.gauge.maxValue)

    def updateMinVal(self):
        self.ui.gauge.setMinValue(self.ui.MinValueSlider.value())
        self.ui.lcdMinVal.display(int(self.ui.MinValueSlider.value()))
        self.ui.ActualValueSlider.setMinimum(self.ui.gauge.minValue)

    def updateAngleOffset(self):
        self.ui.gauge.setAngleOffset(self.ui.offsetSlider.value())
        self.ui.lcdGaugeOffset.display(int(self.ui.offsetSlider.value()))

    def updateGaugeColorOuterRadius(self):
        self.ui.gauge.setGaugeColorOuterRadiusFactor(self.ui.OuterRadiusSlider.value())
        self.ui.lcdOuterRadius.display(int(self.ui.OuterRadiusSlider.value()))

    def updateGaugeColorInnerRadius(self):
        self.ui.gauge.setGaugeColorInnerRadiusFactor(self.ui.InnenRadiusSlider.value())
        self.ui.lcdInnerRadius.display(int(self.ui.InnenRadiusSlider.value()))

    def updateStartScaleAngle(self):
        self.ui.gauge.setScaleStartAngle(self.ui.GaugeStartSlider.value())
        self.ui.lcdGaugeStart.display(int(self.ui.GaugeStartSlider.value()))

    def updateScaleAngleSize(self):
        self.ui.gauge.setTotalScaleAngleSize(self.ui.GaugeSizeSlider.value())
        self.ui.lcdGaugeSize.display(int(self.ui.GaugeSizeSlider.value()))

    def updateSliderValue(self):
        self.ui.ActualValueSlider.setValue(int(self.ui.gauge.value))
        self.ui.lcdGaugeValue.display(int(self.ui.gauge.value))
        self.ui.ActualValue.display(int(self.ui.gauge.value))

    def updateGaugeValue(self):
        self.ui.gauge.setValue(self.ui.ActualValueSlider.value())
        self.ui.lcdGaugeValue.display(int(self.ui.gauge.value))
        self.ui.ActualValue.display(int(self.ui.gauge.value))

    # RGBA slider groups -> typed QColor setters on the widget
    def setNeedleColor(self):
        self.ui.gauge.setNeedleColor(QColor(
            self.ui.RedSlider_Needle.value(),
            self.ui.GreenSlider_Needle.value(),
            self.ui.BlueSlider_Needle.value(),
            self.ui.TrancSlider_Needle.value(),
        ))

    def setNeedleColorOnDrag(self):
        self.ui.gauge.setNeedleColorOnDrag(QColor(
            self.ui.RedSlider_NeedleDrag.value(),
            self.ui.GreenSlider_NeedleDrag.value(),
            self.ui.BlueSlider_NeedleDrag.value(),
            self.ui.TrancSlider_NeedleDrag.value(),
        ))

    def setScaleValueColor(self):
        self.ui.gauge.setScaleValueColor(QColor(
            self.ui.RedSlider_Scale.value(),
            self.ui.GreenSlider_Scale.value(),
            self.ui.BlueSlider_Scale.value(),
            self.ui.TrancSlider_Scale.value(),
        ))

    def setDisplayValueColor(self):
        self.ui.gauge.setDisplayValueColor(QColor(
            self.ui.RedSlider_Display.value(),
            self.ui.GreenSlider_Display.value(),
            self.ui.BlueSlider_Display.value(),
            self.ui.TrancSlider_Display.value(),
        ))

    # Show/hide toggles
    def toggleBarGraphMarker(self):
        self.ui.gauge.setEnableBarGraph(self.ui.CB_barGraph.isChecked())

    def toggleValueText(self):
        self.ui.gauge.setEnableValueText(self.ui.CB_ValueText.isChecked())

    def toggleCenterPoint(self):
        self.ui.gauge.setEnableCenterPoint(self.ui.CB_CenterPoint.isChecked())

    def toggleNeedle(self):
        self.ui.gauge.setEnableNeedlePolygon(self.ui.CB_Needle.isChecked())

    def toggleScaleText(self):
        self.ui.gauge.setEnableScaleText(self.ui.CB_ScaleText.isChecked())

    def setEnableScalePolygon(self):
        self.ui.gauge.setEnableScalePolygon(self.ui.CB_ShowBarGraph.isChecked())

    def toggleScaleGrid(self):
        self.ui.gauge.setEnableBigScaleGrid(self.ui.CB_Grid.isChecked())

    def toggleFineScaleGrid(self):
        self.ui.gauge.setEnableFineScaleGrid(self.ui.CB_fineGrid.isChecked())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
