# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'new_DeviceHero.ui'
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
    QPushButton, QSizePolicy, QSlider, QSpacerItem,
    QVBoxLayout, QWidget)

from Custom_Widgets.QCustomGlassFrame import QCustomGlassFrame
from Custom_Widgets.QCustomQLabel import QCustomQLabel
from Custom_Widgets.QCustomQPushButton import QCustomQPushButton
class Ui_DeviceHero(object):
    def setupUi(self, DeviceHero):
        if not DeviceHero.objectName():
            DeviceHero.setObjectName(u"DeviceHero")
        DeviceHero.resize(520, 320)
        self.heroRoot = QVBoxLayout(DeviceHero)
        self.heroRoot.setSpacing(0)
        self.heroRoot.setObjectName(u"heroRoot")
        self.heroRoot.setContentsMargins(0, 0, 0, 0)
        self.heroGlass = QCustomGlassFrame(DeviceHero)
        self.heroGlass.setObjectName(u"heroGlass")
        self.heroGlass.setProperty(u"cornerRadius", 26)
        self.heroGlass.setProperty(u"liquidEdge", True)
        self.heroGlass.setProperty(u"edgeIntensity", 0.400000000000000)
        self.heroLayout = QHBoxLayout(self.heroGlass)
        self.heroLayout.setSpacing(18)
        self.heroLayout.setObjectName(u"heroLayout")
        self.heroLayout.setContentsMargins(20, 18, 20, 18)
        self.lampImage = QLabel(self.heroGlass)
        self.lampImage.setObjectName(u"lampImage")
        self.lampImage.setMinimumSize(QSize(128, 216))
        self.lampImage.setMaximumSize(QSize(128, 216))
        self.lampImage.setScaledContents(True)

        self.heroLayout.addWidget(self.lampImage, 0, Qt.AlignVCenter)

        self.heroBody = QVBoxLayout()
        self.heroBody.setSpacing(12)
        self.heroBody.setObjectName(u"heroBody")
        self.heroHeader = QHBoxLayout()
        self.heroHeader.setSpacing(10)
        self.heroHeader.setObjectName(u"heroHeader")
        self.heroTitles = QVBoxLayout()
        self.heroTitles.setSpacing(4)
        self.heroTitles.setObjectName(u"heroTitles")
        self.heroKicker = QLabel(self.heroGlass)
        self.heroKicker.setObjectName(u"heroKicker")

        self.heroTitles.addWidget(self.heroKicker)

        self.heroTitle = QLabel(self.heroGlass)
        self.heroTitle.setObjectName(u"heroTitle")
        self.heroTitle.setWordWrap(True)

        self.heroTitles.addWidget(self.heroTitle)


        self.heroHeader.addLayout(self.heroTitles)

        self.heroApps = QCustomQLabel(self.heroGlass)
        self.heroApps.setObjectName(u"heroApps")
        self.heroApps.setMinimumSize(QSize(26, 26))
        self.heroApps.setMaximumSize(QSize(26, 26))

        self.heroHeader.addWidget(self.heroApps, 0, Qt.AlignTop)


        self.heroBody.addLayout(self.heroHeader)

        self.heroStats = QCustomGlassFrame(self.heroGlass)
        self.heroStats.setObjectName(u"heroStats")
        self.heroStats.setProperty(u"cornerRadius", 18)
        self.heroStatsLayout = QHBoxLayout(self.heroStats)
        self.heroStatsLayout.setSpacing(20)
        self.heroStatsLayout.setObjectName(u"heroStatsLayout")
        self.heroStatsLayout.setContentsMargins(18, 14, 18, 14)
        self.timeCol = QVBoxLayout()
        self.timeCol.setSpacing(3)
        self.timeCol.setObjectName(u"timeCol")
        self.timeValue = QLabel(self.heroStats)
        self.timeValue.setObjectName(u"timeValue")

        self.timeCol.addWidget(self.timeValue)

        self.timeLabel = QLabel(self.heroStats)
        self.timeLabel.setObjectName(u"timeLabel")

        self.timeCol.addWidget(self.timeLabel)


        self.heroStatsLayout.addLayout(self.timeCol)

        self.statsDivider = QFrame(self.heroStats)
        self.statsDivider.setObjectName(u"statsDivider")
        self.statsDivider.setFrameShape(QFrame.VLine)
        self.statsDivider.setMaximumSize(QSize(1, 16777215))

        self.heroStatsLayout.addWidget(self.statsDivider)

        self.energyCol = QVBoxLayout()
        self.energyCol.setSpacing(3)
        self.energyCol.setObjectName(u"energyCol")
        self.energyValue = QLabel(self.heroStats)
        self.energyValue.setObjectName(u"energyValue")

        self.energyCol.addWidget(self.energyValue)

        self.energyLabel = QLabel(self.heroStats)
        self.energyLabel.setObjectName(u"energyLabel")

        self.energyCol.addWidget(self.energyLabel)


        self.heroStatsLayout.addLayout(self.energyCol)

        self.heroStatsSpacer = QSpacerItem(10, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.heroStatsLayout.addItem(self.heroStatsSpacer)


        self.heroBody.addWidget(self.heroStats)

        self.heroPills = QHBoxLayout()
        self.heroPills.setSpacing(12)
        self.heroPills.setObjectName(u"heroPills")
        self.onPill = QCustomQPushButton(self.heroGlass)
        self.onPill.setObjectName(u"onPill")
        self.onPill.setMinimumSize(QSize(0, 40))
        self.onPill.setIconSize(QSize(14, 14))
        self.onPill.setLayoutDirection(Qt.RightToLeft)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.onPill.sizePolicy().hasHeightForWidth())
        self.onPill.setSizePolicy(sizePolicy)

        self.heroPills.addWidget(self.onPill)

        self.offPill = QCustomQPushButton(self.heroGlass)
        self.offPill.setObjectName(u"offPill")
        self.offPill.setMinimumSize(QSize(0, 40))
        self.offPill.setIconSize(QSize(14, 14))
        self.offPill.setLayoutDirection(Qt.RightToLeft)
        sizePolicy.setHeightForWidth(self.offPill.sizePolicy().hasHeightForWidth())
        self.offPill.setSizePolicy(sizePolicy)

        self.heroPills.addWidget(self.offPill)


        self.heroBody.addLayout(self.heroPills)

        self.brightRow = QHBoxLayout()
        self.brightRow.setSpacing(12)
        self.brightRow.setObjectName(u"brightRow")
        self.brightIcon = QCustomQLabel(self.heroGlass)
        self.brightIcon.setObjectName(u"brightIcon")
        self.brightIcon.setMinimumSize(QSize(22, 22))
        self.brightIcon.setMaximumSize(QSize(22, 22))

        self.brightRow.addWidget(self.brightIcon)

        self.brightSlider = QSlider(self.heroGlass)
        self.brightSlider.setObjectName(u"brightSlider")
        self.brightSlider.setOrientation(Qt.Horizontal)
        self.brightSlider.setMinimum(0)
        self.brightSlider.setMaximum(100)
        self.brightSlider.setValue(72)

        self.brightRow.addWidget(self.brightSlider)


        self.heroBody.addLayout(self.brightRow)


        self.heroLayout.addLayout(self.heroBody)


        self.heroRoot.addWidget(self.heroGlass)


        self.retranslateUi(DeviceHero)

        QMetaObject.connectSlotsByName(DeviceHero)
    # setupUi

    def retranslateUi(self, DeviceHero):
        self.heroGlass.setProperty(u"backdropSource", QCoreApplication.translate("DeviceHero", u"wallpaper", None))
        self.lampImage.setText("")
        self.heroKicker.setText(QCoreApplication.translate("DeviceHero", u"Device", None))
        self.heroKicker.setProperty(u"role", QCoreApplication.translate("DeviceHero", u"kicker", None))
        self.heroTitle.setText(QCoreApplication.translate("DeviceHero", u"Luminens LED Modern Standing Lamp", None))
        self.heroTitle.setProperty(u"role", QCoreApplication.translate("DeviceHero", u"heroTitle", None))
        self.heroApps.setProperty(u"iconName", QCoreApplication.translate("DeviceHero", u"material_design/apps", None))
        self.heroApps.setProperty(u"role", QCoreApplication.translate("DeviceHero", u"appsIcon", None))
        self.heroStats.setProperty(u"backdropSource", QCoreApplication.translate("DeviceHero", u"wallpaper", None))
        self.timeValue.setText(QCoreApplication.translate("DeviceHero", u"4H 20M", None))
        self.timeValue.setProperty(u"role", QCoreApplication.translate("DeviceHero", u"statValueSm", None))
        self.timeLabel.setText(QCoreApplication.translate("DeviceHero", u"Time Usage", None))
        self.timeLabel.setProperty(u"role", QCoreApplication.translate("DeviceHero", u"mutedSm", None))
        self.energyValue.setText(QCoreApplication.translate("DeviceHero", u"72W", None))
        self.energyValue.setProperty(u"role", QCoreApplication.translate("DeviceHero", u"statValueSm", None))
        self.energyLabel.setText(QCoreApplication.translate("DeviceHero", u"Energy Consumption", None))
        self.energyLabel.setProperty(u"role", QCoreApplication.translate("DeviceHero", u"mutedSm", None))
        self.onPill.setText(QCoreApplication.translate("DeviceHero", u"On from 06:00 PM", None))
        self.onPill.setProperty(u"iconName", QCoreApplication.translate("DeviceHero", u"feather/chevron-down", None))
        self.onPill.setProperty(u"role", QCoreApplication.translate("DeviceHero", u"pill", None))
        self.offPill.setText(QCoreApplication.translate("DeviceHero", u"Off at 05:00 AM", None))
        self.offPill.setProperty(u"iconName", QCoreApplication.translate("DeviceHero", u"feather/chevron-down", None))
        self.offPill.setProperty(u"role", QCoreApplication.translate("DeviceHero", u"pill", None))
        self.brightIcon.setProperty(u"iconName", QCoreApplication.translate("DeviceHero", u"feather/sun", None))
        pass
    # retranslateUi

