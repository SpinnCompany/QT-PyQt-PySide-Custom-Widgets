########################################################################
## QCustomEmptyState + QCustomFileDropZone + QCustomRangeSlider example
##
## An empty-state with an action, a file dropzone, and a price range slider.
## Styled from design tokens. Run:
##     python main.py
########################################################################
import sys
from PySide6 import QtWidgets

from Custom_Widgets.QCustomEmptyState import QCustomEmptyState
from Custom_Widgets.QCustomFileDropZone import QCustomFileDropZone
from Custom_Widgets.QCustomRangeSlider import QCustomRangeSlider
from Custom_Widgets.JSonStyles.tokens import DesignTokens, applyDesignTokens


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Empty state / Dropzone / Range")
        central = QtWidgets.QWidget()
        self.setCentralWidget(central)
        layout = QtWidgets.QVBoxLayout(central)

        empty = QCustomEmptyState(title="No files yet",
                                  description="Drop some below to get started.")
        empty.setActionText("Learn more")
        empty.actionClicked.connect(lambda: self.status.setText("Action clicked"))
        layout.addWidget(empty)

        self.zone = QCustomFileDropZone(extensions=[".png", ".jpg", ".pdf"])
        self.zone.setMinimumHeight(110)
        self.zone.filesChanged.connect(
            lambda fs: self.status.setText("%d file(s)" % len(fs)))
        layout.addWidget(self.zone)

        layout.addWidget(QtWidgets.QLabel("Price range:"))
        self.range = QCustomRangeSlider(minimum=0, maximum=1000)
        self.range.setValues(200, 750)
        self.rangeLbl = QtWidgets.QLabel("$200 - $750")
        self.range.valuesChanged.connect(
            lambda lo, hi: self.rangeLbl.setText("$%d - $%d" % (lo, hi)))
        rr = QtWidgets.QHBoxLayout()
        rr.addWidget(self.range, 1); rr.addWidget(self.rangeLbl)
        layout.addLayout(rr)

        self.status = QtWidgets.QLabel("-")
        layout.addWidget(self.status)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    tokens = DesignTokens(theme="light")
    app.setStyleSheet("QMainWindow, QWidget { background-color: %s; color: %s; }"
                      % (tokens.role("surface"), tokens.role("on-surface")))
    applyDesignTokens(app, tokens=tokens)

    window = MainWindow()
    window.resize(440, 480)
    window.show()
    sys.exit(app.exec())
