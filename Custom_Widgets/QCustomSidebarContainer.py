from qtpy.QtCore import Qt, QPropertyAnimation, QEasingCurve, Property, Signal, QSize
from qtpy.QtWidgets import QWidget, QStyleOption, QStyle, QSizePolicy, QGraphicsOpacityEffect
from qtpy.QtGui import QPainter, QPaintEvent

from Custom_Widgets.QCustomSidebar import QCustomSidebar 

import os

class QCustomSidebarContainer(QWidget):
    """A container widget that can hide or show its contents when the parent sidebar collapses/expands."""
    
    visibilityChanged = Signal(bool)
    script_dir = os.path.dirname(os.path.realpath(__file__))
    WIDGET_ICON = os.path.join(script_dir, "components/icons/featured_play_list.png")
    WIDGET_TOOLTIP = "A container widget that can hide or show its contents when the parent sidebar collapses/expands"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomSidebarContainer' name='customSidebarContainer'>
        </widget>
    </ui>
    """
    WIDGET_MODULE = "Custom_Widgets.QCustomSidebarContainer"

    def __init__(self, parent=None):
        super().__init__(parent)
        self._hideOnCollapse = True
        self._showOnCollapse = False
        self._isVisible = True
        self._connected = False
        self._animationDuration = 500
        
        # Set up opacity effect for animations
        self.opacityEffect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacityEffect)
        
        # Animation setup
        self.animation = QPropertyAnimation(self.opacityEffect, b"opacity")
        self.animation.setEasingCurve(QEasingCurve.InOutQuad)
        self.animation.finished.connect(self.onAnimationFinished)
        
        # Size policy
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

    def startShowAnimation(self):
        """Animate opacity from 0 to 1 and then show the widget."""
        self.setVisible(True)
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1.0)
        self.animation.setDuration(self._animationDuration)
        self.animation.start()

    def startHideAnimation(self):
        """Animate opacity from 1 to 0 and then hide the widget."""
        self.animation.setStartValue(1.0)
        self.animation.setEndValue(0.0)
        self.animation.setDuration(self._animationDuration)
        self.animation.start()

    def onAnimationFinished(self):
        """Handle the visibility of the widget after the animation finishes."""
        if self.animation.endValue() == 0.0:
            self.setVisible(False)

        self.visibilityChanged.emit(self.isVisible())

    def hideContainer(self):
        """Start the hide animation if hideOnCollapse is True."""
        if self._hideOnCollapse:
            self.startHideAnimation()
        elif self._showOnCollapse:
            # If showOnCollapse is True, we should show instead of hide
            self.startShowAnimation()

    def showContainer(self):
        """Start the show animation if hideOnCollapse is True."""
        if self._hideOnCollapse:
            self.startShowAnimation()
        elif self._showOnCollapse:
            # If showOnCollapse is True, we should hide instead of show
            self.startHideAnimation()

    def hideContainerForce(self):
        """Force hide the container regardless of hideOnCollapse/showOnCollapse settings."""
        self.startHideAnimation()

    def showContainerForce(self):
        """Force show the container regardless of hideOnCollapse/showOnCollapse settings."""
        self.startShowAnimation()

    def showEvent(self, e):
        """Handle show event."""
        super().showEvent(e)
        self.connectToParent()
        
        self.update()

    @Property(bool)
    def hideOnCollapse(self):
        """Whether to hide this container when the sidebar collapses."""
        return self._hideOnCollapse

    @hideOnCollapse.setter
    def hideOnCollapse(self, hide):
        self._hideOnCollapse = hide
        # If hideOnCollapse is set to True, ensure showOnCollapse is False
        if hide:
            self._showOnCollapse = False

    @Property(bool)
    def showOnCollapse(self):
        """Whether to show this container when the sidebar collapses (opposite of hideOnCollapse)."""
        return self._showOnCollapse

    @showOnCollapse.setter
    def showOnCollapse(self, show):
        self._showOnCollapse = show
        # If showOnCollapse is set to True, ensure hideOnCollapse is False
        if show:
            self._hideOnCollapse = False

    @Property(int)
    def animationDuration(self):
        """Get the animation duration."""
        return self._animationDuration

    @animationDuration.setter
    def animationDuration(self, duration):
        """Set the animation duration."""
        self._animationDuration = duration

    def connectToParent(self):
        """Connect to the closest QCustomSidebar parent to listen for collapse/expand signals."""
        # Only connect once
        if self._connected:
            return
            
        self.parentSidebar = self.parent()
        while self.parentSidebar and not isinstance(self.parentSidebar, QCustomSidebar):
            self.parentSidebar = self.parentSidebar.parent()

        if self.parentSidebar:
            # Connect to signals emitted on collapse/expand
            self.parentSidebar.onCollapsed.connect(self.hideContainer)
            self.parentSidebar.onExpanded.connect(self.showContainer)

            self.parentSidebar.onCollapsing.connect(self.hideContainer)
            self.parentSidebar.onExpanding.connect(self.showContainer)

            # Use parent sidebar's animation duration
            self._animationDuration = self.parentSidebar.animationDuration

            # Set initial visibility based on sidebar state
            if self.parentSidebar.isCollapsed():
                # When sidebar is collapsed initially
                if self._hideOnCollapse:
                    self.startHideAnimation()
                elif self._showOnCollapse:
                    self.startShowAnimation()
            else:
                # When sidebar is expanded initially
                if self._hideOnCollapse:
                    self.startShowAnimation()
                elif self._showOnCollapse:
                    self.startHideAnimation()
            
            self._connected = True  # Mark as connected

    def paintEvent(self, event: QPaintEvent):
        """Handle paint event."""
        opt = QStyleOption()
        opt.initFrom(self)
        painter = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, painter, self)