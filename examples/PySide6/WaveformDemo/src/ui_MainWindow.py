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
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QLabel,
    QMainWindow, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

from Custom_Widgets.QCustomWaveform import QCustomWaveform
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(960, 620)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.mainGrid = QGridLayout(self.centralwidget)
        self.mainGrid.setObjectName(u"mainGrid")
        self.mainGrid.setHorizontalSpacing(20)
        self.mainGrid.setVerticalSpacing(20)
        self.mainGrid.setContentsMargins(24, 24, 24, 24)
        self.ecgCard = QFrame(self.centralwidget)
        self.ecgCard.setObjectName(u"ecgCard")
        self.ecgCard.setFrameShape(QFrame.StyledPanel)
        self.ecgCardLayout = QVBoxLayout(self.ecgCard)
        self.ecgCardLayout.setSpacing(2)
        self.ecgCardLayout.setObjectName(u"ecgCardLayout")
        self.ecgCardLayout.setContentsMargins(20, 16, 20, 16)
        self.ecgCardTitle = QLabel(self.ecgCard)
        self.ecgCardTitle.setObjectName(u"ecgCardTitle")

        self.ecgCardLayout.addWidget(self.ecgCardTitle)

        self.ecgCardSub = QLabel(self.ecgCard)
        self.ecgCardSub.setObjectName(u"ecgCardSub")

        self.ecgCardLayout.addWidget(self.ecgCardSub)

        self.ecgCardSpacer = QSpacerItem(0, 8, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.ecgCardLayout.addItem(self.ecgCardSpacer)

        self.ecgWave = QCustomWaveform(self.ecgCard)
        self.ecgWave.setObjectName(u"ecgWave")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.ecgWave.sizePolicy().hasHeightForWidth())
        self.ecgWave.setSizePolicy(sizePolicy)
        self.ecgWave.setProperty(u"capacity", 90)
        self.ecgWave.setProperty(u"lineWidth", 2.200000000000000)
        self.ecgWave.setProperty(u"showGrid", True)
        self.ecgWave.setProperty(u"animated", True)

        self.ecgCardLayout.addWidget(self.ecgWave)

        self.ecgCardLayout.setStretch(3, 1)

        self.mainGrid.addWidget(self.ecgCard, 0, 0, 1, 1)

        self.waterCard = QFrame(self.centralwidget)
        self.waterCard.setObjectName(u"waterCard")
        self.waterCard.setFrameShape(QFrame.StyledPanel)
        self.waterCardLayout = QVBoxLayout(self.waterCard)
        self.waterCardLayout.setSpacing(2)
        self.waterCardLayout.setObjectName(u"waterCardLayout")
        self.waterCardLayout.setContentsMargins(20, 16, 20, 16)
        self.waterCardTitle = QLabel(self.waterCard)
        self.waterCardTitle.setObjectName(u"waterCardTitle")

        self.waterCardLayout.addWidget(self.waterCardTitle)

        self.waterCardSub = QLabel(self.waterCard)
        self.waterCardSub.setObjectName(u"waterCardSub")

        self.waterCardLayout.addWidget(self.waterCardSub)

        self.waterCardSpacer = QSpacerItem(0, 8, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.waterCardLayout.addItem(self.waterCardSpacer)

        self.waterWave = QCustomWaveform(self.waterCard)
        self.waterWave.setObjectName(u"waterWave")
        sizePolicy.setHeightForWidth(self.waterWave.sizePolicy().hasHeightForWidth())
        self.waterWave.setSizePolicy(sizePolicy)
        self.waterWave.setProperty(u"capacity", 40)
        self.waterWave.setProperty(u"barGap", 3.000000000000000)
        self.waterWave.setProperty(u"cornerRadius", 3)
        self.waterWave.setProperty(u"animated", True)

        self.waterCardLayout.addWidget(self.waterWave)

        self.waterCardLayout.setStretch(3, 1)

        self.mainGrid.addWidget(self.waterCard, 0, 1, 1, 1)

        self.voiceCard = QFrame(self.centralwidget)
        self.voiceCard.setObjectName(u"voiceCard")
        self.voiceCard.setFrameShape(QFrame.StyledPanel)
        self.voiceCardLayout = QVBoxLayout(self.voiceCard)
        self.voiceCardLayout.setSpacing(2)
        self.voiceCardLayout.setObjectName(u"voiceCardLayout")
        self.voiceCardLayout.setContentsMargins(20, 16, 20, 16)
        self.voiceCardTitle = QLabel(self.voiceCard)
        self.voiceCardTitle.setObjectName(u"voiceCardTitle")

        self.voiceCardLayout.addWidget(self.voiceCardTitle)

        self.voiceCardSub = QLabel(self.voiceCard)
        self.voiceCardSub.setObjectName(u"voiceCardSub")

        self.voiceCardLayout.addWidget(self.voiceCardSub)

        self.voiceCardSpacer = QSpacerItem(0, 8, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.voiceCardLayout.addItem(self.voiceCardSpacer)

        self.voiceWave = QCustomWaveform(self.voiceCard)
        self.voiceWave.setObjectName(u"voiceWave")
        sizePolicy.setHeightForWidth(self.voiceWave.sizePolicy().hasHeightForWidth())
        self.voiceWave.setSizePolicy(sizePolicy)
        self.voiceWave.setProperty(u"mirror", True)
        self.voiceWave.setProperty(u"barGap", 4.000000000000000)
        self.voiceWave.setProperty(u"cornerRadius", 4)

        self.voiceCardLayout.addWidget(self.voiceWave)

        self.voiceCardLayout.setStretch(3, 1)

        self.mainGrid.addWidget(self.voiceCard, 1, 0, 1, 1)

        self.neonCard = QFrame(self.centralwidget)
        self.neonCard.setObjectName(u"neonCard")
        self.neonCard.setFrameShape(QFrame.StyledPanel)
        self.neonCardLayout = QVBoxLayout(self.neonCard)
        self.neonCardLayout.setSpacing(2)
        self.neonCardLayout.setObjectName(u"neonCardLayout")
        self.neonCardLayout.setContentsMargins(20, 16, 20, 16)
        self.neonCardTitle = QLabel(self.neonCard)
        self.neonCardTitle.setObjectName(u"neonCardTitle")

        self.neonCardLayout.addWidget(self.neonCardTitle)

        self.neonCardSub = QLabel(self.neonCard)
        self.neonCardSub.setObjectName(u"neonCardSub")

        self.neonCardLayout.addWidget(self.neonCardSub)

        self.neonCardSpacer = QSpacerItem(0, 8, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.neonCardLayout.addItem(self.neonCardSpacer)

        self.neonWave = QCustomWaveform(self.neonCard)
        self.neonWave.setObjectName(u"neonWave")
        sizePolicy.setHeightForWidth(self.neonWave.sizePolicy().hasHeightForWidth())
        self.neonWave.setSizePolicy(sizePolicy)
        self.neonWave.setProperty(u"capacity", 44)
        self.neonWave.setProperty(u"glow", True)
        self.neonWave.setProperty(u"glowStrength", 0.900000000000000)
        self.neonWave.setProperty(u"barGap", 3.000000000000000)
        self.neonWave.setProperty(u"animated", True)

        self.neonCardLayout.addWidget(self.neonWave)

        self.neonCardLayout.setStretch(3, 1)

        self.mainGrid.addWidget(self.neonCard, 1, 1, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"QCustomWaveform \u2014 Demo", None))
        self.ecgCardTitle.setText(QCoreApplication.translate("MainWindow", u"Heart rate", None))
        self.ecgCardSub.setText(QCoreApplication.translate("MainWindow", u"110 bpm \u00b7 live", None))
        self.ecgWave.setProperty(u"mode", QCoreApplication.translate("MainWindow", u"line", None))
        self.waterCardTitle.setText(QCoreApplication.translate("MainWindow", u"Water", None))
        self.waterCardSub.setText(QCoreApplication.translate("MainWindow", u"Recording\u2026", None))
        self.waterWave.setProperty(u"mode", QCoreApplication.translate("MainWindow", u"bars", None))
        self.voiceCardTitle.setText(QCoreApplication.translate("MainWindow", u"Voice message", None))
        self.voiceCardSub.setText(QCoreApplication.translate("MainWindow", u"0:14", None))
        self.voiceWave.setProperty(u"mode", QCoreApplication.translate("MainWindow", u"bars", None))
        self.neonCardTitle.setText(QCoreApplication.translate("MainWindow", u"Spectrum", None))
        self.neonCardSub.setText(QCoreApplication.translate("MainWindow", u"Live \u00b7 neon glow", None))
        self.neonWave.setProperty(u"mode", QCoreApplication.translate("MainWindow", u"bars", None))
    # retranslateUi

