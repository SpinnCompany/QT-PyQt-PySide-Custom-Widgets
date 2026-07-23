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

from Custom_Widgets.QCustomComponent import QCustomComponent
from Custom_Widgets.QCustomMiniBarChart import QCustomMiniBarChart
from Custom_Widgets.QCustomPageDots import QCustomPageDots
from Custom_Widgets.QCustomPaymentCard import QCustomPaymentCard
from Custom_Widgets.QCustomQPushButton import QCustomQPushButton
from Custom_Widgets.QCustomTrendChip import QCustomTrendChip
class Ui_DashboardComponent(object):
    def setupUi(self, DashboardComponent):
        if not DashboardComponent.objectName():
            DashboardComponent.setObjectName(u"DashboardComponent")
        DashboardComponent.resize(1180, 800)
        self.dashOuter = QVBoxLayout(DashboardComponent)
        self.dashOuter.setSpacing(0)
        self.dashOuter.setObjectName(u"dashOuter")
        self.dashOuter.setContentsMargins(0, 0, 0, 0)
        self.dashScroll = QScrollArea(DashboardComponent)
        self.dashScroll.setObjectName(u"dashScroll")
        self.dashScroll.setWidgetResizable(True)
        self.dashScroll.setFrameShape(QFrame.NoFrame)
        self.dashScroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.dashScrollContents = QWidget()
        self.dashScrollContents.setObjectName(u"dashScrollContents")
        self.dashScrollContents.setGeometry(QRect(0, 0, 1180, 820))
        self.dashBody = QVBoxLayout(self.dashScrollContents)
        self.dashBody.setSpacing(0)
        self.dashBody.setObjectName(u"dashBody")
        self.dashBody.setContentsMargins(0, 0, 0, 0)
        self.topBar = QWidget(self.dashScrollContents)
        self.topBar.setObjectName(u"topBar")
        self.topBarLayout = QHBoxLayout(self.topBar)
        self.topBarLayout.setSpacing(12)
        self.topBarLayout.setObjectName(u"topBarLayout")
        self.topBarLayout.setContentsMargins(36, 26, 36, 18)
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

        self.topSection = QFrame(self.dashScrollContents)
        self.topSection.setObjectName(u"topSection")
        self.topSection.setFrameShape(QFrame.StyledPanel)
        self.topSectionLayout = QHBoxLayout(self.topSection)
        self.topSectionLayout.setSpacing(28)
        self.topSectionLayout.setObjectName(u"topSectionLayout")
        self.topSectionLayout.setContentsMargins(36, 22, 36, 30)
        self.cardsSide = QVBoxLayout()
        self.cardsSide.setSpacing(18)
        self.cardsSide.setObjectName(u"cardsSide")
        self.cardsHead = QHBoxLayout()
        self.cardsHead.setObjectName(u"cardsHead")
        self.cardsTitle = QLabel(self.topSection)
        self.cardsTitle.setObjectName(u"cardsTitle")

        self.cardsHead.addWidget(self.cardsTitle)

        self.cardsHeadSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.cardsHead.addItem(self.cardsHeadSpacer)

        self.cardsDots = QCustomPageDots(self.topSection)
        self.cardsDots.setObjectName(u"cardsDots")
        self.cardsDots.setProperty(u"count", 3)
        self.cardsDots.setProperty(u"activeIndex", 0)

        self.cardsHead.addWidget(self.cardsDots)


        self.cardsSide.addLayout(self.cardsHead)

        self.cardsRow = QHBoxLayout()
        self.cardsRow.setSpacing(16)
        self.cardsRow.setObjectName(u"cardsRow")
        self.addCardBtn = QPushButton(self.topSection)
        self.addCardBtn.setObjectName(u"addCardBtn")
        self.addCardBtn.setMinimumSize(QSize(68, 150))
        self.addCardBtn.setMaximumSize(QSize(68, 150))
        self.addCardBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.cardsRow.addWidget(self.addCardBtn)

        self.blueCard = QCustomPaymentCard(self.topSection)
        self.blueCard.setObjectName(u"blueCard")
        self.blueCard.setMinimumSize(QSize(250, 150))
        self.blueCard.setMaximumSize(QSize(270, 150))
        self.blueCard.setProperty(u"revealable", True)

        self.cardsRow.addWidget(self.blueCard)

        self.greyCard = QCustomPaymentCard(self.topSection)
        self.greyCard.setObjectName(u"greyCard")
        self.greyCard.setMinimumSize(QSize(250, 150))
        self.greyCard.setMaximumSize(QSize(270, 150))
        self.greyCard.setProperty(u"revealable", True)

        self.cardsRow.addWidget(self.greyCard)

        self.cardsRowSpacer = QSpacerItem(10, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.cardsRow.addItem(self.cardsRowSpacer)


        self.cardsSide.addLayout(self.cardsRow)

        self.cardsSide.setStretch(1, 1)

        self.topSectionLayout.addLayout(self.cardsSide)

        self.topDivider = QFrame(self.topSection)
        self.topDivider.setObjectName(u"topDivider")
        self.topDivider.setMinimumSize(QSize(1, 0))
        self.topDivider.setMaximumSize(QSize(1, 16777215))
        self.topDivider.setFrameShape(QFrame.VLine)

        self.topSectionLayout.addWidget(self.topDivider)

        self.balanceSide = QVBoxLayout()
        self.balanceSide.setSpacing(6)
        self.balanceSide.setObjectName(u"balanceSide")
        self.balanceHead = QHBoxLayout()
        self.balanceHead.setObjectName(u"balanceHead")
        self.balanceTitle = QLabel(self.topSection)
        self.balanceTitle.setObjectName(u"balanceTitle")

        self.balanceHead.addWidget(self.balanceTitle)

        self.balanceHeadSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.balanceHead.addItem(self.balanceHeadSpacer)

        self.lastMonthBtn = QPushButton(self.topSection)
        self.lastMonthBtn.setObjectName(u"lastMonthBtn")
        self.lastMonthBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.lastMonthBtn.setLayoutDirection(Qt.RightToLeft)
        self.lastMonthBtn.setIconSize(QSize(16, 16))

        self.balanceHead.addWidget(self.lastMonthBtn)


        self.balanceSide.addLayout(self.balanceHead)

        self.balanceBig = QLabel(self.topSection)
        self.balanceBig.setObjectName(u"balanceBig")

        self.balanceSide.addWidget(self.balanceBig)

        self.balanceNumber = QLabel(self.topSection)
        self.balanceNumber.setObjectName(u"balanceNumber")

        self.balanceSide.addWidget(self.balanceNumber)

        self.balanceMidSpacer = QSpacerItem(10, 16, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.balanceSide.addItem(self.balanceMidSpacer)

        self.balanceStats = QHBoxLayout()
        self.balanceStats.setSpacing(34)
        self.balanceStats.setObjectName(u"balanceStats")
        self.incomeCol = QVBoxLayout()
        self.incomeCol.setSpacing(8)
        self.incomeCol.setObjectName(u"incomeCol")
        self.incomeLabel = QLabel(self.topSection)
        self.incomeLabel.setObjectName(u"incomeLabel")

        self.incomeCol.addWidget(self.incomeLabel)

        self.incomeRow = QHBoxLayout()
        self.incomeRow.setSpacing(10)
        self.incomeRow.setObjectName(u"incomeRow")
        self.incomeChip = QCustomTrendChip(self.topSection)
        self.incomeChip.setObjectName(u"incomeChip")
        self.incomeChip.setMinimumSize(QSize(30, 30))
        self.incomeChip.setMaximumSize(QSize(30, 30))

        self.incomeRow.addWidget(self.incomeChip)

        self.incomeValue = QLabel(self.topSection)
        self.incomeValue.setObjectName(u"incomeValue")

        self.incomeRow.addWidget(self.incomeValue)

        self.incomeSpacer = QSpacerItem(10, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.incomeRow.addItem(self.incomeSpacer)


        self.incomeCol.addLayout(self.incomeRow)


        self.balanceStats.addLayout(self.incomeCol)

        self.expenseCol = QVBoxLayout()
        self.expenseCol.setSpacing(8)
        self.expenseCol.setObjectName(u"expenseCol")
        self.expenseLabel = QLabel(self.topSection)
        self.expenseLabel.setObjectName(u"expenseLabel")

        self.expenseCol.addWidget(self.expenseLabel)

        self.expenseRow = QHBoxLayout()
        self.expenseRow.setSpacing(10)
        self.expenseRow.setObjectName(u"expenseRow")
        self.expenseChip = QCustomTrendChip(self.topSection)
        self.expenseChip.setObjectName(u"expenseChip")
        self.expenseChip.setMinimumSize(QSize(30, 30))
        self.expenseChip.setMaximumSize(QSize(30, 30))

        self.expenseRow.addWidget(self.expenseChip)

        self.expenseValue = QLabel(self.topSection)
        self.expenseValue.setObjectName(u"expenseValue")

        self.expenseRow.addWidget(self.expenseValue)

        self.expenseSpacer = QSpacerItem(10, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.expenseRow.addItem(self.expenseSpacer)


        self.expenseCol.addLayout(self.expenseRow)


        self.balanceStats.addLayout(self.expenseCol)


        self.balanceSide.addLayout(self.balanceStats)

        self.balanceBottomSpacer = QSpacerItem(10, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.balanceSide.addItem(self.balanceBottomSpacer)


        self.topSectionLayout.addLayout(self.balanceSide)


        self.dashBody.addWidget(self.topSection)

        self.bottomSection = QFrame(self.dashScrollContents)
        self.bottomSection.setObjectName(u"bottomSection")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.bottomSection.sizePolicy().hasHeightForWidth())
        self.bottomSection.setSizePolicy(sizePolicy)
        self.bottomSection.setFrameShape(QFrame.StyledPanel)
        self.bottomSectionLayout = QHBoxLayout(self.bottomSection)
        self.bottomSectionLayout.setSpacing(28)
        self.bottomSectionLayout.setObjectName(u"bottomSectionLayout")
        self.bottomSectionLayout.setContentsMargins(36, 28, 36, 30)
        self.summarySide = QVBoxLayout()
        self.summarySide.setSpacing(20)
        self.summarySide.setObjectName(u"summarySide")
        self.summaryHead = QHBoxLayout()
        self.summaryHead.setObjectName(u"summaryHead")
        self.summaryTitle = QLabel(self.bottomSection)
        self.summaryTitle.setObjectName(u"summaryTitle")

        self.summaryHead.addWidget(self.summaryTitle)

        self.summaryHeadSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.summaryHead.addItem(self.summaryHeadSpacer)

        self.generateReportBtn = QPushButton(self.bottomSection)
        self.generateReportBtn.setObjectName(u"generateReportBtn")
        self.generateReportBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.summaryHead.addWidget(self.generateReportBtn)


        self.summarySide.addLayout(self.summaryHead)

        self.summaryBody = QHBoxLayout()
        self.summaryBody.setSpacing(22)
        self.summaryBody.setObjectName(u"summaryBody")
        self.summaryBox = QFrame(self.bottomSection)
        self.summaryBox.setObjectName(u"summaryBox")
        self.summaryBox.setMinimumSize(QSize(210, 150))
        self.summaryBox.setMaximumSize(QSize(240, 16777215))
        self.summaryBox.setFrameShape(QFrame.StyledPanel)
        self.summaryBoxLayout = QVBoxLayout(self.summaryBox)
        self.summaryBoxLayout.setSpacing(4)
        self.summaryBoxLayout.setObjectName(u"summaryBoxLayout")
        self.summaryBoxLayout.setContentsMargins(22, 22, 22, 22)
        self.sumIncomeLabel = QLabel(self.summaryBox)
        self.sumIncomeLabel.setObjectName(u"sumIncomeLabel")

        self.summaryBoxLayout.addWidget(self.sumIncomeLabel)

        self.sumIncomeValue = QLabel(self.summaryBox)
        self.sumIncomeValue.setObjectName(u"sumIncomeValue")

        self.summaryBoxLayout.addWidget(self.sumIncomeValue)

        self.sumBoxDiv = QSpacerItem(10, 16, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.summaryBoxLayout.addItem(self.sumBoxDiv)

        self.sumExpenseLabel = QLabel(self.summaryBox)
        self.sumExpenseLabel.setObjectName(u"sumExpenseLabel")

        self.summaryBoxLayout.addWidget(self.sumExpenseLabel)

        self.sumExpenseValue = QLabel(self.summaryBox)
        self.sumExpenseValue.setObjectName(u"sumExpenseValue")

        self.summaryBoxLayout.addWidget(self.sumExpenseValue)


        self.summaryBody.addWidget(self.summaryBox)

        self.chartCol = QVBoxLayout()
        self.chartCol.setSpacing(10)
        self.chartCol.setObjectName(u"chartCol")
        self.barsChart = QCustomMiniBarChart(self.bottomSection)
        self.barsChart.setObjectName(u"barsChart")
        self.barsChart.setMinimumSize(QSize(0, 150))
        self.barsChart.setProperty(u"barWidth", 9)
        self.barsChart.setProperty(u"cornerRadius", 4)

        self.chartCol.addWidget(self.barsChart)

        self.summaryFoot = QHBoxLayout()
        self.summaryFoot.setObjectName(u"summaryFoot")
        self.summaryDates = QLabel(self.bottomSection)
        self.summaryDates.setObjectName(u"summaryDates")

        self.summaryFoot.addWidget(self.summaryDates)

        self.summaryFootSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.summaryFoot.addItem(self.summaryFootSpacer)

        self.summaryDots = QCustomPageDots(self.bottomSection)
        self.summaryDots.setObjectName(u"summaryDots")
        self.summaryDots.setProperty(u"count", 3)
        self.summaryDots.setProperty(u"activeIndex", 2)

        self.summaryFoot.addWidget(self.summaryDots)


        self.chartCol.addLayout(self.summaryFoot)


        self.summaryBody.addLayout(self.chartCol)


        self.summarySide.addLayout(self.summaryBody)

        self.summaryBottomSpacer = QSpacerItem(10, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.summarySide.addItem(self.summaryBottomSpacer)


        self.bottomSectionLayout.addLayout(self.summarySide)

        self.bottomDivider = QFrame(self.bottomSection)
        self.bottomDivider.setObjectName(u"bottomDivider")
        self.bottomDivider.setMinimumSize(QSize(1, 0))
        self.bottomDivider.setMaximumSize(QSize(1, 16777215))
        self.bottomDivider.setFrameShape(QFrame.VLine)

        self.bottomSectionLayout.addWidget(self.bottomDivider)

        self.txnSide = QVBoxLayout()
        self.txnSide.setSpacing(16)
        self.txnSide.setObjectName(u"txnSide")
        self.txnHead = QHBoxLayout()
        self.txnHead.setObjectName(u"txnHead")
        self.txnTitle = QLabel(self.bottomSection)
        self.txnTitle.setObjectName(u"txnTitle")

        self.txnHead.addWidget(self.txnTitle)

        self.txnHeadSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.txnHead.addItem(self.txnHeadSpacer)

        self.checkAllBtn = QPushButton(self.bottomSection)
        self.checkAllBtn.setObjectName(u"checkAllBtn")
        self.checkAllBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.txnHead.addWidget(self.checkAllBtn)


        self.txnSide.addLayout(self.txnHead)

        self.txnBody = QWidget(self.bottomSection)
        self.txnBody.setObjectName(u"txnBody")
        self.txnBodyLayout = QVBoxLayout(self.txnBody)
        self.txnBodyLayout.setSpacing(14)
        self.txnBodyLayout.setObjectName(u"txnBodyLayout")
        self.txnBodyLayout.setContentsMargins(0, 4, 0, 4)

        self.txnSide.addWidget(self.txnBody)

        self.txnSpacer = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.txnSide.addItem(self.txnSpacer)

        self.txnButtons = QHBoxLayout()
        self.txnButtons.setSpacing(14)
        self.txnButtons.setObjectName(u"txnButtons")
        self.newTransactionBtn = QCustomQPushButton(self.bottomSection)
        self.newTransactionBtn.setObjectName(u"newTransactionBtn")
        self.newTransactionBtn.setMinimumSize(QSize(0, 48))
        self.newTransactionBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.txnButtons.addWidget(self.newTransactionBtn)

        self.settingsBtn = QCustomQPushButton(self.bottomSection)
        self.settingsBtn.setObjectName(u"settingsBtn")
        self.settingsBtn.setMinimumSize(QSize(0, 48))
        self.settingsBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.txnButtons.addWidget(self.settingsBtn)


        self.txnSide.addLayout(self.txnButtons)


        self.bottomSectionLayout.addLayout(self.txnSide)


        self.dashBody.addWidget(self.bottomSection)

        self.dashScroll.setWidget(self.dashScrollContents)

        self.dashOuter.addWidget(self.dashScroll)


        self.retranslateUi(DashboardComponent)

        QMetaObject.connectSlotsByName(DashboardComponent)
    # setupUi

    def retranslateUi(self, DashboardComponent):
        self.crumbActive.setText(QCoreApplication.translate("DashboardComponent", u"Dashboard", None))
        self.crumbActive.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"crumbActive", None))
        self.crumbSep.setText("")
        self.crumbSep.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"crumbSep", None))
        self.crumbHello.setText(QCoreApplication.translate("DashboardComponent", u"Hello Matt, welcome back.", None))
        self.crumbHello.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"crumbHello", None))
        self.clockLabel.setText(QCoreApplication.translate("DashboardComponent", u"10:33, 01 April 2019", None))
        self.clockLabel.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"clock", None))
        self.topSection.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"topPanel", None))
        self.cardsTitle.setText(QCoreApplication.translate("DashboardComponent", u"My cards", None))
        self.cardsTitle.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"panelTitle", None))
        self.addCardBtn.setText("")
        self.blueCard.setProperty(u"brand", QCoreApplication.translate("DashboardComponent", u"VISA", None))
        self.blueCard.setProperty(u"amount", QCoreApplication.translate("DashboardComponent", u"$5 400.55", None))
        self.blueCard.setProperty(u"number", QCoreApplication.translate("DashboardComponent", u"4558", None))
        self.blueCard.setProperty(u"variant", QCoreApplication.translate("DashboardComponent", u"gradient", None))
        self.blueCard.setProperty(u"fullNumber", QCoreApplication.translate("DashboardComponent", u"4539 1482 0343 4558", None))
        self.greyCard.setProperty(u"brand", QCoreApplication.translate("DashboardComponent", u"VISA", None))
        self.greyCard.setProperty(u"amount", QCoreApplication.translate("DashboardComponent", u"$23 400,55", None))
        self.greyCard.setProperty(u"number", QCoreApplication.translate("DashboardComponent", u"3225", None))
        self.greyCard.setProperty(u"variant", QCoreApplication.translate("DashboardComponent", u"flat", None))
        self.greyCard.setProperty(u"fullNumber", QCoreApplication.translate("DashboardComponent", u"4024 0071 9876 3225", None))
        self.topDivider.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"vdivider", None))
        self.balanceTitle.setText(QCoreApplication.translate("DashboardComponent", u"Balance", None))
        self.balanceTitle.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"panelTitle", None))
        self.lastMonthBtn.setText(QCoreApplication.translate("DashboardComponent", u"Last month", None))
        self.balanceBig.setText(QCoreApplication.translate("DashboardComponent", u"$5 400.55", None))
        self.balanceBig.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"balanceBig", None))
        self.balanceNumber.setText(QCoreApplication.translate("DashboardComponent", u"**** **** ****  4558", None))
        self.balanceNumber.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"balanceNumber", None))
        self.incomeLabel.setText(QCoreApplication.translate("DashboardComponent", u"Income", None))
        self.incomeLabel.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"statLabel", None))
        self.incomeChip.setProperty(u"direction", QCoreApplication.translate("DashboardComponent", u"up", None))
        self.incomeChip.setProperty(u"variant", QCoreApplication.translate("DashboardComponent", u"circle", None))
        self.incomeValue.setText(QCoreApplication.translate("DashboardComponent", u"+ $6 320.15", None))
        self.incomeValue.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"statValue", None))
        self.expenseLabel.setText(QCoreApplication.translate("DashboardComponent", u"Expense", None))
        self.expenseLabel.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"statLabel", None))
        self.expenseChip.setProperty(u"direction", QCoreApplication.translate("DashboardComponent", u"down", None))
        self.expenseChip.setProperty(u"variant", QCoreApplication.translate("DashboardComponent", u"circle", None))
        self.expenseValue.setText(QCoreApplication.translate("DashboardComponent", u"- $919.60", None))
        self.expenseValue.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"statValue", None))
        self.bottomSection.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"bottomPanel", None))
        self.summaryTitle.setText(QCoreApplication.translate("DashboardComponent", u"Monthly summary", None))
        self.summaryTitle.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"panelTitle", None))
        self.generateReportBtn.setText(QCoreApplication.translate("DashboardComponent", u"Generate report", None))
        self.generateReportBtn.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"link", None))
        self.summaryBox.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"dashBox", None))
        self.sumIncomeLabel.setText(QCoreApplication.translate("DashboardComponent", u"Income", None))
        self.sumIncomeLabel.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"statLabel", None))
        self.sumIncomeValue.setText(QCoreApplication.translate("DashboardComponent", u"+ $5000.00", None))
        self.sumIncomeValue.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"moneyPos", None))
        self.sumExpenseLabel.setText(QCoreApplication.translate("DashboardComponent", u"Expense", None))
        self.sumExpenseLabel.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"statLabel", None))
        self.sumExpenseValue.setText(QCoreApplication.translate("DashboardComponent", u"- $234.55", None))
        self.sumExpenseValue.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"moneyNeg", None))
        self.summaryDates.setText(QCoreApplication.translate("DashboardComponent", u"23 - 31 Mar, 2019", None))
        self.summaryDates.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"panelSub", None))
        self.bottomDivider.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"vdivider", None))
        self.txnTitle.setText(QCoreApplication.translate("DashboardComponent", u"Latest transaction", None))
        self.txnTitle.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"panelTitle", None))
        self.checkAllBtn.setText(QCoreApplication.translate("DashboardComponent", u"Check all", None))
        self.checkAllBtn.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"link", None))
        self.newTransactionBtn.setText(QCoreApplication.translate("DashboardComponent", u"New transaction", None))
        self.settingsBtn.setText(QCoreApplication.translate("DashboardComponent", u"Settings", None))
        pass
    # retranslateUi

