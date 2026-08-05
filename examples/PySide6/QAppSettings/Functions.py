########################################################################
## App functions for the QAppSettings demo.
##
## The point of this example is PERSISTENCE: everything the user does here
## (register, login, theme choice) is written to QSettings under the
## organization/application names declared in json-styles/style.json, so it
## survives a restart. The original tutorial validated the app id/key against
## a remote server; this offline version generates and validates the session
## locally so the demo runs deterministically anywhere.
##
## Styling note: no inline style or icon calls in here. Validation errors
## flip a `state` property that Qss/scss/defaultStyle.scss styles, and the
## eye buttons swap their icon the same way.
########################################################################
import uuid
from datetime import datetime, timedelta

from qtpy.QtCore import QSettings
from qtpy.QtWidgets import QLineEdit, QMessageBox


def _repolish(widget):
    """Re-evaluate the style sheet after a dynamic property change."""
    widget.style().unpolish(widget)
    widget.style().polish(widget)
    widget.update()


def _setResponse(label, text, error=False):
    """Show a form response; `state=error` is styled in defaultStyle.scss."""
    label.setText(text)
    label.setProperty("state", "error" if error else "")
    _repolish(label)


def _togglePasswordEcho(lineEdit, button):
    """Flip echo mode; the button's `state` property swaps the eye icon."""
    hidden = lineEdit.echoMode() == QLineEdit.EchoMode.Password
    lineEdit.setEchoMode(QLineEdit.EchoMode.Normal if hidden
                         else QLineEdit.EchoMode.Password)
    button.setProperty("state", "visible" if hidden else "")
    _repolish(button)


