# Custom Widgets Registration for Qt Designer
# Author: Khamisi Kibet

# Dump a native + Python traceback to stderr on a fatal signal (SIGSEGV/SIGABRT)
# so custom-widget crashes inside the Designer process are diagnosable instead
# of silently returning -11.
import os as _os
try:
    import faulthandler as _faulthandler
    _fh_path = _os.path.join(
        _os.path.expanduser("~/.local/share/customwidgets/logs"),
        "designer_faulthandler.log")
    _os.makedirs(_os.path.dirname(_fh_path), exist_ok=True)
    _fh_file = open(_fh_path, "a", buffering=1)
    _faulthandler.enable(file=_fh_file, all_threads=True)
except Exception:
    pass

# Import custom logging module
from Custom_Widgets.Log import *

# Ensure the logger is set up
setupLogger(designer = True)

import PySide6.QtDesigner as QtDesigner

logInfo("Registering Custom Widgets")

# Capture the form editor core (needed to open forms into this Designer
# instance) - must be registered before/with the other custom widgets.
try:
    from Custom_Widgets.DesignerBridge import registerCoreCapture, addCoreListener
    registerCoreCapture()
    # Present QCustomQMainWindow.appTheme as a theme-name dropdown in the
    # property editor once Designer hands us the form-editor core.
    from Custom_Widgets.DesignerExtensions import registerDesignerExtensions
    addCoreListener(registerDesignerExtensions)
except Exception as e:
    logException(e, message="Error registering Designer core capture")

from Custom_Widgets.QCustomQMainWindow import QCustomQMainWindow

# Registering QCustomQMainWindow with error handling
try:
    logInfo("Registering QCustomQMainWindow")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomQMainWindow, module=QCustomQMainWindow.WIDGET_MODULE,
        tool_tip=QCustomQMainWindow.WIDGET_TOOLTIP, 
        xml=QCustomQMainWindow.WIDGET_DOM_XML,
        icon=QCustomQMainWindow.WIDGET_ICON, container=True, group="Main Window"
    )
except Exception as e:
    logException(e, message="Error registering QCustomQMainWindow")


from Custom_Widgets.QAvatarWidget import QAvatarWidget 

# Registering QAvatarWidget with error handling
try:
    logInfo("Registering QAvatarWidget")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QAvatarWidget, module=QAvatarWidget.WIDGET_MODULE,
        tool_tip=QAvatarWidget.WIDGET_TOOLTIP, 
        xml=QAvatarWidget.WIDGET_DOM_XML,
        icon=QAvatarWidget.WIDGET_ICON
    )
except Exception as e:
    logException(e, message="Error registering QAvatarWidget")


from Custom_Widgets.QBadgeWidget import QBadgeWidget 

# Registering QBadgeWidget with error handling
try:
    logInfo("Registering QBadgeWidget")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QBadgeWidget, module=QBadgeWidget.WIDGET_MODULE,
        tool_tip=QBadgeWidget.WIDGET_TOOLTIP, 
        xml=QBadgeWidget.WIDGET_DOM_XML,
        icon=QBadgeWidget.WIDGET_ICON
    )
except Exception as e:
    logException(e, message="Error registering QBadgeWidget")


from Custom_Widgets.AnalogGaugeWidget import AnalogGaugeWidget 

# Registering AnalogGaugeWidget with error handling
try:
    logInfo("Registering AnalogGaugeWidget")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        AnalogGaugeWidget, module=AnalogGaugeWidget.WIDGET_MODULE,
        tool_tip=AnalogGaugeWidget.WIDGET_TOOLTIP, 
        xml=AnalogGaugeWidget.WIDGET_DOM_XML,
        icon=AnalogGaugeWidget.WIDGET_ICON
    )
except Exception as e:
    logException(e, message="Error registering AnalogGaugeWidget")


from Custom_Widgets.QCustomDataTable import QCustomDataTable

# Registering QCustomDataTable with error handling
try:
    logInfo("Registering QCustomDataTable")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomDataTable, module=QCustomDataTable.WIDGET_MODULE,
        tool_tip=QCustomDataTable.WIDGET_TOOLTIP,
        xml=QCustomDataTable.WIDGET_DOM_XML,
        icon=QCustomDataTable.WIDGET_ICON, group="Item Views"
    )
