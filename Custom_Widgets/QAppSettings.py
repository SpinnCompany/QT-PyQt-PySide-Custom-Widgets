########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/spinnTv
# WEBSITE: spinncode.com
########################################################################

########################################################################
## IMPORTS
########################################################################
import os

########################################################################
## MODULE UPDATED TO USE QT.PY
########################################################################
from qtpy.QtCore import QCoreApplication, QSettings

from Custom_Widgets.Log import *

########################################################################
## QT APP SETTINGS
########################################################################
class QAppSettings():
    def __init__(self, parent=None):
        super(QAppSettings, self).__init__(parent)
        ########################################################################
        ## CREATE APP SETTINGS
        ########################################################################

    def updateAppSettings(self, generateIcons: bool = True, reloadJson: bool = True, paintEntireApp: bool = True, QtDesignerMode: bool = False):
        
        if not hasattr(self, "themeEngine"):
            return

        themeEngine = self.themeEngine

        if len(str(themeEngine.organizationName)) > 0:
            QCoreApplication.setOrganizationName(str(themeEngine.organizationName))
        if len(str(themeEngine.applicationName)) > 0:
            QCoreApplication.setApplicationName(str(themeEngine.applicationName))
        if len(str(themeEngine.organizationDomain)) > 0:
            QCoreApplication.setOrganizationDomain(str(themeEngine.organizationDomain))

        settings = QSettings()

        # if theme not set
        init_theme_set = settings.value("INIT-THEME-SET")
        if settings.value("THEME") is None or not init_theme_set:
            for theme in themeEngine.themes:
                if theme.defaultTheme:
                    # update app theme
                    if (init_theme_set is None or not init_theme_set):
                        settings.setValue("THEME", theme.name)
                        settings.setValue("INIT-THEME-SET", True)
                        logInfo(f"Initial theme set... {theme.name}")

        settings.setValue("THEMES-LIST", themeEngine.themes)

        #######################################################################
        # APPLY COMPILED STYLESHEET
        #######################################################################
        if reloadJson:
            themeEngine.reloadJsonStyles(update = False)
            
        themeEngine.applyCompiledSass(generateIcons = generateIcons, paintEntireApp = paintEntireApp)

        #######################################################################
        # DEV: expose this running app to Designer / the MCP for live
        # observe + navigate. No-op unless CUSTOM_WIDGETS_APP_CONTROL is set
        # (the dev server sets it for Run'd apps), so production is untouched.
        #######################################################################
        try:
            from Custom_Widgets.AppControl import maybe_start_app_control
            maybe_start_app_control()
        except Exception as e:
            logDebug(f"App control: not started: {e}")


########################################################################
## END
########################################################################
