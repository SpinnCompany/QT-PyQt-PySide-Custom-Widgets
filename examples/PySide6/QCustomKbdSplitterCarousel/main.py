########################################################################
## QCustomKbd + QCustomSplitter + QCustomCarousel example
##
## Keyboard-shortcut keycaps, a tokenized splitter, and a slideshow carousel
## with auto-advance. Styled from design tokens. Run:
##     python main.py
########################################################################
import sys
from PySide6 import QtCore, QtWidgets

from Custom_Widgets.QCustomKbd import QCustomKbd
from Custom_Widgets.QCustomSplitter import QCustomSplitter
from Custom_Widgets.QCustomCarousel import QCustomCarousel
from Custom_Widgets.JSonStyles.tokens import applyDesignTokens


def _panel(title, body):
    frame = QtWidgets.QFrame()
    frame.setObjectName("QCustomCard")           # reuse the card surface styling
    lay = QtWidgets.QVBoxLayout(frame)
    lay.setContentsMargins(16, 16, 16, 16)
    t = QtWidgets.QLabel(title)
    t.setObjectName("cardTitle")
    b = QtWidgets.QLabel(body)
    b.setWordWrap(True)
    b.setAlignment(QtCore.Qt.AlignTop)
    lay.addWidget(t)
    lay.addWidget(b, 1)
    return frame


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kbd / Splitter / Carousel")
        central = QtWidgets.QWidget()
        self.setCentralWidget(central)
        root = QtWidgets.QVBoxLayout(central)
        root.setContentsMargins(18, 18, 18, 18)
        root.setSpacing(14)

        # --- keyboard shortcuts row ---
        root.addWidget(QtWidgets.QLabel("Keyboard shortcuts"))
        kbd_row = QtWidgets.QHBoxLayout()
        kbd_row.setSpacing(16)
        for label, keys in (("Command palette", "Ctrl+K"),
                            ("Save all", "Ctrl+Shift+S"),
                            ("Close", "Alt+F4")):
            cell = QtWidgets.QHBoxLayout()
            cell.setSpacing(8)
            cell.addWidget(QtWidgets.QLabel(label))
            cell.addWidget(QCustomKbd(keys))
            kbd_row.addLayout(cell)
        kbd_row.addStretch(1)
        root.addLayout(kbd_row)

        # --- splitter ---
        root.addWidget(QtWidgets.QLabel("Resizable splitter (drag the handles)"))
        splitter = QCustomSplitter(QtCore.Qt.Horizontal)
        splitter.addWidget(_panel("Sidebar", "Navigation, files, and outline live here."))
        splitter.addWidget(_panel("Editor", "The main working area. Drag a handle to resize."))
        splitter.addWidget(_panel("Preview", "Live output / preview pane."))
        splitter.setSizes([160, 320, 220])
        splitter.setMinimumHeight(150)
        root.addWidget(splitter, 1)

        # --- carousel ---
        root.addWidget(QtWidgets.QLabel("Carousel (auto-advances every 2.5s)"))
        carousel = QCustomCarousel()
        for title, body in (
                ("Welcome", "QCustomCarousel shows one slide at a time."),
                ("Navigate", "Use the arrows or click a dot below."),
                ("Automate", "setAutoAdvance(ms) cycles the slides for you.")):
            carousel.addSlide(_panel(title, body))
        carousel.setMinimumHeight(140)
        carousel.setAutoAdvance(2500)
        root.addWidget(carousel, 1)


def main():
    app = QtWidgets.QApplication(sys.argv)
    applyDesignTokens(app, theme="light")
    win = MainWindow()
    win.resize(720, 620)
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
