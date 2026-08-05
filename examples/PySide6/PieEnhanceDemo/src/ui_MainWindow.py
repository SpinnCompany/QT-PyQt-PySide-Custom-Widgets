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

from Custom_Widgets.QCustomCharts.QCustomPieChart import QCustomPieChart
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1020, 560)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.mainRow = QHBoxLayout(self.centralwidget)
        self.mainRow.setSpacing(20)
        self.mainRow.setObjectName(u"mainRow")
        self.mainRow.setContentsMargins(24, 24, 24, 24)
        self.transferCard = QFrame(self.centralwidget)
        self.transferCard.setObjectName(u"transferCard")
        self.transferCard.setFrameShape(QFrame.StyledPanel)
        self.transferCardLayout = QVBoxLayout(self.transferCard)
        self.transferCardLayout.setSpacing(2)
        self.transferCardLayout.setObjectName(u"transferCardLayout")
        self.transferCardLayout.setContentsMargins(18, 14, 18, 14)
        self.transferTitle = QLabel(self.transferCard)
        self.transferTitle.setObjectName(u"transferTitle")

        self.transferCardLayout.addWidget(self.transferTitle)

        self.transferSub = QLabel(self.transferCard)
        self.transferSub.setObjectName(u"transferSub")

        self.transferCardLayout.addWidget(self.transferSub)

        self.transferSpacer = QSpacerItem(0, 6, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.transferCardLayout.addItem(self.transferSpacer)

        self.transferPie = QCustomPieChart(self.transferCard)
        self.transferPie.setObjectName(u"transferPie")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.transferPie.sizePolicy().hasHeightForWidth())
        self.transferPie.setSizePolicy(sizePolicy)

        self.transferCardLayout.addWidget(self.transferPie)

        self.transferCardLayout.setStretch(3, 1)

        self.mainRow.addWidget(self.transferCard)

        self.storageCard = QFrame(self.centralwidget)
        self.storageCard.setObjectName(u"storageCard")
        self.storageCard.setFrameShape(QFrame.StyledPanel)
        self.storageCardLayout = QVBoxLayout(self.storageCard)
        self.storageCardLayout.setSpacing(2)
        self.storageCardLayout.setObjectName(u"storageCardLayout")
        self.storageCardLayout.setContentsMargins(18, 14, 18, 14)
        self.storageTitle = QLabel(self.storageCard)
        self.storageTitle.setObjectName(u"storageTitle")

        self.storageCardLayout.addWidget(self.storageTitle)

        self.storageSub = QLabel(self.storageCard)
        self.storageSub.setObjectName(u"storageSub")

        self.storageCardLayout.addWidget(self.storageSub)

        self.storageSpacer = QSpacerItem(0, 6, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.storageCardLayout.addItem(self.storageSpacer)

        self.storagePie = QCustomPieChart(self.storageCard)
        self.storagePie.setObjectName(u"storagePie")
        sizePolicy.setHeightForWidth(self.storagePie.sizePolicy().hasHeightForWidth())
        self.storagePie.setSizePolicy(sizePolicy)

        self.storageCardLayout.addWidget(self.storagePie)

        self.storageCardLayout.setStretch(3, 1)

        self.mainRow.addWidget(self.storageCard)

        self.defaultCard = QFrame(self.centralwidget)
        self.defaultCard.setObjectName(u"defaultCard")
        self.defaultCard.setFrameShape(QFrame.StyledPanel)
        self.defaultCardLayout = QVBoxLayout(self.defaultCard)
        self.defaultCardLayout.setSpacing(2)
        self.defaultCardLayout.setObjectName(u"defaultCardLayout")
        self.defaultCardLayout.setContentsMargins(18, 14, 18, 14)
        self.defaultTitle = QLabel(self.defaultCard)
        self.defaultTitle.setObjectName(u"defaultTitle")

        self.defaultCardLayout.addWidget(self.defaultTitle)

        self.defaultSub = QLabel(self.defaultCard)
        self.defaultSub.setObjectName(u"defaultSub")

        self.defaultCardLayout.addWidget(self.defaultSub)

        self.defaultSpacer = QSpacerItem(0, 6, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.defaultCardLayout.addItem(self.defaultSpacer)

        self.defaultPie = QCustomPieChart(self.defaultCard)
        self.defaultPie.setObjectName(u"defaultPie")
        sizePolicy.setHeightForWidth(self.defaultPie.sizePolicy().hasHeightForWidth())
        self.defaultPie.setSizePolicy(sizePolicy)

        self.defaultCardLayout.addWidget(self.defaultPie)

        self.defaultCardLayout.setStretch(3, 1)

        self.mainRow.addWidget(self.defaultCard)

        self.mainRow.setStretch(0, 1)
        self.mainRow.setStretch(1, 1)
        self.mainRow.setStretch(2, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"QCustomPieChart \u2014 % callouts + hatch", None))
        self.transferTitle.setText(QCoreApplication.translate("MainWindow", u"Transfer history", None))
        self.transferSub.setText(QCoreApplication.translate("MainWindow", u"% inside + hatched slices", None))
        self.storageTitle.setText(QCoreApplication.translate("MainWindow", u"Storage", None))
        self.storageSub.setText(QCoreApplication.translate("MainWindow", u"cross hatch on Other", None))
        self.defaultTitle.setText(QCoreApplication.translate("MainWindow", u"Default", None))
        self.defaultSub.setText(QCoreApplication.translate("MainWindow", u"enhancements off", None))
    # retranslateUi

