import sys
from qtpy.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QHBoxLayout
from Custom_Widgets.QCustomQPushButton import QCustomQPushButton
from Custom_Widgets.QCustomToast import QCustomToast
from Custom_Widgets.QCustomForm import QCustomForm, QCustomFormField
from Custom_Widgets.QCustomComboBox import QCustomComboBox
from Custom_Widgets.QCustomInput import QCustomInput
from Custom_Widgets.QCustomButtonGroup import QCustomButtonGroup
from Custom_Widgets.JSonStyles import loadJsonStyle
from Custom_Widgets.QCustomTheme import QCustomTheme


class ReleaseStarterWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Custom Widgets Release Starter")
        self.resize(760, 520)

        self.theme = QCustomTheme()
        self.theme.setTheme("Light")
        loadJsonStyle(self, self.theme)

        layout = QVBoxLayout(self)
        title = QLabel("Release-ready starter app")
        title.setStyleSheet("font-size: 20px; font-weight: 600;")
        layout.addWidget(title)

        form = QCustomForm(self)
        
        # Name field using QCustomInput
        name_input = QCustomInput(self)
        name_input.setPlaceholderText("Enter your name")
        name_input.variant = "outline"
        name_input.sizeVariant = "md"
        name_field = QCustomFormField("Name", widget=name_input)
        name_field.set_required(True)
        form.add_field(name_field)

        # Email field using QCustomInput
        email_input = QCustomInput(self)
        email_input.setPlaceholderText("Enter your email")
        email_input.variant = "outline"
        email_field = QCustomFormField("Email", widget=email_input)
        email_field.set_validator(lambda value: "@" in value)
        form.add_field(email_field)

        # Region selection
        region = QCustomComboBox(self, editable=True)
        region.setPlaceholderText("Choose a region")
        region.setItems(["North America", "Europe", "Asia Pacific", "Latin America"])
        region.setCurrentIndex(0)
        region_field = QCustomFormField("Region", widget=region)
        form.add_field(region_field)

        # Preference buttons using QCustomButtonGroup
        pref_label = QLabel("Preference")
        pref_label.setStyleSheet("font-weight: 500; margin-top: 8px;")
        layout.addWidget(pref_label)
        
        prefs = QCustomButtonGroup(self, exclusive=True, orientation="horizontal")
        prefs.setButtons(["Light Mode", "Dark Mode", "Auto"])
        prefs.setSelectedId(2)
        layout.addWidget(prefs)

        form.submitted.connect(self._handle_submit)
        layout.addWidget(form)

        button = QCustomQPushButton("Submit sample")
        button.clicked.connect(lambda: QCustomToast.success(self, "Starter app ready", title="Success"))
        layout.addWidget(button)

    def _handle_submit(self, payload):
        QCustomToast.success(self, f"Submitted {payload['Name']}", title="Form")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ReleaseStarterWindow()
    window.show()
    sys.exit(app.exec())
