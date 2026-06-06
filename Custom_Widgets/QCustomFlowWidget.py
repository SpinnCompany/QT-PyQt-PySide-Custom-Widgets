# QCustomFlowWidget.py

from qtpy import QtCore, QtWidgets
from qtpy.QtCore import Property, QSize
from qtpy.QtWidgets import QWidget, QSizePolicy
import os

from Custom_Widgets.QCustomFlowLayout import QCustomFlowLayout


class QCustomFlowWidget(QWidget):
    """
    A container widget that uses QCustomFlowLayout internally.
    ALL custom properties are exposed here for Qt Designer.
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
            <property name="equalDistribution">
                <bool>true</bool>
            </property>
            <property name="autoFillWidth">
                <bool>false</bool>
            </property>
            <property name="autoFillHeight">
                <bool>false</bool>
            </property>
            <property name="justifySpacing">
                <bool>false</bool>
            </property>
            <property name="orderJsonPath">
                <string></string>
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
        self._equalDistribution = True
        self._autoFillWidth = False
        self._autoFillHeight = False
        self._justifySpacing = False
        self._orderJsonPath = ""

    def adoptExistingChildren(self):
        """Adopt existing child widgets from Qt Designer in their original order"""
        if self._adoptingChildren:
            return
        
        self._adoptingChildren = True
        
        # IMPORTANT: Get children in the order they appear in the UI file
        # The findChildren returns in no guaranteed order, so we need to sort
        # by their position in the widget hierarchy
        children = []
        for child in self.findChildren(QWidget):
            if child.parent() == self and child != self and child.layout() != self._flowLayout:
                # Check if already in layout
                already_managed = False
                for i in range(self._flowLayout.count()):
                    item = self._flowLayout.itemAt(i)
                    if item and item.widget() == child:
                        already_managed = True
                        break
                
                if not already_managed:
                    children.append(child)
        
        # Sort children by their visual order (approximate)
        # This tries to preserve the order from Qt Designer
        children.sort(key=lambda w: (w.y(), w.x()))
        
        # Add children to layout in order
        for child in children:
            child.setParent(None)
            child.setParent(self)
            self._flowLayout.addWidget(child)
        
        self._adoptingChildren = False
        self._forceLayoutUpdate()
    
    def showEvent(self, event):
        """Handle show events - adopt existing children when shown"""
        super().showEvent(event)
        self.adoptExistingChildren()
        self._forceLayoutUpdate()
    
    def childEvent(self, event):
        """Handle child events to detect when widgets are added"""
        if event.type() == QtCore.QEvent.Type.ChildAdded:
            child = event.child()
            if isinstance(child, QWidget) and child.parent() == self and not self._adoptingChildren:
                if child != self and child.layout() != self._flowLayout:
                    already_in_layout = False
                    for i in range(self._flowLayout.count()):
                        item = self._flowLayout.itemAt(i)
                        if item and item.widget() == child:
                            already_in_layout = True
                            break
                    
                    if not already_in_layout:
                        QtCore.QTimer.singleShot(10, lambda: self._addChildToLayout(child))
        
        super().childEvent(event)
    
    def _addChildToLayout(self, child):
        """Safely add a child widget to the flow layout"""
        if child and child.parent() == self and not self._adoptingChildren:
            self._adoptingChildren = True
            child.setParent(None)
            child.setParent(self)
            self._flowLayout.addWidget(child)
            self._adoptingChildren = False
            self._forceLayoutUpdate()

    # ========== Spacing Properties ==========
    
    @Property(int)
    def spacing(self):
        return self._spacing
    
    @spacing.setter
    def spacing(self, value):
        self._spacing = value
        self._horizontalSpacing = value
        self._verticalSpacing = value
        if hasattr(self, '_flowLayout'):
            self._flowLayout.setSpacing(value)
            self._forceLayoutUpdate()

    @Property(int)
    def horizontalSpacing(self):
        return self._horizontalSpacing
    
    @horizontalSpacing.setter
    def horizontalSpacing(self, value):
        self._horizontalSpacing = value
        if hasattr(self, '_flowLayout'):
            avg_spacing = (self._horizontalSpacing + self._verticalSpacing) // 2
            self._flowLayout.setSpacing(avg_spacing)
            self._forceLayoutUpdate()

    @Property(int)
    def verticalSpacing(self):
        return self._verticalSpacing
    
    @verticalSpacing.setter
    def verticalSpacing(self, value):
        self._verticalSpacing = value
        if hasattr(self, '_flowLayout'):
            avg_spacing = (self._horizontalSpacing + self._verticalSpacing) // 2
            self._flowLayout.setSpacing(avg_spacing)
            self._forceLayoutUpdate()

    # ========== Margin Property ==========
    
    @Property(int)
    def margin(self):
        return self._margin
    
    @margin.setter
    def margin(self, value):
        self._margin = value
        if hasattr(self, '_flowLayout'):
            self._flowLayout.setContentsMargins(value, value, value, value)
            self._forceLayoutUpdate()

    # ========== Animation Properties ==========
    
    @Property(bool)
    def animationEnabled(self):
        return self._animationEnabled
    
    @animationEnabled.setter
    def animationEnabled(self, enabled):
        self._animationEnabled = enabled
        if hasattr(self, '_flowLayout'):
            self._flowLayout.setAnimated(enabled)

    @Property(int)
    def animationDuration(self):
        return self._animationDuration
    
    @animationDuration.setter
    def animationDuration(self, duration):
        self._animationDuration = duration
        if hasattr(self, '_flowLayout'):
            self._flowLayout.setAnimationDuration(duration)

    @Property(str)
    def animationEasingCurve(self):
        return self._animationEasingCurve
    
    @animationEasingCurve.setter
    def animationEasingCurve(self, curveName):
        self._animationEasingCurve = curveName
        if hasattr(self, '_flowLayout'):
            self._flowLayout.setAnimationEasingCurve(curveName)

    # ========== Layout Strategy Properties ==========
    
    @Property(bool)
    def equalDistribution(self):
        return self._equalDistribution
    
    @equalDistribution.setter
    def equalDistribution(self, enabled):
        self._equalDistribution = enabled
        if hasattr(self, '_flowLayout'):
            self._flowLayout.equalDistribution = enabled
            self._forceLayoutUpdate()
    
    @Property(bool)
    def autoFillWidth(self):
        return self._autoFillWidth
    
    @autoFillWidth.setter
    def autoFillWidth(self, enabled):
        self._autoFillWidth = enabled
        if enabled:
            self._equalDistribution = enabled
        if hasattr(self, '_flowLayout'):
            self._flowLayout.autoFillWidth = enabled
            self._forceLayoutUpdate()

    @Property(bool)
    def autoFillHeight(self):
        return self._autoFillHeight
    
    @autoFillHeight.setter
    def autoFillHeight(self, enabled):
        self._autoFillHeight = enabled
        if hasattr(self, '_flowLayout'):
            self._flowLayout.autoFillHeight = enabled
            self._forceLayoutUpdate()

    @Property(bool)
    def justifySpacing(self):
        return self._justifySpacing
    
    @justifySpacing.setter
    def justifySpacing(self, enabled):
        self._justifySpacing = enabled
        if hasattr(self, '_flowLayout'):
            self._flowLayout.justifySpacing = enabled
            self._forceLayoutUpdate()

    # ========== Order Configuration ==========
    
    @Property(str)
    def orderJsonPath(self):
        return self._orderJsonPath
    
    @orderJsonPath.setter
    def orderJsonPath(self, path):
        self._orderJsonPath = path if path else ""
        if hasattr(self, '_flowLayout'):
            self._flowLayout.orderJsonPath = self._orderJsonPath
            self._forceLayoutUpdate()

    # ========== Helper Methods ==========
    
    def _forceLayoutUpdate(self):
        """Force an immediate layout update"""
        if hasattr(self, '_flowLayout'):
            if hasattr(self._flowLayout, '_updateTimer'):
                self._flowLayout._updateTimer.stop()
            
            rect = self.geometry()
            if rect.isValid():
                if self._animationEnabled:
                    self._flowLayout._performAnimatedLayout()
                else:
                    self._flowLayout._performImmediateLayout()
    
    def addWidget(self, widget, position=None):
        """Add a widget to the flow layout"""
        if position is not None:
            self._flowLayout.addWidget(widget, position)
        else:
            self._flowLayout.addWidget(widget)
        self._forceLayoutUpdate()
        widget.show()
    
    def removeWidget(self, widget):
        """Remove a widget from the flow layout"""
        self._flowLayout.removeWidget(widget)
        self._forceLayoutUpdate()
    
    def clear(self):
        """Remove all widgets from the flow layout"""
        self.stopAllAnimations()
        while self._flowLayout.count():
            item = self._flowLayout.takeAt(0)
            if item and item.widget():
                item.widget().hide()
                item.widget().deleteLater()
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
    
    def resizeEvent(self, event):
        """Handle resize events"""
        super().resizeEvent(event)
        if hasattr(self, '_flowLayout'):
            self._flowLayout._scheduleLayoutUpdate()