except Exception as e:
    logException(e, message="Error registering QCustomDataTable")


from Custom_Widgets.QCustomComboBox import QCustomComboBox

# Registering QCustomComboBox with error handling
try:
    logInfo("Registering QCustomComboBox")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomComboBox, module=QCustomComboBox.WIDGET_MODULE,
        tool_tip=QCustomComboBox.WIDGET_TOOLTIP,
        xml=QCustomComboBox.WIDGET_DOM_XML,
        icon=QCustomComboBox.WIDGET_ICON, group="Input Widgets"
    )
except Exception as e:
    logException(e, message="Error registering QCustomComboBox")


from Custom_Widgets.QCustomDateTimeEdit import (QCustomDateEdit, QCustomTimeEdit,
                                                QCustomDateRangeEdit)

for _dtw, _grp in ((QCustomDateEdit, "Input Widgets"),
                   (QCustomTimeEdit, "Input Widgets"),
                   (QCustomDateRangeEdit, "Input Widgets")):
    try:
        logInfo("Registering %s" % _dtw.__name__)
        QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
            _dtw, module=_dtw.WIDGET_MODULE, tool_tip=_dtw.WIDGET_TOOLTIP,
            xml=_dtw.WIDGET_DOM_XML, icon=_dtw.WIDGET_ICON, group=_grp)
    except Exception as e:
        logException(e, message="Error registering %s" % _dtw.__name__)


from Custom_Widgets.QCustomThemeList import QCustomThemeList

# Registering QCustomThemeList with error handling
try:
    logInfo("Registering QCustomThemeList")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomThemeList, module=QCustomThemeList.WIDGET_MODULE,
        tool_tip=QCustomThemeList.WIDGET_TOOLTIP, 
        xml=QCustomThemeList.WIDGET_DOM_XML,
        icon=QCustomThemeList.WIDGET_ICON
    )
except Exception as e:
    logException(e, message="Error registering QCustomThemeList")

from Custom_Widgets.QCustomThemeDarkLightToggle import QCustomThemeDarkLightToggle 

# Registering QCustomThemeDarkLightToggle with error handling
try:
    logInfo("Registering QCustomThemeDarkLightToggle")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomThemeDarkLightToggle, module=QCustomThemeDarkLightToggle.WIDGET_MODULE,
        tool_tip=QCustomThemeDarkLightToggle.WIDGET_TOOLTIP, 
        xml=QCustomThemeDarkLightToggle.WIDGET_DOM_XML,
        icon=QCustomThemeDarkLightToggle.WIDGET_ICON
    )
except Exception as e:
    logException(e, message="Error registering QCustomThemeDarkLightToggle")


from Custom_Widgets.QCustomCheckBox import QCustomCheckBox 

# Registering QCustomCheckBox with error handling
try:
    logInfo("Registering QCustomCheckBox")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomCheckBox, module=QCustomCheckBox.WIDGET_MODULE,
        tool_tip=QCustomCheckBox.WIDGET_TOOLTIP, 
        xml=QCustomCheckBox.WIDGET_DOM_XML,
        icon=QCustomCheckBox.WIDGET_ICON
    )
except Exception as e:
    logException(e, message="Error registering QCustomCheckBox")


from Custom_Widgets.QCustomSidebar import QCustomSidebar 

# Registering QCustomSidebar with error handling
try:
    logInfo("Registering QCustomSidebar")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomSidebar, module=QCustomSidebar.WIDGET_MODULE,
        tool_tip=QCustomSidebar.WIDGET_TOOLTIP, 
        xml=QCustomSidebar.WIDGET_DOM_XML,
        icon=QCustomSidebar.WIDGET_ICON, container=True, group="Sidebar"
    )
except Exception as e:
    logException(e, message="Error registering QCustomSidebar")


# ADD HAMBURGER MENU WIDGETS HERE - RIGHT AFTER SIDEBAR REGISTRATION

from Custom_Widgets.QCustomHamburgerMenu import QCustomHamburgerMenu

# Registering QCustomHamburgerMenu with error handling
try:
    logInfo("Registering QCustomHamburgerMenu")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomHamburgerMenu, module=QCustomHamburgerMenu.WIDGET_MODULE,
        tool_tip=QCustomHamburgerMenu.WIDGET_TOOLTIP, 
        xml=QCustomHamburgerMenu.WIDGET_DOM_XML,
        icon=QCustomHamburgerMenu.WIDGET_ICON, container=True, group="Hamburger Menu"
    )
