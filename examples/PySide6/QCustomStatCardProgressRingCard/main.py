########################################################################
## QCustomStatCard + QCustomProgressRing + QCustomCard example
##
## A tiny dashboard: KPI stat cards, circular progress rings, and a card
## container wrapping them. Styled from design tokens. Run:
##     python main.py
########################################################################
import sys
from PySide6 import QtCore, QtWidgets

from Custom_Widgets.QCustomStatCard import QCustomStatCard
from Custom_Widgets.QCustomProgressRing import QCustomProgressRing
from Custom_Widgets.QCustomCard import QCustomCard
from Custom_Widgets.JSonStyles.tokens import DesignTokens, applyDesignTokens


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Stat cards / Progress rings / Card")
        central = QtWidgets.QWidget()
        self.setCentralWidget(central)
        root = QtWidgets.QVBoxLayout(central)
        root.setSpacing(14)

        # KPI stat cards
        stats = QtWidgets.QHBoxLayout()
        stats.setSpacing(12)
        for label, value, delta, trend, cap in (
                ("Revenue", "$48.2k", "12.5%", "up", "vs last mo"),
                ("Churn", "2.1%", "0.4%", "down", "vs last mo"),
                ("Sign-ups", "1,204", "0%", "flat", "this week")):
            stats.addWidget(QCustomStatCard(label=label, value=value,
                                            delta=delta, trend=trend, caption=cap))
        root.addLayout(stats)

        # a card wrapping progress rings
        card = QCustomCard(title="Quarterly goals",
                           subtitle="Progress toward Q3 targets")
        rings = QtWidgets.QHBoxLayout()
        rings.setSpacing(20)
        self._rings = []
        for name, target in (("Sales", 72), ("Support", 45), ("Marketing", 90)):
            col = QtWidgets.QVBoxLayout()
            ring = QCustomProgressRing(value=0)
            ring.setMinimumSize(96, 96)
            col.addWidget(ring, 0, QtCore.Qt.AlignHCenter)
            col.addWidget(QtWidgets.QLabel(name), 0, QtCore.Qt.AlignHCenter)
            rings.addLayout(col)
            self._rings.append((ring, target))
        card.addLayout(rings)
        root.addWidget(card)
        root.addStretch(1)

        # animate the rings filling up
        self._tick = 0
        self._timer = QtCore.QTimer(self)
        self._timer.timeout.connect(self._advance)
        self._timer.start(20)

    def _advance(self):
        self._tick += 1
        done = True
        for ring, target in self._rings:
            if ring.value() < target:
                ring.setValue(ring.value() + 1)
                done = False
        if done:
            self._timer.stop()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    tokens = DesignTokens(theme="light")
    app.setStyleSheet("QMainWindow, QWidget { background-color: %s; color: %s; }"
                      % (tokens.role("surface-muted"), tokens.role("on-surface")))
    applyDesignTokens(app, tokens=tokens)

    window = MainWindow()
    window.resize(560, 420)
    window.show()
    sys.exit(app.exec())
