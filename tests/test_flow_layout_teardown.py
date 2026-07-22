"""QCustomFlowLayout must tear down cleanly even when its debounce timer's C++
object has already been deleted (regression: __del__ -> takeAt ->
_scheduleLayoutUpdate -> QTimer.start on a deleted timer)."""
from qtpy.QtCore import QCoreApplication
from qtpy.QtWidgets import QWidget, QLabel


def test_schedule_update_safe_after_timer_deleted(qapp):
    from Custom_Widgets.QCustomFlowLayout import QCustomFlowLayout
    host = QWidget()
    fl = QCustomFlowLayout(host)
    fl.addWidget(QLabel("a"))
    fl.addWidget(QLabel("b"))

    # simulate the teardown ordering where the timer is gone first
    fl._updateTimer.deleteLater()
    QCoreApplication.processEvents()

    # scheduling must not raise now
    fl._scheduleLayoutUpdate()

    # draining items (what __del__ does) must not raise either
    item = fl.takeAt(0)
    while item:
        item = fl.takeAt(0)
    assert fl.count() == 0


def test_del_suppresses_scheduling(qapp):
    from Custom_Widgets.QCustomFlowLayout import QCustomFlowLayout
    host = QWidget()
    fl = QCustomFlowLayout(host)
    fl.addWidget(QLabel("x"))
    fl.__del__()                       # explicit; must not raise
    assert fl._updatingLayout is True
