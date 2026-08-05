# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'new_MainWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.11.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QFrame, QHBoxLayout,
    QLabel, QLineEdit, QMainWindow, QPushButton,
    QSizePolicy, QSpacerItem, QStackedWidget, QVBoxLayout,
    QWidget)

from Custom_Widgets.QCustomQStackedWidget import QCustomQStackedWidget
from Custom_Widgets.QCustomSlideMenu import QCustomSlideMenu
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1000, 640)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralLayout = QVBoxLayout(self.centralwidget)
        self.centralLayout.setSpacing(0)
        self.centralLayout.setObjectName(u"centralLayout")
        self.centralLayout.setContentsMargins(0, 0, 0, 0)
        self.header = QWidget(self.centralwidget)
        self.header.setObjectName(u"header")
        self.headerLayout = QHBoxLayout(self.header)
        self.headerLayout.setObjectName(u"headerLayout")
        self.headerLayout.setContentsMargins(16, 10, 16, 10)
        self.appTitleLabel = QLabel(self.header)
        self.appTitleLabel.setObjectName(u"appTitleLabel")

        self.headerLayout.addWidget(self.appTitleLabel)

        self.headerSpacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.headerLayout.addItem(self.headerSpacer)

        self.helpBtn = QPushButton(self.header)
        self.helpBtn.setObjectName(u"helpBtn")

        self.headerLayout.addWidget(self.helpBtn)

        self.show_hide_exit_prompt = QPushButton(self.header)
        self.show_hide_exit_prompt.setObjectName(u"show_hide_exit_prompt")

        self.headerLayout.addWidget(self.show_hide_exit_prompt)


        self.centralLayout.addWidget(self.header)

        self.exitPrompt = QCustomSlideMenu(self.centralwidget)
        self.exitPrompt.setObjectName(u"exitPrompt")
        self.exitPromptLayout = QHBoxLayout(self.exitPrompt)
        self.exitPromptLayout.setObjectName(u"exitPromptLayout")
        self.exitPromptLayout.setContentsMargins(16, 8, 16, 8)
        self.exitPromptLabel = QLabel(self.exitPrompt)
        self.exitPromptLabel.setObjectName(u"exitPromptLabel")

        self.exitPromptLayout.addWidget(self.exitPromptLabel)

        self.exitPromptSpacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.exitPromptLayout.addItem(self.exitPromptSpacer)

        self.close_exit_prompt = QPushButton(self.exitPrompt)
        self.close_exit_prompt.setObjectName(u"close_exit_prompt")

        self.exitPromptLayout.addWidget(self.close_exit_prompt)

        self.exit = QPushButton(self.exitPrompt)
        self.exit.setObjectName(u"exit")

        self.exitPromptLayout.addWidget(self.exit)


        self.centralLayout.addWidget(self.exitPrompt)

        self.bodyLayout = QHBoxLayout()
        self.bodyLayout.setSpacing(0)
        self.bodyLayout.setObjectName(u"bodyLayout")
        self.mainPages = QCustomQStackedWidget(self.centralwidget)
        self.mainPages.setObjectName(u"mainPages")
        self.loginPage = QWidget()
        self.loginPage.setObjectName(u"loginPage")
        self.loginPageLayout = QVBoxLayout(self.loginPage)
        self.loginPageLayout.setSpacing(12)
        self.loginPageLayout.setObjectName(u"loginPageLayout")
        self.loginPageLayout.setContentsMargins(60, 30, 60, 30)
        self.loginTopSpacer = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.loginPageLayout.addItem(self.loginTopSpacer)

        self.loginCard = QFrame(self.loginPage)
        self.loginCard.setObjectName(u"loginCard")
        self.loginCard.setMinimumSize(QSize(460, 0))
        self.loginCard.setMaximumSize(QSize(560, 16777215))
        self.loginCard.setFrameShape(QFrame.StyledPanel)
        self.loginCardLayout = QVBoxLayout(self.loginCard)
        self.loginCardLayout.setSpacing(10)
        self.loginCardLayout.setObjectName(u"loginCardLayout")
        self.loginCardLayout.setContentsMargins(24, 24, 24, 24)
        self.loginTitle = QLabel(self.loginCard)
        self.loginTitle.setObjectName(u"loginTitle")

        self.loginCardLayout.addWidget(self.loginTitle)

        self.loginResponse = QLabel(self.loginCard)
        self.loginResponse.setObjectName(u"loginResponse")
        self.loginResponse.setWordWrap(True)

        self.loginCardLayout.addWidget(self.loginResponse)

        self.loginUsername = QLineEdit(self.loginCard)
        self.loginUsername.setObjectName(u"loginUsername")

        self.loginCardLayout.addWidget(self.loginUsername)

        self.loginPasswordRow = QHBoxLayout()
        self.loginPasswordRow.setSpacing(6)
        self.loginPasswordRow.setObjectName(u"loginPasswordRow")
        self.loginPassword = QLineEdit(self.loginCard)
        self.loginPassword.setObjectName(u"loginPassword")
        self.loginPassword.setEchoMode(QLineEdit.Password)

        self.loginPasswordRow.addWidget(self.loginPassword)

        self.showHideLoginPass = QPushButton(self.loginCard)
        self.showHideLoginPass.setObjectName(u"showHideLoginPass")
        self.showHideLoginPass.setMaximumSize(QSize(36, 16777215))

        self.loginPasswordRow.addWidget(self.showHideLoginPass)


        self.loginCardLayout.addLayout(self.loginPasswordRow)

        self.submitLogin = QPushButton(self.loginCard)
        self.submitLogin.setObjectName(u"submitLogin")

        self.loginCardLayout.addWidget(self.submitLogin)

        self.loginAltRow = QHBoxLayout()
        self.loginAltRow.setObjectName(u"loginAltRow")
        self.loginAltLabel = QLabel(self.loginCard)
        self.loginAltLabel.setObjectName(u"loginAltLabel")

        self.loginAltRow.addWidget(self.loginAltLabel)

        self.signUpBtn = QPushButton(self.loginCard)
        self.signUpBtn.setObjectName(u"signUpBtn")

        self.loginAltRow.addWidget(self.signUpBtn)

        self.loginAltSpacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.loginAltRow.addItem(self.loginAltSpacer)


        self.loginCardLayout.addLayout(self.loginAltRow)


        self.loginPageLayout.addWidget(self.loginCard, 0, Qt.AlignHCenter)

        self.loginBottomSpacer = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.loginPageLayout.addItem(self.loginBottomSpacer)

        self.mainPages.addWidget(self.loginPage)
        self.signUpPage = QWidget()
        self.signUpPage.setObjectName(u"signUpPage")
        self.signUpPageLayout = QVBoxLayout(self.signUpPage)
        self.signUpPageLayout.setObjectName(u"signUpPageLayout")
        self.signUpPageLayout.setContentsMargins(60, 30, 60, 30)
        self.signupTopSpacer = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.signUpPageLayout.addItem(self.signupTopSpacer)

        self.signupCard = QFrame(self.signUpPage)
        self.signupCard.setObjectName(u"signupCard")
        self.signupCard.setMinimumSize(QSize(460, 0))
        self.signupCard.setMaximumSize(QSize(560, 16777215))
        self.signupCard.setFrameShape(QFrame.StyledPanel)
        self.signupCardLayout = QVBoxLayout(self.signupCard)
        self.signupCardLayout.setSpacing(10)
        self.signupCardLayout.setObjectName(u"signupCardLayout")
        self.signupCardLayout.setContentsMargins(24, 24, 24, 24)
        self.signupTitle = QLabel(self.signupCard)
        self.signupTitle.setObjectName(u"signupTitle")

        self.signupCardLayout.addWidget(self.signupTitle)

        self.registerResponse = QLabel(self.signupCard)
        self.registerResponse.setObjectName(u"registerResponse")
        self.registerResponse.setWordWrap(True)

        self.signupCardLayout.addWidget(self.registerResponse)

        self.signup_username = QLineEdit(self.signupCard)
        self.signup_username.setObjectName(u"signup_username")

        self.signupCardLayout.addWidget(self.signup_username)

        self.signupPasswordRow = QHBoxLayout()
        self.signupPasswordRow.setSpacing(6)
        self.signupPasswordRow.setObjectName(u"signupPasswordRow")
        self.signup_password = QLineEdit(self.signupCard)
        self.signup_password.setObjectName(u"signup_password")
        self.signup_password.setEchoMode(QLineEdit.Password)

        self.signupPasswordRow.addWidget(self.signup_password)

        self.show_hide_signup_password = QPushButton(self.signupCard)
        self.show_hide_signup_password.setObjectName(u"show_hide_signup_password")
        self.show_hide_signup_password.setMaximumSize(QSize(36, 16777215))

        self.signupPasswordRow.addWidget(self.show_hide_signup_password)


        self.signupCardLayout.addLayout(self.signupPasswordRow)

        self.signupConfPasswordRow = QHBoxLayout()
        self.signupConfPasswordRow.setSpacing(6)
        self.signupConfPasswordRow.setObjectName(u"signupConfPasswordRow")
        self.signup_conf_password = QLineEdit(self.signupCard)
        self.signup_conf_password.setObjectName(u"signup_conf_password")
        self.signup_conf_password.setEchoMode(QLineEdit.Password)

        self.signupConfPasswordRow.addWidget(self.signup_conf_password)

        self.show_hide_signup_conf_password = QPushButton(self.signupCard)
        self.show_hide_signup_conf_password.setObjectName(u"show_hide_signup_conf_password")
        self.show_hide_signup_conf_password.setMaximumSize(QSize(36, 16777215))

        self.signupConfPasswordRow.addWidget(self.show_hide_signup_conf_password)


        self.signupCardLayout.addLayout(self.signupConfPasswordRow)

        self.signup_btn = QPushButton(self.signupCard)
        self.signup_btn.setObjectName(u"signup_btn")

        self.signupCardLayout.addWidget(self.signup_btn)

        self.signupAltRow = QHBoxLayout()
        self.signupAltRow.setObjectName(u"signupAltRow")
        self.signupAltLabel = QLabel(self.signupCard)
        self.signupAltLabel.setObjectName(u"signupAltLabel")

        self.signupAltRow.addWidget(self.signupAltLabel)

        self.loginBtn = QPushButton(self.signupCard)
        self.loginBtn.setObjectName(u"loginBtn")

        self.signupAltRow.addWidget(self.loginBtn)

        self.signupAltSpacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.signupAltRow.addItem(self.signupAltSpacer)


        self.signupCardLayout.addLayout(self.signupAltRow)


        self.signUpPageLayout.addWidget(self.signupCard, 0, Qt.AlignHCenter)

        self.signupBottomSpacer = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.signUpPageLayout.addItem(self.signupBottomSpacer)

        self.mainPages.addWidget(self.signUpPage)
        self.homePage = QWidget()
        self.homePage.setObjectName(u"homePage")
        self.homePageLayout = QVBoxLayout(self.homePage)
        self.homePageLayout.setObjectName(u"homePageLayout")
        self.homePageLayout.setContentsMargins(60, 30, 60, 30)
        self.homeTopSpacer = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.homePageLayout.addItem(self.homeTopSpacer)

        self.homeCard = QFrame(self.homePage)
        self.homeCard.setObjectName(u"homeCard")
        self.homeCard.setMinimumSize(QSize(460, 0))
        self.homeCard.setMaximumSize(QSize(560, 16777215))
        self.homeCard.setFrameShape(QFrame.StyledPanel)
        self.homeCardLayout = QVBoxLayout(self.homeCard)
        self.homeCardLayout.setSpacing(12)
        self.homeCardLayout.setObjectName(u"homeCardLayout")
        self.homeCardLayout.setContentsMargins(24, 24, 24, 24)
        self.homeTitle = QLabel(self.homeCard)
        self.homeTitle.setObjectName(u"homeTitle")

        self.homeCardLayout.addWidget(self.homeTitle)

        self.appDetails = QLabel(self.homeCard)
        self.appDetails.setObjectName(u"appDetails")
        self.appDetails.setWordWrap(True)

        self.homeCardLayout.addWidget(self.appDetails)

        self.logoutBtn = QPushButton(self.homeCard)
        self.logoutBtn.setObjectName(u"logoutBtn")

        self.homeCardLayout.addWidget(self.logoutBtn)


        self.homePageLayout.addWidget(self.homeCard, 0, Qt.AlignHCenter)

        self.homeBottomSpacer = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.homePageLayout.addItem(self.homeBottomSpacer)

        self.mainPages.addWidget(self.homePage)
        self.networkErrorPage = QWidget()
        self.networkErrorPage.setObjectName(u"networkErrorPage")
        self.networkErrorLayout = QVBoxLayout(self.networkErrorPage)
        self.networkErrorLayout.setSpacing(12)
        self.networkErrorLayout.setObjectName(u"networkErrorLayout")
        self.networkErrorLayout.setContentsMargins(60, 30, 60, 30)
        self.networkTopSpacer = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.networkErrorLayout.addItem(self.networkTopSpacer)

        self.networkErrorTitle = QLabel(self.networkErrorPage)
        self.networkErrorTitle.setObjectName(u"networkErrorTitle")
        self.networkErrorTitle.setAlignment(Qt.AlignCenter)

        self.networkErrorLayout.addWidget(self.networkErrorTitle)

        self.networkErrorBody = QLabel(self.networkErrorPage)
        self.networkErrorBody.setObjectName(u"networkErrorBody")
        self.networkErrorBody.setAlignment(Qt.AlignCenter)
        self.networkErrorBody.setWordWrap(True)

        self.networkErrorLayout.addWidget(self.networkErrorBody)

        self.tryAgain = QPushButton(self.networkErrorPage)
        self.tryAgain.setObjectName(u"tryAgain")

        self.networkErrorLayout.addWidget(self.tryAgain)

        self.networkBottomSpacer = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.networkErrorLayout.addItem(self.networkBottomSpacer)

        self.mainPages.addWidget(self.networkErrorPage)

        self.bodyLayout.addWidget(self.mainPages)

        self.userAccount = QCustomSlideMenu(self.centralwidget)
        self.userAccount.setObjectName(u"userAccount")
        self.userAccountLayout = QVBoxLayout(self.userAccount)
        self.userAccountLayout.setSpacing(10)
        self.userAccountLayout.setObjectName(u"userAccountLayout")
        self.userAccountLayout.setContentsMargins(14, 14, 14, 14)
        self.accountTitle = QLabel(self.userAccount)
        self.accountTitle.setObjectName(u"accountTitle")

        self.userAccountLayout.addWidget(self.accountTitle)

        self.userAccountPages = QStackedWidget(self.userAccount)
        self.userAccountPages.setObjectName(u"userAccountPages")
        self.loginAccount = QWidget()
        self.loginAccount.setObjectName(u"loginAccount")
        self.loginAccountLayout = QVBoxLayout(self.loginAccount)
        self.loginAccountLayout.setSpacing(8)
        self.loginAccountLayout.setObjectName(u"loginAccountLayout")
        self.accountHintTitle = QLabel(self.loginAccount)
        self.accountHintTitle.setObjectName(u"accountHintTitle")

        self.loginAccountLayout.addWidget(self.accountHintTitle)

        self.accountHintBody = QLabel(self.loginAccount)
        self.accountHintBody.setObjectName(u"accountHintBody")
        self.accountHintBody.setWordWrap(True)

        self.loginAccountLayout.addWidget(self.accountHintBody)

        self.accountHintSpacer = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.loginAccountLayout.addItem(self.accountHintSpacer)

        self.userAccountPages.addWidget(self.loginAccount)
        self.loggedAccountDetails = QWidget()
        self.loggedAccountDetails.setObjectName(u"loggedAccountDetails")
        self.loggedAccountLayout = QVBoxLayout(self.loggedAccountDetails)
        self.loggedAccountLayout.setSpacing(6)
        self.loggedAccountLayout.setObjectName(u"loggedAccountLayout")
        self.usernameCaption = QLabel(self.loggedAccountDetails)
        self.usernameCaption.setObjectName(u"usernameCaption")

        self.loggedAccountLayout.addWidget(self.usernameCaption)

        self.username = QLabel(self.loggedAccountDetails)
        self.username.setObjectName(u"username")

        self.loggedAccountLayout.addWidget(self.username)

        self.appIdCaption = QLabel(self.loggedAccountDetails)
        self.appIdCaption.setObjectName(u"appIdCaption")

        self.loggedAccountLayout.addWidget(self.appIdCaption)

        self.app_id = QLabel(self.loggedAccountDetails)
        self.app_id.setObjectName(u"app_id")

        self.loggedAccountLayout.addWidget(self.app_id)

        self.appKeyCaption = QLabel(self.loggedAccountDetails)
        self.appKeyCaption.setObjectName(u"appKeyCaption")

        self.loggedAccountLayout.addWidget(self.appKeyCaption)

        self.app_key = QLabel(self.loggedAccountDetails)
        self.app_key.setObjectName(u"app_key")
        self.app_key.setWordWrap(True)

        self.loggedAccountLayout.addWidget(self.app_key)

        self.keyDateCaption = QLabel(self.loggedAccountDetails)
        self.keyDateCaption.setObjectName(u"keyDateCaption")

        self.loggedAccountLayout.addWidget(self.keyDateCaption)

        self.key_date = QLabel(self.loggedAccountDetails)
        self.key_date.setObjectName(u"key_date")

        self.loggedAccountLayout.addWidget(self.key_date)

        self.loggedAccountSpacer = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.loggedAccountLayout.addItem(self.loggedAccountSpacer)

        self.logoutUser = QPushButton(self.loggedAccountDetails)
        self.logoutUser.setObjectName(u"logoutUser")

        self.loggedAccountLayout.addWidget(self.logoutUser)

        self.userAccountPages.addWidget(self.loggedAccountDetails)

        self.userAccountLayout.addWidget(self.userAccountPages)


        self.bodyLayout.addWidget(self.userAccount)


        self.centralLayout.addLayout(self.bodyLayout)

        self.footer = QWidget(self.centralwidget)
        self.footer.setObjectName(u"footer")
        self.footerLayout = QHBoxLayout(self.footer)
        self.footerLayout.setSpacing(10)
        self.footerLayout.setObjectName(u"footerLayout")
        self.footerLayout.setContentsMargins(16, 10, 16, 10)
        self.pushButton = QPushButton(self.footer)
        self.pushButton.setObjectName(u"pushButton")

        self.footerLayout.addWidget(self.pushButton)

        self.footerSpacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.footerLayout.addItem(self.footerSpacer)

        self.themeCaption = QLabel(self.footer)
        self.themeCaption.setObjectName(u"themeCaption")

        self.footerLayout.addWidget(self.themeCaption)

        self.checkBox = QCheckBox(self.footer)
        self.checkBox.setObjectName(u"checkBox")

        self.footerLayout.addWidget(self.checkBox)

        self.show_hide_user_account = QPushButton(self.footer)
        self.show_hide_user_account.setObjectName(u"show_hide_user_account")

        self.footerLayout.addWidget(self.show_hide_user_account)


        self.centralLayout.addWidget(self.footer)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.mainPages.setCurrentIndex(0)
        self.userAccountPages.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"QAppSettings \u2014 Theme & Session Persistence", None))
        self.appTitleLabel.setText(QCoreApplication.translate("MainWindow", u"QT Settings Session", None))
        self.helpBtn.setText(QCoreApplication.translate("MainWindow", u"Help", None))
        self.show_hide_exit_prompt.setText(QCoreApplication.translate("MainWindow", u"Exit app", None))
        self.exitPromptLabel.setText(QCoreApplication.translate("MainWindow", u"Do you really want to exit the app?", None))
        self.close_exit_prompt.setText(QCoreApplication.translate("MainWindow", u"Cancel", None))
        self.exit.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
        self.loginTitle.setText(QCoreApplication.translate("MainWindow", u"Login", None))
        self.loginResponse.setText(QCoreApplication.translate("MainWindow", u"Please login or register to activate the app", None))
        self.loginUsername.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Username", None))
        self.loginPassword.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Password", None))
        self.showHideLoginPass.setText("")
        self.submitLogin.setText(QCoreApplication.translate("MainWindow", u"Login", None))
        self.loginAltLabel.setText(QCoreApplication.translate("MainWindow", u"No account yet?", None))
        self.signUpBtn.setText(QCoreApplication.translate("MainWindow", u"Create account", None))
        self.signupTitle.setText(QCoreApplication.translate("MainWindow", u"Create your account", None))
        self.registerResponse.setText(QCoreApplication.translate("MainWindow", u"Register to generate your app id and key", None))
        self.signup_username.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Username", None))
        self.signup_password.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Password", None))
        self.show_hide_signup_password.setText("")
        self.signup_conf_password.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Confirm password", None))
        self.show_hide_signup_conf_password.setText("")
        self.signup_btn.setText(QCoreApplication.translate("MainWindow", u"Register", None))
        self.signupAltLabel.setText(QCoreApplication.translate("MainWindow", u"Already registered?", None))
        self.loginBtn.setText(QCoreApplication.translate("MainWindow", u"Back to login", None))
        self.homeTitle.setText(QCoreApplication.translate("MainWindow", u"App session active", None))
        self.appDetails.setText(QCoreApplication.translate("MainWindow", u"Your app details will appear here.", None))
        self.logoutBtn.setText(QCoreApplication.translate("MainWindow", u"Logout", None))
        self.networkErrorTitle.setText(QCoreApplication.translate("MainWindow", u"Something went wrong", None))
        self.networkErrorBody.setText(QCoreApplication.translate("MainWindow", u"The app session could not be verified. Please try again.", None))
        self.tryAgain.setText(QCoreApplication.translate("MainWindow", u"Try again", None))
        self.accountTitle.setText(QCoreApplication.translate("MainWindow", u"My Account", None))
        self.accountHintTitle.setText(QCoreApplication.translate("MainWindow", u"Not logged in", None))
        self.accountHintBody.setText(QCoreApplication.translate("MainWindow", u"Login or register to view your stored app session.", None))
        self.usernameCaption.setText(QCoreApplication.translate("MainWindow", u"Username", None))
        self.username.setText(QCoreApplication.translate("MainWindow", u"\u2014", None))
        self.appIdCaption.setText(QCoreApplication.translate("MainWindow", u"App ID", None))
        self.app_id.setText(QCoreApplication.translate("MainWindow", u"\u2014", None))
        self.appKeyCaption.setText(QCoreApplication.translate("MainWindow", u"App key", None))
        self.app_key.setText(QCoreApplication.translate("MainWindow", u"\u2014", None))
        self.keyDateCaption.setText(QCoreApplication.translate("MainWindow", u"Expiry date", None))
        self.key_date.setText(QCoreApplication.translate("MainWindow", u"\u2014", None))
        self.logoutUser.setText(QCoreApplication.translate("MainWindow", u"Logout", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Actions", None))
        self.themeCaption.setText(QCoreApplication.translate("MainWindow", u"Dark theme", None))
        self.checkBox.setText("")
        self.show_hide_user_account.setText(QCoreApplication.translate("MainWindow", u"My account", None))
    # retranslateUi

