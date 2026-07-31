"""
Comprehensive widget showcase — demonstrates the complete Custom Widgets library.
Shows form inputs, selections, data visualization, and interactive components.
"""
import sys
from qtpy.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QLabel, QScrollArea, QFrame
)
from qtpy.QtCore import Qt

from Custom_Widgets.QCustomQPushButton import QCustomQPushButton
from Custom_Widgets.QCustomToast import QCustomToast
from Custom_Widgets.QCustomInput import QCustomInput
from Custom_Widgets.QCustomButtonGroup import QCustomButtonGroup
from Custom_Widgets.QCustomComboBox import QCustomComboBox
from Custom_Widgets.QCustomCheckBox import QCustomCheckBox
from Custom_Widgets.QCustomForm import QCustomForm, QCustomFormField
from Custom_Widgets.QCustomCard import QCustomCard
from Custom_Widgets.QCustomBadge import QCustomBadge
from Custom_Widgets.QCustomStatCard import QCustomStatCard
from Custom_Widgets.QCustomAlert import QCustomAlert
from Custom_Widgets.QCustomAccordion import QCustomAccordion
from Custom_Widgets.QCustomSwitch import QCustomSwitch
from Custom_Widgets.QCustomRangeSlider import QCustomRangeSlider
from Custom_Widgets.QCustomProgressRing import QCustomProgressRing
from Custom_Widgets.QCustomRating import QCustomRating
from Custom_Widgets.JSonStyles import loadJsonStyle
from Custom_Widgets.QCustomTheme import QCustomTheme


