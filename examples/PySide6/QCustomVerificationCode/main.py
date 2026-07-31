########################################################################
## QCustomVerificationCode example
##
## A confirm-your-email screen: a 6-digit numeric code that validates on
## completion, plus a masked alphanumeric variant and a grouped 3+3 layout.
## Try pasting "123 456" into any of them - the formatting is ignored.
## Run:
##     python main.py
########################################################################
import sys
from PySide6 import QtWidgets

from Custom_Widgets.QCustomVerificationCode import QCustomVerificationCode
from Custom_Widgets.JSonStyles.tokens import applyDesignTokens

EXPECTED = "123456"


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QCustomVerificationCode")
        central = QtWidgets.QWidget()
        self.setCentralWidget(central)
        layout = QtWidgets.QVBoxLayout(central)
        layout.setContentsMargins(28, 28, 28, 28)
        layout.setSpacing(18)
        self._theme = "light"

        layout.addWidget(self._heading("Enter the 6-digit code we emailed you"))
        hint = QtWidgets.QLabel("(the demo accepts %s)" % EXPECTED)
        layout.addWidget(hint)

        self.code = QCustomVerificationCode(digits=6)
        self.code.completed.connect(self._onCompleted)
        self.code.codeChanged.connect(self._onChanged)
        layout.addWidget(self.code)

        layout.addWidget(self._heading("Grouped 3 + 3"))
        grouped = QCustomVerificationCode(digits=6)
        grouped.separatorAfter = 3
        layout.addWidget(grouped)

        layout.addWidget(self._heading("Masked, alphanumeric, 8 characters"))
        masked = QCustomVerificationCode(digits=8, inputMode="alphanumeric")
        masked.masked = True
        masked.boxWidth = 34
        layout.addWidget(masked)

        row = QtWidgets.QHBoxLayout()
        for text, slot in (("Clear", lambda: self.code.clear()),
                           ("Paste '123 456'", self._pasteFormatted),
                           ("Light / dark", self._toggleTheme)):
            btn = QtWidgets.QPushButton(text)
            btn.clicked.connect(slot)
            row.addWidget(btn)
        row.addStretch(1)
        layout.addLayout(row)

        self.status = QtWidgets.QLabel("Waiting for a code...")
        layout.addWidget(self.status)
        layout.addStretch(1)
        self.resize(460, 480)

    @staticmethod
    def _heading(text):
        label = QtWidgets.QLabel(text)
        font = label.font()
        font.setBold(True)
        label.setFont(font)
        return label

    def _onChanged(self, code):
        if self.code.state == "error" and len(code) < 6:
            self.code.state = "default"
        self.status.setText("Entered %d/6" % len(code))

    def _onCompleted(self, code):
        if code == EXPECTED:
            self.code.state = "default"
            self.status.setText("Code accepted")
        else:
            self.code.state = "error"
            self.status.setText("That code is not correct")

    def _pasteFormatted(self):
        # Demonstrates that separators and spaces are stripped on the way in.
        self.code.setCodeText("123 456")

    def _toggleTheme(self):
        self._theme = "dark" if self._theme == "light" else "light"
        applyDesignTokens(QtWidgets.QApplication.instance(), theme=self._theme)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    applyDesignTokens(app, theme="light")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
