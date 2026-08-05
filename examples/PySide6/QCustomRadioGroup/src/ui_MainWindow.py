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
from PySide6.QtWidgets import (QApplication, QFrame, QLabel, QMainWindow,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

from Custom_Widgets.QCustomRadioGroup import QCustomRadioGroup
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(500, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.mainLayout = QVBoxLayout(self.centralwidget)
        self.mainLayout.setSpacing(18)
        self.mainLayout.setObjectName(u"mainLayout")
        self.mainLayout.setContentsMargins(24, 24, 24, 24)
        self.planCard = QFrame(self.centralwidget)
        self.planCard.setObjectName(u"planCard")
        self.planCard.setFrameShape(QFrame.StyledPanel)
        self.planCardLayout = QVBoxLayout(self.planCard)
        self.planCardLayout.setObjectName(u"planCardLayout")
        self.planGroup = QCustomRadioGroup(self.planCard)
        self.planGroup.setObjectName(u"planGroup")
        self.planGroup.setProperty(u"optionsCsv", u"free=Community - free forever,pro=Pro - $12/month,studio=Studio - $29/month")
        self.planGroup.setProperty(u"selectedValue", u"free")
        self.planGroup.setProperty(u"title", u"Choose a plan")

        self.planCardLayout.addWidget(self.planGroup)


        self.mainLayout.addWidget(self.planCard)

        self.billingCard = QFrame(self.centralwidget)
        self.billingCard.setObjectName(u"billingCard")
        self.billingCard.setFrameShape(QFrame.StyledPanel)
        self.billingCardLayout = QVBoxLayout(self.billingCard)
        self.billingCardLayout.setObjectName(u"billingCardLayout")
        self.billingGroup = QCustomRadioGroup(self.billingCard)
        self.billingGroup.setObjectName(u"billingGroup")
        self.billingGroup.setProperty(u"optionsCsv", u"monthly=Monthly,yearly=Yearly")
        self.billingGroup.setProperty(u"selectedValue", u"monthly")
        self.billingGroup.setProperty(u"orientation", u"horizontal")
        self.billingGroup.setProperty(u"title", u"Billing period")

        self.billingCardLayout.addWidget(self.billingGroup)


        self.mainLayout.addWidget(self.billingCard)

        self.seatsCard = QFrame(self.centralwidget)
        self.seatsCard.setObjectName(u"seatsCard")
        self.seatsCard.setFrameShape(QFrame.StyledPanel)
        self.seatsCardLayout = QVBoxLayout(self.seatsCard)
        self.seatsCardLayout.setSpacing(12)
        self.seatsCardLayout.setObjectName(u"seatsCardLayout")
        self.seatsGroup = QCustomRadioGroup(self.seatsCard)
        self.seatsGroup.setObjectName(u"seatsGroup")
        self.seatsGroup.setProperty(u"optionsCsv", u"1,2,5")
        self.seatsGroup.setProperty(u"selectedValue", u"2")
        self.seatsGroup.setProperty(u"orientation", u"horizontal")
        self.seatsGroup.setProperty(u"title", u"Seats")

        self.seatsCardLayout.addWidget(self.seatsGroup)

        self.swapButton = QPushButton(self.seatsCard)
        self.swapButton.setObjectName(u"swapButton")
        self.swapButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.seatsCardLayout.addWidget(self.swapButton)


        self.mainLayout.addWidget(self.seatsCard)

        self.mainSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.mainLayout.addItem(self.mainSpacer)

        self.statusLabel = QLabel(self.centralwidget)
        self.statusLabel.setObjectName(u"statusLabel")

        self.mainLayout.addWidget(self.statusLabel)

        self.themeButton = QPushButton(self.centralwidget)
        self.themeButton.setObjectName(u"themeButton")
        self.themeButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.mainLayout.addWidget(self.themeButton)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"QCustomRadioGroup", None))
        self.swapButton.setText(QCoreApplication.translate("MainWindow", u"Replace seat options with 2, 5, 10", None))
        self.statusLabel.setText(QCoreApplication.translate("MainWindow", u"plan=free  billing=monthly", None))
        self.themeButton.setText(QCoreApplication.translate("MainWindow", u"Toggle light / dark", None))
    # retranslateUi

