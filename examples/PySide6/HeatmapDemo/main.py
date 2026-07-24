"""QCustomHeatmap — live preview.

A quick showcase (not the full forms pipeline — just a preview of the new widget):
a grid "Activity by time" heatmap, a GitHub-style contributions calendar, and a
second grid with a different ramp/labels — showing grid + calendar modes, the
colour ramp, labels, legend and flex sizing.

Run through the MCP: designer_launch(project=…) then designer_run_app(project=…).
"""
import sys
import itertools

from qtpy.QtCore import Qt
from qtpy.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel,
                            QGridLayout, QVBoxLayout, QFrame)

from Custom_Widgets.QCustomHeatmap import QCustomHeatmap


def card(title, widget, subtitle="Last 30 days"):
    frame = QFrame()
    frame.setObjectName("card")
    lay = QVBoxLayout(frame)
    lay.setContentsMargins(20, 18, 20, 18)
    lay.setSpacing(2)
    cap = QLabel(title); cap.setObjectName("cardTitle")
    sub = QLabel(subtitle); sub.setObjectName("cardSub")
    lay.addWidget(cap)
    lay.addWidget(sub)
    lay.addSpacing(8)
    lay.addWidget(widget, 1)
    return frame


def _cycle(seq, n):
    it = itertools.cycle(seq)
    return [float(next(it)) for _ in range(n)]


class Preview(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QCustomHeatmap — preview")
        self.resize(1040, 640)
        root = QWidget()
        self.setCentralWidget(root)
        grid = QGridLayout(root)
        grid.setContentsMargins(24, 24, 24, 24)
        grid.setHorizontalSpacing(20)
        grid.setVerticalSpacing(20)

        # 1) Activity by time — grid mode, purple ramp (the Loud reference)
        activity = QCustomHeatmap()
        activity.setValues([_cycle([3, 8, 2, 6, 9, 1, 4, 7, 5][i % 9:] +
                                    [3, 8, 2, 6, 9, 1, 4, 7, 5][:i % 9], 7)
                            for i in range(6)])
        activity.setColors("#1e1b3a", "#b3a4ff", empty="#17152b")
        activity.setLabels(row_labels=["1pm", "2pm", "3pm", "4pm", "5pm", "6pm"],
                           col_labels=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])
        grid.addWidget(card("Activity by time", activity, "This week"), 0, 0)

        # 2) Contributions — calendar mode, green ramp (GitHub-style)
        cal = QCustomHeatmap(mode="calendar",
                             values=_cycle([0, 1, 0, 2, 4, 1, 3, 0, 5, 2, 6, 1,
                                            0, 3, 4, 2, 0, 1, 5, 3], 7 * 20))
        cal.setColors("#161b22", "#39d353", empty="#161b22")
        cal.showLabels = False
        grid.addWidget(card("Contributions", cal, "Last 20 weeks"), 0, 1)

        # 3) Server load by hour — grid mode, teal ramp, different labels (flex)
        load = QCustomHeatmap()
        load.setValues([_cycle([2, 5, 9, 7, 3, 6, 8, 4][i % 8:] +
                                [2, 5, 9, 7, 3, 6, 8, 4][:i % 8], 7) for i in range(8)])
        load.setColors("#0f2230", "#28d1c4", empty="#0e1a22")
        load.setLabels(row_labels=["00h", "03h", "06h", "09h", "12h", "15h", "18h", "21h"],
                       col_labels=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])
        grid.addWidget(card("Server load by hour", load, "Avg req/s"), 1, 0, 1, 2)

        self.setStyleSheet("""
            QMainWindow { background: #0e1016; }
            QWidget { color: #e7e9ef; font-family: 'Segoe UI', 'Inter', sans-serif; }
            QFrame#card {
                background: #171a22; border: 1px solid #232833; border-radius: 18px;
            }
            QLabel#cardTitle { font-size: 16px; font-weight: 600; color: #f4f6fb; }
            QLabel#cardSub  { font-size: 11px; color: #6b7280; }
        """)


def main():
    app = QApplication.instance() or QApplication(sys.argv)
    win = Preview()
    win.show()
    # enable the MCP in-app control server (app_screenshot) when run under the dev
    # server — no-op otherwise. Harness only, not part of the widget.
    try:
        from Custom_Widgets.AppControl import maybe_start_app_control
        maybe_start_app_control()
    except Exception:
        pass
    app.exec()


if __name__ == "__main__":
    main()
