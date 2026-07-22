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
from Custom_Widgets.QPropertyAnimation import returnAnimationEasingCurve, easingCurveToInt

class QCustomSidebar(QCustomSlideMenu):
    script_dir = os.path.dirname(os.path.realpath(__file__))
    WIDGET_ICON = os.path.join(script_dir, "components/icons/view_sidebar.png")
    WIDGET_TOOLTIP = "A custom collapsible sidebar widget"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomSidebar' name='customSidebar'>
        </widget>
    </ui>
    """
    WIDGET_MODULE = "Custom_Widgets.QCustomSidebar"

    # Rich editors for the Designer "Custom Properties" dock (see
    # DesignerTools.CustomPropertiesDock).
    DESIGNER_CUSTOM_PROPS = [
        {"name": "defaultWidth", "kind": "int", "group": "Size"},
        {"name": "defaultHeight", "kind": "int", "group": "Size"},
        {"name": "collapsedWidth", "kind": "int", "group": "Size"},
        {"name": "collapsedHeight", "kind": "int", "group": "Size"},
        {"name": "expandedWidth", "kind": "int", "group": "Size"},
        {"name": "expandedHeight", "kind": "int", "group": "Size"},
        {"name": "toggleButtonName", "kind": "widget-ref",
         "types": ("QPushButton", "QToolButton"), "group": "Toggle"},
        {"name": "iconCollapsed", "kind": "file",
         "filter": "Images (*.svg *.png *.ico *.jpg);;All files (*)",
         "group": "Toggle"},
        {"name": "iconExpanded", "kind": "file",
         "filter": "Images (*.svg *.png *.ico *.jpg);;All files (*)",
         "group": "Toggle"},
        {"name": "animationDuration", "kind": "int", "group": "Animation"},
        {"name": "animationEasingCurve", "kind": "easing", "group": "Animation"},
        {"name": "shadowColor", "kind": "color", "group": "Shadow"},
        {"name": "shadowBlurRadius", "kind": "int", "group": "Shadow"},
        {"name": "shadowXOffset", "kind": "int", "group": "Shadow"},
        {"name": "shadowYOffset", "kind": "int", "group": "Shadow"},
    ]

    def __init__(self, parent=None):
        super().__init__(parent)
        # Shadow properties
        self._shadowColor = QColor(0, 0, 0, 0)
        self._shadowBlurRadius = 0
        self._shadowXOffset = 0
        self._shadowYOffset = 0

        # Add these default values:
        
        # Size properties - default values
        self._defaultWidth = 300
        self._defaultHeight = "parent"
        self._collapsedWidth = 50
        self._collapsedHeight = "parent"
        self._expandedWidth = 300
        self._expandedHeight = "parent"
        
        # Toggle button properties - default values
        self._toggleButtonName = ""
        self._iconCollapsed = ""
        self._iconExpanded = ""
        
        # Animation properties - default values
        self._animationDuration = 500  # milliseconds
        self._animationEasingCurve = "OutQuad"
        
        # JSON file path
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

    # Size properties are typed as int for Qt Designer. A value of -1 means
    # "match the parent's size" (stored internally as the "parent" sentinel
    # the slide menu understands). Legacy string values ("parent"/"250")
    # are still accepted so older .ui files keep loading.
    MATCH_PARENT = -1

    def _sizeToInt(self, value):
        """internal storage (int or 'parent') -> public int (-1 == parent)"""
        if value == "parent":
            return self.MATCH_PARENT
        return self.convert_to_int(value)

    def _intToSize(self, value):
        """public value (int/-1 or legacy string) -> internal storage"""
        if isinstance(value, str) and value.strip().lower() == "parent":
            return "parent"
        value = self.convert_to_int(value)
        if value == self.MATCH_PARENT:
            return "parent"
        return value

    # Properties for default size (separate width and height)
    @Property(int)
    def defaultWidth(self):
        return self._sizeToInt(self._defaultWidth)

    @defaultWidth.setter
    def defaultWidth(self, width):
        self._defaultWidth = self._intToSize(width)
        self.setMinSize()
        self.customizeQCustomSlideMenu(update=False, defaultWidth=self._defaultWidth)

    @Property(int)
    def defaultHeight(self):
        return self._sizeToInt(self._defaultHeight)

    @defaultHeight.setter
    def defaultHeight(self, height):
        self._defaultHeight = self._intToSize(height)
        self.setMinSize()
        self.customizeQCustomSlideMenu(update=False, defaultHeight=self._defaultHeight)


    # Properties for collapsed size (separate width and height)
    @Property(int)
    def collapsedWidth(self):
        return self._sizeToInt(self._collapsedWidth)

    @collapsedWidth.setter
    def collapsedWidth(self, width):
        self._collapsedWidth = self._intToSize(width)
        self.customizeQCustomSlideMenu(update=False, collapsedWidth=self._collapsedWidth, collapsedHeight=self._collapsedHeight)

    @Property(int)
    def collapsedHeight(self):
        return self._sizeToInt(self._collapsedHeight)

    @collapsedHeight.setter
    def collapsedHeight(self, height):
        self._collapsedHeight = self._intToSize(height)
        self.customizeQCustomSlideMenu(update=False, collapsedWidth=self._collapsedWidth, collapsedHeight=self._collapsedHeight)

    # Properties for expanded size (separate width and height)
    @Property(int)
    def expandedWidth(self):
        return self._sizeToInt(self._expandedWidth)

    @expandedWidth.setter
    def expandedWidth(self, width):
        self._expandedWidth = self._intToSize(width)
        self.customizeQCustomSlideMenu(update=False, expandedWidth=self._expandedWidth, expandedHeight=self._expandedHeight)


    @Property(int)
    def expandedHeight(self):
        return self._sizeToInt(self._expandedHeight)

    @expandedHeight.setter
    def expandedHeight(self, height):
        self._expandedHeight = self._intToSize(height)
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
        
    @Property(int)
    def animationEasingCurve(self):
        """Easing as an int (a QEasingCurve.Type value). Developers can use
        QEasingCurve.OutQuad etc.; Designer shows a spin box."""
        return easingCurveToInt(self._animationEasingCurve)

    @animationEasingCurve.setter
    def animationEasingCurve(self, curve):
        # Accept int / QEasingCurve.Type / legacy name string.
        self._animationEasingCurve = curve
        _curve = returnAnimationEasingCurve(curve)
        self.customizeQCustomSlideMenu(update=False, animationEasingCurve=_curve)
        
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

    def showEvent(self, event):
        super().showEvent(event)
        if is_in_designer(self):
            self.expandMenu()
            self.customizeQCustomSlideMenu(update=False, toggleButtonName=self.toggleButtonName)

    def paintEvent(self, e):
        """Handle the paint event to customize the appearance of the widget."""
        super().paintEvent(e)
        opt = QStyleOption()
        opt.initFrom(self)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, painter, self)




