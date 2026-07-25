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
        icon = QIcon()
        icon.addFile(u"theme-icons:icons/material_design/auto_awesome.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.tabNew.setIcon(icon)
        self.tabNew.setIconSize(QSize(14, 14))

        self.topBarLayout.addWidget(self.tabNew)

        self.tabFramer = QCustomQPushButton(self.topBar)
        self.tabFramer.setObjectName(u"tabFramer")
        self.tabFramer.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon1 = QIcon()
        icon1.addFile(u"theme-icons:icons/material_design/dashboard.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.tabFramer.setIcon(icon1)
        self.tabFramer.setIconSize(QSize(14, 14))

        self.topBarLayout.addWidget(self.tabFramer)

        self.tabUntitled = QCustomQPushButton(self.topBar)
        self.tabUntitled.setObjectName(u"tabUntitled")
        self.tabUntitled.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon2 = QIcon()
        icon2.addFile(u"theme-icons:icons/feather/hexagon.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.tabUntitled.setIcon(icon2)
        self.tabUntitled.setIconSize(QSize(14, 14))

        self.topBarLayout.addWidget(self.tabUntitled)

        self.tabAdd = QCustomQPushButton(self.topBar)
        self.tabAdd.setObjectName(u"tabAdd")
        self.tabAdd.setMinimumSize(QSize(30, 30))
        self.tabAdd.setMaximumSize(QSize(30, 30))
        self.tabAdd.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon3 = QIcon()
        icon3.addFile(u"theme-icons:icons/material_design/add.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.tabAdd.setIcon(icon3)
        self.tabAdd.setIconSize(QSize(18, 18))

        self.topBarLayout.addWidget(self.tabAdd)

        self.topSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.topBarLayout.addItem(self.topSpacer)

        self.navPrev = QCustomQPushButton(self.topBar)
        self.navPrev.setObjectName(u"navPrev")
        self.navPrev.setMinimumSize(QSize(32, 32))
        self.navPrev.setMaximumSize(QSize(32, 32))
        icon4 = QIcon()
        icon4.addFile(u"theme-icons:icons/material_design/arrow_back_ios_new.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.navPrev.setIcon(icon4)
        self.navPrev.setIconSize(QSize(16, 16))

        self.topBarLayout.addWidget(self.navPrev)

        self.navNext = QCustomQPushButton(self.topBar)
        self.navNext.setObjectName(u"navNext")
        self.navNext.setMinimumSize(QSize(32, 32))
        self.navNext.setMaximumSize(QSize(32, 32))
        icon5 = QIcon()
        icon5.addFile(u"theme-icons:icons/material_design/arrow_forward_ios.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.navNext.setIcon(icon5)
        self.navNext.setIconSize(QSize(16, 16))

        self.topBarLayout.addWidget(self.navNext)

        self.durationBtn = QCustomQPushButton(self.topBar)
        self.durationBtn.setObjectName(u"durationBtn")
        self.durationBtn.setMinimumSize(QSize(66, 32))
        icon6 = QIcon()
        icon6.addFile(u"theme-icons:icons/material_design/timer.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.durationBtn.setIcon(icon6)
        self.durationBtn.setIconSize(QSize(15, 15))

        self.topBarLayout.addWidget(self.durationBtn)

        self.codeBtn = QCustomQPushButton(self.topBar)
        self.codeBtn.setObjectName(u"codeBtn")
        self.codeBtn.setMinimumSize(QSize(36, 32))
        self.codeBtn.setMaximumSize(QSize(36, 32))
        icon7 = QIcon()
        icon7.addFile(u"theme-icons:icons/feather/code.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.codeBtn.setIcon(icon7)
        self.codeBtn.setIconSize(QSize(18, 18))

        self.topBarLayout.addWidget(self.codeBtn)

        self.playBtn = QCustomQPushButton(self.topBar)
        self.playBtn.setObjectName(u"playBtn")
        self.playBtn.setMinimumSize(QSize(36, 32))
        self.playBtn.setMaximumSize(QSize(36, 32))
        icon8 = QIcon()
        icon8.addFile(u"theme-icons:icons/material_design/play_arrow.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.playBtn.setIcon(icon8)
        self.playBtn.setIconSize(QSize(18, 18))

        self.topBarLayout.addWidget(self.playBtn)

        self.shareBtn = QCustomQPushButton(self.topBar)
        self.shareBtn.setObjectName(u"shareBtn")
        self.shareBtn.setMinimumSize(QSize(36, 32))
        self.shareBtn.setMaximumSize(QSize(36, 32))
        icon9 = QIcon()
        icon9.addFile(u"theme-icons:icons/material_design/ios_share.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.shareBtn.setIcon(icon9)
        self.shareBtn.setIconSize(QSize(18, 18))

        self.topBarLayout.addWidget(self.shareBtn)

        self.exportBtn = QCustomQPushButton(self.topBar)
        self.exportBtn.setObjectName(u"exportBtn")
        self.exportBtn.setMinimumSize(QSize(88, 32))
        self.exportBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon10 = QIcon()
        icon10.addFile(u"theme-icons:icons/material_design/bolt.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.exportBtn.setIcon(icon10)
        self.exportBtn.setIconSize(QSize(16, 16))

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
        icon11 = QIcon()
        icon11.addFile(u"theme-icons:icons/material_design/text_fields.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.rlText.setIcon(icon11)
        self.rlText.setIconSize(QSize(20, 20))

        self.leftRailLayout.addWidget(self.rlText)

        self.rlLayers = QCustomQPushButton(self.leftRail)
        self.rlLayers.setObjectName(u"rlLayers")
        self.rlLayers.setMinimumSize(QSize(34, 34))
        self.rlLayers.setMaximumSize(QSize(34, 34))
        icon12 = QIcon()
        icon12.addFile(u"theme-icons:icons/feather/layers.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.rlLayers.setIcon(icon12)
        self.rlLayers.setIconSize(QSize(20, 20))

        self.leftRailLayout.addWidget(self.rlLayers)

        self.rlPen = QCustomQPushButton(self.leftRail)
        self.rlPen.setObjectName(u"rlPen")
        self.rlPen.setMinimumSize(QSize(34, 34))
        self.rlPen.setMaximumSize(QSize(34, 34))
        icon13 = QIcon()
        icon13.addFile(u"theme-icons:icons/material_design/edit_note.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.rlPen.setIcon(icon13)
        self.rlPen.setIconSize(QSize(20, 20))

        self.leftRailLayout.addWidget(self.rlPen)

        self.rlBrush = QCustomQPushButton(self.leftRail)
        self.rlBrush.setObjectName(u"rlBrush")
        self.rlBrush.setMinimumSize(QSize(34, 34))
        self.rlBrush.setMaximumSize(QSize(34, 34))
        icon14 = QIcon()
        icon14.addFile(u"theme-icons:icons/material_design/brush.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.rlBrush.setIcon(icon14)
        self.rlBrush.setIconSize(QSize(20, 20))

        self.leftRailLayout.addWidget(self.rlBrush)

        self.rlGrid = QCustomQPushButton(self.leftRail)
        self.rlGrid.setObjectName(u"rlGrid")
        self.rlGrid.setMinimumSize(QSize(34, 34))
        self.rlGrid.setMaximumSize(QSize(34, 34))
        icon15 = QIcon()
        icon15.addFile(u"theme-icons:icons/material_design/grid_view.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.rlGrid.setIcon(icon15)
        self.rlGrid.setIconSize(QSize(20, 20))

        self.leftRailLayout.addWidget(self.rlGrid)

        self.rlAttach = QCustomQPushButton(self.leftRail)
        self.rlAttach.setObjectName(u"rlAttach")
        self.rlAttach.setMinimumSize(QSize(34, 34))
        self.rlAttach.setMaximumSize(QSize(34, 34))
        icon16 = QIcon()
        icon16.addFile(u"theme-icons:icons/material_design/attach_file.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.rlAttach.setIcon(icon16)
        self.rlAttach.setIconSize(QSize(20, 20))

        self.leftRailLayout.addWidget(self.rlAttach)

        self.railSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.leftRailLayout.addItem(self.railSpacer)

        self.themeToggle = QCustomQPushButton(self.leftRail)
        self.themeToggle.setObjectName(u"themeToggle")
        self.themeToggle.setMinimumSize(QSize(34, 34))
        self.themeToggle.setMaximumSize(QSize(34, 34))
        self.themeToggle.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon17 = QIcon()
        icon17.addFile(u"theme-icons:icons/material_design/dark_mode.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.themeToggle.setIcon(icon17)
        self.themeToggle.setIconSize(QSize(20, 20))

        self.leftRailLayout.addWidget(self.themeToggle)

        self.fabAdd = QCustomQPushButton(self.leftRail)
        self.fabAdd.setObjectName(u"fabAdd")
        self.fabAdd.setMinimumSize(QSize(34, 34))
        self.fabAdd.setMaximumSize(QSize(34, 34))
        self.fabAdd.setIcon(icon3)
        self.fabAdd.setIconSize(QSize(20, 20))

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
        icon18 = QIcon()
        icon18.addFile(u"theme-icons:icons/material_design/near_me.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.rrCursor.setIcon(icon18)
        self.rrCursor.setIconSize(QSize(18, 18))

        self.rightRailLayout.addWidget(self.rrCursor)

        self.rrStar = QCustomQPushButton(self.rightRail)
        self.rrStar.setObjectName(u"rrStar")
        self.rrStar.setMinimumSize(QSize(32, 32))
        self.rrStar.setMaximumSize(QSize(32, 32))
        icon19 = QIcon()
        icon19.addFile(u"theme-icons:icons/material_design/star_border.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.rrStar.setIcon(icon19)
        self.rrStar.setIconSize(QSize(18, 18))

        self.rightRailLayout.addWidget(self.rrStar)

        self.rrDrop = QCustomQPushButton(self.rightRail)
        self.rrDrop.setObjectName(u"rrDrop")
        self.rrDrop.setMinimumSize(QSize(32, 32))
        self.rrDrop.setMaximumSize(QSize(32, 32))
        icon20 = QIcon()
        icon20.addFile(u"theme-icons:icons/material_design/opacity.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.rrDrop.setIcon(icon20)
        self.rrDrop.setIconSize(QSize(18, 18))

        self.rightRailLayout.addWidget(self.rrDrop)

        self.rrLock = QCustomQPushButton(self.rightRail)
        self.rrLock.setObjectName(u"rrLock")
        self.rrLock.setMinimumSize(QSize(32, 32))
        self.rrLock.setMaximumSize(QSize(32, 32))
        icon21 = QIcon()
        icon21.addFile(u"theme-icons:icons/feather/lock.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.rrLock.setIcon(icon21)
        self.rrLock.setIconSize(QSize(18, 18))

        self.rightRailLayout.addWidget(self.rrLock)

        self.rrBulb = QCustomQPushButton(self.rightRail)
        self.rrBulb.setObjectName(u"rrBulb")
        self.rrBulb.setMinimumSize(QSize(32, 32))
        self.rrBulb.setMaximumSize(QSize(32, 32))
        icon22 = QIcon()
        icon22.addFile(u"theme-icons:icons/material_design/lightbulb.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.rrBulb.setIcon(icon22)
        self.rrBulb.setIconSize(QSize(18, 18))

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