class WidgetShowcase(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Custom Widgets Showcase — Complete Library")
        self.resize(1200, 800)

        # Setup theme
        self.theme = QCustomTheme()
        self.theme.setTheme("Light")
        loadJsonStyle(self, self.theme)

        # Main container
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(12)

        # Header
        header = QLabel("Custom Widgets — Complete Release Showcase")
        header.setStyleSheet("font-size: 24px; font-weight: 700; margin-bottom: 12px;")
        main_layout.addWidget(header)

        # Theme switcher
        theme_bar = QHBoxLayout()
        theme_label = QLabel("Theme:")
        theme_label.setStyleSheet("font-weight: 500;")
        theme_group = QCustomButtonGroup(exclusive=True, orientation="horizontal")
        theme_group.setButtons(["Light", "Dark"])
        theme_group.setSelectedId(0)
        theme_group.selectionChanged.connect(self._on_theme_changed)
        theme_bar.addWidget(theme_label)
        theme_bar.addWidget(theme_group)
        theme_bar.addStretch()
        main_layout.addLayout(theme_bar)

        # Tabs for different categories
        tabs = QTabWidget()
        tabs.addTab(self._create_inputs_tab(), "Inputs & Forms")
        tabs.addTab(self._create_data_viz_tab(), "Data & Visualization")
        tabs.addTab(self._create_feedback_tab(), "Feedback & Status")
        tabs.addTab(self._create_advanced_tab(), "Advanced Components")
        main_layout.addWidget(tabs)

        self.setCentralWidget(main_widget)

    def _create_inputs_tab(self):
        """Form inputs, buttons, selections."""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(16)

        # Forms section
        forms_label = QLabel("Forms & Validation")
        forms_label.setStyleSheet("font-size: 16px; font-weight: 600;")
        layout.addWidget(forms_label)

        form = QCustomForm(tab)
        
        # Text inputs
        name_input = QCustomInput(tab)
        name_input.setPlaceholderText("Enter your name")
        name_field = QCustomFormField("Name", widget=name_input)
        name_field.set_required(True)
        form.add_field(name_field)

        email_input = QCustomInput(tab)
        email_input.setPlaceholderText("user@example.com")
        email_field = QCustomFormField("Email", widget=email_input)
        email_field.set_validator(lambda v: "@" in v if v else False)
        form.add_field(email_field)

        # Combo
        combo = QCustomComboBox(tab, editable=True)
        combo.setItems(["Option A", "Option B", "Option C"])
        combo_field = QCustomFormField("Selection", widget=combo)
        form.add_field(combo_field)

        layout.addWidget(form)

        # Button group selection
        group_label = QLabel("Selection Buttons")
        group_label.setStyleSheet("font-weight: 500; margin-top: 12px;")
        layout.addWidget(group_label)

        pref_group = QCustomButtonGroup(exclusive=True, orientation="horizontal")
        pref_group.setButtons(["Monthly", "Quarterly", "Annual"])
        pref_group.setSelectedId(0)
        layout.addWidget(pref_group)

        # Checkbox
        check = QCustomCheckBox("I agree to the terms")
        check.setChecked(True)
        layout.addWidget(check)

        # Range slider
        range_label = QLabel("Range Selector")
        range_label.setStyleSheet("font-weight: 500; margin-top: 12px;")
        layout.addWidget(range_label)

        slider = QCustomRangeSlider(tab)
        slider.setRange(0, 100)
        slider.setValues(20, 80)
        layout.addWidget(slider)

        # Switch
        switch_label = QLabel("Toggles")
        switch_label.setStyleSheet("font-weight: 500; margin-top: 12px;")
        layout.addWidget(switch_label)

        switch = QCustomSwitch(tab)
        switch.setChecked(True)
        layout.addWidget(switch)

        layout.addStretch()
        return self._wrap_in_scroll(tab)

    def _create_data_viz_tab(self):
        """Data display and visualization widgets."""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(16)

        # KPI cards
        kpi_label = QLabel("KPI Statistics")
        kpi_label.setStyleSheet("font-size: 16px; font-weight: 600;")
        layout.addWidget(kpi_label)

        kpi_row = QHBoxLayout()
        for title, value, delta, trend in [
            ("Revenue", "$12.5K", "+8.2%", "up"),
            ("Users", "1,234", "+12%", "up"),
            ("Retention", "92%", "-2%", "down"),
        ]:
            card = QCustomStatCard(tab, label=title, value=value, delta=delta, trend=trend)
            kpi_row.addWidget(card)
        layout.addLayout(kpi_row)

        # Progress ring
        progress_label = QLabel("Progress Indicators")
        progress_label.setStyleSheet("font-weight: 500; margin-top: 12px;")
        layout.addWidget(progress_label)

        progress_row = QHBoxLayout()
        for value, label_text in [(65, "CPU"), (42, "Memory"), (88, "Disk")]:
            ring = QCustomProgressRing(tab)
            ring.value = value
            progress_row.addWidget(ring)
        layout.addLayout(progress_row)

        # Rating
        rating_label = QLabel("User Rating")
        rating_label.setStyleSheet("font-weight: 500; margin-top: 12px;")
        layout.addWidget(rating_label)

        rating = QCustomRating(tab)
        rating.value = 4
        layout.addWidget(rating)

        # Badges
        badge_label = QLabel("Status Indicators")
        badge_label.setStyleSheet("font-weight: 500; margin-top: 12px;")
        layout.addWidget(badge_label)

        badge_row = QHBoxLayout()
        for variant, text in [("primary", "Active"), ("success", "Approved"), ("warning", "Pending"), ("danger", "Failed")]:
            badge = QCustomBadge(text, variant=variant)
            badge_row.addWidget(badge)
        layout.addLayout(badge_row)

        layout.addStretch()
        return self._wrap_in_scroll(tab)

    def _create_feedback_tab(self):
        """Feedback, alerts, and notifications."""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(16)

        # Alerts
        alerts_label = QLabel("Alert Messages")
        alerts_label.setStyleSheet("font-size: 16px; font-weight: 600;")
        layout.addWidget(alerts_label)

        for variant, title, msg_text in [
            ("info", "Information", "This is an informational alert."),
            ("success", "Success", "Operation completed successfully."),
            ("warning", "Warning", "Please review this warning carefully."),
            ("destructive", "Error", "An error has occurred."),
        ]:
            alert = QCustomAlert(tab, title=title, text=msg_text, variant=variant)
            layout.addWidget(alert)

        # Toast buttons
        toast_label = QLabel("Notifications (Toast)")
        toast_label.setStyleSheet("font-weight: 500; margin-top: 16px;")
        layout.addWidget(toast_label)

        toast_row = QHBoxLayout()
        for variant, label in [("info", "Info"), ("success", "Success"), ("warning", "Warning"), ("error", "Error")]:
            btn = QCustomQPushButton(tab)
            btn.setText(label)
            btn.variant = "outline"
            btn.sizeVariant = "md"
            btn.clicked.connect(lambda checked=False, v=variant: self._show_toast(v))
            toast_row.addWidget(btn)
        layout.addLayout(toast_row)

        layout.addStretch()
        return self._wrap_in_scroll(tab)

    def _create_advanced_tab(self):
        """Advanced containers and layouts."""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(16)

        # Cards
        card_label = QLabel("Card Containers")
        card_label.setStyleSheet("font-size: 16px; font-weight: 600;")
        layout.addWidget(card_label)

        card = QCustomCard(tab)
        card_layout = QVBoxLayout(card)
        title = QLabel("Feature Card")
        title.setStyleSheet("font-weight: 600; font-size: 14px;")
        desc = QLabel("This demonstrates the QCustomCard container with nested content.")
        card_layout.addWidget(title)
        card_layout.addWidget(desc)
        layout.addWidget(card)

        # Accordion
        accordion_label = QLabel("Collapsible Content")
        accordion_label.setStyleSheet("font-weight: 500; margin-top: 12px;")
        layout.addWidget(accordion_label)

        accordion = QCustomAccordion(tab)
        for i, title_text in enumerate(["Section 1", "Section 2", "Section 3"]):
            section = QWidget()
            section_layout = QVBoxLayout(section)
            section_layout.addWidget(QLabel(f"Content for {title_text}"))
            accordion.addSection(title_text, section)
        layout.addWidget(accordion)

        layout.addStretch()
        return self._wrap_in_scroll(tab)

    def _wrap_in_scroll(self, widget):
        """Wrap a widget in a scroll area."""
        scroll = QScrollArea()
        scroll.setWidget(widget)
        scroll.setWidgetResizable(True)
        return scroll

    def _on_theme_changed(self, bid, text):
        """Switch theme."""
        self.theme.setTheme(text)
        loadJsonStyle(self, self.theme)

    def _show_toast(self, variant):
        """Show a toast notification."""
        messages = {
            "info": ("Information", "This is an info message."),
            "success": ("Success", "Operation completed!"),
            "warning": ("Warning", "Please check this."),
            "error": ("Error", "Something went wrong."),
        }
        title, msg = messages.get(variant, ("Notification", ""))
        getattr(QCustomToast, variant)(self, msg, title=title)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WidgetShowcase()
    window.show()
    sys.exit(app.exec())
