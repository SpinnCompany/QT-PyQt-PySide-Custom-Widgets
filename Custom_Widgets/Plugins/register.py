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


def _iconFor(widget):
    """Absolute, existing path for a widget's Designer palette icon, or "".

    Most widgets declare a BARE RELATIVE WIDGET_ICON
    ("components/icons/combobox.png"). Designer resolves that against its own
    working directory, not the package, so the icon silently never loads even
    though the file is right there — 44 registered widgets were in exactly that
    state. Anchor it to the package instead.

    A path that does not resolve returns "" rather than a dead path: Designer
    then draws its default placeholder instead of a broken-image box, and the
    difference tells you the icon is genuinely missing rather than mislocated.
    """
    path = getattr(widget, "WIDGET_ICON", "") or ""
    if not path:
        return ""
    if not _os.path.isabs(path):
        path = _os.path.normpath(_os.path.join(_PKG_DIR, path))
    return path if _os.path.isfile(path) else ""


try:
    from Custom_Widgets._resources import packageDir as _packageDir
    _PKG_DIR = _packageDir()
except Exception:
    # Fall back to this file's grandparent (Custom_Widgets/), so a failure to
    # import the helper degrades to no icons rather than no widgets.
    _PKG_DIR = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))

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
        icon=_iconFor(QCustomQMainWindow), container=True, group="Main Window"
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
        icon=_iconFor(QCustomQPushButton), group="Buttons"
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
        icon=_iconFor(QAvatarWidget)
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
        icon=_iconFor(QCustomBadge), group="Display Widgets"
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
        icon=_iconFor(AnalogGaugeWidget)
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
        icon=_iconFor(QCustomDataTable), group="Item Views"
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
        icon=_iconFor(QCustomTableToolbar), group="Item Views"
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
        icon=_iconFor(QCustomComboBox), group="Input Widgets"
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
            xml=_dtw.WIDGET_DOM_XML, icon=_iconFor(_dtw), group=_grp)
    except Exception as e:
        logException(e, message="Error registering %s" % _dtw.__name__)


from Custom_Widgets.QCustomTabWidget import QCustomTabWidget
from Custom_Widgets.QCustomAccordion import QCustomAccordion

for _ctr, _cont in ((QCustomTabWidget, True), (QCustomAccordion, False)):
    try:
        logInfo("Registering %s" % _ctr.__name__)
        QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
            _ctr, module=_ctr.WIDGET_MODULE, tool_tip=_ctr.WIDGET_TOOLTIP,
            xml=_ctr.WIDGET_DOM_XML, icon=_iconFor(_ctr),
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
            xml=_w.WIDGET_DOM_XML, icon=_iconFor(_w), group=_grp)
    except Exception as e:
        logException(e, message="Error registering %s" % _w.__name__)


from Custom_Widgets.QCustomRichTextEditor import QCustomRichTextEditor
from Custom_Widgets.QCustomColorPicker import QCustomColorPicker

for _iw in (QCustomRichTextEditor, QCustomColorPicker):
    try:
        logInfo("Registering %s" % _iw.__name__)
        QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
            _iw, module=_iw.WIDGET_MODULE, tool_tip=_iw.WIDGET_TOOLTIP,
            xml=_iw.WIDGET_DOM_XML, icon=_iconFor(_iw), group="Input Widgets")
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
            xml=_dw.WIDGET_DOM_XML, icon=_iconFor(_dw), group="Display Widgets")
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
            xml=_sw.WIDGET_DOM_XML, icon=_iconFor(_sw), group="Display Widgets")
    except Exception as e:
        logException(e, message="Error registering %s" % _sw.__name__)


from Custom_Widgets.QCustomPagination import QCustomPagination
from Custom_Widgets.QCustomSegmentedControl import QCustomSegmentedControl

for _pw in (QCustomPagination, QCustomSegmentedControl):
    try:
        logInfo("Registering %s" % _pw.__name__)
        QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
            _pw, module=_pw.WIDGET_MODULE, tool_tip=_pw.WIDGET_TOOLTIP,
            xml=_pw.WIDGET_DOM_XML, icon=_iconFor(_pw), group="Input Widgets")
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
            xml=_xw.WIDGET_DOM_XML, icon=_iconFor(_xw), group=_xg)
    except Exception as e:
        logException(e, message="Error registering %s" % _xw.__name__)


from Custom_Widgets.QCustomSwitch import QCustomSwitch
from Custom_Widgets.QCustomNumberInput import QCustomNumberInput
from Custom_Widgets.QCustomAlert import QCustomAlert
from Custom_Widgets.QCustomRadioButton import QCustomRadioButton
from Custom_Widgets.QCustomRadioGroup import QCustomRadioGroup
from Custom_Widgets.QCustomTextArea import QCustomTextArea
from Custom_Widgets.QCustomVerificationCode import QCustomVerificationCode
from Custom_Widgets.QCustomMultiSelect import QCustomMultiSelect
from Custom_Widgets.QCustomImagePicker import QCustomImagePicker
from Custom_Widgets.QCustomGradientPicker import QCustomGradientPicker

for _nw, _ng in ((QCustomSwitch, "Input Widgets"),
                 (QCustomNumberInput, "Input Widgets"),
                 (QCustomRadioButton, "Input Widgets"),
                 (QCustomRadioGroup, "Input Widgets"),
                 (QCustomTextArea, "Input Widgets"),
                 (QCustomVerificationCode, "Input Widgets"),
                 (QCustomMultiSelect, "Input Widgets"),
                 (QCustomImagePicker, "Input Widgets"),
                 (QCustomGradientPicker, "Input Widgets"),
                 (QCustomAlert, "Display Widgets")):
    try:
        logInfo("Registering %s" % _nw.__name__)
        QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
            _nw, module=_nw.WIDGET_MODULE, tool_tip=_nw.WIDGET_TOOLTIP,
            xml=_nw.WIDGET_DOM_XML, icon=_iconFor(_nw), group=_ng)
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
            xml=_dw2.WIDGET_DOM_XML, icon=_iconFor(_dw2), group=_dg2)
    except Exception as e:
        logException(e, message="Error registering %s" % _dw2.__name__)


