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

from Custom_Widgets.QCustomHeatmap import QCustomHeatmap
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1040, 640)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.mainGrid = QGridLayout(self.centralwidget)
        self.mainGrid.setObjectName(u"mainGrid")
        self.mainGrid.setHorizontalSpacing(20)
        self.mainGrid.setVerticalSpacing(20)
        self.mainGrid.setContentsMargins(24, 24, 24, 24)
        self.activityCard = QFrame(self.centralwidget)
        self.activityCard.setObjectName(u"activityCard")
        self.activityCard.setFrameShape(QFrame.StyledPanel)
        self.activityCardLayout = QVBoxLayout(self.activityCard)
        self.activityCardLayout.setSpacing(2)
        self.activityCardLayout.setObjectName(u"activityCardLayout")
        self.activityCardLayout.setContentsMargins(20, 18, 20, 18)
        self.activityTitle = QLabel(self.activityCard)
        self.activityTitle.setObjectName(u"activityTitle")

        self.activityCardLayout.addWidget(self.activityTitle)

        self.activitySub = QLabel(self.activityCard)
        self.activitySub.setObjectName(u"activitySub")

        self.activityCardLayout.addWidget(self.activitySub)

        self.activitySpacer = QSpacerItem(0, 8, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.activityCardLayout.addItem(self.activitySpacer)

        self.activityHeatmap = QCustomHeatmap(self.activityCard)
        self.activityHeatmap.setObjectName(u"activityHeatmap")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.activityHeatmap.sizePolicy().hasHeightForWidth())
        self.activityHeatmap.setSizePolicy(sizePolicy)

        self.activityCardLayout.addWidget(self.activityHeatmap)

        self.activityCardLayout.setStretch(3, 1)

        self.mainGrid.addWidget(self.activityCard, 0, 0, 1, 1)

        self.contributionsCard = QFrame(self.centralwidget)
        self.contributionsCard.setObjectName(u"contributionsCard")
        self.contributionsCard.setFrameShape(QFrame.StyledPanel)
        self.contributionsCardLayout = QVBoxLayout(self.contributionsCard)
        self.contributionsCardLayout.setSpacing(2)
        self.contributionsCardLayout.setObjectName(u"contributionsCardLayout")
        self.contributionsCardLayout.setContentsMargins(20, 18, 20, 18)
        self.contributionsTitle = QLabel(self.contributionsCard)
        self.contributionsTitle.setObjectName(u"contributionsTitle")

        self.contributionsCardLayout.addWidget(self.contributionsTitle)

        self.contributionsSub = QLabel(self.contributionsCard)
        self.contributionsSub.setObjectName(u"contributionsSub")

        self.contributionsCardLayout.addWidget(self.contributionsSub)

        self.contributionsSpacer = QSpacerItem(0, 8, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.contributionsCardLayout.addItem(self.contributionsSpacer)

        self.contributionsHeatmap = QCustomHeatmap(self.contributionsCard)
        self.contributionsHeatmap.setObjectName(u"contributionsHeatmap")
        sizePolicy.setHeightForWidth(self.contributionsHeatmap.sizePolicy().hasHeightForWidth())
        self.contributionsHeatmap.setSizePolicy(sizePolicy)
        self.contributionsHeatmap.setProperty(u"showLabels", False)

        self.contributionsCardLayout.addWidget(self.contributionsHeatmap)

        self.contributionsCardLayout.setStretch(3, 1)

        self.mainGrid.addWidget(self.contributionsCard, 0, 1, 1, 1)

        self.loadCard = QFrame(self.centralwidget)
        self.loadCard.setObjectName(u"loadCard")
        self.loadCard.setFrameShape(QFrame.StyledPanel)
        self.loadCardLayout = QVBoxLayout(self.loadCard)
        self.loadCardLayout.setSpacing(2)
        self.loadCardLayout.setObjectName(u"loadCardLayout")
        self.loadCardLayout.setContentsMargins(20, 18, 20, 18)
        self.loadTitle = QLabel(self.loadCard)
        self.loadTitle.setObjectName(u"loadTitle")

        self.loadCardLayout.addWidget(self.loadTitle)

        self.loadSub = QLabel(self.loadCard)
        self.loadSub.setObjectName(u"loadSub")

        self.loadCardLayout.addWidget(self.loadSub)

        self.loadSpacer = QSpacerItem(0, 8, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.loadCardLayout.addItem(self.loadSpacer)

        self.loadHeatmap = QCustomHeatmap(self.loadCard)
        self.loadHeatmap.setObjectName(u"loadHeatmap")
        sizePolicy.setHeightForWidth(self.loadHeatmap.sizePolicy().hasHeightForWidth())
        self.loadHeatmap.setSizePolicy(sizePolicy)

        self.loadCardLayout.addWidget(self.loadHeatmap)

        self.loadCardLayout.setStretch(3, 1)

        self.mainGrid.addWidget(self.loadCard, 1, 0, 1, 2)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"QCustomHeatmap \u2014 Demo", None))
        self.activityTitle.setText(QCoreApplication.translate("MainWindow", u"Activity by time", None))
        self.activitySub.setText(QCoreApplication.translate("MainWindow", u"This week", None))
        self.contributionsTitle.setText(QCoreApplication.translate("MainWindow", u"Contributions", None))
        self.contributionsSub.setText(QCoreApplication.translate("MainWindow", u"Last 20 weeks", None))
        self.contributionsHeatmap.setProperty(u"mode", QCoreApplication.translate("MainWindow", u"calendar", None))
        self.loadTitle.setText(QCoreApplication.translate("MainWindow", u"Server load by hour", None))
        self.loadSub.setText(QCoreApplication.translate("MainWindow", u"Avg req/s", None))
    # retranslateUi

