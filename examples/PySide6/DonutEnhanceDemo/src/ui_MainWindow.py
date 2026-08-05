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
    QMainWindow, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

from Custom_Widgets.QCustomDonut import QCustomDonut
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1000, 560)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.cardsRow = QHBoxLayout(self.centralwidget)
        self.cardsRow.setSpacing(20)
        self.cardsRow.setObjectName(u"cardsRow")
        self.cardsRow.setContentsMargins(24, 24, 24, 24)
        self.transferCard = QFrame(self.centralwidget)
        self.transferCard.setObjectName(u"transferCard")
        self.transferCard.setFrameShape(QFrame.NoFrame)
        self.transferLayout = QVBoxLayout(self.transferCard)
        self.transferLayout.setSpacing(2)
        self.transferLayout.setObjectName(u"transferLayout")
        self.transferLayout.setContentsMargins(20, 16, 20, 16)
        self.transferTitle = QLabel(self.transferCard)
        self.transferTitle.setObjectName(u"transferTitle")

        self.transferLayout.addWidget(self.transferTitle)

        self.transferSub = QLabel(self.transferCard)
        self.transferSub.setObjectName(u"transferSub")

        self.transferLayout.addWidget(self.transferSub)

        self.transferTopSpacer = QSpacerItem(0, 8, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.transferLayout.addItem(self.transferTopSpacer)

        self.transferDonut = QCustomDonut(self.transferCard)
        self.transferDonut.setObjectName(u"transferDonut")
        self.transferDonut.setProperty(u"gapDegrees", 5.000000000000000)
        self.transferDonut.setProperty(u"showPercentLabels", True)

        self.transferLayout.addWidget(self.transferDonut)

        self.transferMidSpacer = QSpacerItem(0, 6, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.transferLayout.addItem(self.transferMidSpacer)

        self.transferLegRow1 = QHBoxLayout()
        self.transferLegRow1.setSpacing(8)
        self.transferLegRow1.setObjectName(u"transferLegRow1")
        self.transferDot1 = QFrame(self.transferCard)
        self.transferDot1.setObjectName(u"transferDot1")
        self.transferDot1.setMinimumSize(QSize(10, 10))
        self.transferDot1.setMaximumSize(QSize(10, 10))
        self.transferDot1.setFrameShape(QFrame.NoFrame)

        self.transferLegRow1.addWidget(self.transferDot1)

        self.transferName1 = QLabel(self.transferCard)
        self.transferName1.setObjectName(u"transferName1")

        self.transferLegRow1.addWidget(self.transferName1)

        self.transferLegSpacer1 = QSpacerItem(10, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.transferLegRow1.addItem(self.transferLegSpacer1)

        self.transferVal1 = QLabel(self.transferCard)
        self.transferVal1.setObjectName(u"transferVal1")

        self.transferLegRow1.addWidget(self.transferVal1)


        self.transferLayout.addLayout(self.transferLegRow1)

        self.transferLegRow2 = QHBoxLayout()
        self.transferLegRow2.setSpacing(8)
        self.transferLegRow2.setObjectName(u"transferLegRow2")
        self.transferDot2 = QFrame(self.transferCard)
        self.transferDot2.setObjectName(u"transferDot2")
        self.transferDot2.setMinimumSize(QSize(10, 10))
        self.transferDot2.setMaximumSize(QSize(10, 10))
        self.transferDot2.setFrameShape(QFrame.NoFrame)

        self.transferLegRow2.addWidget(self.transferDot2)

        self.transferName2 = QLabel(self.transferCard)
        self.transferName2.setObjectName(u"transferName2")

        self.transferLegRow2.addWidget(self.transferName2)

        self.transferLegSpacer2 = QSpacerItem(10, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.transferLegRow2.addItem(self.transferLegSpacer2)

        self.transferVal2 = QLabel(self.transferCard)
        self.transferVal2.setObjectName(u"transferVal2")

        self.transferLegRow2.addWidget(self.transferVal2)


        self.transferLayout.addLayout(self.transferLegRow2)

        self.transferLegRow3 = QHBoxLayout()
        self.transferLegRow3.setSpacing(8)
        self.transferLegRow3.setObjectName(u"transferLegRow3")
        self.transferDot3 = QFrame(self.transferCard)
        self.transferDot3.setObjectName(u"transferDot3")
        self.transferDot3.setMinimumSize(QSize(10, 10))
        self.transferDot3.setMaximumSize(QSize(10, 10))
        self.transferDot3.setFrameShape(QFrame.NoFrame)

        self.transferLegRow3.addWidget(self.transferDot3)

        self.transferName3 = QLabel(self.transferCard)
        self.transferName3.setObjectName(u"transferName3")

        self.transferLegRow3.addWidget(self.transferName3)

        self.transferLegSpacer3 = QSpacerItem(10, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.transferLegRow3.addItem(self.transferLegSpacer3)

        self.transferVal3 = QLabel(self.transferCard)
        self.transferVal3.setObjectName(u"transferVal3")

        self.transferLegRow3.addWidget(self.transferVal3)


        self.transferLayout.addLayout(self.transferLegRow3)

        self.transferLegRow4 = QHBoxLayout()
        self.transferLegRow4.setSpacing(8)
        self.transferLegRow4.setObjectName(u"transferLegRow4")
        self.transferDot4 = QFrame(self.transferCard)
        self.transferDot4.setObjectName(u"transferDot4")
        self.transferDot4.setMinimumSize(QSize(10, 10))
        self.transferDot4.setMaximumSize(QSize(10, 10))
        self.transferDot4.setFrameShape(QFrame.NoFrame)

        self.transferLegRow4.addWidget(self.transferDot4)

        self.transferName4 = QLabel(self.transferCard)
        self.transferName4.setObjectName(u"transferName4")

        self.transferLegRow4.addWidget(self.transferName4)

        self.transferLegSpacer4 = QSpacerItem(10, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.transferLegRow4.addItem(self.transferLegSpacer4)

        self.transferVal4 = QLabel(self.transferCard)
        self.transferVal4.setObjectName(u"transferVal4")

        self.transferLegRow4.addWidget(self.transferVal4)


        self.transferLayout.addLayout(self.transferLegRow4)

        self.transferLegRow5 = QHBoxLayout()
        self.transferLegRow5.setSpacing(8)
        self.transferLegRow5.setObjectName(u"transferLegRow5")
        self.transferDot5 = QFrame(self.transferCard)
        self.transferDot5.setObjectName(u"transferDot5")
        self.transferDot5.setMinimumSize(QSize(10, 10))
        self.transferDot5.setMaximumSize(QSize(10, 10))
        self.transferDot5.setFrameShape(QFrame.NoFrame)

        self.transferLegRow5.addWidget(self.transferDot5)

        self.transferName5 = QLabel(self.transferCard)
        self.transferName5.setObjectName(u"transferName5")

        self.transferLegRow5.addWidget(self.transferName5)

        self.transferLegSpacer5 = QSpacerItem(10, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.transferLegRow5.addItem(self.transferLegSpacer5)

        self.transferVal5 = QLabel(self.transferCard)
        self.transferVal5.setObjectName(u"transferVal5")

        self.transferLegRow5.addWidget(self.transferVal5)


        self.transferLayout.addLayout(self.transferLegRow5)

        self.transferLayout.setStretch(3, 1)

        self.cardsRow.addWidget(self.transferCard)

        self.storageCard = QFrame(self.centralwidget)
        self.storageCard.setObjectName(u"storageCard")
        self.storageCard.setFrameShape(QFrame.NoFrame)
        self.storageLayout = QVBoxLayout(self.storageCard)
        self.storageLayout.setSpacing(2)
        self.storageLayout.setObjectName(u"storageLayout")
        self.storageLayout.setContentsMargins(20, 16, 20, 16)
        self.storageTitle = QLabel(self.storageCard)
        self.storageTitle.setObjectName(u"storageTitle")

        self.storageLayout.addWidget(self.storageTitle)

        self.storageSub = QLabel(self.storageCard)
        self.storageSub.setObjectName(u"storageSub")

        self.storageLayout.addWidget(self.storageSub)

        self.storageTopSpacer = QSpacerItem(0, 8, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.storageLayout.addItem(self.storageTopSpacer)

        self.storageDonut = QCustomDonut(self.storageCard)
        self.storageDonut.setObjectName(u"storageDonut")
        self.storageDonut.setProperty(u"gapDegrees", 5.000000000000000)
        self.storageDonut.setProperty(u"showPercentLabels", True)

        self.storageLayout.addWidget(self.storageDonut)

        self.storageMidSpacer = QSpacerItem(0, 6, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.storageLayout.addItem(self.storageMidSpacer)

        self.storageLegRow1 = QHBoxLayout()
        self.storageLegRow1.setSpacing(8)
        self.storageLegRow1.setObjectName(u"storageLegRow1")
        self.storageDot1 = QFrame(self.storageCard)
        self.storageDot1.setObjectName(u"storageDot1")
        self.storageDot1.setMinimumSize(QSize(10, 10))
        self.storageDot1.setMaximumSize(QSize(10, 10))
        self.storageDot1.setFrameShape(QFrame.NoFrame)

        self.storageLegRow1.addWidget(self.storageDot1)

        self.storageName1 = QLabel(self.storageCard)
        self.storageName1.setObjectName(u"storageName1")

        self.storageLegRow1.addWidget(self.storageName1)

        self.storageLegSpacer1 = QSpacerItem(10, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.storageLegRow1.addItem(self.storageLegSpacer1)

        self.storageVal1 = QLabel(self.storageCard)
        self.storageVal1.setObjectName(u"storageVal1")

        self.storageLegRow1.addWidget(self.storageVal1)


        self.storageLayout.addLayout(self.storageLegRow1)

        self.storageLegRow2 = QHBoxLayout()
        self.storageLegRow2.setSpacing(8)
        self.storageLegRow2.setObjectName(u"storageLegRow2")
        self.storageDot2 = QFrame(self.storageCard)
        self.storageDot2.setObjectName(u"storageDot2")
        self.storageDot2.setMinimumSize(QSize(10, 10))
        self.storageDot2.setMaximumSize(QSize(10, 10))
        self.storageDot2.setFrameShape(QFrame.NoFrame)

        self.storageLegRow2.addWidget(self.storageDot2)

        self.storageName2 = QLabel(self.storageCard)
        self.storageName2.setObjectName(u"storageName2")

        self.storageLegRow2.addWidget(self.storageName2)

        self.storageLegSpacer2 = QSpacerItem(10, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.storageLegRow2.addItem(self.storageLegSpacer2)

        self.storageVal2 = QLabel(self.storageCard)
        self.storageVal2.setObjectName(u"storageVal2")

        self.storageLegRow2.addWidget(self.storageVal2)


        self.storageLayout.addLayout(self.storageLegRow2)

        self.storageLegRow3 = QHBoxLayout()
        self.storageLegRow3.setSpacing(8)
        self.storageLegRow3.setObjectName(u"storageLegRow3")
        self.storageDot3 = QFrame(self.storageCard)
        self.storageDot3.setObjectName(u"storageDot3")
        self.storageDot3.setMinimumSize(QSize(10, 10))
        self.storageDot3.setMaximumSize(QSize(10, 10))
        self.storageDot3.setFrameShape(QFrame.NoFrame)

        self.storageLegRow3.addWidget(self.storageDot3)

        self.storageName3 = QLabel(self.storageCard)
        self.storageName3.setObjectName(u"storageName3")

        self.storageLegRow3.addWidget(self.storageName3)

        self.storageLegSpacer3 = QSpacerItem(10, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.storageLegRow3.addItem(self.storageLegSpacer3)

        self.storageVal3 = QLabel(self.storageCard)
        self.storageVal3.setObjectName(u"storageVal3")

        self.storageLegRow3.addWidget(self.storageVal3)


        self.storageLayout.addLayout(self.storageLegRow3)

        self.storageLegRow4 = QHBoxLayout()
        self.storageLegRow4.setSpacing(8)
        self.storageLegRow4.setObjectName(u"storageLegRow4")
        self.storageDot4 = QFrame(self.storageCard)
        self.storageDot4.setObjectName(u"storageDot4")
        self.storageDot4.setMinimumSize(QSize(10, 10))
        self.storageDot4.setMaximumSize(QSize(10, 10))
        self.storageDot4.setFrameShape(QFrame.NoFrame)

        self.storageLegRow4.addWidget(self.storageDot4)

        self.storageName4 = QLabel(self.storageCard)
        self.storageName4.setObjectName(u"storageName4")

        self.storageLegRow4.addWidget(self.storageName4)

        self.storageLegSpacer4 = QSpacerItem(10, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.storageLegRow4.addItem(self.storageLegSpacer4)

        self.storageVal4 = QLabel(self.storageCard)
        self.storageVal4.setObjectName(u"storageVal4")

        self.storageLegRow4.addWidget(self.storageVal4)


        self.storageLayout.addLayout(self.storageLegRow4)

        self.storageLayout.setStretch(3, 1)

        self.cardsRow.addWidget(self.storageCard)

        self.classicCard = QFrame(self.centralwidget)
        self.classicCard.setObjectName(u"classicCard")
        self.classicCard.setFrameShape(QFrame.NoFrame)
        self.classicLayout = QVBoxLayout(self.classicCard)
        self.classicLayout.setSpacing(2)
        self.classicLayout.setObjectName(u"classicLayout")
        self.classicLayout.setContentsMargins(20, 16, 20, 16)
        self.classicTitle = QLabel(self.classicCard)
        self.classicTitle.setObjectName(u"classicTitle")

        self.classicLayout.addWidget(self.classicTitle)

        self.classicSub = QLabel(self.classicCard)
        self.classicSub.setObjectName(u"classicSub")

        self.classicLayout.addWidget(self.classicSub)

        self.classicTopSpacer = QSpacerItem(0, 8, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.classicLayout.addItem(self.classicTopSpacer)

        self.classicDonut = QCustomDonut(self.classicCard)
        self.classicDonut.setObjectName(u"classicDonut")

        self.classicLayout.addWidget(self.classicDonut)

        self.classicLayout.setStretch(3, 1)

        self.cardsRow.addWidget(self.classicCard)

        self.cardsRow.setStretch(0, 1)
        self.cardsRow.setStretch(1, 1)
        self.cardsRow.setStretch(2, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"QCustomDonut \u2014 % callouts + hatch", None))
        self.transferTitle.setText(QCoreApplication.translate("MainWindow", u"Transfer history", None))
        self.transferSub.setText(QCoreApplication.translate("MainWindow", u"This month \u00b7 % on arcs", None))
        self.transferDonut.setProperty(u"mode", QCoreApplication.translate("MainWindow", u"segments", None))
        self.transferDonut.setProperty(u"hatchPattern", QCoreApplication.translate("MainWindow", u"bdiag", None))
        self.transferName1.setText(QCoreApplication.translate("MainWindow", u"Product", None))
        self.transferVal1.setText(QCoreApplication.translate("MainWindow", u"30%", None))
        self.transferName2.setText(QCoreApplication.translate("MainWindow", u"Restaurants & bars", None))
        self.transferVal2.setText(QCoreApplication.translate("MainWindow", u"23%", None))
        self.transferName3.setText(QCoreApplication.translate("MainWindow", u"Internet & media", None))
        self.transferVal3.setText(QCoreApplication.translate("MainWindow", u"18%", None))
        self.transferName4.setText(QCoreApplication.translate("MainWindow", u"Pay for workplace", None))
        self.transferVal4.setText(QCoreApplication.translate("MainWindow", u"17%", None))
        self.transferName5.setText(QCoreApplication.translate("MainWindow", u"Other", None))
        self.transferVal5.setText(QCoreApplication.translate("MainWindow", u"12%", None))
        self.storageTitle.setText(QCoreApplication.translate("MainWindow", u"Storage", None))
        self.storageSub.setText(QCoreApplication.translate("MainWindow", u"cross hatch on Free", None))
        self.storageDonut.setProperty(u"mode", QCoreApplication.translate("MainWindow", u"segments", None))
        self.storageDonut.setProperty(u"hatchPattern", QCoreApplication.translate("MainWindow", u"cross", None))
        self.storageName1.setText(QCoreApplication.translate("MainWindow", u"Photos", None))
        self.storageVal1.setText(QCoreApplication.translate("MainWindow", u"44%", None))
        self.storageName2.setText(QCoreApplication.translate("MainWindow", u"Apps", None))
        self.storageVal2.setText(QCoreApplication.translate("MainWindow", u"26%", None))
        self.storageName3.setText(QCoreApplication.translate("MainWindow", u"Media", None))
        self.storageVal3.setText(QCoreApplication.translate("MainWindow", u"16%", None))
        self.storageName4.setText(QCoreApplication.translate("MainWindow", u"Free", None))
        self.storageVal4.setText(QCoreApplication.translate("MainWindow", u"14%", None))
        self.classicTitle.setText(QCoreApplication.translate("MainWindow", u"Classic (rings)", None))
        self.classicSub.setText(QCoreApplication.translate("MainWindow", u"enhancements OFF \u2014 unchanged", None))
    # retranslateUi

