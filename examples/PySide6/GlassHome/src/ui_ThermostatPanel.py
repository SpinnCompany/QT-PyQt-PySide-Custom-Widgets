# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'new_ThermostatPanel.ui'
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

from Custom_Widgets.QCustomQPushButton import QCustomQPushButton
from Custom_Widgets.QCustomRadialGauge import QCustomRadialGauge
from Custom_Widgets.QCustomSwitch import QCustomSwitch
class Ui_ThermostatPanel(object):
    def setupUi(self, ThermostatPanel):
        if not ThermostatPanel.objectName():
            ThermostatPanel.setObjectName(u"ThermostatPanel")
        ThermostatPanel.resize(280, 420)
        self.thermoRoot = QVBoxLayout(ThermostatPanel)
        self.thermoRoot.setSpacing(12)
        self.thermoRoot.setObjectName(u"thermoRoot")
        self.thermoRoot.setContentsMargins(0, 0, 0, 0)
        self.clockLabel = QLabel(ThermostatPanel)
        self.clockLabel.setObjectName(u"clockLabel")

        self.thermoRoot.addWidget(self.clockLabel)

        self.clockDivider = QFrame(ThermostatPanel)
        self.clockDivider.setObjectName(u"clockDivider")
        self.clockDivider.setFrameShape(QFrame.HLine)
        self.clockDivider.setMaximumSize(QSize(16777215, 1))

        self.thermoRoot.addWidget(self.clockDivider)

        self.thermoHeader = QHBoxLayout()
        self.thermoHeader.setObjectName(u"thermoHeader")
        self.thermoTitle = QLabel(ThermostatPanel)
        self.thermoTitle.setObjectName(u"thermoTitle")

        self.thermoHeader.addWidget(self.thermoTitle)

        self.thermoHeaderSpacer = QSpacerItem(10, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.thermoHeader.addItem(self.thermoHeaderSpacer)

        self.thermoSwitch = QCustomSwitch(ThermostatPanel)
        self.thermoSwitch.setObjectName(u"thermoSwitch")
        self.thermoSwitch.setProperty(u"checked", True)

        self.thermoHeader.addWidget(self.thermoSwitch)


        self.thermoRoot.addLayout(self.thermoHeader)

        self.thermoGauge = QCustomRadialGauge(ThermostatPanel)
        self.thermoGauge.setObjectName(u"thermoGauge")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.thermoGauge.sizePolicy().hasHeightForWidth())
        self.thermoGauge.setSizePolicy(sizePolicy)
        self.thermoGauge.setMinimumSize(QSize(190, 190))
        self.thermoGauge.setProperty(u"minimum", 40.000000000000000)
        self.thermoGauge.setProperty(u"maximum", 90.000000000000000)
        self.thermoGauge.setProperty(u"value", 64.000000000000000)
        self.thermoGauge.setProperty(u"startAngle", 225.000000000000000)
        self.thermoGauge.setProperty(u"spanAngle", -270.000000000000000)
        self.thermoGauge.setProperty(u"arcWidth", 12)
        self.thermoGauge.setProperty(u"showNeedle", False)
        self.thermoGauge.setProperty(u"showHandle", True)
        self.thermoGauge.setProperty(u"showGuide", False)
        self.thermoGauge.setProperty(u"showScaleLabels", False)
        self.thermoGauge.setProperty(u"showTicks", False)
        self.thermoGauge.setProperty(u"roundedCaps", True)
        self.thermoGauge.setProperty(u"animated", True)

        self.thermoRoot.addWidget(self.thermoGauge)

        self.thermoAdjustRow = QHBoxLayout()
        self.thermoAdjustRow.setSpacing(22)
        self.thermoAdjustRow.setObjectName(u"thermoAdjustRow")
        self.adjLeft = QSpacerItem(10, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.thermoAdjustRow.addItem(self.adjLeft)

        self.thermoMinus = QCustomQPushButton(ThermostatPanel)
        self.thermoMinus.setObjectName(u"thermoMinus")
        self.thermoMinus.setMinimumSize(QSize(40, 40))
        self.thermoMinus.setMaximumSize(QSize(40, 40))
        self.thermoMinus.setIconSize(QSize(16, 16))

        self.thermoAdjustRow.addWidget(self.thermoMinus)

        self.thermoPlus = QCustomQPushButton(ThermostatPanel)
        self.thermoPlus.setObjectName(u"thermoPlus")
        self.thermoPlus.setMinimumSize(QSize(40, 40))
        self.thermoPlus.setMaximumSize(QSize(40, 40))
        self.thermoPlus.setIconSize(QSize(16, 16))

        self.thermoAdjustRow.addWidget(self.thermoPlus)

        self.adjRight = QSpacerItem(10, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.thermoAdjustRow.addItem(self.adjRight)


        self.thermoRoot.addLayout(self.thermoAdjustRow)


        self.retranslateUi(ThermostatPanel)

        QMetaObject.connectSlotsByName(ThermostatPanel)
    # setupUi

    def retranslateUi(self, ThermostatPanel):
        self.clockLabel.setText(QCoreApplication.translate("ThermostatPanel", u"10:02 PM", None))
        self.clockLabel.setProperty(u"role", QCoreApplication.translate("ThermostatPanel", u"clock", None))
        self.thermoTitle.setText(QCoreApplication.translate("ThermostatPanel", u"Thermostat", None))
        self.thermoTitle.setProperty(u"role", QCoreApplication.translate("ThermostatPanel", u"cardTitle", None))
        self.thermoSwitch.setProperty(u"sizeVariant", QCoreApplication.translate("ThermostatPanel", u"sm", None))
        self.thermoGauge.setProperty(u"zonesCsv", "")
        self.thermoGauge.setProperty(u"centerText", QCoreApplication.translate("ThermostatPanel", u"64", None))
        self.thermoGauge.setProperty(u"centerSuffix", QCoreApplication.translate("ThermostatPanel", u"\u00b0", None))
        self.thermoGauge.setProperty(u"statusText", QCoreApplication.translate("ThermostatPanel", u"(\u00b0Fahrenheit)", None))
        self.thermoMinus.setProperty(u"iconName", QCoreApplication.translate("ThermostatPanel", u"feather/minus", None))
        self.thermoMinus.setProperty(u"role", QCoreApplication.translate("ThermostatPanel", u"roundBtn", None))
        self.thermoPlus.setProperty(u"iconName", QCoreApplication.translate("ThermostatPanel", u"feather/plus", None))
        self.thermoPlus.setProperty(u"role", QCoreApplication.translate("ThermostatPanel", u"roundBtn", None))
        pass
    # retranslateUi

