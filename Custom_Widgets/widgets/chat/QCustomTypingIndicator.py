########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/@SpinnTV
# WEBSITE: customwidgets.org
########################################################################

########################################################################
## QCustomTypingIndicator - the animated "… is typing" dots.
##
## Three dots that bounce/fade in sequence, painted with QPainter (no assets),
## optionally inside a chat-bubble-style pill. Call start()/stop() (or set the
## `running` property) to animate; colour and dot size are qproperties.
## Designer-droppable so it drops straight into a thread.
########################################################################
import math

from qtpy.QtCore import Qt, Property, QTimer, QRectF
from qtpy.QtGui import QColor, QPainter, QBrush
from qtpy.QtWidgets import QWidget, QSizePolicy


class QCustomTypingIndicator(QWidget):

    WIDGET_ICON = "components/icons/typing_indicator.png"
    WIDGET_TOOLTIP = "Animated typing dots"
    WIDGET_MODULE = "Custom_Widgets.QCustomTypingIndicator"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomTypingIndicator' name='customTypingIndicator'>
            <property name='geometry'><rect><x>0</x><y>0</y><width>64</width><height>34</height></rect></property>
        </widget>
    </ui>
    """
    __catalog__ = {
        "name": "QCustomTypingIndicator",
        "props": {"running": {"type": "bool", "default": True},
                  "dotColor": {"type": "color", "default": "#8a93a6"},
                  "dotSize": {"type": "int", "default": 7},
                  "bubble": {"type": "bool", "default": True},
                  "bubbleColor": {"type": "color", "default": "#eef1f5"}},
        "signals": [],
        "tokens_used": ["accent"],
    }

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("QCustomTypingIndicator")
        self._dot = QColor("#8a93a6")
        self._dot_size = 7
        self._bubble = True
        self._bubble_color = QColor("#eef1f5")
        self._phase = 0.0
        self._timer = QTimer(self)
        self._timer.setInterval(60)
        self._timer.timeout.connect(self._tick)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.setMinimumSize(58, 32)
        self.start()

    def start(self):
        if not self._timer.isActive():
            self._timer.start()

    def stop(self):
        self._timer.stop()

    def _tick(self):
        self._phase += 0.22
        self.update()

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, True)
        w, h = self.width(), self.height()
        d = self._dot_size
        gap = d + 6
        total = 3 * d + 2 * 6
        x0 = (w - total) / 2.0
        cy = h / 2.0
        if self._bubble:
            p.setPen(Qt.NoPen)
            p.setBrush(QBrush(self._bubble_color))
            bw = total + 24
            p.drawRoundedRect(QRectF((w - bw) / 2.0, (h - (d + 16)) / 2.0, bw, d + 16),
                              (d + 16) / 2.0, (d + 16) / 2.0)
        p.setPen(Qt.NoPen)
        for i in range(3):
            # each dot bounces on a sine offset by phase; alpha pulses too
            off = math.sin(self._phase - i * 0.7)
            dy = -off * 3.0
            a = 0.45 + 0.55 * (0.5 + 0.5 * off)
            c = QColor(self._dot)
            c.setAlphaF(max(0.25, min(1.0, a)))
            p.setBrush(QBrush(c))
            p.drawEllipse(QRectF(x0 + i * gap, cy - d / 2.0 + dy, d, d))
        p.end()

    # ------------------------------------------------------------------ #
    ## Designer properties
    # ------------------------------------------------------------------ #
    @Property(bool)
    def running(self):
        return self._timer.isActive()

    @running.setter
    def running(self, v):
        self.start() if bool(v) else self.stop()

    @Property(QColor)
    def dotColor(self):
        return self._dot

    @dotColor.setter
    def dotColor(self, c):
        self._dot = QColor(c)
        self.update()

    @Property(int)
    def dotSize(self):
        return self._dot_size

    @dotSize.setter
    def dotSize(self, v):
        self._dot_size = max(3, int(v))
        self.update()

    @Property(bool)
    def bubble(self):
        return self._bubble

    @bubble.setter
    def bubble(self, v):
        self._bubble = bool(v)
        self.update()

    @Property(QColor)
    def bubbleColor(self):
        return self._bubble_color

    @bubbleColor.setter
    def bubbleColor(self, c):
        self._bubble_color = QColor(c)
        self.update()
