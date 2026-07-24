"""QCustomCompass — live preview.

A quick showcase (not the full forms pipeline — just a preview of the new widget):
a heading rose (needle rotates), an aircraft-style rotating-card compass, and a
compact map-corner compass. The top one drifts its heading so you can watch it
ease; drag any of them to set the heading.

Run through the MCP: designer_launch(project=…) then designer_run_app(project=…).
"""
import sys

from qtpy.QtCore import Qt, QTimer
from qtpy.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel,
                            QGridLayout, QVBoxLayout, QFrame)

from Custom_Widgets.QCustomCompass import QCustomCompass
from Custom_Widgets.QCustomCompassDial import QCustomCompassDial


def card(title, subtitle, widget):
    frame = QFrame(); frame.setObjectName("card")
    lay = QVBoxLayout(frame); lay.setContentsMargins(20, 16, 20, 16); lay.setSpacing(2)
    cap = QLabel(title); cap.setObjectName("cardTitle")
    sub = QLabel(subtitle); sub.setObjectName("cardSub")
    lay.addWidget(cap); lay.addWidget(sub); lay.addSpacing(8)
    lay.addWidget(widget, 1)
    return frame


class Preview(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QCustomCompass — preview")
        self.resize(880, 560)
        root = QWidget(); self.setCentralWidget(root)
        grid = QGridLayout(root)
        grid.setContentsMargins(24, 24, 24, 24)
        grid.setHorizontalSpacing(20); grid.setVerticalSpacing(20)

        # Heading rose — needle rotates, drifts automatically
        self.rose = QCustomCompass(heading=315)
        grid.addWidget(card("Heading", "Drag or watch it drift", self.rose), 0, 0)

        # Aircraft-style rotating card — needle up, rose spins
        card_c = QCustomCompass(heading=120)
        card_c.rotateBezel = True
        card_c.northColor = "#ffb703"
        grid.addWidget(card("Course (rotating card)", "N stays on the card", card_c), 0, 1)

        # Map-corner mini — compact, no intercardinals
        mini = QCustomCompass(heading=45)
        mini.showIntercardinals = False
        mini.northColor = "#3aa0ff"
        mini.ringColor = "#233043"
        grid.addWidget(card("Map heading", "NE · compact", mini), 1, 0)

        # Premium beveled instrument dial (the Haulix look) — drifts too
        self.dial = QCustomCompassDial(heading=315)
        grid.addWidget(card("Vehicle heading (dial)", "Premium beveled", self.dial), 1, 1)

        self.setStyleSheet("""
            QMainWindow { background: #0e1016; }
            QWidget { color: #e7e9ef; font-family: 'Segoe UI', 'Inter', sans-serif; }
            QFrame#card {
                background: #171a22; border: 1px solid #232833; border-radius: 18px;
            }
            QLabel#cardTitle { font-size: 16px; font-weight: 600; color: #f4f6fb; }
            QLabel#cardSub  { font-size: 11px; color: #6b7280; }
        """)

        # drift the first compass so the ease animation is visible
        self._steps = [30, 75, 130, 210, 300, 350, 20, 315]
        self._i = 0
        self._drift = QTimer(self); self._drift.setInterval(2200)
        self._drift.timeout.connect(self._next); self._drift.start()

    def _next(self):
        h = self._steps[self._i % len(self._steps)]
        self.rose.setHeading(h)
        self.dial.setHeading((h + 90) % 360)
        self._i += 1


def main():
    app = QApplication.instance() or QApplication(sys.argv)
    win = Preview()
    win.show()
    try:
        from Custom_Widgets.AppControl import maybe_start_app_control
        maybe_start_app_control()
    except Exception:
        pass
    app.exec()


if __name__ == "__main__":
    main()
