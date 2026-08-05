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
    QPushButton, QSizePolicy, QSlider, QSpacerItem,
    QSpinBox, QVBoxLayout, QWidget)

from Custom_Widgets.QCustomRadialLines import QCustomRadialLines
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(580, 620)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.radialLines = QCustomRadialLines(self.centralwidget)
        self.radialLines.setObjectName(u"radialLines")
        self.radialLines.setMinimumSize(QSize(0, 360))
        self.radialLines.setProperty(u"showMarkers", True)

        self.verticalLayout.addWidget(self.radialLines)

        self.controlsRow = QHBoxLayout()
        self.controlsRow.setObjectName(u"controlsRow")
        self.ringsCaption = QLabel(self.centralwidget)
        self.ringsCaption.setObjectName(u"ringsCaption")

        self.controlsRow.addWidget(self.ringsCaption)

        self.ringsSpin = QSpinBox(self.centralwidget)
        self.ringsSpin.setObjectName(u"ringsSpin")
        self.ringsSpin.setMinimum(1)
        self.ringsSpin.setMaximum(10)
        self.ringsSpin.setValue(4)

        self.controlsRow.addWidget(self.ringsSpin)

        self.fillCaption = QLabel(self.centralwidget)
        self.fillCaption.setObjectName(u"fillCaption")

        self.controlsRow.addWidget(self.fillCaption)

        self.fillSlider = QSlider(self.centralwidget)
        self.fillSlider.setObjectName(u"fillSlider")
        self.fillSlider.setMaximum(100)
        self.fillSlider.setValue(15)
        self.fillSlider.setOrientation(Qt.Horizontal)

        self.controlsRow.addWidget(self.fillSlider)

        self.closedBtn = QPushButton(self.centralwidget)
        self.closedBtn.setObjectName(u"closedBtn")

        self.controlsRow.addWidget(self.closedBtn)

        self.markersBtn = QPushButton(self.centralwidget)
        self.markersBtn.setObjectName(u"markersBtn")

        self.controlsRow.addWidget(self.markersBtn)

        self.gridBtn = QPushButton(self.centralwidget)
        self.gridBtn.setObjectName(u"gridBtn")

        self.controlsRow.addWidget(self.gridBtn)

        self.themeBtn = QPushButton(self.centralwidget)
        self.themeBtn.setObjectName(u"themeBtn")

        self.controlsRow.addWidget(self.themeBtn)

        self.controlsSpacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.controlsRow.addItem(self.controlsSpacer)


        self.verticalLayout.addLayout(self.controlsRow)

        self.statusLabel = QLabel(self.centralwidget)
        self.statusLabel.setObjectName(u"statusLabel")

        self.verticalLayout.addWidget(self.statusLabel)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"QCustomRadialLines", None))
        self.ringsCaption.setText(QCoreApplication.translate("MainWindow", u"Rings", None))
        self.fillCaption.setText(QCoreApplication.translate("MainWindow", u"Fill", None))
        self.closedBtn.setText(QCoreApplication.translate("MainWindow", u"Closed", None))
        self.markersBtn.setText(QCoreApplication.translate("MainWindow", u"Markers", None))
        self.gridBtn.setText(QCoreApplication.translate("MainWindow", u"Grid", None))
        self.themeBtn.setText(QCoreApplication.translate("MainWindow", u"Light / dark", None))
        self.statusLabel.setText(QCoreApplication.translate("MainWindow", u"Hover a shape", None))
    # retranslateUi

