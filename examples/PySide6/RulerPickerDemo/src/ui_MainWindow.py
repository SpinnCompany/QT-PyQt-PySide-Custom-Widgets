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
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QHBoxLayout,
    QLabel, QMainWindow, QPushButton, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

from Custom_Widgets.QCustomRulerPicker import QCustomRulerPicker
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(940, 620)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.mainGrid = QGridLayout(self.centralwidget)
        self.mainGrid.setObjectName(u"mainGrid")
        self.mainGrid.setHorizontalSpacing(20)
        self.mainGrid.setVerticalSpacing(20)
        self.mainGrid.setContentsMargins(24, 24, 24, 24)
        self.weightCard = QFrame(self.centralwidget)
        self.weightCard.setObjectName(u"weightCard")
        self.weightCard.setFrameShape(QFrame.StyledPanel)
        self.weightCardLayout = QVBoxLayout(self.weightCard)
        self.weightCardLayout.setSpacing(4)
        self.weightCardLayout.setObjectName(u"weightCardLayout")
        self.weightCardLayout.setContentsMargins(20, 16, 20, 16)
        self.weightCardHeader = QHBoxLayout()
        self.weightCardHeader.setObjectName(u"weightCardHeader")
        self.weightCardTitle = QLabel(self.weightCard)
        self.weightCardTitle.setObjectName(u"weightCardTitle")

        self.weightCardHeader.addWidget(self.weightCardTitle)

        self.weightCardHeaderSpacer = QSpacerItem(10, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.weightCardHeader.addItem(self.weightCardHeaderSpacer)

        self.weightValue = QLabel(self.weightCard)
        self.weightValue.setObjectName(u"weightValue")

        self.weightCardHeader.addWidget(self.weightValue)

        self.weightUnit = QLabel(self.weightCard)
        self.weightUnit.setObjectName(u"weightUnit")

        self.weightCardHeader.addWidget(self.weightUnit)


        self.weightCardLayout.addLayout(self.weightCardHeader)

        self.weightCardSpacer = QSpacerItem(0, 6, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.weightCardLayout.addItem(self.weightCardSpacer)

        self.weightRuler = QCustomRulerPicker(self.weightCard)
        self.weightRuler.setObjectName(u"weightRuler")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.weightRuler.sizePolicy().hasHeightForWidth())
        self.weightRuler.setSizePolicy(sizePolicy)
        self.weightRuler.setProperty(u"minimum", 40.000000000000000)
        self.weightRuler.setProperty(u"maximum", 120.000000000000000)
        self.weightRuler.setProperty(u"step", 1.000000000000000)
        self.weightRuler.setProperty(u"value", 65.000000000000000)
        self.weightRuler.setProperty(u"majorEvery", 5)

        self.weightCardLayout.addWidget(self.weightRuler)

        self.weightCardLayout.setStretch(2, 1)

        self.mainGrid.addWidget(self.weightCard, 0, 0, 1, 2)

        self.heightCard = QFrame(self.centralwidget)
        self.heightCard.setObjectName(u"heightCard")
        self.heightCard.setFrameShape(QFrame.StyledPanel)
        self.heightCardLayout = QVBoxLayout(self.heightCard)
        self.heightCardLayout.setSpacing(4)
        self.heightCardLayout.setObjectName(u"heightCardLayout")
        self.heightCardLayout.setContentsMargins(20, 16, 20, 16)
        self.heightCardHeader = QHBoxLayout()
        self.heightCardHeader.setObjectName(u"heightCardHeader")
        self.heightCardTitle = QLabel(self.heightCard)
        self.heightCardTitle.setObjectName(u"heightCardTitle")

        self.heightCardHeader.addWidget(self.heightCardTitle)

        self.heightCardHeaderSpacer = QSpacerItem(10, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.heightCardHeader.addItem(self.heightCardHeaderSpacer)


        self.heightCardLayout.addLayout(self.heightCardHeader)

        self.heightCardSpacer = QSpacerItem(0, 6, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.heightCardLayout.addItem(self.heightCardSpacer)

        self.heightRuler = QCustomRulerPicker(self.heightCard)
        self.heightRuler.setObjectName(u"heightRuler")
        sizePolicy.setHeightForWidth(self.heightRuler.sizePolicy().hasHeightForWidth())
        self.heightRuler.setSizePolicy(sizePolicy)
        self.heightRuler.setProperty(u"minimum", 120.000000000000000)
        self.heightRuler.setProperty(u"maximum", 210.000000000000000)
        self.heightRuler.setProperty(u"step", 1.000000000000000)
        self.heightRuler.setProperty(u"value", 178.000000000000000)
        self.heightRuler.setProperty(u"centered", True)
        self.heightRuler.setProperty(u"tickSpacing", 10.000000000000000)
        self.heightRuler.setProperty(u"majorEvery", 5)
        self.heightRuler.setProperty(u"showValue", True)

        self.heightCardLayout.addWidget(self.heightRuler)

        self.heightCardLayout.setStretch(2, 1)

        self.mainGrid.addWidget(self.heightCard, 1, 0, 1, 1)

        self.bodyFatCard = QFrame(self.centralwidget)
        self.bodyFatCard.setObjectName(u"bodyFatCard")
        self.bodyFatCard.setFrameShape(QFrame.StyledPanel)
        self.bodyFatCardLayout = QVBoxLayout(self.bodyFatCard)
        self.bodyFatCardLayout.setSpacing(4)
        self.bodyFatCardLayout.setObjectName(u"bodyFatCardLayout")
        self.bodyFatCardLayout.setContentsMargins(20, 16, 20, 16)
        self.bodyFatCardHeader = QHBoxLayout()
        self.bodyFatCardHeader.setObjectName(u"bodyFatCardHeader")
        self.bodyFatCardTitle = QLabel(self.bodyFatCard)
        self.bodyFatCardTitle.setObjectName(u"bodyFatCardTitle")

        self.bodyFatCardHeader.addWidget(self.bodyFatCardTitle)

        self.bodyFatCardHeaderSpacer = QSpacerItem(10, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.bodyFatCardHeader.addItem(self.bodyFatCardHeaderSpacer)


        self.bodyFatCardLayout.addLayout(self.bodyFatCardHeader)

        self.bodyFatCardSpacer = QSpacerItem(0, 6, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.bodyFatCardLayout.addItem(self.bodyFatCardSpacer)

        self.bodyFatRuler = QCustomRulerPicker(self.bodyFatCard)
        self.bodyFatRuler.setObjectName(u"bodyFatRuler")
        sizePolicy.setHeightForWidth(self.bodyFatRuler.sizePolicy().hasHeightForWidth())
        self.bodyFatRuler.setSizePolicy(sizePolicy)
        self.bodyFatRuler.setProperty(u"minimum", 5.000000000000000)
        self.bodyFatRuler.setProperty(u"maximum", 40.000000000000000)
        self.bodyFatRuler.setProperty(u"step", 0.500000000000000)
        self.bodyFatRuler.setProperty(u"value", 18.500000000000000)
        self.bodyFatRuler.setProperty(u"majorEvery", 10)
        self.bodyFatRuler.setProperty(u"showValue", True)

        self.bodyFatCardLayout.addWidget(self.bodyFatRuler)

        self.bodyFatCardLayout.setStretch(2, 1)

        self.mainGrid.addWidget(self.bodyFatCard, 1, 1, 1, 1)

        self.thermoCard = QFrame(self.centralwidget)
        self.thermoCard.setObjectName(u"thermoCard")
        self.thermoCard.setFrameShape(QFrame.StyledPanel)
        self.thermoCardLayout = QVBoxLayout(self.thermoCard)
        self.thermoCardLayout.setSpacing(4)
        self.thermoCardLayout.setObjectName(u"thermoCardLayout")
        self.thermoCardLayout.setContentsMargins(20, 16, 20, 16)
        self.thermoCardHeader = QHBoxLayout()
        self.thermoCardHeader.setObjectName(u"thermoCardHeader")
        self.thermoCardTitle = QLabel(self.thermoCard)
        self.thermoCardTitle.setObjectName(u"thermoCardTitle")

        self.thermoCardHeader.addWidget(self.thermoCardTitle)

        self.thermoCardHeaderSpacer = QSpacerItem(10, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.thermoCardHeader.addItem(self.thermoCardHeaderSpacer)


        self.thermoCardLayout.addLayout(self.thermoCardHeader)

        self.thermoCardSpacer = QSpacerItem(0, 6, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.thermoCardLayout.addItem(self.thermoCardSpacer)

        self.thermoRuler = QCustomRulerPicker(self.thermoCard)
        self.thermoRuler.setObjectName(u"thermoRuler")
        sizePolicy.setHeightForWidth(self.thermoRuler.sizePolicy().hasHeightForWidth())
        self.thermoRuler.setSizePolicy(sizePolicy)
        self.thermoRuler.setProperty(u"minimum", 16.000000000000000)
        self.thermoRuler.setProperty(u"maximum", 30.000000000000000)
        self.thermoRuler.setProperty(u"step", 1.000000000000000)
        self.thermoRuler.setProperty(u"value", 22.000000000000000)
        self.thermoRuler.setProperty(u"majorEvery", 2)
        self.thermoRuler.setProperty(u"showValue", True)

        self.thermoCardLayout.addWidget(self.thermoRuler)

        self.thermoCardLayout.setStretch(2, 1)

        self.mainGrid.addWidget(self.thermoCard, 0, 2, 2, 1)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"QCustomRulerPicker \u2014 Demo", None))
        self.weightCardTitle.setText(QCoreApplication.translate("MainWindow", u"Weight", None))
        self.weightValue.setText(QCoreApplication.translate("MainWindow", u"65", None))
        self.weightUnit.setText(QCoreApplication.translate("MainWindow", u"Kg", None))
        self.heightCardTitle.setText(QCoreApplication.translate("MainWindow", u"Height", None))
        self.heightRuler.setProperty(u"unit", QCoreApplication.translate("MainWindow", u"cm", None))
        self.bodyFatCardTitle.setText(QCoreApplication.translate("MainWindow", u"Body fat", None))
        self.bodyFatRuler.setProperty(u"unit", QCoreApplication.translate("MainWindow", u"%", None))
        self.thermoCardTitle.setText(QCoreApplication.translate("MainWindow", u"Thermostat", None))
        self.thermoRuler.setProperty(u"orientation", QCoreApplication.translate("MainWindow", u"vertical", None))
        self.thermoRuler.setProperty(u"unit", QCoreApplication.translate("MainWindow", u"\u00b0C", None))
    # retranslateUi

