########################################################################
## QCustomRichTextEditor + QCustomColorPicker example
##
## A rich-text editor and a colour picker whose choice tints a preview.
## Styled from design tokens. Run:
##     python main.py
########################################################################
import sys
from PySide6 import QtWidgets

from Custom_Widgets.QCustomRichTextEditor import QCustomRichTextEditor
from Custom_Widgets.QCustomColorPicker import QCustomColorPicker
from Custom_Widgets.JSonStyles.tokens import DesignTokens, applyDesignTokens


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Rich Text + Colour Picker")
        central = QtWidgets.QWidget()
        self.setCentralWidget(central)
        layout = QtWidgets.QVBoxLayout(central)

        self.editor = QCustomRichTextEditor()
        self.editor.setHtml("<h2>Release notes</h2>"
                            "<p>Type here. Use the toolbar for <b>bold</b>, "
                            "<i>italics</i>, headings and lists.</p>")
        layout.addWidget(self.editor, 1)

        row = QtWidgets.QHBoxLayout()
        row.addWidget(QtWidgets.QLabel("Accent colour:"))
        self.picker = QCustomColorPicker(color="#22c55e")
        self.preview = QtWidgets.QLabel("  Preview  ")
        self._tint(self.picker.color())
        self.picker.colorChanged.connect(self._tint)
        row.addWidget(self.picker)
        row.addWidget(self.preview)
        row.addStretch(1)
        layout.addLayout(row)

    def _tint(self, color):
        self.preview.setStyleSheet(
            "background-color: %s; color: white; padding: 6px; border-radius: 6px;"
            % color.name())


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    tokens = DesignTokens(theme="light")
    app.setStyleSheet("QMainWindow, QWidget { background-color: %s; color: %s; }"
                      % (tokens.role("surface"), tokens.role("on-surface")))
    applyDesignTokens(app, tokens=tokens)

    window = MainWindow()
    window.resize(560, 460)
    window.show()
    sys.exit(app.exec())
