# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'new_RoomTabs.ui'
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
    QSizePolicy, QVBoxLayout, QWidget)

from Custom_Widgets.QCustomGlassFrame import QCustomGlassFrame
from Custom_Widgets.QCustomPageDots import QCustomPageDots
from Custom_Widgets.QCustomQPushButton import QCustomQPushButton
from Custom_Widgets.QCustomSegmentedControl import QCustomSegmentedControl
class Ui_RoomTabs(object):
    def setupUi(self, RoomTabs):
        if not RoomTabs.objectName():
            RoomTabs.setObjectName(u"RoomTabs")
        RoomTabs.resize(720, 92)
        self.tabsRoot = QVBoxLayout(RoomTabs)
        self.tabsRoot.setSpacing(8)
        self.tabsRoot.setObjectName(u"tabsRoot")
        self.tabsRoot.setContentsMargins(0, 0, 0, 0)
        self.tabsGlass = QCustomGlassFrame(RoomTabs)
        self.tabsGlass.setObjectName(u"tabsGlass")
        self.tabsGlass.setProperty(u"cornerRadius", 27)
        self.tabsLayout = QHBoxLayout(self.tabsGlass)
        self.tabsLayout.setSpacing(10)
        self.tabsLayout.setObjectName(u"tabsLayout")
        self.tabsLayout.setContentsMargins(8, 7, 8, 7)
        self.roomSegments = QCustomSegmentedControl(self.tabsGlass)
        self.roomSegments.setObjectName(u"roomSegments")
        self.roomSegments.setProperty(u"currentIndex", 0)
        self.roomSegments.setMinimumSize(QSize(560, 40))

        self.tabsLayout.addWidget(self.roomSegments)

        self.roomAdd = QCustomQPushButton(self.tabsGlass)
        self.roomAdd.setObjectName(u"roomAdd")
        self.roomAdd.setMinimumSize(QSize(40, 40))
        self.roomAdd.setMaximumSize(QSize(40, 40))
        self.roomAdd.setIconSize(QSize(18, 18))

        self.tabsLayout.addWidget(self.roomAdd)


        self.tabsRoot.addWidget(self.tabsGlass, 0, Qt.AlignHCenter)

        self.roomDots = QCustomPageDots(RoomTabs)
        self.roomDots.setObjectName(u"roomDots")
        self.roomDots.setProperty(u"count", 5)
        self.roomDots.setProperty(u"activeIndex", 0)
        self.roomDots.setMinimumSize(QSize(90, 14))

        self.tabsRoot.addWidget(self.roomDots, 0, Qt.AlignHCenter)


        self.retranslateUi(RoomTabs)

        QMetaObject.connectSlotsByName(RoomTabs)
    # setupUi

    def retranslateUi(self, RoomTabs):
        self.tabsGlass.setProperty(u"backdropSource", QCoreApplication.translate("RoomTabs", u"wallpaper", None))
        self.roomSegments.setProperty(u"segments", QCoreApplication.translate("RoomTabs", u"Living Room,Bedroom,Kitchen,Backyard,Garage", None))
        self.roomAdd.setProperty(u"iconName", QCoreApplication.translate("RoomTabs", u"feather/plus", None))
        self.roomAdd.setProperty(u"role", QCoreApplication.translate("RoomTabs", u"addBtn", None))
        pass
    # retranslateUi

