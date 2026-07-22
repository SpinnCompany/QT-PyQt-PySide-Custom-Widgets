########################################################################
## QCustomCommandPalette example - press Ctrl+K (Cmd+K on macOS)
##
## A fuzzy-searchable command launcher overlay. Type to filter, arrows to
## navigate, Enter to run, Esc to close. Styled from design tokens. Run:
##     python main.py
########################################################################
import sys
from PySide6 import QtWidgets

from Custom_Widgets.QCustomCommandPalette import QCustomCommandPalette
from Custom_Widgets.QCustomToast import QCustomToast
from Custom_Widgets.JSonStyles.tokens import DesignTokens, applyDesignTokens


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QCustomCommandPalette Example")
        central = QtWidgets.QWidget()
        self.setCentralWidget(central)
        layout = QtWidgets.QVBoxLayout(central)
        layout.addWidget(QtWidgets.QLabel("Press  Ctrl+K  (Cmd+K on macOS)  to open the palette"))
        layout.addStretch(1)

        self.palette = QCustomCommandPalette.installShortcut(self, "Ctrl+K", commands=[
            {"id": "new", "title": "New File", "shortcut": "Ctrl+N",
             "callback": lambda: QCustomToast.success(self, "New file created")},
            {"id": "save", "title": "Save File", "shortcut": "Ctrl+S",
             "callback": lambda: QCustomToast.success(self, "Saved")},
            {"id": "open", "title": "Open Folder", "subtitle": "Browse for a folder",
             "callback": lambda: QCustomToast.info(self, "Open folder")},
            {"id": "theme", "title": "Toggle Dark Theme",
             "callback": lambda: QCustomToast.info(self, "Theme toggled")},
            {"id": "close", "title": "Close Window", "shortcut": "Ctrl+W",
             "callback": lambda: QCustomToast.warning(self, "Close requested")},
        ])


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    tokens = DesignTokens(theme="light")
    app.setStyleSheet("QMainWindow, QWidget { background-color: %s; color: %s; }"
                      % (tokens.role("surface"), tokens.role("on-surface")))
    applyDesignTokens(app, tokens=tokens)

    window = MainWindow()
    window.resize(640, 420)
    window.show()
    sys.exit(app.exec())
