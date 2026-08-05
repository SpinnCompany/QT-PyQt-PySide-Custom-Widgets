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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QMainWindow,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

from Custom_Widgets.QCustomAccordion import QCustomAccordion
from Custom_Widgets.QCustomComboBox import QCustomComboBox
from Custom_Widgets.QCustomTabWidget import QCustomTabWidget
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(560, 540)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.rootLayout = QVBoxLayout(self.centralwidget)
        self.rootLayout.setSpacing(16)
        self.rootLayout.setObjectName(u"rootLayout")
        self.rootLayout.setContentsMargins(20, 20, 20, 20)
        self.styleRow = QHBoxLayout()
        self.styleRow.setSpacing(10)
        self.styleRow.setObjectName(u"styleRow")
        self.styleLabel = QLabel(self.centralwidget)
        self.styleLabel.setObjectName(u"styleLabel")

        self.styleRow.addWidget(self.styleLabel)

        self.styleBox = QCustomComboBox(self.centralwidget)
        self.styleBox.addItem("")
        self.styleBox.addItem("")
        self.styleBox.addItem("")
        self.styleBox.setObjectName(u"styleBox")
        self.styleBox.setEditable(False)

        self.styleRow.addWidget(self.styleBox)

        self.styleSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.styleRow.addItem(self.styleSpacer)


        self.rootLayout.addLayout(self.styleRow)

        self.tabs = QCustomTabWidget(self.centralwidget)
        self.tabs.setObjectName(u"tabs")
        self.profilePage = QWidget()
        self.profilePage.setObjectName(u"profilePage")
        self.profileLayout = QVBoxLayout(self.profilePage)
        self.profileLayout.setObjectName(u"profileLayout")
        self.profileLabel = QLabel(self.profilePage)
        self.profileLabel.setObjectName(u"profileLabel")

        self.profileLayout.addWidget(self.profileLabel)

        self.profileSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.profileLayout.addItem(self.profileSpacer)

        self.tabs.addTab(self.profilePage, "")
        self.accountPage = QWidget()
        self.accountPage.setObjectName(u"accountPage")
        self.accountLayout = QVBoxLayout(self.accountPage)
        self.accountLayout.setObjectName(u"accountLayout")
        self.accountLabel = QLabel(self.accountPage)
        self.accountLabel.setObjectName(u"accountLabel")

        self.accountLayout.addWidget(self.accountLabel)

        self.accountSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.accountLayout.addItem(self.accountSpacer)

        self.tabs.addTab(self.accountPage, "")
        self.notificationsPage = QWidget()
        self.notificationsPage.setObjectName(u"notificationsPage")
        self.notificationsLayout = QVBoxLayout(self.notificationsPage)
        self.notificationsLayout.setObjectName(u"notificationsLayout")
        self.notificationsLabel = QLabel(self.notificationsPage)
        self.notificationsLabel.setObjectName(u"notificationsLabel")

        self.notificationsLayout.addWidget(self.notificationsLabel)

        self.notificationsSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.notificationsLayout.addItem(self.notificationsSpacer)

        self.tabs.addTab(self.notificationsPage, "")

        self.rootLayout.addWidget(self.tabs)

        self.accordion = QCustomAccordion(self.centralwidget)
        self.accordion.setObjectName(u"accordion")

        self.rootLayout.addWidget(self.accordion)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.tabs.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"QCustomTabWidget + QCustomAccordion", None))
        self.styleLabel.setText(QCoreApplication.translate("MainWindow", u"Tab style:", None))
        self.styleBox.setItemText(0, QCoreApplication.translate("MainWindow", u"underline", None))
        self.styleBox.setItemText(1, QCoreApplication.translate("MainWindow", u"pills", None))
        self.styleBox.setItemText(2, QCoreApplication.translate("MainWindow", u"enclosed", None))

        self.profileLabel.setText(QCoreApplication.translate("MainWindow", u"Profile settings go here.", None))
        self.tabs.setTabText(self.tabs.indexOf(self.profilePage), QCoreApplication.translate("MainWindow", u"Profile", None))
        self.accountLabel.setText(QCoreApplication.translate("MainWindow", u"Account settings go here.", None))
        self.tabs.setTabText(self.tabs.indexOf(self.accountPage), QCoreApplication.translate("MainWindow", u"Account", None))
        self.notificationsLabel.setText(QCoreApplication.translate("MainWindow", u"Notification settings go here.", None))
        self.tabs.setTabText(self.tabs.indexOf(self.notificationsPage), QCoreApplication.translate("MainWindow", u"Notifications", None))
    # retranslateUi

