# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'new_SecurityCard.ui'
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
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

from Custom_Widgets.QCustomSwitch import QCustomSwitch
class Ui_SecurityCard(object):
    def setupUi(self, SecurityCard):
        if not SecurityCard.objectName():
            SecurityCard.setObjectName(u"SecurityCard")
        SecurityCard.resize(280, 300)
        self.secRoot = QVBoxLayout(SecurityCard)
        self.secRoot.setSpacing(0)
        self.secRoot.setObjectName(u"secRoot")
        self.secRoot.setContentsMargins(0, 0, 0, 0)
        self.securityCard = QFrame(SecurityCard)
        self.securityCard.setObjectName(u"securityCard")
        self.securityCard.setFrameShape(QFrame.StyledPanel)
        self.secLayout = QVBoxLayout(self.securityCard)
        self.secLayout.setSpacing(12)
        self.secLayout.setObjectName(u"secLayout")
        self.secLayout.setContentsMargins(28, 26, 28, 26)
        self.secHeader = QHBoxLayout()
        self.secHeader.setObjectName(u"secHeader")
        self.securityTitle = QLabel(self.securityCard)
        self.securityTitle.setObjectName(u"securityTitle")

        self.secHeader.addWidget(self.securityTitle)

        self.secHeaderSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.secHeader.addItem(self.secHeaderSpacer)

        self.securityMenu = QPushButton(self.securityCard)
        self.securityMenu.setObjectName(u"securityMenu")
        self.securityMenu.setMinimumSize(QSize(30, 26))
        self.securityMenu.setMaximumSize(QSize(30, 26))

        self.secHeader.addWidget(self.securityMenu)


        self.secLayout.addLayout(self.secHeader)

        self.shieldIcon = QLabel(self.securityCard)
        self.shieldIcon.setObjectName(u"shieldIcon")
        self.shieldIcon.setMinimumSize(QSize(96, 96))
        self.shieldIcon.setMaximumSize(QSize(96, 96))

        self.secLayout.addWidget(self.shieldIcon, 0, Qt.AlignHCenter)

        self.secMid = QSpacerItem(10, 12, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.secLayout.addItem(self.secMid)

        self.switchRow = QHBoxLayout()
        self.switchRow.setSpacing(10)
        self.switchRow.setObjectName(u"switchRow")
        self.swLeft = QSpacerItem(20, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.switchRow.addItem(self.swLeft)

        self.lockLabel = QLabel(self.securityCard)
        self.lockLabel.setObjectName(u"lockLabel")

        self.switchRow.addWidget(self.lockLabel)

        self.lockSwitch = QCustomSwitch(self.securityCard)
        self.lockSwitch.setObjectName(u"lockSwitch")

        self.switchRow.addWidget(self.lockSwitch)

        self.swRight = QSpacerItem(20, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.switchRow.addItem(self.swRight)


        self.secLayout.addLayout(self.switchRow)

        self.doorRow = QHBoxLayout()
        self.doorRow.setObjectName(u"doorRow")
        self.prevDoor = QPushButton(self.securityCard)
        self.prevDoor.setObjectName(u"prevDoor")
        self.prevDoor.setMinimumSize(QSize(34, 34))
        self.prevDoor.setMaximumSize(QSize(34, 34))

        self.doorRow.addWidget(self.prevDoor)

        self.doorLabel = QLabel(self.securityCard)
        self.doorLabel.setObjectName(u"doorLabel")
        self.doorLabel.setAlignment(Qt.AlignCenter)

        self.doorRow.addWidget(self.doorLabel)

        self.nextDoor = QPushButton(self.securityCard)
        self.nextDoor.setObjectName(u"nextDoor")
        self.nextDoor.setMinimumSize(QSize(34, 34))
        self.nextDoor.setMaximumSize(QSize(34, 34))

        self.doorRow.addWidget(self.nextDoor)


        self.secLayout.addLayout(self.doorRow)


        self.secRoot.addWidget(self.securityCard)


        self.retranslateUi(SecurityCard)

        QMetaObject.connectSlotsByName(SecurityCard)
    # setupUi

    def retranslateUi(self, SecurityCard):
        self.securityCard.setProperty(u"role", QCoreApplication.translate("SecurityCard", u"card", None))
        self.securityTitle.setText(QCoreApplication.translate("SecurityCard", u"Security", None))
        self.securityTitle.setProperty(u"role", QCoreApplication.translate("SecurityCard", u"cardTitle", None))
        self.securityMenu.setText("")
        self.securityMenu.setProperty(u"role", QCoreApplication.translate("SecurityCard", u"menuBtn", None))
        self.shieldIcon.setText("")
        self.lockLabel.setText(QCoreApplication.translate("SecurityCard", u"Locked", None))
        self.lockLabel.setProperty(u"role", QCoreApplication.translate("SecurityCard", u"lockLabel", None))
        self.prevDoor.setText("")
        self.prevDoor.setProperty(u"role", QCoreApplication.translate("SecurityCard", u"stepBtn", None))
        self.doorLabel.setText(QCoreApplication.translate("SecurityCard", u"Front Door", None))
        self.doorLabel.setProperty(u"role", QCoreApplication.translate("SecurityCard", u"stepLabel", None))
        self.nextDoor.setText("")
        self.nextDoor.setProperty(u"role", QCoreApplication.translate("SecurityCard", u"stepBtn", None))
        pass
    # retranslateUi