except Exception as e:
    logException(e, message="Error registering QCustomHamburgerMenu")


from Custom_Widgets.QCustomHorizontalSeparator import QCustomHorizontalSeparator 

# Registering QCustomHorizontalSeparator with error handling
try:
    logInfo("Registering QCustomHorizontalSeparator")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomHorizontalSeparator, module=QCustomHorizontalSeparator.WIDGET_MODULE,
        tool_tip=QCustomHorizontalSeparator.WIDGET_TOOLTIP, 
        xml=QCustomHorizontalSeparator.WIDGET_DOM_XML,
        icon=QCustomHorizontalSeparator.WIDGET_ICON, container=False, group="Sidebar"
    )
except Exception as e:
    logException(e, message="Error registering QCustomHorizontalSeparator")

from Custom_Widgets.QCustomVerticalSeparator import QCustomVerticalSeparator 

# Registering QCustomVerticalSeparator with error handling
try:
    logInfo("Registering QCustomVerticalSeparator")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomVerticalSeparator, module=QCustomVerticalSeparator.WIDGET_MODULE,
        tool_tip=QCustomVerticalSeparator.WIDGET_TOOLTIP, 
        xml=QCustomVerticalSeparator.WIDGET_DOM_XML,
        icon=QCustomVerticalSeparator.WIDGET_ICON, container=False, group="Sidebar"
    )
except Exception as e:
    logException(e, message="Error registering QCustomVerticalSeparator")


from Custom_Widgets.QCustomSidebarLabel import QCustomSidebarLabel 

# Registering QCustomSidebarLabel with error handling
try:
    logInfo("Registering QCustomSidebarLabel")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomSidebarLabel, module=QCustomSidebarLabel.WIDGET_MODULE,
        tool_tip=QCustomSidebarLabel.WIDGET_TOOLTIP, 
        xml=QCustomSidebarLabel.WIDGET_DOM_XML,
        icon=QCustomSidebarLabel.WIDGET_ICON, group="Sidebar"
    )
except Exception as e:
    logException(e, message="Error registering QCustomSidebarLabel")


from Custom_Widgets.QCustomSidebarButton import QCustomSidebarButton 

# Registering QCustomSidebarButton with error handling
try:
    logInfo("Registering QCustomSidebarButton")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomSidebarButton, module=QCustomSidebarButton.WIDGET_MODULE,
        tool_tip=QCustomSidebarButton.WIDGET_TOOLTIP, 
        xml=QCustomSidebarButton.WIDGET_DOM_XML,
        icon=QCustomSidebarButton.WIDGET_ICON, group="Sidebar"
    )
except Exception as e:
    logException(e, message="Error registering QCustomSidebarButton")


from Custom_Widgets.QCustomSidebarContainer import QCustomSidebarContainer

# Registering QCustomSidebarContainer with error handling
try:
    logInfo("Registering QCustomSidebarContainer")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomSidebarContainer, module=QCustomSidebarContainer.WIDGET_MODULE,
        tool_tip=QCustomSidebarContainer.WIDGET_TOOLTIP, 
        xml=QCustomSidebarContainer.WIDGET_DOM_XML,
        icon=QCustomSidebarContainer.WIDGET_ICON, container=True, group="Sidebar"
    )
except Exception as e:
    logException(e, message="Error registering QCustomSidebarContainer")

from Custom_Widgets.QCustomProgressBars import QCustomRoundProgressBar 

# Registering QCustomRoundProgressBar with error handling
try:
    logInfo("Registering QCustomRoundProgressBar")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomRoundProgressBar, module=QCustomRoundProgressBar.WIDGET_MODULE,
        tool_tip=QCustomRoundProgressBar.WIDGET_TOOLTIP, 
        xml=QCustomRoundProgressBar.WIDGET_DOM_XML,
        icon=QCustomRoundProgressBar.WIDGET_ICON, group="Progressbars"
    )
except Exception as e:
    logException(e, message="Error registering QCustomRoundProgressBar")

from Custom_Widgets.QCustomComponent import QCustomComponent

