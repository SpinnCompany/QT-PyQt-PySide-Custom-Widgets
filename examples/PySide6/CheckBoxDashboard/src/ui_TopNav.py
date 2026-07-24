# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'new_TopNav.ui'
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
class Ui_TopNav(object):
    def setupUi(self, TopNav):
        if not TopNav.objectName():
            TopNav.setObjectName(u"TopNav")
        TopNav.resize(1180, 60)
        self.topNavLayout = QHBoxLayout(TopNav)
        self.topNavLayout.setSpacing(12)
        self.topNavLayout.setObjectName(u"topNavLayout")
        self.topNavLayout.setContentsMargins(0, 0, 0, 0)
        self.logo = QLabel(TopNav)
        self.logo.setObjectName(u"logo")
        self.logo.setMinimumSize(QSize(46, 46))
        self.logo.setMaximumSize(QSize(46, 46))
        self.logo.setAlignment(Qt.AlignCenter)

        self.topNavLayout.addWidget(self.logo)

        self.navBtn0 = QPushButton(TopNav)
        self.navBtn0.setObjectName(u"navBtn0")
        self.navBtn0.setMinimumSize(QSize(0, 46))
        self.navBtn0.setCheckable(True)
        self.navBtn0.setChecked(True)

        self.topNavLayout.addWidget(self.navBtn0)

        self.navBtn1 = QPushButton(TopNav)
        self.navBtn1.setObjectName(u"navBtn1")
        self.navBtn1.setMinimumSize(QSize(0, 46))
        self.navBtn1.setCheckable(True)

        self.topNavLayout.addWidget(self.navBtn1)

        self.navBtn2 = QPushButton(TopNav)
        self.navBtn2.setObjectName(u"navBtn2")
        self.navBtn2.setMinimumSize(QSize(0, 46))
        self.navBtn2.setCheckable(True)

        self.topNavLayout.addWidget(self.navBtn2)

        self.searchBtn = QPushButton(TopNav)
        self.searchBtn.setObjectName(u"searchBtn")
        self.searchBtn.setMinimumSize(QSize(46, 46))
        self.searchBtn.setMaximumSize(QSize(46, 46))

        self.topNavLayout.addWidget(self.searchBtn)

        self.topSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.topNavLayout.addItem(self.topSpacer)

        self.profileTextLayout = QVBoxLayout()
        self.profileTextLayout.setSpacing(0)
        self.profileTextLayout.setObjectName(u"profileTextLayout")
        self.profileName = QLabel(TopNav)
        self.profileName.setObjectName(u"profileName")
        self.profileName.setAlignment(Qt.AlignRight|Qt.AlignVCenter)

        self.profileTextLayout.addWidget(self.profileName)

        self.profileHandle = QLabel(TopNav)
        self.profileHandle.setObjectName(u"profileHandle")
        self.profileHandle.setAlignment(Qt.AlignRight|Qt.AlignVCenter)

        self.profileTextLayout.addWidget(self.profileHandle)


        self.topNavLayout.addLayout(self.profileTextLayout)

        self.avatar = QLabel(TopNav)
        self.avatar.setObjectName(u"avatar")
        self.avatar.setMinimumSize(QSize(46, 46))
        self.avatar.setMaximumSize(QSize(46, 46))
        self.avatar.setAlignment(Qt.AlignCenter)

        self.topNavLayout.addWidget(self.avatar)


        self.retranslateUi(TopNav)

        QMetaObject.connectSlotsByName(TopNav)
    # setupUi

    def retranslateUi(self, TopNav):
        self.logo.setText(QCoreApplication.translate("TopNav", u"N", None))
        self.navBtn0.setText(QCoreApplication.translate("TopNav", u"Check Box", None))
        self.navBtn0.setProperty(u"role", QCoreApplication.translate("TopNav", u"navPill", None))
        self.navBtn1.setText(QCoreApplication.translate("TopNav", u"Monitoring", None))
        self.navBtn1.setProperty(u"role", QCoreApplication.translate("TopNav", u"navPill", None))
        self.navBtn2.setText(QCoreApplication.translate("TopNav", u"Support", None))
        self.navBtn2.setProperty(u"role", QCoreApplication.translate("TopNav", u"navPill", None))
        self.searchBtn.setText("")
        self.searchBtn.setProperty(u"role", QCoreApplication.translate("TopNav", u"iconPill", None))
        self.profileName.setText(QCoreApplication.translate("TopNav", u"Bogdan Nikitin", None))
        self.profileName.setProperty(u"role", QCoreApplication.translate("TopNav", u"profileName", None))
        self.profileHandle.setText(QCoreApplication.translate("TopNav", u"@Nixtio", None))
        self.profileHandle.setProperty(u"role", QCoreApplication.translate("TopNav", u"profileHandle", None))
        self.avatar.setText("")
        pass
    # retranslateUi

