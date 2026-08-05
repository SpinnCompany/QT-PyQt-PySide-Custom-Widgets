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
    QVBoxLayout, QWidget)

from Custom_Widgets.QCustomRadialBars import QCustomRadialBars
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(560, 620)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.radialBars = QCustomRadialBars(self.centralwidget)
        self.radialBars.setObjectName(u"radialBars")
        self.radialBars.setMinimumSize(QSize(0, 340))

        self.verticalLayout.addWidget(self.radialBars)

        self.controlsRow = QHBoxLayout()
        self.controlsRow.setObjectName(u"controlsRow")
        self.thicknessCaption = QLabel(self.centralwidget)
        self.thicknessCaption.setObjectName(u"thicknessCaption")

        self.controlsRow.addWidget(self.thicknessCaption)

        self.thicknessSlider = QSlider(self.centralwidget)
        self.thicknessSlider.setObjectName(u"thicknessSlider")
        self.thicknessSlider.setMinimum(4)
        self.thicknessSlider.setMaximum(40)
        self.thicknessSlider.setValue(18)
        self.thicknessSlider.setOrientation(Qt.Horizontal)

        self.controlsRow.addWidget(self.thicknessSlider)

        self.startCaption = QLabel(self.centralwidget)
        self.startCaption.setObjectName(u"startCaption")

        self.controlsRow.addWidget(self.startCaption)

        self.startSlider = QSlider(self.centralwidget)
        self.startSlider.setObjectName(u"startSlider")
        self.startSlider.setMaximum(359)
        self.startSlider.setValue(90)
        self.startSlider.setOrientation(Qt.Horizontal)

        self.controlsRow.addWidget(self.startSlider)

        self.roundedBtn = QPushButton(self.centralwidget)
        self.roundedBtn.setObjectName(u"roundedBtn")

        self.controlsRow.addWidget(self.roundedBtn)

        self.trackBtn = QPushButton(self.centralwidget)
        self.trackBtn.setObjectName(u"trackBtn")

        self.controlsRow.addWidget(self.trackBtn)

        self.clockwiseBtn = QPushButton(self.centralwidget)
        self.clockwiseBtn.setObjectName(u"clockwiseBtn")

        self.controlsRow.addWidget(self.clockwiseBtn)

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
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"QCustomRadialBars", None))
        self.thicknessCaption.setText(QCoreApplication.translate("MainWindow", u"Thickness", None))
        self.startCaption.setText(QCoreApplication.translate("MainWindow", u"Start", None))
        self.roundedBtn.setText(QCoreApplication.translate("MainWindow", u"Rounded", None))
        self.trackBtn.setText(QCoreApplication.translate("MainWindow", u"Track", None))
        self.clockwiseBtn.setText(QCoreApplication.translate("MainWindow", u"Clockwise", None))
        self.themeBtn.setText(QCoreApplication.translate("MainWindow", u"Light / dark", None))
        self.statusLabel.setText(QCoreApplication.translate("MainWindow", u"Hover a ring", None))
    # retranslateUi

