# coding:utf-8
from enum import Enum
from typing import Union

from qtpy.QtCore import Qt, QPoint, QObject, QPointF, QTimer, QPropertyAnimation, QEvent, QSize, Signal, QAbstractAnimation, QRect
from qtpy.QtGui import QPainter, QColor, QPainterPath, QIcon, QPolygonF, QPixmap, QImage, QPaintEvent, QCursor
from qtpy.QtWidgets import QWidget, QGraphicsDropShadowEffect, QGraphicsOpacityEffect, QStyle, QStyleOption, QApplication

from Custom_Widgets.QCustomTheme import QCustomTheme

from Custom_Widgets.components.python.ui_info import Ui_Form
from Custom_Widgets.QCustomComponentLoader import QCustomComponentLoader

class LoadForm(QWidget):
    def __init__(self, form):
        super().__init__()
        # self.ui = Ui_Form()
        self.form = form
        self.form.setupUi(self)

class QCustomTipOverlay(QWidget, Ui_Form):
    """ QCustomOvelay """
    closed = Signal()
    def __init__(self, title: str = "", description: str = "", icon: Union[QIcon, str] = None,
               image: Union[str, QPixmap, QImage] = None, isClosable=False, target: Union[QWidget, QPoint, QPointF] = None,
               parent=None, aniType="pull-up", deleteOnClose=True, duration=1000, tailPosition="bottom-center", showForm = None, addWidget=None,
               closeIcon: Union[QIcon, str] = None, toolFlag = False):

        super().__init__()
        self.setupUi(self)
        
        # Store the original target for position calculation
        self.original_target = target
        self.duration = duration
        self.deleteOnClose = deleteOnClose
        self.title = title
        self.description = description
        self.icon = icon
        self.image = image
        self.isClosable = isClosable
        self.aniType = aniType
        self.tailPosition = tailPosition
        self.showForm = showForm
        self.shownForm = showForm
        self.widget = addWidget
        self.closeIcon = closeIcon
        self.closeButton.setStyleSheet("background-color: transparent; padding: 0")
        self.closeButton.clicked.connect(self._fadeOut)

        self.layout().setContentsMargins(20, 20, 20, 20)
        self.manager = QCustomTipOverlayManager.make(self.tailPosition)
        
        self.setIcon(self.icon)
        self.setCloseIcon(self.closeIcon)
        self.setTitle(self.title)
        self.setDescription(self.description)
        self.loadForm(self.showForm)
        self.addWidget(self.widget)
        self.setClosable(self.isClosable)
        self.moveButton()

        # Connect the signal to a slot
        try:
            self.parent().themeEngine.onThemeChanged.connect(self.handleThemeChanged)
        except:
            pass

        # Track if we're currently closing to prevent recursive calls
        self._is_closing = False
        self._is_showing = False
        self._auto_close_timer = None
        
        # Will create opacity effect and animation in showEvent
        self.opacity_effect = None
        self.opacityAni = None

        self.setShadowEffect()
        if toolFlag:
            self.setWindowFlags(Qt.Popup | Qt.ToolTip | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        else:
            self.setWindowFlags(Qt.Popup | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_ShowWithoutActivating)

        # Handle parent and event filter
        if parent:
            self.setParent(parent)
            if parent.window():
                parent.window().installEventFilter(self)
        else:
            # If no parent, set to application active window
            app = QApplication.instance()
            if app and app.activeWindow():
                self.setParent(app.activeWindow())
    
        self.setStyleSheet("#frame{background-color: transparent; padding: 10px;}")
    
    def setShadowEffect(self):
        self.setGraphicsEffect(None)
        self.effect = QGraphicsDropShadowEffect(self)
        self.effect.setColor(QColor(0, 0, 0, 200))
        self.effect.setBlurRadius(10)
        self.effect.setXOffset(0)
        self.effect.setYOffset(0)
        self.setGraphicsEffect(self.effect)

    def handleThemeChanged(self):
        self.setIcon(None)
        self.setIcon(self.icon)
        self.setCloseIcon(None)
        self.setCloseIcon(self.closeIcon)
    
    def _fadeOut(self):
        """ fade out using widget-level opacity """
        if self._is_closing or not self.opacity_effect:
            return
            
        self._is_closing = True
        
        # Cancel any pending auto-close timer
        if self._auto_close_timer and self._auto_close_timer.isActive():
            self._auto_close_timer.stop()
        
        # Stop any running animation
        if self.opacityAni and self.opacityAni.state() == QPropertyAnimation.Running:
            self.opacityAni.stop()
        
        # Disconnect any existing connections
        try:
            if self.opacityAni:
                self.opacityAni.finished.disconnect()
        except:
            pass
        
        # Start fade out animation
        self.opacityAni.setDuration(500)
        try:
            self.opacityAni.setStartValue(self.opacity_effect.opacity())
        except:
            self.opacityAni.setStartValue(1)
            # Create new opacity effect and animation
            self.opacity_effect = QGraphicsOpacityEffect(self)
            self.opacity_effect.setOpacity(1)  # Start transparent
            self.setGraphicsEffect(self.opacity_effect)
            
            # Create property animation on the opacity effect
            self.opacityAni = QPropertyAnimation(self.opacity_effect, b'opacity', self)

        self.opacityAni.setEndValue(0.0)
        self.opacityAni.finished.connect(self._onFadeOutFinished)
        self.opacityAni.start()

    def _onFadeOutFinished(self):
        """ Called when fade out animation finishes """
        self._is_closing = False
        self._is_showing = False
        self.closed.emit()
        self.close()
        if self.deleteOnClose:
            self.deleteLater()

    def showEvent(self, e):
        if self._is_showing:
            return
            
        self._is_showing = True
        self._is_closing = False
        
        # Clean up any existing animations/effects
        self._cleanupEffects()
        
        # Create new opacity effect and animation
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.opacity_effect.setOpacity(0.0)  # Start transparent
        self.setGraphicsEffect(self.opacity_effect)
        
        # Create property animation on the opacity effect
        self.opacityAni = QPropertyAnimation(self.opacity_effect, b'opacity', self)
        
        self.adjustSizeToContent()
        self.raise_()
        
        # Start fade in animation
        self.opacityAni.setDuration(500)
        self.opacityAni.setStartValue(0.0)
        self.opacityAni.setEndValue(1.0)
        self.opacityAni.finished.connect(self._onFadeInFinished)
        self.opacityAni.start()
        
        # Setup timer for auto-close if duration is specified
        if self.duration >= 0:
            self._auto_close_timer = QTimer()
            self._auto_close_timer.setSingleShot(True)
            self._auto_close_timer.timeout.connect(self._fadeOut)
            self._auto_close_timer.start(self.duration)
        
        super().showEvent(e)
    
    def _onFadeInFinished(self):
        """ Called when fade in animation finishes """
        self._is_showing = False
        self.setShadowEffect()

    def closeEvent(self, e):
        # If we're already closing via animation, accept the event
        if self._is_closing:
            e.accept()
            return
            
        # Otherwise, start fade out and ignore the event
        self._fadeOut()
        e.ignore()

    def _cleanupEffects(self):
        """ Clean up opacity effect and animation """
        # Stop and delete animation
        if self.opacityAni:
            try:
                if self.opacityAni.state() == QPropertyAnimation.Running:
                    self.opacityAni.stop()
                self.opacityAni.deleteLater()
            except:
                pass
            self.opacityAni = None
        
        # Remove and delete opacity effect
        if self.opacity_effect:
            try:
                self.setGraphicsEffect(None)
                self.opacity_effect.deleteLater()
            except:
                pass
            self.opacity_effect = None
        
        # Stop auto-close timer
        if self._auto_close_timer:
            try:
                if self._auto_close_timer.isActive():
                    self._auto_close_timer.stop()
                self._auto_close_timer.deleteLater()
            except:
                pass
            self._auto_close_timer = None

    def eventFilter(self, obj, e: QEvent):
        if e.type() in [QEvent.Resize, QEvent.WindowStateChange, QEvent.Move, QEvent.Paint]:
            self.adjustSizeToContent()

        return super().eventFilter(obj, e)
    
    def paintEvent(self, e: QPaintEvent):
        # Don't paint if we're closing
        if self._is_closing:
            return
            
        super().paintEvent(e)
        # Move the widget to the position determined by the animation manager
        # self.move(self.manager.position(self))

        self.painter = QPainter(self)
        self.painter.setRenderHints(QPainter.Antialiasing)
        self.painter.setPen(Qt.NoPen)

        # Set the brush color to the parent's background color if a parent is set
        if self.parent():
            self.painter.setBrush(self.parent().palette().window())
        else:
            self.painter.setBrush(self.palette().window())

        w, h = self.width(), self.height()
        margins = self.layout().contentsMargins()

        self.path = QPainterPath()
        self.path.addRoundedRect(margins.left()/2, margins.top()/2, w - margins.right(), h - margins.bottom(), 8, 8)
        
        self.manager.draw(self, self.painter, self.path)

        self.moveButton()

        self.painter.end()

    def setIcon(self, icon):
        self.iconlabel.show()
        if isinstance(icon, QIcon):
            pixmap = icon.pixmap(QSize(32, 32))
            self.iconlabel.setPixmap(pixmap)
        elif isinstance(icon, str):
            # Assuming icon is a path to an image file
            pixmap = QPixmap(icon).scaled(QSize(32, 32))
            self.iconlabel.setPixmap(pixmap)
        else:
            self.iconlabel.hide()
    
    def setCloseIcon(self, iconFile):
        if isinstance(iconFile, QIcon):
            self.closeButton.setIcon(self.closeIcon)
        elif isinstance(iconFile, str):
            icon = QIcon()
            icon.addFile(iconFile, QSize(32, 32), QIcon.Normal, QIcon.Off)
            self.closeButton.setIcon(icon)
        else:
            icon = self.style().standardIcon(QStyle.SP_TitleBarCloseButton).pixmap(QSize(32, 32))
            self.closeButton.setIcon(icon)

    def setDescription(self, description):
        self.description = description
        if not self.description:
            self.bodyLabel.hide()
            return
        self.bodyLabel.setText(description)
        self.adjustSizeToContent()
    
    def setTitle(self, title):
        self.title = title
        if not self.title:
            self.titlelabel.hide()
            return
        self.titlelabel.setText(title)
        self.adjustSizeToContent()

    def loadForm(self, form):
        self.showForm = form
        # load form
        if self.showForm:
            self.form = QCustomComponentLoader()
            self.form.loadComponent(formClass = self.showForm)
            self.layout().addWidget(self.form) 
        
    def addWidget(self, widget):
        self.widget = widget
        if self.widget:
            self.layout().addWidget(self.widget) 
    
    def adjustSizeToContent(self):
        # Adjust the size to fit the content
        self.adjustSize()

        # Calculate position using the manager
        position = self.manager.position(self)
        self.move(position)

        self.update()

    def setClosable(self, clossable: bool = True):
        self.isClosable = clossable
        if clossable:
            self.closeButton.show()
        else:
            self.closeButton.hide()

    def moveButton(self):
        # Move the button to the calculated position
        margins = self.layout().contentsMargins()
        x, y = margins.right() * 4, margins.top() / 2
        w, h = self.width(), self.height()
        self.closeButton.setParent(self)
        self.closeButton.setLayout(None)
        self.closeButton.move(w - x, y)


class QCustomTipOverlayManager(QObject):
    """ QCustomOvelay manager """
    managers = {}
    def __init__(self):
        super().__init__()

    @classmethod
    def register(tipOverlay, name):
        """Register menu animation manager"""
        def wrapper(Manager):
            if name not in tipOverlay.managers:
                tipOverlay.managers[name] = Manager

            return Manager

        return wrapper

    @classmethod
    def make(tipOverlay, position: str):
        """Create info bar manager according to the display position"""
        if position not in tipOverlay.managers:
            raise ValueError(f'`{position}` is an invalid animation type.')

        return tipOverlay.managers[position]()

@QCustomTipOverlayManager.register("top-center")
class TopTailQCustomQToolTipManager(QCustomTipOverlayManager):
    """ Top tail QCustomOvelay manager """

    def draw(self, tipOverlay, painter, path):
        w, h = tipOverlay.width(), tipOverlay.height()
        margins = tipOverlay.layout().contentsMargins()
        
        # Draw the tail pointing downwards
        path.addPolygon(
            QPolygonF([QPointF(w/2 - margins.right()/2, margins.top()/2), 
                      QPointF(w/2, 1), 
                      QPointF(w/2 + margins.right()/2, margins.top()/2)]))

        painter.drawPath(path.simplified())

    def position(self, tipOverlay: QCustomTipOverlay):
        target = tipOverlay.original_target
        if isinstance(target, (QPoint, QPointF)):
            # For QPoint target, place the tip with tail pointing to the point
            # The tip should be above the point
            if isinstance(target, QPointF):
                pos = target.toPoint()
            else:
                pos = target
            
            # Center the tip horizontally over the point
            x = pos.x() - tipOverlay.width() // 2
            # Place the tip above the point (tail points to the point)
            y = pos.y() - tipOverlay.height()
            return QPoint(x, y)
        else:
            # For QWidget target, calculate position below the widget
            pos = target.mapToGlobal(QPoint(target.width()//2, target.height()))
            x = pos.x() - tipOverlay.width() // 2
            y = pos.y()
            return QPoint(x, y)

@QCustomTipOverlayManager.register("bottom-center")
class BottomTailQCustomQToolTipManager(QCustomTipOverlayManager):
    """ Bottom tail QCustomOvelay manager """

    def draw(self, tipOverlay, painter, path):
        w, h = tipOverlay.width(), tipOverlay.height()
        margins = tipOverlay.layout().contentsMargins()
        
        # Draw the tail pointing upwards
        path.addPolygon(
            QPolygonF([QPointF(w/2 - margins.right()/2, h - margins.top()/2), 
                      QPointF(w/2, h - 1), 
                      QPointF(w/2 + margins.right()/2, h - margins.top()/2)]))

        painter.drawPath(path.simplified())

    def position(self, tipOverlay: QCustomTipOverlay):
        target = tipOverlay.original_target
        if isinstance(target, (QPoint, QPointF)):
            # For QPoint target, place the tip with tail pointing to the point
            # The tip should be below the point
            if isinstance(target, QPointF):
                pos = target.toPoint()
            else:
                pos = target
            
            # Center the tip horizontally under the point
            x = pos.x() - tipOverlay.width() // 2
            # Place the tip below the point (tail points upwards to the point)
            y = pos.y()  # Tip starts at the point's y position
            return QPoint(x, y)
        else:
            # For QWidget target, calculate position above the widget
            pos = target.mapToGlobal(QPoint(target.width()//2, 0))
            x = pos.x() - tipOverlay.width() // 2
            y = pos.y() - tipOverlay.height()
            return QPoint(x, y)

@QCustomTipOverlayManager.register("left-center")
class LeftTailQCustomQToolTipManager(QCustomTipOverlayManager):
    """ Left tail QCustomOvelay manager """

    def draw(self, tipOverlay, painter, path):
        w, h = tipOverlay.width(), tipOverlay.height()
        margins = tipOverlay.layout().contentsMargins()
        
        # Draw the tail pointing to the right
        path.addPolygon(
            QPolygonF([QPointF(margins.right()/2, h/2 - margins.top()/2), 
                      QPointF(1, h/2), 
                      QPointF(margins.right()/2, h/2 + margins.top()/2)]))

        painter.drawPath(path.simplified())

    def position(self, tipOverlay: QCustomTipOverlay):
        target = tipOverlay.original_target
        if isinstance(target, (QPoint, QPointF)):
            # For QPoint target, place the tip with tail pointing to the point
            # The tip should be to the left of the point
            if isinstance(target, QPointF):
                pos = target.toPoint()
            else:
                pos = target
            
            # Place the tip to the left of the point
            x = pos.x() - tipOverlay.width()  # Tip ends at the point's x position
            # Center the tip vertically on the point
            y = pos.y() - tipOverlay.height() // 2
            return QPoint(x, y)
        else:
            # For QWidget target, calculate position to the right of the widget
            pos = target.mapToGlobal(QPoint(target.width(), target.height()//2))
            x = pos.x()
            y = pos.y() - tipOverlay.height() // 2
            return QPoint(x, y)

@QCustomTipOverlayManager.register("right-center")
class RightTailQCustomQToolTipManager(QCustomTipOverlayManager):
    """ Right tail QCustomOvelay manager """

    def draw(self, tipOverlay, painter, path):
        w, h = tipOverlay.width(), tipOverlay.height()
        margins = tipOverlay.layout().contentsMargins()
        
        # Draw the tail pointing to the left
        path.addPolygon(
            QPolygonF([QPointF(w - margins.right()/2, h/2 - margins.top()/2), 
                      QPointF(w - 1, h/2), 
                      QPointF(w - margins.right()/2, h/2 + margins.top()/2)]))

        painter.drawPath(path.simplified())

    def position(self, tipOverlay: QCustomTipOverlay):
        target = tipOverlay.original_target
        if isinstance(target, (QPoint, QPointF)):
            # For QPoint target, place the tip with tail pointing to the point
            # The tip should be to the right of the point
            if isinstance(target, QPointF):
                pos = target.toPoint()
            else:
                pos = target
            
            # Place the tip to the right of the point
            x = pos.x()  # Tip starts at the point's x position
            # Center the tip vertically on the point
            y = pos.y() - tipOverlay.height() // 2
            return QPoint(x, y)
        else:
            # For QWidget target, calculate position to the left of the widget
            pos = target.mapToGlobal(QPoint(0, target.height()//2))
            x = pos.x() - tipOverlay.width()
            y = pos.y() - tipOverlay.height() // 2
            return QPoint(x, y)

@QCustomTipOverlayManager.register("top-left")
class TopLeftTailQCustomQToolTipManager(TopTailQCustomQToolTipManager):
    """ Top left tail QCustomOvelay manager """

    def draw(self, tipOverlay, painter, path):
        w, h = tipOverlay.width(), tipOverlay.height()
        margins = tipOverlay.layout().contentsMargins()
                
        path.addPolygon(
            QPolygonF([QPointF(20, margins.top()/2), 
                      QPointF(27, 1), 
                      QPointF(34, margins.top()/2)]))

        painter.drawPath(path.simplified())

    def position(self, tipOverlay: QCustomTipOverlay):
        target = tipOverlay.original_target
        if isinstance(target, (QPoint, QPointF)):
            # For QPoint target, place the tip with tail pointing to the point
            if isinstance(target, QPointF):
                pos = target.toPoint()
            else:
                pos = target
            
            # The tail is at position 27, so adjust accordingly
            x = pos.x() - 27  # Adjust so tail is at point's x
            y = pos.y()  # Tip starts at the point's y position
            return QPoint(x, y)
        else:
            # For QWidget target, calculate position
            pos = target.mapToGlobal(QPoint(0, target.height()))
            x = pos.x() 
            y = pos.y()
            return QPoint(x, y)

@QCustomTipOverlayManager.register("top-right")
class TopRightTailQCustomQToolTipManager(TopTailQCustomQToolTipManager):
    """ Top right tail QCustomOvelay manager """

    def draw(self, tipOverlay, painter, path):
        w, h = tipOverlay.width(), tipOverlay.height()
        margins = tipOverlay.layout().contentsMargins()
        
        path.addPolygon(
            QPolygonF([QPointF(w - 34, margins.top()/2), 
                      QPointF(w - 27, 1), 
                      QPointF(w - 20, margins.top()/2)]))

        painter.drawPath(path.simplified())

    def position(self, tipOverlay: QCustomTipOverlay):
        target = tipOverlay.original_target
        if isinstance(target, (QPoint, QPointF)):
            # For QPoint target, place the tip with tail pointing to the point
            if isinstance(target, QPointF):
                pos = target.toPoint()
            else:
                pos = target
            
            # The tail is at position width-27, so adjust accordingly
            x = pos.x() - (tipOverlay.width() - 27)  # Adjust so tail is at point's x
            y = pos.y()  # Tip starts at the point's y position
            return QPoint(x, y)
        else:
            # For QWidget target, calculate position
            pos = target.mapToGlobal(QPoint(target.width(), target.height()))
            x = pos.x() - tipOverlay.width()
            y = pos.y()
            return QPoint(x, y)

@QCustomTipOverlayManager.register("bottom-left")
class BottomLeftTailQCustomQToolTipManager(BottomTailQCustomQToolTipManager):
    """ Bottom left tail QCustomOvelay manager """

    def draw(self, tipOverlay, painter, path):
        w, h = tipOverlay.width(), tipOverlay.height()
        margins =tipOverlay.layout().contentsMargins()
        
        path.addPolygon(
            QPolygonF([QPointF(20, h - margins.top()/2), 
                      QPointF(27, h - 1), 
                      QPointF(34, h - margins.top()/2)]))

        painter.drawPath(path.simplified())

    def position(self, tipOverlay: QCustomTipOverlay):
        target = tipOverlay.original_target
        if isinstance(target, (QPoint, QPointF)):
            # For QPoint target, place the tip with tail pointing to the point
            if isinstance(target, QPointF):
                pos = target.toPoint()
            else:
                pos = target
            
            # The tail is at position 27, so adjust accordingly
            x = pos.x() - 27  # Adjust so tail is at point's x
            y = pos.y() - tipOverlay.height()  # Tip is above the point
            return QPoint(x, y)
        else:
            # For QWidget target, calculate position
            pos = target.mapToGlobal(QPoint(0, 0))
            x = pos.x()
            y = pos.y() - tipOverlay.height()
            return QPoint(x, y)

@QCustomTipOverlayManager.register("bottom-right")
class BottomRightTailQCustomQToolTipManager(BottomTailQCustomQToolTipManager):
    """ Bottom right tail QCustomOvelay manager """

    def draw(self, tipOverlay, painter, path):
        w, h = tipOverlay.width(), tipOverlay.height()
        margins =tipOverlay.layout().contentsMargins()
        path.addPolygon(
            QPolygonF([QPointF(w - 34, h - margins.top()/2), 
                      QPointF(w - 27, h - 1), 
                      QPointF(w - 20, h - margins.top()/2)]))

        painter.drawPath(path.simplified())
       
    def position(self, tipOverlay: QCustomTipOverlay):
        target = tipOverlay.original_target
        if isinstance(target, (QPoint, QPointF)):
            # For QPoint target, place the tip with tail pointing to the point
            if isinstance(target, QPointF):
                pos = target.toPoint()
            else:
                pos = target
            
            # The tail is at position width-27, so adjust accordingly
            x = pos.x() - (tipOverlay.width() - 27)  # Adjust so tail is at point's x
            y = pos.y() - tipOverlay.height()  # Tip is above the point
            return QPoint(x, y)
        else:
            # For QWidget target, calculate position
            pos = target.mapToGlobal(QPoint(target.width(), 0))
            x = pos.x() - tipOverlay.width()
            y = pos.y() - tipOverlay.height()
            return QPoint(x, y)

@QCustomTipOverlayManager.register("left-top")
class LeftTopTailQCustomQToolTipManager(LeftTailQCustomQToolTipManager):
    """ Left top tail QCustomOvelay manager """

    def draw(self, tipOverlay, painter, path):
        w, h = tipOverlay.width(), tipOverlay.height()
        margins =tipOverlay.layout().contentsMargins()
        
        path.addPolygon(
            QPolygonF([QPointF(margins.right()/2, margins.top()), 
                      QPointF(1, margins.top() + 7), 
                      QPointF(margins.right()/2, margins.top() + 14)]))

        painter.drawPath(path.simplified())

    def position(self, tipOverlay: QCustomTipOverlay):
        target = tipOverlay.original_target
        if isinstance(target, (QPoint, QPointF)):
            # For QPoint target, place the tip with tail pointing to the point
            if isinstance(target, QPointF):
                pos = target.toPoint()
            else:
                pos = target
            
            # The tail is at position (1, margins.top() + 7), so adjust accordingly
            x = pos.x() - tipOverlay.width()  # Tip is to the left of the point
            y = pos.y() - (margins.top() + 7)  # Adjust so tail is at point's y
            return QPoint(x, y)
        else:
            # For QWidget target, calculate position
            pos = target.mapToGlobal(QPoint(target.width(), 0))
            x = pos.x()
            y = pos.y()
            return QPoint(x, y)

@QCustomTipOverlayManager.register("left-bottom")
class LeftBottomTailQCustomQToolTipManager(LeftTailQCustomQToolTipManager):
    """ Left bottom tail QCustomOvelay manager """

    def draw(self, tipOverlay, painter, path):
        w, h = tipOverlay.width(), tipOverlay.height()
        margins =tipOverlay.layout().contentsMargins()
        
        path.addPolygon(
            QPolygonF([QPointF(margins.right()/2, h - margins.top() - 14), 
                      QPointF(1, h - margins.top() - 7), 
                      QPointF(margins.right()/2, h - margins.top())]))

        painter.drawPath(path.simplified())

    def position(self, tipOverlay: QCustomTipOverlay):
        target = tipOverlay.original_target
        if isinstance(target, (QPoint, QPointF)):
            # For QPoint target, place the tip with tail pointing to the point
            if isinstance(target, QPointF):
                pos = target.toPoint()
            else:
                pos = target
            
            # The tail is at position (1, h - margins.top() - 7), so adjust accordingly
            x = pos.x() - tipOverlay.width()  # Tip is to the left of the point
            y = pos.y() - (tipOverlay.height() - margins.top() - 7)  # Adjust so tail is at point's y
            return QPoint(x, y)
        else:
            # For QWidget target, calculate position
            pos = target.mapToGlobal(QPoint(target.width(), target.height()))
            x = pos.x()
            y = pos.y() - tipOverlay.height()
            return QPoint(x, y)

@QCustomTipOverlayManager.register("right-top")
class RightTopTailQCustomQToolTipManager(RightTailQCustomQToolTipManager):
    """ Right top tail QCustomOvelay manager """

    def draw(self, tipOverlay, painter, path):
        w, h = tipOverlay.width(), tipOverlay.height()
        margins =tipOverlay.layout().contentsMargins()
        
        path.addPolygon(
            QPolygonF([QPointF(w - margins.right()/2, margins.top()), 
                      QPointF(w - 1, margins.top() + 7), 
                      QPointF(w - margins.right()/2, margins.top() + 14)]))

        painter.drawPath(path.simplified())

    def position(self, tipOverlay: QCustomTipOverlay):
        target = tipOverlay.original_target
        if isinstance(target, (QPoint, QPointF)):
            # For QPoint target, place the tip with tail pointing to the point
            if isinstance(target, QPointF):
                pos = target.toPoint()
            else:
                pos = target
            
            # The tail is at position (w-1, margins.top() + 7), so adjust accordingly
            x = pos.x()  # Tip starts at the point's x position
            y = pos.y() - (margins.top() + 7)  # Adjust so tail is at point's y
            return QPoint(x, y)
        else:
            # For QWidget target, calculate position
            pos = target.mapToGlobal(QPoint(0, 0))
            x = pos.x() - tipOverlay.width()
            y = pos.y()
            return QPoint(x, y)

@QCustomTipOverlayManager.register("right-bottom")
class RightBottomTailQCustomQToolTipManager(RightTailQCustomQToolTipManager):
    """ Right bottom tail QCustomOvelay manager """

    def draw(self, tipOverlay, painter, path):
        w, h = tipOverlay.width(), tipOverlay.height()
        margins =tipOverlay.layout().contentsMargins()
        
        path.addPolygon(
            QPolygonF([QPointF(w - margins.right()/2, h - margins.top() - 14), 
                      QPointF(w - 1, h - margins.top() - 7), 
                      QPointF(w - margins.right()/2, h - margins.top())]))

        painter.drawPath(path.simplified())

    def position(self, tipOverlay: QCustomTipOverlay):
        target = tipOverlay.original_target
        if isinstance(target, (QPoint, QPointF)):
            # For QPoint target, place the tip with tail pointing to the point
            if isinstance(target, QPointF):
                pos = target.toPoint()
            else:
                pos = target
            
            # The tail is at position (w-1, h - margins.top() - 7), so adjust accordingly
            x = pos.x()  # Tip starts at the point's x position
            y = pos.y() - (tipOverlay.height() - margins.top() - 7)  # Adjust so tail is at point's y
            return QPoint(x, y)
        else:
            # For QWidget target, calculate position
            pos = target.mapToGlobal(QPoint(0, target.height()))
            x = pos.x() - tipOverlay.width()
            y = pos.y() - tipOverlay.height()
            return QPoint(x, y)

@QCustomTipOverlayManager.register("auto")
class AutoPositionQCustomQToolTipManager(QCustomTipOverlayManager):
    """ Auto-positioning QCustomOverlay manager """

    def draw(self, tipOverlay, painter, path):
        self.manager = self.createManager(tipOverlay)
        self.manager.draw(tipOverlay, painter, path)

    def position(self, tipOverlay: QCustomTipOverlay):
        manager = self.createManager(tipOverlay)
        position = manager.position(tipOverlay)
        return position
    
    def createManager(self, tipOverlay: QCustomTipOverlay):
        tip_position = self.getTipOverlay(tipOverlay)
        
        manager = QCustomTipOverlayManager.make(tip_position)
        return manager
    
    def getTipOverlay(self, tipOverlay: QCustomTipOverlay):
        # Get the current screen's available geometry
        app = QApplication.instance()
        target = tipOverlay.original_target
        
        # Get the screen where the target is located
        if isinstance(target, (QPoint, QPointF)):
            point = target
            if isinstance(point, QPointF):
                point = point.toPoint()
            screen = app.screenAt(point)
            if not screen:
                screen = app.primaryScreen()
            app_window = screen.availableGeometry()
            # Create a small virtual rectangle around the point
            point_rect = QRect(point.x() - 5, point.y() - 5, 10, 10)
            
            # For QPoint target, use the point itself as reference
            # Calculate position based on available space
        else:
            # For widget, get its geometry
            target_rect = target.geometry()
            point = target.mapToGlobal(QPoint(target_rect.width()//2, target_rect.height()//2))
            screen = app.screenAt(point)
            if not screen:
                screen = app.primaryScreen()
            app_window = screen.availableGeometry()
            point_rect = QRect(point.x() - target_rect.width()//2, point.y() - target_rect.height()//2, 
                             target_rect.width(), target_rect.height())
            
            # For widget target, use mouse cursor relative to widget
            mouse_pos = QCursor.pos()
            target_pos = target.mapFromGlobal(mouse_pos)
            rel_x = target_pos.x() / target_rect.width() if target_rect.width() > 0 else 0.5
            rel_y = target_pos.y() / target_rect.height() if target_rect.height() > 0 else 0.5
        
        # Calculate available space around the target point
        top_space = point_rect.top() - app_window.top()
        bottom_space = app_window.bottom() - point_rect.bottom()
        left_space = point_rect.left() - app_window.left()
        right_space = app_window.right() - point_rect.right()
        
        if isinstance(target, (QPoint, QPointF)):
            # For point targets, use available space only
            if bottom_space >= tipOverlay.height() and bottom_space >= top_space:
                # Try to place below the point
                if right_space >= tipOverlay.width() and right_space >= left_space:
                    return "top-left"
                elif left_space >= tipOverlay.width():
                    return "top-right"
                else:
                    return "top-center"
            elif top_space >= tipOverlay.height():
                # Try to place above the point
                if right_space >= tipOverlay.width() and right_space >= left_space:
                    return "bottom-left"
                elif left_space >= tipOverlay.width():
                    return "bottom-right"
                else:
                    return "bottom-center"
            elif right_space >= tipOverlay.width():
                # Try to place to the right
                if top_space >= tipOverlay.height() and top_space >= bottom_space:
                    return "left-top"
                elif bottom_space >= tipOverlay.height():
                    return "left-bottom"
                else:
                    return "left-center"
            elif left_space >= tipOverlay.width():
                # Try to place to the left
                if top_space >= tipOverlay.height() and top_space >= bottom_space:
                    return "right-top"
                elif bottom_space >= tipOverlay.height():
                    return "right-bottom"
                else:
                    return "right-center"
        else:
            # For widget targets, consider mouse position
            if bottom_space >= tipOverlay.height() and rel_y > 0.5:
                if right_space >= tipOverlay.width() and rel_x > 0.5:
                    return "top-left"
                elif left_space >= tipOverlay.width() and rel_x <= 0.5:
                    return "top-right"
                else:
                    return "top-center"
            
            if top_space >= tipOverlay.height() and rel_y <= 0.5:
                if right_space >= tipOverlay.width() and rel_x > 0.5:
                    return "bottom-left"
                elif left_space >= tipOverlay.width() and rel_x <= 0.5:
                    return "bottom-right"
                else:
                    return "bottom-center"
            
            if right_space >= tipOverlay.width() and rel_x > 0.5:
                if top_space >= tipOverlay.height() and rel_y <= 0.5:
                    return "left-top"
                elif bottom_space >= tipOverlay.height() and rel_y > 0.5:
                    return "left-bottom"
                else:
                    return "left-center"
            
            if left_space >= tipOverlay.width() and rel_x <= 0.5:
                if top_space >= tipOverlay.height() and rel_y <= 0.5:
                    return "right-top"
                elif bottom_space >= tipOverlay.height() and rel_y > 0.5:
                    return "right-bottom"
                else:
                    return "right-center"
        
        # Default fallback - use the side with most space
        max_space = max(top_space, bottom_space, left_space, right_space)
        if max_space == top_space:
            return "bottom-center"
        elif max_space == bottom_space:
            return "top-center"
        elif max_space == left_space:
            return "right-center"
        else:
            return "left-center"

class QCustomQToolTipFilter(QObject):
    def __init__(self, duration=1500, icon=None, tailPosition="auto"):
        super().__init__()
        self.duration = duration
        self.icon = icon
        self.tailPosition = tailPosition

    def eventFilter(self, obj, event):
        if event.type() == QEvent.ToolTip:
            tooltip_text = obj.toolTip()
            QTimer.singleShot(0, lambda: self.showCustomToolTip(tooltip_text, obj))
            return True
        try:
            return super().eventFilter(obj, event)
        except:
            return False

    def showCustomToolTip(self, text, target):
        if not text or hasattr(target, "customTooltip") and target.customTooltip is not None:
            return
        target.customTooltip = QCustomTipOverlay(text=text, target=target, duration = self.duration, tailPosition=self.tailPosition)
        target.customTooltip.show()