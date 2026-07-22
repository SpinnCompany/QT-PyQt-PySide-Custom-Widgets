########################################################################
## QCustomBadge example
##
## The modern badge: every semantic variant, a live count badge (with a cap),
## a dot indicator, and a count floating over a button's corner. Styled from
## design tokens. Run:
##     python main.py
########################################################################
import sys
from PySide6 import QtCore, QtWidgets

from Custom_Widgets.QCustomBadge import QCustomBadge
from Custom_Widgets.JSonStyles.tokens import DesignTokens, applyDesignTokens


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QCustomBadge")
        central = QtWidgets.QWidget()
        self.setCentralWidget(central)
        root = QtWidgets.QVBoxLayout(central)
        root.setSpacing(16)

        # variants
        root.addWidget(QtWidgets.QLabel("Variants"))
        variants = QtWidgets.QHBoxLayout()
        for v in ("default", "primary", "secondary", "success", "warning",
                  "destructive", "info", "outline"):
            variants.addWidget(QCustomBadge(v.capitalize(), variant=v))
        variants.addStretch(1)
        root.addLayout(variants)

        # sizes + dot
        root.addWidget(QtWidgets.QLabel("Sizes & dot"))
        sizes = QtWidgets.QHBoxLayout()
        for s in ("sm", "md", "lg"):
            b = QCustomBadge(s, variant="primary")
            b.sizeVariant = s
            sizes.addWidget(b)
        for s in ("sm", "md", "lg"):
            d = QCustomBadge(variant="success")
            d.sizeVariant = s
            d.setDot(True)
            sizes.addWidget(d)
        sizes.addStretch(1)
        root.addLayout(sizes)

        # live count
        root.addWidget(QtWidgets.QLabel("Count (click +/- )"))
        countRow = QtWidgets.QHBoxLayout()
        self.count = 3
        self.countBadge = QCustomBadge(variant="destructive")
        self.countBadge.setCount(self.count, maxCount=99)
        minus = QtWidgets.QPushButton("−")
        plus = QtWidgets.QPushButton("+")
        minus.clicked.connect(lambda: self._bump(-1))
        plus.clicked.connect(lambda: self._bump(+1))
        countRow.addWidget(minus)
        countRow.addWidget(self.countBadge)
        countRow.addWidget(plus)
        countRow.addStretch(1)
        root.addLayout(countRow)

        # overlay: a count floating on a button's top-right corner
        root.addWidget(QtWidgets.QLabel("Attached overlay"))
        self.inbox = QtWidgets.QPushButton("  Inbox  ")
        self.inbox.setMinimumHeight(40)
        self.overlay = QCustomBadge(variant="primary")
        self.overlay.setCount(5)
        self.overlay.attachTo(self.inbox, corner="topright", xOffset=-2, yOffset=2)
        row = QtWidgets.QHBoxLayout()
        row.addWidget(self.inbox)
        row.addStretch(1)
        root.addLayout(row)

        root.addStretch(1)

    def _bump(self, delta):
        self.count = max(0, self.count + delta)
        self.countBadge.setCount(self.count, maxCount=99)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    tokens = DesignTokens(theme="light")
    app.setStyleSheet("QMainWindow, QWidget { background-color: %s; color: %s; }"
                      % (tokens.role("surface"), tokens.role("on-surface")))
    applyDesignTokens(app, tokens=tokens)

    window = MainWindow()
    window.resize(560, 380)
    window.show()
    sys.exit(app.exec())
