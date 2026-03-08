from qtpy.QtCore import Qt, QEvent, QPropertyAnimation, QEasingCurve, Property, Signal, QSize, QPoint, QTimer, QCoreApplication
from qtpy.QtWidgets import QPushButton, QWidget, QLabel, QStyleOption, QStyle, QHBoxLayout, QVBoxLayout, QSizePolicy, QGraphicsOpacityEffect, QSpacerItem, QApplication, QGraphicsDropShadowEffect
from qtpy.QtGui import QPainter, QIcon, QPaintEvent, QEnterEvent, QMouseEvent, QHoverEvent, QColor, QCursor
import os

# Import your custom sidebar and utility functions
from Custom_Widgets.QCustomSidebar import QCustomSidebar 
from Custom_Widgets.Utils import replace_url_prefix, is_in_designer, get_icon_path
from Custom_Widgets.Log import *

class QCustomSidebarButton(QPushButton):
    clicked = Signal()

    # Define XML for Qt Designer
    script_dir = os.path.dirname(os.path.realpath(__file__))
    WIDGET_ICON = os.path.join(script_dir, "components/icons/arrow_forward.png")
    WIDGET_TOOLTIP = "A custom button that interacts with the sidebar"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomSidebarButton' name='customSidebarButton'>
        </widget>
    </ui>
    """
    WIDGET_MODULE = "Custom_Widgets.QCustomSidebarButton"

    def __init__(self, parent=None, *args):
        super().__init__(parent)

        # Install event filter for the whole application
        app = QCoreApplication.instance()
        if app is not None:
            app.installEventFilter(self)
        elif self.parent():
            self.parent().installEventFilter(self)

        # Store original text and icon for resetting
        self.originalText = ""
        self.originalIcon = self.icon()
        self._labelHidden = False
        self._hideOnCollapse = True
        self._showOnCollapse = False  # Opposite of hideOnCollapse
        self._textPrefixSpaces = 5

        self._fadingOut = False

        self._isHovered = False
        self._floatingWidget = None
        self._hoverTimer = QTimer(self)
        self._hoverTimer.setSingleShot(True)
        self._hoverTimer.timeout.connect(self.showFloatingButton)
        self._floatPosition = None

    @Property(bool)
    def hideOnCollapse(self):
        """Whether to hide this label when the sidebar collapses."""
        return self._hideOnCollapse

    @hideOnCollapse.setter
    def hideOnCollapse(self, hide):
        # If setting to True, ensure showOnCollapse is False
        if hide:
            self._showOnCollapse = False
        self._hideOnCollapse = hide
        self.update()

    @Property(bool)
    def showOnCollapse(self):
        """Whether to show this label when the sidebar collapses (opposite of hideOnCollapse)."""
        return self._showOnCollapse

    @showOnCollapse.setter
    def showOnCollapse(self, show):
        # If setting to True, ensure hideOnCollapse is False
        if show:
            self._hideOnCollapse = False
        self._showOnCollapse = show
        self.update()

    @Property(int)
    def textPrefixSpaces(self):
        """Get number of spaces to prepend to the text."""
        return self._textPrefixSpaces

    @textPrefixSpaces.setter
    def textPrefixSpaces(self, numSpaces):
        """Set number of spaces to prepend to the text."""
        self._textPrefixSpaces = numSpaces
        self.update()

    # Define the property for labelHidden state
    @Property(bool)
    def labelHidden(self, designable=False):
        return self._labelHidden

    @labelHidden.setter
    def labelHidden(self, state):
        self._labelHidden = state
        self.style().unpolish(self)  # Refresh style
        self.style().polish(self)
        self.update()

    @Property(str, designable=True)
    def labelText(self):
        """Returns the label text for the button (read-only)."""
        return self.originalText or ""

    @labelText.setter
    def labelText(self, text):
        """Sets the original label text for the button."""
        self.originalText = text
        self.update()

    @property
    def text(self):
        return super().text()

    @text.setter
    def text(self, value):
        super().setText(value or 'Sidebar Button')

    def paintEvent(self, event: QPaintEvent):
        """Custom paint event to draw the button with opacity."""
        opt = QStyleOption()
        opt.initFrom(self)
        painter = QPainter(self)
        self.style().drawControl(QStyle.CE_PushButton, opt, painter, self)

        if self.originalText and not self.labelHidden:  
            self.setText(self.originalText) 
        elif self.labelHidden:
            self.setText("**clear")

        self.update()
        super().paintEvent(event) 

    def setText(self, text):
        """Override setText to store the raw text and apply the prefix spaces."""
        if text == "**clear":
            super().setText("")
        else:
            if self.originalText != text:
                self.labelText = text
            super().setText(self.getPrefixedText(text))

    def update(self):
        if self.originalText and not self.labelHidden:  
            self.setText(self.originalText) 
        elif self.labelHidden:
            self.setText("**clear")
        super().update()

    def getPrefixedText(self, text):
        return " " * self._textPrefixSpaces + text.lstrip()

    def connectToParent(self):
        """Connect to the closest QCustomSidebar parent if necessary."""
        self.parentSidebar = self.parent()  # Start with the direct parent
        while self.parentSidebar and not isinstance(self.parentSidebar, QCustomSidebar):
            self.parentSidebar = self.parentSidebar.parent()  # Move up the hierarchy

        if self.parentSidebar:
            self.parentSidebar.onCollapsed.connect(self.hideButtonLabel)
            self.parentSidebar.onExpanded.connect(self.showButtonLabel)

            self.parentSidebar.onCollapsing.connect(self.showButtonLabel)
            self.parentSidebar.onExpanding.connect(self.showButtonLabel)

            if self.parentSidebar and self.parentSidebar.isCollapsed():
                # Check if we should show or hide based on the properties
                if self._hideOnCollapse:
                    self.hideButtonLabel()
                elif self._showOnCollapse:
                    self.showButtonLabel()
            else:
                self.showButtonLabel()

    def hideButtonLabel(self):
        """Hide the button label by clearing the text."""
        try:
            if not self.originalText:
                self.originalText = self.text()
        except:
            pass
        
        if self.originalText:
            self.setText("**clear")  # Clear the button text
            self.labelHidden = True

        # Set the custom property for labelHidden state
        self.labelHidden = True

    def hideButtonIcon(self):
        """Hide the button icon by setting it to an empty QIcon."""
        self.originalIcon = self.icon()
        self.setIcon(QIcon())  # Set an empty icon

    def showButtonLabel(self):
        """Show the button label by restoring the original text."""
        if self.originalText:  # Check if there is original text to show
            self.setText(self.originalText)  # Restore the original text
            self.labelHidden = False

        # Unset the custom property for labelHidden state
        self.labelHidden = False
        self.fadeOutFloatingButton()

    def showButtonIcon(self):
        """Show the button icon by restoring the original icon."""
        if not self.originalIcon.isNull():  # Check if there is an original icon to show
            self.setIcon(self.originalIcon)  # Restore the original icon

    def showEvent(self, e):
        super().showEvent(e)
        self.connectToParent()
        # Adjust size and update the widget
        self.update()

        try:
            if self.parentSidebar and self.parentSidebar.isCollapsed():
                # Check if we should show or hide based on the properties
                if self._hideOnCollapse and not self.labelHidden:
                    self.hideButtonLabel()
                elif self._showOnCollapse and self.labelHidden:
                    self.showButtonLabel()
            if self.parentSidebar and self.parentSidebar.isExpanded():
                if self.labelHidden:
                    self.showButtonLabel()
        except Exception as e:
            logException(e)

    def enterEvent(self, event: QEnterEvent):
        """Show the button label when the button is hovered, even if the sidebar is collapsed."""
        # Only show floating button if hideOnCollapse is True (normal behavior)
        if self.parentSidebar and (self.parentSidebar.isCollapsed() or not self.parentSidebar.isExpanded()):
            if self._hideOnCollapse:  # Only show floating button if button is hidden on collapse
                self._hoverTimer.start(2000)
        super().enterEvent(event)

    def leaveEvent(self, event):
        """Handle mouse leave event to set _isHovered to False."""
        # Only trigger fade out if hideOnCollapse is True
        if self._hideOnCollapse:
            self.fadeOutFloatingButton()
        super().leaveEvent(event)

    def deleteFloatingButton(self, e):
        """Hide the button label when the hover ends, return to original collapsed state."""
        if self._floatingWidget:
            self.fadeOutFloatingButton()  # Fade out the floating button
        self._hoverTimer.stop()  # Cancel any hover event in progress

    def showFloatingButton(self):
        """Show the floating button only if the mouse is still over the main button."""
        # Only show floating button if hideOnCollapse is True
        if not self._hideOnCollapse:
            return
            
        if not self.labelHidden:
            return
        # Check if the mouse is still over the main button
        if not self.rect().contains(self.mapFromGlobal(QCursor.pos())):
            return  # Mouse is no longer hovering over the button, so don't show the floating button

        # If mouse is still over the button, create and display the floating button
        if not self._floatingWidget:
            self.createFloatingButton()
            self._floatingWidget.show()
            self._floatingWidget.setMinimumSize(self._floatingWidget.sizeHint())
            self._floatingButton.adjustSize()
            self._floatingWidget.adjustSize()
            self._floatingWidget.move(self.calculateFloatingPosition())

    def createFloatingButton(self):
        """Create the floating version of the button."""
        # Create a QWidget as the container
        self._floatingWidget = QWidget(self)
        self._floatingWidget.setObjectName("floatingButtonWidget") #for css styling
        
        # Create the QPushButton
        self._floatingButton = QCustomSidebarButton(" " * self._textPrefixSpaces + self.originalText, self._floatingWidget)
        self._floatingWidget.hideOnCollapse = False
        self._floatingButton.setIcon(self.icon())
        self._floatingButton.setObjectName(self.objectName())

        # Create the shadow effect
        shadow = QGraphicsDropShadowEffect(self._floatingButton)
        shadow.setBlurRadius(10)  # Set the blur radius for the shadow
        shadow.setColor(QColor(0, 0, 0, 160))  # Set the shadow color (can be customized)
        shadow.setOffset(0, 0)  # Set the offset for the shadow (horizontal, vertical)

        # Apply the shadow effect to the widget
        self._floatingButton.setGraphicsEffect(shadow)
        
        # Create a QVBoxLayout
        layout = QVBoxLayout(self._floatingWidget)
        layout.addWidget(self._floatingButton)
        
        # Set the layout margins and spacing to zero
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(0)

        # Set the widget's layout
        self._floatingWidget.setLayout(layout)
        # Raise the widget to the front
        self._floatingWidget.raise_()
        self._floatingWidget.setAttribute(Qt.WA_TranslucentBackground, True)
        self._floatingWidget.setWindowFlags(Qt.FramelessWindowHint | Qt.ToolTip | Qt.Popup)

        # 
        self._floatingButton.showEvent = self.fadeInFloatingButton

        # Connect events from the floating button to the main button's event handlers
        self._floatingButton.mousePressEvent = self.mousePressEvent
        self._floatingButton.mouseReleaseEvent = self.mouseReleaseEvent
        self._floatingButton.enterEvent = self.enterEvent
        self._floatingButton.leaveEvent = self.leaveEvent

        self._fadingOut = False

    def passEventToMainButton(self, event):
        """Pass all events from the floating button to the main button."""
        # Forward the event to the main button
        return super(QPushButton, self._floatingButton).event(event)

    def fadeInFloatingButton(self, e=None):
        """Fade in the floating button."""
        if self._floatingWidget and not self._fadingOut:
            # fade animation
            # Create opacity effect and animation
            self._opacityEffect = QGraphicsOpacityEffect(self)
            self._opacityEffect.setOpacity(0.0)  # start transparent
            self.setGraphicsEffect(self._opacityEffect)
            
            self._opacityAni = QPropertyAnimation(self._opacityEffect, b"opacity", self)
            self._opacityAni.setEasingCurve(QEasingCurve.OutCubic)
            self._opacityAni.setDuration(500)
            self._opacityAni.setStartValue(0)
            self._opacityAni.setEndValue(1)
            self._opacityAni.start()

    def fadeOutFloatingButton(self):
        """Fade out the floating button."""
        if self._fadingOut:
            return

        if self._floatingWidget:
            self._fadingOut = True
            # fade animation
            # Create opacity effect and animation
            self._opacityEffect = QGraphicsOpacityEffect(self)
            self._opacityEffect.setOpacity(0.0)  # start transparent
            self.setGraphicsEffect(self._opacityEffect)
            
            self._opacityAni = QPropertyAnimation(self._opacityEffect, b"opacity", self)
            self._opacityAni.setEasingCurve(QEasingCurve.OutCubic)
            self._opacityAni.setDuration(500)
            self._opacityAni.setStartValue(1)
            self._opacityAni.setEndValue(0)
            self._opacityAni.finished.connect(self.hideFloatingButton)
            self._opacityAni.start()

    def hideFloatingButton(self):
        """Hide the floating button after the fade-out."""
        if self._floatingWidget:
            self._floatingWidget.hide()  # Hide the button
            self._floatingWidget.deleteLater()  # Schedule for deletion
            self._floatingWidget = None  # Clear reference

    def calculateFloatingPosition(self):
        """Calculate the exact relative position for the floating button."""
        # Get the position of the main button relative to its parent 
        floatingButtonPos = self.mapToGlobal(QPoint(-10, -10))
        return floatingButtonPos

    def resizeEvent(self, event):
        """Update floating button position on window resize."""
        if self._floatingWidget:
            self._floatingWidget.move(self.calculateFloatingPosition())
        super().resizeEvent(event)

    def moveEvent(self, event):
        """Update floating button position on window move."""
        if self._floatingWidget:
            self._floatingWidget.move(self.calculateFloatingPosition())
        super().moveEvent(event)

    def eventFilter(self, obj, event: QEvent):
        if event.type() in (QEvent.MouseButtonPress, QEvent.MouseButtonRelease, QEvent.MouseButtonDblClick, QEvent.MouseMove):
            # Handle the mouse event here
            localPos = self.mapFromGlobal(event.globalPos())
            if hasattr(self, "_floatingWidget") and self._floatingWidget and not self._floatingButton.rect().contains(localPos):
                self.fadeOutFloatingButton()

        return super().eventFilter(obj, event)