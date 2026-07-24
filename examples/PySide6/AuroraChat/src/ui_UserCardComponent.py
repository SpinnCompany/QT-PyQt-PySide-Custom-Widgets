# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'new_UserCardComponent.ui'
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

from Custom_Widgets.QCustomAvatar import QCustomAvatar
from Custom_Widgets.QCustomComponent import QCustomComponent
class Ui_UserCardComponent(object):
    def setupUi(self, UserCardComponent):
        if not UserCardComponent.objectName():
            UserCardComponent.setObjectName(u"UserCardComponent")
        UserCardComponent.resize(176, 52)
        self.userCardOuter = QVBoxLayout(UserCardComponent)
        self.userCardOuter.setSpacing(0)
        self.userCardOuter.setObjectName(u"userCardOuter")
        self.userCardOuter.setContentsMargins(0, 0, 0, 0)
        self.userCard = QFrame(UserCardComponent)
        self.userCard.setObjectName(u"userCard")
        self.userCard.setMinimumSize(QSize(0, 52))
        self.userCard.setFrameShape(QFrame.StyledPanel)
        self.userRow = QHBoxLayout(self.userCard)
        self.userRow.setSpacing(10)
        self.userRow.setObjectName(u"userRow")
        self.userRow.setContentsMargins(6, 4, 8, 4)
        self.sidebarAvatar = QCustomAvatar(self.userCard)
        self.sidebarAvatar.setObjectName(u"sidebarAvatar")
        self.sidebarAvatar.setMinimumSize(QSize(38, 38))
        self.sidebarAvatar.setMaximumSize(QSize(38, 38))

        self.userRow.addWidget(self.sidebarAvatar)

        self.userName = QLabel(self.userCard)
        self.userName.setObjectName(u"userName")

        self.userRow.addWidget(self.userName)

        self.userSpacer = QSpacerItem(8, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.userRow.addItem(self.userSpacer)

        self.logoutBtn = QPushButton(self.userCard)
        self.logoutBtn.setObjectName(u"logoutBtn")
        self.logoutBtn.setMinimumSize(QSize(28, 28))
        self.logoutBtn.setMaximumSize(QSize(28, 28))
        self.logoutBtn.setIconSize(QSize(18, 18))
        self.logoutBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.userRow.addWidget(self.logoutBtn)


        self.userCardOuter.addWidget(self.userCard)


        self.retranslateUi(UserCardComponent)

        QMetaObject.connectSlotsByName(UserCardComponent)
    # setupUi

    def retranslateUi(self, UserCardComponent):
        self.sidebarAvatar.setProperty(u"text", QCoreApplication.translate("UserCardComponent", u"V", None))
        self.userName.setText(QCoreApplication.translate("UserCardComponent", u"Vivien", None))
        self.userName.setProperty(u"role", QCoreApplication.translate("UserCardComponent", u"userName", None))
        pass
    # retranslateUi

