# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'new_DashboardComponent.ui'
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
    QPushButton, QScrollArea, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

from Custom_Widgets.QCustomCardStack import QCustomCardStack
from Custom_Widgets.QCustomComponent import QCustomComponent
from Custom_Widgets.QCustomDivergingBarChart import QCustomDivergingBarChart
class Ui_DashboardComponent(object):
    def setupUi(self, DashboardComponent):
        if not DashboardComponent.objectName():
            DashboardComponent.setObjectName(u"DashboardComponent")
        DashboardComponent.resize(1200, 860)
        self.dashOuter = QVBoxLayout(DashboardComponent)
        self.dashOuter.setSpacing(0)
        self.dashOuter.setObjectName(u"dashOuter")
        self.dashOuter.setContentsMargins(0, 0, 0, 0)
        self.dashScroll = QScrollArea(DashboardComponent)
        self.dashScroll.setObjectName(u"dashScroll")
        self.dashScroll.setWidgetResizable(True)
        self.dashScroll.setFrameShape(QFrame.NoFrame)
        self.dashScroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.dashScrollContents = QWidget()
        self.dashScrollContents.setObjectName(u"dashScrollContents")
        self.dashScrollContents.setGeometry(QRect(0, 0, 1200, 900))
        self.dashBody = QVBoxLayout(self.dashScrollContents)
        self.dashBody.setSpacing(0)
        self.dashBody.setObjectName(u"dashBody")
        self.dashBody.setContentsMargins(0, 0, 0, 0)
        self.topBar = QWidget(self.dashScrollContents)
        self.topBar.setObjectName(u"topBar")
        self.topBarLayout = QHBoxLayout(self.topBar)
        self.topBarLayout.setSpacing(12)
        self.topBarLayout.setObjectName(u"topBarLayout")
        self.topBarLayout.setContentsMargins(36, 24, 36, 16)
        self.crumbActive = QLabel(self.topBar)
        self.crumbActive.setObjectName(u"crumbActive")

        self.topBarLayout.addWidget(self.crumbActive)

        self.crumbSep = QLabel(self.topBar)
        self.crumbSep.setObjectName(u"crumbSep")
        self.crumbSep.setMinimumSize(QSize(1, 18))
        self.crumbSep.setMaximumSize(QSize(1, 18))
        self.crumbSep.setFrameShape(QFrame.VLine)

        self.topBarLayout.addWidget(self.crumbSep)

        self.crumbHello = QLabel(self.topBar)
        self.crumbHello.setObjectName(u"crumbHello")

        self.topBarLayout.addWidget(self.crumbHello)

        self.topBarSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.topBarLayout.addItem(self.topBarSpacer)

        self.clockLabel = QLabel(self.topBar)
        self.clockLabel.setObjectName(u"clockLabel")

        self.topBarLayout.addWidget(self.clockLabel)


        self.dashBody.addWidget(self.topBar)

        self.pageBody = QWidget(self.dashScrollContents)
        self.pageBody.setObjectName(u"pageBody")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.pageBody.sizePolicy().hasHeightForWidth())
        self.pageBody.setSizePolicy(sizePolicy)
        self.pageBodyLayout = QVBoxLayout(self.pageBody)
        self.pageBodyLayout.setSpacing(22)
        self.pageBodyLayout.setObjectName(u"pageBodyLayout")
        self.pageBodyLayout.setContentsMargins(36, 18, 36, 34)
        self.banner = QFrame(self.pageBody)
        self.banner.setObjectName(u"banner")
        self.banner.setMinimumSize(QSize(0, 112))
        self.banner.setFrameShape(QFrame.StyledPanel)
        self.bannerLayout = QHBoxLayout(self.banner)
        self.bannerLayout.setSpacing(16)
        self.bannerLayout.setObjectName(u"bannerLayout")
        self.bannerLayout.setContentsMargins(30, 22, 24, 22)
        self.bannerTextCol = QVBoxLayout()
        self.bannerTextCol.setSpacing(8)
        self.bannerTextCol.setObjectName(u"bannerTextCol")
        self.bannerTitle = QLabel(self.banner)
        self.bannerTitle.setObjectName(u"bannerTitle")

        self.bannerTextCol.addWidget(self.bannerTitle)

        self.bannerValueRow = QHBoxLayout()
        self.bannerValueRow.setSpacing(14)
        self.bannerValueRow.setObjectName(u"bannerValueRow")
        self.bannerValue = QLabel(self.banner)
        self.bannerValue.setObjectName(u"bannerValue")

        self.bannerValueRow.addWidget(self.bannerValue)

        self.bannerDelta = QWidget(self.banner)
        self.bannerDelta.setObjectName(u"bannerDelta")
        self.bannerDeltaLayout = QHBoxLayout(self.bannerDelta)
        self.bannerDeltaLayout.setSpacing(4)
        self.bannerDeltaLayout.setObjectName(u"bannerDeltaLayout")
        self.bannerDeltaLayout.setContentsMargins(0, 0, 0, 0)

        self.bannerValueRow.addWidget(self.bannerDelta)

        self.bannerValueSpacer = QSpacerItem(10, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.bannerValueRow.addItem(self.bannerValueSpacer)


        self.bannerTextCol.addLayout(self.bannerValueRow)


        self.bannerLayout.addLayout(self.bannerTextCol)

        self.bannerSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.bannerLayout.addItem(self.bannerSpacer)

        self.bannerActions = QHBoxLayout()
        self.bannerActions.setSpacing(10)
        self.bannerActions.setObjectName(u"bannerActions")
        self.addBtn = QPushButton(self.banner)
        self.addBtn.setObjectName(u"addBtn")
        self.addBtn.setMinimumSize(QSize(92, 40))
        self.addBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.bannerActions.addWidget(self.addBtn)

        self.sendBtn = QPushButton(self.banner)
        self.sendBtn.setObjectName(u"sendBtn")
        self.sendBtn.setMinimumSize(QSize(96, 40))
        self.sendBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.bannerActions.addWidget(self.sendBtn)

        self.requestBtn = QPushButton(self.banner)
        self.requestBtn.setObjectName(u"requestBtn")
        self.requestBtn.setMinimumSize(QSize(110, 40))
        self.requestBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.bannerActions.addWidget(self.requestBtn)

        self.moreBtn = QPushButton(self.banner)
        self.moreBtn.setObjectName(u"moreBtn")
        self.moreBtn.setMinimumSize(QSize(40, 40))
        self.moreBtn.setMaximumSize(QSize(40, 40))
        self.moreBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.bannerActions.addWidget(self.moreBtn)


        self.bannerLayout.addLayout(self.bannerActions)


        self.pageBodyLayout.addWidget(self.banner)

        self.cashCard = QFrame(self.pageBody)
        self.cashCard.setObjectName(u"cashCard")
        self.cashCard.setMinimumSize(QSize(0, 280))
        self.cashCard.setFrameShape(QFrame.StyledPanel)
        self.cashCardLayout = QVBoxLayout(self.cashCard)
        self.cashCardLayout.setSpacing(18)
        self.cashCardLayout.setObjectName(u"cashCardLayout")
        self.cashCardLayout.setContentsMargins(24, 20, 24, 20)
        self.cashHead = QHBoxLayout()
        self.cashHead.setSpacing(10)
        self.cashHead.setObjectName(u"cashHead")
        self.cashIcon = QLabel(self.cashCard)
        self.cashIcon.setObjectName(u"cashIcon")
        self.cashIcon.setMinimumSize(QSize(20, 20))
        self.cashIcon.setMaximumSize(QSize(20, 20))

        self.cashHead.addWidget(self.cashIcon)

        self.cashTitle = QLabel(self.cashCard)
        self.cashTitle.setObjectName(u"cashTitle")

        self.cashHead.addWidget(self.cashTitle)

        self.cashHeadSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.cashHead.addItem(self.cashHeadSpacer)

        self.cashSeg = QFrame(self.cashCard)
        self.cashSeg.setObjectName(u"cashSeg")
        self.cashSeg.setFrameShape(QFrame.StyledPanel)
        self.cashSegLayout = QHBoxLayout(self.cashSeg)
        self.cashSegLayout.setSpacing(0)
        self.cashSegLayout.setObjectName(u"cashSegLayout")
        self.cashSegLayout.setContentsMargins(4, 4, 4, 4)
        self.weeklyBtn = QPushButton(self.cashSeg)
        self.weeklyBtn.setObjectName(u"weeklyBtn")
        self.weeklyBtn.setMinimumSize(QSize(72, 30))
        self.weeklyBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.weeklyBtn.setCheckable(True)
        self.weeklyBtn.setAutoExclusive(True)
        self.weeklyBtn.setChecked(True)

        self.cashSegLayout.addWidget(self.weeklyBtn)

        self.dailyBtn = QPushButton(self.cashSeg)
        self.dailyBtn.setObjectName(u"dailyBtn")
        self.dailyBtn.setMinimumSize(QSize(64, 30))
        self.dailyBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.dailyBtn.setCheckable(True)
        self.dailyBtn.setAutoExclusive(True)

        self.cashSegLayout.addWidget(self.dailyBtn)


        self.cashHead.addWidget(self.cashSeg)

        self.manageBtn = QPushButton(self.cashCard)
        self.manageBtn.setObjectName(u"manageBtn")
        self.manageBtn.setMinimumSize(QSize(96, 38))
        self.manageBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.cashHead.addWidget(self.manageBtn)


        self.cashCardLayout.addLayout(self.cashHead)

        self.cashBody = QHBoxLayout()
        self.cashBody.setSpacing(22)
        self.cashBody.setObjectName(u"cashBody")
        self.cashChart = QCustomDivergingBarChart(self.cashCard)
        self.cashChart.setObjectName(u"cashChart")
        self.cashChart.setMinimumSize(QSize(0, 200))
        self.cashChart.setProperty(u"barWidth", 14)
        self.cashChart.setProperty(u"cornerRadius", 3)
        self.cashChart.setProperty(u"zeroGap", 10)

        self.cashBody.addWidget(self.cashChart)

        self.cashDivider = QFrame(self.cashCard)
        self.cashDivider.setObjectName(u"cashDivider")
        self.cashDivider.setMinimumSize(QSize(1, 0))
        self.cashDivider.setMaximumSize(QSize(1, 16777215))
        self.cashDivider.setFrameShape(QFrame.VLine)

        self.cashBody.addWidget(self.cashDivider)

        self.cashSide = QWidget(self.cashCard)
        self.cashSide.setObjectName(u"cashSide")
        self.cashSide.setMinimumSize(QSize(210, 0))
        self.cashSide.setMaximumSize(QSize(230, 16777215))
        self.cashSideLayout = QVBoxLayout(self.cashSide)
        self.cashSideLayout.setSpacing(18)
        self.cashSideLayout.setObjectName(u"cashSideLayout")
        self.cashSideLayout.setContentsMargins(4, 6, 0, 6)
        self.incHead = QHBoxLayout()
        self.incHead.setSpacing(12)
        self.incHead.setObjectName(u"incHead")
        self.incIcon = QLabel(self.cashSide)
        self.incIcon.setObjectName(u"incIcon")
        self.incIcon.setMinimumSize(QSize(40, 40))
        self.incIcon.setMaximumSize(QSize(40, 40))
        self.incIcon.setAlignment(Qt.AlignCenter)

        self.incHead.addWidget(self.incIcon)

        self.incCol = QVBoxLayout()
        self.incCol.setSpacing(3)
        self.incCol.setObjectName(u"incCol")
        self.incLabel = QLabel(self.cashSide)
        self.incLabel.setObjectName(u"incLabel")

        self.incCol.addWidget(self.incLabel)

        self.incValue = QLabel(self.cashSide)
        self.incValue.setObjectName(u"incValue")

        self.incCol.addWidget(self.incValue)


        self.incHead.addLayout(self.incCol)

        self.incSpacer = QSpacerItem(8, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.incHead.addItem(self.incSpacer)

        self.incDelta = QWidget(self.cashSide)
        self.incDelta.setObjectName(u"incDelta")
        self.incDeltaLayout = QHBoxLayout(self.incDelta)
        self.incDeltaLayout.setSpacing(3)
        self.incDeltaLayout.setObjectName(u"incDeltaLayout")
        self.incDeltaLayout.setContentsMargins(0, 0, 0, 0)

        self.incHead.addWidget(self.incDelta)


        self.cashSideLayout.addLayout(self.incHead)

        self.sideDivider = QFrame(self.cashSide)
        self.sideDivider.setObjectName(u"sideDivider")
        self.sideDivider.setMinimumSize(QSize(0, 1))
        self.sideDivider.setMaximumSize(QSize(16777215, 1))
        self.sideDivider.setFrameShape(QFrame.HLine)

        self.cashSideLayout.addWidget(self.sideDivider)

        self.expHead = QHBoxLayout()
        self.expHead.setSpacing(12)
        self.expHead.setObjectName(u"expHead")
        self.expIcon = QLabel(self.cashSide)
        self.expIcon.setObjectName(u"expIcon")
        self.expIcon.setMinimumSize(QSize(40, 40))
        self.expIcon.setMaximumSize(QSize(40, 40))
        self.expIcon.setAlignment(Qt.AlignCenter)

        self.expHead.addWidget(self.expIcon)

        self.expCol = QVBoxLayout()
        self.expCol.setSpacing(3)
        self.expCol.setObjectName(u"expCol")
        self.expLabel = QLabel(self.cashSide)
        self.expLabel.setObjectName(u"expLabel")

        self.expCol.addWidget(self.expLabel)

        self.expValue = QLabel(self.cashSide)
        self.expValue.setObjectName(u"expValue")

        self.expCol.addWidget(self.expValue)


        self.expHead.addLayout(self.expCol)

        self.expSpacer = QSpacerItem(8, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.expHead.addItem(self.expSpacer)

        self.expDelta = QWidget(self.cashSide)
        self.expDelta.setObjectName(u"expDelta")
        self.expDeltaLayout = QHBoxLayout(self.expDelta)
        self.expDeltaLayout.setSpacing(3)
        self.expDeltaLayout.setObjectName(u"expDeltaLayout")
        self.expDeltaLayout.setContentsMargins(0, 0, 0, 0)

        self.expHead.addWidget(self.expDelta)


        self.cashSideLayout.addLayout(self.expHead)

        self.cashSideBottom = QSpacerItem(10, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.cashSideLayout.addItem(self.cashSideBottom)


        self.cashBody.addWidget(self.cashSide)

        self.cashBody.setStretch(0, 1)

        self.cashCardLayout.addLayout(self.cashBody)


        self.pageBodyLayout.addWidget(self.cashCard)

        self.kpiRow = QHBoxLayout()
        self.kpiRow.setSpacing(22)
        self.kpiRow.setObjectName(u"kpiRow")
        self.kpiCard0 = QFrame(self.pageBody)
        self.kpiCard0.setObjectName(u"kpiCard0")
        self.kpiCard0.setMinimumSize(QSize(0, 158))
        self.kpiCard0.setFrameShape(QFrame.StyledPanel)
        self.kpi0Layout = QVBoxLayout(self.kpiCard0)
        self.kpi0Layout.setSpacing(16)
        self.kpi0Layout.setObjectName(u"kpi0Layout")
        self.kpi0Layout.setContentsMargins(22, 20, 22, 20)
        self.kpi0Head = QHBoxLayout()
        self.kpi0Head.setSpacing(12)
        self.kpi0Head.setObjectName(u"kpi0Head")
        self.kpiIcon0 = QLabel(self.kpiCard0)
        self.kpiIcon0.setObjectName(u"kpiIcon0")
        self.kpiIcon0.setMinimumSize(QSize(40, 40))
        self.kpiIcon0.setMaximumSize(QSize(40, 40))
        self.kpiIcon0.setAlignment(Qt.AlignCenter)

        self.kpi0Head.addWidget(self.kpiIcon0)

        self.kpiTitle0 = QLabel(self.kpiCard0)
        self.kpiTitle0.setObjectName(u"kpiTitle0")

        self.kpi0Head.addWidget(self.kpiTitle0)

        self.kpi0Sp = QSpacerItem(20, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.kpi0Head.addItem(self.kpi0Sp)

        self.kpiPeriod0 = QLabel(self.kpiCard0)
        self.kpiPeriod0.setObjectName(u"kpiPeriod0")

        self.kpi0Head.addWidget(self.kpiPeriod0)


        self.kpi0Layout.addLayout(self.kpi0Head)

        self.kpi0ValRow = QHBoxLayout()
        self.kpi0ValRow.setSpacing(12)
        self.kpi0ValRow.setObjectName(u"kpi0ValRow")
        self.kpiValue0 = QLabel(self.kpiCard0)
        self.kpiValue0.setObjectName(u"kpiValue0")

        self.kpi0ValRow.addWidget(self.kpiValue0)

        self.kpiDelta0 = QWidget(self.kpiCard0)
        self.kpiDelta0.setObjectName(u"kpiDelta0")
        self.kpiDelta0Layout = QHBoxLayout(self.kpiDelta0)
        self.kpiDelta0Layout.setSpacing(3)
        self.kpiDelta0Layout.setObjectName(u"kpiDelta0Layout")
        self.kpiDelta0Layout.setContentsMargins(0, 0, 0, 0)

        self.kpi0ValRow.addWidget(self.kpiDelta0)

        self.kpi0ValSp = QSpacerItem(10, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.kpi0ValRow.addItem(self.kpi0ValSp)


        self.kpi0Layout.addLayout(self.kpi0ValRow)

        self.kpiSub0 = QLabel(self.kpiCard0)
        self.kpiSub0.setObjectName(u"kpiSub0")

        self.kpi0Layout.addWidget(self.kpiSub0)


        self.kpiRow.addWidget(self.kpiCard0)

        self.kpiCard1 = QFrame(self.pageBody)
        self.kpiCard1.setObjectName(u"kpiCard1")
        self.kpiCard1.setMinimumSize(QSize(0, 158))
        self.kpiCard1.setFrameShape(QFrame.StyledPanel)
        self.kpi1Layout = QVBoxLayout(self.kpiCard1)
        self.kpi1Layout.setSpacing(16)
        self.kpi1Layout.setObjectName(u"kpi1Layout")
        self.kpi1Layout.setContentsMargins(22, 20, 22, 20)
        self.kpi1Head = QHBoxLayout()
        self.kpi1Head.setSpacing(12)
        self.kpi1Head.setObjectName(u"kpi1Head")
        self.kpiIcon1 = QLabel(self.kpiCard1)
        self.kpiIcon1.setObjectName(u"kpiIcon1")
        self.kpiIcon1.setMinimumSize(QSize(40, 40))
        self.kpiIcon1.setMaximumSize(QSize(40, 40))
        self.kpiIcon1.setAlignment(Qt.AlignCenter)

        self.kpi1Head.addWidget(self.kpiIcon1)

        self.kpiTitle1 = QLabel(self.kpiCard1)
        self.kpiTitle1.setObjectName(u"kpiTitle1")

        self.kpi1Head.addWidget(self.kpiTitle1)

        self.kpi1Sp = QSpacerItem(20, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.kpi1Head.addItem(self.kpi1Sp)

        self.kpiPeriod1 = QLabel(self.kpiCard1)
        self.kpiPeriod1.setObjectName(u"kpiPeriod1")

        self.kpi1Head.addWidget(self.kpiPeriod1)


        self.kpi1Layout.addLayout(self.kpi1Head)

        self.kpi1ValRow = QHBoxLayout()
        self.kpi1ValRow.setSpacing(12)
        self.kpi1ValRow.setObjectName(u"kpi1ValRow")
        self.kpiValue1 = QLabel(self.kpiCard1)
        self.kpiValue1.setObjectName(u"kpiValue1")

        self.kpi1ValRow.addWidget(self.kpiValue1)

        self.kpiDelta1 = QWidget(self.kpiCard1)
        self.kpiDelta1.setObjectName(u"kpiDelta1")
        self.kpiDelta1Layout = QHBoxLayout(self.kpiDelta1)
        self.kpiDelta1Layout.setSpacing(3)
        self.kpiDelta1Layout.setObjectName(u"kpiDelta1Layout")
        self.kpiDelta1Layout.setContentsMargins(0, 0, 0, 0)

        self.kpi1ValRow.addWidget(self.kpiDelta1)

        self.kpi1ValSp = QSpacerItem(10, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.kpi1ValRow.addItem(self.kpi1ValSp)


        self.kpi1Layout.addLayout(self.kpi1ValRow)

        self.kpiSub1 = QLabel(self.kpiCard1)
        self.kpiSub1.setObjectName(u"kpiSub1")

        self.kpi1Layout.addWidget(self.kpiSub1)


        self.kpiRow.addWidget(self.kpiCard1)

        self.kpiCard2 = QFrame(self.pageBody)
        self.kpiCard2.setObjectName(u"kpiCard2")
        self.kpiCard2.setMinimumSize(QSize(0, 158))
        self.kpiCard2.setFrameShape(QFrame.StyledPanel)
        self.kpi2Layout = QVBoxLayout(self.kpiCard2)
        self.kpi2Layout.setSpacing(16)
        self.kpi2Layout.setObjectName(u"kpi2Layout")
        self.kpi2Layout.setContentsMargins(22, 20, 22, 20)
        self.kpi2Head = QHBoxLayout()
        self.kpi2Head.setSpacing(12)
        self.kpi2Head.setObjectName(u"kpi2Head")
        self.kpiIcon2 = QLabel(self.kpiCard2)
        self.kpiIcon2.setObjectName(u"kpiIcon2")
        self.kpiIcon2.setMinimumSize(QSize(40, 40))
        self.kpiIcon2.setMaximumSize(QSize(40, 40))
        self.kpiIcon2.setAlignment(Qt.AlignCenter)

        self.kpi2Head.addWidget(self.kpiIcon2)

        self.kpiTitle2 = QLabel(self.kpiCard2)
        self.kpiTitle2.setObjectName(u"kpiTitle2")

        self.kpi2Head.addWidget(self.kpiTitle2)

        self.kpi2Sp = QSpacerItem(20, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.kpi2Head.addItem(self.kpi2Sp)

        self.kpiPeriod2 = QLabel(self.kpiCard2)
        self.kpiPeriod2.setObjectName(u"kpiPeriod2")

        self.kpi2Head.addWidget(self.kpiPeriod2)


        self.kpi2Layout.addLayout(self.kpi2Head)

        self.kpi2ValRow = QHBoxLayout()
        self.kpi2ValRow.setSpacing(12)
        self.kpi2ValRow.setObjectName(u"kpi2ValRow")
        self.kpiValue2 = QLabel(self.kpiCard2)
        self.kpiValue2.setObjectName(u"kpiValue2")

        self.kpi2ValRow.addWidget(self.kpiValue2)

        self.kpiDelta2 = QWidget(self.kpiCard2)
        self.kpiDelta2.setObjectName(u"kpiDelta2")
        self.kpiDelta2Layout = QHBoxLayout(self.kpiDelta2)
        self.kpiDelta2Layout.setSpacing(3)
        self.kpiDelta2Layout.setObjectName(u"kpiDelta2Layout")
        self.kpiDelta2Layout.setContentsMargins(0, 0, 0, 0)

        self.kpi2ValRow.addWidget(self.kpiDelta2)

        self.kpi2ValSp = QSpacerItem(10, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.kpi2ValRow.addItem(self.kpi2ValSp)


        self.kpi2Layout.addLayout(self.kpi2ValRow)

        self.kpiSub2 = QLabel(self.kpiCard2)
        self.kpiSub2.setObjectName(u"kpiSub2")

        self.kpi2Layout.addWidget(self.kpiSub2)


        self.kpiRow.addWidget(self.kpiCard2)


        self.pageBodyLayout.addLayout(self.kpiRow)

        self.bottomRow = QHBoxLayout()
        self.bottomRow.setSpacing(22)
        self.bottomRow.setObjectName(u"bottomRow")
        self.activityCard = QFrame(self.pageBody)
        self.activityCard.setObjectName(u"activityCard")
        self.activityCard.setMinimumSize(QSize(0, 250))
        self.activityCard.setFrameShape(QFrame.StyledPanel)
        self.activityLayout = QVBoxLayout(self.activityCard)
        self.activityLayout.setSpacing(14)
        self.activityLayout.setObjectName(u"activityLayout")
        self.activityLayout.setContentsMargins(24, 20, 24, 20)
        self.activityHead = QHBoxLayout()
        self.activityHead.setSpacing(10)
        self.activityHead.setObjectName(u"activityHead")
        self.activityIcon = QLabel(self.activityCard)
        self.activityIcon.setObjectName(u"activityIcon")
        self.activityIcon.setMinimumSize(QSize(20, 20))
        self.activityIcon.setMaximumSize(QSize(20, 20))

        self.activityHead.addWidget(self.activityIcon)

        self.activityTitle = QLabel(self.activityCard)
        self.activityTitle.setObjectName(u"activityTitle")

        self.activityHead.addWidget(self.activityTitle)

        self.activityHeadSp = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.activityHead.addItem(self.activityHeadSp)

        self.filterBtn = QPushButton(self.activityCard)
        self.filterBtn.setObjectName(u"filterBtn")
        self.filterBtn.setMinimumSize(QSize(84, 34))
        self.filterBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.activityHead.addWidget(self.filterBtn)

        self.sortBtn = QPushButton(self.activityCard)
        self.sortBtn.setObjectName(u"sortBtn")
        self.sortBtn.setMinimumSize(QSize(78, 34))
        self.sortBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.activityHead.addWidget(self.sortBtn)

        self.activityMore = QPushButton(self.activityCard)
        self.activityMore.setObjectName(u"activityMore")
        self.activityMore.setMinimumSize(QSize(34, 34))
        self.activityMore.setMaximumSize(QSize(34, 34))
        self.activityMore.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.activityHead.addWidget(self.activityMore)


        self.activityLayout.addLayout(self.activityHead)

        self.tableHeader = QWidget(self.activityCard)
        self.tableHeader.setObjectName(u"tableHeader")
        self.tableHeaderLayout = QHBoxLayout(self.tableHeader)
        self.tableHeaderLayout.setSpacing(12)
        self.tableHeaderLayout.setObjectName(u"tableHeaderLayout")
        self.tableHeaderLayout.setContentsMargins(4, 2, 4, 2)
        self.colType = QLabel(self.tableHeader)
        self.colType.setObjectName(u"colType")

        self.tableHeaderLayout.addWidget(self.colType)

        self.colSp1 = QSpacerItem(40, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.tableHeaderLayout.addItem(self.colSp1)

        self.colAmount = QLabel(self.tableHeader)
        self.colAmount.setObjectName(u"colAmount")
        self.colAmount.setMinimumSize(QSize(150, 0))

        self.tableHeaderLayout.addWidget(self.colAmount)

        self.colStatus = QLabel(self.tableHeader)
        self.colStatus.setObjectName(u"colStatus")
        self.colStatus.setMinimumSize(QSize(110, 0))

        self.tableHeaderLayout.addWidget(self.colStatus)

        self.colMethod = QLabel(self.tableHeader)
        self.colMethod.setObjectName(u"colMethod")
        self.colMethod.setMinimumSize(QSize(150, 0))

        self.tableHeaderLayout.addWidget(self.colMethod)


        self.activityLayout.addWidget(self.tableHeader)

        self.tableRule = QFrame(self.activityCard)
        self.tableRule.setObjectName(u"tableRule")
        self.tableRule.setMinimumSize(QSize(0, 1))
        self.tableRule.setMaximumSize(QSize(16777215, 1))
        self.tableRule.setFrameShape(QFrame.HLine)

        self.activityLayout.addWidget(self.tableRule)

        self.activityBody = QWidget(self.activityCard)
        self.activityBody.setObjectName(u"activityBody")
        self.activityBodyLayout = QVBoxLayout(self.activityBody)
        self.activityBodyLayout.setSpacing(6)
        self.activityBodyLayout.setObjectName(u"activityBodyLayout")
        self.activityBodyLayout.setContentsMargins(0, 2, 0, 0)

        self.activityLayout.addWidget(self.activityBody)

        self.activityBottom = QSpacerItem(10, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.activityLayout.addItem(self.activityBottom)


        self.bottomRow.addWidget(self.activityCard)

        self.cardsCard = QFrame(self.pageBody)
        self.cardsCard.setObjectName(u"cardsCard")
        self.cardsCard.setMinimumSize(QSize(0, 250))
        self.cardsCard.setFrameShape(QFrame.StyledPanel)
        self.cardsCardLayout = QVBoxLayout(self.cardsCard)
        self.cardsCardLayout.setSpacing(16)
        self.cardsCardLayout.setObjectName(u"cardsCardLayout")
        self.cardsCardLayout.setContentsMargins(24, 20, 24, 20)
        self.cardsHead = QHBoxLayout()
        self.cardsHead.setSpacing(10)
        self.cardsHead.setObjectName(u"cardsHead")
        self.cardsIcon = QLabel(self.cardsCard)
        self.cardsIcon.setObjectName(u"cardsIcon")
        self.cardsIcon.setMinimumSize(QSize(20, 20))
        self.cardsIcon.setMaximumSize(QSize(20, 20))

        self.cardsHead.addWidget(self.cardsIcon)

        self.cardsTitle = QLabel(self.cardsCard)
        self.cardsTitle.setObjectName(u"cardsTitle")

        self.cardsHead.addWidget(self.cardsTitle)

        self.cardsHeadSp = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.cardsHead.addItem(self.cardsHeadSp)

        self.seeAllBtn = QPushButton(self.cardsCard)
        self.seeAllBtn.setObjectName(u"seeAllBtn")
        self.seeAllBtn.setMinimumSize(QSize(84, 32))
        self.seeAllBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.cardsHead.addWidget(self.seeAllBtn)


        self.cardsCardLayout.addLayout(self.cardsHead)

        self.cardStack = QCustomCardStack(self.cardsCard)
        self.cardStack.setObjectName(u"cardStack")
        self.cardStack.setMinimumSize(QSize(0, 205))
        self.cardStack.setProperty(u"cardHeight", 158)
        self.cardStack.setProperty(u"cardPeek", 20)
        self.cardStack.setProperty(u"xInset", 14)
        self.cardStack.setProperty(u"maxVisible", 3)

        self.cardsCardLayout.addWidget(self.cardStack)

        self.cardsBottom = QSpacerItem(10, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.cardsCardLayout.addItem(self.cardsBottom)


        self.bottomRow.addWidget(self.cardsCard)

        self.bottomRow.setStretch(0, 2)
        self.bottomRow.setStretch(1, 1)

        self.pageBodyLayout.addLayout(self.bottomRow)


        self.dashBody.addWidget(self.pageBody)

        self.dashScroll.setWidget(self.dashScrollContents)

        self.dashOuter.addWidget(self.dashScroll)


        self.retranslateUi(DashboardComponent)

        QMetaObject.connectSlotsByName(DashboardComponent)
    # setupUi

    def retranslateUi(self, DashboardComponent):
        self.crumbActive.setText(QCoreApplication.translate("DashboardComponent", u"Operations Dashboard", None))
        self.crumbActive.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"crumbActive", None))
        self.crumbSep.setText("")
        self.crumbSep.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"crumbSep", None))
        self.crumbHello.setText(QCoreApplication.translate("DashboardComponent", u"Real-time overview", None))
        self.crumbHello.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"crumbHello", None))
        self.clockLabel.setText(QCoreApplication.translate("DashboardComponent", u"Monday, April 8, 2026", None))
        self.clockLabel.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"clock", None))
        self.pageBody.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"pageBand", None))
        self.banner.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"banner", None))
        self.bannerTitle.setText(QCoreApplication.translate("DashboardComponent", u"Total Balance", None))
        self.bannerTitle.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"bannerTitle", None))
        self.bannerValue.setText(QCoreApplication.translate("DashboardComponent", u"\u20ac 320.845,20", None))
        self.bannerValue.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"bannerValue", None))
        self.addBtn.setText(QCoreApplication.translate("DashboardComponent", u"Add", None))
        self.addBtn.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"bannerPrimary", None))
        self.sendBtn.setText(QCoreApplication.translate("DashboardComponent", u"Send", None))
        self.sendBtn.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"bannerGhost", None))
        self.requestBtn.setText(QCoreApplication.translate("DashboardComponent", u"Request", None))
        self.requestBtn.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"bannerGhost", None))
        self.moreBtn.setText("")
        self.moreBtn.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"bannerGhost", None))
        self.cashCard.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"card", None))
        self.cashIcon.setText("")
        self.cashTitle.setText(QCoreApplication.translate("DashboardComponent", u"Cash Flow", None))
        self.cashTitle.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"panelTitle", None))
        self.cashSeg.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"segment", None))
        self.weeklyBtn.setText(QCoreApplication.translate("DashboardComponent", u"Weekly", None))
        self.weeklyBtn.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"segBtn", None))
        self.dailyBtn.setText(QCoreApplication.translate("DashboardComponent", u"Daily", None))
        self.dailyBtn.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"segBtn", None))
        self.manageBtn.setText(QCoreApplication.translate("DashboardComponent", u"Manage", None))
        self.manageBtn.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"outline", None))
        self.cashChart.setProperty(u"axisSuffix", QCoreApplication.translate("DashboardComponent", u"K", None))
        self.cashDivider.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"vdivider", None))
        self.incIcon.setText("")
        self.incIcon.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"sideIcon", None))
        self.incLabel.setText(QCoreApplication.translate("DashboardComponent", u"Income", None))
        self.incLabel.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"statLabel", None))
        self.incValue.setText(QCoreApplication.translate("DashboardComponent", u"\u20ac 12.378,20", None))
        self.incValue.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"sideValue", None))
        self.sideDivider.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"hdivider", None))
        self.expIcon.setText("")
        self.expIcon.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"sideIcon", None))
        self.expLabel.setText(QCoreApplication.translate("DashboardComponent", u"Expense", None))
        self.expLabel.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"statLabel", None))
        self.expValue.setText(QCoreApplication.translate("DashboardComponent", u"\u20ac 5.788,21", None))
        self.expValue.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"sideValue", None))
        self.kpiCard0.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"card", None))
        self.kpiIcon0.setText("")
        self.kpiIcon0.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"sideIcon", None))
        self.kpiTitle0.setText(QCoreApplication.translate("DashboardComponent", u"Business account", None))
        self.kpiTitle0.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"kpiTitle", None))
        self.kpiPeriod0.setText(QCoreApplication.translate("DashboardComponent", u"Last 30 days", None))
        self.kpiPeriod0.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"kpiPeriod", None))
        self.kpiValue0.setText(QCoreApplication.translate("DashboardComponent", u"\u20ac 8.672,20", None))
        self.kpiValue0.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"kpiValue", None))
        self.kpiSub0.setText(QCoreApplication.translate("DashboardComponent", u"vs. 7.120,14 Last Period", None))
        self.kpiSub0.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"kpiSub", None))
        self.kpiCard1.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"card", None))
        self.kpiIcon1.setText("")
        self.kpiIcon1.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"sideIcon", None))
        self.kpiTitle1.setText(QCoreApplication.translate("DashboardComponent", u"Total Saving", None))
        self.kpiTitle1.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"kpiTitle", None))
        self.kpiPeriod1.setText(QCoreApplication.translate("DashboardComponent", u"Last 30 days", None))
        self.kpiPeriod1.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"kpiPeriod", None))
        self.kpiValue1.setText(QCoreApplication.translate("DashboardComponent", u"\u20ac 3.765,35", None))
        self.kpiValue1.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"kpiValue", None))
        self.kpiSub1.setText(QCoreApplication.translate("DashboardComponent", u"vs. 4.116,50 Last Period", None))
        self.kpiSub1.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"kpiSub", None))
        self.kpiCard2.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"card", None))
        self.kpiIcon2.setText("")
        self.kpiIcon2.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"sideIcon", None))
        self.kpiTitle2.setText(QCoreApplication.translate("DashboardComponent", u"Tax Reserve", None))
        self.kpiTitle2.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"kpiTitle", None))
        self.kpiPeriod2.setText(QCoreApplication.translate("DashboardComponent", u"Last 30 days", None))
        self.kpiPeriod2.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"kpiPeriod", None))
        self.kpiValue2.setText(QCoreApplication.translate("DashboardComponent", u"\u20ac 14.376,16", None))
        self.kpiValue2.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"kpiValue", None))
        self.kpiSub2.setText(QCoreApplication.translate("DashboardComponent", u"vs. 10.236,46 Last Period", None))
        self.kpiSub2.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"kpiSub", None))
        self.activityCard.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"card", None))
        self.activityIcon.setText("")
        self.activityTitle.setText(QCoreApplication.translate("DashboardComponent", u"Recent Activity", None))
        self.activityTitle.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"panelTitle", None))
        self.filterBtn.setText(QCoreApplication.translate("DashboardComponent", u"Filter", None))
        self.filterBtn.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"outline", None))
        self.sortBtn.setText(QCoreApplication.translate("DashboardComponent", u"Sort", None))
        self.sortBtn.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"outline", None))
        self.activityMore.setText("")
        self.activityMore.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"outline", None))
        self.colType.setText(QCoreApplication.translate("DashboardComponent", u"TYPE", None))
        self.colType.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"colHead", None))
        self.colAmount.setText(QCoreApplication.translate("DashboardComponent", u"AMOUNT", None))
        self.colAmount.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"colHead", None))
        self.colStatus.setText(QCoreApplication.translate("DashboardComponent", u"STATUS", None))
        self.colStatus.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"colHead", None))
        self.colMethod.setText(QCoreApplication.translate("DashboardComponent", u"METHOD", None))
        self.colMethod.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"colHead", None))
        self.tableRule.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"hdivider", None))
        self.cardsCard.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"card", None))
        self.cardsIcon.setText("")
        self.cardsTitle.setText(QCoreApplication.translate("DashboardComponent", u"My Cards", None))
        self.cardsTitle.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"panelTitle", None))
        self.seeAllBtn.setText(QCoreApplication.translate("DashboardComponent", u"See All", None))
        self.seeAllBtn.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"outline", None))
        pass
    # retranslateUi

