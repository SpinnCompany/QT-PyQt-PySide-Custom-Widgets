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

from Custom_Widgets.QCustomGradientPicker import QCustomGradientPicker
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(560, 480)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.mainLayout = QVBoxLayout(self.centralwidget)
        self.mainLayout.setSpacing(16)
        self.mainLayout.setObjectName(u"mainLayout")
        self.mainLayout.setContentsMargins(24, 24, 24, 24)
        self.headingLabel = QLabel(self.centralwidget)
        self.headingLabel.setObjectName(u"headingLabel")

        self.mainLayout.addWidget(self.headingLabel)

        self.gradientPicker = QCustomGradientPicker(self.centralwidget)
        self.gradientPicker.setObjectName(u"gradientPicker")

        self.mainLayout.addWidget(self.gradientPicker)

        self.previewHolder = QWidget(self.centralwidget)
        self.previewHolder.setObjectName(u"previewHolder")
        self.previewHolder.setMinimumSize(QSize(0, 160))
        self.previewLayout = QVBoxLayout(self.previewHolder)
        self.previewLayout.setSpacing(0)
        self.previewLayout.setObjectName(u"previewLayout")
        self.previewLayout.setContentsMargins(0, 0, 0, 0)

        self.mainLayout.addWidget(self.previewHolder)

        self.controlsRow = QHBoxLayout()
        self.controlsRow.setSpacing(8)
        self.controlsRow.setObjectName(u"controlsRow")
        self.typeCaption = QLabel(self.centralwidget)
        self.typeCaption.setObjectName(u"typeCaption")

        self.controlsRow.addWidget(self.typeCaption)

        self.typeBox = QComboBox(self.centralwidget)
        self.typeBox.addItem("")
        self.typeBox.addItem("")
        self.typeBox.setObjectName(u"typeBox")

        self.controlsRow.addWidget(self.typeBox)

        self.angleCaption = QLabel(self.centralwidget)
        self.angleCaption.setObjectName(u"angleCaption")

        self.controlsRow.addWidget(self.angleCaption)

        self.angleSlider = QSlider(self.centralwidget)
        self.angleSlider.setObjectName(u"angleSlider")
        self.angleSlider.setMaximum(359)
        self.angleSlider.setOrientation(Qt.Horizontal)

        self.controlsRow.addWidget(self.angleSlider)

        self.editStopBtn = QPushButton(self.centralwidget)
        self.editStopBtn.setObjectName(u"editStopBtn")

        self.controlsRow.addWidget(self.editStopBtn)

        self.themeBtn = QPushButton(self.centralwidget)
        self.themeBtn.setObjectName(u"themeBtn")

        self.controlsRow.addWidget(self.themeBtn)

        self.controlsRow.setStretch(3, 1)

        self.mainLayout.addLayout(self.controlsRow)

        self.presetsRow = QHBoxLayout()
        self.presetsRow.setSpacing(8)
        self.presetsRow.setObjectName(u"presetsRow")
        self.presetSunset = QPushButton(self.centralwidget)
        self.presetSunset.setObjectName(u"presetSunset")

        self.presetsRow.addWidget(self.presetSunset)

        self.presetOcean = QPushButton(self.centralwidget)
        self.presetOcean.setObjectName(u"presetOcean")

        self.presetsRow.addWidget(self.presetOcean)

        self.presetFade = QPushButton(self.centralwidget)
        self.presetFade.setObjectName(u"presetFade")

        self.presetsRow.addWidget(self.presetFade)

        self.presetsSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.presetsRow.addItem(self.presetsSpacer)


        self.mainLayout.addLayout(self.presetsRow)

        self.statusLabel = QLabel(self.centralwidget)
        self.statusLabel.setObjectName(u"statusLabel")

        self.mainLayout.addWidget(self.statusLabel)

        self.mainLayout.setStretch(2, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"QCustomGradientPicker", None))
        self.headingLabel.setText(QCoreApplication.translate("MainWindow", u"Gradient", None))
        self.typeCaption.setText(QCoreApplication.translate("MainWindow", u"Type", None))
        self.typeBox.setItemText(0, QCoreApplication.translate("MainWindow", u"linear", None))
        self.typeBox.setItemText(1, QCoreApplication.translate("MainWindow", u"radial", None))

        self.angleCaption.setText(QCoreApplication.translate("MainWindow", u"Angle", None))
        self.editStopBtn.setText(QCoreApplication.translate("MainWindow", u"Edit selected stop", None))
        self.themeBtn.setText(QCoreApplication.translate("MainWindow", u"Light / dark", None))
        self.presetSunset.setText(QCoreApplication.translate("MainWindow", u"Sunset", None))
        self.presetOcean.setText(QCoreApplication.translate("MainWindow", u"Ocean", None))
        self.presetFade.setText(QCoreApplication.translate("MainWindow", u"Fade", None))
        self.statusLabel.setText(QCoreApplication.translate("MainWindow", u"-", None))
    # retranslateUi

