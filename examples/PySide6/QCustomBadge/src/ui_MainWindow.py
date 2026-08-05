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

from Custom_Widgets.QCustomBadge import QCustomBadge
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(560, 380)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.rootLayout = QVBoxLayout(self.centralwidget)
        self.rootLayout.setSpacing(16)
        self.rootLayout.setObjectName(u"rootLayout")
        self.rootLayout.setContentsMargins(16, 16, 16, 16)
        self.sectionVariants = QLabel(self.centralwidget)
        self.sectionVariants.setObjectName(u"sectionVariants")

        self.rootLayout.addWidget(self.sectionVariants)

        self.variantRow = QHBoxLayout()
        self.variantRow.setSpacing(8)
        self.variantRow.setObjectName(u"variantRow")
        self.badgeDefault = QCustomBadge(self.centralwidget)
        self.badgeDefault.setObjectName(u"badgeDefault")

        self.variantRow.addWidget(self.badgeDefault)

        self.badgePrimary = QCustomBadge(self.centralwidget)
        self.badgePrimary.setObjectName(u"badgePrimary")

        self.variantRow.addWidget(self.badgePrimary)

        self.badgeSecondary = QCustomBadge(self.centralwidget)
        self.badgeSecondary.setObjectName(u"badgeSecondary")

        self.variantRow.addWidget(self.badgeSecondary)

        self.badgeSuccess = QCustomBadge(self.centralwidget)
        self.badgeSuccess.setObjectName(u"badgeSuccess")

        self.variantRow.addWidget(self.badgeSuccess)

        self.badgeWarning = QCustomBadge(self.centralwidget)
        self.badgeWarning.setObjectName(u"badgeWarning")

        self.variantRow.addWidget(self.badgeWarning)

        self.badgeDestructive = QCustomBadge(self.centralwidget)
        self.badgeDestructive.setObjectName(u"badgeDestructive")

        self.variantRow.addWidget(self.badgeDestructive)

        self.badgeInfo = QCustomBadge(self.centralwidget)
        self.badgeInfo.setObjectName(u"badgeInfo")

        self.variantRow.addWidget(self.badgeInfo)

        self.badgeOutline = QCustomBadge(self.centralwidget)
        self.badgeOutline.setObjectName(u"badgeOutline")

        self.variantRow.addWidget(self.badgeOutline)

        self.variantSpacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.variantRow.addItem(self.variantSpacer)


        self.rootLayout.addLayout(self.variantRow)

        self.sectionSizes = QLabel(self.centralwidget)
        self.sectionSizes.setObjectName(u"sectionSizes")

        self.rootLayout.addWidget(self.sectionSizes)

        self.sizeRow = QHBoxLayout()
        self.sizeRow.setSpacing(8)
        self.sizeRow.setObjectName(u"sizeRow")
        self.badgeSizeSm = QCustomBadge(self.centralwidget)
        self.badgeSizeSm.setObjectName(u"badgeSizeSm")

        self.sizeRow.addWidget(self.badgeSizeSm)

        self.badgeSizeMd = QCustomBadge(self.centralwidget)
        self.badgeSizeMd.setObjectName(u"badgeSizeMd")

        self.sizeRow.addWidget(self.badgeSizeMd)

        self.badgeSizeLg = QCustomBadge(self.centralwidget)
        self.badgeSizeLg.setObjectName(u"badgeSizeLg")

        self.sizeRow.addWidget(self.badgeSizeLg)

        self.dotSm = QCustomBadge(self.centralwidget)
        self.dotSm.setObjectName(u"dotSm")
        self.dotSm.setProperty(u"dot", True)

        self.sizeRow.addWidget(self.dotSm)

        self.dotMd = QCustomBadge(self.centralwidget)
        self.dotMd.setObjectName(u"dotMd")
        self.dotMd.setProperty(u"dot", True)

        self.sizeRow.addWidget(self.dotMd)

        self.dotLg = QCustomBadge(self.centralwidget)
        self.dotLg.setObjectName(u"dotLg")
        self.dotLg.setProperty(u"dot", True)

        self.sizeRow.addWidget(self.dotLg)

        self.sizeSpacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.sizeRow.addItem(self.sizeSpacer)


        self.rootLayout.addLayout(self.sizeRow)

        self.sectionCount = QLabel(self.centralwidget)
        self.sectionCount.setObjectName(u"sectionCount")

        self.rootLayout.addWidget(self.sectionCount)

        self.countRow = QHBoxLayout()
        self.countRow.setSpacing(8)
        self.countRow.setObjectName(u"countRow")
        self.minusButton = QPushButton(self.centralwidget)
        self.minusButton.setObjectName(u"minusButton")

        self.countRow.addWidget(self.minusButton)

        self.countBadge = QCustomBadge(self.centralwidget)
        self.countBadge.setObjectName(u"countBadge")

        self.countRow.addWidget(self.countBadge)

        self.plusButton = QPushButton(self.centralwidget)
        self.plusButton.setObjectName(u"plusButton")

        self.countRow.addWidget(self.plusButton)

        self.countSpacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.countRow.addItem(self.countSpacer)


        self.rootLayout.addLayout(self.countRow)

        self.sectionOverlay = QLabel(self.centralwidget)
        self.sectionOverlay.setObjectName(u"sectionOverlay")

        self.rootLayout.addWidget(self.sectionOverlay)

        self.overlayRow = QHBoxLayout()
        self.overlayRow.setObjectName(u"overlayRow")
        self.inboxButton = QPushButton(self.centralwidget)
        self.inboxButton.setObjectName(u"inboxButton")
        self.inboxButton.setMinimumSize(QSize(0, 40))

        self.overlayRow.addWidget(self.inboxButton)

        self.overlayBadge = QCustomBadge(self.centralwidget)
        self.overlayBadge.setObjectName(u"overlayBadge")

        self.overlayRow.addWidget(self.overlayBadge)

        self.overlaySpacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.overlayRow.addItem(self.overlaySpacer)


        self.rootLayout.addLayout(self.overlayRow)

        self.bottomSpacer = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.rootLayout.addItem(self.bottomSpacer)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"QCustomBadge", None))
        self.sectionVariants.setText(QCoreApplication.translate("MainWindow", u"Variants", None))
        self.badgeDefault.setText(QCoreApplication.translate("MainWindow", u"Default", None))
        self.badgePrimary.setText(QCoreApplication.translate("MainWindow", u"Primary", None))
        self.badgePrimary.setProperty(u"variant", QCoreApplication.translate("MainWindow", u"primary", None))
        self.badgeSecondary.setText(QCoreApplication.translate("MainWindow", u"Secondary", None))
        self.badgeSecondary.setProperty(u"variant", QCoreApplication.translate("MainWindow", u"secondary", None))
        self.badgeSuccess.setText(QCoreApplication.translate("MainWindow", u"Success", None))
        self.badgeSuccess.setProperty(u"variant", QCoreApplication.translate("MainWindow", u"success", None))
        self.badgeWarning.setText(QCoreApplication.translate("MainWindow", u"Warning", None))
        self.badgeWarning.setProperty(u"variant", QCoreApplication.translate("MainWindow", u"warning", None))
        self.badgeDestructive.setText(QCoreApplication.translate("MainWindow", u"Destructive", None))
        self.badgeDestructive.setProperty(u"variant", QCoreApplication.translate("MainWindow", u"destructive", None))
        self.badgeInfo.setText(QCoreApplication.translate("MainWindow", u"Info", None))
        self.badgeInfo.setProperty(u"variant", QCoreApplication.translate("MainWindow", u"info", None))
        self.badgeOutline.setText(QCoreApplication.translate("MainWindow", u"Outline", None))
        self.badgeOutline.setProperty(u"variant", QCoreApplication.translate("MainWindow", u"outline", None))
        self.sectionSizes.setText(QCoreApplication.translate("MainWindow", u"Sizes & dot", None))
        self.badgeSizeSm.setText(QCoreApplication.translate("MainWindow", u"sm", None))
        self.badgeSizeSm.setProperty(u"variant", QCoreApplication.translate("MainWindow", u"primary", None))
        self.badgeSizeSm.setProperty(u"sizeVariant", QCoreApplication.translate("MainWindow", u"sm", None))
        self.badgeSizeMd.setText(QCoreApplication.translate("MainWindow", u"md", None))
        self.badgeSizeMd.setProperty(u"variant", QCoreApplication.translate("MainWindow", u"primary", None))
        self.badgeSizeMd.setProperty(u"sizeVariant", QCoreApplication.translate("MainWindow", u"md", None))
        self.badgeSizeLg.setText(QCoreApplication.translate("MainWindow", u"lg", None))
        self.badgeSizeLg.setProperty(u"variant", QCoreApplication.translate("MainWindow", u"primary", None))
        self.badgeSizeLg.setProperty(u"sizeVariant", QCoreApplication.translate("MainWindow", u"lg", None))
        self.dotSm.setProperty(u"variant", QCoreApplication.translate("MainWindow", u"success", None))
        self.dotSm.setProperty(u"sizeVariant", QCoreApplication.translate("MainWindow", u"sm", None))
        self.dotMd.setProperty(u"variant", QCoreApplication.translate("MainWindow", u"success", None))
        self.dotMd.setProperty(u"sizeVariant", QCoreApplication.translate("MainWindow", u"md", None))
        self.dotLg.setProperty(u"variant", QCoreApplication.translate("MainWindow", u"success", None))
        self.dotLg.setProperty(u"sizeVariant", QCoreApplication.translate("MainWindow", u"lg", None))
        self.sectionCount.setText(QCoreApplication.translate("MainWindow", u"Count (click +/- )", None))
        self.minusButton.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.countBadge.setProperty(u"variant", QCoreApplication.translate("MainWindow", u"destructive", None))
        self.plusButton.setText(QCoreApplication.translate("MainWindow", u"+", None))
        self.sectionOverlay.setText(QCoreApplication.translate("MainWindow", u"Attached overlay", None))
        self.inboxButton.setText(QCoreApplication.translate("MainWindow", u"  Inbox  ", None))
        self.overlayBadge.setProperty(u"variant", QCoreApplication.translate("MainWindow", u"primary", None))
    # retranslateUi

