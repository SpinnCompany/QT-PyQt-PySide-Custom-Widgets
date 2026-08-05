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
    QSpacerItem, QSpinBox, QVBoxLayout, QWidget)

from Custom_Widgets.QCustomRadarChart import QCustomRadarChart
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(620, 620)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.radarChart = QCustomRadarChart(self.centralwidget)
        self.radarChart.setObjectName(u"radarChart")
        self.radarChart.setMinimumSize(QSize(0, 320))
        self.radarChart.setProperty(u"showRingLabels", True)

        self.verticalLayout.addWidget(self.radarChart)

        self.statusLabel = QLabel(self.centralwidget)
        self.statusLabel.setObjectName(u"statusLabel")

        self.verticalLayout.addWidget(self.statusLabel)

        self.controlsRow = QHBoxLayout()
        self.controlsRow.setObjectName(u"controlsRow")
        self.gridCaption = QLabel(self.centralwidget)
        self.gridCaption.setObjectName(u"gridCaption")

        self.controlsRow.addWidget(self.gridCaption)

        self.gridBox = QComboBox(self.centralwidget)
        self.gridBox.addItem("")
        self.gridBox.addItem("")
        self.gridBox.setObjectName(u"gridBox")

        self.controlsRow.addWidget(self.gridBox)

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
        self.fillSlider.setValue(25)
        self.fillSlider.setOrientation(Qt.Horizontal)

        self.controlsRow.addWidget(self.fillSlider)

        self.rotateCaption = QLabel(self.centralwidget)
        self.rotateCaption.setObjectName(u"rotateCaption")

        self.controlsRow.addWidget(self.rotateCaption)

        self.rotateSlider = QSlider(self.centralwidget)
        self.rotateSlider.setObjectName(u"rotateSlider")
        self.rotateSlider.setMaximum(359)
        self.rotateSlider.setValue(90)
        self.rotateSlider.setOrientation(Qt.Horizontal)

        self.controlsRow.addWidget(self.rotateSlider)


        self.verticalLayout.addLayout(self.controlsRow)

        self.buttonsRow = QHBoxLayout()
        self.buttonsRow.setObjectName(u"buttonsRow")
        self.markersBtn = QPushButton(self.centralwidget)
        self.markersBtn.setObjectName(u"markersBtn")

        self.buttonsRow.addWidget(self.markersBtn)

        self.legendBtn = QPushButton(self.centralwidget)
        self.legendBtn.setObjectName(u"legendBtn")

        self.buttonsRow.addWidget(self.legendBtn)

        self.ringLabelsBtn = QPushButton(self.centralwidget)
        self.ringLabelsBtn.setObjectName(u"ringLabelsBtn")

        self.buttonsRow.addWidget(self.ringLabelsBtn)

        self.dropSeriesBtn = QPushButton(self.centralwidget)
        self.dropSeriesBtn.setObjectName(u"dropSeriesBtn")

        self.buttonsRow.addWidget(self.dropSeriesBtn)

        self.resetBtn = QPushButton(self.centralwidget)
        self.resetBtn.setObjectName(u"resetBtn")

        self.buttonsRow.addWidget(self.resetBtn)

        self.themeBtn = QPushButton(self.centralwidget)
        self.themeBtn.setObjectName(u"themeBtn")

        self.buttonsRow.addWidget(self.themeBtn)

        self.buttonsSpacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.buttonsRow.addItem(self.buttonsSpacer)


        self.verticalLayout.addLayout(self.buttonsRow)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"QCustomRadarChart", None))
        self.statusLabel.setText(QCoreApplication.translate("MainWindow", u"Hover a shape, or click near an axis", None))
        self.gridCaption.setText(QCoreApplication.translate("MainWindow", u"Grid", None))
        self.gridBox.setItemText(0, QCoreApplication.translate("MainWindow", u"polygon", None))
        self.gridBox.setItemText(1, QCoreApplication.translate("MainWindow", u"circle", None))

        self.ringsCaption.setText(QCoreApplication.translate("MainWindow", u"Rings", None))
        self.fillCaption.setText(QCoreApplication.translate("MainWindow", u"Fill", None))
        self.rotateCaption.setText(QCoreApplication.translate("MainWindow", u"Rotate", None))
        self.markersBtn.setText(QCoreApplication.translate("MainWindow", u"Markers", None))
        self.legendBtn.setText(QCoreApplication.translate("MainWindow", u"Legend", None))
        self.ringLabelsBtn.setText(QCoreApplication.translate("MainWindow", u"Ring labels", None))
        self.dropSeriesBtn.setText(QCoreApplication.translate("MainWindow", u"Drop Gamma", None))
        self.resetBtn.setText(QCoreApplication.translate("MainWindow", u"Reset", None))
        self.themeBtn.setText(QCoreApplication.translate("MainWindow", u"Light / dark", None))
    # retranslateUi

