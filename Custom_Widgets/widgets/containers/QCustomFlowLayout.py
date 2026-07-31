from qtpy import QtGui, QtCore, QtWidgets
from qtpy.QtCore import Property, QEasingCurve
import typing
import os
import json

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
    
    def __init__(self, parent=None, margin=0, spacing=-1, animate=True, animationDuration=300):
        super().__init__(parent)

        if parent is not None:
            self.setContentsMargins(margin, margin, margin, margin)

        self.setSpacing(spacing)
        
        self._items = []  # NEVER REORDERED - maintains strict insertion order
        self.__pendingPositions = {}
        self._animate = animate
        self._animationDuration = animationDuration
        self._animationEasingCurve = "OutCubic"
        self._currentAnimations = []
        self._animationGroup = None
        self._updatingLayout = False
        self._lastRect = QtCore.QRect()
        self._margin = margin
        self._equalDistribution = True
        self._autoFillWidth = False
        self._autoFillHeight = False
        self._justifySpacing = False
        self._orderJsonPath = ""
        self._widgetOrder = {}
        self._orderLoaded = False
        
        # Timer to debounce layout updates
        self._updateTimer = QtCore.QTimer()
        self._updateTimer.setSingleShot(True)
        self._updateTimer.timeout.connect(self._performAnimatedLayout)
        
        # Store current widget positions for comparison
        self._currentPositions = {}

    def __del__(self):
        # Suppress layout scheduling during teardown: the debounce timer's C++
        # object may already be deleted, and we don't need to reflow while the
        # layout is being destroyed. Swallow any object-already-deleted errors.
        self._updatingLayout = True
        try:
            item = self.takeAt(0)
            while item:
                item = self.takeAt(0)
        except (RuntimeError, AttributeError):
            pass

    def loadOrderFromJson(self):
        """Load widget order from JSON file if path is provided"""
        if not self._orderJsonPath or not os.path.exists(self._orderJsonPath):
            return False
        
        try:
            with open(self._orderJsonPath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if "QCustomFlowLayoutOrder" in data:
                order_data = data["QCustomFlowLayoutOrder"]
                layout_name = self.parent().objectName() if self.parent() else "default"
                
                if layout_name in order_data:
                    self._widgetOrder = order_data[layout_name]
                    print(f"[QCustomFlowLayout] Loaded order for '{layout_name}'")
                    self._orderLoaded = True
                    return True
                elif "default" in order_data:
                    self._widgetOrder = order_data["default"]
                    print(f"[QCustomFlowLayout] Loaded default order")
                    self._orderLoaded = True
                    return True
        except Exception as e:
            print(f"[QCustomFlowLayout] Error loading JSON: {e}")
        
        return False
    
    def _getOrderKey(self, item):
        """Get order key - uses JSON order if available, otherwise insertion index"""
        widget = item.widget()
        if not widget:
            return float('inf')
        
        if self._orderLoaded and self._widgetOrder:
            obj_name = widget.objectName()
            if isinstance(self._widgetOrder, list):
                if obj_name in self._widgetOrder:
                    return self._widgetOrder.index(obj_name)
            elif isinstance(self._widgetOrder, dict):
                if obj_name in self._widgetOrder:
                    return self._widgetOrder[obj_name]
        
        # Fallback to insertion order - THIS PRESERVES UI ORDER
        for idx, stored_item in enumerate(self._items):
            if stored_item == item:
                return idx
        
        return float('inf')
    
    def _getOrderedItems(self):
        """Return items sorted by order - PRESERVES RELATIVE ORDER"""
        items_with_order = []
        for item in self._items:
            widget = item.widget()
            if widget and not widget.isHidden():
                items_with_order.append((self._getOrderKey(item), item))
        
        items_with_order.sort(key=lambda x: x[0])
        return [item for _, item in items_with_order]
    
    def addItem(self, a0: QtWidgets.QLayoutItem) -> None:
        """ALWAYS APPEND - never reorder"""
        self._items.append(a0)
        if a0.widget() in self.__pendingPositions:
            del self.__pendingPositions[a0.widget()]
        self._scheduleLayoutUpdate()

    def addWidget(self, w: QtWidgets.QWidget, position: int = None, align: QtCore.Qt.AlignmentFlag = None) -> None:
        """ALWAYS APPEND - position parameter IGNORED to preserve order"""
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
        if a0 in self._items:
            self._items.remove(a0)
        if a0.widget():
            a0.widget().deleteLater()
        self._scheduleLayoutUpdate()

    def removeWidget(self, w: QtWidgets.QWidget) -> None:
        for item in self._items[:]:
            if item.widget() == w:
                self._items.remove(item)
                break
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
    
    # ========== Properties (set by QCustomFlowWidget) ==========
    
    @property
    def equalDistribution(self):
        return self._equalDistribution
    
    @equalDistribution.setter
    def equalDistribution(self, enabled):
        self._equalDistribution = enabled
        self._scheduleLayoutUpdate()
    
    @property
    def autoFillWidth(self):
        return self._autoFillWidth
    
    @autoFillWidth.setter
    def autoFillWidth(self, enabled):
        self._autoFillWidth = enabled
        if enabled:
            self._equalDistribution = enabled
        self._scheduleLayoutUpdate()
    
    @property
    def autoFillHeight(self):
        return self._autoFillHeight
    
    @autoFillHeight.setter
    def autoFillHeight(self, enabled):
        self._autoFillHeight = enabled
        self._scheduleLayoutUpdate()
    
    @property
    def justifySpacing(self):
        return self._justifySpacing
    
    @justifySpacing.setter
    def justifySpacing(self, enabled):
        self._justifySpacing = enabled
        self._scheduleLayoutUpdate()
    
    @property
    def orderJsonPath(self):
        return self._orderJsonPath
    
    @orderJsonPath.setter
    def orderJsonPath(self, path):
        self._orderJsonPath = path if path else ""
        self._orderLoaded = self.loadOrderFromJson() if self._orderJsonPath else False
        self._scheduleLayoutUpdate()
    
    # ========== Animation Methods ==========
    
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
            try:
                self._updateTimer.start(10)
            except RuntimeError:
                # the debounce timer's C++ object was already deleted (e.g.
                # during teardown); there is nothing left to schedule.
                pass
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
        if not widget:
            return QtCore.QSize(0, 0)
        
        size = widget.sizeHint()
        if not size.isValid():
            size = widget.minimumSizeHint()
        if not size.isValid():
            size = widget.minimumSize()
        if not size.isValid():
            size = widget.size()
        
        max_width = widget.maximumWidth()
        max_height = widget.maximumHeight()
        
        if max_width > 0 and max_width < 32767:
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
        """widgets_and_sizes is list of (widget, size) tuples"""
        n = len(widgets_and_sizes)
        if n == 0:
            return []
        
        min_widths = []
        max_widths = []
        
        for widget, size in widgets_and_sizes:
            min_w = widget.minimumWidth() if widget.minimumWidth() > 0 else size.width()
            max_w = widget.maximumWidth() if widget.maximumWidth() < 32767 else 32767
            min_widths.append(min_w)
            max_widths.append(max_w)
        
        total_spacing = (n - 1) * spacing
        available_for_widgets = available_width - total_spacing
        equal_width = available_for_widgets / n
        
        widths = []
        for i in range(n):
            clamped = max(min_widths[i], min(equal_width, max_widths[i]))
            widths.append(clamped)
        
        total_width = sum(widths)
        
        if total_width < available_for_widgets:
            remaining = available_for_widgets - total_width
            expandable_indices = [i for i in range(n) if widths[i] < max_widths[i]]
            
            while remaining > 0.1 and expandable_indices:
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
        
        elif total_width > available_for_widgets:
            excess = total_width - available_for_widgets
            shrinkable_indices = [i for i in range(n) if widths[i] > min_widths[i]]
            
            while excess > 0.1 and shrinkable_indices:
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
    
    def _buildRows(self, effective_width):
        """Build rows using STRICT ORDER - items flow left to right, top to bottom"""
        ordered_items = self._getOrderedItems()
        
        if not ordered_items:
            return []
        
        spacing = self.spacing()
        rows = []
        current_row = []
        current_width = 0
        max_height = 0
        
        for item in ordered_items:
            widget = item.widget()
            if not widget or widget.isHidden():
                continue
            
            size = self._getWidgetSize(widget)
            item_width = size.width()
            
            projected = current_width
            if current_row:
                projected += spacing + item_width
            else:
                projected += item_width
            
            if projected > effective_width and current_row:
                rows.append((current_row, current_width, max_height))
                current_row = [(widget, size)]
                current_width = item_width
                max_height = size.height()
            else:
                current_row.append((widget, size))
                if len(current_row) > 1:
                    current_width += spacing
                current_width += item_width
                max_height = max(max_height, size.height())
        
        if current_row:
            rows.append((current_row, current_width, max_height))
        
        return rows
    
    def _calculateLayout(self, rect, outGeometries):
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
        rows = self._buildRows(effectiveRect.width())
        
        currentY = rect.y() + margins[1]
        
        for row_items, total_natural_width, natural_row_height in rows:
            currentX = effectiveRect.x()
            row_height = natural_row_height
            
            if self._equalDistribution and len(row_items) > 0:
                widths = self._distributeEqualWidths(row_items, effectiveRect.width(), spacing)
                
                for i, (widget, _) in enumerate(row_items):
                    new_width = widths[i]
                    
                    max_width = widget.maximumWidth()
                    if max_width > 0 and max_width < 32767:
                        new_width = min(new_width, max_width)
                    
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
                remaining_space = effectiveRect.width() - total_natural_width
                space_between = remaining_space / (len(row_items) - 1)
                
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
                for widget, itemSize in row_items:
                    widgetGeometry = QtCore.QRect(
                        QtCore.QPoint(int(currentX), currentY),
                        itemSize
                    )
                    outGeometries[widget] = widgetGeometry
                    currentX += itemSize.width() + spacing
            
            currentY += row_height + spacing
        
        # Handle autoFillHeight
        if self._autoFillHeight and len(rows) > 0:
            total_spacing_y = (len(rows) - 1) * spacing
            available_height = effectiveRect.height() - total_spacing_y
            total_original_height = sum(row_height for _, _, row_height in rows)
            
            if available_height > total_original_height:
                extra_per_row = (available_height - total_original_height) / len(rows)
                currentY = rect.y() + margins[1]
                
                for row_items, _, row_height in rows:
                    new_row_height = row_height + extra_per_row
                    
                    for widget, _ in row_items:
                        max_height = widget.maximumHeight()
                        final_height = new_row_height
                        if max_height > 0 and max_height < 32767:
                            final_height = min(final_height, max_height)
                        
                        if widget in outGeometries:
                            old_geom = outGeometries[widget]
                            outGeometries[widget] = QtCore.QRect(
                                old_geom.topLeft(),
                                QtCore.QSize(old_geom.width(), int(final_height))
                            )
                    
                    currentY += new_row_height + spacing
    
    def _doLayout(self, rect, testOnly, animate=True):
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
        rows = self._buildRows(effectiveRect.width())
        
        currentY = rect.y() + margins[1]
        
        for row_items, total_natural_width, natural_row_height in rows:
            currentX = effectiveRect.x()
            row_height = natural_row_height
            
            if self._equalDistribution and len(row_items) > 0:
                widths = self._distributeEqualWidths(row_items, effectiveRect.width(), spacing)
                
                for i, (widget, _) in enumerate(row_items):
                    new_width = widths[i]
                    
                    max_width = widget.maximumWidth()
                    if max_width > 0 and max_width < 32767:
                        new_width = min(new_width, max_width)
                    
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
                                animation.setEasingCurve(self._getEasingCurve())
                                animation.setStartValue(widget.geometry())
                                animation.setEndValue(targetGeometry)
                                animation.start()
                                self._currentAnimations.append(animation)
                                animation.finished.connect(lambda a=animation: self._cleanupAnimation(a))
                        else:
                            widget.setGeometry(targetGeometry)
                    
                    currentX += new_width + spacing
                    
            elif self._justifySpacing and len(row_items) > 1:
                remaining_space = effectiveRect.width() - total_natural_width
                space_between = remaining_space / (len(row_items) - 1)
                
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
                                animation.setEasingCurve(self._getEasingCurve())
                                animation.setStartValue(widget.geometry())
                                animation.setEndValue(targetGeometry)
                                animation.start()
                                self._currentAnimations.append(animation)
                                animation.finished.connect(lambda a=animation: self._cleanupAnimation(a))
                        else:
                            widget.setGeometry(targetGeometry)
                    
                    currentX += itemSize.width()
                    if i < len(row_items) - 1:
                        currentX += space_between
            else:
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
                                animation.setEasingCurve(self._getEasingCurve())
                                animation.setStartValue(widget.geometry())
                                animation.setEndValue(targetGeometry)
                                animation.start()
                                self._currentAnimations.append(animation)
                                animation.finished.connect(lambda a=animation: self._cleanupAnimation(a))
                        else:
                            widget.setGeometry(targetGeometry)
                    
                    currentX += itemSize.width() + spacing
            
            currentY += row_height + spacing
        
        # Handle autoFillHeight
        if self._autoFillHeight and len(rows) > 0 and not testOnly:
            total_spacing_y = (len(rows) - 1) * spacing
            available_height = effectiveRect.height() - total_spacing_y
            total_original_height = sum(row_height for _, _, row_height in rows)
            
            if available_height > total_original_height:
                extra_per_row = (available_height - total_original_height) / len(rows)
                currentY = rect.y() + margins[1]
                
                for row_items, _, row_height in rows:
                    new_row_height = row_height + extra_per_row
                    
                    for widget, _ in row_items:
                        max_height = widget.maximumHeight()
                        final_height = new_row_height
                        if max_height > 0 and max_height < 32767:
                            final_height = min(final_height, max_height)
                        
                        current_geom = widget.geometry()
                        targetGeometry = QtCore.QRect(
                            current_geom.topLeft(),
                            QtCore.QSize(current_geom.width(), int(final_height))
                        )
                        
                        if animate and self._animate and not self._updatingLayout:
                            if widget.geometry() != targetGeometry:
                                animation = QtCore.QPropertyAnimation(widget, b"geometry")
                                animation.setDuration(self._animationDuration)
                                animation.setEasingCurve(self._getEasingCurve())
                                animation.setStartValue(widget.geometry())
                                animation.setEndValue(targetGeometry)
                                animation.start()
                                self._currentAnimations.append(animation)
                                animation.finished.connect(lambda a=animation: self._cleanupAnimation(a))
                        else:
                            widget.setGeometry(targetGeometry)
                    
                    currentY += new_row_height + spacing
        
        total_height = currentY - spacing + margins[3] - rect.y()
        return max(total_height, 0)
    
    def _cleanupAnimation(self, animation):
        if animation in self._currentAnimations:
            self._currentAnimations.remove(animation)
    
    def stopAllAnimations(self):
        for animation in self._currentAnimations:
            animation.stop()
        self._currentAnimations.clear()
        if self._animationGroup:
            self._animationGroup.stop()
            self._animationGroup = None
    
    def isAnimating(self):
        return len(self._currentAnimations) > 0 or self._animationGroup is not None