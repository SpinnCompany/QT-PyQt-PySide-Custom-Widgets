# Custom Widgets Registration for Qt Designer
# Author: Khamisi Kibet

# Dump a native + Python traceback to stderr on a fatal signal (SIGSEGV/SIGABRT)
# so custom-widget crashes inside the Designer process are diagnosable instead
# of silently returning -11.
import os as _os
try:
    import faulthandler as _faulthandler
    from datetime import datetime as _datetime
    _fh_path = _os.path.join(
        _os.path.expanduser("~/.local/share/customwidgets/logs"),
        "designer_faulthandler.log")
    _os.makedirs(_os.path.dirname(_fh_path), exist_ok=True)
    # Truncate on startup ("w"): each Designer launch starts with a clean log,
    # so a dump found here unambiguously belongs to the current session
    # (appending made stale crash dumps look current). A timestamped header
    # marks when this session began.
    _fh_file = open(_fh_path, "w", buffering=1)
    _fh_file.write(
        f"# customwidgets designer faulthandler - session started "
        f"{_datetime.now().isoformat(timespec='seconds')} (pid {_os.getpid()})\n")
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


from Custom_Widgets.QCustomQPushButton import QCustomQPushButton

# Registering QCustomQPushButton with error handling
try:
    logInfo("Registering QCustomQPushButton")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomQPushButton, module=QCustomQPushButton.WIDGET_MODULE,
        tool_tip=QCustomQPushButton.WIDGET_TOOLTIP,
        xml=QCustomQPushButton.WIDGET_DOM_XML,
        icon=QCustomQPushButton.WIDGET_ICON, group="Buttons"
    )
except Exception as e:
    logException(e, message="Error registering QCustomQPushButton")


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


from Custom_Widgets.QCustomBadge import QCustomBadge

# Registering QCustomBadge with error handling
try:
    logInfo("Registering QCustomBadge")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomBadge, module=QCustomBadge.WIDGET_MODULE,
        tool_tip=QCustomBadge.WIDGET_TOOLTIP,
        xml=QCustomBadge.WIDGET_DOM_XML,
        icon=QCustomBadge.WIDGET_ICON, group="Display Widgets"
    )
except Exception as e:
    logException(e, message="Error registering QCustomBadge")


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


from Custom_Widgets.QCustomTableToolbar import QCustomTableToolbar

# Registering QCustomTableToolbar with error handling
try:
    logInfo("Registering QCustomTableToolbar")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomTableToolbar, module=QCustomTableToolbar.WIDGET_MODULE,
        tool_tip=QCustomTableToolbar.WIDGET_TOOLTIP,
        xml=QCustomTableToolbar.WIDGET_DOM_XML,
        icon=QCustomTableToolbar.WIDGET_ICON, group="Item Views"
    )
except Exception as e:
    logException(e, message="Error registering QCustomTableToolbar")


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


from Custom_Widgets.QCustomTabWidget import QCustomTabWidget
from Custom_Widgets.QCustomAccordion import QCustomAccordion

for _ctr, _cont in ((QCustomTabWidget, True), (QCustomAccordion, False)):
    try:
        logInfo("Registering %s" % _ctr.__name__)
        QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
            _ctr, module=_ctr.WIDGET_MODULE, tool_tip=_ctr.WIDGET_TOOLTIP,
            xml=_ctr.WIDGET_DOM_XML, icon=_ctr.WIDGET_ICON,
            container=_cont, group="Containers")
    except Exception as e:
        logException(e, message="Error registering %s" % _ctr.__name__)


from Custom_Widgets.QCustomTreeWidget import QCustomTreeWidget
from Custom_Widgets.QCustomStepper import QCustomStepper

for _w, _grp in ((QCustomTreeWidget, "Item Views"), (QCustomStepper, "Display Widgets")):
    try:
        logInfo("Registering %s" % _w.__name__)
        QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
            _w, module=_w.WIDGET_MODULE, tool_tip=_w.WIDGET_TOOLTIP,
            xml=_w.WIDGET_DOM_XML, icon=_w.WIDGET_ICON, group=_grp)
    except Exception as e:
        logException(e, message="Error registering %s" % _w.__name__)


