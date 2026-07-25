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
    QPushButton, QSizePolicy, QSpacerItem, QSplitter,
    QVBoxLayout, QWidget)

from Custom_Widgets.QCustomComponentContainer import QCustomComponentContainer
from Custom_Widgets.QCustomQMainWindow import QCustomQMainWindow
from Custom_Widgets.QCustomQPushButton import QCustomQPushButton
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1280, 820)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.rootLayout = QVBoxLayout(self.centralwidget)
        self.rootLayout.setSpacing(0)
        self.rootLayout.setObjectName(u"rootLayout")
        self.rootLayout.setContentsMargins(0, 0, 0, 0)
        self.topBar = QFrame(self.centralwidget)
        self.topBar.setObjectName(u"topBar")
        self.topBar.setFrameShape(QFrame.StyledPanel)
        self.topBar.setMinimumSize(QSize(0, 56))
        self.topBar.setMaximumSize(QSize(16777215, 56))
        self.topBarLayout = QHBoxLayout(self.topBar)
        self.topBarLayout.setSpacing(8)
        self.topBarLayout.setObjectName(u"topBarLayout")
        self.topBarLayout.setContentsMargins(14, 8, 14, 8)
        self.appMark = QLabel(self.topBar)
        self.appMark.setObjectName(u"appMark")
        self.appMark.setMinimumSize(QSize(30, 30))
        self.appMark.setMaximumSize(QSize(30, 30))

        self.topBarLayout.addWidget(self.appMark)

        self.tabNew = QCustomQPushButton(self.topBar)
        self.tabNew.setObjectName(u"tabNew")
        self.tabNew.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.topBarLayout.addWidget(self.tabNew)

        self.tabFramer = QCustomQPushButton(self.topBar)
        self.tabFramer.setObjectName(u"tabFramer")
        self.tabFramer.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.topBarLayout.addWidget(self.tabFramer)

        self.tabUntitled = QCustomQPushButton(self.topBar)
        self.tabUntitled.setObjectName(u"tabUntitled")
        self.tabUntitled.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.topBarLayout.addWidget(self.tabUntitled)

        self.tabAdd = QCustomQPushButton(self.topBar)
        self.tabAdd.setObjectName(u"tabAdd")
        self.tabAdd.setMinimumSize(QSize(30, 30))
        self.tabAdd.setMaximumSize(QSize(30, 30))
        self.tabAdd.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.topBarLayout.addWidget(self.tabAdd)

        self.topSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.topBarLayout.addItem(self.topSpacer)

        self.navPrev = QCustomQPushButton(self.topBar)
        self.navPrev.setObjectName(u"navPrev")
        self.navPrev.setMinimumSize(QSize(32, 32))
        self.navPrev.setMaximumSize(QSize(32, 32))

        self.topBarLayout.addWidget(self.navPrev)

        self.navNext = QCustomQPushButton(self.topBar)
        self.navNext.setObjectName(u"navNext")
        self.navNext.setMinimumSize(QSize(32, 32))
        self.navNext.setMaximumSize(QSize(32, 32))

        self.topBarLayout.addWidget(self.navNext)

        self.durationBtn = QCustomQPushButton(self.topBar)
        self.durationBtn.setObjectName(u"durationBtn")
        self.durationBtn.setMinimumSize(QSize(66, 32))

        self.topBarLayout.addWidget(self.durationBtn)

        self.codeBtn = QCustomQPushButton(self.topBar)
        self.codeBtn.setObjectName(u"codeBtn")
        self.codeBtn.setMinimumSize(QSize(36, 32))
        self.codeBtn.setMaximumSize(QSize(36, 32))

        self.topBarLayout.addWidget(self.codeBtn)

        self.playBtn = QCustomQPushButton(self.topBar)
        self.playBtn.setObjectName(u"playBtn")
        self.playBtn.setMinimumSize(QSize(36, 32))
        self.playBtn.setMaximumSize(QSize(36, 32))

        self.topBarLayout.addWidget(self.playBtn)

        self.shareBtn = QCustomQPushButton(self.topBar)
        self.shareBtn.setObjectName(u"shareBtn")
        self.shareBtn.setMinimumSize(QSize(36, 32))
        self.shareBtn.setMaximumSize(QSize(36, 32))

        self.topBarLayout.addWidget(self.shareBtn)

        self.exportBtn = QCustomQPushButton(self.topBar)
        self.exportBtn.setObjectName(u"exportBtn")
        self.exportBtn.setMinimumSize(QSize(88, 32))
        self.exportBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.topBarLayout.addWidget(self.exportBtn)


        self.rootLayout.addWidget(self.topBar)

        self.bodyLayout = QHBoxLayout()
        self.bodyLayout.setSpacing(0)
        self.bodyLayout.setObjectName(u"bodyLayout")
        self.bodyLayout.setContentsMargins(0, 0, 0, 0)
        self.leftRail = QFrame(self.centralwidget)
        self.leftRail.setObjectName(u"leftRail")
        self.leftRail.setFrameShape(QFrame.StyledPanel)
        self.leftRail.setMinimumSize(QSize(54, 0))
        self.leftRail.setMaximumSize(QSize(54, 16777215))
        self.leftRailLayout = QVBoxLayout(self.leftRail)
        self.leftRailLayout.setSpacing(6)
        self.leftRailLayout.setObjectName(u"leftRailLayout")
        self.leftRailLayout.setContentsMargins(10, 12, 10, 12)
        self.rlText = QCustomQPushButton(self.leftRail)
        self.rlText.setObjectName(u"rlText")
        self.rlText.setMinimumSize(QSize(34, 34))
        self.rlText.setMaximumSize(QSize(34, 34))

        self.leftRailLayout.addWidget(self.rlText)

        self.rlLayers = QCustomQPushButton(self.leftRail)
        self.rlLayers.setObjectName(u"rlLayers")
        self.rlLayers.setMinimumSize(QSize(34, 34))
        self.rlLayers.setMaximumSize(QSize(34, 34))

        self.leftRailLayout.addWidget(self.rlLayers)

        self.rlPen = QCustomQPushButton(self.leftRail)
        self.rlPen.setObjectName(u"rlPen")
        self.rlPen.setMinimumSize(QSize(34, 34))
        self.rlPen.setMaximumSize(QSize(34, 34))

        self.leftRailLayout.addWidget(self.rlPen)

        self.rlBrush = QCustomQPushButton(self.leftRail)
        self.rlBrush.setObjectName(u"rlBrush")
        self.rlBrush.setMinimumSize(QSize(34, 34))
        self.rlBrush.setMaximumSize(QSize(34, 34))

        self.leftRailLayout.addWidget(self.rlBrush)

        self.rlGrid = QCustomQPushButton(self.leftRail)
        self.rlGrid.setObjectName(u"rlGrid")
        self.rlGrid.setMinimumSize(QSize(34, 34))
        self.rlGrid.setMaximumSize(QSize(34, 34))

        self.leftRailLayout.addWidget(self.rlGrid)

        self.rlAttach = QCustomQPushButton(self.leftRail)
        self.rlAttach.setObjectName(u"rlAttach")
        self.rlAttach.setMinimumSize(QSize(34, 34))
        self.rlAttach.setMaximumSize(QSize(34, 34))

        self.leftRailLayout.addWidget(self.rlAttach)

        self.railSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.leftRailLayout.addItem(self.railSpacer)

        self.themeToggle = QCustomQPushButton(self.leftRail)
        self.themeToggle.setObjectName(u"themeToggle")
        self.themeToggle.setMinimumSize(QSize(34, 34))
        self.themeToggle.setMaximumSize(QSize(34, 34))
        self.themeToggle.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.leftRailLayout.addWidget(self.themeToggle)

        self.fabAdd = QCustomQPushButton(self.leftRail)
        self.fabAdd.setObjectName(u"fabAdd")
        self.fabAdd.setMinimumSize(QSize(34, 34))
        self.fabAdd.setMaximumSize(QSize(34, 34))

        self.leftRailLayout.addWidget(self.fabAdd)


        self.bodyLayout.addWidget(self.leftRail)

        self.mainSplitter = QSplitter(self.centralwidget)
        self.mainSplitter.setObjectName(u"mainSplitter")
        self.mainSplitter.setOrientation(Qt.Horizontal)
        self.mainSplitter.setHandleWidth(10)
        self.mainSplitter.setChildrenCollapsible(False)
        self.leftColumn = QSplitter(self.mainSplitter)
        self.leftColumn.setObjectName(u"leftColumn")
        self.leftColumn.setOrientation(Qt.Vertical)
        self.leftColumn.setHandleWidth(10)
        self.leftColumn.setChildrenCollapsible(False)
        self.canvasContainer = QCustomComponentContainer(self.leftColumn)
        self.canvasContainer.setObjectName(u"canvasContainer")
        self.canvasContainer.setProperty(u"previewComponent", False)
        self.leftColumn.addWidget(self.canvasContainer)
        self.thoughtsContainer = QCustomComponentContainer(self.leftColumn)
        self.thoughtsContainer.setObjectName(u"thoughtsContainer")
        self.thoughtsContainer.setMinimumSize(QSize(0, 150))
        self.thoughtsContainer.setProperty(u"previewComponent", False)
        self.leftColumn.addWidget(self.thoughtsContainer)
        self.mainSplitter.addWidget(self.leftColumn)
        self.rightColumn = QSplitter(self.mainSplitter)
        self.rightColumn.setObjectName(u"rightColumn")
        self.rightColumn.setOrientation(Qt.Vertical)
        self.rightColumn.setHandleWidth(10)
        self.rightColumn.setChildrenCollapsible(False)
        self.rightColumn.setMinimumSize(QSize(360, 0))
        self.previewContainer = QCustomComponentContainer(self.rightColumn)
        self.previewContainer.setObjectName(u"previewContainer")
        self.previewContainer.setProperty(u"previewComponent", False)
        self.rightColumn.addWidget(self.previewContainer)
        self.timelineContainer = QCustomComponentContainer(self.rightColumn)
        self.timelineContainer.setObjectName(u"timelineContainer")
        self.timelineContainer.setMinimumSize(QSize(0, 150))
        self.timelineContainer.setMaximumSize(QSize(16777215, 210))
        self.timelineContainer.setProperty(u"previewComponent", False)
        self.rightColumn.addWidget(self.timelineContainer)
        self.mainSplitter.addWidget(self.rightColumn)

        self.bodyLayout.addWidget(self.mainSplitter)

        self.rightRail = QFrame(self.centralwidget)
        self.rightRail.setObjectName(u"rightRail")
        self.rightRail.setFrameShape(QFrame.StyledPanel)
        self.rightRail.setMinimumSize(QSize(50, 0))
        self.rightRail.setMaximumSize(QSize(50, 16777215))
        self.rightRailLayout = QVBoxLayout(self.rightRail)
        self.rightRailLayout.setSpacing(6)
        self.rightRailLayout.setObjectName(u"rightRailLayout")
        self.rightRailLayout.setContentsMargins(9, 12, 9, 12)
        self.rrCursor = QCustomQPushButton(self.rightRail)
        self.rrCursor.setObjectName(u"rrCursor")
        self.rrCursor.setMinimumSize(QSize(32, 32))
        self.rrCursor.setMaximumSize(QSize(32, 32))

        self.rightRailLayout.addWidget(self.rrCursor)

        self.rrStar = QCustomQPushButton(self.rightRail)
        self.rrStar.setObjectName(u"rrStar")
        self.rrStar.setMinimumSize(QSize(32, 32))
        self.rrStar.setMaximumSize(QSize(32, 32))

        self.rightRailLayout.addWidget(self.rrStar)

        self.rrDrop = QCustomQPushButton(self.rightRail)
        self.rrDrop.setObjectName(u"rrDrop")
        self.rrDrop.setMinimumSize(QSize(32, 32))
        self.rrDrop.setMaximumSize(QSize(32, 32))

        self.rightRailLayout.addWidget(self.rrDrop)

        self.rrLock = QCustomQPushButton(self.rightRail)
        self.rrLock.setObjectName(u"rrLock")
        self.rrLock.setMinimumSize(QSize(32, 32))
        self.rrLock.setMaximumSize(QSize(32, 32))

        self.rightRailLayout.addWidget(self.rrLock)

        self.rrBulb = QCustomQPushButton(self.rightRail)
        self.rrBulb.setObjectName(u"rrBulb")
        self.rrBulb.setMinimumSize(QSize(32, 32))
        self.rrBulb.setMaximumSize(QSize(32, 32))

        self.rightRailLayout.addWidget(self.rrBulb)

        self.rightRailSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.rightRailLayout.addItem(self.rightRailSpacer)


        self.bodyLayout.addWidget(self.rightRail)


        self.rootLayout.addLayout(self.bodyLayout)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Node Studio", None))
        self.appMark.setText("")
        self.tabNew.setText(QCoreApplication.translate("MainWindow", u"New Character", None))
        self.tabFramer.setText(QCoreApplication.translate("MainWindow", u"Framer Templates", None))
        self.tabUntitled.setText(QCoreApplication.translate("MainWindow", u"Untitled", None))
        self.tabAdd.setText("")
        self.navPrev.setText("")
        self.navNext.setText("")
        self.durationBtn.setText(QCoreApplication.translate("MainWindow", u"10s", None))
        self.codeBtn.setText("")
        self.playBtn.setText("")
        self.shareBtn.setText("")
        self.exportBtn.setText(QCoreApplication.translate("MainWindow", u"Export", None))
        self.rlText.setText("")
        self.rlLayers.setText("")
        self.rlPen.setText("")
        self.rlBrush.setText("")
        self.rlGrid.setText("")
        self.rlAttach.setText("")
        self.themeToggle.setText("")
        self.fabAdd.setText("")
        self.canvasContainer.setProperty(u"filePath", QCoreApplication.translate("MainWindow", u"ui/CanvasComponent.ui", None))
        self.thoughtsContainer.setProperty(u"filePath", QCoreApplication.translate("MainWindow", u"ui/ThoughtsComponent.ui", None))
        self.previewContainer.setProperty(u"filePath", QCoreApplication.translate("MainWindow", u"ui/PreviewComponent.ui", None))
        self.timelineContainer.setProperty(u"filePath", QCoreApplication.translate("MainWindow", u"ui/TimelineComponent.ui", None))
        self.rrCursor.setText("")
        self.rrStar.setText("")
        self.rrDrop.setText("")
        self.rrLock.setText("")
        self.rrBulb.setText("")
    # retranslateUi

