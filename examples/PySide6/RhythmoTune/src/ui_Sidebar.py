# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'new_Sidebar.ui'
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

from Custom_Widgets.QCustomQLabel import QCustomQLabel
from Custom_Widgets.QCustomQPushButton import QCustomQPushButton
class Ui_Sidebar(object):
    def setupUi(self, sidebarRoot):
        if not sidebarRoot.objectName():
            sidebarRoot.setObjectName(u"sidebarRoot")
        sidebarRoot.resize(244, 720)
        self.sidebarLayout = QVBoxLayout(sidebarRoot)
        self.sidebarLayout.setSpacing(8)
        self.sidebarLayout.setObjectName(u"sidebarLayout")
        self.sidebarLayout.setContentsMargins(20, 26, 18, 22)
        self.logoLayout = QHBoxLayout()
        self.logoLayout.setSpacing(10)
        self.logoLayout.setObjectName(u"logoLayout")
        self.logoIcon = QCustomQLabel(sidebarRoot)
        self.logoIcon.setObjectName(u"logoIcon")
        self.logoIcon.setMinimumSize(QSize(28, 28))
        self.logoIcon.setMaximumSize(QSize(28, 28))

        self.logoLayout.addWidget(self.logoIcon)

        self.logoText = QLabel(sidebarRoot)
        self.logoText.setObjectName(u"logoText")

        self.logoLayout.addWidget(self.logoText)

        self.logoSpacer = QSpacerItem(10, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.logoLayout.addItem(self.logoSpacer)


        self.sidebarLayout.addLayout(self.logoLayout)

        self.afterLogo = QSpacerItem(10, 22, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.sidebarLayout.addItem(self.afterLogo)

        self.navHome = QCustomQPushButton(sidebarRoot)
        self.navHome.setObjectName(u"navHome")
        self.navHome.setMinimumSize(QSize(0, 46))
        self.navHome.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.navHome.setCheckable(True)
        self.navHome.setChecked(True)
        self.navHome.setIconSize(QSize(20, 20))

        self.sidebarLayout.addWidget(self.navHome)

        self.navCategories = QCustomQPushButton(sidebarRoot)
        self.navCategories.setObjectName(u"navCategories")
        self.navCategories.setMinimumSize(QSize(0, 46))
        self.navCategories.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.navCategories.setCheckable(True)
        self.navCategories.setIconSize(QSize(20, 20))

        self.sidebarLayout.addWidget(self.navCategories)

        self.navArtists = QCustomQPushButton(sidebarRoot)
        self.navArtists.setObjectName(u"navArtists")
        self.navArtists.setMinimumSize(QSize(0, 46))
        self.navArtists.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.navArtists.setCheckable(True)
        self.navArtists.setIconSize(QSize(20, 20))

        self.sidebarLayout.addWidget(self.navArtists)

        self.beforePlaylists = QSpacerItem(10, 14, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.sidebarLayout.addItem(self.beforePlaylists)

        self.playlistsHeader = QHBoxLayout()
        self.playlistsHeader.setObjectName(u"playlistsHeader")
        self.playlistsHeader.setContentsMargins(10, -1, -1, -1)
        self.playlistsIcon = QCustomQLabel(sidebarRoot)
        self.playlistsIcon.setObjectName(u"playlistsIcon")
        self.playlistsIcon.setMinimumSize(QSize(16, 16))
        self.playlistsIcon.setMaximumSize(QSize(16, 16))

        self.playlistsHeader.addWidget(self.playlistsIcon)

        self.playlistsTitle = QLabel(sidebarRoot)
        self.playlistsTitle.setObjectName(u"playlistsTitle")

        self.playlistsHeader.addWidget(self.playlistsTitle)

        self.plHeaderSpacer = QSpacerItem(10, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.playlistsHeader.addItem(self.plHeaderSpacer)

        self.playlistsChevron = QCustomQLabel(sidebarRoot)
        self.playlistsChevron.setObjectName(u"playlistsChevron")
        self.playlistsChevron.setMinimumSize(QSize(16, 16))
        self.playlistsChevron.setMaximumSize(QSize(16, 16))

        self.playlistsHeader.addWidget(self.playlistsChevron)


        self.sidebarLayout.addLayout(self.playlistsHeader)

        self.playlistsBox = QWidget(sidebarRoot)
        self.playlistsBox.setObjectName(u"playlistsBox")
        self.playlistsBoxLayout = QVBoxLayout(self.playlistsBox)
        self.playlistsBoxLayout.setSpacing(4)
        self.playlistsBoxLayout.setObjectName(u"playlistsBoxLayout")
        self.playlistsBoxLayout.setContentsMargins(4, 6, 0, 0)

        self.sidebarLayout.addWidget(self.playlistsBox)

        self.sidebarStretch = QSpacerItem(10, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.sidebarLayout.addItem(self.sidebarStretch)

        self.navLogout = QCustomQPushButton(sidebarRoot)
        self.navLogout.setObjectName(u"navLogout")
        self.navLogout.setMinimumSize(QSize(0, 44))
        self.navLogout.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.navLogout.setIconSize(QSize(19, 19))

        self.sidebarLayout.addWidget(self.navLogout)


        self.retranslateUi(sidebarRoot)

        QMetaObject.connectSlotsByName(sidebarRoot)
    # setupUi

    def retranslateUi(self, sidebarRoot):
        self.logoIcon.setProperty(u"iconName", QCoreApplication.translate("Sidebar", u"activity", None))
        self.logoIcon.setText("")
        self.logoText.setText(QCoreApplication.translate("Sidebar", u"RhythmoTune", None))
        self.navHome.setText(QCoreApplication.translate("Sidebar", u"Home", None))
        self.navHome.setProperty(u"iconName", QCoreApplication.translate("Sidebar", u"home", None))
        self.navCategories.setText(QCoreApplication.translate("Sidebar", u"Categories", None))
        self.navCategories.setProperty(u"iconName", QCoreApplication.translate("Sidebar", u"grid", None))
        self.navArtists.setText(QCoreApplication.translate("Sidebar", u"Artists", None))
        self.navArtists.setProperty(u"iconName", QCoreApplication.translate("Sidebar", u"user", None))
        self.playlistsIcon.setProperty(u"iconName", QCoreApplication.translate("Sidebar", u"music", None))
        self.playlistsIcon.setText("")
        self.playlistsTitle.setText(QCoreApplication.translate("Sidebar", u"Playlists", None))
        self.playlistsChevron.setProperty(u"iconName", QCoreApplication.translate("Sidebar", u"chevron-up", None))
        self.playlistsChevron.setText("")
        self.navLogout.setText(QCoreApplication.translate("Sidebar", u"Logout", None))
        self.navLogout.setProperty(u"iconName", QCoreApplication.translate("Sidebar", u"log-out", None))
        pass
    # retranslateUi

