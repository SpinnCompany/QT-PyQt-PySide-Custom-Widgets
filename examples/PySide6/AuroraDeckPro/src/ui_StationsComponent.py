# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'new_StationsComponent.ui'
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

from Custom_Widgets.QCustomComboBox import QCustomComboBox
from Custom_Widgets.QCustomComponent import QCustomComponent
from Custom_Widgets.QCustomDataTable import QCustomDataTable
from Custom_Widgets.QCustomNumberInput import QCustomNumberInput
from Custom_Widgets.QCustomRangeSlider import QCustomRangeSlider
from Custom_Widgets.QCustomSwitch import QCustomSwitch
class Ui_StationsComponent(object):
    def setupUi(self, StationsComponent):
        if not StationsComponent.objectName():
            StationsComponent.setObjectName(u"StationsComponent")
        StationsComponent.resize(940, 680)
        self.StationsOuter = QVBoxLayout(StationsComponent)
        self.StationsOuter.setSpacing(0)
        self.StationsOuter.setObjectName(u"StationsOuter")
        self.StationsOuter.setContentsMargins(0, 0, 0, 0)
        self.StationsScroll = QScrollArea(StationsComponent)
        self.StationsScroll.setObjectName(u"StationsScroll")
        self.StationsScroll.setWidgetResizable(True)
        self.StationsScroll.setFrameShape(QFrame.NoFrame)
        self.StationsScroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.StationsScrollContents = QWidget()
        self.StationsScrollContents.setObjectName(u"StationsScrollContents")
        self.StationsScrollContents.setGeometry(QRect(0, 0, 1200, 760))
        self.StationsCenterRow = QHBoxLayout(self.StationsScrollContents)
        self.StationsCenterRow.setSpacing(0)
        self.StationsCenterRow.setObjectName(u"StationsCenterRow")
        self.StationsCenterRow.setContentsMargins(28, 24, 28, 24)
        self.StationsLeftSp = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.StationsCenterRow.addItem(self.StationsLeftSp)

        self.StationsColumn = QWidget(self.StationsScrollContents)
        self.StationsColumn.setObjectName(u"StationsColumn")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(20)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.StationsColumn.sizePolicy().hasHeightForWidth())
        self.StationsColumn.setSizePolicy(sizePolicy)
        self.StationsColumn.setMaximumSize(QSize(1360, 16777215))
        self.StationsColLayout = QVBoxLayout(self.StationsColumn)
        self.StationsColLayout.setSpacing(14)
        self.StationsColLayout.setObjectName(u"StationsColLayout")
        self.StationsColLayout.setContentsMargins(0, 0, 0, 0)
        self.stationsHeader = QVBoxLayout()
        self.stationsHeader.setSpacing(2)
        self.stationsHeader.setObjectName(u"stationsHeader")
        self.stationsKicker = QLabel(self.StationsColumn)
        self.stationsKicker.setObjectName(u"stationsKicker")

        self.stationsHeader.addWidget(self.stationsKicker)

        self.stationsTitle = QLabel(self.StationsColumn)
        self.stationsTitle.setObjectName(u"stationsTitle")

        self.stationsHeader.addWidget(self.stationsTitle)

        self.stationsSub = QLabel(self.StationsColumn)
        self.stationsSub.setObjectName(u"stationsSub")

        self.stationsHeader.addWidget(self.stationsSub)


        self.StationsColLayout.addLayout(self.stationsHeader)

        self.stationsPanel = QFrame(self.StationsColumn)
        self.stationsPanel.setObjectName(u"stationsPanel")
        self.stationsPanel.setFrameShape(QFrame.StyledPanel)
        self.panelLayout = QVBoxLayout(self.stationsPanel)
        self.panelLayout.setSpacing(12)
        self.panelLayout.setObjectName(u"panelLayout")
        self.panelLayout.setContentsMargins(18, 16, 18, 16)
        self.toolbarRow = QHBoxLayout()
        self.toolbarRow.setSpacing(14)
        self.toolbarRow.setObjectName(u"toolbarRow")
        self.regionCombo = QCustomComboBox(self.stationsPanel)
        self.regionCombo.setObjectName(u"regionCombo")
        self.regionCombo.setMinimumSize(QSize(150, 0))
        self.regionCombo.setProperty(u"editable", False)

        self.toolbarRow.addWidget(self.regionCombo)

        self.minKpLabel = QLabel(self.stationsPanel)
        self.minKpLabel.setObjectName(u"minKpLabel")

        self.toolbarRow.addWidget(self.minKpLabel)

        self.minKp = QCustomNumberInput(self.stationsPanel)
        self.minKp.setObjectName(u"minKp")
        self.minKp.setProperty(u"minimum", 0.000000000000000)
        self.minKp.setProperty(u"maximum", 9.000000000000000)
        self.minKp.setProperty(u"singleStep", 1.000000000000000)
        self.minKp.setProperty(u"decimals", 0)

        self.toolbarRow.addWidget(self.minKp)

        self.liveOnlyLabel = QLabel(self.stationsPanel)
        self.liveOnlyLabel.setObjectName(u"liveOnlyLabel")

        self.toolbarRow.addWidget(self.liveOnlyLabel)

        self.liveOnly = QCustomSwitch(self.stationsPanel)
        self.liveOnly.setObjectName(u"liveOnly")
        self.liveOnly.setProperty(u"checked", False)

        self.toolbarRow.addWidget(self.liveOnly)

        self.toolbarSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.toolbarRow.addItem(self.toolbarSpacer)

        self.searchBox = QLineEdit(self.stationsPanel)
        self.searchBox.setObjectName(u"searchBox")
        self.searchBox.setMinimumSize(QSize(180, 0))
        self.searchBox.setMaximumSize(QSize(180, 16777215))

        self.toolbarRow.addWidget(self.searchBox)


        self.panelLayout.addLayout(self.toolbarRow)

        self.cloudRow = QHBoxLayout()
        self.cloudRow.setSpacing(10)
        self.cloudRow.setObjectName(u"cloudRow")
        self.cloudLabel = QLabel(self.stationsPanel)
        self.cloudLabel.setObjectName(u"cloudLabel")

        self.cloudRow.addWidget(self.cloudLabel)

        self.cloudRange = QCustomRangeSlider(self.stationsPanel)
        self.cloudRange.setObjectName(u"cloudRange")
        self.cloudRange.setProperty(u"minimum", 0)
        self.cloudRange.setProperty(u"maximum", 100)
        self.cloudRange.setProperty(u"lowerValue", 0)
        self.cloudRange.setProperty(u"upperValue", 100)

        self.cloudRow.addWidget(self.cloudRange)


        self.panelLayout.addLayout(self.cloudRow)

        self.stationsTable = QCustomDataTable(self.stationsPanel)
        self.stationsTable.setObjectName(u"stationsTable")
        self.stationsTable.setProperty(u"pageSize", 8)

        self.panelLayout.addWidget(self.stationsTable)

        self.stationsStatus = QLabel(self.stationsPanel)
        self.stationsStatus.setObjectName(u"stationsStatus")

        self.panelLayout.addWidget(self.stationsStatus)


        self.StationsColLayout.addWidget(self.stationsPanel)


        self.StationsCenterRow.addWidget(self.StationsColumn)

        self.StationsRightSp = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.StationsCenterRow.addItem(self.StationsRightSp)

        self.StationsScroll.setWidget(self.StationsScrollContents)

        self.StationsOuter.addWidget(self.StationsScroll)


        self.retranslateUi(StationsComponent)

        QMetaObject.connectSlotsByName(StationsComponent)
    # setupUi

    def retranslateUi(self, StationsComponent):
        self.stationsKicker.setProperty(u"role", QCoreApplication.translate("StationsComponent", u"kicker", None))
        self.stationsKicker.setText(QCoreApplication.translate("StationsComponent", u"NETWORK", None))
        self.stationsTitle.setProperty(u"role", QCoreApplication.translate("StationsComponent", u"h1", None))
        self.stationsTitle.setText(QCoreApplication.translate("StationsComponent", u"Ground Stations", None))
        self.stationsSub.setProperty(u"role", QCoreApplication.translate("StationsComponent", u"muted", None))
        self.stationsSub.setText(QCoreApplication.translate("StationsComponent", u"Filter the array by region, activity and sky.", None))
        self.stationsPanel.setProperty(u"role", QCoreApplication.translate("StationsComponent", u"panel", None))
        self.minKpLabel.setProperty(u"role", QCoreApplication.translate("StationsComponent", u"muted", None))
        self.minKpLabel.setText(QCoreApplication.translate("StationsComponent", u"Min Kp", None))
        self.liveOnlyLabel.setProperty(u"role", QCoreApplication.translate("StationsComponent", u"muted", None))
        self.liveOnlyLabel.setText(QCoreApplication.translate("StationsComponent", u"Live only", None))
        self.searchBox.setPlaceholderText(QCoreApplication.translate("StationsComponent", u"Search\u2026", None))
        self.cloudLabel.setProperty(u"role", QCoreApplication.translate("StationsComponent", u"muted", None))
        self.cloudLabel.setText(QCoreApplication.translate("StationsComponent", u"Cloud cover %", None))
        self.stationsTable.setProperty(u"selectionMode", QCoreApplication.translate("StationsComponent", u"SingleRow", None))
        self.stationsStatus.setProperty(u"role", QCoreApplication.translate("StationsComponent", u"muted", None))
        self.stationsStatus.setText("")
        pass
    # retranslateUi