from Custom_Widgets.QCustomRichTextEditor import QCustomRichTextEditor
from Custom_Widgets.QCustomColorPicker import QCustomColorPicker

for _iw in (QCustomRichTextEditor, QCustomColorPicker):
    try:
        logInfo("Registering %s" % _iw.__name__)
        QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
            _iw, module=_iw.WIDGET_MODULE, tool_tip=_iw.WIDGET_TOOLTIP,
            xml=_iw.WIDGET_DOM_XML, icon=_iw.WIDGET_ICON, group="Input Widgets")
    except Exception as e:
        logException(e, message="Error registering %s" % _iw.__name__)


from Custom_Widgets.QCustomBreadcrumbs import QCustomBreadcrumbs
from Custom_Widgets.QCustomRating import QCustomRating
from Custom_Widgets.QCustomChip import QCustomChipGroup

for _dw in (QCustomBreadcrumbs, QCustomRating, QCustomChipGroup):
    try:
        logInfo("Registering %s" % _dw.__name__)
        QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
            _dw, module=_dw.WIDGET_MODULE, tool_tip=_dw.WIDGET_TOOLTIP,
            xml=_dw.WIDGET_DOM_XML, icon=_dw.WIDGET_ICON, group="Display Widgets")
    except Exception as e:
        logException(e, message="Error registering %s" % _dw.__name__)


from Custom_Widgets.QCustomSkeleton import QCustomSkeleton
from Custom_Widgets.QCustomAvatarGroup import QCustomAvatarGroup
from Custom_Widgets.QCustomTimeline import QCustomTimeline

for _sw in (QCustomSkeleton, QCustomAvatarGroup, QCustomTimeline):
    try:
        logInfo("Registering %s" % _sw.__name__)
        QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
            _sw, module=_sw.WIDGET_MODULE, tool_tip=_sw.WIDGET_TOOLTIP,
            xml=_sw.WIDGET_DOM_XML, icon=_sw.WIDGET_ICON, group="Display Widgets")
    except Exception as e:
        logException(e, message="Error registering %s" % _sw.__name__)


from Custom_Widgets.QCustomPagination import QCustomPagination
from Custom_Widgets.QCustomSegmentedControl import QCustomSegmentedControl

for _pw in (QCustomPagination, QCustomSegmentedControl):
    try:
        logInfo("Registering %s" % _pw.__name__)
        QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
            _pw, module=_pw.WIDGET_MODULE, tool_tip=_pw.WIDGET_TOOLTIP,
            xml=_pw.WIDGET_DOM_XML, icon=_pw.WIDGET_ICON, group="Input Widgets")
    except Exception as e:
        logException(e, message="Error registering %s" % _pw.__name__)


from Custom_Widgets.QCustomEmptyState import QCustomEmptyState
from Custom_Widgets.QCustomFileDropZone import QCustomFileDropZone
from Custom_Widgets.QCustomRangeSlider import QCustomRangeSlider

for _xw, _xg in ((QCustomEmptyState, "Display Widgets"),
                 (QCustomFileDropZone, "Input Widgets"),
                 (QCustomRangeSlider, "Input Widgets")):
    try:
        logInfo("Registering %s" % _xw.__name__)
        QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
            _xw, module=_xw.WIDGET_MODULE, tool_tip=_xw.WIDGET_TOOLTIP,
            xml=_xw.WIDGET_DOM_XML, icon=_xw.WIDGET_ICON, group=_xg)
    except Exception as e:
        logException(e, message="Error registering %s" % _xw.__name__)


from Custom_Widgets.QCustomSwitch import QCustomSwitch
from Custom_Widgets.QCustomNumberInput import QCustomNumberInput
from Custom_Widgets.QCustomAlert import QCustomAlert

for _nw, _ng in ((QCustomSwitch, "Input Widgets"),
                 (QCustomNumberInput, "Input Widgets"),
                 (QCustomAlert, "Display Widgets")):
    try:
        logInfo("Registering %s" % _nw.__name__)
        QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
            _nw, module=_nw.WIDGET_MODULE, tool_tip=_nw.WIDGET_TOOLTIP,
            xml=_nw.WIDGET_DOM_XML, icon=_nw.WIDGET_ICON, group=_ng)
    except Exception as e:
        logException(e, message="Error registering %s" % _nw.__name__)