from Custom_Widgets.QCustomCard import QCustomCard

# QCustomCard is a container (widgets drop into its body)
try:
    logInfo("Registering QCustomCard")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomCard, module=QCustomCard.WIDGET_MODULE,
        tool_tip=QCustomCard.WIDGET_TOOLTIP, xml=QCustomCard.WIDGET_DOM_XML,
        icon=_iconFor(QCustomCard), container=True, group="Containers")
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
        icon=_iconFor(QCustomThemeList)
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
        icon=_iconFor(QCustomThemeDarkLightToggle)
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
        icon=_iconFor(QCustomCheckBox)
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
        icon=_iconFor(QCustomSidebar), container=True, group="Sidebar"
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
        icon=_iconFor(QCustomHamburgerMenu), container=True, group="Hamburger Menu"
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
        icon=_iconFor(QCustomHorizontalSeparator), container=False, group="Sidebar"
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
        icon=_iconFor(QCustomVerticalSeparator), container=False, group="Sidebar"
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
        icon=_iconFor(QCustomSidebarLabel), group="Sidebar"
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
        icon=_iconFor(QCustomSidebarButton), group="Sidebar"
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
        icon=_iconFor(QCustomSidebarContainer), container=True, group="Sidebar"
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
        icon=_iconFor(QCustomRoundProgressBar), group="Progressbars"
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
        icon=_iconFor(QCustomComponent), container=True, group="Component Container"
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
        icon=_iconFor(QCustomComponentContainer), container=False, group="Component Container"
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
        icon=_iconFor(QCustomQStackedWidget), container=True
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
        icon=_iconFor(QCustomQProgressBar), group="Progressbars"
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
        icon=_iconFor(QCustomQRGenerator), container=False, group="QR Generator"
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
        icon=_iconFor(QCustomLineChart), 
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
        icon=_iconFor(QCustomBarChart), 
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
        icon=_iconFor(QCustomAreaChart), 
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
        icon=_iconFor(QCustomPieChart), 
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
        icon=_iconFor(QCustomVerticalBarSeries),
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
        icon=_iconFor(QCustomHorizontalBarSeries),
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
        icon=_iconFor(QCustomFlowWidget),
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
        icon=_iconFor(QCustomKbd), group="Display Widgets")
except Exception as e:
    logException(e, message="Error registering QCustomKbd")


from Custom_Widgets.QCustomCarousel import QCustomCarousel

# Registering QCustomCarousel with error handling
try:
    logInfo("Registering QCustomCarousel")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomCarousel, module=QCustomCarousel.WIDGET_MODULE,
        tool_tip=QCustomCarousel.WIDGET_TOOLTIP, xml=QCustomCarousel.WIDGET_DOM_XML,
        icon=_iconFor(QCustomCarousel), group="Containers")
except Exception as e:
    logException(e, message="Error registering QCustomCarousel")


from Custom_Widgets.QCustomSplitter import QCustomSplitter

# Registering QCustomSplitter with error handling (container: widgets drop in)
try:
    logInfo("Registering QCustomSplitter")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomSplitter, module=QCustomSplitter.WIDGET_MODULE,
        tool_tip=QCustomSplitter.WIDGET_TOOLTIP, xml=QCustomSplitter.WIDGET_DOM_XML,
        icon=_iconFor(QCustomSplitter), container=True, group="Containers")
except Exception as e:
    logException(e, message="Error registering QCustomSplitter")

from Custom_Widgets.QCustomPaymentCard import QCustomPaymentCard

# Registering QCustomPaymentCard with error handling
try:
    logInfo("Registering QCustomPaymentCard")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomPaymentCard, module=QCustomPaymentCard.WIDGET_MODULE,
        tool_tip=QCustomPaymentCard.WIDGET_TOOLTIP, xml=QCustomPaymentCard.WIDGET_DOM_XML,
        icon=_iconFor(QCustomPaymentCard), group="Display Widgets")
except Exception as e:
    logException(e, message="Error registering QCustomPaymentCard")


from Custom_Widgets.QCustomMiniBarChart import QCustomMiniBarChart

# Registering QCustomMiniBarChart with error handling
try:
    logInfo("Registering QCustomMiniBarChart")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomMiniBarChart, module=QCustomMiniBarChart.WIDGET_MODULE,
        tool_tip=QCustomMiniBarChart.WIDGET_TOOLTIP, xml=QCustomMiniBarChart.WIDGET_DOM_XML,
        icon=_iconFor(QCustomMiniBarChart), group="Charts")
except Exception as e:
    logException(e, message="Error registering QCustomMiniBarChart")


from Custom_Widgets.QCustomDivergingBarChart import QCustomDivergingBarChart

# Registering QCustomDivergingBarChart with error handling
try:
    logInfo("Registering QCustomDivergingBarChart")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomDivergingBarChart, module=QCustomDivergingBarChart.WIDGET_MODULE,
        tool_tip=QCustomDivergingBarChart.WIDGET_TOOLTIP, xml=QCustomDivergingBarChart.WIDGET_DOM_XML,
        icon=_iconFor(QCustomDivergingBarChart), group="Charts")
except Exception as e:
    logException(e, message="Error registering QCustomDivergingBarChart")


from Custom_Widgets.QCustomDotMatrix import QCustomDotMatrix

# Registering QCustomDotMatrix with error handling
try:
    logInfo("Registering QCustomDotMatrix")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomDotMatrix, module=QCustomDotMatrix.WIDGET_MODULE,
        tool_tip=QCustomDotMatrix.WIDGET_TOOLTIP, xml=QCustomDotMatrix.WIDGET_DOM_XML,
        icon=_iconFor(QCustomDotMatrix), group="Charts")
except Exception as e:
    logException(e, message="Error registering QCustomDotMatrix")


from Custom_Widgets.QCustomBeeswarm import QCustomBeeswarm

# Registering QCustomBeeswarm with error handling
try:
    logInfo("Registering QCustomBeeswarm")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomBeeswarm, module=QCustomBeeswarm.WIDGET_MODULE,
        tool_tip=QCustomBeeswarm.WIDGET_TOOLTIP, xml=QCustomBeeswarm.WIDGET_DOM_XML,
        icon=_iconFor(QCustomBeeswarm), group="Charts")
