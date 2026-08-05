########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/@SpinnTV
# WEBSITE: customwidgets.org
########################################################################

########################################################################
## QCustomClockLabel - a self-ticking clock label.
##
## Shows the current time in `format` (QTime.toString syntax, default
## "h:mm AP") and re-renders itself every `interval` ms - no app-side QTimer
## or formatting code. `running` (default True) pauses the tick; style it
## like any QLabel from QSS.
########################################################################
from qtpy.QtCore import Property, QTime, QTimer
from qtpy.QtWidgets import QLabel


class QCustomClockLabel(QLabel):

    WIDGET_ICON = "components/icons/schedule.png"
    WIDGET_TOOLTIP = "A self-ticking clock label (QTime format string)"
    WIDGET_MODULE = "Custom_Widgets.QCustomClockLabel"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomClockLabel' name='clockLabel'>
            <property name='geometry'><rect><x>0</x><y>0</y><width>120</width><height>36</height></rect></property>
        </widget>
    </ui>
    """
    __catalog__ = {
        "name": "QCustomClockLabel",
        "props": {"format": {"type": "string", "default": "h:mm AP"},
                  "interval": {"type": "int", "default": 1000},
                  "running": {"type": "bool", "default": True}},
        "signals": [],
        "tokens_used": [],
    }
    DESIGNER_CUSTOM_PROPS = [
        {"name": "format", "kind": "str", "group": "Clock"},
        {"name": "interval", "kind": "int", "group": "Clock"},
        {"name": "running", "kind": "bool", "group": "Clock"},
    ]

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("QCustomClockLabel")
        self._format = "h:mm AP"
        self._timer = QTimer(self)
        self._timer.setInterval(1000)
        self._timer.timeout.connect(self._tick)
        self._tick()
        self._timer.start()

    def _tick(self):
        self.setText(QTime.currentTime().toString(self._format))

    # ------------------------------------------------------------------ #
    ## Designer properties
    # ------------------------------------------------------------------ #
    @Property(str)
    def format(self):
        return self._format

    @format.setter
    def format(self, fmt):
        self._format = str(fmt) or "h:mm AP"
        self._tick()

    @Property(int)
    def interval(self):
        return self._timer.interval()

    @interval.setter
    def interval(self, ms):
        self._timer.setInterval(max(50, int(ms)))

    @Property(bool)
    def running(self):
        return self._timer.isActive()

    @running.setter
    def running(self, on):
        if bool(on):
            self._tick()
            self._timer.start()
        else:
            self._timer.stop()
