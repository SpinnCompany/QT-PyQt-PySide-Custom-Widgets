"""QCustomPieChart % callout labels + hatch fills — live preview.

The QtCharts pie already renders labels; here it shows the convenience %-inside
toggle + the new per-slice HATCH fills (indices via setHatchIndices/hatchCsv),
next to a default pie (enhancements off).

Run through the MCP: designer_launch(project=…) then designer_run_app(project=…).
"""
import sys

from qtpy.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel,
                            QHBoxLayout, QVBoxLayout, QFrame)

from Custom_Widgets.QCustomCharts.QCustomPieChart import QCustomPieChart


def card(title, subtitle, chart):
    frame = QFrame(); frame.setObjectName("card")
    lay = QVBoxLayout(frame); lay.setContentsMargins(18, 14, 18, 14); lay.setSpacing(2)
    cap = QLabel(title); cap.setObjectName("cardTitle")
    sub = QLabel(subtitle); sub.setObjectName("cardSub")
    lay.addWidget(cap); lay.addWidget(sub); lay.addSpacing(6)
    lay.addWidget(chart, 1)
    return frame


def pie(data, colors, hatch=None, pattern="bdiag", pct=False, hole=0.0):
    c = QCustomPieChart()
    c.setChartTitle("") if hasattr(c, "setChartTitle") else None
    c._chart.setTitle("")
    c.addSeries("S", data, colors=colors)
    try:
        c.holeSize = hole
    except Exception:
        pass
    if pct:
        c.setShowPercentLabels(True)
    if hatch:
        c.setHatchIndices(hatch)
        c.setHatchPattern(pattern)
    return c


class Preview(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QCustomPieChart — % callouts + hatch")
        self.resize(1020, 560)
        root = QWidget(); self.setCentralWidget(root)
        row = QHBoxLayout(root); row.setContentsMargins(24, 24, 24, 24); row.setSpacing(20)

        data = [("Product", 30), ("Restaurants", 23), ("Media", 18),
                ("Pay", 17), ("Other", 12)]
        cols = ["#8b5cf6", "#c3f53c", "#1f9bff", "#3a4150", "#5b6472"]

        # 1) % labels inside + hatched Pay/Other (bdiag), donut hole
        row.addWidget(card("Transfer history", "% inside + hatched slices",
                           pie(data, cols, hatch=[3, 4], pattern="bdiag",
                               pct=True, hole=0.45)), 1)

        # 2) cross-hatch on one slice, full pie
        row.addWidget(card("Storage", "cross hatch on Other",
                           pie([("Photos", 44), ("Apps", 26), ("Media", 16), ("Free", 14)],
                               ["#3aa0ff", "#7c5cff", "#28c2d1", "#3a4150"],
                               hatch=[3], pattern="cross", pct=True, hole=0.0)), 1)

        # 3) default pie — enhancements OFF
        row.addWidget(card("Default", "enhancements off",
                           pie(data, cols, hole=0.0)), 1)

        self.setStyleSheet("""
            QMainWindow { background: #0e1016; }
            QWidget { color: #e7e9ef; font-family: 'Segoe UI', 'Inter', sans-serif; }
            QFrame#card { background: #171a22; border: 1px solid #232833; border-radius: 18px; }
            QLabel#cardTitle { font-size: 15px; font-weight: 600; color: #f4f6fb; }
            QLabel#cardSub  { font-size: 11px; color: #6b7280; }
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