except Exception as e:
    logException(e, message="Error registering QCustomBeeswarm")


from Custom_Widgets.QCustomGanttChart import QCustomGanttChart

# Registering QCustomGanttChart with error handling
try:
    logInfo("Registering QCustomGanttChart")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomGanttChart, module=QCustomGanttChart.WIDGET_MODULE,
        tool_tip=QCustomGanttChart.WIDGET_TOOLTIP, xml=QCustomGanttChart.WIDGET_DOM_XML,
        icon=_iconFor(QCustomGanttChart), group="Charts")
except Exception as e:
    logException(e, message="Error registering QCustomGanttChart")


from Custom_Widgets.QCustomTileButton import QCustomTileButton

# Registering QCustomTileButton with error handling
try:
    logInfo("Registering QCustomTileButton")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomTileButton, module=QCustomTileButton.WIDGET_MODULE,
        tool_tip=QCustomTileButton.WIDGET_TOOLTIP, xml=QCustomTileButton.WIDGET_DOM_XML,
        icon=_iconFor(QCustomTileButton), group="Buttons")
except Exception as e:
    logException(e, message="Error registering QCustomTileButton")


from Custom_Widgets.QCustomCardStack import QCustomCardStack

# Registering QCustomCardStack with error handling
try:
    logInfo("Registering QCustomCardStack")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomCardStack, module=QCustomCardStack.WIDGET_MODULE,
        tool_tip=QCustomCardStack.WIDGET_TOOLTIP, xml=QCustomCardStack.WIDGET_DOM_XML,
        icon=_iconFor(QCustomCardStack), group="Containers", container=True)
except Exception as e:
    logException(e, message="Error registering QCustomCardStack")


from Custom_Widgets.QCustomMenu import QCustomMenu

# Registering QCustomMenu with error handling
try:
    logInfo("Registering QCustomMenu")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomMenu, module=QCustomMenu.WIDGET_MODULE,
        tool_tip=QCustomMenu.WIDGET_TOOLTIP, xml=QCustomMenu.WIDGET_DOM_XML,
        icon=_iconFor(QCustomMenu), group="Menus")
except Exception as e:
    logException(e, message="Error registering QCustomMenu")


from Custom_Widgets.QCustomModal import QCustomModal

# Registering QCustomModal with error handling
try:
    logInfo("Registering QCustomModal")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomModal, module=QCustomModal.WIDGET_MODULE,
        tool_tip=QCustomModal.WIDGET_TOOLTIP, xml=QCustomModal.WIDGET_DOM_XML,
        icon=_iconFor(QCustomModal), group="Menus")
except Exception as e:
    logException(e, message="Error registering QCustomModal")


from Custom_Widgets.QCustomCompassDial import QCustomCompassDial

# Registering QCustomCompassDial with error handling
try:
    logInfo("Registering QCustomCompassDial")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomCompassDial, module=QCustomCompassDial.WIDGET_MODULE,
        tool_tip=QCustomCompassDial.WIDGET_TOOLTIP, xml=QCustomCompassDial.WIDGET_DOM_XML,
        icon=_iconFor(QCustomCompassDial), group="Display Widgets")
except Exception as e:
    logException(e, message="Error registering QCustomCompassDial")


from Custom_Widgets.QCustomCompass import QCustomCompass

# Registering QCustomCompass with error handling
try:
    logInfo("Registering QCustomCompass")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomCompass, module=QCustomCompass.WIDGET_MODULE,
        tool_tip=QCustomCompass.WIDGET_TOOLTIP, xml=QCustomCompass.WIDGET_DOM_XML,
        icon=_iconFor(QCustomCompass), group="Display Widgets")
except Exception as e:
    logException(e, message="Error registering QCustomCompass")


from Custom_Widgets.QCustomBubbleChart import QCustomBubbleChart

# Registering QCustomBubbleChart with error handling
try:
    logInfo("Registering QCustomBubbleChart")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomBubbleChart, module=QCustomBubbleChart.WIDGET_MODULE,
        tool_tip=QCustomBubbleChart.WIDGET_TOOLTIP, xml=QCustomBubbleChart.WIDGET_DOM_XML,
        icon=_iconFor(QCustomBubbleChart), group="Charts")
except Exception as e:
    logException(e, message="Error registering QCustomBubbleChart")


from Custom_Widgets.QCustomCandlestickChart import QCustomCandlestickChart
from Custom_Widgets.QCustomRadarChart import QCustomRadarChart
from Custom_Widgets.QCustomScatterChart import QCustomScatterChart
from Custom_Widgets.QCustomFunnelChart import QCustomFunnelChart
from Custom_Widgets.QCustomRangeBarChart import QCustomRangeBarChart
from Custom_Widgets.QCustomRadialBars import QCustomRadialBars
from Custom_Widgets.QCustomRadialLines import QCustomRadialLines
from Custom_Widgets.QCustomSankey import QCustomSankey
from Custom_Widgets.QCustomFeaturedIcon import QCustomFeaturedIcon
from Custom_Widgets.QCustomCopyButton import QCustomCopyButton
from Custom_Widgets.QCustomSocialButton import QCustomSocialButton
from Custom_Widgets.QCustomHeaderNav import QCustomHeaderNav
from Custom_Widgets.QCustomNumberCounter import QCustomNumberCounter
from Custom_Widgets.QCustomTypewriterText import QCustomTypewriterText
from Custom_Widgets.QCustomGradientText import QCustomGradientText
from Custom_Widgets.QCustomRainbowButton import QCustomRainbowButton
from Custom_Widgets.QCustomSparklesText import QCustomSparklesText

# Registering QCustomCandlestickChart with error handling
try:
    logInfo("Registering QCustomCandlestickChart")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomCandlestickChart, module=QCustomCandlestickChart.WIDGET_MODULE,
        tool_tip=QCustomCandlestickChart.WIDGET_TOOLTIP,
        xml=QCustomCandlestickChart.WIDGET_DOM_XML,
        icon=_iconFor(QCustomCandlestickChart), group="Charts")
