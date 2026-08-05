# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'new_MainWindow.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QLabel,
    QMainWindow, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

from Custom_Widgets.QCustomLiquidGauge import QCustomLiquidGauge
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(860, 680)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.mainGrid = QGridLayout(self.centralwidget)
        self.mainGrid.setObjectName(u"mainGrid")
        self.mainGrid.setHorizontalSpacing(20)
        self.mainGrid.setVerticalSpacing(20)
        self.mainGrid.setContentsMargins(24, 24, 24, 24)
        self.fuelCard = QFrame(self.centralwidget)
        self.fuelCard.setObjectName(u"fuelCard")
        self.fuelCard.setFrameShape(QFrame.StyledPanel)
        self.fuelCardLayout = QVBoxLayout(self.fuelCard)
        self.fuelCardLayout.setSpacing(2)
        self.fuelCardLayout.setObjectName(u"fuelCardLayout")
        self.fuelCardLayout.setContentsMargins(20, 18, 20, 18)
        self.fuelTitle = QLabel(self.fuelCard)
        self.fuelTitle.setObjectName(u"fuelTitle")

        self.fuelCardLayout.addWidget(self.fuelTitle)

        self.fuelSub = QLabel(self.fuelCard)
        self.fuelSub.setObjectName(u"fuelSub")

        self.fuelCardLayout.addWidget(self.fuelSub)

        self.fuelSpacer = QSpacerItem(0, 6, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.fuelCardLayout.addItem(self.fuelSpacer)

        self.fuelGauge = QCustomLiquidGauge(self.fuelCard)
        self.fuelGauge.setObjectName(u"fuelGauge")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.fuelGauge.sizePolicy().hasHeightForWidth())
        self.fuelGauge.setSizePolicy(sizePolicy)
        self.fuelGauge.setProperty(u"value", 0.000000000000000)

        self.fuelCardLayout.addWidget(self.fuelGauge)

        self.fuelCardLayout.setStretch(3, 1)

        self.mainGrid.addWidget(self.fuelCard, 0, 0, 1, 1)

        self.batteryCard = QFrame(self.centralwidget)
        self.batteryCard.setObjectName(u"batteryCard")
        self.batteryCard.setFrameShape(QFrame.StyledPanel)
        self.batteryCardLayout = QVBoxLayout(self.batteryCard)
        self.batteryCardLayout.setSpacing(2)
        self.batteryCardLayout.setObjectName(u"batteryCardLayout")
        self.batteryCardLayout.setContentsMargins(20, 18, 20, 18)
        self.batteryTitle = QLabel(self.batteryCard)
        self.batteryTitle.setObjectName(u"batteryTitle")

        self.batteryCardLayout.addWidget(self.batteryTitle)

        self.batterySub = QLabel(self.batteryCard)
        self.batterySub.setObjectName(u"batterySub")

        self.batteryCardLayout.addWidget(self.batterySub)

        self.batterySpacer = QSpacerItem(0, 6, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.batteryCardLayout.addItem(self.batterySpacer)

        self.batteryGauge = QCustomLiquidGauge(self.batteryCard)
        self.batteryGauge.setObjectName(u"batteryGauge")
        sizePolicy.setHeightForWidth(self.batteryGauge.sizePolicy().hasHeightForWidth())
        self.batteryGauge.setSizePolicy(sizePolicy)
        self.batteryGauge.setProperty(u"value", 0.000000000000000)
        self.batteryGauge.setProperty(u"cornerRadius", 26)

        self.batteryCardLayout.addWidget(self.batteryGauge)

        self.batteryCardLayout.setStretch(3, 1)

        self.mainGrid.addWidget(self.batteryCard, 0, 1, 1, 1)

        self.tankCard = QFrame(self.centralwidget)
        self.tankCard.setObjectName(u"tankCard")
        self.tankCard.setFrameShape(QFrame.StyledPanel)
        self.tankCardLayout = QVBoxLayout(self.tankCard)
        self.tankCardLayout.setSpacing(2)
        self.tankCardLayout.setObjectName(u"tankCardLayout")
        self.tankCardLayout.setContentsMargins(20, 18, 20, 18)
        self.tankTitle = QLabel(self.tankCard)
        self.tankTitle.setObjectName(u"tankTitle")

        self.tankCardLayout.addWidget(self.tankTitle)

        self.tankSub = QLabel(self.tankCard)
        self.tankSub.setObjectName(u"tankSub")

        self.tankCardLayout.addWidget(self.tankSub)

        self.tankSpacer = QSpacerItem(0, 6, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.tankCardLayout.addItem(self.tankSpacer)

        self.tankGauge = QCustomLiquidGauge(self.tankCard)
        self.tankGauge.setObjectName(u"tankGauge")
        sizePolicy.setHeightForWidth(self.tankGauge.sizePolicy().hasHeightForWidth())
        self.tankGauge.setSizePolicy(sizePolicy)
        self.tankGauge.setProperty(u"value", 0.000000000000000)

        self.tankCardLayout.addWidget(self.tankGauge)

        self.tankCardLayout.setStretch(3, 1)

        self.mainGrid.addWidget(self.tankCard, 1, 0, 1, 1)

        self.humidityCard = QFrame(self.centralwidget)
        self.humidityCard.setObjectName(u"humidityCard")
        self.humidityCard.setFrameShape(QFrame.StyledPanel)
        self.humidityCardLayout = QVBoxLayout(self.humidityCard)
        self.humidityCardLayout.setSpacing(2)
        self.humidityCardLayout.setObjectName(u"humidityCardLayout")
        self.humidityCardLayout.setContentsMargins(20, 18, 20, 18)
        self.humidityTitle = QLabel(self.humidityCard)
        self.humidityTitle.setObjectName(u"humidityTitle")

        self.humidityCardLayout.addWidget(self.humidityTitle)

        self.humiditySub = QLabel(self.humidityCard)
        self.humiditySub.setObjectName(u"humiditySub")

        self.humidityCardLayout.addWidget(self.humiditySub)

        self.humiditySpacer = QSpacerItem(0, 6, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.humidityCardLayout.addItem(self.humiditySpacer)

        self.humidityGauge = QCustomLiquidGauge(self.humidityCard)
        self.humidityGauge.setObjectName(u"humidityGauge")
        sizePolicy.setHeightForWidth(self.humidityGauge.sizePolicy().hasHeightForWidth())
        self.humidityGauge.setSizePolicy(sizePolicy)
        self.humidityGauge.setProperty(u"value", 0.000000000000000)

        self.humidityCardLayout.addWidget(self.humidityGauge)

        self.humidityCardLayout.setStretch(3, 1)

        self.mainGrid.addWidget(self.humidityCard, 1, 1, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"QCustomLiquidGauge \u2014 Demo", None))
        self.fuelTitle.setText(QCoreApplication.translate("MainWindow", u"Fuel level", None))
        self.fuelSub.setText(QCoreApplication.translate("MainWindow", u"Tank \u00b7 11.6 gal", None))
        self.fuelGauge.setProperty(u"centerText", QCoreApplication.translate("MainWindow", u"3.61", None))
        self.fuelGauge.setProperty(u"centerSuffix", QCoreApplication.translate("MainWindow", u"gal", None))
        self.batteryTitle.setText(QCoreApplication.translate("MainWindow", u"Battery", None))
        self.batterySub.setText(QCoreApplication.translate("MainWindow", u"Charging", None))
        self.batteryGauge.setProperty(u"shape", QCoreApplication.translate("MainWindow", u"roundedRect", None))
        self.batteryGauge.setProperty(u"centerSuffix", QCoreApplication.translate("MainWindow", u"%", None))
        self.tankTitle.setText(QCoreApplication.translate("MainWindow", u"Water tank", None))
        self.tankSub.setText(QCoreApplication.translate("MainWindow", u"Reservoir A", None))
        self.tankGauge.setProperty(u"centerSuffix", QCoreApplication.translate("MainWindow", u"%", None))
        self.humidityTitle.setText(QCoreApplication.translate("MainWindow", u"Humidity", None))
        self.humiditySub.setText(QCoreApplication.translate("MainWindow", u"Living room", None))
        self.humidityGauge.setProperty(u"centerSuffix", QCoreApplication.translate("MainWindow", u"%", None))
    # retranslateUi

