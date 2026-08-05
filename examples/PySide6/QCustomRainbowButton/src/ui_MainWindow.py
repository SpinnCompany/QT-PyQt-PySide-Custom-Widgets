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

from Custom_Widgets.QCustomRainbowButton import QCustomRainbowButton
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(560, 340)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.mainLayout = QVBoxLayout(self.centralwidget)
        self.mainLayout.setSpacing(16)
        self.mainLayout.setObjectName(u"mainLayout")
        self.mainLayout.setContentsMargins(24, 24, 24, 24)
        self.startButton = QCustomRainbowButton(self.centralwidget)
        self.startButton.setObjectName(u"startButton")
        self.startButton.setProperty(u"text", u"Get started")

        self.mainLayout.addWidget(self.startButton)

        self.upgradeButton = QCustomRainbowButton(self.centralwidget)
        self.upgradeButton.setObjectName(u"upgradeButton")
        self.upgradeButton.setProperty(u"text", u"Upgrade")
        self.upgradeButton.setProperty(u"filled", True)

        self.mainLayout.addWidget(self.upgradeButton)

        self.glowButton = QCustomRainbowButton(self.centralwidget)
        self.glowButton.setObjectName(u"glowButton")
        self.glowButton.setProperty(u"text", u"Glow")
        self.glowButton.setProperty(u"glow", True)

        self.mainLayout.addWidget(self.glowButton)

        self.statusLabel = QLabel(self.centralwidget)
        self.statusLabel.setObjectName(u"statusLabel")

        self.mainLayout.addWidget(self.statusLabel)

        self.controlsRow = QHBoxLayout()
        self.controlsRow.setSpacing(10)
        self.controlsRow.setObjectName(u"controlsRow")
        self.speedLabel = QLabel(self.centralwidget)
        self.speedLabel.setObjectName(u"speedLabel")

        self.controlsRow.addWidget(self.speedLabel)

        self.speedSlider = QSlider(self.centralwidget)
        self.speedSlider.setObjectName(u"speedSlider")
        self.speedSlider.setMinimum(16)
        self.speedSlider.setMaximum(200)
        self.speedSlider.setValue(40)
        self.speedSlider.setOrientation(Qt.Horizontal)

        self.controlsRow.addWidget(self.speedSlider)

        self.animateButton = QPushButton(self.centralwidget)
        self.animateButton.setObjectName(u"animateButton")
        self.animateButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.controlsRow.addWidget(self.animateButton)

        self.themeButton = QPushButton(self.centralwidget)
        self.themeButton.setObjectName(u"themeButton")
        self.themeButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.controlsRow.addWidget(self.themeButton)

        self.controlsSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.controlsRow.addItem(self.controlsSpacer)


        self.mainLayout.addLayout(self.controlsRow)

        self.mainSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.mainLayout.addItem(self.mainSpacer)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"QCustomRainbowButton", None))
        self.statusLabel.setText(QCoreApplication.translate("MainWindow", u"Click a button", None))
        self.speedLabel.setText(QCoreApplication.translate("MainWindow", u"Speed", None))
        self.animateButton.setText(QCoreApplication.translate("MainWindow", u"Animate", None))
        self.themeButton.setText(QCoreApplication.translate("MainWindow", u"Light / dark", None))
    # retranslateUi