except Exception as e:
    logException(e, message="Error registering QCustomCandlestickChart")

# Registering QCustomRadarChart with error handling
try:
    logInfo("Registering QCustomRadarChart")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomRadarChart, module=QCustomRadarChart.WIDGET_MODULE,
        tool_tip=QCustomRadarChart.WIDGET_TOOLTIP,
        xml=QCustomRadarChart.WIDGET_DOM_XML,
        icon=_iconFor(QCustomRadarChart), group="Charts")
except Exception as e:
    logException(e, message="Error registering QCustomRadarChart")

# Registering QCustomScatterChart with error handling
try:
    logInfo("Registering QCustomScatterChart")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomScatterChart, module=QCustomScatterChart.WIDGET_MODULE,
        tool_tip=QCustomScatterChart.WIDGET_TOOLTIP,
        xml=QCustomScatterChart.WIDGET_DOM_XML,
        icon=_iconFor(QCustomScatterChart), group="Charts")
except Exception as e:
    logException(e, message="Error registering QCustomScatterChart")

# Registering QCustomFunnelChart with error handling
try:
    logInfo("Registering QCustomFunnelChart")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomFunnelChart, module=QCustomFunnelChart.WIDGET_MODULE,
        tool_tip=QCustomFunnelChart.WIDGET_TOOLTIP,
        xml=QCustomFunnelChart.WIDGET_DOM_XML,
        icon=_iconFor(QCustomFunnelChart), group="Charts")
except Exception as e:
    logException(e, message="Error registering QCustomFunnelChart")

# Registering QCustomRangeBarChart with error handling
try:
    logInfo("Registering QCustomRangeBarChart")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomRangeBarChart, module=QCustomRangeBarChart.WIDGET_MODULE,
        tool_tip=QCustomRangeBarChart.WIDGET_TOOLTIP,
        xml=QCustomRangeBarChart.WIDGET_DOM_XML,
        icon=_iconFor(QCustomRangeBarChart), group="Charts")
except Exception as e:
    logException(e, message="Error registering QCustomRangeBarChart")

# Registering QCustomRadialBars with error handling
try:
    logInfo("Registering QCustomRadialBars")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomRadialBars, module=QCustomRadialBars.WIDGET_MODULE,
        tool_tip=QCustomRadialBars.WIDGET_TOOLTIP,
        xml=QCustomRadialBars.WIDGET_DOM_XML,
        icon=_iconFor(QCustomRadialBars), group="Charts")
except Exception as e:
    logException(e, message="Error registering QCustomRadialBars")

# Registering QCustomRadialLines with error handling
try:
    logInfo("Registering QCustomRadialLines")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomRadialLines, module=QCustomRadialLines.WIDGET_MODULE,
        tool_tip=QCustomRadialLines.WIDGET_TOOLTIP,
        xml=QCustomRadialLines.WIDGET_DOM_XML,
        icon=_iconFor(QCustomRadialLines), group="Charts")
except Exception as e:
    logException(e, message="Error registering QCustomRadialLines")

# Registering QCustomSankey with error handling
try:
    logInfo("Registering QCustomSankey")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomSankey, module=QCustomSankey.WIDGET_MODULE,
        tool_tip=QCustomSankey.WIDGET_TOOLTIP,
        xml=QCustomSankey.WIDGET_DOM_XML,
        icon=_iconFor(QCustomSankey), group="Charts")
except Exception as e:
    logException(e, message="Error registering QCustomSankey")

# Registering QCustomFeaturedIcon with error handling
try:
    logInfo("Registering QCustomFeaturedIcon")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomFeaturedIcon, module=QCustomFeaturedIcon.WIDGET_MODULE,
        tool_tip=QCustomFeaturedIcon.WIDGET_TOOLTIP,
        xml=QCustomFeaturedIcon.WIDGET_DOM_XML,
        icon=_iconFor(QCustomFeaturedIcon), group="Display Widgets")
except Exception as e:
    logException(e, message="Error registering QCustomFeaturedIcon")

# Registering QCustomCopyButton with error handling
try:
    logInfo("Registering QCustomCopyButton")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomCopyButton, module=QCustomCopyButton.WIDGET_MODULE,
        tool_tip=QCustomCopyButton.WIDGET_TOOLTIP,
        xml=QCustomCopyButton.WIDGET_DOM_XML,
        icon=_iconFor(QCustomCopyButton), group="Buttons")
except Exception as e:
    logException(e, message="Error registering QCustomCopyButton")

# Registering QCustomSocialButton with error handling
try:
    logInfo("Registering QCustomSocialButton")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomSocialButton, module=QCustomSocialButton.WIDGET_MODULE,
        tool_tip=QCustomSocialButton.WIDGET_TOOLTIP,
        xml=QCustomSocialButton.WIDGET_DOM_XML,
        icon=_iconFor(QCustomSocialButton), group="Buttons")
except Exception as e:
    logException(e, message="Error registering QCustomSocialButton")

# Registering QCustomHeaderNav with error handling
try:
    logInfo("Registering QCustomHeaderNav")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomHeaderNav, module=QCustomHeaderNav.WIDGET_MODULE,
        tool_tip=QCustomHeaderNav.WIDGET_TOOLTIP,
        xml=QCustomHeaderNav.WIDGET_DOM_XML,
        icon=_iconFor(QCustomHeaderNav), group="Navigation")
except Exception as e:
    logException(e, message="Error registering QCustomHeaderNav")

# Registering QCustomNumberCounter with error handling
try:
    logInfo("Registering QCustomNumberCounter")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomNumberCounter, module=QCustomNumberCounter.WIDGET_MODULE,
        tool_tip=QCustomNumberCounter.WIDGET_TOOLTIP,
        xml=QCustomNumberCounter.WIDGET_DOM_XML,
        icon=_iconFor(QCustomNumberCounter), group="Display Widgets")
except Exception as e:
    logException(e, message="Error registering QCustomNumberCounter")

