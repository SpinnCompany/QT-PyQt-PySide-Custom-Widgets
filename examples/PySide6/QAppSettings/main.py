########################################################################
## QAppSettings example — theme + session persistence with QSettings.
##
## The star of this demo is the QAppSettings workflow:
##   * json-styles/style.json declares the org/app names and two themes
##   * the theme checkbox writes THEME to QSettings and calls
##     QAppSettings.updateAppSettings() to restyle the running app
##   * login/register store an app id/key in QSettings (Functions.py), so
##     both the chosen theme and the session survive a restart
########################################################################
import os
import sys

# Force PySide6 to match compiled ui files
os.environ.setdefault("QT_API", "pyside6")

from Custom_Widgets.Project import setProjectRoot
setProjectRoot(__file__)

from Custom_Widgets import *
from Custom_Widgets.QAppSettings import QAppSettings
from qtpy.QtCore import QCoreApplication, QSettings
from qtpy.QtWidgets import QApplication, QMenu

# App functions
from Functions import AppFunctions


class MainWindow(QCustomMainWindow):
    def __init__(self, parent=None):
        QCustomMainWindow.__init__(self)
        from src.ui_MainWindow import Ui_MainWindow
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        loadJsonStyle(self, self.ui, jsonFiles={"json-styles/style.json"})

        self.show()
        themeEngine = self.themeEngine
        org = getattr(themeEngine, "organizationName", "")
        if org:
            QCoreApplication.setOrganizationName(str(org))
        appn = getattr(themeEngine, "applicationName", "")
        if appn:
            QCoreApplication.setApplicationName(str(appn))
        orgd = getattr(themeEngine, "organizationDomain", "")
        if orgd:
            QCoreApplication.setOrganizationDomain(str(orgd))
        s = QSettings()
        init_set = s.value("INIT-THEME-SET")
        if s.value("THEME") is None or not init_set:
            # Name the app's default theme explicitly: a stale THEME key in the
            # pre-appName fallback QSettings file makes the json loader drop
            # every Default-Theme flag, so relying on the flag alone can leave
            # the app with no theme selected at all.
            target = "Default-Light"
            for t in themeEngine.themes:
                if getattr(t, "defaultTheme", False):
                    target = t.name
                    break
            s.setValue("THEME", target)
            s.setValue("INIT-THEME-SET", True)
        s.setValue("THEMES-LIST", themeEngine.themes)
        themeEngine.reloadJsonStyles(update=False)
        themeEngine.applyCompiledSass(generateIcons=False, paintEntireApp=True)

        from Custom_Widgets.AppControl import maybe_start_app_control
        try:
            maybe_start_app_control()
        except Exception:
            pass

        #######################################################################
        # THEME PERSISTENCE (the QAppSettings workflow)
        #######################################################################
        # Reflect the persisted theme BEFORE wiring the signal, so restoring
        # the checkbox state cannot re-trigger a theme switch during boot.
        currentTheme = QSettings().value("THEME")
        self.ui.checkBox.blockSignals(True)
        self.ui.checkBox.setChecked(currentTheme == "Default-Dark")
        self.ui.checkBox.blockSignals(False)
        self.ui.checkBox.stateChanged.connect(lambda: self.changeAppTheme())

        #######################################################################
        # APPLICATION FUNCTIONS AND EVENTS
        #######################################################################
        # Collapse the exit prompt (its expand toggle is wired via style.json)
        self.ui.close_exit_prompt.clicked.connect(
            lambda: self.ui.exitPrompt.collapseMenu())

        # Show/hide passwords
        self.ui.showHideLoginPass.clicked.connect(
            lambda: AppFunctions.showHideLoginPassword(self))
        self.ui.show_hide_signup_password.clicked.connect(
            lambda: AppFunctions.showHideSignupPassword(self))
        self.ui.show_hide_signup_conf_password.clicked.connect(
            lambda: AppFunctions.showHideSignupConfPassword(self))
        # Submit login details/form
        self.ui.submitLogin.clicked.connect(lambda: AppFunctions.login(self))
        # Submit register details/form
        self.ui.signup_btn.clicked.connect(lambda: AppFunctions.register(self))
        # Logout user
        self.ui.logoutBtn.clicked.connect(lambda: AppFunctions.logout(self))
        self.ui.logoutUser.clicked.connect(lambda: AppFunctions.logout(self))
        # Re-check the stored session (e.g. after an unexpected failure)
        self.ui.tryAgain.clicked.connect(lambda: AppFunctions.checkAppKey(self))
        # Check the stored app session on startup
        AppFunctions.checkAppKey(self)

        # Context menus on plain buttons
        self.menu = QMenu()
        self.menu.addAction("Action One", self.actionOne)
        self.menu.addAction("Action Two", self.actionTwo)
        self.ui.pushButton.setMenu(self.menu)

        self.helpMenu = QMenu()
        self.helpMenu.addAction("Help", self.help)
        self.helpMenu.addAction("About", self.about)
        self.ui.helpBtn.setMenu(self.helpMenu)

    # Menu action handlers
    def actionOne(self):
        print("Action one clicked!")

    def actionTwo(self):
        print("Action two clicked!")

    def help(self):
        print("Should open help page!")

    def about(self):
        print("Should open about page!")

    # Change app theme — persisted via QSettings + QAppSettings
    def changeAppTheme(self):
        settings = QSettings()
        if self.ui.checkBox.isChecked():
            settings.setValue("THEME", "Default-Dark")
        else:
            settings.setValue("THEME", "Default-Light")

        # generateIcons=False: restyle from the compiled sass only (icon
        # regeneration runs threaded workers this small demo doesn't need).
        QAppSettings.updateAppSettings(self, generateIcons=False)


########################################################################
## EXECUTE APP
########################################################################
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
