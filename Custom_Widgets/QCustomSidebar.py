########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/spinnTv
# WEBSITE: spinncode.com
########################################################################
from qtpy.QtCore import QSize, Property, QEasingCurve, QCoreApplication
from qtpy.QtGui import QColor, QPaintEvent, QPainter
from qtpy.QtWidgets import QApplication, QStyleOption, QStyle

import os

from Custom_Widgets.QCustomSlideMenu import QCustomSlideMenu
from Custom_Widgets.JSonStyles import updateJson
from Custom_Widgets.Log import *
from Custom_Widgets.Utils import replace_url_prefix, is_in_designer, get_icon_path

class QCustomSidebar(QCustomSlideMenu):
    script_dir = os.path.dirname(os.path.realpath(__file__))
    WIDGET_ICON = os.path.join(script_dir, "components/icons/sidebar.png")
    WIDGET_TOOLTIP = "A custom collapsible sidebar widget"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomSidebar' name='customSidebar'>
        </widget>
    </ui>
    """
    WIDGET_MODULE = "Custom_Widgets.QCustomSidebar"

    def __init__(self, parent=None):
        super().__init__(parent)
        # Style properties
        self._containerStyleCollapsed = self._collapsedStyle
        self._containerStyleExpanded = self._expandedStyle

        # Shadow properties
        self._shadowColor = QColor(0, 0, 0, 0)
        self._shadowBlurRadius = 0
        self._shadowXOffset = 0
        self._shadowYOffset = 0

        self._jsonFilePath = "json-styles/style.json"

        self.onCollapsed.connect(self.updateProperties)
        self.onExpanded.connect(self.updateProperties)

        self.onCollapsing.connect(lambda: self.updateProperties(state="collapsing"))
        self.onExpanding.connect(lambda: self.updateProperties(state="expanding"))

        self.updateProperties()


    def updateProperties(self, state=None):
        if state is None:
            if self.isExpanded() and not self.isCollapsed():
                self.setProperty("state", "expanded")
            else:
                self.setProperty("state", "collapsed")

        elif state == "collapsing":
            self.setProperty("state", "collapsing")

        elif state == "expanding":
            self.setProperty("state", "expanding")

        self.style().unpolish(self) 
        self.style().polish(self)

    def convert_to_int(self, s):
        try:
            # Try converting the string to an integer
            return int(s)
        except ValueError:
            # If conversion fails, return the original string
            return s

    # Properties for default size (separate width and height)
    @Property(str)
    def defaultWidth(self):
        return str(self._defaultWidth)

    @defaultWidth.setter
    def defaultWidth(self, width):
        self._defaultWidth = self.convert_to_int(width)
        self.setMinSize()
        self.customizeQCustomSlideMenu(update=False, defaultWidth=self._defaultWidth)

    @Property(str)
    def defaultHeight(self):
        return str(self._defaultHeight)

    @defaultHeight.setter
    def defaultHeight(self, height):
        self._defaultHeight = self.convert_to_int(height)
        self.setMinSize()
        self.customizeQCustomSlideMenu(update=False, defaultHeight=self._defaultHeight)


    # Properties for collapsed size (separate width and height)
    @Property(str)
    def collapsedWidth(self):
        return str(self._collapsedWidth)

    @collapsedWidth.setter
    def collapsedWidth(self, width):
        self._collapsedWidth = self.convert_to_int(width)
        self.customizeQCustomSlideMenu(update=False, collapsedWidth=self._collapsedWidth, collapsedHeight=self._collapsedHeight)

    @Property(str)
    def collapsedHeight(self):
        return str(self._collapsedHeight)

    @collapsedHeight.setter
    def collapsedHeight(self, height):
        self._collapsedHeight = self.convert_to_int(height)
        self.customizeQCustomSlideMenu(update=False, collapsedWidth=self._collapsedWidth, collapsedHeight=self._collapsedHeight)

    # Properties for expanded size (separate width and height)
    @Property(str)
    def expandedWidth(self):
        return str(self._expandedWidth)

    @expandedWidth.setter
    def expandedWidth(self, width):
        self._expandedWidth = self.convert_to_int(width)
        self.customizeQCustomSlideMenu(update=False, expandedWidth=self._expandedWidth, expandedHeight=self._expandedHeight)
        

    @Property(str)
    def expandedHeight(self):
        return str(self._expandedHeight)

    @expandedHeight.setter
    def expandedHeight(self, height):
        self._expandedHeight = self.convert_to_int(height)
        self.customizeQCustomSlideMenu(update=False, expandedWidth=self._expandedWidth, expandedHeight=self._expandedHeight)
        

    # Toggle button properties
    @Property(str)
    def toggleButtonName(self):
        return self._toggleButtonName
    
    @toggleButtonName.setter
    def toggleButtonName(self, name):
        self._toggleButtonName = name
        self.customizeQCustomSlideMenu(update=False, toggleButtonName=name)
        

    @Property(str)
    def iconCollapsed(self):
        return self._iconCollapsed
    
    @iconCollapsed.setter
    def iconCollapsed(self, icon):
        self._iconCollapsed = icon
        self.customizeQCustomSlideMenu(update=False, iconWhenMenuIsCollapsed=icon)
        
    @Property(str)
    def iconExpanded(self):
        return self._iconExpanded
    
    @iconExpanded.setter
    def iconExpanded(self, icon):
        self._iconExpanded = icon
        self.customizeQCustomSlideMenu(update=False, iconWhenMenuIsExpanded=icon)
        
    # Animation properties
    @Property(int)
    def animationDuration(self):
        return self._animationDuration
    
    @animationDuration.setter
    def animationDuration(self, duration):
        self._animationDuration = duration
        self.customizeQCustomSlideMenu(update=False, animationDuration=duration)
        
    @Property(QEasingCurve)
    def animationEasingCurve(self):
        return self._animationEasingCurve
    
    @animationEasingCurve.setter
    def animationEasingCurve(self, curve):
        self._animationEasingCurve = curve
        self.customizeQCustomSlideMenu(update=False, animationEasingCurve=curve)
        
    # Style properties
    @Property(str)
    def containerStyleCollapsed(self):
        return self._containerStyleCollapsed
    
    @containerStyleCollapsed.setter
    def containerStyleCollapsed(self, style):
        self._containerStyleCollapsed = style
        self.customizeQCustomSlideMenu(update=False, collapsedStyle=style)
        
    @Property(str)
    def containerStyleExpanded(self):
        return self._containerStyleExpanded
    
    @containerStyleExpanded.setter
    def containerStyleExpanded(self, style):
        self._containerStyleExpanded = style
        self.customizeQCustomSlideMenu(update=False, expandedStyle=style)
        

    # Floating menu and auto-hide
    @Property(bool)
    def float(self):
        return self._float
    
    @float.setter
    def float(self, enabled):
        self._float = enabled
        self.customizeQCustomSlideMenu(update=False, floatMenu=enabled)
        

    @Property(str)
    def floatPosition(self):
        return self._floatPosition
    
    @floatPosition.setter
    def floatPosition(self, position):
        self._floatPosition = position
        self.customizeQCustomSlideMenu(update=False, position=position)
      

    @Property(bool)
    def autoHide(self):
        return self._autoHide
    
    @autoHide.setter
    def autoHide(self, enabled):
        self._autoHide = enabled
        self.customizeQCustomSlideMenu(update=False, autoHide=enabled)

    # Shadow effect properties
    @Property(QColor)
    def shadowColor(self):
        return self._shadowColor
    
    @shadowColor.setter
    def shadowColor(self, color):
        self._shadowColor = color
        self.customizeQCustomSlideMenu(update=False, shadowColor=color.name())
 
    @Property(int)
    def shadowBlurRadius(self):
        return self._shadowBlurRadius
    
    @shadowBlurRadius.setter
    def shadowBlurRadius(self, radius):
        self._shadowBlurRadius = radius
        self.customizeQCustomSlideMenu(update=False, shadowBlurRadius=radius)

    @Property(int)
    def shadowXOffset(self):
        return self._shadowXOffset
    
    @shadowXOffset.setter
    def shadowXOffset(self, offset):
        self._shadowXOffset = offset
        self.customizeQCustomSlideMenu(update=False, shadowXOffset=offset)


    @Property(int)
    def shadowYOffset(self):
        return self._shadowYOffset
    
    @shadowYOffset.setter
    def shadowYOffset(self, offset):
        self._shadowYOffset = offset
        self.customizeQCustomSlideMenu(update=False, shadowYOffset=offset)

    # Margin Properties
    @Property(int)
    def marginTop(self):
        return self._marginTop

    @marginTop.setter
    def marginTop(self, margin):
        self._marginTop = margin
        self.customizeQCustomSlideMenu(update=False, marginTop=margin)

    @Property(int)
    def marginRight(self):
        return self._marginRight

    @marginRight.setter
    def marginRight(self, margin):
        self._marginRight = margin
        self.customizeQCustomSlideMenu(update=False, marginRight=margin)

    @Property(int)
    def marginBottom(self):
        return self._marginBottom

    @marginBottom.setter
    def marginBottom(self, margin):
        self._marginBottom = margin
        self.customizeQCustomSlideMenu(update=False, marginBottom=margin)

    @Property(int)
    def marginLeft(self):
        return self._marginLeft

    @marginLeft.setter
    def marginLeft(self, margin):
        self._marginLeft = margin
        self.customizeQCustomSlideMenu(update=False, marginLeft=margin)

    def paintEvent(self, e):
        """Handle the paint event to customize the appearance of the widget."""
        super().paintEvent(e)
        opt = QStyleOption()
        opt.initFrom(self)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, painter, self)




