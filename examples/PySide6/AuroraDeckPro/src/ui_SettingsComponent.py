# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'new_SettingsComponent.ui'
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

from Custom_Widgets.QCustomColorPicker import QCustomColorPicker
from Custom_Widgets.QCustomComponent import QCustomComponent
from Custom_Widgets.QCustomQPushButton import QCustomQPushButton
from Custom_Widgets.QCustomSegmentedControl import QCustomSegmentedControl
from Custom_Widgets.QCustomSwitch import QCustomSwitch
from Custom_Widgets.QCustomThemeDarkLightToggle import QCustomThemeDarkLightToggle
class Ui_SettingsComponent(object):
    def setupUi(self, SettingsComponent):
        if not SettingsComponent.objectName():
            SettingsComponent.setObjectName(u"SettingsComponent")
        SettingsComponent.resize(940, 680)
        self.SettingsOuter = QVBoxLayout(SettingsComponent)
        self.SettingsOuter.setSpacing(0)
        self.SettingsOuter.setObjectName(u"SettingsOuter")
        self.SettingsOuter.setContentsMargins(0, 0, 0, 0)
        self.SettingsScroll = QScrollArea(SettingsComponent)
        self.SettingsScroll.setObjectName(u"SettingsScroll")
        self.SettingsScroll.setWidgetResizable(True)
        self.SettingsScroll.setFrameShape(QFrame.NoFrame)
        self.SettingsScroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.SettingsScrollContents = QWidget()
        self.SettingsScrollContents.setObjectName(u"SettingsScrollContents")
        self.SettingsScrollContents.setGeometry(QRect(0, 0, 1200, 760))
        self.SettingsCenterRow = QHBoxLayout(self.SettingsScrollContents)
        self.SettingsCenterRow.setSpacing(0)
        self.SettingsCenterRow.setObjectName(u"SettingsCenterRow")
        self.SettingsCenterRow.setContentsMargins(28, 24, 28, 24)
        self.SettingsLeftSp = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.SettingsCenterRow.addItem(self.SettingsLeftSp)

        self.SettingsColumn = QWidget(self.SettingsScrollContents)
        self.SettingsColumn.setObjectName(u"SettingsColumn")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(20)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SettingsColumn.sizePolicy().hasHeightForWidth())
        self.SettingsColumn.setSizePolicy(sizePolicy)
        self.SettingsColumn.setMaximumSize(QSize(900, 16777215))
        self.SettingsColLayout = QVBoxLayout(self.SettingsColumn)
        self.SettingsColLayout.setSpacing(14)
        self.SettingsColLayout.setObjectName(u"SettingsColLayout")
        self.SettingsColLayout.setContentsMargins(0, 0, 0, 0)
        self.settingsHeader = QVBoxLayout()
        self.settingsHeader.setSpacing(2)
        self.settingsHeader.setObjectName(u"settingsHeader")
        self.settingsKicker = QLabel(self.SettingsColumn)
        self.settingsKicker.setObjectName(u"settingsKicker")

        self.settingsHeader.addWidget(self.settingsKicker)

        self.settingsTitle = QLabel(self.SettingsColumn)
        self.settingsTitle.setObjectName(u"settingsTitle")

        self.settingsHeader.addWidget(self.settingsTitle)

        self.settingsSub = QLabel(self.SettingsColumn)
        self.settingsSub.setObjectName(u"settingsSub")

        self.settingsHeader.addWidget(self.settingsSub)


        self.SettingsColLayout.addLayout(self.settingsHeader)

        self.appearanceCard = QFrame(self.SettingsColumn)
        self.appearanceCard.setObjectName(u"appearanceCard")
        self.appearanceLayout = QVBoxLayout(self.appearanceCard)
        self.appearanceLayout.setSpacing(12)
        self.appearanceLayout.setObjectName(u"appearanceLayout")
        self.appearanceLayout.setContentsMargins(18, 16, 18, 16)
        self.appearanceTitle = QLabel(self.appearanceCard)
        self.appearanceTitle.setObjectName(u"appearanceTitle")

        self.appearanceLayout.addWidget(self.appearanceTitle)

        self.appearanceSub = QLabel(self.appearanceCard)
        self.appearanceSub.setObjectName(u"appearanceSub")

        self.appearanceLayout.addWidget(self.appearanceSub)

        self.themeRow = QHBoxLayout()
        self.themeRow.setSpacing(12)
        self.themeRow.setObjectName(u"themeRow")
        self.themeSeg = QCustomSegmentedControl(self.appearanceCard)
        self.themeSeg.setObjectName(u"themeSeg")
        self.themeSeg.setProperty(u"currentIndex", 1)

        self.themeRow.addWidget(self.themeSeg)

        self.themeToggle = QCustomThemeDarkLightToggle(self.appearanceCard)
        self.themeToggle.setObjectName(u"themeToggle")

        self.themeRow.addWidget(self.themeToggle)

        self.themeSp = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.themeRow.addItem(self.themeSp)


        self.appearanceLayout.addLayout(self.themeRow)

        self.accentPicker = QCustomColorPicker(self.appearanceCard)
        self.accentPicker.setObjectName(u"accentPicker")

        self.appearanceLayout.addWidget(self.accentPicker)


        self.SettingsColLayout.addWidget(self.appearanceCard)

        self.notifCard = QFrame(self.SettingsColumn)
        self.notifCard.setObjectName(u"notifCard")
        self.notifLayout = QVBoxLayout(self.notifCard)
        self.notifLayout.setSpacing(10)
        self.notifLayout.setObjectName(u"notifLayout")
        self.notifLayout.setContentsMargins(18, 16, 18, 16)
        self.notifTitle = QLabel(self.notifCard)
        self.notifTitle.setObjectName(u"notifTitle")

        self.notifLayout.addWidget(self.notifTitle)

        self.notifStormRow = QHBoxLayout()
        self.notifStormRow.setObjectName(u"notifStormRow")
        self.notifStormLbl = QLabel(self.notifCard)
        self.notifStormLbl.setObjectName(u"notifStormLbl")

        self.notifStormRow.addWidget(self.notifStormLbl)

        self.notifStormSp = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.notifStormRow.addItem(self.notifStormSp)

        self.notifStorm = QCustomSwitch(self.notifCard)
        self.notifStorm.setObjectName(u"notifStorm")
        self.notifStorm.setProperty(u"checked", True)

        self.notifStormRow.addWidget(self.notifStorm)


        self.notifLayout.addLayout(self.notifStormRow)

        self.notifOfflineRow = QHBoxLayout()
        self.notifOfflineRow.setObjectName(u"notifOfflineRow")
        self.notifOfflineLbl = QLabel(self.notifCard)
        self.notifOfflineLbl.setObjectName(u"notifOfflineLbl")

        self.notifOfflineRow.addWidget(self.notifOfflineLbl)

        self.notifOfflineSp = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.notifOfflineRow.addItem(self.notifOfflineSp)

        self.notifOffline = QCustomSwitch(self.notifCard)
        self.notifOffline.setObjectName(u"notifOffline")
        self.notifOffline.setProperty(u"checked", True)

        self.notifOfflineRow.addWidget(self.notifOffline)


        self.notifLayout.addLayout(self.notifOfflineRow)

        self.notifClearRow = QHBoxLayout()
        self.notifClearRow.setObjectName(u"notifClearRow")
        self.notifClearLbl = QLabel(self.notifCard)
        self.notifClearLbl.setObjectName(u"notifClearLbl")

        self.notifClearRow.addWidget(self.notifClearLbl)

        self.notifClearSp = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.notifClearRow.addItem(self.notifClearSp)

        self.notifClear = QCustomSwitch(self.notifCard)
        self.notifClear.setObjectName(u"notifClear")
        self.notifClear.setProperty(u"checked", False)

        self.notifClearRow.addWidget(self.notifClear)


        self.notifLayout.addLayout(self.notifClearRow)


        self.SettingsColLayout.addWidget(self.notifCard)

        self.saveBtn = QCustomQPushButton(self.SettingsColumn)
        self.saveBtn.setObjectName(u"saveBtn")

        self.SettingsColLayout.addWidget(self.saveBtn)

        self.settingsSpacer = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.SettingsColLayout.addItem(self.settingsSpacer)


        self.SettingsCenterRow.addWidget(self.SettingsColumn)

        self.SettingsRightSp = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.SettingsCenterRow.addItem(self.SettingsRightSp)

        self.SettingsScroll.setWidget(self.SettingsScrollContents)

        self.SettingsOuter.addWidget(self.SettingsScroll)


        self.retranslateUi(SettingsComponent)

        QMetaObject.connectSlotsByName(SettingsComponent)
    # setupUi

    def retranslateUi(self, SettingsComponent):
        self.settingsKicker.setProperty(u"role", QCoreApplication.translate("SettingsComponent", u"kicker", None))
        self.settingsKicker.setText(QCoreApplication.translate("SettingsComponent", u"PREFERENCES", None))
        self.settingsTitle.setProperty(u"role", QCoreApplication.translate("SettingsComponent", u"h1", None))
        self.settingsTitle.setText(QCoreApplication.translate("SettingsComponent", u"Settings", None))
        self.settingsSub.setProperty(u"role", QCoreApplication.translate("SettingsComponent", u"muted", None))
        self.settingsSub.setText(QCoreApplication.translate("SettingsComponent", u"Tune the deck to your watch.", None))
        self.appearanceCard.setProperty(u"role", QCoreApplication.translate("SettingsComponent", u"card", None))
        self.appearanceTitle.setProperty(u"role", QCoreApplication.translate("SettingsComponent", u"h2", None))
        self.appearanceTitle.setText(QCoreApplication.translate("SettingsComponent", u"Appearance", None))
        self.appearanceSub.setProperty(u"role", QCoreApplication.translate("SettingsComponent", u"muted", None))
        self.appearanceSub.setText(QCoreApplication.translate("SettingsComponent", u"Theme and accent", None))
        self.themeToggle.setText(QCoreApplication.translate("SettingsComponent", u"Toggle", None))
        self.notifCard.setProperty(u"role", QCoreApplication.translate("SettingsComponent", u"card", None))
        self.notifTitle.setProperty(u"role", QCoreApplication.translate("SettingsComponent", u"h2", None))
        self.notifTitle.setText(QCoreApplication.translate("SettingsComponent", u"Notifications", None))
        self.notifStormLbl.setProperty(u"role", QCoreApplication.translate("SettingsComponent", u"muted", None))
        self.notifStormLbl.setText(QCoreApplication.translate("SettingsComponent", u"Storm alerts (Kp \u2265 6)", None))
        self.notifOfflineLbl.setProperty(u"role", QCoreApplication.translate("SettingsComponent", u"muted", None))
        self.notifOfflineLbl.setText(QCoreApplication.translate("SettingsComponent", u"Station offline", None))
        self.notifClearLbl.setProperty(u"role", QCoreApplication.translate("SettingsComponent", u"muted", None))
        self.notifClearLbl.setText(QCoreApplication.translate("SettingsComponent", u"Clear-sky windows", None))
        self.saveBtn.setText(QCoreApplication.translate("SettingsComponent", u"Save preferences", None))
        self.saveBtn.setProperty(u"variant", QCoreApplication.translate("SettingsComponent", u"primary", None))
        pass
    # retranslateUi