from Custom_Widgets.QCustomStatCard import QCustomStatCard
from Custom_Widgets.QCustomProgressRing import QCustomProgressRing

for _dw2, _dg2 in ((QCustomStatCard, "Display Widgets"),
                   (QCustomProgressRing, "Progressbars")):
    try:
        logInfo("Registering %s" % _dw2.__name__)
        QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
            _dw2, module=_dw2.WIDGET_MODULE, tool_tip=_dw2.WIDGET_TOOLTIP,
            xml=_dw2.WIDGET_DOM_XML, icon=_dw2.WIDGET_ICON, group=_dg2)
    except Exception as e:
        logException(e, message="Error registering %s" % _dw2.__name__)


from Custom_Widgets.QCustomCard import QCustomCard

# QCustomCard is a container (widgets drop into its body)
try:
    logInfo("Registering QCustomCard")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomCard, module=QCustomCard.WIDGET_MODULE,
        tool_tip=QCustomCard.WIDGET_TOOLTIP, xml=QCustomCard.WIDGET_DOM_XML,
        icon=QCustomCard.WIDGET_ICON, container=True, group="Containers")
except Exception as e:
    logException(e, message="Error registering QCustomCard")


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


from Custom_Widgets.QCustomKbd import QCustomKbd

# Registering QCustomKbd with error handling
try:
    logInfo("Registering QCustomKbd")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomKbd, module=QCustomKbd.WIDGET_MODULE,
        tool_tip=QCustomKbd.WIDGET_TOOLTIP, xml=QCustomKbd.WIDGET_DOM_XML,
        icon=QCustomKbd.WIDGET_ICON, group="Display Widgets")
except Exception as e:
    logException(e, message="Error registering QCustomKbd")


from Custom_Widgets.QCustomCarousel import QCustomCarousel

# Registering QCustomCarousel with error handling
try:
    logInfo("Registering QCustomCarousel")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomCarousel, module=QCustomCarousel.WIDGET_MODULE,
        tool_tip=QCustomCarousel.WIDGET_TOOLTIP, xml=QCustomCarousel.WIDGET_DOM_XML,
        icon=QCustomCarousel.WIDGET_ICON, group="Containers")
except Exception as e:
    logException(e, message="Error registering QCustomCarousel")


from Custom_Widgets.QCustomSplitter import QCustomSplitter

# Registering QCustomSplitter with error handling (container: widgets drop in)
try:
    logInfo("Registering QCustomSplitter")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomSplitter, module=QCustomSplitter.WIDGET_MODULE,
        tool_tip=QCustomSplitter.WIDGET_TOOLTIP, xml=QCustomSplitter.WIDGET_DOM_XML,
        icon=QCustomSplitter.WIDGET_ICON, container=True, group="Containers")
except Exception as e:
    logException(e, message="Error registering QCustomSplitter")

from Custom_Widgets.QCustomPaymentCard import QCustomPaymentCard

# Registering QCustomPaymentCard with error handling
try:
    logInfo("Registering QCustomPaymentCard")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomPaymentCard, module=QCustomPaymentCard.WIDGET_MODULE,
        tool_tip=QCustomPaymentCard.WIDGET_TOOLTIP, xml=QCustomPaymentCard.WIDGET_DOM_XML,
        icon=QCustomPaymentCard.WIDGET_ICON, group="Display Widgets")
except Exception as e:
    logException(e, message="Error registering QCustomPaymentCard")


from Custom_Widgets.QCustomMiniBarChart import QCustomMiniBarChart

# Registering QCustomMiniBarChart with error handling
try:
    logInfo("Registering QCustomMiniBarChart")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomMiniBarChart, module=QCustomMiniBarChart.WIDGET_MODULE,
        tool_tip=QCustomMiniBarChart.WIDGET_TOOLTIP, xml=QCustomMiniBarChart.WIDGET_DOM_XML,
        icon=QCustomMiniBarChart.WIDGET_ICON, group="Charts")
except Exception as e:
    logException(e, message="Error registering QCustomMiniBarChart")


