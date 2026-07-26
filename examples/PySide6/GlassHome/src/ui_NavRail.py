# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'new_NavRail.ui'
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
from PySide6.QtWidgets import (QApplication, QLabel, QPushButton, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

from Custom_Widgets.QCustomAvatar import QCustomAvatar
from Custom_Widgets.QCustomGlassFrame import QCustomGlassFrame
from Custom_Widgets.QCustomQPushButton import QCustomQPushButton
from Custom_Widgets.QCustomThemeDarkLightToggle import QCustomThemeDarkLightToggle
class Ui_NavRail(object):
    def setupUi(self, NavRail):
        if not NavRail.objectName():
            NavRail.setObjectName(u"NavRail")
        NavRail.resize(84, 620)
        self.navRoot = QVBoxLayout(NavRail)
        self.navRoot.setSpacing(0)
        self.navRoot.setObjectName(u"navRoot")
        self.navRoot.setContentsMargins(0, 0, 0, 0)
        self.navTopStretch = QSpacerItem(10, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.navRoot.addItem(self.navTopStretch)

        self.navGlass = QCustomGlassFrame(NavRail)
        self.navGlass.setObjectName(u"navGlass")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.navGlass.sizePolicy().hasHeightForWidth())
        self.navGlass.setSizePolicy(sizePolicy)
        self.navGlass.setProperty(u"cornerRadius", 30)
        self.navLayout = QVBoxLayout(self.navGlass)
        self.navLayout.setSpacing(14)
        self.navLayout.setObjectName(u"navLayout")
        self.navLayout.setContentsMargins(14, 20, 14, 18)
        self.navDashboard = QCustomQPushButton(self.navGlass)
        self.navDashboard.setObjectName(u"navDashboard")
        self.navDashboard.setMinimumSize(QSize(46, 46))
        self.navDashboard.setMaximumSize(QSize(46, 46))
        self.navDashboard.setCheckable(True)
        self.navDashboard.setChecked(True)
        self.navDashboard.setAutoExclusive(True)
        self.navDashboard.setIconSize(QSize(21, 21))

        self.navLayout.addWidget(self.navDashboard, 0, Qt.AlignHCenter)

        self.navDevices = QCustomQPushButton(self.navGlass)
        self.navDevices.setObjectName(u"navDevices")
        self.navDevices.setMinimumSize(QSize(46, 46))
        self.navDevices.setMaximumSize(QSize(46, 46))
        self.navDevices.setCheckable(True)
        self.navDevices.setAutoExclusive(True)
        self.navDevices.setIconSize(QSize(21, 21))

        self.navLayout.addWidget(self.navDevices, 0, Qt.AlignHCenter)

        self.navStats = QCustomQPushButton(self.navGlass)
        self.navStats.setObjectName(u"navStats")
        self.navStats.setMinimumSize(QSize(46, 46))
        self.navStats.setMaximumSize(QSize(46, 46))
        self.navStats.setCheckable(True)
        self.navStats.setAutoExclusive(True)
        self.navStats.setIconSize(QSize(21, 21))

        self.navLayout.addWidget(self.navStats, 0, Qt.AlignHCenter)

        self.navAdd = QCustomQPushButton(self.navGlass)
        self.navAdd.setObjectName(u"navAdd")
        self.navAdd.setMinimumSize(QSize(46, 46))
        self.navAdd.setMaximumSize(QSize(46, 46))
        self.navAdd.setCheckable(True)
        self.navAdd.setAutoExclusive(True)
        self.navAdd.setIconSize(QSize(21, 21))

        self.navLayout.addWidget(self.navAdd, 0, Qt.AlignHCenter)

        self.navAutomation = QCustomQPushButton(self.navGlass)
        self.navAutomation.setObjectName(u"navAutomation")
        self.navAutomation.setMinimumSize(QSize(46, 46))
        self.navAutomation.setMaximumSize(QSize(46, 46))
        self.navAutomation.setCheckable(True)
        self.navAutomation.setAutoExclusive(True)
        self.navAutomation.setIconSize(QSize(21, 21))

        self.navLayout.addWidget(self.navAutomation, 0, Qt.AlignHCenter)

        self.navSpacer = QSpacerItem(20, 30, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.navLayout.addItem(self.navSpacer)

        self.navThemeToggle = QCustomThemeDarkLightToggle(self.navGlass)
        self.navThemeToggle.setObjectName(u"navThemeToggle")
        self.navThemeToggle.setMinimumSize(QSize(46, 46))
        self.navThemeToggle.setMaximumSize(QSize(46, 46))
        self.navThemeToggle.setProperty(u"updateLabelText", False)
        self.navThemeToggle.setProperty(u"updateButtonIcon", False)
        self.navThemeToggle.setIconSize(QSize(20, 20))

        self.navLayout.addWidget(self.navThemeToggle, 0, Qt.AlignHCenter)

        self.navAvatar = QCustomAvatar(self.navGlass)
        self.navAvatar.setObjectName(u"navAvatar")
        self.navAvatar.setMinimumSize(QSize(46, 46))
        self.navAvatar.setMaximumSize(QSize(46, 46))
        self.navAvatar.setProperty(u"showStatus", False)
        self.navAvatar.setProperty(u"ringWidth", 2)

        self.navLayout.addWidget(self.navAvatar, 0, Qt.AlignHCenter)


        self.navRoot.addWidget(self.navGlass)

        self.navBottomStretch = QSpacerItem(10, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.navRoot.addItem(self.navBottomStretch)


        self.retranslateUi(NavRail)

        QMetaObject.connectSlotsByName(NavRail)
    # setupUi

    def retranslateUi(self, NavRail):
        self.navGlass.setProperty(u"backdropSource", QCoreApplication.translate("NavRail", u"wallpaper", None))
        self.navDashboard.setProperty(u"iconName", QCoreApplication.translate("NavRail", u"feather/grid", None))
        self.navDashboard.setProperty(u"role", QCoreApplication.translate("NavRail", u"navBtn", None))
        self.navDevices.setProperty(u"iconName", QCoreApplication.translate("NavRail", u"feather/cpu", None))
        self.navDevices.setProperty(u"role", QCoreApplication.translate("NavRail", u"navBtn", None))
        self.navStats.setProperty(u"iconName", QCoreApplication.translate("NavRail", u"feather/bar-chart-2", None))
        self.navStats.setProperty(u"role", QCoreApplication.translate("NavRail", u"navBtn", None))
        self.navAdd.setProperty(u"iconName", QCoreApplication.translate("NavRail", u"feather/plus", None))
        self.navAdd.setProperty(u"role", QCoreApplication.translate("NavRail", u"navBtn", None))
        self.navAutomation.setProperty(u"iconName", QCoreApplication.translate("NavRail", u"feather/sliders", None))
        self.navAutomation.setProperty(u"role", QCoreApplication.translate("NavRail", u"navBtn", None))
        self.navThemeToggle.setProperty(u"darkTheme", QCoreApplication.translate("NavRail", u"Glass Dusk", None))
        self.navThemeToggle.setProperty(u"lightTheme", QCoreApplication.translate("NavRail", u"Glass Day", None))
        self.navThemeToggle.setProperty(u"role", QCoreApplication.translate("NavRail", u"navBtn", None))
        self.navAvatar.setText(QCoreApplication.translate("NavRail", u"K", None))
        self.navAvatar.setProperty(u"imageSource", QCoreApplication.translate("NavRail", u"https://i.pravatar.cc/96?img=12", None))
        pass
    # retranslateUi

