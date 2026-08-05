# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'new_DeviceTile.ui'
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

from Custom_Widgets.QCustomGlassFrame import QCustomGlassFrame
from Custom_Widgets.QCustomQLabel import QCustomQLabel
from Custom_Widgets.QCustomSwitch import QCustomSwitch
class Ui_DeviceTile(object):
    def setupUi(self, DeviceTile):
        if not DeviceTile.objectName():
            DeviceTile.setObjectName(u"DeviceTile")
        DeviceTile.resize(200, 150)
        self.tileRoot = QVBoxLayout(DeviceTile)
        self.tileRoot.setSpacing(0)
        self.tileRoot.setObjectName(u"tileRoot")
        self.tileRoot.setContentsMargins(0, 0, 0, 0)
        self.tileGlass = QCustomGlassFrame(DeviceTile)
        self.tileGlass.setObjectName(u"tileGlass")
        self.tileGlass.setProperty(u"cornerRadius", 22)
        self.tileLayout = QVBoxLayout(self.tileGlass)
        self.tileLayout.setSpacing(8)
        self.tileLayout.setObjectName(u"tileLayout")
        self.tileLayout.setContentsMargins(16, 14, 14, 14)
        self.tileTop = QHBoxLayout()
        self.tileTop.setObjectName(u"tileTop")
        self.tileApps = QCustomQLabel(self.tileGlass)
        self.tileApps.setObjectName(u"tileApps")
        self.tileApps.setMinimumSize(QSize(22, 22))
        self.tileApps.setMaximumSize(QSize(22, 22))

        self.tileTop.addWidget(self.tileApps)

        self.tileTopSpacer = QSpacerItem(10, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.tileTop.addItem(self.tileTopSpacer)

        self.tileSwitch = QCustomSwitch(self.tileGlass)
        self.tileSwitch.setObjectName(u"tileSwitch")

        self.tileTop.addWidget(self.tileSwitch)


        self.tileLayout.addLayout(self.tileTop)

        self.tileSpacer = QSpacerItem(10, 18, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.tileLayout.addItem(self.tileSpacer)

        self.tileVendor = QLabel(self.tileGlass)
        self.tileVendor.setObjectName(u"tileVendor")

        self.tileLayout.addWidget(self.tileVendor)

        self.tileName = QLabel(self.tileGlass)
        self.tileName.setObjectName(u"tileName")
        self.tileName.setWordWrap(True)

        self.tileLayout.addWidget(self.tileName)


        self.tileRoot.addWidget(self.tileGlass)


        self.retranslateUi(DeviceTile)

        QMetaObject.connectSlotsByName(DeviceTile)
    # setupUi

    def retranslateUi(self, DeviceTile):
        self.tileGlass.setProperty(u"backdropSource", QCoreApplication.translate("DeviceTile", u"wallpaper", None))
        self.tileApps.setProperty(u"iconName", QCoreApplication.translate("DeviceTile", u"material_design/apps", None))
        self.tileApps.setProperty(u"role", QCoreApplication.translate("DeviceTile", u"appsIcon", None))
        self.tileSwitch.setProperty(u"sizeVariant", QCoreApplication.translate("DeviceTile", u"sm", None))
        self.tileVendor.setText(QCoreApplication.translate("DeviceTile", u"Gaabor", None))
        self.tileVendor.setProperty(u"role", QCoreApplication.translate("DeviceTile", u"mutedSm", None))
        self.tileName.setText(QCoreApplication.translate("DeviceTile", u"Gaabor Humidifier", None))
        self.tileName.setProperty(u"role", QCoreApplication.translate("DeviceTile", u"tileName", None))
        pass
    # retranslateUi