class AppFunctions():
    def __init__(self, arg):
        super(AppFunctions, self).__init__()
        self.arg = arg

    #######################################################################
    # LOGIN FORM VALIDATION
    #######################################################################
    def login(self):
        if len(self.ui.loginUsername.text()) > 3:
            if len(self.ui.loginPassword.text()) < 2:
                _setResponse(self.ui.loginResponse,
                             "Please enter a valid password", error=True)
            else:
                _setResponse(self.ui.loginResponse, "Please wait...")
                AppFunctions.loginUser(self)
        else:
            _setResponse(self.ui.loginResponse,
                         "Please enter a valid username", error=True)

    #######################################################################
    # LOGIN: create/refresh the locally stored app session
    #######################################################################
    def loginUser(self):
        username = self.ui.loginUsername.text()
        try:
            id, key = AppFunctions.getAppIdKey(self)
            if not id or not key:
                # First login on this machine: mint a local app id/key pair
                # (the remote tutorial got these from the server).
                id = uuid.uuid4().hex[:8].upper()
                key = uuid.uuid4().hex
            AppFunctions.createNewAppKey(self, id, key, username)
            _setResponse(self.ui.loginResponse, "Logged in")
            AppFunctions.checkAppKey(self)
        except Exception as e:
            self.ui.mainPages.setCurrentWidget(self.ui.networkErrorPage)
            AppFunctions.showPopUpError(
                self, "The app session could not be created.", e)

    #######################################################################
    # SHOW / HIDE PASSWORDS
    #######################################################################
    def showHideLoginPassword(self):
        _togglePasswordEcho(self.ui.loginPassword, self.ui.showHideLoginPass)

    def showHideSignupPassword(self):
        _togglePasswordEcho(self.ui.signup_password,
                            self.ui.show_hide_signup_password)

    def showHideSignupConfPassword(self):
        _togglePasswordEcho(self.ui.signup_conf_password,
                            self.ui.show_hide_signup_conf_password)

    #######################################################################
    # REGISTRATION FORM VALIDATION
    #######################################################################
    def register(self):
        if len(self.ui.signup_username.text()) > 3:
            if len(self.ui.signup_password.text()) < 4:
                _setResponse(self.ui.registerResponse,
                             "Please enter a valid password. "
                             "Minimum password length is 4", error=True)
            else:
                if self.ui.signup_password.text() == \
                        self.ui.signup_conf_password.text():
                    _setResponse(self.ui.registerResponse, "Please wait...")
                    AppFunctions.registerUser(self)
                else:
                    _setResponse(self.ui.registerResponse,
                                 "Passwords not matching, please check "
                                 "your password.", error=True)
        else:
            _setResponse(self.ui.registerResponse,
                         "Please enter a valid username", error=True)

    #######################################################################
    # REGISTER: mint and store a new local app session
    #######################################################################
    def registerUser(self):
        username = self.ui.signup_username.text()
        try:
            id = uuid.uuid4().hex[:8].upper()
            key = uuid.uuid4().hex
            AppFunctions.createNewAppKey(self, id, key, username)
            _setResponse(self.ui.registerResponse, "Account created")
            AppFunctions.checkAppKey(self)
        except Exception as e:
            self.ui.mainPages.setCurrentWidget(self.ui.networkErrorPage)
            AppFunctions.showPopUpError(
                self, "The app session could not be created.", e)

    #######################################################################
    # SAVE APP DETAILS (QSettings — the persistence this demo teaches)
    #######################################################################
    def createNewAppKey(self, id, key, username=""):
        settings = QSettings()
        settings.setValue("APPID", id)
        settings.setValue("APPKEY", key)
        if username:
            settings.setValue("APPUSER", username)
        expiry = (datetime.now() + timedelta(days=30)).strftime("%d %b %Y")
        settings.setValue("APPKEY-EXPIRY", expiry)

    #######################################################################
    # GET APP KEY AND ID
    #######################################################################
    def getAppIdKey(self):
        settings = QSettings()
        id = settings.value("APPID")
        key = settings.value("APPKEY")
        return id, key

    #######################################################################
    # VALIDATE THE SAVED APP KEY AND ID (local, deterministic)
    #######################################################################
    def checkAppKey(self):
        try:
            id, key = AppFunctions.getAppIdKey(self)

            if not id or not key:
                # Nothing stored yet: ask the user to login/register.
                _setResponse(self.ui.loginResponse,
                             "Please login or register to activate the app")
                self.ui.mainPages.setCurrentWidget(self.ui.loginPage)
                self.ui.userAccountPages.setCurrentWidget(self.ui.loginAccount)
                return

            settings = QSettings()
            username = settings.value("APPUSER") or "user"
            expiry = settings.value("APPKEY-EXPIRY") or "—"

            self.ui.mainPages.setCurrentWidget(self.ui.homePage)
            self.ui.appDetails.setText(
                """
                <html><head/><body>
                <p align="center">
                <span style=" font-weight:600;">Username:</span> %s</p>
                <p align="center"><span style=" font-weight:600;">App ID:</span> %s</p>
                <p align="center"><span style=" font-weight:600;">APP Key:</span> %s</p>
                <p align="center"><span style=" font-weight:600;">Expiry Date:</span> %s</p>
                </body></html>
                """ % (username, id, key, expiry))

            self.ui.userAccountPages.setCurrentWidget(
                self.ui.loggedAccountDetails)
            self.ui.username.setText(str(username))
            self.ui.app_id.setText(str(id))
            self.ui.app_key.setText(str(key))
            self.ui.key_date.setText(str(expiry))

        except Exception as e:
            self.ui.mainPages.setCurrentWidget(self.ui.networkErrorPage)
            AppFunctions.showPopUpError(
                self, "The stored app session could not be read.", e)

    #######################################################################
    # LOGOUT
    #######################################################################
    def logout(self):
        settings = QSettings()
        settings.setValue("APPKEY", "")
        _setResponse(self.ui.loginResponse,
                     "Account logged out. Please login.")
        self.ui.mainPages.setCurrentWidget(self.ui.loginPage)
        self.ui.userAccountPages.setCurrentWidget(self.ui.loginAccount)

    #######################################################################
    # SHOW POPUP MESSAGE (unexpected failures only)
    #######################################################################
    def showPopUpError(self, message, more):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(message)
        msg.setInformativeText(str(more))
        msg.setWindowTitle("Error")
        msg.exec()
