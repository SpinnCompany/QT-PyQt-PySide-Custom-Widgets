from qtpy.QtCore import Qt, Signal, Property
from qtpy.QtGui import QPixmap, QPainter, QPen, QColor, QPainterPath
from qtpy.QtWidgets import QFrame
import os 

class QAvatarWidget(QFrame):
    # Custom widget icon
    script_dir = os.path.dirname(os.path.realpath(__file__))
    WIDGET_ICON = os.path.join(script_dir, "components/icons/user.png")

    WIDGET_TOOLTIP = "A custom avatar widget"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QAvatarWidget' name='customAvatar'>
        </widget>
    </ui>
    """
    WIDGET_MODULE = "Custom_Widgets.QAvatarWidget"

    clicked = Signal()

    def __init__(self, parent=None, avatarPath=""):
        super().__init__(parent)

        # Initialize avatar pixmap
        self._avatar_path = avatarPath if avatarPath else self.WIDGET_ICON
        self._pixmap = QPixmap(self._avatar_path)

        # Border settings
        self._border_color = QColor(255, 255, 255)
        self._border_width = 2
        
        # Widget settings
        self.setFixedSize(100, 100)
        self.setCursor(Qt.PointingHandCursor)
        self.setAvatar(self._avatar_path)
    
    @Property(QPixmap)
    def avatarPath(self):
        return self._pixmap
    
    @avatarPath.setter
    def avatarPath(self, value):
        if isinstance(value, QPixmap):
            self._pixmap = value
        elif isinstance(value, str):
            self.setAvatar(value)
        self.update()
    
    @Property(QColor)
    def borderColor(self):
        return self._border_color
    
    @borderColor.setter
    def borderColor(self, color):
        self._border_color = color
        self.update()
    
    @Property(int)
    def borderWidth(self):
        return self._border_width
    
    @borderWidth.setter
    def borderWidth(self, width):
        self._border_width = width
        self.update()
    
    def setAvatar(self, avatarPath):
        """Loads the avatar from the given path and updates the widget."""
        self._avatar_path = avatarPath
        self._pixmap = QPixmap(avatarPath).scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.update()
    
    def roundedPixmap(self, pixmap):
        """Creates a rounded version of the provided pixmap."""
        size = min(pixmap.width(), pixmap.height())
        output = QPixmap(size, size)
        output.fill(Qt.transparent)
        
        painter = QPainter(output)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)
        
        path = QPainterPath()
        path.addRoundedRect(0, 0, size, size, size / 2, size / 2)
        painter.setClipPath(path)
        
        if not pixmap.isNull():
            painter.drawPixmap(0, 0, pixmap)
            
            pen = QPen(self._border_color)
            pen.setWidth(self._border_width)
            painter.setPen(pen)
            painter.drawRoundedRect(0, 0, size, size, size / 2, size / 2)
        
        painter.end()
        
        return output
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)
        
        rounded_pixmap = self.roundedPixmap(self._pixmap)
        painter.drawPixmap(0, 0, self.width(), self.height(), rounded_pixmap)
    
    def mousePressEvent(self, event):
        self.clicked.emit()

    def showEvent(self, event):
        super().showEvent(event)
        self.update()