# Registering QCustomTypewriterText with error handling
try:
    logInfo("Registering QCustomTypewriterText")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomTypewriterText, module=QCustomTypewriterText.WIDGET_MODULE,
        tool_tip=QCustomTypewriterText.WIDGET_TOOLTIP,
        xml=QCustomTypewriterText.WIDGET_DOM_XML,
        icon=_iconFor(QCustomTypewriterText), group="Display Widgets")
except Exception as e:
    logException(e, message="Error registering QCustomTypewriterText")

# Registering QCustomGradientText with error handling
try:
    logInfo("Registering QCustomGradientText")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomGradientText, module=QCustomGradientText.WIDGET_MODULE,
        tool_tip=QCustomGradientText.WIDGET_TOOLTIP,
        xml=QCustomGradientText.WIDGET_DOM_XML,
        icon=_iconFor(QCustomGradientText), group="Display Widgets")
except Exception as e:
    logException(e, message="Error registering QCustomGradientText")

# Registering QCustomRainbowButton with error handling
try:
    logInfo("Registering QCustomRainbowButton")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomRainbowButton, module=QCustomRainbowButton.WIDGET_MODULE,
        tool_tip=QCustomRainbowButton.WIDGET_TOOLTIP,
        xml=QCustomRainbowButton.WIDGET_DOM_XML,
        icon=_iconFor(QCustomRainbowButton), group="Buttons")
except Exception as e:
    logException(e, message="Error registering QCustomRainbowButton")

# Registering QCustomSparklesText with error handling
try:
    logInfo("Registering QCustomSparklesText")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomSparklesText, module=QCustomSparklesText.WIDGET_MODULE,
        tool_tip=QCustomSparklesText.WIDGET_TOOLTIP,
        xml=QCustomSparklesText.WIDGET_DOM_XML,
        icon=_iconFor(QCustomSparklesText), group="Display Widgets")
except Exception as e:
    logException(e, message="Error registering QCustomSparklesText")


from Custom_Widgets.QCustomAgendaList import QCustomAgendaList

# Registering QCustomAgendaList with error handling
try:
    logInfo("Registering QCustomAgendaList")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomAgendaList, module=QCustomAgendaList.WIDGET_MODULE,
        tool_tip=QCustomAgendaList.WIDGET_TOOLTIP, xml=QCustomAgendaList.WIDGET_DOM_XML,
        icon=_iconFor(QCustomAgendaList), group="Display Widgets")
except Exception as e:
    logException(e, message="Error registering QCustomAgendaList")


from Custom_Widgets.QCustomWaveform import QCustomWaveform

# Registering QCustomWaveform with error handling
try:
    logInfo("Registering QCustomWaveform")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomWaveform, module=QCustomWaveform.WIDGET_MODULE,
        tool_tip=QCustomWaveform.WIDGET_TOOLTIP, xml=QCustomWaveform.WIDGET_DOM_XML,
        icon=_iconFor(QCustomWaveform), group="Charts")
except Exception as e:
    logException(e, message="Error registering QCustomWaveform")


from Custom_Widgets.QCustomDateRangePicker import QCustomDateRangePicker

# Registering QCustomDateRangePicker with error handling
try:
    logInfo("Registering QCustomDateRangePicker")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomDateRangePicker, module=QCustomDateRangePicker.WIDGET_MODULE,
        tool_tip=QCustomDateRangePicker.WIDGET_TOOLTIP, xml=QCustomDateRangePicker.WIDGET_DOM_XML,
        icon=_iconFor(QCustomDateRangePicker), group="Input Widgets")
except Exception as e:
    logException(e, message="Error registering QCustomDateRangePicker")


from Custom_Widgets.QCustomRulerPicker import QCustomRulerPicker

# Registering QCustomRulerPicker with error handling
try:
    logInfo("Registering QCustomRulerPicker")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomRulerPicker, module=QCustomRulerPicker.WIDGET_MODULE,
        tool_tip=QCustomRulerPicker.WIDGET_TOOLTIP, xml=QCustomRulerPicker.WIDGET_DOM_XML,
        icon=_iconFor(QCustomRulerPicker), group="Input Widgets")
except Exception as e:
    logException(e, message="Error registering QCustomRulerPicker")


from Custom_Widgets.QCustomLiquidGauge import QCustomLiquidGauge

# Registering QCustomLiquidGauge with error handling
try:
    logInfo("Registering QCustomLiquidGauge")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomLiquidGauge, module=QCustomLiquidGauge.WIDGET_MODULE,
        tool_tip=QCustomLiquidGauge.WIDGET_TOOLTIP, xml=QCustomLiquidGauge.WIDGET_DOM_XML,
        icon=_iconFor(QCustomLiquidGauge), group="Progressbars")
except Exception as e:
    logException(e, message="Error registering QCustomLiquidGauge")


from Custom_Widgets.QCustomHeatmap import QCustomHeatmap

# Registering QCustomHeatmap with error handling
try:
    logInfo("Registering QCustomHeatmap")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomHeatmap, module=QCustomHeatmap.WIDGET_MODULE,
        tool_tip=QCustomHeatmap.WIDGET_TOOLTIP, xml=QCustomHeatmap.WIDGET_DOM_XML,
        icon=_iconFor(QCustomHeatmap), group="Charts")
except Exception as e:
    logException(e, message="Error registering QCustomHeatmap")


from Custom_Widgets.QCustomRadialGauge import QCustomRadialGauge

# Registering QCustomRadialGauge with error handling
try:
    logInfo("Registering QCustomRadialGauge")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomRadialGauge, module=QCustomRadialGauge.WIDGET_MODULE,
        tool_tip=QCustomRadialGauge.WIDGET_TOOLTIP, xml=QCustomRadialGauge.WIDGET_DOM_XML,
        icon=_iconFor(QCustomRadialGauge), group="Progressbars")
except Exception as e:
    logException(e, message="Error registering QCustomRadialGauge")


from Custom_Widgets.QCustomListRow import QCustomListRow

# Registering QCustomListRow with error handling
try:
    logInfo("Registering QCustomListRow")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomListRow, module=QCustomListRow.WIDGET_MODULE,
        tool_tip=QCustomListRow.WIDGET_TOOLTIP, xml=QCustomListRow.WIDGET_DOM_XML,
        icon=_iconFor(QCustomListRow), group="Display Widgets")
