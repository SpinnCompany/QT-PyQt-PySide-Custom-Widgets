"""QCustomWaveform — live preview.

A quick showcase (not the full forms pipeline — just a preview of the new widget):
a live ECG line ("110 bpm"), a live audio-level equalizer ("Water"), a static
voice-message mirror waveform, and a glowing neon bar chart. The ECG + equalizer
self-animate via push().

Run through the MCP: designer_launch(project=…) then designer_run_app(project=…).
"""
import sys

from qtpy.QtCore import Qt
from qtpy.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel,
                            QGridLayout, QVBoxLayout, QFrame)

from Custom_Widgets.QCustomWaveform import QCustomWaveform


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
        self.setWindowTitle("QCustomWaveform — preview")
        self.resize(960, 620)
        root = QWidget(); self.setCentralWidget(root)
        grid = QGridLayout(root)
        grid.setContentsMargins(24, 24, 24, 24)
        grid.setHorizontalSpacing(20); grid.setVerticalSpacing(20)

        # Heart rate — streaming ECG line (animated), red on a faint grid
        ecg = QCustomWaveform(mode="line")
        ecg.capacity = 90
        ecg.lineColor = "#ff5c6c"; ecg.lineWidth = 2.2
        ecg.showGrid = True; ecg.gridColor = "#242a38"
        ecg.animated = True
        grid.addWidget(card("Heart rate", "110 bpm · live", ecg), 0, 0)

        # Water — audio-level equalizer bars (animated), blue→cyan
        water = QCustomWaveform(mode="bars")
        water.capacity = 40
        water.barColor = "#38bdf8"; water.barColor2 = "#3aa0ff"
        water.barGap = 3; water.cornerRadius = 3
        water.animated = True
        grid.addWidget(card("Water", "Recording…", water), 0, 1)

        # Voice message — static mirror waveform (center-symmetric)
        voice = QCustomWaveform(mode="bars")
        voice.setValues([0.3, 0.6, 0.4, 0.85, 0.5, 0.7, 0.35, 0.9, 0.55, 0.65,
                         0.45, 0.8, 0.4, 0.7, 0.5, 0.6, 0.3, 0.75, 0.5, 0.4])
        voice.mirror = True
        voice.barColor = "#8b5cf6"; voice.barColor2 = "#a78bfa"
        voice.barGap = 4; voice.cornerRadius = 4
        grid.addWidget(card("Voice message", "0:14", voice), 1, 0)

        # Neon spectrum — glowing bars (the HYPER-CHARTS look)
        neon = QCustomWaveform(mode="bars")
        neon.capacity = 44
        neon.barColor = "#39d353"; neon.barColor2 = "#8affc1"
        neon.glow = True; neon.glowStrength = 0.9
        neon.barGap = 3
        neon.animated = True
        grid.addWidget(card("Spectrum", "Live · neon glow", neon), 1, 1)

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
    try:
        from Custom_Widgets.AppControl import maybe_start_app_control
        maybe_start_app_control()
    except Exception:
        pass
    app.exec()


if __name__ == "__main__":
    main()
