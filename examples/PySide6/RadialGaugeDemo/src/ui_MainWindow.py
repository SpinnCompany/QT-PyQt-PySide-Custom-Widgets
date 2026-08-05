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
    QMainWindow, QPushButton, QSizePolicy, QVBoxLayout,
    QWidget)

from Custom_Widgets.QCustomRadialGauge import QCustomRadialGauge
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1000, 620)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.mainGrid = QGridLayout(self.centralwidget)
        self.mainGrid.setObjectName(u"mainGrid")
        self.mainGrid.setHorizontalSpacing(20)
        self.mainGrid.setVerticalSpacing(20)
        self.mainGrid.setContentsMargins(24, 24, 24, 24)
        self.threatCard1 = QFrame(self.centralwidget)
        self.threatCard1.setObjectName(u"threatCard1")
        self.threatCard1.setFrameShape(QFrame.StyledPanel)
        self.threatCard1Layout = QVBoxLayout(self.threatCard1)
        self.threatCard1Layout.setSpacing(4)
        self.threatCard1Layout.setObjectName(u"threatCard1Layout")
        self.threatCard1Layout.setContentsMargins(18, 16, 18, 16)
        self.threatCard1Title = QLabel(self.threatCard1)
        self.threatCard1Title.setObjectName(u"threatCard1Title")

        self.threatCard1Layout.addWidget(self.threatCard1Title)

        self.threatCard1Sub = QLabel(self.threatCard1)
        self.threatCard1Sub.setObjectName(u"threatCard1Sub")

        self.threatCard1Layout.addWidget(self.threatCard1Sub)

        self.threatGauge1 = QCustomRadialGauge(self.threatCard1)
        self.threatGauge1.setObjectName(u"threatGauge1")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.threatGauge1.sizePolicy().hasHeightForWidth())
        self.threatGauge1.setSizePolicy(sizePolicy)
        self.threatGauge1.setProperty(u"value", 0.000000000000000)
        self.threatGauge1.setProperty(u"animated", True)
        self.threatGauge1.setProperty(u"animationDuration", 900)
        self.threatGauge1.setProperty(u"glow", True)

        self.threatCard1Layout.addWidget(self.threatGauge1)

        self.threatCard1Layout.setStretch(2, 1)

        self.mainGrid.addWidget(self.threatCard1, 0, 0, 1, 1)

        self.threatCard2 = QFrame(self.centralwidget)
        self.threatCard2.setObjectName(u"threatCard2")
        self.threatCard2.setFrameShape(QFrame.StyledPanel)
        self.threatCard2Layout = QVBoxLayout(self.threatCard2)
        self.threatCard2Layout.setSpacing(4)
        self.threatCard2Layout.setObjectName(u"threatCard2Layout")
        self.threatCard2Layout.setContentsMargins(18, 16, 18, 16)
        self.threatCard2Title = QLabel(self.threatCard2)
        self.threatCard2Title.setObjectName(u"threatCard2Title")

        self.threatCard2Layout.addWidget(self.threatCard2Title)

        self.threatCard2Sub = QLabel(self.threatCard2)
        self.threatCard2Sub.setObjectName(u"threatCard2Sub")

        self.threatCard2Layout.addWidget(self.threatCard2Sub)

        self.threatGauge2 = QCustomRadialGauge(self.threatCard2)
        self.threatGauge2.setObjectName(u"threatGauge2")
        sizePolicy.setHeightForWidth(self.threatGauge2.sizePolicy().hasHeightForWidth())
        self.threatGauge2.setSizePolicy(sizePolicy)
        self.threatGauge2.setProperty(u"value", 0.000000000000000)
        self.threatGauge2.setProperty(u"animated", True)
        self.threatGauge2.setProperty(u"animationDuration", 900)
        self.threatGauge2.setProperty(u"glow", True)

        self.threatCard2Layout.addWidget(self.threatGauge2)

        self.threatCard2Layout.setStretch(2, 1)

        self.mainGrid.addWidget(self.threatCard2, 0, 1, 1, 1)

        self.threatCard3 = QFrame(self.centralwidget)
        self.threatCard3.setObjectName(u"threatCard3")
        self.threatCard3.setFrameShape(QFrame.StyledPanel)
        self.threatCard3Layout = QVBoxLayout(self.threatCard3)
        self.threatCard3Layout.setSpacing(4)
        self.threatCard3Layout.setObjectName(u"threatCard3Layout")
        self.threatCard3Layout.setContentsMargins(18, 16, 18, 16)
        self.threatCard3Title = QLabel(self.threatCard3)
        self.threatCard3Title.setObjectName(u"threatCard3Title")

        self.threatCard3Layout.addWidget(self.threatCard3Title)

        self.threatCard3Sub = QLabel(self.threatCard3)
        self.threatCard3Sub.setObjectName(u"threatCard3Sub")

        self.threatCard3Layout.addWidget(self.threatCard3Sub)

        self.threatGauge3 = QCustomRadialGauge(self.threatCard3)
        self.threatGauge3.setObjectName(u"threatGauge3")
        sizePolicy.setHeightForWidth(self.threatGauge3.sizePolicy().hasHeightForWidth())
        self.threatGauge3.setSizePolicy(sizePolicy)
        self.threatGauge3.setProperty(u"value", 0.000000000000000)
        self.threatGauge3.setProperty(u"animated", True)
        self.threatGauge3.setProperty(u"animationDuration", 900)
        self.threatGauge3.setProperty(u"glow", True)

        self.threatCard3Layout.addWidget(self.threatGauge3)

        self.threatCard3Layout.setStretch(2, 1)

        self.mainGrid.addWidget(self.threatCard3, 0, 2, 1, 1)

        self.speedCard = QFrame(self.centralwidget)
        self.speedCard.setObjectName(u"speedCard")
        self.speedCard.setFrameShape(QFrame.StyledPanel)
        self.speedCardLayout = QVBoxLayout(self.speedCard)
        self.speedCardLayout.setSpacing(4)
        self.speedCardLayout.setObjectName(u"speedCardLayout")
        self.speedCardLayout.setContentsMargins(18, 16, 18, 16)
        self.speedCardTitle = QLabel(self.speedCard)
        self.speedCardTitle.setObjectName(u"speedCardTitle")

        self.speedCardLayout.addWidget(self.speedCardTitle)

        self.speedCardSub = QLabel(self.speedCard)
        self.speedCardSub.setObjectName(u"speedCardSub")

        self.speedCardLayout.addWidget(self.speedCardSub)

        self.speedGauge = QCustomRadialGauge(self.speedCard)
        self.speedGauge.setObjectName(u"speedGauge")
        sizePolicy.setHeightForWidth(self.speedGauge.sizePolicy().hasHeightForWidth())
        self.speedGauge.setSizePolicy(sizePolicy)
        self.speedGauge.setProperty(u"value", 0.000000000000000)
        self.speedGauge.setProperty(u"minimum", 0.000000000000000)
        self.speedGauge.setProperty(u"maximum", 150.000000000000000)
        self.speedGauge.setProperty(u"startAngle", 210.000000000000000)
        self.speedGauge.setProperty(u"spanAngle", -240.000000000000000)
        self.speedGauge.setProperty(u"arcWidth", 18)
        self.speedGauge.setProperty(u"scaleLabelEvery", 30.000000000000000)
        self.speedGauge.setProperty(u"glow", True)
        self.speedGauge.setProperty(u"animated", True)
        self.speedGauge.setProperty(u"animationDuration", 1100)

        self.speedCardLayout.addWidget(self.speedGauge)

        self.speedCardLayout.setStretch(2, 1)

        self.mainGrid.addWidget(self.speedCard, 1, 0, 1, 1)

        self.usageCard = QFrame(self.centralwidget)
        self.usageCard.setObjectName(u"usageCard")
        self.usageCard.setFrameShape(QFrame.StyledPanel)
        self.usageCardLayout = QVBoxLayout(self.usageCard)
        self.usageCardLayout.setSpacing(4)
        self.usageCardLayout.setObjectName(u"usageCardLayout")
        self.usageCardLayout.setContentsMargins(18, 16, 18, 16)
        self.usageCardTitle = QLabel(self.usageCard)
        self.usageCardTitle.setObjectName(u"usageCardTitle")

        self.usageCardLayout.addWidget(self.usageCardTitle)

        self.usageCardSub = QLabel(self.usageCard)
        self.usageCardSub.setObjectName(u"usageCardSub")

        self.usageCardLayout.addWidget(self.usageCardSub)

        self.usageGauge = QCustomRadialGauge(self.usageCard)
        self.usageGauge.setObjectName(u"usageGauge")
        sizePolicy.setHeightForWidth(self.usageGauge.sizePolicy().hasHeightForWidth())
        self.usageGauge.setSizePolicy(sizePolicy)
        self.usageGauge.setProperty(u"value", 0.000000000000000)
        self.usageGauge.setProperty(u"minimum", 0.000000000000000)
        self.usageGauge.setProperty(u"maximum", 100.000000000000000)
        self.usageGauge.setProperty(u"startAngle", 90.000000000000000)
        self.usageGauge.setProperty(u"spanAngle", -360.000000000000000)
        self.usageGauge.setProperty(u"showNeedle", False)
        self.usageGauge.setProperty(u"scaleLabelEvery", 25.000000000000000)
        self.usageGauge.setProperty(u"glow", True)
        self.usageGauge.setProperty(u"animated", True)
        self.usageGauge.setProperty(u"animationDuration", 1100)

        self.usageCardLayout.addWidget(self.usageGauge)

        self.usageCardLayout.setStretch(2, 1)

        self.mainGrid.addWidget(self.usageCard, 1, 1, 1, 1)

        self.timerCard = QFrame(self.centralwidget)
        self.timerCard.setObjectName(u"timerCard")
        self.timerCard.setFrameShape(QFrame.StyledPanel)
        self.timerCardLayout = QVBoxLayout(self.timerCard)
        self.timerCardLayout.setSpacing(4)
        self.timerCardLayout.setObjectName(u"timerCardLayout")
        self.timerCardLayout.setContentsMargins(18, 16, 18, 16)
        self.timerCardTitle = QLabel(self.timerCard)
        self.timerCardTitle.setObjectName(u"timerCardTitle")

        self.timerCardLayout.addWidget(self.timerCardTitle)

        self.timerCardSub = QLabel(self.timerCard)
        self.timerCardSub.setObjectName(u"timerCardSub")

        self.timerCardLayout.addWidget(self.timerCardSub)

        self.timerGauge = QCustomRadialGauge(self.timerCard)
        self.timerGauge.setObjectName(u"timerGauge")
        sizePolicy.setHeightForWidth(self.timerGauge.sizePolicy().hasHeightForWidth())
        self.timerGauge.setSizePolicy(sizePolicy)
        self.timerGauge.setProperty(u"value", 17.000000000000000)
        self.timerGauge.setProperty(u"minimum", 0.000000000000000)
        self.timerGauge.setProperty(u"maximum", 20.000000000000000)
        self.timerGauge.setProperty(u"startAngle", 90.000000000000000)
        self.timerGauge.setProperty(u"spanAngle", -360.000000000000000)
        self.timerGauge.setProperty(u"tickCount", 60)
        self.timerGauge.setProperty(u"showGuide", True)
        self.timerGauge.setProperty(u"scaleLabelEvery", 5.000000000000000)
        self.timerGauge.setProperty(u"glow", True)

        self.timerCardLayout.addWidget(self.timerGauge)

        self.timerCardLayout.setStretch(2, 1)

        self.mainGrid.addWidget(self.timerCard, 1, 2, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"QCustomRadialGauge \u2014 Demo", None))
        self.threatCard1Title.setText(QCoreApplication.translate("MainWindow", u"Threat Level", None))
        self.threatCard1Sub.setText(QCoreApplication.translate("MainWindow", u"Last updated on 15th January, 2024", None))
        self.threatGauge1.setProperty(u"centerSuffix", QCoreApplication.translate("MainWindow", u"%", None))
        self.threatGauge1.setProperty(u"statusText", QCoreApplication.translate("MainWindow", u"Very Low", None))
        self.threatCard2Title.setText(QCoreApplication.translate("MainWindow", u"Threat Level", None))
        self.threatCard2Sub.setText(QCoreApplication.translate("MainWindow", u"Last updated on 15th January, 2024", None))
        self.threatGauge2.setProperty(u"centerSuffix", QCoreApplication.translate("MainWindow", u"%", None))
        self.threatGauge2.setProperty(u"statusText", QCoreApplication.translate("MainWindow", u"Medium", None))
        self.threatCard3Title.setText(QCoreApplication.translate("MainWindow", u"Threat Level", None))
        self.threatCard3Sub.setText(QCoreApplication.translate("MainWindow", u"Last updated on 15th January, 2024", None))
        self.threatGauge3.setProperty(u"centerSuffix", QCoreApplication.translate("MainWindow", u"%", None))
        self.threatGauge3.setProperty(u"statusText", QCoreApplication.translate("MainWindow", u"High", None))
        self.speedCardTitle.setText(QCoreApplication.translate("MainWindow", u"Speed", None))
        self.speedCardSub.setText(QCoreApplication.translate("MainWindow", u"Last updated on 15th January, 2024", None))
        self.speedGauge.setProperty(u"centerSuffix", QCoreApplication.translate("MainWindow", u"mph", None))
        self.usageCardTitle.setText(QCoreApplication.translate("MainWindow", u"Usage", None))
        self.usageCardSub.setText(QCoreApplication.translate("MainWindow", u"Last updated on 15th January, 2024", None))
        self.usageGauge.setProperty(u"centerSuffix", QCoreApplication.translate("MainWindow", u"%", None))
        self.timerCardTitle.setText(QCoreApplication.translate("MainWindow", u"Timer", None))
        self.timerCardSub.setText(QCoreApplication.translate("MainWindow", u"Last updated on 15th January, 2024", None))
        self.timerGauge.setProperty(u"gaugeStyle", QCoreApplication.translate("MainWindow", u"tick", None))
        self.timerGauge.setProperty(u"centerText", QCoreApplication.translate("MainWindow", u"17", None))
        self.timerGauge.setProperty(u"centerSuffix", QCoreApplication.translate("MainWindow", u"Sec", None))
        self.timerGauge.setProperty(u"activeTickExtend", QCoreApplication.translate("MainWindow", u"outward", None))
    # retranslateUi

