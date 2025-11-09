from qtpy.QtCore import Qt, Property, Signal
from qtpy.QtGui import QColor, QPainter, QFont
from qtpy.QtWidgets import QFrame, QSizePolicy
import os

class QBadgeWidget(QFrame):
    script_dir = os.path.dirname(os.path.realpath(__file__))
    WIDGET_ICON = os.path.join(script_dir, "components/icons/award.png")
    WIDGET_TOOLTIP = "A custom badge widget"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QBadgeWidget' name='customBadge'>
        </widget>
    </ui>
    """
    WIDGET_MODULE="Custom_Widgets.QBadgeWidget"

    clicked = Signal()

    def __init__(
            self, 
            parent=None,
            text="Badge text",
            background_color=QColor(255, 0, 0),
            text_color=QColor(255, 255, 255)
            ):
        QFrame.__init__(self, parent=parent)
        
        self._text = text
        self._background_color = background_color
        self._text_color = text_color
        
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        # self.setMinimumSize(80, 30)
        self.setCursor(Qt.PointingHandCursor)
        self.setGeometry(0, 0, 80, 30)

    
    @Property(str)
    def text(self):
        return self._text
    
    @text.setter
    def text(self, value):
        self._text = value
        self.update()
    
    @Property(QColor)
    def backgroundColor(self):
        return self._background_color
    
    @backgroundColor.setter
    def backgroundColor(self, color):
        self._background_color = color
        self.update()
    
    @Property(QColor)
    def textColor(self):
        return self._text_color
    
    @textColor.setter
    def textColor(self, color):
        self._text_color = color
        self.update()
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        painter.setBrush(self._background_color)
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(self.rect(), 10, 10)
        
        painter.setPen(self._text_color)
        painter.setFont(QFont('Arial', 10))
        painter.drawText(self.rect(), Qt.AlignCenter, self._text)
    
    def mousePressEvent(self, event):
        self.clicked.emit()

    def showEvent(self, event):
        super().showEvent(event)
        self.update()
