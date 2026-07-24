# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'new_LightingCard.ui'
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
class Ui_LightingCard(object):
    def setupUi(self, LightingCard):
        if not LightingCard.objectName():
            LightingCard.setObjectName(u"LightingCard")
        LightingCard.resize(280, 300)
        self.lightRoot = QVBoxLayout(LightingCard)
        self.lightRoot.setSpacing(0)
        self.lightRoot.setObjectName(u"lightRoot")
        self.lightRoot.setContentsMargins(0, 0, 0, 0)
        self.lightingCard = QFrame(LightingCard)
        self.lightingCard.setObjectName(u"lightingCard")
        self.lightingCard.setFrameShape(QFrame.StyledPanel)
        self.lightLayout = QVBoxLayout(self.lightingCard)
        self.lightLayout.setSpacing(12)
        self.lightLayout.setObjectName(u"lightLayout")
        self.lightLayout.setContentsMargins(28, 26, 28, 26)
        self.lightHeader = QHBoxLayout()
        self.lightHeader.setObjectName(u"lightHeader")
        self.lightingTitle = QLabel(self.lightingCard)
        self.lightingTitle.setObjectName(u"lightingTitle")

        self.lightHeader.addWidget(self.lightingTitle)

        self.lightHeaderSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.lightHeader.addItem(self.lightHeaderSpacer)

        self.lightingMenu = QPushButton(self.lightingCard)
        self.lightingMenu.setObjectName(u"lightingMenu")
        self.lightingMenu.setMinimumSize(QSize(30, 26))
        self.lightingMenu.setMaximumSize(QSize(30, 26))

        self.lightHeader.addWidget(self.lightingMenu)


        self.lightLayout.addLayout(self.lightHeader)

        self.bulbIcon = QLabel(self.lightingCard)
        self.bulbIcon.setObjectName(u"bulbIcon")
        self.bulbIcon.setMinimumSize(QSize(96, 96))
        self.bulbIcon.setMaximumSize(QSize(96, 96))

        self.lightLayout.addWidget(self.bulbIcon, 0, Qt.AlignHCenter)

        self.lightMid = QSpacerItem(10, 12, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.lightLayout.addItem(self.lightMid)

        self.sliderRow = QHBoxLayout()
        self.sliderRow.setSpacing(10)
        self.sliderRow.setObjectName(u"sliderRow")
        self.sunLow = QLabel(self.lightingCard)
        self.sunLow.setObjectName(u"sunLow")
        self.sunLow.setMinimumSize(QSize(16, 16))
        self.sunLow.setMaximumSize(QSize(16, 16))

        self.sliderRow.addWidget(self.sunLow)

        self.brightness = QSlider(self.lightingCard)
        self.brightness.setObjectName(u"brightness")
        self.brightness.setOrientation(Qt.Horizontal)
        self.brightness.setMinimum(0)
        self.brightness.setMaximum(100)
        self.brightness.setValue(62)

        self.sliderRow.addWidget(self.brightness)

        self.sunHigh = QLabel(self.lightingCard)
        self.sunHigh.setObjectName(u"sunHigh")
        self.sunHigh.setMinimumSize(QSize(20, 20))
        self.sunHigh.setMaximumSize(QSize(20, 20))

        self.sliderRow.addWidget(self.sunHigh)


        self.lightLayout.addLayout(self.sliderRow)

        self.roomRow = QHBoxLayout()
        self.roomRow.setObjectName(u"roomRow")
        self.prevRoom = QPushButton(self.lightingCard)
        self.prevRoom.setObjectName(u"prevRoom")
        self.prevRoom.setMinimumSize(QSize(34, 34))
        self.prevRoom.setMaximumSize(QSize(34, 34))

        self.roomRow.addWidget(self.prevRoom)

        self.roomLabel = QLabel(self.lightingCard)
        self.roomLabel.setObjectName(u"roomLabel")
        self.roomLabel.setAlignment(Qt.AlignCenter)

        self.roomRow.addWidget(self.roomLabel)

        self.nextRoom = QPushButton(self.lightingCard)
        self.nextRoom.setObjectName(u"nextRoom")
        self.nextRoom.setMinimumSize(QSize(34, 34))
        self.nextRoom.setMaximumSize(QSize(34, 34))

        self.roomRow.addWidget(self.nextRoom)


        self.lightLayout.addLayout(self.roomRow)


        self.lightRoot.addWidget(self.lightingCard)


        self.retranslateUi(LightingCard)

        QMetaObject.connectSlotsByName(LightingCard)
    # setupUi

    def retranslateUi(self, LightingCard):
        self.lightingCard.setProperty(u"role", QCoreApplication.translate("LightingCard", u"card", None))
        self.lightingTitle.setText(QCoreApplication.translate("LightingCard", u"Lighting", None))
        self.lightingTitle.setProperty(u"role", QCoreApplication.translate("LightingCard", u"cardTitle", None))
        self.lightingMenu.setText("")
        self.lightingMenu.setProperty(u"role", QCoreApplication.translate("LightingCard", u"menuBtn", None))
        self.bulbIcon.setText("")
        self.sunLow.setText("")
        self.sunHigh.setText("")
        self.prevRoom.setText("")
        self.prevRoom.setProperty(u"role", QCoreApplication.translate("LightingCard", u"stepBtn", None))
        self.roomLabel.setText(QCoreApplication.translate("LightingCard", u"Studio", None))
        self.roomLabel.setProperty(u"role", QCoreApplication.translate("LightingCard", u"stepLabel", None))
        self.nextRoom.setText("")
        self.nextRoom.setProperty(u"role", QCoreApplication.translate("LightingCard", u"stepBtn", None))
        pass
    # retranslateUi

