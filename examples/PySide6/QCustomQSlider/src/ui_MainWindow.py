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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QMainWindow, QPushButton, QSizePolicy, QVBoxLayout,
    QWidget)

from Custom_Widgets.QCustomQSlider import QCustomQSlider
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(700, 500)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.titleLabel = QLabel(self.centralwidget)
        self.titleLabel.setObjectName(u"titleLabel")

        self.verticalLayout.addWidget(self.titleLabel)

        self.card1 = QFrame(self.centralwidget)
        self.card1.setObjectName(u"card1")
        self.card1.setFrameShape(QFrame.StyledPanel)
        self.card1Layout = QVBoxLayout(self.card1)
        self.card1Layout.setSpacing(0)
        self.card1Layout.setObjectName(u"card1Layout")
        self.section1Title = QLabel(self.card1)
        self.section1Title.setObjectName(u"section1Title")

        self.card1Layout.addWidget(self.section1Title)

        self.hSliderRow1 = QHBoxLayout()
        self.hSliderRow1.setObjectName(u"hSliderRow1")
        self.labelVolume = QLabel(self.card1)
        self.labelVolume.setObjectName(u"labelVolume")

        self.hSliderRow1.addWidget(self.labelVolume)

        self.volumeSlider = QCustomQSlider(self.card1)
        self.volumeSlider.setObjectName(u"volumeSlider")
        self.volumeSlider.setProperty(u"value", 65)
        self.volumeSlider.setOrientation(Qt.Horizontal)

        self.hSliderRow1.addWidget(self.volumeSlider)

        self.volumeValue = QLabel(self.card1)
        self.volumeValue.setObjectName(u"volumeValue")

        self.hSliderRow1.addWidget(self.volumeValue)


        self.card1Layout.addLayout(self.hSliderRow1)

        self.hSliderRow2 = QHBoxLayout()
        self.hSliderRow2.setObjectName(u"hSliderRow2")
        self.labelBrightness = QLabel(self.card1)
        self.labelBrightness.setObjectName(u"labelBrightness")

        self.hSliderRow2.addWidget(self.labelBrightness)

        self.brightnessSlider = QCustomQSlider(self.card1)
        self.brightnessSlider.setObjectName(u"brightnessSlider")
        self.brightnessSlider.setProperty(u"value", 85)
        self.brightnessSlider.setOrientation(Qt.Horizontal)

        self.hSliderRow2.addWidget(self.brightnessSlider)

        self.brightnessValue = QLabel(self.card1)
        self.brightnessValue.setObjectName(u"brightnessValue")

        self.hSliderRow2.addWidget(self.brightnessValue)


        self.card1Layout.addLayout(self.hSliderRow2)

        self.hSliderRow3 = QHBoxLayout()
        self.hSliderRow3.setObjectName(u"hSliderRow3")
        self.labelTemperature = QLabel(self.card1)
        self.labelTemperature.setObjectName(u"labelTemperature")

        self.hSliderRow3.addWidget(self.labelTemperature)

        self.tempSlider = QCustomQSlider(self.card1)
        self.tempSlider.setObjectName(u"tempSlider")
        self.tempSlider.setProperty(u"value", 42)
        self.tempSlider.setOrientation(Qt.Horizontal)

        self.hSliderRow3.addWidget(self.tempSlider)

        self.tempValue = QLabel(self.card1)
        self.tempValue.setObjectName(u"tempValue")

        self.hSliderRow3.addWidget(self.tempValue)


        self.card1Layout.addLayout(self.hSliderRow3)


        self.verticalLayout.addWidget(self.card1)

        self.card2 = QFrame(self.centralwidget)
        self.card2.setObjectName(u"card2")
        self.card2.setFrameShape(QFrame.StyledPanel)
        self.card2Layout = QHBoxLayout(self.card2)
        self.card2Layout.setSpacing(0)
        self.card2Layout.setObjectName(u"card2Layout")
        self.verticalSlider1 = QCustomQSlider(self.card2)
        self.verticalSlider1.setObjectName(u"verticalSlider1")
        self.verticalSlider1.setProperty(u"value", 50)
        self.verticalSlider1.setOrientation(Qt.Vertical)

        self.card2Layout.addWidget(self.verticalSlider1)

        self.verticalSlider2 = QCustomQSlider(self.card2)
        self.verticalSlider2.setObjectName(u"verticalSlider2")
        self.verticalSlider2.setProperty(u"value", 75)
        self.verticalSlider2.setOrientation(Qt.Vertical)

        self.card2Layout.addWidget(self.verticalSlider2)

        self.verticalSlider3 = QCustomQSlider(self.card2)
        self.verticalSlider3.setObjectName(u"verticalSlider3")
        self.verticalSlider3.setProperty(u"value", 25)
        self.verticalSlider3.setOrientation(Qt.Vertical)

        self.card2Layout.addWidget(self.verticalSlider3)

        self.verticalSlider4 = QCustomQSlider(self.card2)
        self.verticalSlider4.setObjectName(u"verticalSlider4")
        self.verticalSlider4.setProperty(u"value", 90)
        self.verticalSlider4.setOrientation(Qt.Vertical)

        self.card2Layout.addWidget(self.verticalSlider4)

        self.verticalSlider5 = QCustomQSlider(self.card2)
        self.verticalSlider5.setObjectName(u"verticalSlider5")
        self.verticalSlider5.setProperty(u"value", 10)
        self.verticalSlider5.setOrientation(Qt.Vertical)

        self.card2Layout.addWidget(self.verticalSlider5)


        self.verticalLayout.addWidget(self.card2)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"QCustomQSlider Showcase", None))
        self.titleLabel.setText(QCoreApplication.translate("MainWindow", u"Slider Showcase", None))
        self.section1Title.setText(QCoreApplication.translate("MainWindow", u"Horizontal Sliders", None))
        self.labelVolume.setText(QCoreApplication.translate("MainWindow", u"Volume", None))
        self.volumeValue.setText(QCoreApplication.translate("MainWindow", u"65", None))
        self.labelBrightness.setText(QCoreApplication.translate("MainWindow", u"Brightness", None))
        self.brightnessValue.setText(QCoreApplication.translate("MainWindow", u"85%", None))
        self.labelTemperature.setText(QCoreApplication.translate("MainWindow", u"Temperature", None))
        self.tempValue.setText(QCoreApplication.translate("MainWindow", u"42\u00b0", None))
    # retranslateUi

