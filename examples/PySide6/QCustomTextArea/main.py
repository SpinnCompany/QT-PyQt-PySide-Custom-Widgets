########################################################################
## QCustomTextArea example
##
## Four fields showing what the stock QPlainTextEdit does not give you: a
## character limit with a live counter, auto-grow between a row range, the
## error state, and the size variants. Includes a live light/dark toggle.
## Run:
##     python main.py
########################################################################
import sys
from PySide6 import QtWidgets

from Custom_Widgets.QCustomTextArea import QCustomTextArea
from Custom_Widgets.JSonStyles.tokens import applyDesignTokens


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QCustomTextArea")
        central = QtWidgets.QWidget()
        self.setCentralWidget(central)
        layout = QtWidgets.QVBoxLayout(central)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)
        self._theme = "light"

        # -- counted field --------------------------------------------------
        layout.addWidget(self._heading("Bio (limited to 140 characters)"))
        self.bio = QCustomTextArea(placeholder="Tell people about yourself...",
                                   maxLength=140)
        self.bio.showCounter = True
        self.bio.minRows = 3
        self.bio.limitReached.connect(
            lambda _: self.status.setText("Bio is at the 140 character limit"))
        self.bio.lengthChanged.connect(
            lambda n: self.status.setText("Bio: %d/140" % n))
        layout.addWidget(self.bio)

        # -- auto-growing field ---------------------------------------------
        layout.addWidget(self._heading("Message (grows from 2 to 6 rows)"))
        self.message = QCustomTextArea(placeholder="Type several lines...")
        self.message.minRows = 2
        self.message.maxRows = 6
        self.message.autoGrow = True
        layout.addWidget(self.message)

        # -- error state ----------------------------------------------------
        layout.addWidget(self._heading("Notes (validated on demand)"))
        self.notes = QCustomTextArea(placeholder="At least 10 characters")
        self.notes.minRows = 2
        layout.addWidget(self.notes)

        row = QtWidgets.QHBoxLayout()
        validate = QtWidgets.QPushButton("Validate notes")
        validate.clicked.connect(self._validate)
        row.addWidget(validate)
        for label in ("sm", "md", "lg"):
            btn = QtWidgets.QPushButton("size %s" % label)
            btn.clicked.connect(lambda _=False, v=label: self._setSize(v))
            row.addWidget(btn)
        theme = QtWidgets.QPushButton("Light / dark")
        theme.clicked.connect(self._toggleTheme)
        row.addWidget(theme)
        row.addStretch(1)
        layout.addLayout(row)

        self.status = QtWidgets.QLabel("Bio: 0/140")
        layout.addWidget(self.status)
        layout.addStretch(1)
        self.resize(520, 640)

    @staticmethod
    def _heading(text):
        label = QtWidgets.QLabel(text)
        font = label.font()
        font.setBold(True)
        label.setFont(font)
        return label

    def _validate(self):
        if self.notes.length() < 10:
            self.notes.setError("Notes must be at least 10 characters")
            self.status.setText("Notes rejected (%d chars)" % self.notes.length())
        else:
            self.notes.setError(None)
            self.status.setText("Notes accepted")

    def _setSize(self, variant):
        for field in (self.bio, self.message, self.notes):
            field.sizeVariant = variant

    def _toggleTheme(self):
        self._theme = "dark" if self._theme == "light" else "light"
        applyDesignTokens(QtWidgets.QApplication.instance(), theme=self._theme)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    applyDesignTokens(app, theme="light")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
