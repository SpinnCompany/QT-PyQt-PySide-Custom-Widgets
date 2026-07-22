########################################################################
## QCustomTabWidget + QCustomAccordion example
##
## A tabbed container (switch the tab style live) and a collapsible
## accordion. Styled from design tokens. Run:
##     python main.py
########################################################################
import sys
from PySide6 import QtWidgets

from Custom_Widgets.QCustomTabWidget import QCustomTabWidget
from Custom_Widgets.QCustomAccordion import QCustomAccordion
from Custom_Widgets.QCustomComboBox import QCustomComboBox
from Custom_Widgets.JSonStyles.tokens import DesignTokens, applyDesignTokens


def _page(text):
    w = QtWidgets.QWidget()
    lay = QtWidgets.QVBoxLayout(w)
    lay.addWidget(QtWidgets.QLabel(text))
    lay.addStretch(1)
    return w


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QCustomTabWidget + QCustomAccordion")
        central = QtWidgets.QWidget()
        self.setCentralWidget(central)
        layout = QtWidgets.QVBoxLayout(central)

        # tab style switcher
        top = QtWidgets.QHBoxLayout()
        self.styleBox = QCustomComboBox(editable=False)
        self.styleBox.setItems(["underline", "pills", "enclosed"])
        self.styleBox.currentTextChanged.connect(self._setTabStyle)
        top.addWidget(QtWidgets.QLabel("Tab style:"))
        top.addWidget(self.styleBox)
        top.addStretch(1)
        layout.addLayout(top)

        self.tabs = QCustomTabWidget()
        self.tabs.addTab(_page("Profile settings go here."), "Profile")
        self.tabs.addTab(_page("Account settings go here."), "Account")
        self.tabs.addTab(_page("Notification settings go here."), "Notifications")
        layout.addWidget(self.tabs)

        acc = QCustomAccordion(exclusive=True)
        acc.addSection("What is this?", QtWidgets.QLabel("A collapsible accordion."))
        acc.addSection("How does it work?", QtWidgets.QLabel("Click a header to expand."))
        acc.addSection("Is it exclusive?", QtWidgets.QLabel("Yes - only one open at a time."))
        acc.setExpanded(0, True)
        layout.addWidget(acc)

    def _setTabStyle(self, style):
        self.tabs.tabStyle = style


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    tokens = DesignTokens(theme="light")
    app.setStyleSheet("QMainWindow, QWidget { background-color: %s; color: %s; }"
                      % (tokens.role("surface"), tokens.role("on-surface")))
    applyDesignTokens(app, tokens=tokens)

    window = MainWindow()
    window.resize(520, 480)
    window.show()
    sys.exit(app.exec())
