# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'new_GalleryComponent.ui'
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

from Custom_Widgets.QCustomAvatarGroup import QCustomAvatarGroup
from Custom_Widgets.QCustomBadge import QCustomBadge
from Custom_Widgets.QCustomBreadcrumbs import QCustomBreadcrumbs
from Custom_Widgets.QCustomChip import QCustomChipGroup
from Custom_Widgets.QCustomColorPicker import QCustomColorPicker
from Custom_Widgets.QCustomComboBox import QCustomComboBox
from Custom_Widgets.QCustomComponent import QCustomComponent
from Custom_Widgets.QCustomFlowWidget import QCustomFlowWidget
from Custom_Widgets.QCustomKbd import QCustomKbd
from Custom_Widgets.QCustomNumberInput import QCustomNumberInput
from Custom_Widgets.QCustomPagination import QCustomPagination
from Custom_Widgets.QCustomProgressRing import QCustomProgressRing
from Custom_Widgets.QCustomQPushButton import QCustomQPushButton
from Custom_Widgets.QCustomRangeSlider import QCustomRangeSlider
from Custom_Widgets.QCustomRating import QCustomRating
from Custom_Widgets.QCustomSegmentedControl import QCustomSegmentedControl
from Custom_Widgets.QCustomSkeleton import QCustomSkeleton
from Custom_Widgets.QCustomSwitch import QCustomSwitch
class Ui_GalleryComponent(object):
    def setupUi(self, GalleryComponent):
        if not GalleryComponent.objectName():
            GalleryComponent.setObjectName(u"GalleryComponent")
        GalleryComponent.resize(940, 680)
        self.galleryOuter = QVBoxLayout(GalleryComponent)
        self.galleryOuter.setSpacing(0)
        self.galleryOuter.setObjectName(u"galleryOuter")
        self.galleryOuter.setContentsMargins(0, 0, 0, 0)
        self.galleryScroll = QScrollArea(GalleryComponent)
        self.galleryScroll.setObjectName(u"galleryScroll")
        self.galleryScroll.setWidgetResizable(True)
        self.galleryScroll.setFrameShape(QFrame.NoFrame)
        self.galleryScroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.galleryContent = QWidget()
        self.galleryContent.setObjectName(u"galleryContent")
        self.galleryContent.setGeometry(QRect(0, 0, 1200, 1200))
        self.galleryContentLayout = QVBoxLayout(self.galleryContent)
        self.galleryContentLayout.setSpacing(16)
        self.galleryContentLayout.setObjectName(u"galleryContentLayout")
        self.galleryContentLayout.setContentsMargins(28, 24, 28, 16)
        self.galleryHeader = QVBoxLayout()
        self.galleryHeader.setSpacing(2)
        self.galleryHeader.setObjectName(u"galleryHeader")
        self.galleryKicker = QLabel(self.galleryContent)
        self.galleryKicker.setObjectName(u"galleryKicker")

        self.galleryHeader.addWidget(self.galleryKicker)

        self.galleryTitle = QLabel(self.galleryContent)
        self.galleryTitle.setObjectName(u"galleryTitle")

        self.galleryHeader.addWidget(self.galleryTitle)

        self.gallerySub = QLabel(self.galleryContent)
        self.gallerySub.setObjectName(u"gallerySub")

        self.galleryHeader.addWidget(self.gallerySub)


        self.galleryContentLayout.addLayout(self.galleryHeader)

        self.galleryFlow = QCustomFlowWidget(self.galleryContent)
        self.galleryFlow.setObjectName(u"galleryFlow")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.galleryFlow.sizePolicy().hasHeightForWidth())
        self.galleryFlow.setSizePolicy(sizePolicy)
        self.galleryFlow.setProperty(u"spacing", 16)
        self.galleryFlow.setProperty(u"horizontalSpacing", 16)
        self.galleryFlow.setProperty(u"verticalSpacing", 16)
        self.galleryFlow.setProperty(u"margin", 0)
        self.galleryFlow.setProperty(u"animationEnabled", True)
        self.galleryFlow.setProperty(u"animationDuration", 300)
        self.galleryFlow.setProperty(u"autoFillWidth", False)
        self.galleryFlow.setProperty(u"autoFillHeight", False)
        self.galleryFlow.setProperty(u"justifySpacing", False)
        self.cardRating = QFrame(self.galleryFlow)
        self.cardRating.setObjectName(u"cardRating")
        self.cardRating.setGeometry(QRect(0, 0, 300, 160))
        self.cardRating.setMinimumSize(QSize(300, 160))
        self.cardRating.setMaximumSize(QSize(300, 160))
        self.lRating = QVBoxLayout(self.cardRating)
        self.lRating.setSpacing(10)
        self.lRating.setObjectName(u"lRating")
        self.lRating.setContentsMargins(16, 16, 16, 16)
        self.tRating = QLabel(self.cardRating)
        self.tRating.setObjectName(u"tRating")

        self.lRating.addWidget(self.tRating)

        self.gRating = QCustomRating(self.cardRating)
        self.gRating.setObjectName(u"gRating")
        self.gRating.setProperty(u"maximum", 5)
        self.gRating.setProperty(u"value", 4)

        self.lRating.addWidget(self.gRating)

        self.cardBadges = QFrame(self.galleryFlow)
        self.cardBadges.setObjectName(u"cardBadges")
        self.cardBadges.setGeometry(QRect(316, 0, 300, 160))
        self.cardBadges.setMinimumSize(QSize(300, 160))
        self.cardBadges.setMaximumSize(QSize(300, 160))
        self.lBadges = QVBoxLayout(self.cardBadges)
        self.lBadges.setSpacing(10)
        self.lBadges.setObjectName(u"lBadges")
        self.lBadges.setContentsMargins(16, 16, 16, 16)
        self.tBadges = QLabel(self.cardBadges)
        self.tBadges.setObjectName(u"tBadges")

        self.lBadges.addWidget(self.tBadges)

        self.badgesRow = QHBoxLayout()
        self.badgesRow.setSpacing(8)
        self.badgesRow.setObjectName(u"badgesRow")
        self.gBadgeDefault = QCustomBadge(self.cardBadges)
        self.gBadgeDefault.setObjectName(u"gBadgeDefault")

        self.badgesRow.addWidget(self.gBadgeDefault)

        self.gBadgeSuccess = QCustomBadge(self.cardBadges)
        self.gBadgeSuccess.setObjectName(u"gBadgeSuccess")

        self.badgesRow.addWidget(self.gBadgeSuccess)

        self.gBadgeWarning = QCustomBadge(self.cardBadges)
        self.gBadgeWarning.setObjectName(u"gBadgeWarning")

        self.badgesRow.addWidget(self.gBadgeWarning)

        self.gBadgeDanger = QCustomBadge(self.cardBadges)
        self.gBadgeDanger.setObjectName(u"gBadgeDanger")

        self.badgesRow.addWidget(self.gBadgeDanger)

        self.badgesSp = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.badgesRow.addItem(self.badgesSp)


        self.lBadges.addLayout(self.badgesRow)

        self.cardSwitches = QFrame(self.galleryFlow)
        self.cardSwitches.setObjectName(u"cardSwitches")
        self.cardSwitches.setGeometry(QRect(632, 0, 300, 160))
        self.cardSwitches.setMinimumSize(QSize(300, 160))
        self.cardSwitches.setMaximumSize(QSize(300, 160))
        self.lSwitches = QVBoxLayout(self.cardSwitches)
        self.lSwitches.setSpacing(10)
        self.lSwitches.setObjectName(u"lSwitches")
        self.lSwitches.setContentsMargins(16, 16, 16, 16)
        self.tSwitches = QLabel(self.cardSwitches)
        self.tSwitches.setObjectName(u"tSwitches")

        self.lSwitches.addWidget(self.tSwitches)

        self.switchRow = QHBoxLayout()
        self.switchRow.setSpacing(14)
        self.switchRow.setObjectName(u"switchRow")
        self.swAlertsLbl = QLabel(self.cardSwitches)
        self.swAlertsLbl.setObjectName(u"swAlertsLbl")

        self.switchRow.addWidget(self.swAlertsLbl)

        self.gSwAlerts = QCustomSwitch(self.cardSwitches)
        self.gSwAlerts.setObjectName(u"gSwAlerts")
        self.gSwAlerts.setProperty(u"checked", True)

        self.switchRow.addWidget(self.gSwAlerts)

        self.swCapLbl = QLabel(self.cardSwitches)
        self.swCapLbl.setObjectName(u"swCapLbl")

        self.switchRow.addWidget(self.swCapLbl)

        self.gSwCapture = QCustomSwitch(self.cardSwitches)
        self.gSwCapture.setObjectName(u"gSwCapture")
        self.gSwCapture.setProperty(u"checked", False)

        self.switchRow.addWidget(self.gSwCapture)

        self.switchSp = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.switchRow.addItem(self.switchSp)


        self.lSwitches.addLayout(self.switchRow)

        self.cardSegmented = QFrame(self.galleryFlow)
        self.cardSegmented.setObjectName(u"cardSegmented")
        self.cardSegmented.setGeometry(QRect(948, 0, 300, 160))
        self.cardSegmented.setMinimumSize(QSize(300, 160))
        self.cardSegmented.setMaximumSize(QSize(300, 160))
        self.lSeg = QVBoxLayout(self.cardSegmented)
        self.lSeg.setSpacing(10)
        self.lSeg.setObjectName(u"lSeg")
        self.lSeg.setContentsMargins(16, 16, 16, 16)
        self.tSeg = QLabel(self.cardSegmented)
        self.tSeg.setObjectName(u"tSeg")

        self.lSeg.addWidget(self.tSeg)

        self.gSegmented = QCustomSegmentedControl(self.cardSegmented)
        self.gSegmented.setObjectName(u"gSegmented")
        self.gSegmented.setProperty(u"currentIndex", 1)

        self.lSeg.addWidget(self.gSegmented)

        self.cardRange = QFrame(self.galleryFlow)
        self.cardRange.setObjectName(u"cardRange")
        self.cardRange.setGeometry(QRect(1264, 0, 300, 160))
        self.cardRange.setMinimumSize(QSize(300, 160))
        self.cardRange.setMaximumSize(QSize(300, 160))
        self.lRange = QVBoxLayout(self.cardRange)
        self.lRange.setSpacing(10)
        self.lRange.setObjectName(u"lRange")
        self.lRange.setContentsMargins(16, 16, 16, 16)
        self.tRange = QLabel(self.cardRange)
        self.tRange.setObjectName(u"tRange")

        self.lRange.addWidget(self.tRange)

        self.gRange = QCustomRangeSlider(self.cardRange)
        self.gRange.setObjectName(u"gRange")
        self.gRange.setProperty(u"minimum", 0)
        self.gRange.setProperty(u"maximum", 100)
        self.gRange.setProperty(u"lowerValue", 20)
        self.gRange.setProperty(u"upperValue", 80)

        self.lRange.addWidget(self.gRange)

        self.cardNumber = QFrame(self.galleryFlow)
        self.cardNumber.setObjectName(u"cardNumber")
        self.cardNumber.setGeometry(QRect(1580, 0, 300, 160))
        self.cardNumber.setMinimumSize(QSize(300, 160))
        self.cardNumber.setMaximumSize(QSize(300, 160))
        self.lNumber = QVBoxLayout(self.cardNumber)
        self.lNumber.setSpacing(10)
        self.lNumber.setObjectName(u"lNumber")
        self.lNumber.setContentsMargins(16, 16, 16, 16)
        self.tNumber = QLabel(self.cardNumber)
        self.tNumber.setObjectName(u"tNumber")

        self.lNumber.addWidget(self.tNumber)

        self.gNumber = QCustomNumberInput(self.cardNumber)
        self.gNumber.setObjectName(u"gNumber")
        self.gNumber.setProperty(u"minimum", 0.000000000000000)
        self.gNumber.setProperty(u"maximum", 9.000000000000000)
        self.gNumber.setProperty(u"singleStep", 1.000000000000000)
        self.gNumber.setProperty(u"decimals", 0)

        self.lNumber.addWidget(self.gNumber)

        self.cardKbd = QFrame(self.galleryFlow)
        self.cardKbd.setObjectName(u"cardKbd")
        self.cardKbd.setGeometry(QRect(1896, 0, 300, 160))
        self.cardKbd.setMinimumSize(QSize(300, 160))
        self.cardKbd.setMaximumSize(QSize(300, 160))
        self.lKbd = QVBoxLayout(self.cardKbd)
        self.lKbd.setSpacing(10)
        self.lKbd.setObjectName(u"lKbd")
        self.lKbd.setContentsMargins(16, 16, 16, 16)
        self.tKbd = QLabel(self.cardKbd)
        self.tKbd.setObjectName(u"tKbd")

        self.lKbd.addWidget(self.tKbd)

        self.kbdRow = QHBoxLayout()
        self.kbdRow.setSpacing(10)
        self.kbdRow.setObjectName(u"kbdRow")
        self.gKbd1 = QCustomKbd(self.cardKbd)
        self.gKbd1.setObjectName(u"gKbd1")

        self.kbdRow.addWidget(self.gKbd1)

        self.gKbd2 = QCustomKbd(self.cardKbd)
        self.gKbd2.setObjectName(u"gKbd2")

        self.kbdRow.addWidget(self.gKbd2)

        self.kbdSp = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.kbdRow.addItem(self.kbdSp)


        self.lKbd.addLayout(self.kbdRow)

        self.cardPagination = QFrame(self.galleryFlow)
        self.cardPagination.setObjectName(u"cardPagination")
        self.cardPagination.setGeometry(QRect(2212, 0, 300, 160))
        self.cardPagination.setMinimumSize(QSize(300, 160))
        self.cardPagination.setMaximumSize(QSize(300, 160))
        self.lPag = QVBoxLayout(self.cardPagination)
        self.lPag.setSpacing(10)
        self.lPag.setObjectName(u"lPag")
        self.lPag.setContentsMargins(16, 16, 16, 16)
        self.tPag = QLabel(self.cardPagination)
        self.tPag.setObjectName(u"tPag")

        self.lPag.addWidget(self.tPag)

        self.gPagination = QCustomPagination(self.cardPagination)
        self.gPagination.setObjectName(u"gPagination")
        self.gPagination.setProperty(u"pageCount", 8)
        self.gPagination.setProperty(u"currentPage", 3)

        self.lPag.addWidget(self.gPagination)

        self.cardColor = QFrame(self.galleryFlow)
        self.cardColor.setObjectName(u"cardColor")
        self.cardColor.setGeometry(QRect(2528, 0, 300, 160))
        self.cardColor.setMinimumSize(QSize(300, 160))
        self.cardColor.setMaximumSize(QSize(300, 160))
        self.lColor = QVBoxLayout(self.cardColor)
        self.lColor.setSpacing(10)
        self.lColor.setObjectName(u"lColor")
        self.lColor.setContentsMargins(16, 16, 16, 16)
        self.tColor = QLabel(self.cardColor)
        self.tColor.setObjectName(u"tColor")

        self.lColor.addWidget(self.tColor)

        self.gColorPicker = QCustomColorPicker(self.cardColor)
        self.gColorPicker.setObjectName(u"gColorPicker")

        self.lColor.addWidget(self.gColorPicker)

        self.cardRings = QFrame(self.galleryFlow)
        self.cardRings.setObjectName(u"cardRings")
        self.cardRings.setGeometry(QRect(2844, 0, 300, 160))
        self.cardRings.setMinimumSize(QSize(300, 160))
        self.cardRings.setMaximumSize(QSize(300, 160))
        self.lRings = QVBoxLayout(self.cardRings)
        self.lRings.setSpacing(10)
        self.lRings.setObjectName(u"lRings")
        self.lRings.setContentsMargins(16, 16, 16, 16)
        self.tRings = QLabel(self.cardRings)
        self.tRings.setObjectName(u"tRings")

        self.lRings.addWidget(self.tRings)

        self.ringsGalRow = QHBoxLayout()
        self.ringsGalRow.setSpacing(14)
        self.ringsGalRow.setObjectName(u"ringsGalRow")
        self.gRing1 = QCustomProgressRing(self.cardRings)
        self.gRing1.setObjectName(u"gRing1")
        self.gRing1.setMinimumSize(QSize(72, 72))
        self.gRing1.setMaximumSize(QSize(72, 72))
        self.gRing1.setProperty(u"value", 34)

        self.ringsGalRow.addWidget(self.gRing1)

        self.gRing2 = QCustomProgressRing(self.cardRings)
        self.gRing2.setObjectName(u"gRing2")
        self.gRing2.setMinimumSize(QSize(72, 72))
        self.gRing2.setMaximumSize(QSize(72, 72))
        self.gRing2.setProperty(u"value", 62)

        self.ringsGalRow.addWidget(self.gRing2)

        self.gRing3 = QCustomProgressRing(self.cardRings)
        self.gRing3.setObjectName(u"gRing3")
        self.gRing3.setMinimumSize(QSize(72, 72))
        self.gRing3.setMaximumSize(QSize(72, 72))
        self.gRing3.setProperty(u"value", 87)

        self.ringsGalRow.addWidget(self.gRing3)

        self.ringsGalSp = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.ringsGalRow.addItem(self.ringsGalSp)


        self.lRings.addLayout(self.ringsGalRow)

        self.cardChips = QFrame(self.galleryFlow)
        self.cardChips.setObjectName(u"cardChips")
        self.cardChips.setGeometry(QRect(3160, 0, 300, 160))
        self.cardChips.setMinimumSize(QSize(300, 160))
        self.cardChips.setMaximumSize(QSize(300, 160))
        self.lChips = QVBoxLayout(self.cardChips)
        self.lChips.setSpacing(10)
        self.lChips.setObjectName(u"lChips")
        self.lChips.setContentsMargins(16, 16, 16, 16)
        self.tChips = QLabel(self.cardChips)
        self.tChips.setObjectName(u"tChips")

        self.lChips.addWidget(self.tChips)

        self.gChips = QCustomChipGroup(self.cardChips)
        self.gChips.setObjectName(u"gChips")
        self.gChips.setProperty(u"selectable", True)

        self.lChips.addWidget(self.gChips)

        self.cardCombo = QFrame(self.galleryFlow)
        self.cardCombo.setObjectName(u"cardCombo")
        self.cardCombo.setGeometry(QRect(3476, 0, 300, 160))
        self.cardCombo.setMinimumSize(QSize(300, 160))
        self.cardCombo.setMaximumSize(QSize(300, 160))
        self.lCombo = QVBoxLayout(self.cardCombo)
        self.lCombo.setSpacing(10)
        self.lCombo.setObjectName(u"lCombo")
        self.lCombo.setContentsMargins(16, 16, 16, 16)
        self.tCombo = QLabel(self.cardCombo)
        self.tCombo.setObjectName(u"tCombo")

        self.lCombo.addWidget(self.tCombo)

        self.gCombo = QCustomComboBox(self.cardCombo)
        self.gCombo.setObjectName(u"gCombo")
        self.gCombo.setProperty(u"editable", False)

        self.lCombo.addWidget(self.gCombo)

        self.cardAvatars = QFrame(self.galleryFlow)
        self.cardAvatars.setObjectName(u"cardAvatars")
        self.cardAvatars.setGeometry(QRect(3792, 0, 300, 160))
        self.cardAvatars.setMinimumSize(QSize(300, 160))
        self.cardAvatars.setMaximumSize(QSize(300, 160))
        self.lAvatars = QVBoxLayout(self.cardAvatars)
        self.lAvatars.setSpacing(10)
        self.lAvatars.setObjectName(u"lAvatars")
        self.lAvatars.setContentsMargins(16, 16, 16, 16)
        self.tAvatars = QLabel(self.cardAvatars)
        self.tAvatars.setObjectName(u"tAvatars")

        self.lAvatars.addWidget(self.tAvatars)

        self.gAvatars = QCustomAvatarGroup(self.cardAvatars)
        self.gAvatars.setObjectName(u"gAvatars")
        self.gAvatars.setProperty(u"maxVisible", 5)
        self.gAvatars.setProperty(u"avatarSize", 34)

        self.lAvatars.addWidget(self.gAvatars)

        self.cardSkeleton = QFrame(self.galleryFlow)
        self.cardSkeleton.setObjectName(u"cardSkeleton")
        self.cardSkeleton.setGeometry(QRect(4108, 0, 300, 160))
        self.cardSkeleton.setMinimumSize(QSize(300, 160))
        self.cardSkeleton.setMaximumSize(QSize(300, 160))
        self.lSkel = QVBoxLayout(self.cardSkeleton)
        self.lSkel.setSpacing(8)
        self.lSkel.setObjectName(u"lSkel")
        self.lSkel.setContentsMargins(16, 16, 16, 16)
        self.tSkel = QLabel(self.cardSkeleton)
        self.tSkel.setObjectName(u"tSkel")

        self.lSkel.addWidget(self.tSkel)

        self.gSkel1 = QCustomSkeleton(self.cardSkeleton)
        self.gSkel1.setObjectName(u"gSkel1")
        self.gSkel1.setMinimumSize(QSize(0, 14))

        self.lSkel.addWidget(self.gSkel1)

        self.gSkel2 = QCustomSkeleton(self.cardSkeleton)
        self.gSkel2.setObjectName(u"gSkel2")
        self.gSkel2.setMinimumSize(QSize(0, 14))

        self.lSkel.addWidget(self.gSkel2)

        self.cardBreadcrumbs = QFrame(self.galleryFlow)
        self.cardBreadcrumbs.setObjectName(u"cardBreadcrumbs")
        self.cardBreadcrumbs.setGeometry(QRect(4424, 0, 300, 160))
        self.cardBreadcrumbs.setMinimumSize(QSize(300, 160))
        self.cardBreadcrumbs.setMaximumSize(QSize(300, 160))
        self.lBc = QVBoxLayout(self.cardBreadcrumbs)
        self.lBc.setSpacing(10)
        self.lBc.setObjectName(u"lBc")
        self.lBc.setContentsMargins(16, 16, 16, 16)
        self.tBc = QLabel(self.cardBreadcrumbs)
        self.tBc.setObjectName(u"tBc")

        self.lBc.addWidget(self.tBc)

        self.gBreadcrumbs = QCustomBreadcrumbs(self.cardBreadcrumbs)
        self.gBreadcrumbs.setObjectName(u"gBreadcrumbs")

        self.lBc.addWidget(self.gBreadcrumbs)

        self.cardToasts = QFrame(self.galleryFlow)
        self.cardToasts.setObjectName(u"cardToasts")
        self.cardToasts.setGeometry(QRect(4740, 0, 300, 160))
        self.cardToasts.setMinimumSize(QSize(300, 160))
        self.cardToasts.setMaximumSize(QSize(300, 160))
        self.lToasts = QVBoxLayout(self.cardToasts)
        self.lToasts.setSpacing(10)
        self.lToasts.setObjectName(u"lToasts")
        self.lToasts.setContentsMargins(16, 16, 16, 16)
        self.tToasts = QLabel(self.cardToasts)
        self.tToasts.setObjectName(u"tToasts")

        self.lToasts.addWidget(self.tToasts)

        self.toastRow = QHBoxLayout()
        self.toastRow.setSpacing(8)
        self.toastRow.setObjectName(u"toastRow")
        self.gToastInfo = QCustomQPushButton(self.cardToasts)
        self.gToastInfo.setObjectName(u"gToastInfo")

        self.toastRow.addWidget(self.gToastInfo)

        self.gToastSuccess = QCustomQPushButton(self.cardToasts)
        self.gToastSuccess.setObjectName(u"gToastSuccess")

        self.toastRow.addWidget(self.gToastSuccess)

        self.gToastWarning = QCustomQPushButton(self.cardToasts)
        self.gToastWarning.setObjectName(u"gToastWarning")

        self.toastRow.addWidget(self.gToastWarning)

        self.toastSp = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.toastRow.addItem(self.toastSp)


        self.lToasts.addLayout(self.toastRow)


        self.galleryContentLayout.addWidget(self.galleryFlow)

        self.gallerySpacer = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.galleryContentLayout.addItem(self.gallerySpacer)

        self.galleryScroll.setWidget(self.galleryContent)

        self.galleryOuter.addWidget(self.galleryScroll)


        self.retranslateUi(GalleryComponent)

        QMetaObject.connectSlotsByName(GalleryComponent)
    # setupUi

    def retranslateUi(self, GalleryComponent):
        self.galleryKicker.setProperty(u"role", QCoreApplication.translate("GalleryComponent", u"kicker", None))
        self.galleryKicker.setText(QCoreApplication.translate("GalleryComponent", u"EVERYTHING", None))
        self.galleryTitle.setProperty(u"role", QCoreApplication.translate("GalleryComponent", u"h1", None))
        self.galleryTitle.setText(QCoreApplication.translate("GalleryComponent", u"Widget Gallery", None))
        self.gallerySub.setProperty(u"role", QCoreApplication.translate("GalleryComponent", u"muted", None))
        self.gallerySub.setText(QCoreApplication.translate("GalleryComponent", u"A tour of the design-token widget set.", None))
        self.galleryFlow.setProperty(u"animationEasingCurve", QCoreApplication.translate("GalleryComponent", u"OutCubic", None))
        self.cardRating.setProperty(u"role", QCoreApplication.translate("GalleryComponent", u"card", None))
        self.tRating.setProperty(u"role", QCoreApplication.translate("GalleryComponent", u"kicker", None))
        self.tRating.setText(QCoreApplication.translate("GalleryComponent", u"RATING", None))
        self.cardBadges.setProperty(u"role", QCoreApplication.translate("GalleryComponent", u"card", None))
        self.tBadges.setProperty(u"role", QCoreApplication.translate("GalleryComponent", u"kicker", None))
        self.tBadges.setText(QCoreApplication.translate("GalleryComponent", u"BADGES", None))
        self.gBadgeDefault.setProperty(u"text", QCoreApplication.translate("GalleryComponent", u"Default", None))
        self.gBadgeDefault.setProperty(u"variant", QCoreApplication.translate("GalleryComponent", u"default", None))
        self.gBadgeSuccess.setProperty(u"text", QCoreApplication.translate("GalleryComponent", u"Success", None))
        self.gBadgeSuccess.setProperty(u"variant", QCoreApplication.translate("GalleryComponent", u"success", None))
        self.gBadgeWarning.setProperty(u"text", QCoreApplication.translate("GalleryComponent", u"Warning", None))
        self.gBadgeWarning.setProperty(u"variant", QCoreApplication.translate("GalleryComponent", u"warning", None))
        self.gBadgeDanger.setProperty(u"text", QCoreApplication.translate("GalleryComponent", u"Danger", None))
        self.gBadgeDanger.setProperty(u"variant", QCoreApplication.translate("GalleryComponent", u"destructive", None))
        self.cardSwitches.setProperty(u"role", QCoreApplication.translate("GalleryComponent", u"card", None))
        self.tSwitches.setProperty(u"role", QCoreApplication.translate("GalleryComponent", u"kicker", None))
        self.tSwitches.setText(QCoreApplication.translate("GalleryComponent", u"SWITCHES", None))
        self.swAlertsLbl.setProperty(u"role", QCoreApplication.translate("GalleryComponent", u"muted", None))
        self.swAlertsLbl.setText(QCoreApplication.translate("GalleryComponent", u"Alerts", None))
        self.swCapLbl.setProperty(u"role", QCoreApplication.translate("GalleryComponent", u"muted", None))
        self.swCapLbl.setText(QCoreApplication.translate("GalleryComponent", u"Auto-capture", None))
        self.cardSegmented.setProperty(u"role", QCoreApplication.translate("GalleryComponent", u"card", None))
        self.tSeg.setProperty(u"role", QCoreApplication.translate("GalleryComponent", u"kicker", None))
        self.tSeg.setText(QCoreApplication.translate("GalleryComponent", u"SEGMENTED CONTROL", None))
        self.cardRange.setProperty(u"role", QCoreApplication.translate("GalleryComponent", u"card", None))
        self.tRange.setProperty(u"role", QCoreApplication.translate("GalleryComponent", u"kicker", None))
        self.tRange.setText(QCoreApplication.translate("GalleryComponent", u"RANGE SLIDER", None))
        self.cardNumber.setProperty(u"role", QCoreApplication.translate("GalleryComponent", u"card", None))
        self.tNumber.setProperty(u"role", QCoreApplication.translate("GalleryComponent", u"kicker", None))
        self.tNumber.setText(QCoreApplication.translate("GalleryComponent", u"NUMBER INPUT", None))
        self.cardKbd.setProperty(u"role", QCoreApplication.translate("GalleryComponent", u"card", None))
        self.tKbd.setProperty(u"role", QCoreApplication.translate("GalleryComponent", u"kicker", None))
        self.tKbd.setText(QCoreApplication.translate("GalleryComponent", u"KEYBOARD SHORTCUTS", None))
        self.gKbd1.setProperty(u"keys", QCoreApplication.translate("GalleryComponent", u"Ctrl+K", None))
        self.gKbd2.setProperty(u"keys", QCoreApplication.translate("GalleryComponent", u"Ctrl+Shift+P", None))
        self.cardPagination.setProperty(u"role", QCoreApplication.translate("GalleryComponent", u"card", None))
        self.tPag.setProperty(u"role", QCoreApplication.translate("GalleryComponent", u"kicker", None))
        self.tPag.setText(QCoreApplication.translate("GalleryComponent", u"PAGINATION", None))
        self.cardColor.setProperty(u"role", QCoreApplication.translate("GalleryComponent", u"card", None))
        self.tColor.setProperty(u"role", QCoreApplication.translate("GalleryComponent", u"kicker", None))
        self.tColor.setText(QCoreApplication.translate("GalleryComponent", u"COLOR PICKER", None))
        self.cardRings.setProperty(u"role", QCoreApplication.translate("GalleryComponent", u"card", None))
        self.tRings.setProperty(u"role", QCoreApplication.translate("GalleryComponent", u"kicker", None))
        self.tRings.setText(QCoreApplication.translate("GalleryComponent", u"PROGRESS RINGS", None))
        self.cardChips.setProperty(u"role", QCoreApplication.translate("GalleryComponent", u"card", None))
        self.tChips.setProperty(u"role", QCoreApplication.translate("GalleryComponent", u"kicker", None))
        self.tChips.setText(QCoreApplication.translate("GalleryComponent", u"CHIPS", None))
        self.cardCombo.setProperty(u"role", QCoreApplication.translate("GalleryComponent", u"card", None))
        self.tCombo.setProperty(u"role", QCoreApplication.translate("GalleryComponent", u"kicker", None))
        self.tCombo.setText(QCoreApplication.translate("GalleryComponent", u"COMBO BOX", None))
        self.cardAvatars.setProperty(u"role", QCoreApplication.translate("GalleryComponent", u"card", None))
        self.tAvatars.setProperty(u"role", QCoreApplication.translate("GalleryComponent", u"kicker", None))
        self.tAvatars.setText(QCoreApplication.translate("GalleryComponent", u"AVATAR GROUP", None))
        self.cardSkeleton.setProperty(u"role", QCoreApplication.translate("GalleryComponent", u"card", None))
        self.tSkel.setProperty(u"role", QCoreApplication.translate("GalleryComponent", u"kicker", None))
        self.tSkel.setText(QCoreApplication.translate("GalleryComponent", u"LOADING SKELETON", None))
        self.gSkel1.setProperty(u"shape", QCoreApplication.translate("GalleryComponent", u"line", None))
        self.gSkel2.setProperty(u"shape", QCoreApplication.translate("GalleryComponent", u"line", None))
        self.cardBreadcrumbs.setProperty(u"role", QCoreApplication.translate("GalleryComponent", u"card", None))
        self.tBc.setProperty(u"role", QCoreApplication.translate("GalleryComponent", u"kicker", None))
        self.tBc.setText(QCoreApplication.translate("GalleryComponent", u"BREADCRUMBS", None))
        self.cardToasts.setProperty(u"role", QCoreApplication.translate("GalleryComponent", u"card", None))
        self.tToasts.setProperty(u"role", QCoreApplication.translate("GalleryComponent", u"kicker", None))
        self.tToasts.setText(QCoreApplication.translate("GalleryComponent", u"TOASTS", None))
        self.gToastInfo.setText(QCoreApplication.translate("GalleryComponent", u"Info", None))
        self.gToastInfo.setProperty(u"variant", QCoreApplication.translate("GalleryComponent", u"outline", None))
        self.gToastInfo.setProperty(u"sizeVariant", QCoreApplication.translate("GalleryComponent", u"sm", None))
        self.gToastSuccess.setText(QCoreApplication.translate("GalleryComponent", u"Success", None))
        self.gToastSuccess.setProperty(u"variant", QCoreApplication.translate("GalleryComponent", u"outline", None))
        self.gToastSuccess.setProperty(u"sizeVariant", QCoreApplication.translate("GalleryComponent", u"sm", None))
        self.gToastWarning.setText(QCoreApplication.translate("GalleryComponent", u"Warning", None))
        self.gToastWarning.setProperty(u"variant", QCoreApplication.translate("GalleryComponent", u"outline", None))
        self.gToastWarning.setProperty(u"sizeVariant", QCoreApplication.translate("GalleryComponent", u"sm", None))
        pass
    # retranslateUi

