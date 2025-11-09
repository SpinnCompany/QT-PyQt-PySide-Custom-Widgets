from qtpy.QtWidgets import QWidget, QSizePolicy, QApplication
from qtpy.QtCore import QSize, Qt, Property
from qtpy.QtGui import QPainter, QColor, QPalette

import os

class QCustomVerticalSeparator(QWidget):
    # Meta-information for integration with Qt Designer or other uses
    script_dir = os.path.dirname(os.path.realpath(__file__))
    WIDGET_ICON = os.path.join(script_dir, "components/icons/line_vertical.png.png")
    WIDGET_TOOLTIP = "A custom vertical separator widget"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomVerticalSeparator' name='customVerticalSeparator'>
        </widget>
    </ui>
    """
    WIDGET_MODULE = "Custom_Widgets.QCustomVerticalSeparator"

    def __init__(self, parent=None, color=None, width=1, margin=8):
        super().__init__(parent)
        
        # If no color is passed, use the default text color from the palette
        if color is not None:
            self.setColor(color)
        
        self._width = width
        self._margin = margin
        
        # Set the size policy correctly using QSizePolicy enums (Fixed for width, Expanding for height)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        self.setSizePolicy(sizePolicy)

    def getColor(self):
        # Get the palette's text color (matches application theme)
        self._color = self.palette().color(QPalette.Text)
        return self._color

    def setColor(self, color):
        """Sets the color of the separator."""
        self._color = QColor(color)
        self.update()

    @Property(QColor)
    def color(self):
        return self.getColor()

    @color.setter
    def color(self, color):
        self.setColor(color)

    # Width Property (equivalent to height in horizontal separator)
    def getWidth(self):
        return self._width

    def setWidth(self, width):
        """Sets the width (thickness) of the separator."""
        self._width = width
        self.updateGeometry()

    @Property(int)
    def width(self):
        return self.getWidth()

    @width.setter
    def width(self, width):
        self.setWidth(width)

    # Margin Property
    def getMargin(self):
        return self._margin

    def setMargin(self, margin):
        """Sets the horizontal margin around the separator line."""
        self._margin = margin
        self.updateGeometry()

    @Property(int)
    def margin(self):
        return self.getMargin()

    @margin.setter
    def margin(self, margin):
        self.setMargin(margin)

    def sizeHint(self):
        """Returns the suggested size for the separator."""
        return QSize(self._width + 2 * self._margin, 100)

    def minimumSizeHint(self):
        """Returns the minimum size hint for the separator."""
        return QSize(self._width + 2 * self._margin, 20)

    def paintEvent(self, event):
        """Overrides the paint event to draw the separator."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Set the pen and brush color for the line
        self._color = self.getColor()
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._color)
        
        # Calculate the position and dimensions for the separator
        x = self._margin
        rect = self.rect()
        painter.drawRect(x, 0, self._width, rect.height())

        painter.end()