from Custom_Widgets.QCustomDivergingBarChart import QCustomDivergingBarChart

# Registering QCustomDivergingBarChart with error handling
try:
    logInfo("Registering QCustomDivergingBarChart")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomDivergingBarChart, module=QCustomDivergingBarChart.WIDGET_MODULE,
        tool_tip=QCustomDivergingBarChart.WIDGET_TOOLTIP, xml=QCustomDivergingBarChart.WIDGET_DOM_XML,
        icon=QCustomDivergingBarChart.WIDGET_ICON, group="Charts")
except Exception as e:
    logException(e, message="Error registering QCustomDivergingBarChart")


from Custom_Widgets.QCustomDotMatrix import QCustomDotMatrix

# Registering QCustomDotMatrix with error handling
try:
    logInfo("Registering QCustomDotMatrix")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomDotMatrix, module=QCustomDotMatrix.WIDGET_MODULE,
        tool_tip=QCustomDotMatrix.WIDGET_TOOLTIP, xml=QCustomDotMatrix.WIDGET_DOM_XML,
        icon=QCustomDotMatrix.WIDGET_ICON, group="Charts")
except Exception as e:
    logException(e, message="Error registering QCustomDotMatrix")


from Custom_Widgets.QCustomBeeswarm import QCustomBeeswarm

# Registering QCustomBeeswarm with error handling
try:
    logInfo("Registering QCustomBeeswarm")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomBeeswarm, module=QCustomBeeswarm.WIDGET_MODULE,
        tool_tip=QCustomBeeswarm.WIDGET_TOOLTIP, xml=QCustomBeeswarm.WIDGET_DOM_XML,
        icon=QCustomBeeswarm.WIDGET_ICON, group="Charts")
except Exception as e:
    logException(e, message="Error registering QCustomBeeswarm")


from Custom_Widgets.QCustomGanttChart import QCustomGanttChart

# Registering QCustomGanttChart with error handling
try:
    logInfo("Registering QCustomGanttChart")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomGanttChart, module=QCustomGanttChart.WIDGET_MODULE,
        tool_tip=QCustomGanttChart.WIDGET_TOOLTIP, xml=QCustomGanttChart.WIDGET_DOM_XML,
        icon=QCustomGanttChart.WIDGET_ICON, group="Charts")
except Exception as e:
    logException(e, message="Error registering QCustomGanttChart")


from Custom_Widgets.QCustomTileButton import QCustomTileButton

# Registering QCustomTileButton with error handling
try:
    logInfo("Registering QCustomTileButton")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomTileButton, module=QCustomTileButton.WIDGET_MODULE,
        tool_tip=QCustomTileButton.WIDGET_TOOLTIP, xml=QCustomTileButton.WIDGET_DOM_XML,
        icon=QCustomTileButton.WIDGET_ICON, group="Buttons")
except Exception as e:
    logException(e, message="Error registering QCustomTileButton")


from Custom_Widgets.QCustomCardStack import QCustomCardStack

# Registering QCustomCardStack with error handling
try:
    logInfo("Registering QCustomCardStack")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomCardStack, module=QCustomCardStack.WIDGET_MODULE,
        tool_tip=QCustomCardStack.WIDGET_TOOLTIP, xml=QCustomCardStack.WIDGET_DOM_XML,
        icon=QCustomCardStack.WIDGET_ICON, group="Containers", container=True)
except Exception as e:
    logException(e, message="Error registering QCustomCardStack")


from Custom_Widgets.QCustomMenu import QCustomMenu

# Registering QCustomMenu with error handling
try:
    logInfo("Registering QCustomMenu")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomMenu, module=QCustomMenu.WIDGET_MODULE,
        tool_tip=QCustomMenu.WIDGET_TOOLTIP, xml=QCustomMenu.WIDGET_DOM_XML,
        icon=QCustomMenu.WIDGET_ICON, group="Menus")
except Exception as e:
    logException(e, message="Error registering QCustomMenu")


from Custom_Widgets.QCustomModal import QCustomModal

