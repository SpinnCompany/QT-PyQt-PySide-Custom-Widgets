from qtpy import QtGui, QtCore, QtWidgets
from qtpy.QtCore import Property, QEasingCurve
import typing
import os

from Custom_Widgets.QPropertyAnimation import returnAnimationEasingCurve

class AnimatedWidgetItem:
    """Helper class to manage animated widget movements"""
    def __init__(self, widget, targetGeometry):
        self.widget = widget
        self.startGeometry = widget.geometry()
        self.targetGeometry = targetGeometry
        self.animation = QtCore.QPropertyAnimation(widget, b"geometry")
        self.animation.setDuration(300)
        self.animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.animation.setStartValue(self.startGeometry)
        self.animation.setEndValue(targetGeometry)
        
    def start(self):
        if self.startGeometry != self.targetGeometry:
            self.animation.start()
        else:
            self.widget.setGeometry(self.targetGeometry)

class QCustomFlowLayout(QtWidgets.QLayout):
    # Signal emitted when layout animation starts
    animationStarted = QtCore.Signal()
    # Signal emitted when layout animation finishes
    animationFinished = QtCore.Signal()
    
    # Qt Designer integration properties
    script_dir = os.path.dirname(os.path.realpath(__file__))
    WIDGET_ICON = os.path.join(script_dir, "components/icons/flow_layout.png")
    WIDGET_TOOLTIP = "A custom flow layout with smooth animations"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomFlowLayout' name='customFlowLayout'>
            <property name="spacing">
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
            <property name="margin">
                <number>10</number>
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
        </widget>
    </ui>
    """
    WIDGET_MODULE = "Custom_Widgets.QCustomFlowLayout"
    
    def __init__(self, parent=None, margin=0, spacing=-1, animate=True, animationDuration=300):
        super().__init__(parent)

        if parent is not None:
            self.setContentsMargins(margin, margin, margin, margin)

        self.setSpacing(spacing)
        
        self._items = []
        self.__pendingPositions = {}
        self._animate = animate
        self._animationDuration = animationDuration
        self._animationEasingCurve = "OutCubic"
        self._currentAnimations = []
        self._animationGroup = None
        self._updatingLayout = False
        self._lastRect = QtCore.QRect()
        self._margin = margin
        self._equalDistribution = True  # New: equal distribution of space among widgets
        self._autoFillWidth = False
        self._autoFillHeight = False
        self._justifySpacing = False  # Default to False now, use equalDistribution instead
        
        # Timer to debounce layout updates
        self._updateTimer = QtCore.QTimer()
        self._updateTimer.setSingleShot(True)
        self._updateTimer.timeout.connect(self._performAnimatedLayout)
        
        # Store current widget positions for comparison
        self._currentPositions = {}

    def __del__(self):
        item = self.takeAt(0)
        while item:
            item = self.takeAt(0)

    def addItem(self, a0: QtWidgets.QLayoutItem) -> None:
        try:
            position = self.__pendingPositions[a0.widget()]
            self._items.insert(position, a0)
            del self.__pendingPositions[a0.widget()]
        except KeyError:
            self._items.append(a0)
        
        self._scheduleLayoutUpdate()

    def addWidget(self, w: QtWidgets.QWidget, position: int = None, align: QtCore.Qt.AlignmentFlag = None) -> None:
        if position is not None:
            self.__pendingPositions[w] = position
        if align is not None:
            frameLayout = w.layout()
            if frameLayout is not None:
                frameLayout.setAlignment(align)
        super().addWidget(w)
        self._scheduleLayoutUpdate()

    def count(self):
        return len(self._items)

    def expandingDirections(self):
        return QtCore.Qt.Orientations(QtCore.Qt.Orientation(0))

    def itemAt(self, index: int) -> QtWidgets.QLayoutItem:
        if 0 <= index < len(self._items):
            return self._items[index]
        return None

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, width):
        height = self._doLayout(QtCore.QRect(0, 0, width, 0), True, False)
        return height

    def minimumSize(self):
        size = QtCore.QSize()

        for item in self._items:
            size = size.expandedTo(item.minimumSize())

        margin, _, _, _ = self.getContentsMargins()
        size += QtCore.QSize(2 * margin, 2 * margin)
        return size

    def removeItem(self, a0: QtWidgets.QLayoutItem) -> None:
        a0.widget().deleteLater()
        self._scheduleLayoutUpdate()

    def removeWidget(self, w: QtWidgets.QWidget) -> None:
        w.deleteLater()
        self._scheduleLayoutUpdate()

    def setGeometry(self, rect):
        super().setGeometry(rect)
        
        if self._animate:
            self._storeCurrentPositions()
        
        self._scheduleLayoutUpdate()

    def sizeHint(self):
        return self.minimumSize()

    def takeAt(self, index: int) -> QtWidgets.QLayoutItem:
        if 0 <= index < len(self._items):
            item = self._items.pop(index)
            self._scheduleLayoutUpdate()
            return item
        return None
    
    # ========== Qt Designer Properties ==========
    
    @Property(bool)
    def animationEnabled(self):
        return self._animate
    
    @animationEnabled.setter
    def animationEnabled(self, animate):
        self._animate = animate
    
    @Property(int)
    def animationDuration(self):
        return self._animationDuration
    
    @animationDuration.setter
    def animationDuration(self, durationMs):
        self._animationDuration = durationMs
    
    @Property(str)
    def animationEasingCurve(self):
        return self._animationEasingCurve
    
    @animationEasingCurve.setter
    def animationEasingCurve(self, curve):
        self._animationEasingCurve = curve
    
    @Property(int)
    def margin(self):
        margins = self.getContentsMargins()
        return margins[0]
    
    @margin.setter
    def margin(self, margin):
        self.setContentsMargins(margin, margin, margin, margin)
        self._margin = margin
        self._scheduleLayoutUpdate()
    
    @Property(bool)
    def equalDistribution(self):
        """Enable/disable equal distribution of available space among widgets in each row"""
        return self._equalDistribution
    
    @equalDistribution.setter
    def equalDistribution(self, enabled):
        self._equalDistribution = enabled
        self._scheduleLayoutUpdate()
    
    @Property(bool)
    def autoFillWidth(self):
        """Auto-fill available width by expanding widgets evenly across each row (deprecated, use equalDistribution)"""
        return self._autoFillWidth
    
    @autoFillWidth.setter
    def autoFillWidth(self, enabled):
        self._autoFillWidth = enabled
        # For backward compatibility, set equalDistribution to enabled when autoFillWidth is enabled
        if enabled:
            self._equalDistribution = enabled
        self._scheduleLayoutUpdate()
    
    @Property(bool)
    def autoFillHeight(self):
        """Auto-fill available height by expanding widgets evenly across all rows"""
        return self._autoFillHeight
    
    @autoFillHeight.setter
    def autoFillHeight(self, enabled):
        self._autoFillHeight = enabled
        self._scheduleLayoutUpdate()
    
    @Property(bool)
    def justifySpacing(self):
        """Enable/disable even spacing between widgets (distribute extra space as gaps)"""
        return self._justifySpacing
    
    @justifySpacing.setter
    def justifySpacing(self, enabled):
        self._justifySpacing = enabled
        self._scheduleLayoutUpdate()
    
    # ========== Animation Control Methods ==========
    
    def setAnimated(self, animate):
        self._animate = animate
    
    def setAnimationDuration(self, durationMs):
        self._animationDuration = durationMs
    
    def setAnimationEasingCurve(self, curve):
        self._animationEasingCurve = curve
    
    def _getEasingCurve(self):
        return returnAnimationEasingCurve(self._animationEasingCurve)
    
    def _storeCurrentPositions(self):
        self._currentPositions.clear()
        for item in self._items:
            widget = item.widget()
            if widget and not widget.isHidden():
                self._currentPositions[widget] = widget.geometry()
    
    def _scheduleLayoutUpdate(self):
        if self._updatingLayout:
            return
        
        if self._animate:
            self._updateTimer.start(10)
        else:
            self._performImmediateLayout()
    
    def _performImmediateLayout(self):
        self._updatingLayout = True
        rect = self.geometry()
        if rect.isValid():
            self._doLayout(rect, False, False)
        self._updatingLayout = False
    
    def _performAnimatedLayout(self):
        if self._updatingLayout:
            return
        
        self._updatingLayout = True
        rect = self.geometry()
        
        if not rect.isValid():
            self._updatingLayout = False
            return
        
        newGeometries = {}
        testRect = QtCore.QRect(0, 0, rect.width(), 0)
        self._calculateLayout(testRect, newGeometries)
        
        animations = []
        for item in self._items:
            widget = item.widget()
            if widget and not widget.isHidden():
                newGeom = newGeometries.get(widget)
                if newGeom and newGeom != widget.geometry():
                    animatedItem = AnimatedWidgetItem(widget, newGeom)
                    animatedItem.animation.setDuration(self._animationDuration)
                    animations.append(animatedItem)
        
        if animations:
            self.animationStarted.emit()
            animationGroup = QtCore.QParallelAnimationGroup()
            
            for animatedItem in animations:
                animationGroup.addAnimation(animatedItem.animation)
            
            animationGroup.finished.connect(self._onAnimationsFinished)
            animationGroup.start()
            self._animationGroup = animationGroup
        else:
            self._doLayout(rect, False, False)
        
        self._updatingLayout = False
    
    def _onAnimationsFinished(self):
        self.animationFinished.emit()
        self._animationGroup = None
        rect = self.geometry()
        if rect.isValid():
            self._doLayout(rect, False, False)
    
    def _getWidgetSize(self, widget):
        """Get the widget's natural/preferred size"""
        if not widget:
            return QtCore.QSize(0, 0)
        
        size = widget.sizeHint()
        
        if not size.isValid():
            size = widget.minimumSizeHint()
        
        if not size.isValid():
            size = widget.minimumSize()
        
        if not size.isValid():
            size = widget.size()
        
        # Check for maximum size constraints
        max_width = widget.maximumWidth()
        max_height = widget.maximumHeight()
        
        if max_width > 0 and max_width < 32767:  # QWIDGETSIZE_MAX is typically 16777215
            size.setWidth(min(size.width(), max_width))
        if max_height > 0 and max_height < 32767:
            size.setHeight(min(size.height(), max_height))
        
        min_width = widget.minimumWidth()
        min_height = widget.minimumHeight()
        
        if min_width > 0:
            size.setWidth(max(size.width(), min_width))
        if min_height > 0:
            size.setHeight(max(size.height(), min_height))
        
        return size
    
    def _distributeEqualWidths(self, widgets_and_sizes, available_width, spacing):
        """
        Distribute available width equally among widgets, respecting min/max constraints.
        Returns a list of final widths for each widget.
        """
        n = len(widgets_and_sizes)
        if n == 0:
            return []
        
        # Get min and max widths for each widget
        min_widths = []
        max_widths = []
        natural_widths = []
        
        for widget, size in widgets_and_sizes:
            min_w = widget.minimumWidth() if widget.minimumWidth() > 0 else size.width()
            max_w = widget.maximumWidth() if widget.maximumWidth() < 32767 else 32767
            natural_w = size.width()
            
            min_widths.append(min_w)
            max_widths.append(max_w)
            natural_widths.append(natural_w)
        
        # Calculate total spacing
        total_spacing = (n - 1) * spacing
        available_for_widgets = available_width - total_spacing
        
        # Start with equal distribution
        equal_width = available_for_widgets / n
        
        # Initialize widths with equal distribution, clamped by min/max
        widths = []
        for i in range(n):
            clamped = max(min_widths[i], min(equal_width, max_widths[i]))
            widths.append(clamped)
        
        # Check if we need to redistribute
        total_width = sum(widths)
        
        # If total is less than available, distribute remaining space to widgets that can expand
        if total_width < available_for_widgets:
            remaining = available_for_widgets - total_width
            # Find widgets that can expand (not at max)
            expandable_indices = [i for i in range(n) if widths[i] < max_widths[i]]
            
            while remaining > 0.1 and expandable_indices:
                # Distribute equally among expandable widgets
                add_per_widget = remaining / len(expandable_indices)
                redistributed = False
                
                for i in expandable_indices[:]:
                    new_width = widths[i] + add_per_widget
                    if new_width >= max_widths[i]:
                        new_width = max_widths[i]
                        expandable_indices.remove(i)
                        redistributed = True
                    
                    remaining -= (new_width - widths[i])
                    widths[i] = new_width
                
                if not redistributed:
                    break
        
        # If total is more than available, reduce from widgets that can shrink
        elif total_width > available_for_widgets:
            excess = total_width - available_for_widgets
            # Find widgets that can shrink (not at min)
            shrinkable_indices = [i for i in range(n) if widths[i] > min_widths[i]]
            
            while excess > 0.1 and shrinkable_indices:
                # Reduce equally among shrinkable widgets
                reduce_per_widget = excess / len(shrinkable_indices)
                redistributed = False
                
                for i in shrinkable_indices[:]:
                    new_width = widths[i] - reduce_per_widget
                    if new_width <= min_widths[i]:
                        new_width = min_widths[i]
                        shrinkable_indices.remove(i)
                        redistributed = True
                    
                    excess -= (widths[i] - new_width)
                    widths[i] = new_width
                
                if not redistributed:
                    break
        
        return widths
    
    def _calculateLayout(self, rect, outGeometries):
        """Calculate layout geometries without applying them"""
        margins = self.getContentsMargins()
        effectiveRect = QtCore.QRect(
            rect.x() + margins[0],
            rect.y() + margins[1],
            rect.width() - margins[0] - margins[2],
            rect.height() - margins[1] - margins[3]
        )
        
        if effectiveRect.width() <= 0:
            return
        
        spacing = self.spacing()
        
        # First pass: organize items into rows with their minimum/natural sizes
        rows = []
        currentRow = []
        currentRowWidth = 0
        currentRowMaxHeight = 0
        
        for item in self._items:
            widget = item.widget()
            if not widget or widget.isHidden():
                continue
            
            itemSize = self._getWidgetSize(widget)
            
            # Check if we need to wrap to next row
            if currentRow and (currentRowWidth + spacing + itemSize.width() > effectiveRect.width()):
                rows.append((currentRow, currentRowWidth, currentRowMaxHeight))
                currentRow = []
                currentRowWidth = 0
                currentRowMaxHeight = 0
            
            currentRow.append((widget, itemSize))
            currentRowWidth += itemSize.width()
            if len(currentRow) > 1:
                currentRowWidth += spacing
            currentRowMaxHeight = max(currentRowMaxHeight, itemSize.height())
        
        # Add the last row
        if currentRow:
            rows.append((currentRow, currentRowWidth, currentRowMaxHeight))
        
        # Second pass: calculate positions with equal distribution if enabled
        currentY = rect.y() + margins[1]
        
        for row_index, (row_items, total_natural_width, natural_row_height) in enumerate(rows):
            currentX = effectiveRect.x()
            
            # Determine the row height (max of natural heights or equal distribution)
            if self._autoFillHeight:
                row_height = natural_row_height  # Will be adjusted later
            else:
                row_height = natural_row_height
            
            # Check if we should use equal distribution
            if self._equalDistribution and len(row_items) > 0:
                # Distribute available width equally among widgets in the row
                widths = self._distributeEqualWidths(row_items, effectiveRect.width(), spacing)
                
                for i, (widget, original_size) in enumerate(row_items):
                    new_width = widths[i]
                    
                    # Apply max width constraint
                    max_width = widget.maximumWidth()
                    if max_width > 0 and max_width < 32767:
                        new_width = min(new_width, max_width)
                    
                    # Apply min width constraint
                    min_width = widget.minimumWidth()
                    if min_width > 0:
                        new_width = max(new_width, min_width)
                    
                    widgetGeometry = QtCore.QRect(
                        QtCore.QPoint(int(currentX), currentY),
                        QtCore.QSize(int(new_width), row_height)
                    )
                    outGeometries[widget] = widgetGeometry
                    
                    currentX += new_width + spacing
                    
            elif self._justifySpacing and len(row_items) > 1:
                # Justify spacing: distribute extra space as gaps between widgets
                remaining_space = effectiveRect.width() - total_natural_width
                space_between = remaining_space / (len(row_items) - 1) if len(row_items) > 1 else 0
                
                for i, (widget, itemSize) in enumerate(row_items):
                    widgetGeometry = QtCore.QRect(
                        QtCore.QPoint(int(currentX), currentY),
                        itemSize
                    )
                    outGeometries[widget] = widgetGeometry
                    
                    currentX += itemSize.width()
                    if i < len(row_items) - 1:
                        currentX += space_between
            else:
                # Default: use fixed spacing with natural sizes
                for widget, itemSize in row_items:
                    widgetGeometry = QtCore.QRect(
                        QtCore.QPoint(int(currentX), currentY),
                        itemSize
                    )
                    outGeometries[widget] = widgetGeometry
                    currentX += itemSize.width() + spacing
            
            currentY += row_height + spacing
        
        # Handle autoFillHeight (distribute extra vertical space)
        if self._autoFillHeight and len(rows) > 0:
            total_spacing_y = (len(rows) - 1) * spacing
            available_height = effectiveRect.height() - total_spacing_y
            total_original_height = sum(row_height for _, _, row_height in rows)
            
            if available_height > total_original_height:
                extra_per_row = (available_height - total_original_height) / len(rows)
                # Recalculate Y positions with expanded heights
                currentY = rect.y() + margins[1]
                row_index = 0
                
                for row_items, total_width, row_height in rows:
                    new_row_height = row_height + extra_per_row
                    
                    # Apply max height constraints per widget in the row
                    for widget, itemSize in row_items:
                        max_height = widget.maximumHeight()
                        final_height = new_row_height
                        if max_height > 0 and max_height < 32767:
                            final_height = min(final_height, max_height)
                        
                        # Update geometry with new height
                        if widget in outGeometries:
                            old_geom = outGeometries[widget]
                            outGeometries[widget] = QtCore.QRect(
                                old_geom.topLeft(),
                                QtCore.QSize(old_geom.width(), int(final_height))
                            )
                    
                    currentY += new_row_height + spacing
                    row_index += 1
    
    def _doLayout(self, rect, testOnly, animate=True):
        """Apply layout with animation support"""
        margins = self.getContentsMargins()
        effectiveRect = QtCore.QRect(
            rect.x() + margins[0],
            rect.y() + margins[1],
            rect.width() - margins[0] - margins[2],
            rect.height() - margins[1] - margins[3]
        )
        
        if effectiveRect.width() <= 0:
            return 0
        
        spacing = self.spacing()
        
        # First pass: organize items into rows with their minimum/natural sizes
        rows = []
        currentRow = []
        currentRowWidth = 0
        currentRowMaxHeight = 0
        
        for item in self._items:
            widget = item.widget()
            if not widget or widget.isHidden():
                continue
            
            itemSize = self._getWidgetSize(widget)
            
            # Check if we need to wrap to next row
            if currentRow and (currentRowWidth + spacing + itemSize.width() > effectiveRect.width()):
                rows.append((currentRow, currentRowWidth, currentRowMaxHeight))
                currentRow = []
                currentRowWidth = 0
                currentRowMaxHeight = 0
            
            currentRow.append((widget, itemSize))
            currentRowWidth += itemSize.width()
            if len(currentRow) > 1:
                currentRowWidth += spacing
            currentRowMaxHeight = max(currentRowMaxHeight, itemSize.height())
        
        # Add the last row
        if currentRow:
            rows.append((currentRow, currentRowWidth, currentRowMaxHeight))
        
        # Second pass: calculate positions with equal distribution if enabled
        currentY = rect.y() + margins[1]
        
        for row_index, (row_items, total_natural_width, natural_row_height) in enumerate(rows):
            currentX = effectiveRect.x()
            
            # Determine the row height
            if self._autoFillHeight:
                row_height = natural_row_height  # Will be adjusted later
            else:
                row_height = natural_row_height
            
            # Check if we should use equal distribution
            if self._equalDistribution and len(row_items) > 0:
                # Distribute available width equally among widgets in the row
                widths = self._distributeEqualWidths(row_items, effectiveRect.width(), spacing)
                
                for i, (widget, original_size) in enumerate(row_items):
                    new_width = widths[i]
                    
                    # Apply max width constraint
                    max_width = widget.maximumWidth()
                    if max_width > 0 and max_width < 32767:
                        new_width = min(new_width, max_width)
                    
                    # Apply min width constraint
                    min_width = widget.minimumWidth()
                    if min_width > 0:
                        new_width = max(new_width, min_width)
                    
                    if not testOnly:
                        targetGeometry = QtCore.QRect(
                            QtCore.QPoint(int(currentX), currentY),
                            QtCore.QSize(int(new_width), row_height)
                        )
                        
                        if animate and self._animate and not self._updatingLayout:
                            if widget.geometry() != targetGeometry:
                                animation = QtCore.QPropertyAnimation(widget, b"geometry")
                                animation.setDuration(self._animationDuration)
                                easingCurve = self._getEasingCurve()
                                animation.setEasingCurve(easingCurve)
                                animation.setStartValue(widget.geometry())
                                animation.setEndValue(targetGeometry)
                                animation.start()
                                self._currentAnimations.append(animation)
                                animation.finished.connect(
                                    lambda a=animation: self._cleanupAnimation(a)
                                )
                        else:
                            widget.setGeometry(targetGeometry)
                    
                    currentX += new_width + spacing
                    
            elif self._justifySpacing and len(row_items) > 1:
                # Justify spacing: distribute extra space as gaps between widgets
                remaining_space = effectiveRect.width() - total_natural_width
                space_between = remaining_space / (len(row_items) - 1) if len(row_items) > 1 else 0
                
                for i, (widget, itemSize) in enumerate(row_items):
                    if not testOnly:
                        targetGeometry = QtCore.QRect(
                            QtCore.QPoint(int(currentX), currentY),
                            itemSize
                        )
                        
                        if animate and self._animate and not self._updatingLayout:
                            if widget.geometry() != targetGeometry:
                                animation = QtCore.QPropertyAnimation(widget, b"geometry")
                                animation.setDuration(self._animationDuration)
                                easingCurve = self._getEasingCurve()
                                animation.setEasingCurve(easingCurve)
                                animation.setStartValue(widget.geometry())
                                animation.setEndValue(targetGeometry)
                                animation.start()
                                self._currentAnimations.append(animation)
                                animation.finished.connect(
                                    lambda a=animation: self._cleanupAnimation(a)
                                )
                        else:
                            widget.setGeometry(targetGeometry)
                    
                    currentX += itemSize.width()
                    if i < len(row_items) - 1:
                        currentX += space_between
            else:
                # Default: use fixed spacing with natural sizes
                for widget, itemSize in row_items:
                    if not testOnly:
                        targetGeometry = QtCore.QRect(
                            QtCore.QPoint(int(currentX), currentY),
                            itemSize
                        )
                        
                        if animate and self._animate and not self._updatingLayout:
                            if widget.geometry() != targetGeometry:
                                animation = QtCore.QPropertyAnimation(widget, b"geometry")
                                animation.setDuration(self._animationDuration)
                                easingCurve = self._getEasingCurve()
                                animation.setEasingCurve(easingCurve)
                                animation.setStartValue(widget.geometry())
                                animation.setEndValue(targetGeometry)
                                animation.start()
                                self._currentAnimations.append(animation)
                                animation.finished.connect(
                                    lambda a=animation: self._cleanupAnimation(a)
                                )
                        else:
                            widget.setGeometry(targetGeometry)
                    
                    currentX += itemSize.width() + spacing
            
            currentY += row_height + spacing
        
        # Handle autoFillHeight (distribute extra vertical space)
        if self._autoFillHeight and len(rows) > 0 and not testOnly:
            total_spacing_y = (len(rows) - 1) * spacing
            available_height = effectiveRect.height() - total_spacing_y
            total_original_height = sum(row_height for _, _, row_height in rows)
            
            if available_height > total_original_height:
                extra_per_row = (available_height - total_original_height) / len(rows)
                # Recalculate Y positions with expanded heights
                currentY = rect.y() + margins[1]
                row_index = 0
                
                for row_items, total_width, row_height in rows:
                    new_row_height = row_height + extra_per_row
                    
                    # Apply max height constraints per widget in the row
                    for widget, itemSize in row_items:
                        max_height = widget.maximumHeight()
                        final_height = new_row_height
                        if max_height > 0 and max_height < 32767:
                            final_height = min(final_height, max_height)
                        
                        # Get current geometry and update height
                        current_geom = widget.geometry()
                        targetGeometry = QtCore.QRect(
                            current_geom.topLeft(),
                            QtCore.QSize(current_geom.width(), int(final_height))
                        )
                        
                        if animate and self._animate and not self._updatingLayout:
                            if widget.geometry() != targetGeometry:
                                animation = QtCore.QPropertyAnimation(widget, b"geometry")
                                animation.setDuration(self._animationDuration)
                                easingCurve = self._getEasingCurve()
                                animation.setEasingCurve(easingCurve)
                                animation.setStartValue(widget.geometry())
                                animation.setEndValue(targetGeometry)
                                animation.start()
                                self._currentAnimations.append(animation)
                                animation.finished.connect(
                                    lambda a=animation: self._cleanupAnimation(a)
                                )
                        else:
                            widget.setGeometry(targetGeometry)
                    
                    currentY += new_row_height + spacing
                    row_index += 1
        
        total_height = currentY - spacing + margins[3] - rect.y()
        return max(total_height, 0)
    
    def _cleanupAnimation(self, animation):
        if animation in self._currentAnimations:
            self._currentAnimations.remove(animation)
    
    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self._animate:
            self._storeCurrentPositions()
            self._scheduleLayoutUpdate()
        else:
            self._doLayout(self.geometry(), False, False)
    
    def stopAllAnimations(self):
        for animation in self._currentAnimations:
            animation.stop()
        self._currentAnimations.clear()
        if self._animationGroup:
            self._animationGroup.stop()
            self._animationGroup = None
    
    def isAnimating(self):
        return len(self._currentAnimations) > 0 or self._animationGroup is not None