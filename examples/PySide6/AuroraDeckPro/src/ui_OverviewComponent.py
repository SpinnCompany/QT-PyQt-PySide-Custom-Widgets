# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'new_OverviewComponent.ui'
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

from Custom_Widgets.QCustomAlert import QCustomAlert
from Custom_Widgets.QCustomAvatarGroup import QCustomAvatarGroup
from Custom_Widgets.QCustomBadge import QCustomBadge
from Custom_Widgets.QCustomComponent import QCustomComponent
from Custom_Widgets.QCustomFlowWidget import QCustomFlowWidget
from Custom_Widgets.QCustomKbd import QCustomKbd
from Custom_Widgets.QCustomStatCard import QCustomStatCard
from Custom_Widgets.QCustomTimeline import QCustomTimeline
class Ui_OverviewComponent(object):
    def setupUi(self, OverviewComponent):
        if not OverviewComponent.objectName():
            OverviewComponent.setObjectName(u"OverviewComponent")
        OverviewComponent.resize(1200, 760)
        self.overviewOuter = QVBoxLayout(OverviewComponent)
        self.overviewOuter.setSpacing(0)
        self.overviewOuter.setObjectName(u"overviewOuter")
        self.overviewOuter.setContentsMargins(0, 0, 0, 0)
        self.overviewScroll = QScrollArea(OverviewComponent)
        self.overviewScroll.setObjectName(u"overviewScroll")
        self.overviewScroll.setWidgetResizable(True)
        self.overviewScroll.setFrameShape(QFrame.NoFrame)
        self.overviewScroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.overviewScrollContents = QWidget()
        self.overviewScrollContents.setObjectName(u"overviewScrollContents")
        self.overviewScrollContents.setGeometry(QRect(0, 0, 1200, 760))
        self.overviewCenterRow = QHBoxLayout(self.overviewScrollContents)
        self.overviewCenterRow.setSpacing(0)
        self.overviewCenterRow.setObjectName(u"overviewCenterRow")
        self.overviewCenterRow.setContentsMargins(28, 28, 28, 28)
        self.ovLeftSpacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.overviewCenterRow.addItem(self.ovLeftSpacer)

        self.overviewColumn = QWidget(self.overviewScrollContents)
        self.overviewColumn.setObjectName(u"overviewColumn")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(20)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.overviewColumn.sizePolicy().hasHeightForWidth())
        self.overviewColumn.setSizePolicy(sizePolicy)
        self.overviewColumn.setMaximumSize(QSize(1320, 16777215))
        self.overviewColLayout = QVBoxLayout(self.overviewColumn)
        self.overviewColLayout.setSpacing(20)
        self.overviewColLayout.setObjectName(u"overviewColLayout")
        self.overviewColLayout.setContentsMargins(0, 0, 0, 0)
        self.heroFrame = QFrame(self.overviewColumn)
        self.heroFrame.setObjectName(u"heroFrame")
        self.heroFrame.setMinimumSize(QSize(0, 96))
        self.heroLayout = QHBoxLayout(self.heroFrame)
        self.heroLayout.setObjectName(u"heroLayout")
        self.heroLayout.setContentsMargins(24, 20, 24, 20)
        self.heroTextLayout = QVBoxLayout()
        self.heroTextLayout.setSpacing(4)
        self.heroTextLayout.setObjectName(u"heroTextLayout")
        self.heroTitle = QLabel(self.heroFrame)
        self.heroTitle.setObjectName(u"heroTitle")

        self.heroTextLayout.addWidget(self.heroTitle)

        self.heroSub = QLabel(self.heroFrame)
        self.heroSub.setObjectName(u"heroSub")

        self.heroTextLayout.addWidget(self.heroSub)


        self.heroLayout.addLayout(self.heroTextLayout)

        self.heroSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.heroLayout.addItem(self.heroSpacer)

        self.paletteHint = QLabel(self.heroFrame)
        self.paletteHint.setObjectName(u"paletteHint")

        self.heroLayout.addWidget(self.paletteHint, 0, Qt.AlignRight|Qt.AlignVCenter)

        self.paletteKbd = QCustomKbd(self.heroFrame)
        self.paletteKbd.setObjectName(u"paletteKbd")

        self.heroLayout.addWidget(self.paletteKbd, 0, Qt.AlignRight|Qt.AlignVCenter)


        self.overviewColLayout.addWidget(self.heroFrame)

        self.statsFlow = QCustomFlowWidget(self.overviewColumn)
        self.statsFlow.setObjectName(u"statsFlow")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.statsFlow.sizePolicy().hasHeightForWidth())
        self.statsFlow.setSizePolicy(sizePolicy1)
        self.statsFlow.setProperty(u"spacing", 16)
        self.statsFlow.setProperty(u"horizontalSpacing", 16)
        self.statsFlow.setProperty(u"verticalSpacing", 16)
        self.statsFlow.setProperty(u"margin", 0)
        self.statsFlow.setProperty(u"animationEnabled", True)
        self.statsFlow.setProperty(u"animationDuration", 300)
        self.statsFlow.setProperty(u"autoFillWidth", False)
        self.statsFlow.setProperty(u"autoFillHeight", False)
        self.statsFlow.setProperty(u"justifySpacing", False)
        self.statLive = QCustomStatCard(self.statsFlow)
        self.statLive.setObjectName(u"statLive")
        self.statLive.setGeometry(QRect(0, 0, 300, 112))
        self.statLive.setMinimumSize(QSize(300, 112))
        self.statLive.setMaximumSize(QSize(300, 112))
        self.statKp = QCustomStatCard(self.statsFlow)
        self.statKp.setObjectName(u"statKp")
        self.statKp.setGeometry(QRect(316, 0, 300, 112))
        self.statKp.setMinimumSize(QSize(300, 112))
        self.statKp.setMaximumSize(QSize(300, 112))
        self.statOdds = QCustomStatCard(self.statsFlow)
        self.statOdds.setObjectName(u"statOdds")
        self.statOdds.setGeometry(QRect(632, 0, 300, 112))
        self.statOdds.setMinimumSize(QSize(300, 112))
        self.statOdds.setMaximumSize(QSize(300, 112))
        self.statClear = QCustomStatCard(self.statsFlow)
        self.statClear.setObjectName(u"statClear")
        self.statClear.setGeometry(QRect(948, 0, 300, 112))
        self.statClear.setMinimumSize(QSize(300, 112))
        self.statClear.setMaximumSize(QSize(300, 112))

        self.overviewColLayout.addWidget(self.statsFlow)

        self.stormAlert = QCustomAlert(self.overviewColumn)
        self.stormAlert.setObjectName(u"stormAlert")
        self.stormAlert.setProperty(u"dismissible", True)

        self.overviewColLayout.addWidget(self.stormAlert)

        self.cardsRow = QHBoxLayout()
        self.cardsRow.setSpacing(16)
        self.cardsRow.setObjectName(u"cardsRow")
        self.activityCard = QFrame(self.overviewColumn)
        self.activityCard.setObjectName(u"activityCard")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(2)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.activityCard.sizePolicy().hasHeightForWidth())
        self.activityCard.setSizePolicy(sizePolicy2)
        self.activityLayout = QVBoxLayout(self.activityCard)
        self.activityLayout.setSpacing(10)
        self.activityLayout.setObjectName(u"activityLayout")
        self.activityLayout.setContentsMargins(18, 16, 18, 16)
        self.activityTitle = QLabel(self.activityCard)
        self.activityTitle.setObjectName(u"activityTitle")

        self.activityLayout.addWidget(self.activityTitle)

        self.activityTimeline = QCustomTimeline(self.activityCard)
        self.activityTimeline.setObjectName(u"activityTimeline")

        self.activityLayout.addWidget(self.activityTimeline)


        self.cardsRow.addWidget(self.activityCard)

        self.shiftCard = QFrame(self.overviewColumn)
        self.shiftCard.setObjectName(u"shiftCard")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.shiftCard.sizePolicy().hasHeightForWidth())
        self.shiftCard.setSizePolicy(sizePolicy3)
        self.shiftCard.setMinimumSize(QSize(320, 0))
        self.shiftCard.setMaximumSize(QSize(380, 16777215))
        self.shiftLayout = QVBoxLayout(self.shiftCard)
        self.shiftLayout.setSpacing(12)
        self.shiftLayout.setObjectName(u"shiftLayout")
        self.shiftLayout.setContentsMargins(18, 16, 18, 16)
        self.shiftTitle = QLabel(self.shiftCard)
        self.shiftTitle.setObjectName(u"shiftTitle")

        self.shiftLayout.addWidget(self.shiftTitle)

        self.shiftAvatars = QCustomAvatarGroup(self.shiftCard)
        self.shiftAvatars.setObjectName(u"shiftAvatars")
        self.shiftAvatars.setProperty(u"maxVisible", 5)
        self.shiftAvatars.setProperty(u"avatarSize", 36)

        self.shiftLayout.addWidget(self.shiftAvatars)

        self.badgeRow = QHBoxLayout()
        self.badgeRow.setSpacing(8)
        self.badgeRow.setObjectName(u"badgeRow")
        self.badgeLive = QCustomBadge(self.shiftCard)
        self.badgeLive.setObjectName(u"badgeLive")

        self.badgeRow.addWidget(self.badgeLive)

        self.badgeG2 = QCustomBadge(self.shiftCard)
        self.badgeG2.setObjectName(u"badgeG2")

        self.badgeRow.addWidget(self.badgeG2)

        self.badgeAlerts = QCustomBadge(self.shiftCard)
        self.badgeAlerts.setObjectName(u"badgeAlerts")

        self.badgeRow.addWidget(self.badgeAlerts)

        self.badgeSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.badgeRow.addItem(self.badgeSpacer)


        self.shiftLayout.addLayout(self.badgeRow)

        self.shiftVSpacer = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.shiftLayout.addItem(self.shiftVSpacer)


        self.cardsRow.addWidget(self.shiftCard)


        self.overviewColLayout.addLayout(self.cardsRow)

        self.pageSpacer = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.overviewColLayout.addItem(self.pageSpacer)


        self.overviewCenterRow.addWidget(self.overviewColumn)

        self.ovRightSpacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.overviewCenterRow.addItem(self.ovRightSpacer)

        self.overviewScroll.setWidget(self.overviewScrollContents)

        self.overviewOuter.addWidget(self.overviewScroll)


        self.retranslateUi(OverviewComponent)

        QMetaObject.connectSlotsByName(OverviewComponent)
    # setupUi

    def retranslateUi(self, OverviewComponent):
        self.heroFrame.setProperty(u"role", QCoreApplication.translate("OverviewComponent", u"hero", None))
        self.heroTitle.setProperty(u"role", QCoreApplication.translate("OverviewComponent", u"h1", None))
        self.heroTitle.setText(QCoreApplication.translate("OverviewComponent", u"\u2726  Good evening, Operator", None))
        self.heroSub.setProperty(u"role", QCoreApplication.translate("OverviewComponent", u"muted", None))
        self.heroSub.setText(QCoreApplication.translate("OverviewComponent", u"G2 storm watch is active. 8 of 12 stations reporting live.", None))
        self.paletteHint.setProperty(u"role", QCoreApplication.translate("OverviewComponent", u"muted", None))
        self.paletteHint.setText(QCoreApplication.translate("OverviewComponent", u"Command palette", None))
        self.paletteKbd.setProperty(u"keys", QCoreApplication.translate("OverviewComponent", u"Ctrl+K", None))
        self.statsFlow.setProperty(u"animationEasingCurve", QCoreApplication.translate("OverviewComponent", u"OutCubic", None))
        self.statLive.setProperty(u"label", QCoreApplication.translate("OverviewComponent", u"STATIONS LIVE", None))
        self.statLive.setProperty(u"value", QCoreApplication.translate("OverviewComponent", u"8 / 12", None))
        self.statLive.setProperty(u"caption", QCoreApplication.translate("OverviewComponent", u"Arctic belt", None))
        self.statLive.setProperty(u"trend", QCoreApplication.translate("OverviewComponent", u"up", None))
        self.statKp.setProperty(u"label", QCoreApplication.translate("OverviewComponent", u"PLANETARY Kp", None))
        self.statKp.setProperty(u"value", QCoreApplication.translate("OverviewComponent", u"6.2", None))
        self.statKp.setProperty(u"caption", QCoreApplication.translate("OverviewComponent", u"G2 watch", None))
        self.statKp.setProperty(u"trend", QCoreApplication.translate("OverviewComponent", u"up", None))
        self.statOdds.setProperty(u"label", QCoreApplication.translate("OverviewComponent", u"AURORA ODDS", None))
        self.statOdds.setProperty(u"value", QCoreApplication.translate("OverviewComponent", u"87%", None))
        self.statOdds.setProperty(u"caption", QCoreApplication.translate("OverviewComponent", u"\u226565\u00b0N", None))
        self.statOdds.setProperty(u"trend", QCoreApplication.translate("OverviewComponent", u"up", None))
        self.statClear.setProperty(u"label", QCoreApplication.translate("OverviewComponent", u"CLEAR SKIES", None))
        self.statClear.setProperty(u"value", QCoreApplication.translate("OverviewComponent", u"5", None))
        self.statClear.setProperty(u"caption", QCoreApplication.translate("OverviewComponent", u"cloud moving in", None))
        self.statClear.setProperty(u"trend", QCoreApplication.translate("OverviewComponent", u"down", None))
        self.stormAlert.setProperty(u"variant", QCoreApplication.translate("OverviewComponent", u"warning", None))
        self.stormAlert.setProperty(u"title", QCoreApplication.translate("OverviewComponent", u"Geomagnetic storm in progress", None))
        self.stormAlert.setProperty(u"text", QCoreApplication.translate("OverviewComponent", u"Kp has crossed 6. Aurora may be visible down to 60\u00b0N tonight.", None))
        self.activityCard.setProperty(u"role", QCoreApplication.translate("OverviewComponent", u"card", None))
        self.activityTitle.setProperty(u"role", QCoreApplication.translate("OverviewComponent", u"h2", None))
        self.activityTitle.setText(QCoreApplication.translate("OverviewComponent", u"Activity", None))
        self.shiftCard.setProperty(u"role", QCoreApplication.translate("OverviewComponent", u"card", None))
        self.shiftTitle.setProperty(u"role", QCoreApplication.translate("OverviewComponent", u"h2", None))
        self.shiftTitle.setText(QCoreApplication.translate("OverviewComponent", u"On shift", None))
        self.badgeLive.setProperty(u"text", QCoreApplication.translate("OverviewComponent", u"LIVE", None))
        self.badgeLive.setProperty(u"variant", QCoreApplication.translate("OverviewComponent", u"success", None))
        self.badgeG2.setProperty(u"text", QCoreApplication.translate("OverviewComponent", u"G2", None))
        self.badgeG2.setProperty(u"variant", QCoreApplication.translate("OverviewComponent", u"warning", None))
        self.badgeAlerts.setProperty(u"text", QCoreApplication.translate("OverviewComponent", u"3 alerts", None))
        self.badgeAlerts.setProperty(u"variant", QCoreApplication.translate("OverviewComponent", u"destructive", None))
        pass
    # retranslateUi

