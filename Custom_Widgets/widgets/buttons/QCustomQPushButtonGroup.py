########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/@SpinnTV
# WEBSITE: customwidgets.org
########################################################################

########################################################################
## IMPORTS
########################################################################

########################################################################
## MODULE UPDATED TO USE QT.PY
########################################################################
from qtpy.QtWidgets import QPushButton

########################################################################
## GROUP BUTTONS
########################################################################
class QCustomQPushButtonGroup(QPushButton):
    # Qt Designer contract. WIDGET_MODULE is the FLAT public path --
    # Custom_Widgets.QCustomQPushButtonGroup is what .ui files carry in <header>, not the
    # subpackage this file now lives in.
    WIDGET_MODULE = "Custom_Widgets.QCustomQPushButtonGroup"
    WIDGET_TOOLTIP = "A button group with active/inactive state management"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomQPushButtonGroup' name='qCustomQPushButtonGroup'>
            <property name='geometry'><rect><x>0</x><y>0</y><width>320</width><height>40</height></rect></property>
        </widget>
    </ui>
    """
    def __init__(self, parent=None):
        super().__init__(parent)

        self.group = None

    ########################################################################
    ## BUTTON GROUP
    ########################################################################
    def getButtonGroup(self):
        return self.group
    def getButtonGroupActiveStyle(self):
        group = self.getButtonGroup()
        if group == None:
            return None
        return getattr(self.groupParent, "group_active_"+str(group))
    def getButtonGroupNotActiveStyle(self):
        group = self.getButtonGroup()
        if group == None:
            return None
        return getattr(self.groupParent, "group_not_active_"+str(group))
    def getButtonGroupButtons(self):
        group = self.getButtonGroup()
        if group == None:
            return None
        return getattr(self.groupParent, "group_btns_"+str(group))

    def setButtonGroupActiveStyle(self, style):
        group = self.getButtonGroup()
        if group == None:
            raise Exception("Unknown button group. The button does not belong to any group")
        setattr(self.groupParent, "group_active_"+str(group), style)
        groupBtns = self.getButtonGroupButtons()
        for x in groupBtns:
            if x.active:
                x.setStyleSheet(style)

    def setButtonGroupNotActiveStyle(self, style):
        group = self.getButtonGroup()
        if group == None:
            raise Exception("Unknown button group. The button does not belong to any group")
        setattr(self.groupParent, "group_not_active_"+str(group), style)