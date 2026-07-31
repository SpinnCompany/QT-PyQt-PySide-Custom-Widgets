########################################################################
## QCustomMultiSelect example
##
## Four fields: a plain multi-select, a searchable one over a longer list, one
## capped at 3 choices, and one that collapses to "+N" past two chips. Click a
## field to open its popup; click a chip's x to drop just that one.
## Run:
##     python main.py
########################################################################
import sys
from PySide6 import QtWidgets

from Custom_Widgets.QCustomMultiSelect import QCustomMultiSelect
from Custom_Widgets.JSonStyles.tokens import applyDesignTokens

LANGUAGES = ["py=Python", "js=JavaScript", "rs=Rust", "go=Go", "cpp=C++",
             "rb=Ruby", "kt=Kotlin", "swift=Swift", "ts=TypeScript"]


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QCustomMultiSelect")
        central = QtWidgets.QWidget()
        self.setCentralWidget(central)
        layout = QtWidgets.QVBoxLayout(central)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)
        self._theme = "light"

        layout.addWidget(self._heading("Colours"))
        self.colours = QCustomMultiSelect(options=["Red", "Green", "Blue"],
                                          placeholder="Choose colours")
        self.colours.selectionChanged.connect(self._report)
        layout.addWidget(self.colours)

        layout.addWidget(self._heading("Languages (searchable)"))
        self.languages = QCustomMultiSelect(options=LANGUAGES,
                                            placeholder="Search and pick")
        self.languages.searchable = True
        self.languages.selectionChanged.connect(self._report)
        layout.addWidget(self.languages)

        layout.addWidget(self._heading("Pick at most 3"))
        self.capped = QCustomMultiSelect(options=LANGUAGES,
                                         placeholder="Up to three")
        self.capped.maxSelection = 3
        self.capped.selectionChanged.connect(self._report)
        layout.addWidget(self.capped)

        layout.addWidget(self._heading("Collapses past 2 chips"))
        self.collapsed = QCustomMultiSelect(
            options=LANGUAGES, selected=["py", "js", "rs", "go"])
        self.collapsed.maxChips = 2
        layout.addWidget(self.collapsed)

        row = QtWidgets.QHBoxLayout()
        for text, slot in (("Clear colours", self.colours.clearSelection),
                           ("Select all languages",
                            lambda: self.languages.setSelected(
                                [o.split("=")[0] for o in LANGUAGES])),
                           ("Light / dark", self._toggleTheme)):
            btn = QtWidgets.QPushButton(text)
            btn.clicked.connect(slot)
            row.addWidget(btn)
        row.addStretch(1)
        layout.addLayout(row)

        self.status = QtWidgets.QLabel("Nothing selected yet")
        layout.addWidget(self.status)
        layout.addStretch(1)
        self.resize(520, 520)

    @staticmethod
    def _heading(text):
        label = QtWidgets.QLabel(text)
        font = label.font()
        font.setBold(True)
        label.setFont(font)
        return label

    def _report(self, _values):
        parts = []
        for name, field in (("colours", self.colours),
                            ("languages", self.languages),
                            ("capped", self.capped)):
            if field.selected():
                parts.append("%s: %s" % (name, ", ".join(field.selectedLabels())))
        self.status.setText(" | ".join(parts) or "Nothing selected yet")

    def _toggleTheme(self):
        self._theme = "dark" if self._theme == "light" else "light"
        applyDesignTokens(QtWidgets.QApplication.instance(), theme=self._theme)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    applyDesignTokens(app, theme="light")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
