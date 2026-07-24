"""QCustomRadialGauge — live preview.

A quick showcase window (not the full forms pipeline — just a preview of the new
widget) exercising the gauge's flexibility: the Threat-Level semicircles (needle
+ zones + status badge + dashed guide), a wide speedometer with a numeric scale,
a full-circle dial, and the "17 Sec" radial-tick countdown (dotted scale ring +
labels + emphasised leading tick). Everything animates in on show.

Run through the MCP: designer_launch(project=…) then designer_run_app(project=…).
"""
import sys

from qtpy.QtCore import Qt, QTimer
from qtpy.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel,
                            QGridLayout, QVBoxLayout, QFrame)

from Custom_Widgets.QCustomRadialGauge import QCustomRadialGauge

THREAT_ZONES = [(0, 33, "#33d17a"), (33, 66, "#f4c44e"), (66, 100, "#f2704e")]


def card(title, gauge):
    """Wrap a gauge in a rounded dark card with a title, like the references."""
    frame = QFrame()
    frame.setObjectName("card")
    lay = QVBoxLayout(frame)
    lay.setContentsMargins(18, 16, 18, 16)
    lay.setSpacing(4)
    cap = QLabel(title)
    cap.setObjectName("cardTitle")
    sub = QLabel("Last updated on 15th January, 2024")
    sub.setObjectName("cardSub")
    lay.addWidget(cap)
    lay.addWidget(sub)
    lay.addWidget(gauge, 1)
    return frame


def threat(value, status):
    g = QCustomRadialGauge(value=0)
    g.setZones(THREAT_ZONES)
    g.centerSuffix = "%"
    g.statusText = status
    g.animated = True
    g.animationDuration = 900
    g.glow = True                # soft neon halo behind the arc
    g._target = value            # animate to this on show
    return g


class Preview(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QCustomRadialGauge — preview")
        self.resize(1000, 620)
        root = QWidget()
        self.setCentralWidget(root)
        grid = QGridLayout(root)
        grid.setContentsMargins(24, 24, 24, 24)
        grid.setHorizontalSpacing(20)
        grid.setVerticalSpacing(20)
        self._animate_in = []

        # Row 1 — the three Threat-Level semicircle gauges (needle + zones + guide)
        for col, (v, s) in enumerate(((24, "Very Low"), (55, "Medium"), (75, "High"))):
            g = threat(v, s)
            self._animate_in.append(g)
            grid.addWidget(card("Threat Level", g), 0, col)

        # Row 2a — a wide speedometer (gradient arc + numeric scale, no zones)
        speedo = QCustomRadialGauge(value=0, minimum=0, maximum=150)
        speedo.startAngle = 210
        speedo.spanAngle = -240
        speedo.arcWidth = 18
        speedo.zonesCsv = ""
        speedo.setGradient("#33d17a", "#f2704e")
        speedo.centerSuffix = "mph"
        speedo.statusText = ""
        speedo.scaleLabelEvery = 30
        speedo.glow = True
        speedo.animated = True
        speedo.animationDuration = 1100
        speedo._target = 92
        self._animate_in.append(speedo)
        grid.addWidget(card("Speed", speedo), 1, 0)

        # Row 2b — a FULL-CIRCLE dial (any start/span; numeric scale; no needle)
        dial = QCustomRadialGauge(value=0, minimum=0, maximum=100)
        dial.startAngle = 90
        dial.spanAngle = -360
        dial.zonesCsv = ""
        dial.setGradient("#5b8cff", "#33d17a")
        dial.centerSuffix = "%"
        dial.statusText = ""
        dial.showNeedle = False
        dial.scaleLabelEvery = 25
        dial.glow = True
        dial.animated = True
        dial.animationDuration = 1100
        dial._target = 68
        self._animate_in.append(dial)
        grid.addWidget(card("Usage", dial), 1, 1)

        # Row 2c — a FULL-360 radial-tick countdown (dotted scale ring + labels +
        # outward-emphasised leading tick)
        self.timer_gauge = QCustomRadialGauge(
            value=17, minimum=0, maximum=20, gaugeStyle="tick")
        self.timer_gauge.startAngle = 90
        self.timer_gauge.spanAngle = -360          # full circle
        self.timer_gauge.tickCount = 60
        self.timer_gauge.zonesCsv = ""
        self.timer_gauge.setGradient("#7c5cff", "#ff5c8a")
        self.timer_gauge.centerText = "17"
        self.timer_gauge.centerSuffix = "Sec"
        self.timer_gauge.statusText = ""
        self.timer_gauge.showGuide = True          # dotted inner scale ring
        self.timer_gauge.scaleLabelEvery = 5       # 0/5/10/15/20 labels
        self.timer_gauge.activeTickExtend = "outward"
        self.timer_gauge.glow = True
        grid.addWidget(card("Timer", self.timer_gauge), 1, 2)

        self.timer_gauge.valueChanged.connect(
            lambda v: self.timer_gauge.setCenterText("%g" % v))
        self.timer_gauge.finished.connect(
            lambda: self.timer_gauge.start(seconds=20))  # loop the demo

        self.setStyleSheet("""
            QMainWindow { background: #0e1016; }
            QWidget { color: #e7e9ef; font-family: 'Segoe UI', 'Inter', sans-serif; }
            QFrame#card {
                background: #171a22; border: 1px solid #232833; border-radius: 18px;
            }
            QLabel#cardTitle { font-size: 16px; font-weight: 600; color: #f4f6fb; }
            QLabel#cardSub  { font-size: 11px; color: #6b7280; }
        """)

        # animate every gauge in from 0, and start the countdown, once shown
        QTimer.singleShot(350, self._run_intro)

    def _run_intro(self):
        for g in self._animate_in:
            g.setValue(g._target)
        self.timer_gauge.start(seconds=20)


def main():
    app = QApplication.instance() or QApplication(sys.argv)
    win = Preview()
    win.show()
    # enable the MCP in-app control server (app_screenshot/app_*) when run under
    # the dev server — no-op otherwise. Not part of the gauge; just the harness.
    try:
        from Custom_Widgets.AppControl import maybe_start_app_control
        maybe_start_app_control()
    except Exception:
        pass
    app.exec()


if __name__ == "__main__":
    main()
