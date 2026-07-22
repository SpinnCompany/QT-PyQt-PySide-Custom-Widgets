########################################################################
## QCustomComboBox - searchable / autocomplete select example
##
## Type to filter (substring), or click the arrow for the full list.
## Styled from design tokens. Run:
##     python main.py
########################################################################
import sys
from PySide6 import QtWidgets

from Custom_Widgets.QCustomComboBox import QCustomComboBox
from Custom_Widgets.JSonStyles.tokens import DesignTokens, applyDesignTokens

COUNTRIES = ["Kenya", "Nigeria", "Ghana", "South Africa", "Tanzania", "Uganda",
             "Egypt", "Morocco", "Ethiopia", "India", "Indonesia", "Brazil",
             "United States", "Germany", "France", "Japan", "Canada", "Mexico"]


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QCustomComboBox Example")
        central = QtWidgets.QWidget()
        self.setCentralWidget(central)
        form = QtWidgets.QFormLayout(central)

        self.search = QCustomComboBox(editable=True)
        self.search.setItems(COUNTRIES)
        self.search.setPlaceholderText("Type to search a country...")

        self.picker = QCustomComboBox(editable=False)
        self.picker.setItems([(c, i) for i, c in enumerate(COUNTRIES)])

        self.result = QtWidgets.QLabel("-")
        self.search.currentTextChanged.connect(
            lambda t: self.result.setText("Search: %s" % t))
        self.picker.currentIndexChanged.connect(
            lambda i: self.result.setText("Picked #%s = %s"
                                          % (self.picker.currentData(),
                                             self.picker.currentText())))

        form.addRow("Autocomplete:", self.search)
        form.addRow("Select:", self.picker)
        form.addRow("Result:", self.result)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    tokens = DesignTokens(theme="light")
    app.setStyleSheet("QMainWindow, QWidget { background-color: %s; color: %s; }"
                      % (tokens.role("surface"), tokens.role("on-surface")))
    applyDesignTokens(app, tokens=tokens)

    window = MainWindow()
    window.resize(420, 200)
    window.show()
    sys.exit(app.exec())
