"""
New Widgets Showcase — QCustomInput, QCustomButtonGroup, and modern data viz.
Demonstrates the release-ready input layer plus high-value chart/gauge widgets.
"""
import sys
from qtpy.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QScrollArea, QGridLayout
)
from qtpy.QtCore import Qt

from Custom_Widgets.QCustomInput import QCustomInput
from Custom_Widgets.QCustomButtonGroup import QCustomButtonGroup
from Custom_Widgets.QCustomForm import QCustomForm, QCustomFormField
from Custom_Widgets.QCustomQPushButton import QCustomQPushButton
from Custom_Widgets.QCustomToast import QCustomToast
from Custom_Widgets.QCustomCard import QCustomCard

# Data viz widgets from the release scope
from Custom_Widgets.QCustomRadialGauge import QCustomRadialGauge
from Custom_Widgets.QCustomLiquidGauge import QCustomLiquidGauge
from Custom_Widgets.QCustomHeatmap import QCustomHeatmap
from Custom_Widgets.QCustomWaveform import QCustomWaveform
from Custom_Widgets.QCustomRulerPicker import QCustomRulerPicker
from Custom_Widgets.QCustomStatCard import QCustomStatCard

from Custom_Widgets.JSonStyles import loadJsonStyle
from Custom_Widgets.QCustomTheme import QCustomTheme


class NewWidgetsShowcase(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("New Widgets Release — Input Layer + Data Viz")
        self.resize(1400, 900)

        # Setup theme
        self.theme = QCustomTheme()
        self.theme.setTheme("Light")
        loadJsonStyle(self, self.theme)

        # Main container
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(16)

        # Header
        header = QLabel("Release Ready: New Widgets Showcase")
        header.setStyleSheet("font-size: 26px; font-weight: 700;")
        main_layout.addWidget(header)

        # Split: Input on left, Data viz on right
        split_layout = QHBoxLayout()

        # ===== LEFT: Input Layer =====
        left_scroll = QScrollArea()
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setSpacing(12)

        # Form section
        form_title = QLabel("Form Input Layer")
        form_title.setStyleSheet("font-size: 16px; font-weight: 600;")
        left_layout.addWidget(form_title)

        form = QCustomForm(left_widget)

        # Text inputs with variants
        self._add_input_variant_section(form, left_layout)

        # Button group with variants
        group_title = QLabel("Selection Buttons (Variants)")
        group_title.setStyleSheet("font-weight: 500; margin-top: 12px;")
        left_layout.addWidget(group_title)

        for variant in ["outline", "primary", "secondary"]:
            var_label = QLabel(f"  {variant.title()}:")
            var_label.setStyleSheet("font-size: 11px; color: #666;")
            left_layout.addWidget(var_label)
            
            group = QCustomButtonGroup(exclusive=True, orientation="horizontal")
            group.setButtons(["Option 1", "Option 2", "Option 3"])
            group.variant = variant
            group.setSelectedId(0)
            left_layout.addWidget(group)

        left_layout.addStretch()
        left_scroll.setWidget(left_widget)
        left_scroll.setWidgetResizable(True)
        split_layout.addWidget(left_scroll, 1)

        # ===== RIGHT: Data Visualization =====
        right_scroll = QScrollArea()
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setSpacing(16)

        viz_title = QLabel("Data Visualization Widgets")
        viz_title.setStyleSheet("font-size: 16px; font-weight: 600;")
        right_layout.addWidget(viz_title)

        # Gauge widgets (2x2 grid)
        gauge_section = QLabel("Gauges")
        gauge_section.setStyleSheet("font-weight: 500; margin-top: 8px;")
        right_layout.addWidget(gauge_section)

        gauge_grid = QGridLayout()
        
        # Radial gauge (needle)
        radial = QCustomRadialGauge(right_widget)
        radial.setMaximumHeight(180)
        radial.value = 65
        gauge_grid.addWidget(QLabel("Radial Gauge"), 0, 0)
        gauge_grid.addWidget(radial, 1, 0)

        # Liquid gauge
        liquid = QCustomLiquidGauge(right_widget)
        liquid.setMaximumHeight(180)
        liquid.value = 72
        gauge_grid.addWidget(QLabel("Liquid Gauge"), 0, 1)
        gauge_grid.addWidget(liquid, 1, 1)

        right_layout.addLayout(gauge_grid)

        # Ruler picker
        picker_label = QLabel("Ruler Picker")
        picker_label.setStyleSheet("font-weight: 500; margin-top: 8px;")
        right_layout.addWidget(picker_label)

        ruler = QCustomRulerPicker(right_widget)
        ruler.setMaximumHeight(80)
        ruler.value = 50
        right_layout.addWidget(ruler)

        # Waveform
        waveform_label = QLabel("Waveform")
        waveform_label.setStyleSheet("font-weight: 500; margin-top: 8px;")
        right_layout.addWidget(waveform_label)

        waveform = QCustomWaveform(right_widget)
        waveform.setMaximumHeight(100)
        waveform.setMode("bars")
        waveform.setAnimated(True)
        right_layout.addWidget(waveform)

        # Heatmap
        heatmap_label = QLabel("Heatmap (Activity Grid)")
        heatmap_label.setStyleSheet("font-weight: 500; margin-top: 8px;")
        right_layout.addWidget(heatmap_label)

        heatmap = QCustomHeatmap(right_widget)
        heatmap.setMaximumHeight(120)
        heatmap.mode = "grid"
        heatmap.setData([
            [1, 2, 3, 4, 5],
            [2, 3, 4, 5, 6],
            [3, 4, 5, 6, 7],
        ])
        right_layout.addWidget(heatmap)

        right_layout.addStretch()
        right_scroll.setWidget(right_widget)
        right_scroll.setWidgetResizable(True)
        split_layout.addWidget(right_scroll, 1)

        main_layout.addLayout(split_layout)

        # Bottom action bar
        action_bar = QHBoxLayout()
        action_bar.addStretch()
        
        submit_btn = QCustomQPushButton("Submit Form", sizeVariant="md")
        submit_btn.variant = "primary"
        submit_btn.clicked.connect(lambda: QCustomToast.success(
            self, "Form submitted successfully!", title="Success"
        ))
        action_bar.addWidget(submit_btn)

        main_layout.addLayout(action_bar)

        self.setCentralWidget(main_widget)

    def _add_input_variant_section(self, form, layout):
        """Add input variants to the form."""
        for variant in ["outline", "primary", "secondary"]:
            var_label = QLabel(f"{variant.title()} Variant")
            var_label.setStyleSheet("font-size: 11px; color: #666; margin-top: 4px;")
            layout.addWidget(var_label)

            inp = QCustomInput()
            inp.variant = variant
            inp.sizeVariant = "md"
            inp.setPlaceholderText(f"Enter text ({variant})")
            
            field = QCustomFormField(f"Field ({variant})", widget=inp)
            if variant == "primary":
                field.set_required(True)
            form.add_field(field)

        form.submitted.connect(self._on_form_submit)
        layout.addWidget(form)

    def _on_form_submit(self, payload):
        """Handle form submission."""
        QCustomToast.success(
            self,
            f"Submitted {len(payload)} fields",
            title="Form Valid"
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NewWidgetsShowcase()
    window.show()
    sys.exit(app.exec())
