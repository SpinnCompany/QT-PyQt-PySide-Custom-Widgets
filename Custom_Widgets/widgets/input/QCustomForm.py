from qtpy.QtCore import Qt, Signal, QObject
from qtpy.QtWidgets import QWidget, QFormLayout, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QPushButton


class QCustomFormField(QObject):
    """Simple form field with required-state and validator support."""

    def __init__(self, label, parent=None, widget=None):
        super().__init__(parent)
        self.label = label
        self._required = False
        self._validator = None
        self._value = ""
        self._error_text = ""
        self._is_valid = True
        if widget is None:
            widget = QLineEdit()
        self.widget = widget
        if hasattr(self.widget, "setPlaceholderText"):
            self.widget.setPlaceholderText(label)

    def set_required(self, required):
        self._required = bool(required)

    def set_validator(self, validator):
        self._validator = validator

    def set_value(self, value):
        self._value = value
        if self.widget is not None:
            if hasattr(self.widget, "setText"):
                self.widget.setText(str(value))

    def value(self):
        if self.widget is not None:
            if hasattr(self.widget, "text"):
                self._value = self.widget.text()
            elif hasattr(self.widget, "currentText"):
                self._value = self.widget.currentText()
        return self._value

    def validate(self):
        self._error_text = ""
        self._is_valid = True
        value = self.value()
        if self._required and not str(value).strip():
            self._error_text = f"{self.label} is required"
            self._is_valid = False
            return False
        if self._validator is not None:
            try:
                ok = bool(self._validator(value))
            except Exception:
                ok = False
            if not ok:
                self._error_text = f"{self.label} is invalid"
                self._is_valid = False
                return False
        return True

    @property
    def error_text(self):
        return self._error_text

    @property
    def is_valid(self):
        return self._is_valid


class QCustomForm(QWidget):
    """Minimal form container with validation and submit signals."""

    submitted = Signal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._fields = []
        self._layout = QVBoxLayout(self)
        self._form_layout = QFormLayout()
        self._layout.addLayout(self._form_layout)

        self._actions = QHBoxLayout()
        self._submit_button = QPushButton("Submit")
        self._submit_button.clicked.connect(self.submit)
        self._actions.addStretch(1)
        self._actions.addWidget(self._submit_button)
        self._layout.addLayout(self._actions)

    def add_field(self, field):
        self._fields.append(field)
        self._form_layout.addRow(field.label, field.widget)
        return field

    def validate(self):
        errors = {}
        for field in self._fields:
            if not field.validate():
                errors[field.label] = field.error_text
        return len(errors) == 0

    def errors(self):
        out = {}
        for field in self._fields:
            if not field.validate():
                out[field.label] = field.error_text
        return out

    def submit(self):
        if not self.validate():
            return False
        payload = {field.label: field.value() for field in self._fields}
        self.submitted.emit(payload)
        return True
