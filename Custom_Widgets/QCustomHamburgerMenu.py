import os
from qtpy.QtCore import Qt, QPropertyAnimation, QSize, QEvent, Property, QEasingCurve, QRect, QPoint
from qtpy.QtWidgets import (QMdiSubWindow, QWidget, QGraphicsDropShadowEffect, 
                              QVBoxLayout, QHBoxLayout, QPushButton, QStyleOption, 
                              QStyle, QLabel, QSizePolicy, QApplication)
from qtpy.QtGui import QPainter, QColor, QPaintEvent, QShowEvent
# Import your custom utilities
from Custom_Widgets.Log import *
from Custom_Widgets.Utils import replace_url_prefix, is_in_designer, get_icon_path

# Import the animation easing curve function
from Custom_Widgets.QPropertyAnimation import returnAnimationEasingCurve


class QCustomHamburgerMenu(QWidget):
    """
    A customizable hamburger menu widget for Qt Designer with four-position support.
    """
    
    script_dir = os.path.dirname(os.path.realpath(__file__))
    WIDGET_ICON = os.path.join(script_dir, "components/icons/reorder.png")
    WIDGET_TOOLTIP = "A customizable hamburger menu with four-position support"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomHamburgerMenu' name='customHamburgerMenu'>
            <property name='geometry'>
                <rect>
                    <x>0</x>
                    <y>0</y>
                    <width>300</width>
                    <height>400</height>
                </rect>
            </property>
        </widget>
    </ui>
    """
    WIDGET_MODULE = "Custom_Widgets.QCustomHamburgerMenu"
    
    # String constants for position property
    POSITION_LEFT = "Left"
    POSITION_RIGHT = "Right"
    POSITION_TOP = "Top"
    POSITION_BOTTOM = "Bottom"

    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Private attributes with default values
        self._position = self.POSITION_LEFT
        self._animationDuration = 250
        self._animationEasingCurve = "OutQuad"
        self._menuWidth = 300
        self._menuHeight = 400
        self._backgroundColor = QColor(255, 255, 255)
        self._shadowColor = QColor(0, 0, 0, 80)
        self._shadowBlurRadius = 30
        self._cornerRadius = 0
        self._autoHide = False
        self._overlayColor = QColor(0, 0, 0, 64)
        self._toggleButtonName = ""
        self._showButtonName = ""
        self._hideButtonName = ""
        self._toggleButtonConnected = None
        self._showButtonConnected = None
        self._hideButtonConnected = None
        self._menuHidden = True
        self._endGeometry = QRect(0, 0, self._menuWidth, self._menuHeight)
        self._sizeWrap = False
        self._center = False
        self._margin = 0 
        
        # Window configuration
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # Create overlay
        self.overlay = QHamburgerMenuOverlay(self)
        
        # Apply initial shadow effect
        self._updateShadowEffect()
        
        # Initialize animation
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.finished.connect(self._onAnimationFinished)
        
        # Install event filter on parent when available
        if parent:
            parent.installEventFilter(self)

        # Initialize in designer if needed
        if not is_in_designer(self):
            self.hide()
            self.hideMenu(duration=100)
    
    def _updateShadowEffect(self):
        """Update the shadow effect without CSS."""
        current_effect = self.graphicsEffect()
        if current_effect:
            current_effect.setEnabled(False)
            self.setGraphicsEffect(None)
        
        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(self._shadowBlurRadius)
        self.shadow.setColor(self._shadowColor)
        self.shadow.setOffset(0, 0)
        self.setGraphicsEffect(self.shadow)
    
    def _stringToPosition(self, position_str):
        """Convert string position to normalized format."""
        position_str = str(position_str).lower().strip()
        
        if position_str in ["left", "0"]:
            return self.POSITION_LEFT
        elif position_str in ["right", "1"]:
            return self.POSITION_RIGHT
        elif position_str in ["top", "2"]:
            return self.POSITION_TOP
        elif position_str in ["bottom", "3"]:
            return self.POSITION_BOTTOM
        else:
            return self.POSITION_LEFT

    def adjustSizeToContent(self):
        """Adjust size to fit content and update positioning."""
        if not self.parent() or is_in_designer(self):
            return
            
        # Calculate the size hint based on the content
        content_size = self.sizeHint()
        
        # Automatically resize to fit content
        self.adjustSize()
        
        # Update dimensions for sizeWrap - ALWAYS use content size when sizeWrap is True
        if self._sizeWrap:
            # For ALL positions, use content size instead of parent dimensions
            self._menuWidth = content_size.width()
            self._menuHeight = content_size.height()
        
        self._updatePosition()

    def _calculateMenuGeometry(self, parent_rect, is_hidden=False):
        """Calculate menu geometry based on current settings."""
        # Calculate actual dimensions based on sizeWrap
        if self._sizeWrap:
            # When sizeWrap is True, ALWAYS use menuWidth/menuHeight (which are set to content size)
            actual_width = self._menuWidth
            actual_height = self._menuHeight
        else:
            # When sizeWrap is False, use parent dimensions for top/bottom positions
            actual_width = self._menuWidth if self._position in [self.POSITION_LEFT, self.POSITION_RIGHT] else parent_rect.width()
            actual_height = self._menuHeight if self._position in [self.POSITION_TOP, self.POSITION_BOTTOM] else parent_rect.height()

        # Calculate positioning with center option
        if self._position == self.POSITION_LEFT:
            if self._center:
                y_pos = (parent_rect.height() - actual_height) // 2
            else:
                y_pos = self._margin
            if is_hidden:
                return QRect(-actual_width, y_pos, actual_width, actual_height)
            else:
                return QRect(self._margin, y_pos, actual_width, actual_height)

        elif self._position == self.POSITION_RIGHT:
            if self._center:
                y_pos = (parent_rect.height() - actual_height) // 2
            else:
                y_pos = self._margin
            if is_hidden:
                return QRect(parent_rect.width(), y_pos, actual_width, actual_height)
            else:
                return QRect(parent_rect.width() - actual_width - self._margin, y_pos, actual_width, actual_height)

        elif self._position == self.POSITION_TOP:
            if self._center:
                x_pos = (parent_rect.width() - actual_width) // 2
            else:
                x_pos = self._margin
            if is_hidden:
                return QRect(x_pos, -actual_height, actual_width, actual_height)
            else:
                return QRect(x_pos, self._margin, actual_width, actual_height)

        elif self._position == self.POSITION_BOTTOM:
            if self._center:
                x_pos = (parent_rect.width() - actual_width) // 2
            else:
                x_pos = self._margin
            if is_hidden:
                return QRect(x_pos, parent_rect.height(), actual_width, actual_height)
            else:
                return QRect(x_pos, parent_rect.height() - actual_height - self._margin, actual_width, actual_height)

        return QRect(0, 0, actual_width, actual_height)

    # Property getters and setters
    @Property(str)
    def position(self):
        return self._position
    
    @position.setter
    def position(self, value):
        normalized_position = self._stringToPosition(value)
        
        if normalized_position in [self.POSITION_LEFT, self.POSITION_RIGHT, 
                                 self.POSITION_TOP, self.POSITION_BOTTOM]:
            self._position = normalized_position
            self._updatePosition()
        else:
            raise ValueError('Position must be "Left", "Right", "Top", or "Bottom"')
    
    @Property(int)
    def animationDuration(self):
        return self._animationDuration
    
    @animationDuration.setter
    def animationDuration(self, value):
        if value > 0:
            self._animationDuration = value
        else:
            raise ValueError("Animation duration must be positive")
    
    @Property(str)
    def animationEasingCurve(self):
        return self._animationEasingCurve
    
    @animationEasingCurve.setter
    def animationEasingCurve(self, value):
        self._animationEasingCurve = value
       
    @Property(int)
    def menuWidth(self):
        return self._menuWidth
    
    @menuWidth.setter
    def menuWidth(self, value):
        if value > 0:
            self._menuWidth = value
            # Only update position if sizeWrap is False
            if not self._sizeWrap:
                self._updatePosition()
        else:
            raise ValueError("Menu width must be positive")
    
    @Property(int)
    def menuHeight(self):
        return self._menuHeight
    
    @menuHeight.setter
    def menuHeight(self, value):
        if value > 0:
            self._menuHeight = value
            # Only update position if sizeWrap is False
            if not self._sizeWrap:
                self._updatePosition()
        else:
            raise ValueError("Menu height must be positive")
    
    @Property(bool)
    def sizeWrap(self):
        return self._sizeWrap
    
    @sizeWrap.setter
    def sizeWrap(self, value):
        self._sizeWrap = bool(value)
        if self._sizeWrap:
            # When enabling sizeWrap, adjust to content
            self.adjustSizeToContent()
        else:
            # When disabling sizeWrap, revert to configured dimensions
            self._updatePosition()
    
    @Property(bool)
    def center(self):
        return self._center
    
    @center.setter
    def center(self, value):
        self._center = bool(value)
        self._updatePosition()
    
    @Property(int)
    def margin(self):
        return self._margin
    
    @margin.setter
    def margin(self, value):
        self._margin = max(0, value)
        self._updatePosition()
    
    @Property(QColor)
    def backgroundColor(self):
        return self._backgroundColor
    
    @backgroundColor.setter
    def backgroundColor(self, value):
        self._backgroundColor = value
    
    @Property(QColor)
    def shadowColor(self):
        return self._shadowColor
    
    @shadowColor.setter
    def shadowColor(self, value):
        self._shadowColor = value
        self._updateShadowEffect()
    
    @Property(int)
    def shadowBlurRadius(self):
        return self._shadowBlurRadius
    
    @shadowBlurRadius.setter
    def shadowBlurRadius(self, value):
        self._shadowBlurRadius = value
        self._updateShadowEffect()
    
    @Property(int)
    def cornerRadius(self):
        return self._cornerRadius
    
    @cornerRadius.setter
    def cornerRadius(self, value):
        self._cornerRadius = max(0, value)
    
    @Property(bool)
    def autoHide(self):
        return self._autoHide
    
    @autoHide.setter
    def autoHide(self, value):
        self._autoHide = bool(value)
    
    @Property(QColor)
    def overlayColor(self):
        return self._overlayColor
    
    @overlayColor.setter
    def overlayColor(self, value):
        self._overlayColor = value
        if hasattr(self, 'overlay'):
            self.overlay.updateOverlayColor()
    
    @Property(str)
    def toggleButtonName(self):
        return self._toggleButtonName
    
    @toggleButtonName.setter
    def toggleButtonName(self, name):
        self._toggleButtonName = name
        toggleButton = self.getButtonByName(name)

        if self._toggleButtonConnected:
            self._toggleButtonConnected.disconnect()

        if toggleButton:
            toggleButton.clicked.connect(self.toggleMenu)
            self._toggleButtonConnected = toggleButton
        
        else:
            logWarning(f"Toggle button '{name}' not found in parent hierarchy.")
    
    @Property(str)
    def showButtonName(self):
        return self._showButtonName
    
    @showButtonName.setter
    def showButtonName(self, name):
        self._showButtonName = name
        showButton = self.getButtonByName(name)
    
        if self._showButtonConnected:
            self._showButtonConnected.disconnect()

        if showButton:
            showButton.clicked.connect(self.showMenu)
            self._showButtonConnected = showButton

        else:
            logWarning(f"Show button '{name}' not found in parent hierarchy.")
    
    @Property(str)
    def hideButtonName(self):
        return self._hideButtonName
    
    @hideButtonName.setter
    def hideButtonName(self, name):
        self._hideButtonName = name
        hideButton = self.getButtonByName(name)
    
        if self._hideButtonConnected:
            self._hideButtonConnected.disconnect()
        
        if hideButton:
            hideButton.clicked.connect(self.hideMenu)
            self._hideButtonConnected = hideButton

        
        else:
            logWarning(f"Hide button '{name}' not found in parent hierarchy.")

    def _updatePosition(self):
        """Update the menu position and size based on current settings."""
        if not self.parent() or is_in_designer(self):
            return

        # Do NOT override geometry while animating
        if self.animation.state() == QPropertyAnimation.Running:
            return

        parent_rect = self.parent().rect()

        # Calculate geometry based on current state
        if self._menuHidden:
            geometry = self._calculateMenuGeometry(parent_rect, is_hidden=True)
        else:
            geometry = self._calculateMenuGeometry(parent_rect, is_hidden=False)

        self.setGeometry(geometry)
        self._endGeometry = geometry

    
    def showMenu(self):
        """Animate the menu opening towards center."""
        if not self.parent() and not is_in_designer(self):
            return
            
        if is_in_designer(self):
            self.show()
            return
        
        self._menuHidden = False
        
        # Adjust size to content if sizeWrap is enabled
        if self._sizeWrap:
            self.adjustSizeToContent()
        
        # Stop any ongoing animation
        if self.animation.state() == QPropertyAnimation.Running:
            self.animation.stop()
            
        parent_rect = self.parent().rect()
        
        # Calculate start and end geometries
        start_geometry = self._calculateMenuGeometry(parent_rect, is_hidden=True)
        end_geometry = self._calculateMenuGeometry(parent_rect, is_hidden=False)
        
        # Set initial position
        self.setGeometry(start_geometry)
        self.show()
        
        # Show and position overlay FIRST (so it's at the bottom)
        if self.parent():
            self.overlay.setParent(self.parent())
            self.overlay.setGeometry(0, 0, parent_rect.width(), parent_rect.height())
            self.overlay.show()
            
            # CRITICAL: Ensure menu is on top of overlay
            self.raise_()
        
        # Animate opening
        self.animation.setDuration(self._animationDuration)
        self.animation.setEasingCurve(returnAnimationEasingCurve(self._animationEasingCurve))
        self.animation.setStartValue(start_geometry)
        self.animation.setEndValue(end_geometry)
        self._endGeometry = end_geometry
        self.animation.start()
    
    def hideMenu(self, duration=None):
        """Animate the menu closing away from center."""
        if not self.parent() and not is_in_designer(self):
            return
            
        if is_in_designer(self):
            return
        
        self._menuHidden = True
        
        # Stop any ongoing animation
        if self.animation.state() == QPropertyAnimation.Running:
            self.animation.stop()
            
        parent_rect = self.parent().rect()
        
        # Calculate end geometry
        start_geometry = self.geometry()
        end_geometry = self._calculateMenuGeometry(parent_rect, is_hidden=True)
        
        # Animate closing
        self.animation.setDuration(duration if duration is not None else self._animationDuration)
        self.animation.setEasingCurve(returnAnimationEasingCurve(self._animationEasingCurve))
        self.animation.setStartValue(start_geometry)
        self.animation.setEndValue(end_geometry)
        self._endGeometry = end_geometry
        self.animation.start()
    
    def _onAnimationFinished(self):
        """Handle animation completion."""
        if self.animation.state() == QPropertyAnimation.Running:
            return

        if self._menuHidden:
            self.hide()
            self.overlay.hide()
            
        self._updatePosition()

    def toggleMenu(self):
        """Toggle the menu visibility."""
        if self._menuHidden:
            self.showMenu()
        else:
            self.hideMenu()

    def getButtonByName(self, buttonName):
        """Recursively search for a button by objectName."""
        button_classes = [QPushButton]

        try:
            from Custom_Widgets.QCustomSidebarButton import QCustomSidebarButton
            button_classes.append(QCustomSidebarButton)
        except ImportError:
            pass

        def search_children(widget):
            if widget.objectName() == buttonName and isinstance(widget, tuple(button_classes)):
                return widget
            for child in widget.children():
                if isinstance(child, QWidget):
                    result = search_children(child)
                    if result:
                        return result
            return None

        def search_parents(widget):
            parent = widget.parent()
            while parent:
                if parent.objectName() == buttonName and isinstance(parent, tuple(button_classes)):
                    return parent
                result = search_children(parent)
                if result:
                    return result
                parent = parent.parent()
            return None

        result = search_children(self)
        if result:
            return result

        return search_parents(self)
    
    def getWidget(self, name: str) -> QWidget:
        try:
            # Validate input
            if not name or not isinstance(name, str):
                raise ValueError("Widget name must be a non-empty string")
            
            # Find the widget
            widget = self.findChild(QWidget, name)
            
            if not widget:
                logWarning(f"Widget '{name}' not found in {self.objectName() or self.__class__.__name__}")
                return None
                
            return widget
            
        except ValueError as e:
            logError(f"Invalid widget name: {e}")
            raise
        except Exception as e:
            logError(f"Unexpected error while finding widget '{name}': {str(e)}")
            return None
    
    def event(self, event):
        """Handle general events."""
        if event.type() == QEvent.ParentChange:
            self._handleParentChange()
        
        return super().event(event)

    def _handleParentChange(self):
        """Handle parent change events."""
        if self.parent() and not is_in_designer(self):
            self.parent().installEventFilter(self)
            self._updatePosition()
            if hasattr(self, 'overlay'):
                self.overlay.setParent(self.parent())

    def paintEvent(self, paintEvent: QPaintEvent) -> None:
        """Paint the widget with proper styling."""
        opt = QStyleOption()
        opt.initFrom(self)
        painter = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, painter, self)

        return super().paintEvent(paintEvent)
    
    def showEvent(self, event: QShowEvent) -> None:
        """Handle show events to update position."""
        # Adjust size to content when shown if sizeWrap is enabled
        if self._sizeWrap:
            self.adjustSizeToContent()
        return super().showEvent(event)
    
    def eventFilter(self, obj, event):
        """Handle parent resize events to adjust menu and overlay size."""
        if obj == self.parent() and event.type() in [QEvent.Resize, QEvent.LayoutRequest]:
            self._updatePosition()
            if self.overlay:
                self.overlay.setGeometry(0, 0, self.parent().width(), self.parent().height())
        return super().eventFilter(obj, event)


class QHamburgerMenuOverlay(QWidget):
    """Overlay that covers the main content when the hamburger menu is open."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.hamburgerMenu = parent
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.hide()
        
    def setParent(self, parent):
        """Set the parent widget and install event filter."""
        super().setParent(parent)
        if parent:
            parent.installEventFilter(self)
        
    def updateOverlayColor(self):
        """Update the overlay color from parent menu."""
        if self.hamburgerMenu:
            color = self.hamburgerMenu.overlayColor
            # Use stylesheet for proper rendering
            self.setStyleSheet(f"""
                background-color: rgba({color.red()}, {color.green()}, {color.blue()}, {color.alpha()});
            """)
            self.update()

    def eventFilter(self, obj, event):
        """Handle parent resize events to adjust overlay size."""
        if obj == self.parent() and event.type() in [QEvent.Resize, QEvent.LayoutRequest]:
            if self.parent():
                self.setGeometry(0, 0, self.parent().width(), self.parent().height())
        return super().eventFilter(obj, event)
    
    def paintEvent(self, event):
        """Paint the overlay with proper styling."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Use the overlay color
        if self.hamburgerMenu:
            color = self.hamburgerMenu.overlayColor
            painter.fillRect(self.rect(), color)
        
        painter.end()
    
    def mousePressEvent(self, event):
        """Close the hamburger menu when overlay is clicked."""
        if self.hamburgerMenu:
            self.hamburgerMenu.hideMenu()
    
    def showEvent(self, event):
        """Setup when overlay is shown."""
        self.updateOverlayColor()
        if self.parent():
            self.setGeometry(0, 0, self.parent().width(), self.parent().height())
        
        return super().showEvent(event)