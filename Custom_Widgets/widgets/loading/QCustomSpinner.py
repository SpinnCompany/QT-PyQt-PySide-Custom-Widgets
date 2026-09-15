#                 PyQt5 Custom Widgets                #
#                GPL 3.0 - Kadir Aksoy                #
#   https://github.com/kadir014/pyqt5-custom-widgets  #


import time
from math import sin, cos, radians
from qtpy.QtCore import Qt, QRectF, Property
from qtpy.QtWidgets import QWidget
from qtpy.QtGui import QPainter, QPen, QPalette, QColor

class QCustomSpinner(QWidget):
    # Qt Designer contract. WIDGET_MODULE is the FLAT public path --
    # Custom_Widgets.QCustomSpinner is what .ui files carry in <header>, not the
    # subpackage this file now lives in.
    __catalog__ = {
        "name": "QCustomSpinner",
        "props": {
            "lineWidth": {},
            "color": {},
            "borderRadius": {},
            "direction": {},
            "animationType": {},
            "speed": {},
            "play": {},
        },
    }
    WIDGET_MODULE = "Custom_Widgets.QCustomSpinner"
    WIDGET_TOOLTIP = "A lightweight spinning busy indicator"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomSpinner' name='qCustomSpinner'>
            <property name='geometry'><rect><x>0</x><y>0</y><width>48</width><height>48</height></rect></property>
        </widget>
    </ui>
    """
    DESIGNER_CUSTOM_PROPS = [
        {"name": "lineWidth", "kind": "int", "group": "Style"},
        {"name": "color", "kind": "color", "group": "Style"},
        {"name": "borderRadius", "kind": "int", "group": "Style"},
        {"name": "direction", "kind": "choice",
         "choices": ["Clockwise", "Counterclockwise"], "group": "Style"},
        {"name": "animationType", "kind": "choice",
         "choices": ["Bounce", "Smooth"], "group": "Animation"},
        {"name": "speed", "kind": "float", "group": "Animation"},
        {"name": "play", "kind": "bool", "group": "Animation"},
    ]

    @Property(int)
    def lineWidth(self):
        return self.w

    @lineWidth.setter
    def lineWidth(self, value):
        self.w = int(value)
        self.update()

    @Property(QColor)
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        self._color = QColor(value)
        self.update()

    @Property(int)
    def borderRadius(self):
        return self._borderRadius

    @borderRadius.setter
    def borderRadius(self, value):
        self._borderRadius = int(value)
        self.update()

    @Property(str)
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, value):
        self._direction = str(value)
        self.update()

    @Property(str)
    def animationType(self):
        return self.animType

    @animationType.setter
    def animationType(self, value):
        self.animType = str(value)
        self.update()

    @Property(float)
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, value):
        self._speed = float(value)

    @Property(bool)
    def play(self):
        return self._play

    @play.setter
    def play(self, value):
        self._play = bool(value)
        self.update()

    # `parent` must come first and reach QWidget: Designer builds every widget
    # as Class(parent), so without it the QWidget was bound to `lineWidth` and
    # the spinner came out unparented — placeable but broken, which is why this
    # widget sat in the tiering manifest's waived list instead of being
    # registered. Every existing caller passes keywords (lineWidth=...,
    # lineColor=...), so taking the first positional slot breaks nothing.
    def __init__(self, parent = None, lineWidth = 2, lineColor = None, direction = "Clockwise", borderRadius = 3, animationType = "Bounce"):
        super().__init__(parent)

        self.w = lineWidth
        if lineColor is None:
            self.color = self.palette().color(QPalette.Highlight)
        else:
            self.color = lineColor
        self.direction = direction
        self.borderRadius = borderRadius

        self.angle = 0
        self.speed = 4.8

        self.animType = animationType

        self.play = True

        self.last_call = time.time()

    def __repr__(self):
        return f"<QCustom.Spinner()>"

    def paintEvent(self, event):
        pt = QPainter()
        pt.begin(self)
        pt.setRenderHint(QPainter.Antialiasing, on=True)

        w = self.w
        try:
            pen = QPen(self.color, w)
        except:
            pen = QPen(QColor(self.color), w)
        # Set the line cap style to round
        pen.setCapStyle(Qt.RoundCap)
        pt.setPen(pen)

        if self.direction == "Counterclockwise":
            start_angle = self.angle
            end_angle = self.angle + 90 * 16
        else:  # 
            start_angle = self.angle
            end_angle = self.angle - 90 * 16

        if self.animType == "Smooth":
            pt.drawArc(w, w, self.width() - w * 2, self.height() - w * 2, start_angle, 90 * 16)
        elif self.animType == "Bounce":
            sa = ((sin(radians(start_angle / 16)) + 1) / 2) * (180 * 16) + (
                        (sin(radians((end_angle / 16) + 130)) + 1) / 2) * (180 * 16)
            pt.drawArc(w, w, self.width() - w * 2, self.height() - w * 2, start_angle, sa)

        pt.end()

        ep = (time.time() - self.last_call) * 1000
        self.last_call = time.time()

        self.angle += self.speed * ep
        if self.angle > 360 * 16:
            self.angle = 0
        elif self.angle < 0:
            self.angle = 360 * 16

        if self.play:
            self.update()


