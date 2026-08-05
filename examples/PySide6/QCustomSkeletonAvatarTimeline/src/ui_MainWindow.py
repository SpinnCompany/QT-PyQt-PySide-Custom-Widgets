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
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

from Custom_Widgets.QCustomAvatarGroup import QCustomAvatarGroup
from Custom_Widgets.QCustomSkeleton import QCustomSkeleton
from Custom_Widgets.QCustomTimeline import QCustomTimeline
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(480, 520)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.rootLayout = QVBoxLayout(self.centralwidget)
        self.rootLayout.setSpacing(10)
        self.rootLayout.setObjectName(u"rootLayout")
        self.rootLayout.setContentsMargins(16, 16, 16, 16)
        self.loadingLabel = QLabel(self.centralwidget)
        self.loadingLabel.setObjectName(u"loadingLabel")

        self.rootLayout.addWidget(self.loadingLabel)

        self.loadingCard = QWidget(self.centralwidget)
        self.loadingCard.setObjectName(u"loadingCard")
        self.loadingCardLayout = QHBoxLayout(self.loadingCard)
        self.loadingCardLayout.setSpacing(10)
        self.loadingCardLayout.setObjectName(u"loadingCardLayout")
        self.loadingCardLayout.setContentsMargins(12, 12, 12, 12)
        self.skeletonAvatar = QCustomSkeleton(self.loadingCard)
        self.skeletonAvatar.setObjectName(u"skeletonAvatar")

        self.loadingCardLayout.addWidget(self.skeletonAvatar)

        self.skeletonLines = QVBoxLayout()
        self.skeletonLines.setSpacing(8)
        self.skeletonLines.setObjectName(u"skeletonLines")
        self.skeletonLine1 = QCustomSkeleton(self.loadingCard)
        self.skeletonLine1.setObjectName(u"skeletonLine1")

        self.skeletonLines.addWidget(self.skeletonLine1)

        self.skeletonLine2 = QCustomSkeleton(self.loadingCard)
        self.skeletonLine2.setObjectName(u"skeletonLine2")

        self.skeletonLines.addWidget(self.skeletonLine2)

        self.skeletonSpacer = QSpacerItem(10, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.skeletonLines.addItem(self.skeletonSpacer)


        self.loadingCardLayout.addLayout(self.skeletonLines)


        self.rootLayout.addWidget(self.loadingCard)

        self.teamLabel = QLabel(self.centralwidget)
        self.teamLabel.setObjectName(u"teamLabel")

        self.rootLayout.addWidget(self.teamLabel)

        self.avatarRow = QHBoxLayout()
        self.avatarRow.setObjectName(u"avatarRow")
        self.avatarGroup = QCustomAvatarGroup(self.centralwidget)
        self.avatarGroup.setObjectName(u"avatarGroup")
        self.avatarGroup.setProperty(u"maxVisible", 4)

        self.avatarRow.addWidget(self.avatarGroup)

        self.avatarSpacer = QSpacerItem(10, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.avatarRow.addItem(self.avatarSpacer)


        self.rootLayout.addLayout(self.avatarRow)

        self.activityLabel = QLabel(self.centralwidget)
        self.activityLabel.setObjectName(u"activityLabel")

        self.rootLayout.addWidget(self.activityLabel)

        self.timeline = QCustomTimeline(self.centralwidget)
        self.timeline.setObjectName(u"timeline")

        self.rootLayout.addWidget(self.timeline)

        self.rootLayout.setStretch(5, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Skeleton / Avatars / Timeline", None))
        self.loadingLabel.setText(QCoreApplication.translate("MainWindow", u"Loading card (swaps after 1.5s):", None))
        self.skeletonAvatar.setProperty(u"shape", QCoreApplication.translate("MainWindow", u"circle", None))
        self.teamLabel.setText(QCoreApplication.translate("MainWindow", u"Team:", None))
        self.activityLabel.setText(QCoreApplication.translate("MainWindow", u"Activity:", None))
    # retranslateUi