# Registering QCustomModal with error handling
try:
    logInfo("Registering QCustomModal")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomModal, module=QCustomModal.WIDGET_MODULE,
        tool_tip=QCustomModal.WIDGET_TOOLTIP, xml=QCustomModal.WIDGET_DOM_XML,
        icon=QCustomModal.WIDGET_ICON, group="Menus")
except Exception as e:
    logException(e, message="Error registering QCustomModal")


from Custom_Widgets.QCustomCompassDial import QCustomCompassDial

# Registering QCustomCompassDial with error handling
try:
    logInfo("Registering QCustomCompassDial")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomCompassDial, module=QCustomCompassDial.WIDGET_MODULE,
        tool_tip=QCustomCompassDial.WIDGET_TOOLTIP, xml=QCustomCompassDial.WIDGET_DOM_XML,
        icon=QCustomCompassDial.WIDGET_ICON, group="Display Widgets")
except Exception as e:
    logException(e, message="Error registering QCustomCompassDial")


from Custom_Widgets.QCustomCompass import QCustomCompass

# Registering QCustomCompass with error handling
try:
    logInfo("Registering QCustomCompass")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomCompass, module=QCustomCompass.WIDGET_MODULE,
        tool_tip=QCustomCompass.WIDGET_TOOLTIP, xml=QCustomCompass.WIDGET_DOM_XML,
        icon=QCustomCompass.WIDGET_ICON, group="Display Widgets")
except Exception as e:
    logException(e, message="Error registering QCustomCompass")


from Custom_Widgets.QCustomBubbleChart import QCustomBubbleChart

# Registering QCustomBubbleChart with error handling
try:
    logInfo("Registering QCustomBubbleChart")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomBubbleChart, module=QCustomBubbleChart.WIDGET_MODULE,
        tool_tip=QCustomBubbleChart.WIDGET_TOOLTIP, xml=QCustomBubbleChart.WIDGET_DOM_XML,
        icon=QCustomBubbleChart.WIDGET_ICON, group="Charts")
except Exception as e:
    logException(e, message="Error registering QCustomBubbleChart")


from Custom_Widgets.QCustomAgendaList import QCustomAgendaList

# Registering QCustomAgendaList with error handling
try:
    logInfo("Registering QCustomAgendaList")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomAgendaList, module=QCustomAgendaList.WIDGET_MODULE,
        tool_tip=QCustomAgendaList.WIDGET_TOOLTIP, xml=QCustomAgendaList.WIDGET_DOM_XML,
        icon=QCustomAgendaList.WIDGET_ICON, group="Display Widgets")
except Exception as e:
    logException(e, message="Error registering QCustomAgendaList")


from Custom_Widgets.QCustomWaveform import QCustomWaveform

# Registering QCustomWaveform with error handling
try:
    logInfo("Registering QCustomWaveform")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomWaveform, module=QCustomWaveform.WIDGET_MODULE,
        tool_tip=QCustomWaveform.WIDGET_TOOLTIP, xml=QCustomWaveform.WIDGET_DOM_XML,
        icon=QCustomWaveform.WIDGET_ICON, group="Charts")
except Exception as e:
    logException(e, message="Error registering QCustomWaveform")


from Custom_Widgets.QCustomDateRangePicker import QCustomDateRangePicker

# Registering QCustomDateRangePicker with error handling
try:
    logInfo("Registering QCustomDateRangePicker")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomDateRangePicker, module=QCustomDateRangePicker.WIDGET_MODULE,
        tool_tip=QCustomDateRangePicker.WIDGET_TOOLTIP, xml=QCustomDateRangePicker.WIDGET_DOM_XML,
        icon=QCustomDateRangePicker.WIDGET_ICON, group="Input Widgets")
except Exception as e:
    logException(e, message="Error registering QCustomDateRangePicker")


from Custom_Widgets.QCustomRulerPicker import QCustomRulerPicker

# Registering QCustomRulerPicker with error handling
try:
    logInfo("Registering QCustomRulerPicker")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomRulerPicker, module=QCustomRulerPicker.WIDGET_MODULE,
        tool_tip=QCustomRulerPicker.WIDGET_TOOLTIP, xml=QCustomRulerPicker.WIDGET_DOM_XML,
        icon=QCustomRulerPicker.WIDGET_ICON, group="Input Widgets")
