"""QCustomLiquidGauge — live preview.

A quick showcase (not the full forms pipeline — just a preview of the new widget):
fuel / battery / tank / humidity fill gauges showing the circle + rounded-rect
shapes, gradient waves, centre value+suffix and status badges. The waves ripple
continuously and each level animates in from empty on show.

Run through the MCP: designer_launch(project=…) then designer_run_app(project=…).
"""
import sys

from qtpy.QtCore import Qt, QTimer
from qtpy.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel,
                            QGridLayout, QVBoxLayout, QFrame)

from Custom_Widgets.QCustomLiquidGauge import QCustomLiquidGauge


def card(title, widget, subtitle):
    frame = QFrame()
    frame.setObjectName("card")
    lay = QVBoxLayout(frame)
    lay.setContentsMargins(20, 18, 20, 18)
    lay.setSpacing(2)
    cap = QLabel(title); cap.setObjectName("cardTitle")
    sub = QLabel(subtitle); sub.setObjectName("cardSub")
    lay.addWidget(cap)
    lay.addWidget(sub)
    lay.addSpacing(6)
    lay.addWidget(widget, 1)
    return frame


class Preview(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QCustomLiquidGauge — preview")
        self.resize(860, 680)
        root = QWidget()
        self.setCentralWidget(root)
        grid = QGridLayout(root)
        grid.setContentsMargins(24, 24, 24, 24)
        grid.setHorizontalSpacing(20)
        grid.setVerticalSpacing(20)
        self._intro = []

        # Fuel — circle, blue→purple, "3.61 gal" + 31% badge
        fuel = QCustomLiquidGauge(value=0)
        fuel.setColors("#3aa0ff", "#7c5cff", background="#141826")
        fuel.centerText = "3.61"; fuel.centerSuffix = "gal"
        fuel.setBadge("31%", "#3aa0ff")
        fuel._target = 31
        self._intro.append(fuel)
        grid.addWidget(card("Fuel level", fuel, "Tank · 11.6 gal"), 0, 0)

        # Battery — rounded rect, green, 72%
        batt = QCustomLiquidGauge(value=0)
        batt.shape = "roundedRect"; batt.cornerRadius = 26
        batt.setColors("#2fd27a", "#7be0a8", background="#101a16")
        batt.centerSuffix = "%"
        batt._target = 72
        self._intro.append(batt)
        grid.addWidget(card("Battery", batt, "Charging"), 0, 1)

        # Water tank — circle, teal, 88%, "88%" + badge
        tank = QCustomLiquidGauge(value=0)
        tank.setColors("#28c2d1", "#5bd6e0", background="#0f1f26")
        tank.centerSuffix = "%"
        tank.setBadge("High", "#28c2d1")
        tank._target = 88
        self._intro.append(tank)
        grid.addWidget(card("Water tank", tank, "Reservoir A"), 1, 0)

        # Humidity — circle, cyan/indigo, 54%
        hum = QCustomLiquidGauge(value=0)
        hum.setColors("#5b8cff", "#8ab4ff", background="#12131f")
        hum.centerSuffix = "%"
        hum.setBadge("Indoor", "#5b8cff")
        hum._target = 54
        self._intro.append(hum)
        grid.addWidget(card("Humidity", hum, "Living room"), 1, 1)

        self.setStyleSheet("""
            QMainWindow { background: #0e1016; }
            QWidget { color: #e7e9ef; font-family: 'Segoe UI', 'Inter', sans-serif; }
            QFrame#card {
                background: #171a22; border: 1px solid #232833; border-radius: 18px;
            }
            QLabel#cardTitle { font-size: 16px; font-weight: 600; color: #f4f6fb; }
            QLabel#cardSub  { font-size: 11px; color: #6b7280; }
        """)

        QTimer.singleShot(400, self._run_intro)

    def _run_intro(self):
        for g in self._intro:
            g.setValue(g._target)


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
