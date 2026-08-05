########################################################################
## QT GUI BY SPINN TV(YOUTUBE)
########################################################################

########################################################################
## IMPORTS
########################################################################
import os
import sys

# Make the app location-independent: the project root is THIS file's
# folder, wherever the app is launched from.
from Custom_Widgets.Project import setProjectRoot
setProjectRoot(__file__)

########################################################################
# IMPORT Custom widgets
# NOTE: the compiled UI class (src/ui_QCustomQMainWindow.py) is imported
# INSIDE build() below, not here - that is what lets hot reload pick up the
# freshly regenerated module every time your .ui changes.
from Custom_Widgets import *
from Custom_Widgets.QAppSettings import QAppSettings
########################################################################

########################################################################
## MAIN WINDOW CLASS
########################################################################
class MainWindow(QCustomMainWindow):
    def __init__(self, parent=None):
        QCustomMainWindow.__init__(self)

        ########################################################################
        # HOT RELOAD
        # enable_hot_reload runs build() once now, then re-runs it in place
        # whenever the compiled Ui_ module changes - no app restart needed.
        # Keep `python main.py` running and, in another terminal, keep the UI
        # watcher running (`Custom_Widgets --monitor-ui ./ui`); editing your
        # .ui in Qt Designer recompiles it and the window rebuilds live.
        ########################################################################
        enable_hot_reload(self, self.build)

    def build(self):
        """(Re)construct the UI and re-connect signals.

        Called by enable_hot_reload on startup and after every change to the
        compiled UI module. Import the Ui_ class HERE (not at module top) so a
        reloaded module is picked up. Window geometry is preserved across
        rebuilds by the hot-reload helper.
        """
        ########################################################################
        # IMPORT GUI FILE (inside build so hot reload sees the fresh module)
        from src.ui_QCustomQMainWindow import Ui_CustomMainWindow
        self.ui = Ui_CustomMainWindow()
        self.ui.setupUi(self)

        ########################################################################
        # APPLY JSON STYLESHEET
        ########################################################################
        # self = QMainWindow class
        # self.ui = Ui_CustomMainWindow / user interface class
        #Use this if you only have one json file named "style.json" inside the root directory, "json" directory or "jsonstyles" folder.
        # loadJsonStyle(self, self.ui)

        # Use this to specify your json file(s) path/name
        loadJsonStyle(self, self.ui, jsonFiles = {
            "json-styles/style.json"
            })

        ########################################################################

        # CONNECT YOUR SIGNALS HERE so they are re-wired on every hot reload,
        # e.g. self.ui.myButton.clicked.connect(self.on_click)

        #######################################################################
        # SHOW WINDOW
        #######################################################################
        self.show()

        ########################################################################
        # UPDATE APP SETTINGS LOADED FROM JSON STYLESHEET
        # ITS IMPORTANT TO RUN THIS AFTER SHOWING THE WINDOW
        # THIS PROCESS WILL RUN ON A SEPARATE THREAD WHEN GENERATING NEW ICONS
        # TO PREVENT THE WINDOW FROM BEING UNRESPONSIVE
        ########################################################################
        # self = QMainWindow class
        QAppSettings.updateAppSettings(self)

        ########################################################################
        # To apply a new theme from your JSon file
        # Import custom wdgets theme engine
        # from Custom_Widgets.QCustomTheme import QCustomTheme

        # init theme engine
        # self.themeEngine = QCustomTheme()

        # check current theme name
        # print(self.themeEngine.theme)

        # set the theme name from json file
        # self.themeEngine.theme = "Default-theme" #or Light, Dark or any custom theme name from the json file
        # self.themeEngine.theme = "Dark"
        # self.themeEngine.theme = "Light"
        ########################################################################


########################################################################
## EXECUTE APP
########################################################################
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ########################################################################
    ## 
    ########################################################################
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
########################################################################
## END===>
########################################################################  
