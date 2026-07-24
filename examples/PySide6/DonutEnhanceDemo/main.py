"""QCustomDonut % callouts + hatch fills — live preview.

Shows the opt-in enhancements (segments mode): on-arc % pills + hatched slices
(the "Transfer history" reference), a variant with a cross hatch, and the classic
rings mode untouched (proof the enhancements default OFF).

Run through the MCP: designer_launch(project=…) then designer_run_app(project=…).
"""
import sys

from qtpy.QtCore import Qt
from qtpy.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel, QHBoxLayout,
                            QVBoxLayout, QFrame)

from Custom_Widgets.QCustomDonut import QCustomDonut


def dot(color):
    d = QLabel(); d.setFixedSize(10, 10)
    d.setStyleSheet("background:%s; border-radius:5px;" % color)
    return d


def legend(rows):
    box = QVBoxLayout(); box.setSpacing(6)
    for name, pct, color in rows:
        r = QHBoxLayout(); r.setSpacing(8)
        r.addWidget(dot(color))
        lbl = QLabel(name); lbl.setObjectName("legName")
        val = QLabel("%d%%" % pct); val.setObjectName("legVal")
        r.addWidget(lbl); r.addStretch(1); r.addWidget(val)
        box.addLayout(r)
    box.addStretch(1)
    return box


def card(title, subtitle, donut, legend_rows=None):
    frame = QFrame(); frame.setObjectName("card")
    lay = QVBoxLayout(frame); lay.setContentsMargins(20, 16, 20, 16); lay.setSpacing(2)
    cap = QLabel(title); cap.setObjectName("cardTitle")
    sub = QLabel(subtitle); sub.setObjectName("cardSub")
    lay.addWidget(cap); lay.addWidget(sub); lay.addSpacing(8)
    lay.addWidget(donut, 1)
    if legend_rows:
        lay.addSpacing(6)
        lay.addLayout(legend(legend_rows))
    return frame


class Preview(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QCustomDonut — % callouts + hatch")
        self.resize(1000, 560)
        root = QWidget(); self.setCentralWidget(root)
        row = QHBoxLayout(root); row.setContentsMargins(24, 24, 24, 24); row.setSpacing(20)

        PURPLE, LIME, BLUE, DARK, GRAY = "#8b5cf6", "#c3f53c", "#1f9bff", "#3a4150", "#5b6472"

        # 1) Transfer history — % pills + hatched Pay/Other slices (the reference)
        d1 = QCustomDonut(values=[30, 23, 18, 17, 12])
        d1.setMode("segments")
        d1.setColors([PURPLE, LIME, BLUE, DARK, GRAY])
        d1.gapDegrees = 5
        d1.setShowPercentLabels(True)
        d1.setHatchIndices([3, 4])          # Pay-for-workplace + Other = hatched
        d1.setHatchPattern("bdiag")
        row.addWidget(card("Transfer history", "This month · % on arcs", d1, [
            ("Product", 30, PURPLE), ("Restaurants & bars", 23, LIME),
            ("Internet & media", 18, BLUE), ("Pay for workplace", 17, DARK),
            ("Other", 12, GRAY)]), 1)

        # 2) Storage — % pills + a cross-hatch on one slice, gradient-ish colours
        d2 = QCustomDonut(values=[44, 26, 16, 14])
        d2.setMode("segments")
        d2.setColors(["#3aa0ff", "#7c5cff", "#28c2d1", "#3a4150"])
        d2.gapDegrees = 5
        d2.setShowPercentLabels(True)
        d2.percentPillColor = "#0e1016"
        d2.setHatchIndices([3]); d2.setHatchPattern("cross")
        row.addWidget(card("Storage", "cross hatch on Free", d2, [
            ("Photos", 44, "#3aa0ff"), ("Apps", 26, "#7c5cff"),
            ("Media", 16, "#28c2d1"), ("Free", 14, "#3a4150")]), 1)

        # 3) Classic rings mode — UNCHANGED (enhancements default OFF)
        d3 = QCustomDonut(values=[82, 55, 30])
        d3.setColors(["#7c6cf6", "#f2794b", "#f4c44e"])
        # showPercentLabels left False -> classic look
        row.addWidget(card("Classic (rings)", "enhancements OFF — unchanged", d3), 1)

        self.setStyleSheet("""
            QMainWindow { background: #0e1016; }
            QWidget { color: #e7e9ef; font-family: 'Segoe UI', 'Inter', sans-serif; }
            QFrame#card {
                background: #171a22; border: 1px solid #232833; border-radius: 18px;
            }
            QLabel#cardTitle { font-size: 16px; font-weight: 600; color: #f4f6fb; }
            QLabel#cardSub  { font-size: 11px; color: #6b7280; }
            QLabel#legName  { font-size: 12px; color: #c3c8d2; }
            QLabel#legVal   { font-size: 12px; font-weight: 600; color: #f4f6fb; }
        """)


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
