# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'new_TopBar.ui'
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
    QLineEdit, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

from Custom_Widgets.QCustomAvatar import QCustomAvatar
from Custom_Widgets.QCustomQLabel import QCustomQLabel
from Custom_Widgets.QCustomQPushButton import QCustomQPushButton
class Ui_TopBar(object):
    def setupUi(self, topBarRoot):
        if not topBarRoot.objectName():
            topBarRoot.setObjectName(u"topBarRoot")
        topBarRoot.resize(960, 84)
        self.topBarLayout = QHBoxLayout(topBarRoot)
        self.topBarLayout.setSpacing(14)
        self.topBarLayout.setObjectName(u"topBarLayout")
        self.topBarLayout.setContentsMargins(24, 16, 24, 12)
        self.searchFrame = QFrame(topBarRoot)
        self.searchFrame.setObjectName(u"searchFrame")
        self.searchFrame.setMinimumSize(QSize(360, 48))
        self.searchFrame.setMaximumSize(QSize(470, 48))
        self.searchFrame.setFrameShape(QFrame.StyledPanel)
        self.searchLayout = QHBoxLayout(self.searchFrame)
        self.searchLayout.setSpacing(10)
        self.searchLayout.setObjectName(u"searchLayout")
        self.searchLayout.setContentsMargins(18, 0, 16, 0)
        self.searchEdit = QLineEdit(self.searchFrame)
        self.searchEdit.setObjectName(u"searchEdit")
        self.searchEdit.setFrame(False)

        self.searchLayout.addWidget(self.searchEdit)

        self.searchIcon = QCustomQLabel(self.searchFrame)
        self.searchIcon.setObjectName(u"searchIcon")
        self.searchIcon.setMinimumSize(QSize(18, 18))
        self.searchIcon.setMaximumSize(QSize(18, 18))

        self.searchLayout.addWidget(self.searchIcon)


        self.topBarLayout.addWidget(self.searchFrame)

        self.topSpacer = QSpacerItem(40, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.topBarLayout.addItem(self.topSpacer)

        self.userAvatar = QCustomAvatar(topBarRoot)
        self.userAvatar.setObjectName(u"userAvatar")
        self.userAvatar.setMinimumSize(QSize(44, 44))
        self.userAvatar.setMaximumSize(QSize(44, 44))
        self.userAvatar.setProperty(u"showStatus", False)

        self.topBarLayout.addWidget(self.userAvatar)

        self.userTextLayout = QVBoxLayout()
        self.userTextLayout.setSpacing(2)
        self.userTextLayout.setObjectName(u"userTextLayout")
        self.userName = QLabel(topBarRoot)
        self.userName.setObjectName(u"userName")

        self.userTextLayout.addWidget(self.userName)

        self.planBadge = QLabel(topBarRoot)
        self.planBadge.setObjectName(u"planBadge")
        self.planBadge.setMinimumSize(QSize(0, 18))
        self.planBadge.setMaximumSize(QSize(72, 18))
        self.planBadge.setAlignment(Qt.AlignCenter)

        self.userTextLayout.addWidget(self.planBadge)


        self.topBarLayout.addLayout(self.userTextLayout)

        self.heartBtn = QCustomQPushButton(topBarRoot)
        self.heartBtn.setObjectName(u"heartBtn")
        self.heartBtn.setMinimumSize(QSize(44, 44))
        self.heartBtn.setMaximumSize(QSize(44, 44))
        self.heartBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.heartBtn.setIconSize(QSize(19, 19))

        self.topBarLayout.addWidget(self.heartBtn)

        self.settingsBtn = QCustomQPushButton(topBarRoot)
        self.settingsBtn.setObjectName(u"settingsBtn")
        self.settingsBtn.setMinimumSize(QSize(44, 44))
        self.settingsBtn.setMaximumSize(QSize(44, 44))
        self.settingsBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.settingsBtn.setIconSize(QSize(19, 19))

        self.topBarLayout.addWidget(self.settingsBtn)


        self.retranslateUi(topBarRoot)

        QMetaObject.connectSlotsByName(topBarRoot)
    # setupUi

    def retranslateUi(self, topBarRoot):
        self.searchEdit.setPlaceholderText(QCoreApplication.translate("TopBar", u"Search for a song", None))
        self.searchIcon.setProperty(u"iconName", QCoreApplication.translate("TopBar", u"search", None))
        self.searchIcon.setText("")
        self.userAvatar.setProperty(u"text", QCoreApplication.translate("TopBar", u"MH", None))
        self.userName.setText(QCoreApplication.translate("TopBar", u"Molly Hunter", None))
        self.planBadge.setText(QCoreApplication.translate("TopBar", u"Premium", None))
        self.heartBtn.setText("")
        self.heartBtn.setProperty(u"iconName", QCoreApplication.translate("TopBar", u"heart", None))
        self.settingsBtn.setText("")
        self.settingsBtn.setProperty(u"iconName", QCoreApplication.translate("TopBar", u"settings", None))
        pass
    # retranslateUi