except Exception as e:
    logException(e, message="Error registering QCustomRulerPicker")


from Custom_Widgets.QCustomLiquidGauge import QCustomLiquidGauge

# Registering QCustomLiquidGauge with error handling
try:
    logInfo("Registering QCustomLiquidGauge")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomLiquidGauge, module=QCustomLiquidGauge.WIDGET_MODULE,
        tool_tip=QCustomLiquidGauge.WIDGET_TOOLTIP, xml=QCustomLiquidGauge.WIDGET_DOM_XML,
        icon=QCustomLiquidGauge.WIDGET_ICON, group="Progressbars")
except Exception as e:
    logException(e, message="Error registering QCustomLiquidGauge")


from Custom_Widgets.QCustomHeatmap import QCustomHeatmap

# Registering QCustomHeatmap with error handling
try:
    logInfo("Registering QCustomHeatmap")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomHeatmap, module=QCustomHeatmap.WIDGET_MODULE,
        tool_tip=QCustomHeatmap.WIDGET_TOOLTIP, xml=QCustomHeatmap.WIDGET_DOM_XML,
        icon=QCustomHeatmap.WIDGET_ICON, group="Charts")
except Exception as e:
    logException(e, message="Error registering QCustomHeatmap")


from Custom_Widgets.QCustomRadialGauge import QCustomRadialGauge

# Registering QCustomRadialGauge with error handling
try:
    logInfo("Registering QCustomRadialGauge")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomRadialGauge, module=QCustomRadialGauge.WIDGET_MODULE,
        tool_tip=QCustomRadialGauge.WIDGET_TOOLTIP, xml=QCustomRadialGauge.WIDGET_DOM_XML,
        icon=QCustomRadialGauge.WIDGET_ICON, group="Progressbars")
except Exception as e:
    logException(e, message="Error registering QCustomRadialGauge")


from Custom_Widgets.QCustomListRow import QCustomListRow

# Registering QCustomListRow with error handling
try:
    logInfo("Registering QCustomListRow")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomListRow, module=QCustomListRow.WIDGET_MODULE,
        tool_tip=QCustomListRow.WIDGET_TOOLTIP, xml=QCustomListRow.WIDGET_DOM_XML,
        icon=QCustomListRow.WIDGET_ICON, group="Display Widgets")
except Exception as e:
    logException(e, message="Error registering QCustomListRow")


from Custom_Widgets.QCustomAvatar import QCustomAvatar

# Registering QCustomAvatar with error handling
try:
    logInfo("Registering QCustomAvatar")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomAvatar, module=QCustomAvatar.WIDGET_MODULE,
        tool_tip=QCustomAvatar.WIDGET_TOOLTIP, xml=QCustomAvatar.WIDGET_DOM_XML,
        icon=QCustomAvatar.WIDGET_ICON, group="Display Widgets")
except Exception as e:
    logException(e, message="Error registering QCustomAvatar")


from Custom_Widgets.QCustomTrendChip import QCustomTrendChip

# Registering QCustomTrendChip with error handling
try:
    logInfo("Registering QCustomTrendChip")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomTrendChip, module=QCustomTrendChip.WIDGET_MODULE,
        tool_tip=QCustomTrendChip.WIDGET_TOOLTIP, xml=QCustomTrendChip.WIDGET_DOM_XML,
        icon=QCustomTrendChip.WIDGET_ICON, group="Charts")
except Exception as e:
    logException(e, message="Error registering QCustomTrendChip")


from Custom_Widgets.QCustomPageDots import QCustomPageDots

# Registering QCustomPageDots with error handling
try:
    logInfo("Registering QCustomPageDots")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomPageDots, module=QCustomPageDots.WIDGET_MODULE,
        tool_tip=QCustomPageDots.WIDGET_TOOLTIP, xml=QCustomPageDots.WIDGET_DOM_XML,
        icon=QCustomPageDots.WIDGET_ICON, group="Navigation")
except Exception as e:
    logException(e, message="Error registering QCustomPageDots")


from Custom_Widgets.QCustomChatListItem import QCustomChatListItem

