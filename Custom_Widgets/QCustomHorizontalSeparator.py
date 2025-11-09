from qtpy.QtWidgets import QWidget, QSizePolicy, QApplication
from qtpy.QtCore import QSize, Qt, Property
from qtpy.QtGui import QPainter, QColor, QPalette

import os

class QCustomHorizontalSeparator(QWidget):
    # Meta-information for integration with Qt Designer or other uses
    script_dir = os.path.dirname(os.path.realpath(__file__))
    WIDGET_ICON = os.path.join(script_dir, "components/icons/toolbar_separator_vertical.png")
    WIDGET_TOOLTIP = "A custom horizontal separator widget"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomHorizontalSeparator' name='customHorizontalSeparator'>
        </widget>
    </ui>
    """
    WIDGET_MODULE = "Custom_Widgets.QCustomHorizontalSeparator"

    def __init__(self, parent=None, color=None, height=1, margin=8):
        super().__init__(parent)
        
        # If no color is passed, use the default text color from the palette
        if color is not None:
            self.setColor(color)
        
        self._height = height
        self._margin = margin
        
        # Set the size policy correctly using QSizePolicy enums
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
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

    # Height Property
    def getHeight(self):
        return self._height

    def setHeight(self, height):
        """Sets the height (thickness) of the separator."""
        self._height = height
        self.updateGeometry()

    @Property(int)
    def height(self):
        return self.getHeight()

    @height.setter
    def height(self, height):
        self.setHeight(height)

    # Margin Property
    def getMargin(self):
        return self._margin

    def setMargin(self, margin):
        """Sets the vertical margin around the separator line."""
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
        return QSize(100, self._height + 2 * self._margin)

    def minimumSizeHint(self):
        """Returns the minimum size hint for the separator."""
        return QSize(20, self._height + 2 * self._margin)

    def paintEvent(self, event):
        """Overrides the paint event to draw the separator."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Set the pen and brush color for the line
        self._color = self.getColor()
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._color)
        
        # Calculate the position and dimensions for the separator
        y = self._margin
        rect = self.rect()
        painter.drawRect(0, y, rect.width(), self._height)

        painter.end()