# Registering QCustomComponent with error handling
try:
    logInfo("Registering QCustomComponent")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomComponent, module=QCustomComponent.WIDGET_MODULE,
        tool_tip=QCustomComponent.WIDGET_TOOLTIP, 
        xml=QCustomComponent.WIDGET_DOM_XML,
        icon=QCustomComponent.WIDGET_ICON, container=True, group="Component Container"
    )
except Exception as e:
    logException(e, message="Error registering QCustomComponent")

from Custom_Widgets.QCustomComponentContainer import QCustomComponentContainer

# Registering QCustomComponentContainer with error handling
try:
    logInfo("Registering QCustomComponentContainer")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomComponentContainer, module=QCustomComponentContainer.WIDGET_MODULE,
        tool_tip=QCustomComponentContainer.WIDGET_TOOLTIP, 
        xml=QCustomComponentContainer.WIDGET_DOM_XML,
        icon=QCustomComponentContainer.WIDGET_ICON, container=False, group="Component Container"
    )
except Exception as e:
    logException(e, message="Error registering QCustomComponentContainer")

from Custom_Widgets.QCustomQStackedWidget import QCustomQStackedWidget

try:
    logInfo("Registering QCustomQStackedWidget")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomQStackedWidget, module=QCustomQStackedWidget.WIDGET_MODULE,
        tool_tip=QCustomQStackedWidget.WIDGET_TOOLTIP, 
        xml=QCustomQStackedWidget.WIDGET_DOM_XML,
        icon=QCustomQStackedWidget.WIDGET_ICON, container=True
    )
except Exception as e:
    logException(e, message="Error registering QCustomQStackedWidget")

from Custom_Widgets.QCustomLoadingIndicators import QCustomQProgressBar 

# Registering QCustomQProgressBar with error handling
try:
    logInfo("Registering QCustomQProgressBar")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomQProgressBar, module=QCustomQProgressBar.WIDGET_MODULE,
        tool_tip=QCustomQProgressBar.WIDGET_TOOLTIP, 
        xml=QCustomQProgressBar.WIDGET_DOM_XML,
        icon=QCustomQProgressBar.WIDGET_ICON, group="Progressbars"
    )
except Exception as e:
    logException(e, message="Error registering QCustomQProgressBar")

from Custom_Widgets.QCustomQRGenerator import QCustomQRGenerator

# Registering QCustomQRGenerator with error handling
try:
    logInfo("Registering QCustomQRGenerator")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomQRGenerator, module=QCustomQRGenerator.WIDGET_MODULE,
        tool_tip=QCustomQRGenerator.WIDGET_TOOLTIP, 
        xml=QCustomQRGenerator.WIDGET_DOM_XML,
        icon=QCustomQRGenerator.WIDGET_ICON, container=False, group="QR Generator"
    )
except Exception as e:
    logException(e, message="Error registering QCustomQRGenerator")
    
    
try:
    from Custom_Widgets.QCustomCharts import QCustomLineChart
    
    logInfo("Registering QCustomLineChart")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomLineChart, 
        module=QCustomLineChart.WIDGET_MODULE,
        tool_tip=QCustomLineChart.WIDGET_TOOLTIP, 
        xml=QCustomLineChart.WIDGET_DOM_XML,
        icon=QCustomLineChart.WIDGET_ICON, 
        container=False, 
        group="Charts"
    )
    logInfo("QCustomLineChart registered successfully")
    
except ImportError as e:
    logError(f"Failed to import QCustomLineChart: {e}")
except Exception as e:
    logException(e, message="Error registering QCustomLineChart")

try:
    from Custom_Widgets.QCustomCharts import QCustomBarChart
    
    logInfo("Registering QCustomBarChart")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomBarChart, 
        module=QCustomBarChart.WIDGET_MODULE,
        tool_tip=QCustomBarChart.WIDGET_TOOLTIP, 
        xml=QCustomBarChart.WIDGET_DOM_XML,
        icon=QCustomBarChart.WIDGET_ICON, 
        container=False, 
        group="Charts"
    )
    logInfo("QCustomBarChart registered successfully")
    
except ImportError as e:
    logError(f"Failed to import QCustomBarChart: {e}")
except Exception as e:
    logException(e, message="Error registering QCustomBarChart")

