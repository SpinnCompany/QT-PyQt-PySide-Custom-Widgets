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
class Ui_NavRail(object):
    def setupUi(self, NavRail):
        if not NavRail.objectName():
            NavRail.setObjectName(u"NavRail")
        NavRail.resize(84, 620)
        self.navRoot = QVBoxLayout(NavRail)
        self.navRoot.setSpacing(0)
        self.navRoot.setObjectName(u"navRoot")
        self.navRoot.setContentsMargins(0, 0, 0, 0)
        self.navGlass = QCustomGlassFrame(NavRail)
        self.navGlass.setObjectName(u"navGlass")
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

        self.navSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.navLayout.addItem(self.navSpacer)

        self.navAvatar = QCustomAvatar(self.navGlass)
        self.navAvatar.setObjectName(u"navAvatar")
        self.navAvatar.setMinimumSize(QSize(46, 46))
        self.navAvatar.setMaximumSize(QSize(46, 46))
        self.navAvatar.setProperty(u"showStatus", False)
        self.navAvatar.setProperty(u"ringWidth", 2)

        self.navLayout.addWidget(self.navAvatar, 0, Qt.AlignHCenter)


        self.navRoot.addWidget(self.navGlass)


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
        self.navAvatar.setText(QCoreApplication.translate("NavRail", u"K", None))
        pass
    # retranslateUi

