# QCustomFlowWidget.py

from qtpy import QtCore, QtWidgets
from qtpy.QtCore import Property, QSize
from qtpy.QtWidgets import QWidget, QSizePolicy
import os

from Custom_Widgets.QCustomFlowLayout import QCustomFlowLayout


class QCustomFlowWidget(QWidget):
    """
    A container widget that uses QCustomFlowLayout internally.
    Fully customizable in Qt Designer with properties for:
    - spacing (horizontal/vertical)
    - margins
    - animation settings
    
    Also properly manages existing child widgets when loaded from Qt Designer.
    """
    
    # Qt Designer integration properties
    script_dir = os.path.dirname(os.path.realpath(__file__))
    WIDGET_ICON = os.path.join(script_dir, "components/icons/flow_layout.png")
    WIDGET_TOOLTIP = "A flow layout container widget with smooth animations"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomFlowWidget' name='customFlowWidget'>
            <property name="geometry">
                <rect>
                    <x>0</x>
                    <y>0</y>
                    <width>400</width>
                    <height>300</height>
                </rect>
            </property>
            <property name="spacing">
                <number>10</number>
            </property>
            <property name="horizontalSpacing">
                <number>10</number>
            </property>
            <property name="verticalSpacing">
                <number>10</number>
            </property>
            <property name="margin">
                <number>10</number>
            </property>
            <property name="animationEnabled">
                <bool>true</bool>
            </property>
            <property name="animationDuration">
                <number>300</number>
            </property>
            <property name="animationEasingCurve">
                <string>OutCubic</string>
            </property>
            <property name="justifySpacing">
                <bool>true</bool>
            </property>
            <property name="autoFillWidth">
                <bool>false</bool>
            </property>
            <property name="autoFillHeight">
                <bool>false</bool>
            </property>
        </widget>
    </ui>
    """
    WIDGET_MODULE = "Custom_Widgets.QCustomFlowWidget"

    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Flag to prevent recursive adoption
        self._adoptingChildren = False
        
        # Create the flow layout
        self._flowLayout = QCustomFlowLayout(self, margin=10, spacing=10, animate=True)
        
        # Set this widget as the container for the layout
        self.setLayout(self._flowLayout)
        
        # Set size policy to expand both directions
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        # Store property values for Designer access
        self._spacing = 10
        self._horizontalSpacing = 10
        self._verticalSpacing = 10
        self._margin = 10
        self._animationEnabled = True
        self._animationDuration = 300
        self._animationEasingCurve = "OutCubic"
        self._autoFillWidth = False  # Add this
        self._autoFillHeight = False  # Add this

    def adoptExistingChildren(self):
        """
        Adopt any existing child widgets that were placed in this container
        from Qt Designer. This should be called after the UI is loaded.
        """
        if self._adoptingChildren:
            return
        
        self._adoptingChildren = True
        
        # Find all direct child widgets that are not the layout itself
        for child in self.findChildren(QWidget):
            if child.parent() == self and child != self and child.layout() != self._flowLayout:
                # Check if this widget is already managed by the flow layout
                already_managed = False
                for i in range(self._flowLayout.count()):
                    item = self._flowLayout.itemAt(i)
                    if item and item.widget() == child:
                        already_managed = True
                        break
                
                if not already_managed:
                    # Remove the widget from its current geometry management
                    child.setParent(None)
                    child.setParent(self)
                    # Add to flow layout
                    self._flowLayout.addWidget(child)
        
        self._adoptingChildren = False
        
        # Force layout update
        self._forceLayoutUpdate()
    
    def showEvent(self, event):
        """Handle show events - adopt existing children when shown"""
        super().showEvent(event)
        # Adopt any existing children that were added from Designer
        self.adoptExistingChildren()
        self._forceLayoutUpdate()
    
    def childEvent(self, event):
        """
        Handle child events to detect when widgets are added.
        This also catches widgets added from Qt Designer.
        """
        if event.type() == QtCore.QEvent.Type.ChildAdded:
            child = event.child()
            if isinstance(child, QWidget) and child.parent() == self and not self._adoptingChildren:
                # Check if this widget should be managed by the flow layout
                # Only adopt if it's not the layout itself and not already in layout
                if child != self and child.layout() != self._flowLayout:
                    # Check if already in flow layout
                    already_in_layout = False
                    for i in range(self._flowLayout.count()):
                        item = self._flowLayout.itemAt(i)
                        if item and item.widget() == child:
                            already_in_layout = True
                            break
                    
                    if not already_in_layout:
                        # Schedule adoption after a short delay to allow all UI setup
                        QtCore.QTimer.singleShot(10, lambda: self._addChildToLayout(child))
        
        super().childEvent(event)
    
    def _addChildToLayout(self, child):
        """Safely add a child widget to the flow layout"""
        if child and child.parent() == self and not self._adoptingChildren:
            # Temporarily block adoption to prevent recursion
            self._adoptingChildren = True
            child.setParent(None)
            child.setParent(self)
            self._flowLayout.addWidget(child)
            self._adoptingChildren = False
            self._forceLayoutUpdate()

    # ========== Spacing Properties ==========
    
    @Property(int)
    def spacing(self):
        """Get the spacing between items (both directions)"""
        return self._spacing
    
    @spacing.setter
    def spacing(self, value):
        """Set the spacing between items (both directions)"""
        self._spacing = value
        self._horizontalSpacing = value
        self._verticalSpacing = value
        if hasattr(self, '_flowLayout'):
            self._flowLayout.setSpacing(value)
            self._forceLayoutUpdate()

    @Property(int)
    def horizontalSpacing(self):
        """Get horizontal spacing between items"""
        return self._horizontalSpacing
    
    @horizontalSpacing.setter
    def horizontalSpacing(self, value):
        """Set horizontal spacing between items"""
        self._horizontalSpacing = value
        # QFlowLayout uses single spacing value, so we'll use the average
        if hasattr(self, '_flowLayout'):
            avg_spacing = (self._horizontalSpacing + self._verticalSpacing) // 2
            self._flowLayout.setSpacing(avg_spacing)
            self._forceLayoutUpdate()

    @Property(int)
    def verticalSpacing(self):
        """Get vertical spacing between items"""
        return self._verticalSpacing
    
    @verticalSpacing.setter
    def verticalSpacing(self, value):
        """Set vertical spacing between items"""
        self._verticalSpacing = value
        if hasattr(self, '_flowLayout'):
            avg_spacing = (self._horizontalSpacing + self._verticalSpacing) // 2
            self._flowLayout.setSpacing(avg_spacing)
            self._forceLayoutUpdate()

    # ========== Margin Property ==========
    
    @Property(int)
    def margin(self):
        """Get the margin around the layout"""
        return self._margin
    
    @margin.setter
    def margin(self, value):
        """Set the margin around the layout"""
        self._margin = value
        if hasattr(self, '_flowLayout'):
            self._flowLayout.setContentsMargins(value, value, value, value)
            self._forceLayoutUpdate()

    # ========== Animation Properties ==========
    
    @Property(bool)
    def animationEnabled(self):
        """Enable or disable animations"""
        return self._animationEnabled
    
    @animationEnabled.setter
    def animationEnabled(self, enabled):
        """Enable or disable animations"""
        self._animationEnabled = enabled
        if hasattr(self, '_flowLayout'):
            self._flowLayout.setAnimated(enabled)

    @Property(int)
    def animationDuration(self):
        """Get animation duration in milliseconds"""
        return self._animationDuration
    
    @animationDuration.setter
    def animationDuration(self, duration):
        """Set animation duration in milliseconds"""
        self._animationDuration = duration
        if hasattr(self, '_flowLayout'):
            self._flowLayout.setAnimationDuration(duration)

    @Property(str)
    def animationEasingCurve(self):
        """Get easing curve name"""
        return self._animationEasingCurve
    
    @animationEasingCurve.setter
    def animationEasingCurve(self, curveName):
        """Set easing curve by name"""
        self._animationEasingCurve = curveName
        if hasattr(self, '_flowLayout'):
            self._flowLayout.setAnimationEasingCurve(curveName)

    @Property(bool)
    def justifySpacing(self):
        """Enable/disable even spacing between widgets"""
        if hasattr(self, '_flowLayout'):
            return self._flowLayout.justifySpacing
        return True

    @justifySpacing.setter
    def justifySpacing(self, enabled):
        if hasattr(self, '_flowLayout'):
            self._flowLayout.justifySpacing = enabled
            self._forceLayoutUpdate()
    
    @Property(bool)
    def autoFillWidth(self):
        """Auto-fill available width by expanding widgets evenly across each row"""
        return self._autoFillWidth if hasattr(self, '_autoFillWidth') else False

    @autoFillWidth.setter
    def autoFillWidth(self, enabled):
        self._autoFillWidth = enabled
        if hasattr(self, '_flowLayout'):
            self._flowLayout.autoFillWidth = enabled
            self._forceLayoutUpdate()

    @Property(bool)
    def autoFillHeight(self):
        """Auto-fill available height by expanding widgets evenly across all rows"""
        return self._autoFillHeight if hasattr(self, '_autoFillHeight') else False

    @autoFillHeight.setter
    def autoFillHeight(self, enabled):
        self._autoFillHeight = enabled
        if hasattr(self, '_flowLayout'):
            self._flowLayout.autoFillHeight = enabled
            self._forceLayoutUpdate()

    @Property(bool)
    def equalDistribution(self):
        """Enable/disable equal distribution of available space among widgets in each row"""
        if hasattr(self, '_flowLayout'):
            return self._flowLayout.equalDistribution
        return True

    @equalDistribution.setter
    def equalDistribution(self, enabled):
        if hasattr(self, '_flowLayout'):
            self._flowLayout.equalDistribution = enabled
            self._forceLayoutUpdate()

    # ========== Helper Methods ==========
    
    def _scheduleLayoutUpdate(self):
        """Schedule a layout update (debounced)"""
        if hasattr(self, '_flowLayout'):
            self._flowLayout._scheduleLayoutUpdate()
    
    def _forceLayoutUpdate(self):
        """Force an immediate layout update"""
        if hasattr(self, '_flowLayout'):
            # Cancel any pending timer
            if hasattr(self._flowLayout, '_updateTimer'):
                self._flowLayout._updateTimer.stop()
            
            # Force immediate layout
            rect = self.geometry()
            if rect.isValid():
                if self._animationEnabled:
                    self._flowLayout._performAnimatedLayout()
                else:
                    self._flowLayout._performImmediateLayout()
    
    def addWidget(self, widget, position=None):
        """
        Add a widget to the flow layout
        
        Args:
            widget: QWidget to add
            position: Optional position index to insert at
        """
        if position is not None:
            self._flowLayout.addWidget(widget, position)
        else:
            self._flowLayout.addWidget(widget)
        
        # Force layout update immediately after adding
        self._forceLayoutUpdate()
        
        # Also ensure widget is visible
        widget.show()
    
    def insertWidget(self, index, widget):
        """
        Insert a widget at a specific index
        
        Args:
            index: Position to insert at
            widget: QWidget to insert
        """
        self._flowLayout.addWidget(widget, index)
        self._forceLayoutUpdate()
        widget.show()
    
    def removeWidget(self, widget):
        """Remove a widget from the flow layout"""
        self._flowLayout.removeWidget(widget)
        self._forceLayoutUpdate()
    
    def clear(self):
        """Remove all widgets from the flow layout"""
        # Stop any ongoing animations first
        self.stopAllAnimations()
        
        # Remove all items
        while self._flowLayout.count():
            item = self._flowLayout.takeAt(0)
            if item and item.widget():
                widget = item.widget()
                widget.hide()
                widget.deleteLater()
        
        self._forceLayoutUpdate()
    
    def getFlowLayout(self):
        """Get the underlying flow layout"""
        return self._flowLayout
    
    def stopAllAnimations(self):
        """Stop all ongoing animations"""
        if hasattr(self, '_flowLayout'):
            self._flowLayout.stopAllAnimations()
    
    def isAnimating(self):
        """Check if animations are running"""
        if hasattr(self, '_flowLayout'):
            return self._flowLayout.isAnimating()
        return False
    
    def refreshLayout(self):
        """Manually refresh the layout"""
        self._forceLayoutUpdate()
    
    # ========== Event Handlers ==========
    
    def resizeEvent(self, event):
        """Handle resize events"""
        super().resizeEvent(event)
        if hasattr(self, '_flowLayout'):
            self._scheduleLayoutUpdate()