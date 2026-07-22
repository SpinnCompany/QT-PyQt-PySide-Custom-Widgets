########################################################################
## QCustomBreadcrumbs + QCustomRating + QCustomChip example
##
## A breadcrumb trail, a star rating, and removable + filter chips.
## Styled from design tokens. Run:
##     python main.py
########################################################################
import sys
from PySide6 import QtWidgets

from Custom_Widgets.QCustomBreadcrumbs import QCustomBreadcrumbs
from Custom_Widgets.QCustomRating import QCustomRating
from Custom_Widgets.QCustomChip import QCustomChipGroup
from Custom_Widgets.JSonStyles.tokens import DesignTokens, applyDesignTokens


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Breadcrumbs / Rating / Chips")
        central = QtWidgets.QWidget()
        self.setCentralWidget(central)
        form = QtWidgets.QVBoxLayout(central)

        crumbs = QCustomBreadcrumbs()
        crumbs.setItems([("Home", "/"), ("Library", "/lib"), ("Widgets", "/lib/widgets"),
                         "Rating"])
        crumbs.itemClicked.connect(lambda i, d: self.status.setText("Go to: %s" % d))
        form.addWidget(crumbs)

        rating = QCustomRating(maximum=5)
        rating.setValue(3)
        rating.valueChanged.connect(lambda v: self.status.setText("Rated %d/5" % v))
        rrow = QtWidgets.QHBoxLayout()
        rrow.addWidget(QtWidgets.QLabel("Rate:"))
        rrow.addWidget(rating)
        rrow.addStretch(1)
        form.addLayout(rrow)

        form.addWidget(QtWidgets.QLabel("Removable tags:"))
        tags = QCustomChipGroup(closable=True)
        tags.setChips(["python", "pyside6", "qt", "widgets", "tokens"])
        form.addWidget(tags)

        form.addWidget(QtWidgets.QLabel("Filter (multi-select):"))
        filters = QCustomChipGroup(selectable=True, exclusive=False)
        filters.setChips(["All", "Free", "Pro", "New"])
        filters.selectionChanged.connect(
            lambda sel: self.status.setText("Filters: %s" % (", ".join(map(str, sel)) or "none")))
        form.addWidget(filters)

        self.status = QtWidgets.QLabel("-")
        form.addStretch(1)
        form.addWidget(self.status)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    tokens = DesignTokens(theme="light")
    app.setStyleSheet("QMainWindow, QWidget { background-color: %s; color: %s; }"
                      % (tokens.role("surface"), tokens.role("on-surface")))
    applyDesignTokens(app, tokens=tokens)

    window = MainWindow()
    window.resize(480, 420)
    window.show()
    sys.exit(app.exec())