except Exception as e:
    logException(e, message="Error registering QCustomListRow")


from Custom_Widgets.QCustomAvatar import QCustomAvatar

# Registering QCustomAvatar with error handling
try:
    logInfo("Registering QCustomAvatar")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomAvatar, module=QCustomAvatar.WIDGET_MODULE,
        tool_tip=QCustomAvatar.WIDGET_TOOLTIP, xml=QCustomAvatar.WIDGET_DOM_XML,
        icon=_iconFor(QCustomAvatar), group="Display Widgets")
except Exception as e:
    logException(e, message="Error registering QCustomAvatar")


from Custom_Widgets.QCustomTrendChip import QCustomTrendChip

# Registering QCustomTrendChip with error handling
try:
    logInfo("Registering QCustomTrendChip")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomTrendChip, module=QCustomTrendChip.WIDGET_MODULE,
        tool_tip=QCustomTrendChip.WIDGET_TOOLTIP, xml=QCustomTrendChip.WIDGET_DOM_XML,
        icon=_iconFor(QCustomTrendChip), group="Charts")
except Exception as e:
    logException(e, message="Error registering QCustomTrendChip")


from Custom_Widgets.QCustomPageDots import QCustomPageDots

# Registering QCustomPageDots with error handling
try:
    logInfo("Registering QCustomPageDots")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomPageDots, module=QCustomPageDots.WIDGET_MODULE,
        tool_tip=QCustomPageDots.WIDGET_TOOLTIP, xml=QCustomPageDots.WIDGET_DOM_XML,
        icon=_iconFor(QCustomPageDots), group="Navigation")
except Exception as e:
    logException(e, message="Error registering QCustomPageDots")


from Custom_Widgets.QCustomChatListItem import QCustomChatListItem

# Registering QCustomChatListItem with error handling
try:
    logInfo("Registering QCustomChatListItem")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomChatListItem, module=QCustomChatListItem.WIDGET_MODULE,
        tool_tip=QCustomChatListItem.WIDGET_TOOLTIP, xml=QCustomChatListItem.WIDGET_DOM_XML,
        icon=_iconFor(QCustomChatListItem), group="Display Widgets")
except Exception as e:
    logException(e, message="Error registering QCustomChatListItem")


from Custom_Widgets.QCustomChatBubble import QCustomChatBubble

# Registering QCustomChatBubble with error handling
try:
    logInfo("Registering QCustomChatBubble")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomChatBubble, module=QCustomChatBubble.WIDGET_MODULE,
        tool_tip=QCustomChatBubble.WIDGET_TOOLTIP, xml=QCustomChatBubble.WIDGET_DOM_XML,
        icon=_iconFor(QCustomChatBubble), group="Display Widgets")
except Exception as e:
    logException(e, message="Error registering QCustomChatBubble")


from Custom_Widgets.QCustomVoiceMessage import QCustomVoiceMessage

# Registering QCustomVoiceMessage with error handling
try:
    logInfo("Registering QCustomVoiceMessage")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomVoiceMessage, module=QCustomVoiceMessage.WIDGET_MODULE,
        tool_tip=QCustomVoiceMessage.WIDGET_TOOLTIP, xml=QCustomVoiceMessage.WIDGET_DOM_XML,
        icon=_iconFor(QCustomVoiceMessage), group="Display Widgets")
except Exception as e:
    logException(e, message="Error registering QCustomVoiceMessage")


# ---- Chat / messaging component widgets (normalization batch) ------------- #
def _register_widget(cls, group):
    try:
        logInfo("Registering %s" % cls.__name__)
        QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
            cls, module=cls.WIDGET_MODULE, tool_tip=cls.WIDGET_TOOLTIP,
            xml=cls.WIDGET_DOM_XML, icon=_iconFor(cls), group=group)
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
        icon=_iconFor(QCustomCoverCard), group="Media")
except Exception as e:
    logException(e, message="Error registering QCustomCoverCard")


from Custom_Widgets.QCustomCoverFlow import QCustomCoverFlow

# Registering QCustomCoverFlow with error handling
try:
    logInfo("Registering QCustomCoverFlow")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomCoverFlow, module=QCustomCoverFlow.WIDGET_MODULE,
        tool_tip=QCustomCoverFlow.WIDGET_TOOLTIP, xml=QCustomCoverFlow.WIDGET_DOM_XML,
        icon=_iconFor(QCustomCoverFlow), group="Media")
except Exception as e:
    logException(e, message="Error registering QCustomCoverFlow")


from Custom_Widgets.QCustomPlayerBar import QCustomPlayerBar

# Registering QCustomPlayerBar with error handling
try:
    logInfo("Registering QCustomPlayerBar")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomPlayerBar, module=QCustomPlayerBar.WIDGET_MODULE,
        tool_tip=QCustomPlayerBar.WIDGET_TOOLTIP, xml=QCustomPlayerBar.WIDGET_DOM_XML,
        icon=_iconFor(QCustomPlayerBar), group="Media")
except Exception as e:
    logException(e, message="Error registering QCustomPlayerBar")


from Custom_Widgets.QCustomNodeGraph import QCustomNodeGraph

# Registering QCustomNodeGraph with error handling
try:
    logInfo("Registering QCustomNodeGraph")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomNodeGraph, module=QCustomNodeGraph.WIDGET_MODULE,
        tool_tip=QCustomNodeGraph.WIDGET_TOOLTIP, xml=QCustomNodeGraph.WIDGET_DOM_XML,
        icon=_iconFor(QCustomNodeGraph), group="Containers")
except Exception as e:
    logException(e, message="Error registering QCustomNodeGraph")


from Custom_Widgets.QCustomMediaTimeline import QCustomMediaTimeline

# Registering QCustomMediaTimeline with error handling
try:
    logInfo("Registering QCustomMediaTimeline")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomMediaTimeline, module=QCustomMediaTimeline.WIDGET_MODULE,
        tool_tip=QCustomMediaTimeline.WIDGET_TOOLTIP, xml=QCustomMediaTimeline.WIDGET_DOM_XML,
        icon=_iconFor(QCustomMediaTimeline), group="Media")