# Registering QCustomChatListItem with error handling
try:
    logInfo("Registering QCustomChatListItem")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomChatListItem, module=QCustomChatListItem.WIDGET_MODULE,
        tool_tip=QCustomChatListItem.WIDGET_TOOLTIP, xml=QCustomChatListItem.WIDGET_DOM_XML,
        icon=QCustomChatListItem.WIDGET_ICON, group="Display Widgets")
except Exception as e:
    logException(e, message="Error registering QCustomChatListItem")


from Custom_Widgets.QCustomChatBubble import QCustomChatBubble

# Registering QCustomChatBubble with error handling
try:
    logInfo("Registering QCustomChatBubble")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomChatBubble, module=QCustomChatBubble.WIDGET_MODULE,
        tool_tip=QCustomChatBubble.WIDGET_TOOLTIP, xml=QCustomChatBubble.WIDGET_DOM_XML,
        icon=QCustomChatBubble.WIDGET_ICON, group="Display Widgets")
except Exception as e:
    logException(e, message="Error registering QCustomChatBubble")


from Custom_Widgets.QCustomVoiceMessage import QCustomVoiceMessage

# Registering QCustomVoiceMessage with error handling
try:
    logInfo("Registering QCustomVoiceMessage")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomVoiceMessage, module=QCustomVoiceMessage.WIDGET_MODULE,
        tool_tip=QCustomVoiceMessage.WIDGET_TOOLTIP, xml=QCustomVoiceMessage.WIDGET_DOM_XML,
        icon=QCustomVoiceMessage.WIDGET_ICON, group="Display Widgets")
except Exception as e:
    logException(e, message="Error registering QCustomVoiceMessage")


# ---- Chat / messaging component widgets (normalization batch) ------------- #
def _register_widget(cls, group):
    try:
        logInfo("Registering %s" % cls.__name__)
        QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
            cls, module=cls.WIDGET_MODULE, tool_tip=cls.WIDGET_TOOLTIP,
            xml=cls.WIDGET_DOM_XML, icon=getattr(cls, "WIDGET_ICON", ""), group=group)
    except Exception as e:
        logException(e, message="Error registering %s" % cls.__name__)


try:
    from Custom_Widgets.QCustomActionButton import QCustomActionButton
    from Custom_Widgets.QCustomChatDivider import QCustomChatDivider
    from Custom_Widgets.QCustomTypingIndicator import QCustomTypingIndicator
    from Custom_Widgets.QCustomMediaGrid import QCustomMediaGrid
    from Custom_Widgets.QCustomChatList import QCustomChatList
    from Custom_Widgets.QCustomChatThread import QCustomChatThread
    from Custom_Widgets.QCustomChatInput import QCustomChatInput
    _register_widget(QCustomActionButton, "Buttons")
    _register_widget(QCustomChatDivider, "Chat")
    _register_widget(QCustomTypingIndicator, "Chat")
    _register_widget(QCustomMediaGrid, "Display Widgets")
    _register_widget(QCustomChatList, "Chat")
    _register_widget(QCustomChatThread, "Chat")
    _register_widget(QCustomChatInput, "Chat")
except Exception as e:
    logException(e, message="Error registering chat component widgets")


# ---- Media / attachment widgets (P2 batch) -------------------------------- #
try:
    from Custom_Widgets.QCustomImageViewer import QCustomImageViewer
    from Custom_Widgets.QCustomVideoPlayer import QCustomVideoPlayer
    from Custom_Widgets.QCustomFileCard import QCustomFileCard
    from Custom_Widgets.QCustomLinkPreview import QCustomLinkPreview
    _register_widget(QCustomImageViewer, "Display Widgets")
    _register_widget(QCustomVideoPlayer, "Display Widgets")
    _register_widget(QCustomFileCard, "Display Widgets")
    _register_widget(QCustomLinkPreview, "Display Widgets")
except Exception as e:
    logException(e, message="Error registering media widgets")


# ---- Messaging widgets (P3 batch) ----------------------------------------- #
try:
    from Custom_Widgets.QCustomReactionBar import QCustomReactionBar
    from Custom_Widgets.QCustomMessageStatus import QCustomMessageStatus
    _register_widget(QCustomReactionBar, "Chat")
    _register_widget(QCustomMessageStatus, "Chat")
