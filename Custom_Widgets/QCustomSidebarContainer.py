from qtpy.QtCore import Qt, QPropertyAnimation, QEasingCurve, Property, Signal, QSize
from qtpy.QtWidgets import QWidget, QStyleOption, QStyle, QSizePolicy, QGraphicsOpacityEffect
from qtpy.QtGui import QPainter, QPaintEvent

from Custom_Widgets.QCustomSidebar import QCustomSidebar 
from Custom_Widgets.Utils import is_in_designer

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

    # Rich editors for the Designer "Custom Properties" dock (see
    # DesignerTools.CustomPropertiesDock).
    DESIGNER_CUSTOM_PROPS = [
        {"name": "hideOnCollapse", "kind": "bool", "group": "Sidebar"},
        {"name": "showOnCollapse", "kind": "bool", "group": "Sidebar"},
        {"name": "animationDuration", "kind": "int", "group": "Animation"},
    ]

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

    def startShowAnimation(self):
        """Animate opacity from 0 to 1 and then show the widget."""
        # Skip in designer mode
        if is_in_designer(self):
            self.setVisible(True)
            return
            
        self.setVisible(True)
        self.updateGeometry()
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1.0)
        self.animation.setDuration(self._animationDuration)
        self.animation.start()

    def startHideAnimation(self):
        """Animate opacity from 1 to 0 and then hide the widget."""
        # Skip in designer mode
        if is_in_designer(self):
            self.setVisible(False)
            return
            
        self.animation.setStartValue(1.0)
        self.animation.setEndValue(0.0)
        self.animation.setDuration(self._animationDuration)
        self.animation.start()

    def onAnimationFinished(self):
        if self.animation.endValue() == 0.0:
            self.setVisible(False)
        else:
            self.setVisible(True)
            self._adjustToContent()

        self.visibilityChanged.emit(self.isVisible())

    def _adjustToContent(self):
        if not self.layout():
            return
        
        # Skip in designer mode to prevent crashes
        if is_in_designer(self):
            return

        try:
            size = self.layout().sizeHint()
            # Enforce minimum to prevent squeezing
            self.setMinimumSize(size)
            # Let Qt compute final size properly
            self.adjustSize()
            
            # Force parent layout refresh with safety checks
            if self.parentWidget():
                parent_layout = self.parentWidget().layout()
                if parent_layout is not None:
                    try:
                        parent_layout.activate()
                    except (RuntimeError, AttributeError):
                        # Layout might be deleted, just ignore
                        pass
        except (RuntimeError, AttributeError):
            # Layout or parent might be deleted, just ignore
            pass

    def minimumSizeHint(self):
        if self.layout():
            return self.layout().minimumSize()
        return super().minimumSizeHint()

    def hideContainer(self):
        """Start the hide animation if hideOnCollapse is True."""
        # Skip in designer mode
        if is_in_designer(self):
            return
            
        if self._hideOnCollapse:
            self.startHideAnimation()
        elif self._showOnCollapse:
            self.startShowAnimation()

    def showContainer(self):
        """Start the show animation if hideOnCollapse is True."""
        # Skip in designer mode
        if is_in_designer(self):
            return
            
        if self._hideOnCollapse:
            self.startShowAnimation()
        elif self._showOnCollapse:
            self.startHideAnimation()

    def hideContainerForce(self):
        """Force hide the container regardless of hideOnCollapse/showOnCollapse settings."""
        if is_in_designer(self):
            self.setVisible(False)
            return
        self.startHideAnimation()

    def showContainerForce(self):
        """Force show the container regardless of hideOnCollapse/showOnCollapse settings."""
        if is_in_designer(self):
            self.setVisible(True)
            return
        self.startShowAnimation()

    def showEvent(self, e):
        """Handle show event."""
        super().showEvent(e)
        
        # Skip designer mode to prevent crashes
        if is_in_designer(self):
            return
            
        self.connectToParent()
        self._adjustToContent()
        self.update()

    @Property(bool)
    def hideOnCollapse(self):
        """Whether to hide this container when the sidebar collapses."""
        return self._hideOnCollapse

    @hideOnCollapse.setter
    def hideOnCollapse(self, hide):
        self._hideOnCollapse = hide
        if hide:
            self._showOnCollapse = False

    @Property(bool)
    def showOnCollapse(self):
        """Whether to show this container when the sidebar collapses (opposite of hideOnCollapse)."""
        return self._showOnCollapse

    @showOnCollapse.setter
    def showOnCollapse(self, show):
        self._showOnCollapse = show
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
        # Skip in designer mode
        if is_in_designer(self):
            return
            
        # Only connect once
        if self._connected:
            return
            
        self.parentSidebar = self.parent()
        while self.parentSidebar and not isinstance(self.parentSidebar, QCustomSidebar):
            self.parentSidebar = self.parentSidebar.parent()

        if self.parentSidebar:
            try:
                # Connect to signals emitted on collapse/expand
                self.parentSidebar.onCollapsed.connect(self.hideContainer)
                self.parentSidebar.onExpanded.connect(self.showContainer)

                self.parentSidebar.onCollapsing.connect(self.hideContainer)
                self.parentSidebar.onExpanding.connect(self.showContainer)

                # Use parent sidebar's animation duration
                self._animationDuration = self.parentSidebar.animationDuration

                # Set initial visibility based on sidebar state
                if self.parentSidebar.isCollapsed():
                    if self._hideOnCollapse:
                        self.startHideAnimation()
                    elif self._showOnCollapse:
                        self.startShowAnimation()
                else:
                    if self._hideOnCollapse:
                        self.startShowAnimation()
                    elif self._showOnCollapse:
                        self.startHideAnimation()
                
                self._connected = True
            except (RuntimeError, AttributeError):
                # Parent sidebar might be partially destroyed
                pass

    def paintEvent(self, event: QPaintEvent):
        """Handle paint event."""
        opt = QStyleOption()
        opt.initFrom(self)
        painter = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, painter, self)