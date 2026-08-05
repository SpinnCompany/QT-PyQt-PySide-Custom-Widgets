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
    QPushButton, QSizePolicy, QSlider, QSpacerItem,
    QVBoxLayout, QWidget)

from Custom_Widgets.QCustomGradientText import QCustomGradientText
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(620, 320)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.mainLayout = QVBoxLayout(self.centralwidget)
        self.mainLayout.setSpacing(16)
        self.mainLayout.setObjectName(u"mainLayout")
        self.mainLayout.setContentsMargins(24, 24, 24, 24)
        self.headlineBuild = QCustomGradientText(self.centralwidget)
        self.headlineBuild.setObjectName(u"headlineBuild")

        self.mainLayout.addWidget(self.headlineBuild)

        self.headlineShip = QCustomGradientText(self.centralwidget)
        self.headlineShip.setObjectName(u"headlineShip")

        self.mainLayout.addWidget(self.headlineShip)

        self.headlineZero = QCustomGradientText(self.centralwidget)
        self.headlineZero.setObjectName(u"headlineZero")

        self.mainLayout.addWidget(self.headlineZero)

        self.controlsRow = QHBoxLayout()
        self.controlsRow.setSpacing(8)
        self.controlsRow.setObjectName(u"controlsRow")
        self.angleCaption = QLabel(self.centralwidget)
        self.angleCaption.setObjectName(u"angleCaption")

        self.controlsRow.addWidget(self.angleCaption)

        self.angleSlider = QSlider(self.centralwidget)
        self.angleSlider.setObjectName(u"angleSlider")
        self.angleSlider.setMaximum(359)
        self.angleSlider.setOrientation(Qt.Horizontal)

        self.controlsRow.addWidget(self.angleSlider)

        self.animateBtn = QPushButton(self.centralwidget)
        self.animateBtn.setObjectName(u"animateBtn")

        self.controlsRow.addWidget(self.animateBtn)

        self.themeBtn = QPushButton(self.centralwidget)
        self.themeBtn.setObjectName(u"themeBtn")

        self.controlsRow.addWidget(self.themeBtn)

        self.controlsSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.controlsRow.addItem(self.controlsSpacer)

        self.controlsRow.setStretch(1, 1)

        self.mainLayout.addLayout(self.controlsRow)

        self.bottomSpacer = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.mainLayout.addItem(self.bottomSpacer)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"QCustomGradientText", None))
        self.headlineBuild.setProperty(u"text", QCoreApplication.translate("MainWindow", u"Build something great", None))
        self.headlineShip.setProperty(u"text", QCoreApplication.translate("MainWindow", u"Ship it today", None))
        self.headlineZero.setProperty(u"text", QCoreApplication.translate("MainWindow", u"Zero to one", None))
        self.angleCaption.setText(QCoreApplication.translate("MainWindow", u"Angle", None))
        self.animateBtn.setText(QCoreApplication.translate("MainWindow", u"Animate", None))
        self.themeBtn.setText(QCoreApplication.translate("MainWindow", u"Light / dark", None))
    # retranslateUi

