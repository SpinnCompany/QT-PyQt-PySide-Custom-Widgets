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
    QLineEdit, QPushButton, QScrollArea, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

from Custom_Widgets.QCustomAvatar import QCustomAvatar
from Custom_Widgets.QCustomAvatarGroup import QCustomAvatarGroup
from Custom_Widgets.QCustomCharts.QCustomAreaChart import QCustomAreaChart
from Custom_Widgets.QCustomComponent import QCustomComponent
from Custom_Widgets.QCustomDataTable import QCustomDataTable
from Custom_Widgets.QCustomQPushButton import QCustomQPushButton
from Custom_Widgets.QCustomSegmentedControl import QCustomSegmentedControl
from Custom_Widgets.QCustomTrendChip import QCustomTrendChip
class Ui_DashboardComponent(object):
    def setupUi(self, DashboardComponent):
        if not DashboardComponent.objectName():
            DashboardComponent.setObjectName(u"DashboardComponent")
        DashboardComponent.resize(1280, 840)
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
        self.dashScrollContents.setGeometry(QRect(0, 0, 1280, 840))
        self.dashBody = QVBoxLayout(self.dashScrollContents)
        self.dashBody.setSpacing(20)
        self.dashBody.setObjectName(u"dashBody")
        self.dashBody.setContentsMargins(4, 2, 4, 6)
        self.topBar = QWidget(self.dashScrollContents)
        self.topBar.setObjectName(u"topBar")
        self.topBarLayout = QHBoxLayout(self.topBar)
        self.topBarLayout.setSpacing(12)
        self.topBarLayout.setObjectName(u"topBarLayout")
        self.topBarLayout.setContentsMargins(6, 4, 6, 0)
        self.pageTitle = QLabel(self.topBar)
        self.pageTitle.setObjectName(u"pageTitle")

        self.topBarLayout.addWidget(self.pageTitle)

        self.topBarSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.topBarLayout.addItem(self.topBarSpacer)

        self.userChip = QFrame(self.topBar)
        self.userChip.setObjectName(u"userChip")
        self.userChip.setFrameShape(QFrame.StyledPanel)
        self.userChipLayout = QHBoxLayout(self.userChip)
        self.userChipLayout.setSpacing(10)
        self.userChipLayout.setObjectName(u"userChipLayout")
        self.userChipLayout.setContentsMargins(6, 6, 14, 6)
        self.userAvatar = QCustomAvatar(self.userChip)
        self.userAvatar.setObjectName(u"userAvatar")
        self.userAvatar.setMinimumSize(QSize(42, 42))
        self.userAvatar.setMaximumSize(QSize(42, 42))

        self.userChipLayout.addWidget(self.userAvatar)

        self.userTextCol = QVBoxLayout()
        self.userTextCol.setSpacing(0)
        self.userTextCol.setObjectName(u"userTextCol")
        self.userName = QLabel(self.userChip)
        self.userName.setObjectName(u"userName")

        self.userTextCol.addWidget(self.userName)

        self.userId = QLabel(self.userChip)
        self.userId.setObjectName(u"userId")

        self.userTextCol.addWidget(self.userId)


        self.userChipLayout.addLayout(self.userTextCol)

        self.userChevron = QPushButton(self.userChip)
        self.userChevron.setObjectName(u"userChevron")
        self.userChevron.setMinimumSize(QSize(26, 26))
        self.userChevron.setMaximumSize(QSize(26, 26))
        self.userChevron.setIconSize(QSize(16, 16))
        self.userChevron.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.userChipLayout.addWidget(self.userChevron)


        self.topBarLayout.addWidget(self.userChip)


        self.dashBody.addWidget(self.topBar)

        self.contentRow = QHBoxLayout()
        self.contentRow.setSpacing(20)
        self.contentRow.setObjectName(u"contentRow")
        self.contentRow.setContentsMargins(6, 0, 6, 4)
        self.leftCol = QVBoxLayout()
        self.leftCol.setSpacing(20)
        self.leftCol.setObjectName(u"leftCol")
        self.overviewCard = QFrame(self.dashScrollContents)
        self.overviewCard.setObjectName(u"overviewCard")
        self.overviewCard.setFrameShape(QFrame.StyledPanel)
        self.overviewLayout = QVBoxLayout(self.overviewCard)
        self.overviewLayout.setSpacing(12)
        self.overviewLayout.setObjectName(u"overviewLayout")
        self.overviewLayout.setContentsMargins(26, 22, 26, 18)
        self.overviewHead = QHBoxLayout()
        self.overviewHead.setObjectName(u"overviewHead")
        self.overviewTitle = QLabel(self.overviewCard)
        self.overviewTitle.setObjectName(u"overviewTitle")

        self.overviewHead.addWidget(self.overviewTitle)

        self.overviewHeadSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.overviewHead.addItem(self.overviewHeadSpacer)

        self.rangeControl = QCustomSegmentedControl(self.overviewCard)
        self.rangeControl.setObjectName(u"rangeControl")
        self.rangeControl.setMinimumSize(QSize(216, 38))
        self.rangeControl.setMaximumSize(QSize(216, 38))

        self.overviewHead.addWidget(self.rangeControl)


        self.overviewLayout.addLayout(self.overviewHead)

        self.overviewValueRow = QHBoxLayout()
        self.overviewValueRow.setSpacing(10)
        self.overviewValueRow.setObjectName(u"overviewValueRow")
        self.bigValue = QLabel(self.overviewCard)
        self.bigValue.setObjectName(u"bigValue")

        self.overviewValueRow.addWidget(self.bigValue)

        self.coinPick = QPushButton(self.overviewCard)
        self.coinPick.setObjectName(u"coinPick")
        self.coinPick.setMinimumSize(QSize(26, 26))
        self.coinPick.setMaximumSize(QSize(26, 26))
        self.coinPick.setIconSize(QSize(15, 15))
        self.coinPick.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.overviewValueRow.addWidget(self.coinPick)

        self.approxValue = QLabel(self.overviewCard)
        self.approxValue.setObjectName(u"approxValue")

        self.overviewValueRow.addWidget(self.approxValue)

        self.overviewValueSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.overviewValueRow.addItem(self.overviewValueSpacer)


        self.overviewLayout.addLayout(self.overviewValueRow)

        self.overviewChangeRow = QHBoxLayout()
        self.overviewChangeRow.setSpacing(8)
        self.overviewChangeRow.setObjectName(u"overviewChangeRow")
        self.changeChip = QCustomTrendChip(self.overviewCard)
        self.changeChip.setObjectName(u"changeChip")
        self.changeChip.setMinimumSize(QSize(24, 24))
        self.changeChip.setMaximumSize(QSize(24, 24))

        self.overviewChangeRow.addWidget(self.changeChip)

        self.changeValue = QLabel(self.overviewCard)
        self.changeValue.setObjectName(u"changeValue")

        self.overviewChangeRow.addWidget(self.changeValue)

        self.overviewChangeSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.overviewChangeRow.addItem(self.overviewChangeSpacer)


        self.overviewLayout.addLayout(self.overviewChangeRow)

        self.overviewChart = QCustomAreaChart(self.overviewCard)
        self.overviewChart.setObjectName(u"overviewChart")
        self.overviewChart.setMinimumSize(QSize(0, 172))

        self.overviewLayout.addWidget(self.overviewChart)

        self.timeRow = QWidget(self.overviewCard)
        self.timeRow.setObjectName(u"timeRow")
        self.timeRowLayout = QHBoxLayout(self.timeRow)
        self.timeRowLayout.setSpacing(0)
        self.timeRowLayout.setObjectName(u"timeRowLayout")
        self.timeRowLayout.setContentsMargins(6, 0, 6, 0)

        self.overviewLayout.addWidget(self.timeRow)


        self.leftCol.addWidget(self.overviewCard)

        self.marketCard = QFrame(self.dashScrollContents)
        self.marketCard.setObjectName(u"marketCard")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.marketCard.sizePolicy().hasHeightForWidth())
        self.marketCard.setSizePolicy(sizePolicy)
        self.marketCard.setFrameShape(QFrame.StyledPanel)
        self.marketLayout = QVBoxLayout(self.marketCard)
        self.marketLayout.setSpacing(14)
        self.marketLayout.setObjectName(u"marketLayout")
        self.marketLayout.setContentsMargins(26, 22, 26, 18)
        self.marketHead = QHBoxLayout()
        self.marketHead.setObjectName(u"marketHead")
        self.marketTitle = QLabel(self.marketCard)
        self.marketTitle.setObjectName(u"marketTitle")

        self.marketHead.addWidget(self.marketTitle)

        self.marketHeadSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.marketHead.addItem(self.marketHeadSpacer)

        self.marketTabs = QCustomSegmentedControl(self.marketCard)
        self.marketTabs.setObjectName(u"marketTabs")
        self.marketTabs.setMinimumSize(QSize(268, 38))
        self.marketTabs.setMaximumSize(QSize(268, 38))

        self.marketHead.addWidget(self.marketTabs)


        self.marketLayout.addLayout(self.marketHead)

        self.marketTable = QCustomDataTable(self.marketCard)
        self.marketTable.setObjectName(u"marketTable")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(1)
        sizePolicy1.setHeightForWidth(self.marketTable.sizePolicy().hasHeightForWidth())
        self.marketTable.setSizePolicy(sizePolicy1)
        self.marketTable.setMinimumSize(QSize(0, 256))

        self.marketLayout.addWidget(self.marketTable)


        self.leftCol.addWidget(self.marketCard)

        self.leftCol.setStretch(1, 1)

        self.contentRow.addLayout(self.leftCol)

        self.rightPanel = QWidget(self.dashScrollContents)
        self.rightPanel.setObjectName(u"rightPanel")
        self.rightPanel.setMinimumSize(QSize(352, 0))
        self.rightPanel.setMaximumSize(QSize(368, 16777215))
        self.rightCol = QVBoxLayout(self.rightPanel)
        self.rightCol.setSpacing(20)
        self.rightCol.setObjectName(u"rightCol")
        self.rightCol.setContentsMargins(0, 0, 0, 0)
        self.promoCard = QFrame(self.rightPanel)
        self.promoCard.setObjectName(u"promoCard")
        self.promoCard.setMinimumSize(QSize(0, 178))
        self.promoCard.setMaximumSize(QSize(16777215, 178))
        self.promoCard.setFrameShape(QFrame.StyledPanel)
        self.promoLayout = QVBoxLayout(self.promoCard)
        self.promoLayout.setSpacing(0)
        self.promoLayout.setObjectName(u"promoLayout")
        self.promoLayout.setContentsMargins(26, 24, 26, 22)
        self.promoTitle = QLabel(self.promoCard)
        self.promoTitle.setObjectName(u"promoTitle")

        self.promoLayout.addWidget(self.promoTitle)

        self.promoSub = QLabel(self.promoCard)
        self.promoSub.setObjectName(u"promoSub")

        self.promoLayout.addWidget(self.promoSub)

        self.promoMidSpacer = QSpacerItem(10, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.promoLayout.addItem(self.promoMidSpacer)

        self.promoFoot = QHBoxLayout()
        self.promoFoot.setObjectName(u"promoFoot")
        self.promoFootSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.promoFoot.addItem(self.promoFootSpacer)

        self.promoCoins = QCustomAvatarGroup(self.promoCard)
        self.promoCoins.setObjectName(u"promoCoins")
        self.promoCoins.setProperty(u"maxVisible", 5)
        self.promoCoins.setProperty(u"avatarSize", 36)

        self.promoFoot.addWidget(self.promoCoins)


        self.promoLayout.addLayout(self.promoFoot)


        self.rightCol.addWidget(self.promoCard)

        self.tradeCard = QFrame(self.rightPanel)
        self.tradeCard.setObjectName(u"tradeCard")
        sizePolicy.setHeightForWidth(self.tradeCard.sizePolicy().hasHeightForWidth())
        self.tradeCard.setSizePolicy(sizePolicy)
        self.tradeCard.setFrameShape(QFrame.StyledPanel)
        self.tradeLayout = QVBoxLayout(self.tradeCard)
        self.tradeLayout.setSpacing(12)
        self.tradeLayout.setObjectName(u"tradeLayout")
        self.tradeLayout.setContentsMargins(24, 22, 24, 22)
        self.tradeTitle = QLabel(self.tradeCard)
        self.tradeTitle.setObjectName(u"tradeTitle")

        self.tradeLayout.addWidget(self.tradeTitle)

        self.tradeTabs = QCustomSegmentedControl(self.tradeCard)
        self.tradeTabs.setObjectName(u"tradeTabs")
        self.tradeTabs.setMinimumSize(QSize(0, 38))

        self.tradeLayout.addWidget(self.tradeTabs)

        self.coinLabel = QLabel(self.tradeCard)
        self.coinLabel.setObjectName(u"coinLabel")

        self.tradeLayout.addWidget(self.coinLabel)

        self.coinField = QFrame(self.tradeCard)
        self.coinField.setObjectName(u"coinField")
        self.coinField.setMinimumSize(QSize(0, 54))
        self.coinField.setFrameShape(QFrame.StyledPanel)
        self.coinFieldLayout = QHBoxLayout(self.coinField)
        self.coinFieldLayout.setSpacing(10)
        self.coinFieldLayout.setObjectName(u"coinFieldLayout")
        self.coinFieldLayout.setContentsMargins(12, 6, 14, 6)
        self.coinAvatar = QCustomAvatar(self.coinField)
        self.coinAvatar.setObjectName(u"coinAvatar")
        self.coinAvatar.setMinimumSize(QSize(30, 30))
        self.coinAvatar.setMaximumSize(QSize(30, 30))
        self.coinAvatar.setProperty(u"showStatus", False)

        self.coinFieldLayout.addWidget(self.coinAvatar)

        self.coinName = QLabel(self.coinField)
        self.coinName.setObjectName(u"coinName")

        self.coinFieldLayout.addWidget(self.coinName)

        self.coinTicker = QLabel(self.coinField)
        self.coinTicker.setObjectName(u"coinTicker")

        self.coinFieldLayout.addWidget(self.coinTicker)

        self.coinFieldSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.coinFieldLayout.addItem(self.coinFieldSpacer)

        self.coinFieldChevron = QPushButton(self.coinField)
        self.coinFieldChevron.setObjectName(u"coinFieldChevron")
        self.coinFieldChevron.setMinimumSize(QSize(22, 22))
        self.coinFieldChevron.setMaximumSize(QSize(22, 22))
        self.coinFieldChevron.setIconSize(QSize(16, 16))

        self.coinFieldLayout.addWidget(self.coinFieldChevron)


        self.tradeLayout.addWidget(self.coinField)

        self.amountLabel = QLabel(self.tradeCard)
        self.amountLabel.setObjectName(u"amountLabel")

        self.tradeLayout.addWidget(self.amountLabel)

        self.amountField = QFrame(self.tradeCard)
        self.amountField.setObjectName(u"amountField")
        self.amountField.setMinimumSize(QSize(0, 54))
        self.amountField.setFrameShape(QFrame.StyledPanel)
        self.amountFieldLayout = QHBoxLayout(self.amountField)
        self.amountFieldLayout.setSpacing(10)
        self.amountFieldLayout.setObjectName(u"amountFieldLayout")
        self.amountFieldLayout.setContentsMargins(12, 6, 14, 6)
        self.amountBadge = QCustomAvatar(self.amountField)
        self.amountBadge.setObjectName(u"amountBadge")
        self.amountBadge.setMinimumSize(QSize(30, 30))
        self.amountBadge.setMaximumSize(QSize(30, 30))
        self.amountBadge.setProperty(u"showStatus", False)

        self.amountFieldLayout.addWidget(self.amountBadge)

        self.amountEdit = QLineEdit(self.amountField)
        self.amountEdit.setObjectName(u"amountEdit")
        self.amountEdit.setFrame(False)

        self.amountFieldLayout.addWidget(self.amountEdit)

        self.amountCurrency = QLabel(self.amountField)
        self.amountCurrency.setObjectName(u"amountCurrency")

        self.amountFieldLayout.addWidget(self.amountCurrency)

        self.amountChevron = QPushButton(self.amountField)
        self.amountChevron.setObjectName(u"amountChevron")
        self.amountChevron.setMinimumSize(QSize(22, 22))
        self.amountChevron.setMaximumSize(QSize(22, 22))
        self.amountChevron.setIconSize(QSize(16, 16))

        self.amountFieldLayout.addWidget(self.amountChevron)


        self.tradeLayout.addWidget(self.amountField)

        self.tradeRate = QLabel(self.tradeCard)
        self.tradeRate.setObjectName(u"tradeRate")
        self.tradeRate.setAlignment(Qt.AlignCenter)

        self.tradeLayout.addWidget(self.tradeRate)

        self.receiptBox = QFrame(self.tradeCard)
        self.receiptBox.setObjectName(u"receiptBox")
        self.receiptBox.setFrameShape(QFrame.StyledPanel)
        self.receiptLayout = QVBoxLayout(self.receiptBox)
        self.receiptLayout.setSpacing(10)
        self.receiptLayout.setObjectName(u"receiptLayout")
        self.receiptLayout.setContentsMargins(16, 14, 16, 14)
        self.promoRow = QHBoxLayout()
        self.promoRow.setObjectName(u"promoRow")
        self.promoCodeBtn = QPushButton(self.receiptBox)
        self.promoCodeBtn.setObjectName(u"promoCodeBtn")
        self.promoCodeBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.promoCodeBtn.setLayoutDirection(Qt.RightToLeft)
        self.promoCodeBtn.setIconSize(QSize(15, 15))

        self.promoRow.addWidget(self.promoCodeBtn)

        self.promoRowSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.promoRow.addItem(self.promoRowSpacer)


        self.receiptLayout.addLayout(self.promoRow)

        self.feeRow = QHBoxLayout()
        self.feeRow.setObjectName(u"feeRow")
        self.feeLabel = QLabel(self.receiptBox)
        self.feeLabel.setObjectName(u"feeLabel")

        self.feeRow.addWidget(self.feeLabel)

        self.feeSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.feeRow.addItem(self.feeSpacer)

        self.feeValue = QLabel(self.receiptBox)
        self.feeValue.setObjectName(u"feeValue")

        self.feeRow.addWidget(self.feeValue)


        self.receiptLayout.addLayout(self.feeRow)

        self.recvRow = QHBoxLayout()
        self.recvRow.setObjectName(u"recvRow")
        self.receivedLabel = QLabel(self.receiptBox)
        self.receivedLabel.setObjectName(u"receivedLabel")

        self.recvRow.addWidget(self.receivedLabel)

        self.recvSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.recvRow.addItem(self.recvSpacer)

        self.receivedValue = QLabel(self.receiptBox)
        self.receivedValue.setObjectName(u"receivedValue")

        self.recvRow.addWidget(self.receivedValue)


        self.receiptLayout.addLayout(self.recvRow)


        self.tradeLayout.addWidget(self.receiptBox)

        self.tradeBottomSpacer = QSpacerItem(10, 6, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.tradeLayout.addItem(self.tradeBottomSpacer)

        self.buyBtn = QCustomQPushButton(self.tradeCard)
        self.buyBtn.setObjectName(u"buyBtn")
        self.buyBtn.setMinimumSize(QSize(0, 52))
        self.buyBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.tradeLayout.addWidget(self.buyBtn)


        self.rightCol.addWidget(self.tradeCard)

        self.rightCol.setStretch(1, 1)

        self.contentRow.addWidget(self.rightPanel)

        self.contentRow.setStretch(0, 1)

        self.dashBody.addLayout(self.contentRow)

        self.dashScroll.setWidget(self.dashScrollContents)

        self.dashOuter.addWidget(self.dashScroll)


        self.retranslateUi(DashboardComponent)

        QMetaObject.connectSlotsByName(DashboardComponent)
    # setupUi

    def retranslateUi(self, DashboardComponent):
        self.pageTitle.setText(QCoreApplication.translate("DashboardComponent", u"Dashboard", None))
        self.pageTitle.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"pageTitle", None))
        self.userChip.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"userChip", None))
        self.userAvatar.setProperty(u"text", QCoreApplication.translate("DashboardComponent", u"A", None))
        self.userName.setText(QCoreApplication.translate("DashboardComponent", u"Anna cathcart", None))
        self.userName.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"userName", None))
        self.userId.setText(QCoreApplication.translate("DashboardComponent", u"ID: 32324254", None))
        self.userId.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"userId", None))
        self.userChevron.setText("")
        self.overviewCard.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"card", None))
        self.overviewTitle.setText(QCoreApplication.translate("DashboardComponent", u"Overview of all wallets", None))
        self.overviewTitle.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"cardTitle", None))
        self.bigValue.setText(QCoreApplication.translate("DashboardComponent", u"0.00263788 BTC", None))
        self.bigValue.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"bigValue", None))
        self.coinPick.setText("")
        self.approxValue.setText(QCoreApplication.translate("DashboardComponent", u"\u2248 $69.82", None))
        self.approxValue.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"approx", None))
        self.changeChip.setProperty(u"direction", QCoreApplication.translate("DashboardComponent", u"up", None))
        self.changeChip.setProperty(u"variant", QCoreApplication.translate("DashboardComponent", u"plain", None))
        self.changeValue.setText(QCoreApplication.translate("DashboardComponent", u"8.89%", None))
        self.changeValue.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"changePos", None))
        self.marketCard.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"card", None))
        self.marketTitle.setText(QCoreApplication.translate("DashboardComponent", u"Market", None))
        self.marketTitle.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"cardTitle", None))
        self.promoCard.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"promoCard", None))
        self.promoTitle.setText(QCoreApplication.translate("DashboardComponent", u"Unlimited access to\n"
"130+ assets", None))
        self.promoTitle.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"promoTitle", None))
        self.promoSub.setText(QCoreApplication.translate("DashboardComponent", u"Start earning today with\n"
"My Container and avg. APY of 10%", None))
        self.promoSub.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"promoSub", None))
        self.tradeCard.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"card", None))
        self.tradeTitle.setText(QCoreApplication.translate("DashboardComponent", u"Trade", None))
        self.tradeTitle.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"cardTitle", None))
        self.coinLabel.setText(QCoreApplication.translate("DashboardComponent", u"Coin", None))
        self.coinLabel.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"fieldLabel", None))
        self.coinField.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"field", None))
        self.coinAvatar.setProperty(u"text", QCoreApplication.translate("DashboardComponent", u"E", None))
        self.coinName.setText(QCoreApplication.translate("DashboardComponent", u"Ethereum", None))
        self.coinName.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"fieldValue", None))
        self.coinTicker.setText(QCoreApplication.translate("DashboardComponent", u"ETH", None))
        self.coinTicker.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"fieldMuted", None))
        self.coinFieldChevron.setText("")
        self.amountLabel.setText(QCoreApplication.translate("DashboardComponent", u"Amount", None))
        self.amountLabel.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"fieldLabel", None))
        self.amountField.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"field", None))
        self.amountBadge.setProperty(u"text", QCoreApplication.translate("DashboardComponent", u"$", None))
        self.amountEdit.setText(QCoreApplication.translate("DashboardComponent", u"34994", None))
        self.amountEdit.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"amountEdit", None))
        self.amountCurrency.setText(QCoreApplication.translate("DashboardComponent", u"USD", None))
        self.amountCurrency.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"fieldMuted", None))
        self.amountChevron.setText("")
        self.tradeRate.setText(QCoreApplication.translate("DashboardComponent", u"Exchange rate, 1 ETH = 1844.29", None))
        self.tradeRate.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"exchangeRate", None))
        self.receiptBox.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"receipt", None))
        self.promoCodeBtn.setText(QCoreApplication.translate("DashboardComponent", u"Promo Code", None))
        self.promoCodeBtn.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"link", None))
        self.feeLabel.setText(QCoreApplication.translate("DashboardComponent", u"Transfer fee:", None))
        self.feeLabel.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"receiptLabel", None))
        self.feeValue.setText(QCoreApplication.translate("DashboardComponent", u"2322.40", None))
        self.feeValue.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"receiptValue", None))
        self.receivedLabel.setText(QCoreApplication.translate("DashboardComponent", u"You received:", None))
        self.receivedLabel.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"receiptLabel", None))
        self.receivedValue.setText(QCoreApplication.translate("DashboardComponent", u"$33831.90", None))
        self.receivedValue.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"receiptBig", None))
        self.buyBtn.setText(QCoreApplication.translate("DashboardComponent", u"Buy ETH", None))
        pass
    # retranslateUi

