# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'new_PowerChart.ui'
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
from Custom_Widgets.QCustomMiniBarChart import QCustomMiniBarChart
from Custom_Widgets.QCustomQLabel import QCustomQLabel
class Ui_PowerChart(object):
    def setupUi(self, PowerChart):
        if not PowerChart.objectName():
            PowerChart.setObjectName(u"PowerChart")
        PowerChart.resize(420, 320)
        self.powerRoot = QVBoxLayout(PowerChart)
        self.powerRoot.setSpacing(0)
        self.powerRoot.setObjectName(u"powerRoot")
        self.powerRoot.setContentsMargins(0, 0, 0, 0)
        self.powerGlass = QCustomGlassFrame(PowerChart)
        self.powerGlass.setObjectName(u"powerGlass")
        self.powerGlass.setProperty(u"cornerRadius", 26)
        self.powerLayout = QVBoxLayout(self.powerGlass)
        self.powerLayout.setSpacing(10)
        self.powerLayout.setObjectName(u"powerLayout")
        self.powerLayout.setContentsMargins(20, 18, 20, 16)
        self.powerHeader = QHBoxLayout()
        self.powerHeader.setSpacing(8)
        self.powerHeader.setObjectName(u"powerHeader")
        self.powerTitle = QLabel(self.powerGlass)
        self.powerTitle.setObjectName(u"powerTitle")

        self.powerHeader.addWidget(self.powerTitle)

        self.powerUnit = QLabel(self.powerGlass)
        self.powerUnit.setObjectName(u"powerUnit")

        self.powerHeader.addWidget(self.powerUnit)

        self.powerHeaderSpacer = QSpacerItem(10, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.powerHeader.addItem(self.powerHeaderSpacer)

        self.powerMenu = QCustomQLabel(self.powerGlass)
        self.powerMenu.setObjectName(u"powerMenu")
        self.powerMenu.setMinimumSize(QSize(24, 24))
        self.powerMenu.setMaximumSize(QSize(24, 24))

        self.powerHeader.addWidget(self.powerMenu)


        self.powerLayout.addLayout(self.powerHeader)

        self.powerBars = QCustomMiniBarChart(self.powerGlass)
        self.powerBars.setObjectName(u"powerBars")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.powerBars.sizePolicy().hasHeightForWidth())
        self.powerBars.setSizePolicy(sizePolicy)
        self.powerBars.setProperty(u"highlightIndexProp", 2)
        self.powerBars.setProperty(u"barWidth", 14)
        self.powerBars.setProperty(u"cornerRadius", 7)
        self.powerBars.setProperty(u"showLabels", True)

        self.powerLayout.addWidget(self.powerBars)


        self.powerRoot.addWidget(self.powerGlass)


        self.retranslateUi(PowerChart)

        QMetaObject.connectSlotsByName(PowerChart)
    # setupUi

    def retranslateUi(self, PowerChart):
        self.powerGlass.setProperty(u"backdropSource", QCoreApplication.translate("PowerChart", u"wallpaper", None))
        self.powerTitle.setText(QCoreApplication.translate("PowerChart", u"Power Consumption", None))
        self.powerTitle.setProperty(u"role", QCoreApplication.translate("PowerChart", u"cardTitle", None))
        self.powerUnit.setText(QCoreApplication.translate("PowerChart", u"(kWh)", None))
        self.powerUnit.setProperty(u"role", QCoreApplication.translate("PowerChart", u"mutedSm", None))
        self.powerMenu.setProperty(u"iconName", QCoreApplication.translate("PowerChart", u"feather/more-horizontal", None))
        self.powerMenu.setProperty(u"role", QCoreApplication.translate("PowerChart", u"appsIcon", None))
        self.powerBars.setProperty(u"valuesCsv", QCoreApplication.translate("PowerChart", u"90,120,169,60,130,105", None))
        self.powerBars.setProperty(u"labelsCsv", QCoreApplication.translate("PowerChart", u"Jan,Feb,Mar,Apr,May,Jun", None))
        self.powerBars.setProperty(u"yLabelsCsv", QCoreApplication.translate("PowerChart", u"0,50,90,130,170", None))
        self.powerBars.setProperty(u"calloutText", QCoreApplication.translate("PowerChart", u"169 kWh", None))
        pass
    # retranslateUi

