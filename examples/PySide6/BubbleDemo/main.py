"""QCustomBubbleChart — live preview.

Interactive sentiment bubble cloud + market-share chart: hover for a CUSTOM
tooltip card, wheel/±/drag to zoom & pan, double-click to reset, type in the
search box (or click the painted search icon) to highlight matches.

Run through the MCP: designer_launch(project=…) then designer_run_app(project=…).
"""
import sys

from qtpy.QtCore import Qt
from qtpy.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel, QHBoxLayout,
                            QVBoxLayout, QFrame, QLineEdit)

from Custom_Widgets.QCustomBubbleChart import QCustomBubbleChart


def card(title, chart):
    frame = QFrame(); frame.setObjectName("card")
    lay = QVBoxLayout(frame); lay.setContentsMargins(20, 16, 20, 16); lay.setSpacing(10)
    head = QHBoxLayout()
    cap = QLabel(title); cap.setObjectName("cardTitle")
    search = QLineEdit(); search.setObjectName("search")
    search.setPlaceholderText("Search…"); search.setMaximumWidth(180)
    search.textChanged.connect(chart.setSearchQuery)
    chart.searchRequested.connect(search.setFocus)
    head.addWidget(cap); head.addStretch(1); head.addWidget(search)
    lay.addLayout(head)
    lay.addWidget(chart, 1)
    return frame


class Preview(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QCustomBubbleChart — preview")
        self.resize(1040, 620)
        root = QWidget(); self.setCentralWidget(root)
        row = QHBoxLayout(root); row.setContentsMargins(24, 24, 24, 24); row.setSpacing(20)

        # Sentiment cloud — grouped by category (positive / negative / neutral lobes)
        sent = QCustomBubbleChart()
        sent.setCategoryColors({"positive": "#3fb27f", "negative": "#e0607e",
                                "neutral": "#8b9cff"})
        sent.groupByCategory = True
        row.addWidget(card("Customer sentiment", sent), 1)

        # Market share — single-blob, different data
        share = QCustomBubbleChart(items=[
            {"label": "Chrome", "value": 64, "category": "a"},
            {"label": "Safari", "value": 19, "category": "b"},
            {"label": "Edge", "value": 5, "category": "c"},
            {"label": "Firefox", "value": 3, "category": "c"},
            {"label": "Opera", "value": 2, "category": "c"},
            {"label": "Samsung", "value": 3, "category": "b"},
            {"label": "UC", "value": 1, "category": "c"},
            {"label": "Other", "value": 3, "category": "c"},
        ])
        share.setCategoryColors({"a": "#3aa0ff", "b": "#7c5cff", "c": "#5bd6e0"})
        share.minLabelRadius = 12
        row.addWidget(card("Browser share", share), 1)

        self.setStyleSheet("""
            QMainWindow { background: #0e1016; }
            QWidget { color: #e7e9ef; font-family: 'Segoe UI', 'Inter', sans-serif; }
            QFrame#card {
                background: #171a22; border: 1px solid #232833; border-radius: 18px;
            }
            QLabel#cardTitle { font-size: 16px; font-weight: 600; color: #f4f6fb; }
            QLineEdit#search {
                background: #0e1016; border: 1px solid #2b3040; border-radius: 14px;
                padding: 6px 12px; color: #e7e9ef;
            }
            QLineEdit#search:focus { border-color: #3aa0ff; }
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
