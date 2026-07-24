"""QCustomRulerPicker — live preview.

A quick showcase (not the full forms pipeline — just a preview of the new widget):
a weight ruler (fixed span, the reference "Wight" card), a height ruler with a big
readout, a scrolling-centered picker, and a vertical ruler — showing fixed vs
centered, horizontal vs vertical, snap, units and the live value readout.

Run through the MCP: designer_launch(project=…) then designer_run_app(project=…).
"""
import sys

from qtpy.QtCore import Qt
from qtpy.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel, QHBoxLayout,
                            QGridLayout, QVBoxLayout, QFrame)

from Custom_Widgets.QCustomRulerPicker import QCustomRulerPicker

ACCENT = "#7c5cff"


def card(title, unit, widget, header_value_label=None):
    frame = QFrame()
    frame.setObjectName("card")
    lay = QVBoxLayout(frame)
    lay.setContentsMargins(20, 16, 20, 16)
    lay.setSpacing(4)
    head = QHBoxLayout()
    cap = QLabel(title); cap.setObjectName("cardTitle")
    u = QLabel(unit); u.setObjectName("cardUnit")
    head.addWidget(cap)
    head.addStretch(1)
    if header_value_label is not None:
        head.addWidget(header_value_label)
    head.addWidget(u)
    lay.addLayout(head)
    lay.addSpacing(6)
    lay.addWidget(widget, 1)
    return frame


class Preview(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QCustomRulerPicker — preview")
        self.resize(940, 620)
        root = QWidget()
        self.setCentralWidget(root)
        grid = QGridLayout(root)
        grid.setContentsMargins(24, 24, 24, 24)
        grid.setHorizontalSpacing(20)
        grid.setVerticalSpacing(20)

        # Weight — fixed span (the reference), value shown in the header
        self.wlabel = QLabel("65"); self.wlabel.setObjectName("headVal")
        weight = QCustomRulerPicker(value=65, minimum=40, maximum=120, step=1)
        weight.majorEvery = 5
        weight.indicatorColor = ACCENT
        weight.valueChanged.connect(lambda v: self.wlabel.setText("%g" % v))
        grid.addWidget(card("Weight", "Kg", weight, self.wlabel), 0, 0, 1, 2)

        # Height — centered scrolling picker, big value readout
        height = QCustomRulerPicker(value=178, minimum=120, maximum=210, step=1)
        height.centered = True
        height.tickSpacing = 10
        height.majorEvery = 5
        height.showValue = True
        height.unit = "cm"
        height.indicatorColor = "#2fd27a"
        grid.addWidget(card("Height", "", height), 1, 0)

        # Body fat — fixed, fine step, one decimal
        bf = QCustomRulerPicker(value=18.5, minimum=5, maximum=40, step=0.5)
        bf.majorEvery = 10          # a label every 5.0
        bf.showValue = True
        bf.unit = "%"
        bf.indicatorColor = "#f4a63b"
        grid.addWidget(card("Body fat", "", bf), 1, 1)

        # Vertical ruler — temperature
        temp = QCustomRulerPicker(value=22, minimum=16, maximum=30, step=1,
                                  orientation="vertical")
        temp.majorEvery = 2
        temp.showValue = True
        temp.unit = "°C"
        temp.indicatorColor = "#3aa0ff"
        grid.addWidget(card("Thermostat", "", temp), 0, 2, 2, 1)

        self.setStyleSheet("""
            QMainWindow { background: #0e1016; }
            QWidget { color: #e7e9ef; font-family: 'Segoe UI', 'Inter', sans-serif; }
            QFrame#card {
                background: #171a22; border: 1px solid #232833; border-radius: 18px;
            }
            QLabel#cardTitle { font-size: 16px; font-weight: 600; color: #f4f6fb; }
            QLabel#cardUnit  { font-size: 13px; color: #6b7280; }
            QLabel#headVal   { font-size: 18px; font-weight: 700; color: #7c5cff; }
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
