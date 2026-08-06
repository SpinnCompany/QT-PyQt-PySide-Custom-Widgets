#                 PyQt5 Custom Widgets                #
#                GPL 3.0 - Kadir Aksoy                #
#   https://github.com/kadir014/pyqt5-custom-widgets  #


import time
from math import sin, cos, radians
from qtpy.QtCore import Qt, QRectF
from qtpy.QtWidgets import QWidget
from qtpy.QtGui import QPainter, QPen, QPalette, QColor

class QCustomSpinner(QWidget):
    # Qt Designer contract. WIDGET_MODULE is the FLAT public path --
    # Custom_Widgets.QCustomSpinner is what .ui files carry in <header>, not the
    # subpackage this file now lives in.
    WIDGET_MODULE = "Custom_Widgets.QCustomSpinner"
    WIDGET_TOOLTIP = "A lightweight spinning busy indicator"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomSpinner' name='qCustomSpinner'>
            <property name='geometry'><rect><x>0</x><y>0</y><width>48</width><height>48</height></rect></property>
        </widget>
    </ui>
    """
    def __init__(self, lineWidth = 2, lineColor = None, direction = "Clockwise", borderRadius = 3, animationType = "Bounce"):
        super().__init__()

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