try:
    from Custom_Widgets.QCustomCharts import QCustomAreaChart
    
    logInfo("Registering QCustomAreaChart")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomAreaChart, 
        module=QCustomAreaChart.WIDGET_MODULE,
        tool_tip=QCustomAreaChart.WIDGET_TOOLTIP, 
        xml=QCustomAreaChart.WIDGET_DOM_XML,
        icon=QCustomAreaChart.WIDGET_ICON, 
        container=False, 
        group="Charts"
    )
    logInfo("QCustomAreaChart registered successfully")
    
except ImportError as e:
    logError(f"Failed to import QCustomAreaChart: {e}")
except Exception as e:
    logException(e, message="Error registering QCustomAreaChart")

try:
    from Custom_Widgets.QCustomCharts import QCustomPieChart
    
    logInfo("Registering QCustomPieChart")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomPieChart, 
        module=QCustomPieChart.WIDGET_MODULE,
        tool_tip=QCustomPieChart.WIDGET_TOOLTIP, 
        xml=QCustomPieChart.WIDGET_DOM_XML,
        icon=QCustomPieChart.WIDGET_ICON, 
        container=False, 
        group="Charts"
    )
    logInfo("QCustomPieChart registered successfully")
    
except ImportError as e:
    logError(f"Failed to import QCustomPieChart: {e}")
except Exception as e:
    logException(e, message="Error registering QCustomPieChart")

try:
    from Custom_Widgets.QCustomCharts import QCustomVerticalBarSeries

    logInfo("Registering QCustomVerticalBarSeries")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomVerticalBarSeries,
        module=QCustomVerticalBarSeries.WIDGET_MODULE,
        tool_tip=QCustomVerticalBarSeries.WIDGET_TOOLTIP,
        xml=QCustomVerticalBarSeries.WIDGET_DOM_XML,
        icon=QCustomVerticalBarSeries.WIDGET_ICON,
        container=False,
        group="Charts"
    )
except ImportError as e:
    logError(f"Failed to import QCustomVerticalBarSeries: {e}")
except Exception as e:
    logException(e, message="Error registering QCustomVerticalBarSeries")

try:
    from Custom_Widgets.QCustomCharts import QCustomHorizontalBarSeries

    logInfo("Registering QCustomHorizontalBarSeries")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomHorizontalBarSeries,
        module=QCustomHorizontalBarSeries.WIDGET_MODULE,
        tool_tip=QCustomHorizontalBarSeries.WIDGET_TOOLTIP,
        xml=QCustomHorizontalBarSeries.WIDGET_DOM_XML,
        icon=QCustomHorizontalBarSeries.WIDGET_ICON,
        container=False,
        group="Charts"
    )
except ImportError as e:
    logError(f"Failed to import QCustomHorizontalBarSeries: {e}")
except Exception as e:
    logException(e, message="Error registering QCustomHorizontalBarSeries")

# NOTE: QCustomFlowLayout is a QLayout subclass, not a QWidget, so it cannot be
# registered as a Designer custom widget. Register QCustomFlowWidget instead -
# the QWidget container that wraps QCustomFlowLayout.
from Custom_Widgets.QCustomFlowWidget import QCustomFlowWidget

# Registering QCustomFlowWidget with error handling
try:
    logInfo("Registering QCustomFlowWidget")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomFlowWidget,
        module=QCustomFlowWidget.WIDGET_MODULE,
        tool_tip=QCustomFlowWidget.WIDGET_TOOLTIP,
        xml=QCustomFlowWidget.WIDGET_DOM_XML,
        icon=QCustomFlowWidget.WIDGET_ICON,
        container=True,
        group="Layouts"
    )
    logInfo("QCustomFlowWidget registered successfully")
except Exception as e:
    logException(e, message="Error registering QCustomFlowWidget")

logInfo(" All chart widgets registered successfully!")

########################################################################
## DESIGNER BRIDGE - lets a running app push theme changes into Designer
## (refresh icons / restyle open forms). See Custom_Widgets/DesignerBridge.py
########################################################################
try:
    from Custom_Widgets.DesignerBridge import startDesignerBridge
    startDesignerBridge()
except Exception as e:
    logException(e, message="Error starting Designer bridge")

## Tool docks: Log View, UI Workspace, QSS Editor (see DesignerTools.py)
try:
    from Custom_Widgets.DesignerTools import installDesignerTools
    installDesignerTools()
except Exception as e:
    logException(e, message="Error installing Designer tools")