except Exception as e:
    logException(e, message="Error registering QCustomMediaTimeline")


from Custom_Widgets.QCustomQLabel import QCustomQLabel

# Registering QCustomQLabel with error handling
try:
    logInfo("Registering QCustomQLabel")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomQLabel, module=QCustomQLabel.WIDGET_MODULE,
        tool_tip=QCustomQLabel.WIDGET_TOOLTIP, xml=QCustomQLabel.WIDGET_DOM_XML,
        icon=_iconFor(QCustomQLabel), group="Display Widgets")
except Exception as e:
    logException(e, message="Error registering QCustomQLabel")


from Custom_Widgets.QCustomGlassFrame import QCustomGlassFrame

# Registering QCustomGlassFrame with error handling
try:
    logInfo("Registering QCustomGlassFrame")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomGlassFrame, module=QCustomGlassFrame.WIDGET_MODULE,
        tool_tip=QCustomGlassFrame.WIDGET_TOOLTIP, xml=QCustomGlassFrame.WIDGET_DOM_XML,
        icon=_iconFor(QCustomGlassFrame), group="Containers", container=True)
except Exception as e:
    logException(e, message="Error registering QCustomGlassFrame")


from Custom_Widgets.QCustomWallpaper import QCustomWallpaper

# Registering QCustomWallpaper with error handling
try:
    logInfo("Registering QCustomWallpaper")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomWallpaper, module=QCustomWallpaper.WIDGET_MODULE,
        tool_tip=QCustomWallpaper.WIDGET_TOOLTIP, xml=QCustomWallpaper.WIDGET_DOM_XML,
        icon=_iconFor(QCustomWallpaper), group="Display Widgets")
except Exception as e:
    logException(e, message="Error registering QCustomWallpaper")


from Custom_Widgets.QCustomClockLabel import QCustomClockLabel

# Registering QCustomClockLabel with error handling
try:
    logInfo("Registering QCustomClockLabel")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomClockLabel, module=QCustomClockLabel.WIDGET_MODULE,
        tool_tip=QCustomClockLabel.WIDGET_TOOLTIP, xml=QCustomClockLabel.WIDGET_DOM_XML,
        icon=_iconFor(QCustomClockLabel), group="Display Widgets")
except Exception as e:
    logException(e, message="Error registering QCustomClockLabel")


########################################################################
## Widgets that already declared the full Designer contract
## (WIDGET_MODULE / WIDGET_TOOLTIP / WIDGET_DOM_XML / WIDGET_ICON) but were
## never actually registered here, so they could not be dropped onto a form —
## a silent violation of the project rule that every widget is authorable in
## Qt Designer. Each is instantiable from a bare parent, which is all Designer
## gives a custom widget.
########################################################################

from Custom_Widgets.QCustomInput import QCustomInput

try:
    logInfo("Registering QCustomInput")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomInput, module=QCustomInput.WIDGET_MODULE,
        tool_tip=QCustomInput.WIDGET_TOOLTIP, xml=QCustomInput.WIDGET_DOM_XML,
        icon=_iconFor(QCustomInput), group="Input Widgets")
except Exception as e:
    logException(e, message="Error registering QCustomInput")


from Custom_Widgets.QCustomButtonGroup import QCustomButtonGroup

try:
    logInfo("Registering QCustomButtonGroup")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomButtonGroup, module=QCustomButtonGroup.WIDGET_MODULE,
        tool_tip=QCustomButtonGroup.WIDGET_TOOLTIP,
        xml=QCustomButtonGroup.WIDGET_DOM_XML,
        icon=_iconFor(QCustomButtonGroup), group="Buttons")
except Exception as e:
    logException(e, message="Error registering QCustomButtonGroup")


from Custom_Widgets.QCustomDonut import QCustomDonut

try:
    logInfo("Registering QCustomDonut")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomDonut, module=QCustomDonut.WIDGET_MODULE,
        tool_tip=QCustomDonut.WIDGET_TOOLTIP, xml=QCustomDonut.WIDGET_DOM_XML,
        icon=_iconFor(QCustomDonut), group="Charts")
except Exception as e:
    logException(e, message="Error registering QCustomDonut")


from Custom_Widgets.QCustomSparkline import QCustomSparkline

try:
    logInfo("Registering QCustomSparkline")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomSparkline, module=QCustomSparkline.WIDGET_MODULE,
        tool_tip=QCustomSparkline.WIDGET_TOOLTIP,
        xml=QCustomSparkline.WIDGET_DOM_XML,
        icon=_iconFor(QCustomSparkline), group="Charts")
except Exception as e:
    logException(e, message="Error registering QCustomSparkline")


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


########################################################################
## Widgets that had no Designer contract at all, so they could not be placed
## on a form despite the project rule that every widget is authorable in Qt
## Designer. Each declares WIDGET_MODULE / WIDGET_TOOLTIP / WIDGET_DOM_XML in
## its own module and instantiates from a bare parent.
##
## No icon= argument: 44 of the already-registered widgets point WIDGET_ICON at
## files that do not exist, so they show nothing in the palette anyway. Adding
## 16 more broken paths would grow that problem; Designer's default icon is the
## honest fallback until real icons are drawn.
########################################################################

from Custom_Widgets.QCustom3CirclesLoader import QCustom3CirclesLoader

try:
    logInfo("Registering QCustom3CirclesLoader")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustom3CirclesLoader, module=QCustom3CirclesLoader.WIDGET_MODULE,
        tool_tip=QCustom3CirclesLoader.WIDGET_TOOLTIP, xml=QCustom3CirclesLoader.WIDGET_DOM_XML,
        group="Progressbars")
except Exception as e:
    logException(e, message="Error registering QCustom3CirclesLoader")

from Custom_Widgets.QCustomArcLoader import QCustomArcLoader

try:
    logInfo("Registering QCustomArcLoader")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomArcLoader, module=QCustomArcLoader.WIDGET_MODULE,
        tool_tip=QCustomArcLoader.WIDGET_TOOLTIP, xml=QCustomArcLoader.WIDGET_DOM_XML,
        group="Progressbars")
