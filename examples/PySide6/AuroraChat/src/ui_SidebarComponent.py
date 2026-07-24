# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'new_SidebarComponent.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QPushButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

from Custom_Widgets.QCustomAvatar import QCustomAvatar
from Custom_Widgets.QCustomComponent import QCustomComponent
from Custom_Widgets.QCustomComponentContainer import QCustomComponentContainer
from Custom_Widgets.QCustomSidebar import QCustomSidebar
from Custom_Widgets.QCustomSidebarButton import QCustomSidebarButton
class Ui_SidebarComponent(object):
    def setupUi(self, SidebarComponent):
        if not SidebarComponent.objectName():
            SidebarComponent.setObjectName(u"SidebarComponent")
        SidebarComponent.resize(212, 860)
        SidebarComponent.setMinimumSize(QSize(212, 0))
        SidebarComponent.setMaximumSize(QSize(212, 16777215))
        self.sidebarComponentOuter = QVBoxLayout(SidebarComponent)
        self.sidebarComponentOuter.setSpacing(0)
        self.sidebarComponentOuter.setObjectName(u"sidebarComponentOuter")
        self.sidebarComponentOuter.setContentsMargins(0, 0, 0, 0)
        self.sidebar = QCustomSidebar(SidebarComponent)
        self.sidebar.setObjectName(u"sidebar")
        self.sidebar.setProperty(u"collapsedWidth", 84)
        self.sidebar.setProperty(u"expandedWidth", 212)
        self.sidebar.setProperty(u"defaultWidth", 212)
        self.sidebar.setProperty(u"animationDuration", 300)
        self.sidebarLayout = QVBoxLayout(self.sidebar)
        self.sidebarLayout.setSpacing(6)
        self.sidebarLayout.setObjectName(u"sidebarLayout")
        self.sidebarLayout.setContentsMargins(18, 22, 18, 22)
        self.logoRow = QHBoxLayout()
        self.logoRow.setSpacing(10)
        self.logoRow.setObjectName(u"logoRow")
        self.brandLogo = QCustomAvatar(self.sidebar)
        self.brandLogo.setObjectName(u"brandLogo")
        self.brandLogo.setMinimumSize(QSize(44, 44))
        self.brandLogo.setMaximumSize(QSize(44, 44))
        self.brandLogo.setProperty(u"showStatus", False)

        self.logoRow.addWidget(self.brandLogo)

        self.brandName = QLabel(self.sidebar)
        self.brandName.setObjectName(u"brandName")

        self.logoRow.addWidget(self.brandName)

        self.logoSpacer = QSpacerItem(8, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.logoRow.addItem(self.logoSpacer)


        self.sidebarLayout.addLayout(self.logoRow)

        self.navTopSpacer = QSpacerItem(10, 26, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.sidebarLayout.addItem(self.navTopSpacer)

        self.navChat = QCustomSidebarButton(self.sidebar)
        self.navChat.setObjectName(u"navChat")
        self.navChat.setMinimumSize(QSize(0, 48))
        self.navChat.setCheckable(True)
        self.navChat.setAutoExclusive(True)
        self.navChat.setChecked(True)
        self.navChat.setIconSize(QSize(22, 22))
        self.navChat.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.sidebarLayout.addWidget(self.navChat)

        self.navPeople = QCustomSidebarButton(self.sidebar)
        self.navPeople.setObjectName(u"navPeople")
        self.navPeople.setMinimumSize(QSize(0, 48))
        self.navPeople.setCheckable(True)
        self.navPeople.setAutoExclusive(True)
        self.navPeople.setIconSize(QSize(22, 22))
        self.navPeople.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.sidebarLayout.addWidget(self.navPeople)

        self.navShop = QCustomSidebarButton(self.sidebar)
        self.navShop.setObjectName(u"navShop")
        self.navShop.setMinimumSize(QSize(0, 48))
        self.navShop.setCheckable(True)
        self.navShop.setAutoExclusive(True)
        self.navShop.setIconSize(QSize(22, 22))
        self.navShop.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.sidebarLayout.addWidget(self.navShop)

        self.navRequests = QCustomSidebarButton(self.sidebar)
        self.navRequests.setObjectName(u"navRequests")
        self.navRequests.setMinimumSize(QSize(0, 48))
        self.navRequests.setCheckable(True)
        self.navRequests.setAutoExclusive(True)
        self.navRequests.setIconSize(QSize(22, 22))
        self.navRequests.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.sidebarLayout.addWidget(self.navRequests)

        self.navArchive = QCustomSidebarButton(self.sidebar)
        self.navArchive.setObjectName(u"navArchive")
        self.navArchive.setMinimumSize(QSize(0, 48))
        self.navArchive.setCheckable(True)
        self.navArchive.setAutoExclusive(True)
        self.navArchive.setIconSize(QSize(22, 22))
        self.navArchive.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.sidebarLayout.addWidget(self.navArchive)

        self.sidebarSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.sidebarLayout.addItem(self.sidebarSpacer)

        self.themeToggle = QCustomSidebarButton(self.sidebar)
        self.themeToggle.setObjectName(u"themeToggle")
        self.themeToggle.setMinimumSize(QSize(0, 46))
        self.themeToggle.setIconSize(QSize(20, 20))
        self.themeToggle.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.sidebarLayout.addWidget(self.themeToggle)

        self.userCardContainer = QCustomComponentContainer(self.sidebar)
        self.userCardContainer.setObjectName(u"userCardContainer")
        self.userCardContainer.setProperty(u"previewComponent", False)

        self.sidebarLayout.addWidget(self.userCardContainer)


        self.sidebarComponentOuter.addWidget(self.sidebar)


        self.retranslateUi(SidebarComponent)

        QMetaObject.connectSlotsByName(SidebarComponent)
    # setupUi

    def retranslateUi(self, SidebarComponent):
        self.brandLogo.setProperty(u"text", QCoreApplication.translate("SidebarComponent", u"A", None))
        self.brandName.setText(QCoreApplication.translate("SidebarComponent", u"Aurora", None))
        self.brandName.setProperty(u"role", QCoreApplication.translate("SidebarComponent", u"brandName", None))
        self.navChat.setProperty(u"labelText", QCoreApplication.translate("SidebarComponent", u"Chat", None))
        self.navPeople.setProperty(u"labelText", QCoreApplication.translate("SidebarComponent", u"People", None))
        self.navShop.setProperty(u"labelText", QCoreApplication.translate("SidebarComponent", u"Shop", None))
        self.navRequests.setProperty(u"labelText", QCoreApplication.translate("SidebarComponent", u"Requests", None))
        self.navArchive.setProperty(u"labelText", QCoreApplication.translate("SidebarComponent", u"Archive", None))
        self.themeToggle.setProperty(u"labelText", QCoreApplication.translate("SidebarComponent", u"Dark mode", None))
        self.userCardContainer.setProperty(u"filePath", QCoreApplication.translate("SidebarComponent", u"ui/UserCardComponent.ui", None))
        pass
    # retranslateUi

