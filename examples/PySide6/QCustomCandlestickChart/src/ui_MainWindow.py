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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QMainWindow,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

from Custom_Widgets.QCustomCandlestickChart import QCustomCandlestickChart
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(720, 460)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.rootLayout = QVBoxLayout(self.centralwidget)
        self.rootLayout.setSpacing(14)
        self.rootLayout.setObjectName(u"rootLayout")
        self.rootLayout.setContentsMargins(20, 20, 20, 20)
        self.chart = QCustomCandlestickChart(self.centralwidget)
        self.chart.setObjectName(u"chart")
        self.chart.setMinimumSize(QSize(0, 300))

        self.rootLayout.addWidget(self.chart)

        self.readoutLabel = QLabel(self.centralwidget)
        self.readoutLabel.setObjectName(u"readoutLabel")

        self.rootLayout.addWidget(self.readoutLabel)

        self.controlsRow = QHBoxLayout()
        self.controlsRow.setSpacing(8)
        self.controlsRow.setObjectName(u"controlsRow")
        self.hollowButton = QPushButton(self.centralwidget)
        self.hollowButton.setObjectName(u"hollowButton")

        self.controlsRow.addWidget(self.hollowButton)

        self.gridButton = QPushButton(self.centralwidget)
        self.gridButton.setObjectName(u"gridButton")

        self.controlsRow.addWidget(self.gridButton)

        self.tooltipButton = QPushButton(self.centralwidget)
        self.tooltipButton.setObjectName(u"tooltipButton")

        self.controlsRow.addWidget(self.tooltipButton)

        self.themeButton = QPushButton(self.centralwidget)
        self.themeButton.setObjectName(u"themeButton")

        self.controlsRow.addWidget(self.themeButton)

        self.controlsSpacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.controlsRow.addItem(self.controlsSpacer)


        self.rootLayout.addLayout(self.controlsRow)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"QCustomCandlestickChart", None))
        self.readoutLabel.setText(QCoreApplication.translate("MainWindow", u"Hover a candle to inspect its OHLC", None))
        self.hollowButton.setText(QCoreApplication.translate("MainWindow", u"Hollow up candles", None))
        self.gridButton.setText(QCoreApplication.translate("MainWindow", u"Grid", None))
        self.tooltipButton.setText(QCoreApplication.translate("MainWindow", u"Tooltip", None))
        self.themeButton.setText(QCoreApplication.translate("MainWindow", u"Light / dark", None))
    # retranslateUi

