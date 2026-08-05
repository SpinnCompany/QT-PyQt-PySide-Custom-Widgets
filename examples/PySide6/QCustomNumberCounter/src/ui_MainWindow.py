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

from Custom_Widgets.QCustomNumberCounter import QCustomNumberCounter
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(560, 300)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(16)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(24, 24, 24, 24)
        self.usersHeading = QLabel(self.centralwidget)
        self.usersHeading.setObjectName(u"usersHeading")
        font = QFont()
        font.setBold(True)
        self.usersHeading.setFont(font)

        self.verticalLayout.addWidget(self.usersHeading)

        self.usersCounter = QCustomNumberCounter(self.centralwidget)
        self.usersCounter.setObjectName(u"usersCounter")
        self.usersCounter.setProperty(u"fontScale", 1.800000000000000)

        self.verticalLayout.addWidget(self.usersCounter)

        self.revenueHeading = QLabel(self.centralwidget)
        self.revenueHeading.setObjectName(u"revenueHeading")
        self.revenueHeading.setFont(font)

        self.verticalLayout.addWidget(self.revenueHeading)

        self.revenueCounter = QCustomNumberCounter(self.centralwidget)
        self.revenueCounter.setObjectName(u"revenueCounter")
        self.revenueCounter.setProperty(u"decimals", 2)
        self.revenueCounter.setProperty(u"fontScale", 1.800000000000000)

        self.verticalLayout.addWidget(self.revenueCounter)

        self.uptimeHeading = QLabel(self.centralwidget)
        self.uptimeHeading.setObjectName(u"uptimeHeading")
        self.uptimeHeading.setFont(font)

        self.verticalLayout.addWidget(self.uptimeHeading)

        self.uptimeCounter = QCustomNumberCounter(self.centralwidget)
        self.uptimeCounter.setObjectName(u"uptimeCounter")
        self.uptimeCounter.setProperty(u"decimals", 1)
        self.uptimeCounter.setProperty(u"fontScale", 1.800000000000000)

        self.verticalLayout.addWidget(self.uptimeCounter)

        self.controlsRow = QHBoxLayout()
        self.controlsRow.setObjectName(u"controlsRow")
        self.countUpButton = QPushButton(self.centralwidget)
        self.countUpButton.setObjectName(u"countUpButton")

        self.controlsRow.addWidget(self.countUpButton)

        self.differentButton = QPushButton(self.centralwidget)
        self.differentButton.setObjectName(u"differentButton")

        self.controlsRow.addWidget(self.differentButton)

        self.resetButton = QPushButton(self.centralwidget)
        self.resetButton.setObjectName(u"resetButton")

        self.controlsRow.addWidget(self.resetButton)

        self.themeButton = QPushButton(self.centralwidget)
        self.themeButton.setObjectName(u"themeButton")

        self.controlsRow.addWidget(self.themeButton)

        self.controlsSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.controlsRow.addItem(self.controlsSpacer)


        self.verticalLayout.addLayout(self.controlsRow)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"QCustomNumberCounter", None))
        self.usersHeading.setText(QCoreApplication.translate("MainWindow", u"Users", None))
        self.usersCounter.setProperty(u"suffix", QCoreApplication.translate("MainWindow", u"+", None))
        self.usersCounter.setProperty(u"alignment", QCoreApplication.translate("MainWindow", u"left", None))
        self.revenueHeading.setText(QCoreApplication.translate("MainWindow", u"Revenue", None))
        self.revenueCounter.setProperty(u"prefix", QCoreApplication.translate("MainWindow", u"$", None))
        self.revenueCounter.setProperty(u"alignment", QCoreApplication.translate("MainWindow", u"left", None))
        self.uptimeHeading.setText(QCoreApplication.translate("MainWindow", u"Uptime", None))
        self.uptimeCounter.setProperty(u"suffix", QCoreApplication.translate("MainWindow", u"%", None))
        self.uptimeCounter.setProperty(u"alignment", QCoreApplication.translate("MainWindow", u"left", None))
        self.countUpButton.setText(QCoreApplication.translate("MainWindow", u"Count up", None))
        self.differentButton.setText(QCoreApplication.translate("MainWindow", u"Different", None))
        self.resetButton.setText(QCoreApplication.translate("MainWindow", u"Reset", None))
        self.themeButton.setText(QCoreApplication.translate("MainWindow", u"Light / dark", None))
    # retranslateUi

