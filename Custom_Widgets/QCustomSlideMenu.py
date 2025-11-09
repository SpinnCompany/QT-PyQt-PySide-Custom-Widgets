########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/spinnTv
# WEBSITE: spinncode.com
########################################################################

from qtpy.QtCore import Qt, QEasingCurve, QRect, QSettings, QParallelAnimationGroup, QPropertyAnimation, QSize, QEvent, Signal
from qtpy.QtGui import QColor, QPaintEvent, QPainter, QResizeEvent, QMoveEvent
from qtpy.QtWidgets import QWidget, QGraphicsDropShadowEffect, QStyleOption, QStyle, QPushButton

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

        # SET DEFAULT SIZE
        self._defaultWidth = self.width()
        self._defaultHeight = self.height()

        self._collapsedWidth = 0
        self._collapsedHeight = 0

        self._expandedWidth = self._defaultWidth
        self._expandedHeight = self._defaultHeight

        self._animationDuration = 500
        self._animationEasingCurve = QEasingCurve.Linear

        self._collapsingAnimationDuration = self._animationDuration
        self._collapsingAnimationEasingCurve = self._animationEasingCurve

        self._expandingAnimationDuration = self._animationDuration
        self._expandingAnimationEasingCurve = self._animationEasingCurve

        self._collapsedStyle = ""
        self._expandedStyle = ""

        self._iconCollapsed = ""
        self._iconExpanded = ""

        self._collapsed = False
        self._expanded = False

        self._float = False
        self._floatPosition = ""
        self._floatParent = None
        self._autoHide = False
        # Initialize margin properties
        self._marginTop = 0
        self._marginRight = 0
        self._marginBottom = 0
        self._marginLeft = 0

        self._toggleButton = None
        self._toggleButtonName = ""

        self._widgetObjectName = self.objectName()
        self._originalSize = self.size()

        self._isColllapsed = False
        self._isExpanded = False
    
    def setMinSize(self):
        try:
            self.setMinimumSize(QSize(self._defaultWidth, self._defaultHeight))
        except:
            pass

    def setObjectName(self, name):
        self._widgetObjectName = name

    # Customize menu
    def customizeQCustomSlideMenu(self, **customValues):
        if "update" in customValues and customValues["update"]:
            update = customValues["update"]
        else:
            update = False
        if "defaultWidth" in customValues:
            self._defaultWidth = customValues["defaultWidth"]
            if isinstance(customValues["defaultWidth"], int):
                if not update:
                    self.setMaximumWidth(customValues["defaultWidth"])
                    self.setMinimumWidth(customValues["defaultWidth"])

            elif customValues["defaultWidth"] == "parent":
                self.setMinimumWidth(self.parent().width())
                self.setMaximumWidth(16777215)


        if "defaultHeight" in customValues:
            self._defaultHeight = customValues["defaultHeight"]
            if isinstance(customValues["defaultHeight"], int):
                if not update:
                    self.setMaximumHeight(customValues["defaultHeight"])
                    self.setMinimumHeight(customValues["defaultHeight"])

            elif customValues["defaultHeight"] == "parent":
                self.setMinimumHeight(self.parent().height())
                self.setMaximumHeight(16777215)

        if "collapsedWidth" in customValues:
            self._collapsedWidth = customValues["collapsedWidth"]

        if "collapsedHeight" in customValues:
            self._collapsedHeight = customValues["collapsedHeight"]

        if "expandedWidth" in customValues:
            self._expandedWidth = customValues["expandedWidth"]

        if "expandedHeight" in customValues:
            self._expandedHeight = customValues["expandedHeight"]

        if "animationDuration" in customValues and int(customValues["animationDuration"]) > 0:
            self._animationDuration = customValues["animationDuration"]

        if "animationEasingCurve" in customValues and len(str(customValues["animationEasingCurve"])) > 0:
            self._animationEasingCurve = customValues["animationEasingCurve"]

        if "collapsingAnimationDuration" in customValues and int(customValues["collapsingAnimationDuration"]) > 0:
            self._collapsingAnimationDuration = customValues["collapsingAnimationDuration"]

        if "collapsingAnimationEasingCurve" in customValues and len(str(customValues["collapsingAnimationEasingCurve"])) > 0:
            self._collapsingAnimationEasingCurve = customValues["collapsingAnimationEasingCurve"]

        if "expandingAnimationDuration" in customValues and int(customValues["expandingAnimationDuration"]) > 0:
            self._expandingAnimationDuration = customValues["expandingAnimationDuration"]

        if "expandingAnimationEasingCurve" in customValues and len(str(customValues["expandingAnimationEasingCurve"])) > 0:
            self._expandingAnimationEasingCurve = customValues["expandingAnimationEasingCurve"]

        if "collapsedStyle" in customValues and len(str(customValues["collapsedStyle"])) > 0:
            self._collapsedStyle = str(customValues["collapsedStyle"])
            if self._collapsed:
                self.setStyleSheet(str(customValues["collapsedStyle"]))

        if "expandedStyle" in customValues and len(str(customValues["expandedStyle"])) > 0:
            self._expandedStyle = str(customValues["expandedStyle"])
            if self._expanded:
                self.setStyleSheet(str(customValues["expandedStyle"]))

        if "floatMenu" in customValues and customValues["floatMenu"] == True:
            self._float = True

        if "relativeTo" in customValues and len(str(customValues["relativeTo"])) > 0:
            self._floatParent = str(customValues["relativeTo"])

        if "position" in customValues and len(str(customValues["position"])) > 0:
            self._floatPosition = str(customValues["position"])

        
        self.shadow_effect = QGraphicsDropShadowEffect(self)
        if "shadowColor" in customValues:
            self.shadow_effect.setColor(QColor(str(customValues["shadowColor"])))
        
        self._apply_shadow = False
        if "shadowBlurRadius" in customValues:
            self.shadow_effect.setBlurRadius(int(customValues["shadowBlurRadius"]))
            self._apply_shadow = int(customValues["shadowBlurRadius"])
        
        if "shadowXOffset" in customValues:
            self.shadow_effect.setXOffset(int(customValues["shadowXOffset"]))
        
        if "shadowYOffset" in customValues:
            self.shadow_effect.setYOffset(int(customValues["shadowYOffset"]))
        
        if not is_in_designer(self) and self._apply_shadow:
            self.setGraphicsEffect(None)
            self.setGraphicsEffect(self.shadow_effect)

        if "autoHide" in customValues:
            self._autoHide = customValues["autoHide"]

        if "toggleButtonName" in customValues:
            self._toggleButtonName = customValues["toggleButtonName"]
            self.toggleButton(
                buttonName = self._toggleButtonName,
            )
        
        if "iconWhenMenuIsCollapsed" in customValues:
            self._iconWhenMenuIsCollapsed = customValues["iconWhenMenuIsCollapsed"]
            self.toggleButton(
                iconWhenMenuIsCollapsed = self._iconWhenMenuIsCollapsed,
            )
        
        if "iconWhenMenuIsExpanded" in customValues:
            self._iconWhenMenuIsExpanded = customValues["iconWhenMenuIsExpanded"]
            self.toggleButton(
                iconWhenMenuIsExpanded = self._iconWhenMenuIsExpanded,
            )

        if update:
            self.refresh()
            if not self.isCollapsed():
                self.expandMenu()
            else:
                self.collapseMenu()

        elif self._defaultWidth == 0 or self._defaultHeight == 0:
            self.setMaximumWidth(0)
            self.setMaximumHeight(0)
            
    def floatMenu(self):
        if self._float:
            # Step 1: If the widget is inside a layout, remove it from the layout
            parent = self.parent()  # Get the parent widget
            if parent is not None:
                parent_layout = parent.layout()  # Get the layout of the parent
                if parent_layout is not None:
                    try:
                        parent_layout.removeWidget(self)  # Remove widget from layout
                        # logging.info(f"{self} removed from parent layout {parent_layout}.")
                    except RuntimeError as e:
                        logException(e, "Failed to remove widget from parent layout")
                    except Exception as e:
                        logException(e, "Unexpected error occurred while removing widget from layout")

            # Ensure the widget is shown on top
            self.raise_()

            # Step 4: Position the widget based on the desired float position
            if not self._floatPosition:
                self._floatPosition = "center-center"

            position = str(self._floatPosition)
            self.positionFloatingWidget(position)  # Call method to position the widget

            # Step 5: Show the widget in its new floating state
            self.show()


    # Positioning logic with margins applied
    def positionFloatingWidget(self, position):
        _, maxWidth = self.determineWith()
        _, maxHeight = self.determineHeight()

        # Positioning logic with margins applied
        if position == "top-left":
            self.setGeometry(QRect(
                self.parent().x() + self._marginLeft, 
                self.parent().y() + self._marginTop, 
                maxWidth - (self._marginLeft + self._marginRight), 
                maxHeight - (self._marginTop + self._marginBottom)
            ))

        elif position == "top-right":
            self.setGeometry(QRect(
                self.parent().width() - maxWidth - self._marginRight, 
                self.parent().y() + self._marginTop, 
                maxWidth - (self._marginLeft + self._marginRight), 
                maxHeight - (self._marginTop + self._marginBottom)
            ))

        elif position == "top-center":
            self.setGeometry(QRect(
                (self.parent().width() - maxWidth) / 2 + self._marginLeft - self._marginRight, 
                self.parent().y() + self._marginTop, 
                maxWidth - (self._marginLeft + self._marginRight), 
                maxHeight - (self._marginTop + self._marginBottom)
            ))

        elif position == "bottom-right":
            self.setGeometry(QRect(
                self.parent().width() - maxWidth - self._marginRight, 
                self.parent().height() - maxHeight - self._marginBottom, 
                maxWidth - (self._marginLeft + self._marginRight), 
                maxHeight - (self._marginTop + self._marginBottom)
            ))

        elif position == "bottom-left":
            self.setGeometry(QRect(
                self.parent().x() + self._marginLeft, 
                self.parent().height() - maxHeight - self._marginBottom, 
                maxWidth - (self._marginLeft + self._marginRight), 
                maxHeight - (self._marginTop + self._marginBottom)
            ))

        elif position == "bottom-center":
            self.setGeometry(QRect(
                (self.parent().width() - maxWidth) / 2 + self._marginLeft - self._marginRight, 
                self.parent().height() - maxHeight - self._marginBottom, 
                maxWidth - (self._marginLeft + self._marginRight), 
                maxHeight - (self._marginTop + self._marginBottom)
            ))

        elif position == "center-center":
            self.setGeometry(QRect(
                (self.parent().width() - maxWidth) / 2 + self._marginLeft - self._marginRight, 
                (self.parent().height() - maxHeight) / 2 + self._marginTop - self._marginBottom, 
                maxWidth - (self._marginLeft + self._marginRight), 
                maxHeight - (self._marginTop + self._marginBottom)
            ))

        elif position == "center-left":
            self.setGeometry(QRect(
                self.parent().x() + self._marginLeft, 
                (self.parent().height() - maxHeight) / 2 + self._marginTop - self._marginBottom, 
                maxWidth - (self._marginLeft + self._marginRight), 
                maxHeight - (self._marginTop + self._marginBottom)
            ))

        elif position == "center-right":
            self.setGeometry(QRect(
                self.parent().width() - maxWidth - self._marginRight, 
                (self.parent().height() - maxHeight) / 2 + self._marginTop - self._marginBottom, 
                maxWidth - (self._marginLeft + self._marginRight), 
                maxHeight - (self._marginTop + self._marginBottom)
            ))

    # Menu Toggle Button
    def toggleMenu(self):
        self.slideMenu()
        self.applyButtonStyle()

    def toggle(self):
        self.toggleMenu()

    def activateMenuButton(self, buttonObject):
        # Use an attribute to track if the toggleMenu was connected
        if not hasattr(self, "_isMenuConnected"):
            self.isMenuConnected = False
        
        # Disconnect only if the toggleMenu is connected
        if self.isMenuConnected:
            try:
                # Disconnect the toggleMenu from the clicked signal
                buttonObject.clicked.disconnect(self.toggleMenu)
            except TypeError:
                # Ignore if no connection exists
                pass
            
        # Now safely connect the toggleMenu slot
        buttonObject.clicked.connect(lambda: self.toggleMenu())
        self._isMenuConnected = True  # Update the connection status

    def toggleButton(self, **values):
        if not hasattr(self, "_toggleButton") and not "buttonName" in values:
            raise Exception("No button specified for this widget, please specify the QPushButton object")

        if "buttonName" in values:
            buttonName = values["buttonName"]
            
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
                    if not hasattr(toggleButton, 'menuCollapsedStyle'):
                        toggleButton.menuCollapsedStyle = ""
                    if not hasattr(toggleButton, 'menuExpandedStyle'):
                        toggleButton.menuExpandedStyle = ""

                # Assign the new target menu to the button
                toggleButton.targetMenu = self

                # Set the new target button
                self._toggleButton = toggleButton

                # Activate the menu functionality for the button
                self.activateMenuButton(self._toggleButton)
            else:
                print(f"Button with name '{buttonName}' not found.")

        if self._toggleButton:
            if "iconWhenMenuIsCollapsed" in values and len(str(values["iconWhenMenuIsCollapsed"])) > 0:
                self._toggleButton.menuCollapsedIcon = str(values["iconWhenMenuIsCollapsed"])

            if "iconWhenMenuIsExpanded" in values and len(str(values["iconWhenMenuIsExpanded"])) > 0:
                self._toggleButton.menuExpandedIcon = str(values["iconWhenMenuIsExpanded"])

            if "styleWhenMenuIsCollapsed" in values and len(str(values["iconWhenMenuIsExpanded"])) > 0:
                self._toggleButton.menuCollapsedStyle = str(values["styleWhenMenuIsCollapsed"])

            if "styleWhenMenuIsExpanded" in values and len(str(values["styleWhenMenuIsExpanded"])) > 0:
                self._toggleButton.menuExpandedStyle = str(values["styleWhenMenuIsExpanded"])

        self.applyButtonStyle()

    def getButtonByName(self, buttonName):
        # First, try to find the button within the current widget or window
        toggleButton = self.findChild(QPushButton, buttonName)
        
        # If not found, recursively search in parent widgets
        parent = self.parent()
        while toggleButton is None and parent is not None:
            toggleButton = parent.findChild(QPushButton, buttonName)
            parent = parent.parent()  # Move up to the next parent
        
        # Return the found button or None if not found
        return toggleButton

    # Slide menu function
    def slideMenu(self):
        # self.refresh()
        if self._collapsed:
            self.expandMenu()
        else:
            self.collapseMenu()

    def expandMenu(self):
        self._collapsed = True
        self._expanded = False

        self.animateMenu()

        self._collapsed = False
        self._expanded = True

        self.applyButtonStyle()

    def collapseMenu(self):
        self._collapsed = False
        self._expanded = True

        self.animateMenu()

        self._collapsed = True
        self._expanded = False

        self.applyButtonStyle()

    def emitStatusSignal(self):
        if self._expanded:
            self.onExpanded.emit()

        elif self._collapsed:
            self.onCollapsed.emit() 
                
        # if not self.isExpanded() and not self.isCollapsed():
        #     self.animateDefaultSize()

    
    def applyWidgetStyle(self):
        if self.isExpanded() and len(str(self._expandedStyle)) > 0:

            self.setStyleSheet(str(self._expandedStyle))

        if self.isCollapsed() and len(str(self._collapsedStyle)) > 0:
                self.setStyleSheet(str(self._collapsedStyle))

    def applyButtonStyle(self):
        if hasattr(self, "_toggleButton") and self._toggleButton is not None:
            self._toggleButton.menuCollapsedIcon = get_icon_path(self._toggleButton.menuCollapsedIcon)
            self._toggleButton.menuExpandedIcon = get_icon_path(self._toggleButton.menuExpandedIcon)

            if self._collapsed:
                if len(self._toggleButton.menuCollapsedIcon) > 0:
                        # self._toggleButton.setIcon(QtGui.QIcon(self._toggleButton.menuCollapsedIcon))
                        self._toggleButton.setNewIcon(self._toggleButton.menuCollapsedIcon)

                if len(str(self._toggleButton.menuCollapsedStyle)) > 0:
                    self._toggleButton.setStyleSheet(self._toggleButton.menuCollapsedStyle)
            else:
                if len(str(self._toggleButton.menuExpandedIcon)) > 0:
                        # self._toggleButton.setIcon(QtGui.QIcon(self._toggleButton.menuExpandedIcon))
                        self._toggleButton.setNewIcon(self._toggleButton.menuExpandedIcon)

                if len(str(self._toggleButton.menuExpandedStyle)) > 0:
                    self._toggleButton.setStyleSheet(self._toggleButton.menuExpandedStyle)

            self._toggleButton.update()

    def animateMenu(self):
        self.setMinimumSize(QSize(0, 0))
        startHeight = self.height()
        startWidth = self.width()

        # Create a parallel animation group
        self.animation_group = QParallelAnimationGroup(self)

        minWidth, maxWidth = self.determineWith()
        minHeight, maxHeight = self.determineHeight()
        
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

        return int(width), int(width)

    def calculateEndHeight(self, height):       
        if height == "parent":
            return 0, self.parent().height()
        
        return int(height), int(height)

    def adjustMaximumSize(self, property_name):
        if self._expandedWidth == "parent":
                self.setMaximumWidth(16777215)  # Reset to max after expanding

        if self._expandedHeight == "parent":
            self.setMaximumHeight(16777215)  # Reset to max after expanding

    def refresh(self):
        if self.isExpanded() and not self.isCollapsed():
            self._collapsed = False
            self._expanded = True
        else:
            self._collapsed = True
            self._expanded = False

        self.applyWidgetStyle()
        if hasattr(self, "_toggleButton"):
            self.applyButtonStyle()

    def isExpanded(self):
        """
        Determines if the widget is in an expanded state by comparing its
        current width and height to the expanded dimensions.
        """
        if self.width() >= self.getExpandedWidth() and self._expandedWidth != "parent": 
            return True
        elif self.height() >= self.getExpandedHeight() and self._expandedHeight != "parent":
            return True
        
        return False

    def isCollapsed(self):
        """
        Determines if the widget is in a collapsed state by comparing its
        current width and height to the collapsed dimensions.
        """
        return (self.width() <= self.getCollapsedWidth() and
                self.height() <= self.getCollapsedHeight())


    def getDefaultWidth(self):
        if isinstance(self._defaultWidth, int):
            return self._defaultWidth
        if self._defaultWidth == "parent":
            parent = self.parentWidget()
            if parent:
                margins = parent.contentsMargins()
                return parent.sizeHint().width() - (margins.left() + margins.right())
        return 0  # Default return if no valid width is found

    def getDefaultHeight(self):
        if isinstance(self._defaultHeight, int):
            return self._defaultHeight
  
        if self._defaultHeight == "parent":
            parent = self.parentWidget()
            if parent:
                margins = parent.contentsMargins()
                return parent.sizeHint().height() - (margins.top() + margins.bottom())
        return 0  # Default return if no valid height is found

    def getCollapsedWidth(self):
        if isinstance(self._collapsedWidth, int):
            return self._collapsedWidth
        if self._collapsedWidth == "parent":
            parent = self.parentWidget()
            if parent:
                margins = parent.contentsMargins()
                return parent.sizeHint().width() - (margins.left() + margins.right())
        return 0  # Default return if no valid width is found

    def getCollapsedHeight(self):
        if isinstance(self._collapsedHeight, int):
            return self._collapsedHeight
        if self._collapsedHeight == "parent":
            parent = self.parentWidget()
            if parent:
                margins = parent.contentsMargins()
                return parent.sizeHint().height() - (margins.top() + margins.bottom())
        return 0  # Default return if no valid height is found

    def getExpandedWidth(self):
        if isinstance(self._expandedWidth, int):
            return self._expandedWidth

        if self._expandedWidth == "parent":
            parent = self.parentWidget()
            if parent:
                margins = parent.contentsMargins()
                return parent.sizeHint().width() - (margins.left() + margins.right())
        return 0  # Default return if no valid width is found

    def getExpandedHeight(self):
        if isinstance(self._expandedHeight, int):
            return self._expandedHeight
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
        self.adjustSize()
        self.setMinSize()

        self.refresh()

        self.animateDefaultSize()

    def paintEvent(self, event: QPaintEvent):
        opt = QStyleOption()
        opt.initFrom(self)
        painter = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, painter, self)
        
        # self.refresh()
        self.floatMenu()

    def eventFilter(self, obj, event: QEvent):
        if event.type() == QEvent.MouseButtonPress:
            if self._autoHide:
                local_pos = self.mapFromGlobal(event.globalPos())
                if not self.rect().contains(local_pos):
                    self.collapseMenu()

        # Handle Resize, Move, and other events
        elif event.type() == QEvent.Resize:
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
    
    #######################################################################