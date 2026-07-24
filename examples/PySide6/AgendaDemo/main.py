"""QCustomAgendaList — live preview.

A quick showcase (not the full forms pipeline — just a preview of the new widget):
a day-plan schedule card (Running / Cycling / Gym / Swimming) with the connector
rail + done/active/pending status markers, and a second "meetings" agenda — inside
scroll areas so it flexes.

Run through the MCP: designer_launch(project=…) then designer_run_app(project=…).
"""
import sys

from qtpy.QtCore import Qt
from qtpy.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel, QHBoxLayout,
                            QVBoxLayout, QFrame, QScrollArea)

from Custom_Widgets.QCustomAgendaList import QCustomAgendaList


def card(title, subtitle, widget):
    frame = QFrame(); frame.setObjectName("card")
    lay = QVBoxLayout(frame); lay.setContentsMargins(20, 18, 12, 18); lay.setSpacing(2)
    cap = QLabel(title); cap.setObjectName("cardTitle")
    sub = QLabel(subtitle); sub.setObjectName("cardSub")
    lay.addWidget(cap); lay.addWidget(sub); lay.addSpacing(8)
    scroll = QScrollArea(); scroll.setWidgetResizable(True); scroll.setFrameShape(QFrame.NoFrame)
    scroll.setObjectName("scroll")
    scroll.setWidget(widget)
    lay.addWidget(scroll, 1)
    return frame


class Preview(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QCustomAgendaList — preview")
        self.resize(820, 620)
        root = QWidget(); self.setCentralWidget(root)
        row = QHBoxLayout(root); row.setContentsMargins(24, 24, 24, 24); row.setSpacing(20)

        # Today's plan — the reference activities
        plan = QCustomAgendaList()   # seeded with Running/Cycling/Gym/Swimming
        row.addWidget(card("Today's plan", "4 activities", plan), 1)

        # Meetings — a second agenda with different data
        meet = QCustomAgendaList(items=[
            {"time": "09:30", "endTime": "10:00", "title": "Standup",
             "subtitle": "Zoom · Product", "status": "done", "color": "#22c07e"},
            {"time": "11:00", "endTime": "11:45", "title": "Design review",
             "subtitle": "Figma · Aurora", "status": "done", "color": "#8b5cf6"},
            {"time": "13:00", "endTime": "14:00", "title": "1:1 with Sam",
             "subtitle": "Room “Nebula”", "status": "active", "color": "#3aa0ff"},
            {"time": "15:30", "endTime": "16:00", "title": "Roadmap sync",
             "subtitle": "Room “Orbit”", "status": "pending", "color": "#f59e0b"},
            {"time": "17:00", "endTime": "17:30", "title": "Retro",
             "subtitle": "Zoom · Team", "status": "pending", "color": "#ef4444"},
        ])
        row.addWidget(card("Meetings", "Wednesday, 24 Jul", meet), 1)

        self.setStyleSheet("""
            QMainWindow { background: #0e1016; }
            QWidget { color: #e7e9ef; font-family: 'Segoe UI', 'Inter', sans-serif; }
            QFrame#card {
                background: #171a22; border: 1px solid #232833; border-radius: 18px;
            }
            QScrollArea#scroll { background: transparent; }
            QLabel#cardTitle { font-size: 16px; font-weight: 600; color: #f4f6fb; }
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
