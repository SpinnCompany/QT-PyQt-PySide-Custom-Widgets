########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/@SpinnTV
# WEBSITE: customwidgets.org
########################################################################

from qtpy.QtCore import Qt, QEasingCurve, QRect, QSettings, QParallelAnimationGroup, QPropertyAnimation, QSize, QEvent, Signal
from qtpy.QtGui import QColor, QPaintEvent, QPainter, QResizeEvent, QMoveEvent
from qtpy.QtWidgets import QWidget, QGraphicsDropShadowEffect, QStyleOption, QStyle, QPushButton, QToolButton, QRadioButton, QCheckBox

from Custom_Widgets.Utils import get_icon_path, replace_url_prefix, is_in_designer
from Custom_Widgets.Log import *

import re

class QCustomSlideMenu(QWidget):
    # Define new signals for collapse and expand events
    onCollapsed = Signal()
    onExpanded = Signal()

    onCollapsing = Signal()
    onExpanding = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.installEventFilter(self)

        if self.parent():
            self.parent().installEventFilter(self)
        
        self.initializeVariables()

    def initializeVariables(self):
        # SET DEFAULT SIZE - Use current widget dimensions as defaults
        self._defaultWidth = self.width()
        self._defaultHeight = self.height()

        # Collapsed dimensions - widget shrinks to these values when collapsed
        self._collapsedWidth = 0
        self._collapsedHeight = 0

        # Expanded dimensions - widget expands to these values when opened
        self._expandedWidth = self._defaultWidth
        self._expandedHeight = self._defaultHeight

        # Animation properties
        self._animationDuration = 500  # Default animation duration in milliseconds
        self._animationEasingCurve = QEasingCurve.Linear  # Default easing curve

        # Separate animation properties for collapsing and expanding
        self._collapsingAnimationDuration = self._animationDuration
        self._collapsingAnimationEasingCurve = self._animationEasingCurve

        self._expandingAnimationDuration = self._animationDuration
        self._expandingAnimationEasingCurve = self._animationEasingCurve

        # Icon paths for toggle button in different states
        self._iconCollapsed = ""  # Icon when menu is collapsed
        self._iconExpanded = ""   # Icon when menu is expanded

        # State flags
        self._collapsed = False  # Whether menu is currently collapsed
        self._expanded = False   # Whether menu is currently expanded

        # Toggle button properties
        self._toggleButton = None      # Reference to the toggle button widget
        self._toggleButtonName = ""    # Object name of the toggle button

        # Widget original state
        self._originalSize = self.size()            # Store original size

        # State tracking 
        self._isCollapsed = False  # Track if widget is in collapsed state
        self._isExpanded = False   # Track if widget is in expanded state
    
    def setMinSize(self):
        try:
            # getDefault*() resolves the legacy "auto"/"parent" string values
            self.setMinimumSize(QSize(self.getDefaultWidth(), self.getDefaultHeight()))
        except:
            pass

    # Customize menu
    def customizeQCustomSlideMenu(self, **customValues):
        # Extract update flag with safe default
        update = customValues.get("update", False)
        
        # Process size configurations
        self._processSizeConfigurations(customValues, update)
        
        # Process animation configurations  
        self._processAnimationConfigurations(customValues)
        
        # Process shadow effect configurations
        self._processShadowConfigurations(customValues)
        
        # Process toggle button configurations
        self._processToggleButtonConfigurations(customValues)
        
        # Finalize configuration
        self._finalizeConfiguration(update)

    def _processSizeConfigurations(self, customValues, update):
        """Process all size-related configurations."""
        # Default width configuration
        if "defaultWidth" in customValues:
            self._defaultWidth = customValues["defaultWidth"]
            if isinstance(self._defaultWidth, int):
                if not update:
                    self.setMaximumWidth(self._defaultWidth)
                    self.setMinimumWidth(self._defaultWidth)
            elif self._defaultWidth == "parent" and self.parent():
                self.setMinimumWidth(self.parent().width())
                self.setMaximumWidth(16777215)  # Qt's maximum widget size

        # Default height configuration
        if "defaultHeight" in customValues:
            self._defaultHeight = customValues["defaultHeight"]
            if isinstance(self._defaultHeight, int):
                if not update:
                    self.setMaximumHeight(self._defaultHeight)
                    self.setMinimumHeight(self._defaultHeight)
            elif self._defaultHeight == "parent" and self.parent():
                self.setMinimumHeight(self.parent().height())
                self.setMaximumHeight(16777215)

        # Collapsed dimensions
        if "collapsedWidth" in customValues:
            self._collapsedWidth = customValues["collapsedWidth"]
            
        if "collapsedHeight" in customValues:
            self._collapsedHeight = customValues["collapsedHeight"]

        # Expanded dimensions  
        if "expandedWidth" in customValues:
            self._expandedWidth = customValues["expandedWidth"]
            
        if "expandedHeight" in customValues:
            self._expandedHeight = customValues["expandedHeight"]

        self.animateDefaultSize()

    def _processAnimationConfigurations(self, customValues):
        """Process all animation-related configurations."""
        # Main animation properties
        if "animationDuration" in customValues:
            duration = customValues["animationDuration"]
            if int(duration) > 0:
                self._animationDuration = duration

        if "animationEasingCurve" in customValues:
            curve = customValues["animationEasingCurve"]
            if curve:  # Simplified check
                self._animationEasingCurve = curve

        # Collapsing animation properties
        if "collapsingAnimationDuration" in customValues:
            duration = customValues["collapsingAnimationDuration"]
            if int(duration) > 0:
                self._collapsingAnimationDuration = duration

        if "collapsingAnimationEasingCurve" in customValues:
            curve = customValues["collapsingAnimationEasingCurve"]
            if curve:
                self._collapsingAnimationEasingCurve = curve

        # Expanding animation properties
        if "expandingAnimationDuration" in customValues:
            duration = customValues["expandingAnimationDuration"]
            if int(duration) > 0:
                self._expandingAnimationDuration = duration

        if "expandingAnimationEasingCurve" in customValues:
            curve = customValues["expandingAnimationEasingCurve"]
            if curve:
                self._expandingAnimationEasingCurve = curve

    def _processShadowConfigurations(self, customValues):
        """Process shadow effect configurations."""
        # Create or recreate shadow effect
        self.shadow_effect = QGraphicsDropShadowEffect(self)
        
        # Shadow color
        if "shadowColor" in customValues:
            color_str = str(customValues["shadowColor"])
            self.shadow_effect.setColor(QColor(color_str))
        
        # Shadow properties
        self._apply_shadow = False
        
        if "shadowBlurRadius" in customValues:
            blur_radius = int(customValues["shadowBlurRadius"])
            self.shadow_effect.setBlurRadius(blur_radius)
            self._apply_shadow = blur_radius > 0  # Only apply if radius > 0
        
        if "shadowXOffset" in customValues:
            self.shadow_effect.setXOffset(int(customValues["shadowXOffset"]))
        
        if "shadowYOffset" in customValues:
            self.shadow_effect.setYOffset(int(customValues["shadowYOffset"]))
        
        # Apply shadow effect if not in designer and shadow is enabled
        if not is_in_designer(self) and self._apply_shadow:
            self.setGraphicsEffect(None)  # Clear existing effect
            self.setGraphicsEffect(self.shadow_effect)

    def _processToggleButtonConfigurations(self, customValues):
        """Process toggle button configurations."""
        toggle_kwargs = {}
        
        if "toggleButtonName" in customValues:
            self._toggleButtonName = customValues["toggleButtonName"]
            toggle_kwargs["buttonName"] = self._toggleButtonName
        
        if "iconWhenMenuIsCollapsed" in customValues:
            self._iconWhenMenuIsCollapsed = customValues["iconWhenMenuIsCollapsed"]
            toggle_kwargs["iconWhenMenuIsCollapsed"] = self._iconWhenMenuIsCollapsed
        
        if "iconWhenMenuIsExpanded" in customValues:
            self._iconWhenMenuIsExpanded = customValues["iconWhenMenuIsExpanded"]
            toggle_kwargs["iconWhenMenuIsExpanded"] = self._iconWhenMenuIsExpanded
        
        # Configure toggle button if any relevant parameters were provided
        if toggle_kwargs:
            self.toggleButton(**toggle_kwargs)

    def _finalizeConfiguration(self, update):
        """Finalize configuration with updates and state management."""
        if update:
            # Refresh and animate to appropriate state
            self.refresh()
            if not self.isCollapsed():
                self.expandMenu()
            else:
                self.collapseMenu()
        elif self._defaultWidth == 0 or self._defaultHeight == 0:
            # Hide widget if default dimensions are zero
            self.setMaximumWidth(0)
            self.setMaximumHeight(0)

    # Menu Toggle Button
    def toggleMenu(self):
        self.slideMenu()

    def toggle(self):
        self.toggleMenu()

    def activateMenuButton(self, buttonObject):
        if is_in_designer(self):
            return
        # Remove any PREVIOUS connection. We connect a lambda, so we must keep a
        # reference to that exact slot to disconnect it — disconnecting
        # self.toggleMenu (a different object) silently fails and leaves the old
        # lambda connected. Re-wiring then stacks connections, and an even count
        # makes a single click toggle-and-untoggle (the menu never moves).
        prev_slot = getattr(self, "_menuToggleSlot", None)
        prev_btn = getattr(self, "_menuToggleButton", None)
        if prev_slot is not None and prev_btn is not None:
            try:
                prev_btn.clicked.disconnect(prev_slot)
            except (TypeError, RuntimeError):
                pass

        slot = lambda: self.toggleMenu()
        buttonObject.clicked.connect(slot)
        self._menuToggleSlot = slot
        self._menuToggleButton = buttonObject
        self._isMenuConnected = True  # Update the connection status

    def toggleButton(self, **values):
        if not hasattr(self, "_toggleButton") and not "buttonName" in values:
            raise Exception("No button specified for this widget, please specify the QPushButton object")

        if "buttonName" in values:
            buttonName = values["buttonName"]
            
            if not buttonName.strip():
                return
            
            # Attempt to get the button object by name
            toggleButton = self.getButtonByName(buttonName)

            # Proceed only if the button was found
            if toggleButton:
                # Check if the current target button is different from the new one
                if not hasattr(self, "_toggleButton") or self._toggleButton != toggleButton:
                    # Reset properties for the new target button only if they do not exist
                    if not hasattr(toggleButton, 'menuCollapsedIcon'):
                        toggleButton.menuCollapsedIcon = ""
                    if not hasattr(toggleButton, 'menuExpandedIcon'):
                        toggleButton.menuExpandedIcon = ""

                # Assign the new target menu to the button
                toggleButton.targetMenu = self

                # Set the new target button
                self._toggleButton = toggleButton

                # Activate the menu functionality for the button
                self.activateMenuButton(self._toggleButton)
            else:
                logCritical(f"Button with name '{buttonName}' not found.")

        if self._toggleButton:
            if "iconWhenMenuIsCollapsed" in values and len(str(values["iconWhenMenuIsCollapsed"])) > 0:
                self._toggleButton.menuCollapsedIcon = str(values["iconWhenMenuIsCollapsed"])

            if "iconWhenMenuIsExpanded" in values and len(str(values["iconWhenMenuIsExpanded"])) > 0:
                self._toggleButton.menuExpandedIcon = str(values["iconWhenMenuIsExpanded"])


    def getButtonByName(self, buttonName):
        """Recursively search for a button by objectName in children and parent containers."""
        # List of button classes to search for
        button_classes = [QPushButton, QToolButton, QRadioButton, QCheckBox]

        # Add your custom sidebar button
        try:
            from Custom_Widgets.QCustomSidebarButton import QCustomSidebarButton
            button_classes.append(QCustomSidebarButton)
        except ImportError:
            QCustomSidebarButton = None  # optional safety

        # Recursive depth-first search for children
        def search_children(widget: QWidget):
            if widget.objectName() == buttonName and isinstance(widget, tuple(button_classes)):
                return widget
            for child in widget.children():
                if isinstance(child, QWidget):
                    result = search_children(child)
                    if result:
                        return result
            return None

        # Recursive search upwards in parents
        def search_parents(widget: QWidget):
            parent = widget.parent()
            while parent:
                if parent.objectName() == buttonName and isinstance(parent, tuple(button_classes)):
                    return parent
                # Also search siblings/children of the parent
                result = search_children(parent)
                if result:
                    return result
                parent = parent.parent()
            return None

        # First search downwards
        result = search_children(self)
        if result:
            return result

        # If not found, search upwards
        return search_parents(self)


    # Slide menu function
    def slideMenu(self):
        # Toggle on the LOGICAL open state, not the size-derived flags:
        # refresh() recomputes _collapsed/_expanded from the current size,
        # which is ambiguous while animating and whenever an "auto" size
        # hint changes after styles are applied.
        menu_open = getattr(self, "_menuOpen", None)
        if menu_open is None:
            menu_open = not self.isCollapsed()
        if menu_open:
            self.collapseMenu()
        else:
            self.expandMenu()

    def expandMenu(self):
        self._menuOpen = True
        self._collapsed = True
        self._expanded = False

        self.animateMenu()

        self._collapsed = False
        self._expanded = True

    def collapseMenu(self):
        self._menuOpen = False
        self._collapsed = False
        self._expanded = True
        self.animateMenu()
        self._collapsed = True
        self._expanded = False


    def emitStatusSignal(self):
        # Use the direction recorded at animation start: the _expanded /
        # _collapsed flags are rewritten by refresh() while the animation's
        # own resize events are processed, so they are unreliable here.
        direction = getattr(self, "_animatingExpand", None)
        if direction is True:
            self.onExpanded.emit()
        elif direction is False:
            self.onCollapsed.emit()
        elif self._expanded:
            self.onExpanded.emit()
        elif self._collapsed:
            self.onCollapsed.emit()

    def animateMenu(self):
        # Remember which way THIS animation goes (True = expanding). At entry
        # _collapsed is True when expandMenu() started the animation.
        self._animatingExpand = bool(self._collapsed)

        self.setMinimumSize(QSize(0, 0))
        startHeight = self.height()
        startWidth = self.width()

        # Create a parallel animation group
        self.animation_group = QParallelAnimationGroup(self)

        minWidth, maxWidth = self.determineWith()
        minHeight, maxHeight = self.determineHeight()
        
        # print(f"Animating menu from ({startWidth}, {startHeight}) to widths ({minWidth}, {maxWidth}) and heights ({minHeight}, {maxHeight})")

        width_animation = self.createAnimation(b"minimumWidth", startWidth, minWidth)
        height_animation = self.createAnimation(b"minimumHeight", startHeight, minHeight)

        width_animation_2 = self.createAnimation(b"maximumWidth", startWidth, maxWidth)
        height_animation_2 = self.createAnimation(b"maximumHeight", startHeight, maxHeight)

        # Add animations to the parallel group
        if self._collapsedHeight != self._expandedHeight:
            self.animation_group.addAnimation(height_animation)
            self.animation_group.addAnimation(height_animation_2)

        if self._collapsedWidth != self._expandedWidth:
            self.animation_group.addAnimation(width_animation)
            self.animation_group.addAnimation(width_animation_2)
        
        self._expanded = not self._expanded
        self._collapsed = not self._collapsed

        # Start the parallel animations
        self.animation_group.start()

        # Connect finished signal to applyWidgetStyle for both animations
        self.animation_group.finished.connect(self.emitStatusSignal)

    def createAnimation(self, property_name, start_value, end_value):
        animation = QPropertyAnimation(self, property_name)
        animation.setDuration(self._expandingAnimationDuration if self._collapsed else self._collapsingAnimationDuration)
        animation.setEasingCurve(self._expandingAnimationEasingCurve if self._collapsed else self._collapsingAnimationEasingCurve)
        animation.setStartValue(start_value)
        animation.setEndValue(end_value)

        # Handle maximum height or width adjustments after the animation
        animation.finished.connect(lambda: self.adjustMaximumSize(property_name))
        
        return animation

    def determineWith(self):
        # Determine end sizes based on the current state
        if self._collapsed:
            minWidth, maxWidth = self.calculateEndWidth(self._expandedWidth)

        else:  # self._expanded
            minWidth, maxWidth = self.calculateEndWidth(self._collapsedWidth)

        return minWidth, maxWidth

    def determineHeight(self):
        # Determine end sizes based on the current state
        if self._collapsed:
            minHeight, maxHeight = self.calculateEndHeight(self._expandedHeight)

        else:  # self._expanded
            minHeight, maxHeight = self.calculateEndHeight(self._collapsedHeight)

        return minHeight, maxHeight

    def calculateEndWidth(self, width):
        if width == "parent":
            return 0, self.parent().width()

        if width == "auto":
            # "auto" (legacy/Designer value): size to the widget's content hint
            autoWidth = self.autoContentSize().width()
            return autoWidth, autoWidth

        return int(width), int(width)

    def calculateEndHeight(self, height):
        if height == "parent":
            return 0, self.parent().height()

        if height == "auto":
            # "auto" (legacy/Designer value): size to the widget's content hint
            autoHeight = self.autoContentSize().height()
            return autoHeight, autoHeight

        return int(height), int(height)

    def autoContentSize(self):
        """Size used for the legacy "auto" width/height value: the widget's
        own content size hint (falls back to minimumSizeHint)."""
        hint = self.sizeHint()
        if not hint.isValid() or (hint.width() <= 0 and hint.height() <= 0):
            hint = self.minimumSizeHint()
        return QSize(max(hint.width(), 0), max(hint.height(), 0))

    def adjustMaximumSize(self, property_name):
        if not getattr(self, "_animatingExpand", False):
            # Only release the size constraints after an EXPAND animation:
            # doing it after a collapse would let the layout re-open the menu.
            return

        if self._expandedWidth in ("parent", "auto"):
                self.setMaximumWidth(16777215)  # Reset to max after expanding

        if self._expandedHeight in ("parent", "auto"):
            self.setMaximumHeight(16777215)  # Reset to max after expanding

    def refresh(self):
        if self.isExpanded() and not self.isCollapsed():
            self._collapsed = False
            self._expanded = True
        else:
            self._collapsed = True
            self._expanded = False

    def isExpanded(self):
        """
        Determines if the widget is in an expanded state by comparing its
        current width and height to the expanded dimensions. A dimension is
        only meaningful when it actually CHANGES between the collapsed and
        expanded configurations (e.g. with both widths "auto" the width never
        moves, so it must not report the menu as expanded).
        """
        if (self._collapsedWidth != self._expandedWidth
                and self._expandedWidth != "parent"
                and self.width() >= self.getExpandedWidth()):
            return True
        if (self._collapsedHeight != self._expandedHeight
                and self._expandedHeight != "parent"
                and self.height() >= self.getExpandedHeight()):
            return True

        return False

    def isCollapsed(self):
        """
        Determines if the widget is in a collapsed state by comparing its
        current width and height to the collapsed dimensions. Dimensions that
        do not change between the two configurations are ignored.
        """
        checks = []
        if self._collapsedWidth != self._expandedWidth:
            checks.append(self.width() <= self.getCollapsedWidth())
        if self._collapsedHeight != self._expandedHeight:
            checks.append(self.height() <= self.getCollapsedHeight())
        if not checks:
            return (self.width() <= self.getCollapsedWidth() and
                    self.height() <= self.getCollapsedHeight())
        return all(checks)


    def getDefaultWidth(self):
        if isinstance(self._defaultWidth, int):
            return self._defaultWidth
        if self._defaultWidth == "auto":
            return self.autoContentSize().width()
        if self._defaultWidth == "parent":
            parent = self.parentWidget()
            if parent:
                margins = parent.contentsMargins()
                return parent.sizeHint().width() - (margins.left() + margins.right())
        return 0  # Default return if no valid width is found

    def getDefaultHeight(self):
        if isinstance(self._defaultHeight, int):
            return self._defaultHeight

        if self._defaultHeight == "auto":
            return self.autoContentSize().height()

        if self._defaultHeight == "parent":
            parent = self.parentWidget()
            if parent:
                margins = parent.contentsMargins()
                return parent.sizeHint().height() - (margins.top() + margins.bottom())
        return 0  # Default return if no valid height is found

    def getCollapsedWidth(self):
        if isinstance(self._collapsedWidth, int):
            return self._collapsedWidth
        if self._collapsedWidth == "auto":
            return self.autoContentSize().width()
        if self._collapsedWidth == "parent":
            parent = self.parentWidget()
            if parent:
                margins = parent.contentsMargins()
                return parent.sizeHint().width() - (margins.left() + margins.right())
        return 0  # Default return if no valid width is found

    def getCollapsedHeight(self):
        if isinstance(self._collapsedHeight, int):
            return self._collapsedHeight
        if self._collapsedHeight == "auto":
            return self.autoContentSize().height()
        if self._collapsedHeight == "parent":
            parent = self.parentWidget()
            if parent:
                margins = parent.contentsMargins()
                return parent.sizeHint().height() - (margins.top() + margins.bottom())
        return 0  # Default return if no valid height is found

    def getExpandedWidth(self):
        if isinstance(self._expandedWidth, int):
            return self._expandedWidth

        if self._expandedWidth == "auto":
            return self.autoContentSize().width()

        if self._expandedWidth == "parent":
            parent = self.parentWidget()
            if parent:
                margins = parent.contentsMargins()
                return parent.sizeHint().width() - (margins.left() + margins.right())
        return 0  # Default return if no valid width is found

    def getExpandedHeight(self):
        if isinstance(self._expandedHeight, int):
            return self._expandedHeight
        if self._expandedHeight == "auto":
            return self.autoContentSize().height()
        if self._expandedHeight == "parent":
            parent = self.parentWidget()
            if parent:
                margins = parent.contentsMargins()

                return parent.sizeHint().height() - (margins.top() + margins.bottom())
        return 0  # Default return if no valid height is found
    
    def animateDefaultSize(self):
        """
        Determines if the widget is in an expanded state by comparing its
        current width and height to the expanded dimensions.
        """        
        if (self.getDefaultWidth() > self.getCollapsedWidth() or
                self.getDefaultHeight() > self.getCollapsedHeight()):
            self.expandMenu()
        else:
            self.collapseMenu()

    def showEvent(self, event):
        super().showEvent(event)             
        self.setMinSize()
        self.animateDefaultSize()

    def paintEvent(self, event: QPaintEvent):
        opt = QStyleOption()
        opt.initFrom(self)
        painter = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, painter, self)

    def eventFilter(self, obj, event: QEvent):
        # Handle Resize, Move, and other events
        if event.type() == QEvent.Resize:
            resize_event = QResizeEvent(event.size(), event.oldSize())
            self.resize(resize_event.size())
            self.refresh()

        elif event.type() == QEvent.Move:
            move_event = QMoveEvent(event.pos(), event.oldPos())
            self.move(move_event.pos())
            self.refresh()

        elif event.type() in [QEvent.WindowStateChange, QEvent.Paint]:
            if obj is self.window():
                self.refresh()

        return super().eventFilter(obj, event)
    