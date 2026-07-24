"""QCustomDateRangePicker — live preview.

A quick showcase (not the full forms pipeline — just a preview of the new widget):
the inline dual-month travel-dates range picker (the reference), with live
Start/End readouts + a Save button, plus a dark 3-month variant.

Run through the MCP: designer_launch(project=…) then designer_run_app(project=…).
"""
import sys

from qtpy.QtCore import Qt, QDate
from qtpy.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel, QHBoxLayout,
                            QVBoxLayout, QFrame, QPushButton)

from Custom_Widgets.QCustomDateRangePicker import QCustomDateRangePicker

GREEN = "#2f8f5b"


def field(title):
    box = QFrame(); box.setObjectName("field")
    lay = QVBoxLayout(box); lay.setContentsMargins(14, 8, 14, 8); lay.setSpacing(0)
    cap = QLabel(title); cap.setObjectName("fieldCap")
    val = QLabel("—"); val.setObjectName("fieldVal")
    lay.addWidget(cap); lay.addWidget(val)
    return box, val


class Preview(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QCustomDateRangePicker — preview")
        self.resize(1000, 720)
        root = QWidget(); self.setCentralWidget(root)
        outer = QVBoxLayout(root); outer.setContentsMargins(28, 28, 28, 28); outer.setSpacing(20)

        # ---- light travel-dates card (the reference) ----
        light = QFrame(); light.setObjectName("lightCard")
        lv = QVBoxLayout(light); lv.setContentsMargins(24, 22, 24, 22); lv.setSpacing(16)
        title = QLabel("Select your travel dates"); title.setObjectName("lightTitle")
        lv.addWidget(title)

        self.picker = QCustomDateRangePicker(start=QDate(2025, 6, 23),
                                             end=QDate(2025, 7, 9), monthsVisible=2)
        self.picker.setMinimumHeight(320)
        lv.addWidget(self.picker, 1)

        row = QHBoxLayout(); row.setSpacing(12)
        sbox, self.sval = field("Start date")
        ebox, self.eval = field("End date")
        row.addWidget(sbox); row.addWidget(ebox); row.addStretch(1)
        save = QPushButton("Save dates"); save.setObjectName("save")
        save.setCursor(Qt.PointingHandCursor)
        row.addWidget(save)
        lv.addLayout(row)
        outer.addWidget(light, 1)

        self.picker.rangeChanged.connect(self._on_range)
        self._on_range(self.picker.startDate(), self.picker.endDate())

        self.setStyleSheet("""
            QMainWindow { background: #eef1f5; }
            QWidget { font-family: 'Segoe UI', 'Inter', sans-serif; color: #1c2430; }
            QFrame#lightCard { background: #ffffff; border-radius: 22px; }
            QLabel#lightTitle { font-size: 20px; font-weight: 700; color: #1c2430; }
            QFrame#field { background: #ffffff; border: 1px solid #d9dfe6; border-radius: 12px; }
            QLabel#fieldCap { font-size: 11px; color: #8b93a1; }
            QLabel#fieldVal { font-size: 15px; font-weight: 600; color: #1c2430; }
            QPushButton#save {
                background: %s; color: #ffffff; border: none; border-radius: 20px;
                padding: 12px 28px; font-size: 14px; font-weight: 600;
            }
            QPushButton#save:hover { background: #277a4d; }
        """ % GREEN)

    def _on_range(self, s, e):
        self.sval.setText(s.toString("dd.MM.yyyy") if s.isValid() else "—")
        self.eval.setText(e.toString("dd.MM.yyyy") if e.isValid() else "—")


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