except Exception as e:
    logException(e, message="Error registering QCustomArcLoader")

# QCustomPerlinLoader needs the optional [loaders] extra: its __init__ raises
# ImportError without perlin_noise (QCustomPerlinLoader.py:72-75), so an
# unconditional registration would make a bare Designer drag fail on every
# machine that only installed the base package. Gate on availability.
try:
    import perlin_noise  # noqa: F401
    _perlin_available = True
except ImportError:
    _perlin_available = False

if _perlin_available:
    from Custom_Widgets.QCustomPerlinLoader import QCustomPerlinLoader

    try:
        logInfo("Registering QCustomPerlinLoader")
        QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
            QCustomPerlinLoader, module=QCustomPerlinLoader.WIDGET_MODULE,
            tool_tip=QCustomPerlinLoader.WIDGET_TOOLTIP, xml=QCustomPerlinLoader.WIDGET_DOM_XML,
            group="Progressbars")
    except Exception as e:
        logException(e, message="Error registering QCustomPerlinLoader")

# Two loader widgets (spinner + multi-step flow bar) are NOT Designer-registered:
# their __init__ first positional argument is not a parent (lineWidth, and the
# step-detail list respectively), so Designer's `createWidget(parent)` binds the
# parent to that slot and leaves the widget unparented and misconfigured. They
# are waived in the tiering manifest for the same reason as the anchored popups.

from Custom_Widgets.QCustomProgressIndicator import QCustomProgressIndicator

try:
    logInfo("Registering QCustomProgressIndicator")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomProgressIndicator, module=QCustomProgressIndicator.WIDGET_MODULE,
        tool_tip=QCustomProgressIndicator.WIDGET_TOOLTIP, xml=QCustomProgressIndicator.WIDGET_DOM_XML,
        group="Progressbars")
except Exception as e:
    logException(e, message="Error registering QCustomProgressIndicator")

from Custom_Widgets.QCustomQSlider import QCustomQSlider

try:
    logInfo("Registering QCustomQSlider")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomQSlider, module=QCustomQSlider.WIDGET_MODULE,
        tool_tip=QCustomQSlider.WIDGET_TOOLTIP, xml=QCustomQSlider.WIDGET_DOM_XML,
        group="Input Widgets")
except Exception as e:
    logException(e, message="Error registering QCustomQSlider")

from Custom_Widgets.QCustomTagEdit import QTagEdit

try:
    logInfo("Registering QTagEdit")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QTagEdit, module=QTagEdit.WIDGET_MODULE,
        tool_tip=QTagEdit.WIDGET_TOOLTIP, xml=QTagEdit.WIDGET_DOM_XML,
        group="Input Widgets")
except Exception as e:
    logException(e, message="Error registering QTagEdit")

from Custom_Widgets.QCustomForm import QCustomForm

try:
    logInfo("Registering QCustomForm")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomForm, module=QCustomForm.WIDGET_MODULE,
        tool_tip=QCustomForm.WIDGET_TOOLTIP, xml=QCustomForm.WIDGET_DOM_XML,
        group="Input Widgets")
except Exception as e:
    logException(e, message="Error registering QCustomForm")


from Custom_Widgets.QCustomQPushButtonGroup import QCustomQPushButtonGroup

try:
    logInfo("Registering QCustomQPushButtonGroup")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomQPushButtonGroup, module=QCustomQPushButtonGroup.WIDGET_MODULE,
        tool_tip=QCustomQPushButtonGroup.WIDGET_TOOLTIP, xml=QCustomQPushButtonGroup.WIDGET_DOM_XML,
        group="Buttons")
except Exception as e:
    logException(e, message="Error registering QCustomQPushButtonGroup")

from Custom_Widgets.QCustomCommandPalette import QCustomCommandPalette

try:
    logInfo("Registering QCustomCommandPalette")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomCommandPalette, module=QCustomCommandPalette.WIDGET_MODULE,
        tool_tip=QCustomCommandPalette.WIDGET_TOOLTIP, xml=QCustomCommandPalette.WIDGET_DOM_XML,
        group="Navigation")
except Exception as e:
    logException(e, message="Error registering QCustomCommandPalette")

from Custom_Widgets.QCustomDrawer import QCustomDrawer

try:
    logInfo("Registering QCustomDrawer")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomDrawer, module=QCustomDrawer.WIDGET_MODULE,
        tool_tip=QCustomDrawer.WIDGET_TOOLTIP, xml=QCustomDrawer.WIDGET_DOM_XML,
        group="Navigation")
except Exception as e:
    logException(e, message="Error registering QCustomDrawer")

from Custom_Widgets.QCustomSlideMenu import QCustomSlideMenu

try:
    logInfo("Registering QCustomSlideMenu")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomSlideMenu, module=QCustomSlideMenu.WIDGET_MODULE,
        tool_tip=QCustomSlideMenu.WIDGET_TOOLTIP, xml=QCustomSlideMenu.WIDGET_DOM_XML,
        group="Navigation")
except Exception as e:
    logException(e, message="Error registering QCustomSlideMenu")

from Custom_Widgets.QCustomEmbeddedWindow import QCustomEmbeddedWindow

try:
    logInfo("Registering QCustomEmbeddedWindow")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomEmbeddedWindow, module=QCustomEmbeddedWindow.WIDGET_MODULE,
        tool_tip=QCustomEmbeddedWindow.WIDGET_TOOLTIP, xml=QCustomEmbeddedWindow.WIDGET_DOM_XML,
        group="Containers")
except Exception as e:
    logException(e, message="Error registering QCustomEmbeddedWindow")

from Custom_Widgets.QCustomCodeEditor import QCustomCodeEditor

try:
    logInfo("Registering QCustomCodeEditor")
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomCodeEditor, module=QCustomCodeEditor.WIDGET_MODULE,
        tool_tip=QCustomCodeEditor.WIDGET_TOOLTIP, xml=QCustomCodeEditor.WIDGET_DOM_XML,
        group="Input Widgets")
except Exception as e:
    logException(e, message="Error registering QCustomCodeEditor")
