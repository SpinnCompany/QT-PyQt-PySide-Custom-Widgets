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
from PySide6.QtWidgets import (QApplication, QComboBox, QHBoxLayout, QLabel,
    QMainWindow, QPushButton, QSizePolicy, QSlider,
    QSpacerItem, QVBoxLayout, QWidget)

from Custom_Widgets.QCustomRangeBarChart import QCustomRangeBarChart
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(640, 520)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.mainLayout = QVBoxLayout(self.centralwidget)
        self.mainLayout.setSpacing(14)
        self.mainLayout.setObjectName(u"mainLayout")
        self.mainLayout.setContentsMargins(20, 20, 20, 20)
        self.chart = QCustomRangeBarChart(self.centralwidget)
        self.chart.setObjectName(u"chart")
        self.chart.setMinimumSize(QSize(0, 320))
        self.chart.setProperty(u"rangesCsv", u"Mon=4,12;Tue=6,15;Wed=3,9;Thu=8,17;Fri=5,11;Sat=7,14;Sun=2,8")
        self.chart.setProperty(u"showBounds", True)

        self.mainLayout.addWidget(self.chart)

        self.controlsRow = QHBoxLayout()
        self.controlsRow.setSpacing(10)
        self.controlsRow.setObjectName(u"controlsRow")
        self.orientationLabel = QLabel(self.centralwidget)
        self.orientationLabel.setObjectName(u"orientationLabel")

        self.controlsRow.addWidget(self.orientationLabel)

        self.orientationCombo = QComboBox(self.centralwidget)
        self.orientationCombo.addItem("")
        self.orientationCombo.addItem("")
        self.orientationCombo.setObjectName(u"orientationCombo")

        self.controlsRow.addWidget(self.orientationCombo)

        self.widthLabel = QLabel(self.centralwidget)
        self.widthLabel.setObjectName(u"widthLabel")

        self.controlsRow.addWidget(self.widthLabel)

        self.widthSlider = QSlider(self.centralwidget)
        self.widthSlider.setObjectName(u"widthSlider")
        self.widthSlider.setMinimum(10)
        self.widthSlider.setMaximum(100)
        self.widthSlider.setValue(55)
        self.widthSlider.setOrientation(Qt.Horizontal)

        self.controlsRow.addWidget(self.widthSlider)

        self.boundsButton = QPushButton(self.centralwidget)
        self.boundsButton.setObjectName(u"boundsButton")
        self.boundsButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.controlsRow.addWidget(self.boundsButton)

        self.themeButton = QPushButton(self.centralwidget)
        self.themeButton.setObjectName(u"themeButton")
        self.themeButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.controlsRow.addWidget(self.themeButton)

        self.controlsSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.controlsRow.addItem(self.controlsSpacer)


        self.mainLayout.addLayout(self.controlsRow)

        self.statusLabel = QLabel(self.centralwidget)
        self.statusLabel.setObjectName(u"statusLabel")

        self.mainLayout.addWidget(self.statusLabel)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"QCustomRangeBarChart", None))
        self.orientationLabel.setText(QCoreApplication.translate("MainWindow", u"Orientation", None))
        self.orientationCombo.setItemText(0, QCoreApplication.translate("MainWindow", u"vertical", None))
        self.orientationCombo.setItemText(1, QCoreApplication.translate("MainWindow", u"horizontal", None))

        self.widthLabel.setText(QCoreApplication.translate("MainWindow", u"Bar width", None))
        self.boundsButton.setText(QCoreApplication.translate("MainWindow", u"Bounds", None))
        self.themeButton.setText(QCoreApplication.translate("MainWindow", u"Light / dark", None))
        self.statusLabel.setText(QCoreApplication.translate("MainWindow", u"Hover a bar for its range", None))
    # retranslateUi

