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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QMainWindow, QPushButton, QSizePolicy, QSlider,
    QSpacerItem, QVBoxLayout, QWidget)

from Custom_Widgets.QCustomGradientText import QCustomGradientText
from Custom_Widgets.QCustomNumberCounter import QCustomNumberCounter
from Custom_Widgets.QCustomProgressRing import QCustomProgressRing
from Custom_Widgets.QCustomRainbowButton import QCustomRainbowButton
from Custom_Widgets.QCustomSparklesText import QCustomSparklesText
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(780, 560)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.mainLayout = QVBoxLayout(self.centralwidget)
        self.mainLayout.setSpacing(16)
        self.mainLayout.setObjectName(u"mainLayout")
        self.mainLayout.setContentsMargins(24, 24, 24, 24)
        self.headerRow = QHBoxLayout()
        self.headerRow.setObjectName(u"headerRow")
        self.titleLabel = QLabel(self.centralwidget)
        self.titleLabel.setObjectName(u"titleLabel")

        self.headerRow.addWidget(self.titleLabel)

        self.headerSpacer = QSpacerItem(10, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.headerRow.addItem(self.headerSpacer)

        self.themeButton = QPushButton(self.centralwidget)
        self.themeButton.setObjectName(u"themeButton")

        self.headerRow.addWidget(self.themeButton)


        self.mainLayout.addLayout(self.headerRow)

        self.gradientCard = QFrame(self.centralwidget)
        self.gradientCard.setObjectName(u"gradientCard")
        self.gradientCard.setFrameShape(QFrame.StyledPanel)
        self.gradientCardLayout = QVBoxLayout(self.gradientCard)
        self.gradientCardLayout.setSpacing(8)
        self.gradientCardLayout.setObjectName(u"gradientCardLayout")
        self.gradientCaption = QLabel(self.gradientCard)
        self.gradientCaption.setObjectName(u"gradientCaption")

        self.gradientCardLayout.addWidget(self.gradientCaption)

        self.gradientText = QCustomGradientText(self.gradientCard)
        self.gradientText.setObjectName(u"gradientText")
        self.gradientText.setProperty(u"animated", True)
        self.gradientText.setProperty(u"fontScale", 1.600000000000000)
        self.gradientText.setProperty(u"bold", True)

        self.gradientCardLayout.addWidget(self.gradientText)


        self.mainLayout.addWidget(self.gradientCard)

        self.sparkleCard = QFrame(self.centralwidget)
        self.sparkleCard.setObjectName(u"sparkleCard")
        self.sparkleCard.setFrameShape(QFrame.StyledPanel)
        self.sparkleCardLayout = QVBoxLayout(self.sparkleCard)
        self.sparkleCardLayout.setSpacing(8)
        self.sparkleCardLayout.setObjectName(u"sparkleCardLayout")
        self.sparkleCaption = QLabel(self.sparkleCard)
        self.sparkleCaption.setObjectName(u"sparkleCaption")

        self.sparkleCardLayout.addWidget(self.sparkleCaption)

        self.sparklesText = QCustomSparklesText(self.sparkleCard)
        self.sparklesText.setObjectName(u"sparklesText")
        self.sparklesText.setProperty(u"fontScale", 1.400000000000000)
        self.sparklesText.setProperty(u"bold", True)

        self.sparkleCardLayout.addWidget(self.sparklesText)


        self.mainLayout.addWidget(self.sparkleCard)

        self.bottomRow = QHBoxLayout()
        self.bottomRow.setSpacing(16)
        self.bottomRow.setObjectName(u"bottomRow")
        self.rainbowCard = QFrame(self.centralwidget)
        self.rainbowCard.setObjectName(u"rainbowCard")
        self.rainbowCard.setFrameShape(QFrame.StyledPanel)
        self.rainbowCardLayout = QVBoxLayout(self.rainbowCard)
        self.rainbowCardLayout.setSpacing(12)
        self.rainbowCardLayout.setObjectName(u"rainbowCardLayout")
        self.rainbowCaption = QLabel(self.rainbowCard)
        self.rainbowCaption.setObjectName(u"rainbowCaption")

        self.rainbowCardLayout.addWidget(self.rainbowCaption)

        self.rainbowButton = QCustomRainbowButton(self.rainbowCard)
        self.rainbowButton.setObjectName(u"rainbowButton")

        self.rainbowCardLayout.addWidget(self.rainbowButton, 0, Qt.AlignLeft)

        self.launchLabel = QLabel(self.rainbowCard)
        self.launchLabel.setObjectName(u"launchLabel")

        self.rainbowCardLayout.addWidget(self.launchLabel)

        self.rainbowSpacer = QSpacerItem(10, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.rainbowCardLayout.addItem(self.rainbowSpacer)


        self.bottomRow.addWidget(self.rainbowCard)

        self.ringCard = QFrame(self.centralwidget)
        self.ringCard.setObjectName(u"ringCard")
        self.ringCard.setFrameShape(QFrame.StyledPanel)
        self.ringCardLayout = QHBoxLayout(self.ringCard)
        self.ringCardLayout.setSpacing(16)
        self.ringCardLayout.setObjectName(u"ringCardLayout")
        self.progressRing = QCustomProgressRing(self.ringCard)
        self.progressRing.setObjectName(u"progressRing")
        self.progressRing.setMinimumSize(QSize(110, 110))

        self.ringCardLayout.addWidget(self.progressRing)

        self.ringSideLayout = QVBoxLayout()
        self.ringSideLayout.setSpacing(8)
        self.ringSideLayout.setObjectName(u"ringSideLayout")
        self.ringCaption = QLabel(self.ringCard)
        self.ringCaption.setObjectName(u"ringCaption")

        self.ringSideLayout.addWidget(self.ringCaption)

        self.numberCounter = QCustomNumberCounter(self.ringCard)
        self.numberCounter.setObjectName(u"numberCounter")
        self.numberCounter.setProperty(u"fontScale", 1.800000000000000)
        self.numberCounter.setProperty(u"bold", True)

        self.ringSideLayout.addWidget(self.numberCounter)

        self.driveSlider = QSlider(self.ringCard)
        self.driveSlider.setObjectName(u"driveSlider")
        self.driveSlider.setMinimum(0)
        self.driveSlider.setMaximum(100)
        self.driveSlider.setValue(64)
        self.driveSlider.setOrientation(Qt.Horizontal)

        self.ringSideLayout.addWidget(self.driveSlider)


        self.ringCardLayout.addLayout(self.ringSideLayout)


        self.bottomRow.addWidget(self.ringCard)


        self.mainLayout.addLayout(self.bottomRow)

        self.bottomSpacer = QSpacerItem(10, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.mainLayout.addItem(self.bottomSpacer)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Prism Showcase", None))
        self.titleLabel.setText(QCoreApplication.translate("MainWindow", u"Prism Showcase", None))
        self.themeButton.setText(QCoreApplication.translate("MainWindow", u"Light / dark", None))
        self.gradientCaption.setText(QCoreApplication.translate("MainWindow", u"QCustomGradientText \u2014 animated hue sweep", None))
        self.gradientText.setProperty(u"text", QCoreApplication.translate("MainWindow", u"Refracting light into colour", None))
        self.sparkleCaption.setText(QCoreApplication.translate("MainWindow", u"QCustomSparklesText \u2014 click it to reseed the sparkles", None))
        self.sparklesText.setProperty(u"text", QCoreApplication.translate("MainWindow", u"Sparkles included", None))
        self.rainbowCaption.setText(QCoreApplication.translate("MainWindow", u"QCustomRainbowButton", None))
        self.rainbowButton.setProperty(u"text", QCoreApplication.translate("MainWindow", u"Get started", None))
        self.launchLabel.setText(QCoreApplication.translate("MainWindow", u"Not launched yet", None))
        self.ringCaption.setText(QCoreApplication.translate("MainWindow", u"QCustomProgressRing + QCustomNumberCounter", None))
        self.numberCounter.setProperty(u"suffix", QCoreApplication.translate("MainWindow", u"%", None))
    # retranslateUi

