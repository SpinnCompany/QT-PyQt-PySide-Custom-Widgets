########################################################################
## QCustomSkeleton + QCustomAvatarGroup + QCustomTimeline example
##
## A skeleton loading card that swaps to real content after 1.5s, an avatar
## group with overflow, and an event timeline. Styled from design tokens. Run:
##     python main.py
########################################################################
import sys
from PySide6 import QtWidgets
from PySide6.QtCore import QTimer

from Custom_Widgets.QCustomSkeleton import QCustomSkeleton
from Custom_Widgets.QCustomAvatarGroup import QCustomAvatarGroup
from Custom_Widgets.QCustomTimeline import QCustomTimeline
from Custom_Widgets.JSonStyles.tokens import DesignTokens, applyDesignTokens


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Skeleton / Avatars / Timeline")
        central = QtWidgets.QWidget()
        self.setCentralWidget(central)
        layout = QtWidgets.QVBoxLayout(central)

        # skeleton -> content
        layout.addWidget(QtWidgets.QLabel("Loading card (swaps after 1.5s):"))
        self.card = QtWidgets.QWidget()
        cardLay = QtWidgets.QHBoxLayout(self.card)
        self.circ = QCustomSkeleton(shape="circle")
        lines = QtWidgets.QVBoxLayout()
        self.l1 = QCustomSkeleton(shape="line")
        self.l2 = QCustomSkeleton(shape="line")
        lines.addWidget(self.l1); lines.addWidget(self.l2); lines.addStretch(1)
        cardLay.addWidget(self.circ); cardLay.addLayout(lines, 1)
        layout.addWidget(self.card)
        QTimer.singleShot(1500, self._loaded)

        # avatars
        layout.addWidget(QtWidgets.QLabel("Team:"))
        avatars = QCustomAvatarGroup(maxVisible=4)
        avatars.setAvatars(["Ada Lovelace", "Alan Turing", "Grace Hopper",
                            "Linus Torvalds", "Ken Thompson", "Margaret Hamilton"])
        arow = QtWidgets.QHBoxLayout(); arow.addWidget(avatars); arow.addStretch(1)
        layout.addLayout(arow)

        # timeline
        layout.addWidget(QtWidgets.QLabel("Activity:"))
        tl = QCustomTimeline()
        tl.setItems([
            {"title": "Ticket created", "time": "09:00", "description": "Reported by a user."},
            {"title": "Assigned", "time": "09:20"},
            {"title": "Resolved", "time": "14:05", "description": "Fix shipped in v3."},
        ])
        layout.addWidget(tl, 1)

    def _loaded(self):
        for s in (self.circ, self.l1, self.l2):
            s.stop()
        self.card.setParent(None)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    tokens = DesignTokens(theme="light")
    app.setStyleSheet("QMainWindow, QWidget { background-color: %s; color: %s; }"
                      % (tokens.role("surface"), tokens.role("on-surface")))
    applyDesignTokens(app, tokens=tokens)

    window = MainWindow()
    window.resize(480, 520)
    window.show()
    sys.exit(app.exec())