except Exception as e:
    logException(e, message="Error registering messaging widgets")


from Custom_Widgets.QCustomCoverCard import QCustomCoverCard

# Registering QCustomCoverCard with error handling
try:
    logInfo("Registering QCustomCoverCard")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomCoverCard, module=QCustomCoverCard.WIDGET_MODULE,
        tool_tip=QCustomCoverCard.WIDGET_TOOLTIP, xml=QCustomCoverCard.WIDGET_DOM_XML,
        icon=QCustomCoverCard.WIDGET_ICON, group="Media")
except Exception as e:
    logException(e, message="Error registering QCustomCoverCard")


from Custom_Widgets.QCustomCoverFlow import QCustomCoverFlow

# Registering QCustomCoverFlow with error handling
try:
    logInfo("Registering QCustomCoverFlow")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomCoverFlow, module=QCustomCoverFlow.WIDGET_MODULE,
        tool_tip=QCustomCoverFlow.WIDGET_TOOLTIP, xml=QCustomCoverFlow.WIDGET_DOM_XML,
        icon=QCustomCoverFlow.WIDGET_ICON, group="Media")
except Exception as e:
    logException(e, message="Error registering QCustomCoverFlow")


from Custom_Widgets.QCustomPlayerBar import QCustomPlayerBar

# Registering QCustomPlayerBar with error handling
try:
    logInfo("Registering QCustomPlayerBar")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomPlayerBar, module=QCustomPlayerBar.WIDGET_MODULE,
        tool_tip=QCustomPlayerBar.WIDGET_TOOLTIP, xml=QCustomPlayerBar.WIDGET_DOM_XML,
        icon=QCustomPlayerBar.WIDGET_ICON, group="Media")
except Exception as e:
    logException(e, message="Error registering QCustomPlayerBar")


from Custom_Widgets.QCustomNodeGraph import QCustomNodeGraph

# Registering QCustomNodeGraph with error handling
try:
    logInfo("Registering QCustomNodeGraph")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomNodeGraph, module=QCustomNodeGraph.WIDGET_MODULE,
        tool_tip=QCustomNodeGraph.WIDGET_TOOLTIP, xml=QCustomNodeGraph.WIDGET_DOM_XML,
        icon=QCustomNodeGraph.WIDGET_ICON, group="Containers")
except Exception as e:
    logException(e, message="Error registering QCustomNodeGraph")


from Custom_Widgets.QCustomMediaTimeline import QCustomMediaTimeline

# Registering QCustomMediaTimeline with error handling
try:
    logInfo("Registering QCustomMediaTimeline")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomMediaTimeline, module=QCustomMediaTimeline.WIDGET_MODULE,
        tool_tip=QCustomMediaTimeline.WIDGET_TOOLTIP, xml=QCustomMediaTimeline.WIDGET_DOM_XML,
        icon=QCustomMediaTimeline.WIDGET_ICON, group="Media")
except Exception as e:
    logException(e, message="Error registering QCustomMediaTimeline")


from Custom_Widgets.QCustomQLabel import QCustomQLabel

# Registering QCustomQLabel with error handling
try:
    logInfo("Registering QCustomQLabel")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomQLabel, module=QCustomQLabel.WIDGET_MODULE,
        tool_tip=QCustomQLabel.WIDGET_TOOLTIP, xml=QCustomQLabel.WIDGET_DOM_XML,
        icon=QCustomQLabel.WIDGET_ICON, group="Display Widgets")
except Exception as e:
    logException(e, message="Error registering QCustomQLabel")


from Custom_Widgets.QCustomGlassFrame import QCustomGlassFrame

# Registering QCustomGlassFrame with error handling
try:
    logInfo("Registering QCustomGlassFrame")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomGlassFrame, module=QCustomGlassFrame.WIDGET_MODULE,
        tool_tip=QCustomGlassFrame.WIDGET_TOOLTIP, xml=QCustomGlassFrame.WIDGET_DOM_XML,
        icon=QCustomGlassFrame.WIDGET_ICON, group="Containers", container=True)
except Exception as e:
    logException(e, message="Error registering QCustomGlassFrame")


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
