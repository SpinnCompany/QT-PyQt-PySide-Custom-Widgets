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

from Custom_Widgets.QCustomSankey import QCustomSankey
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(720, 560)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.mainLayout = QVBoxLayout(self.centralwidget)
        self.mainLayout.setSpacing(14)
        self.mainLayout.setObjectName(u"mainLayout")
        self.mainLayout.setContentsMargins(20, 20, 20, 20)
        self.chart = QCustomSankey(self.centralwidget)
        self.chart.setObjectName(u"chart")
        self.chart.setMinimumSize(QSize(0, 360))
        self.chart.setProperty(u"linksCsv", u"Search>Signup=120;Social>Signup=80;Referral>Signup=45;Signup>Trial=150;Signup>Bounce=95;Trial>Paid=70;Trial>Churn=80")

        self.mainLayout.addWidget(self.chart)

        self.controlsRow = QHBoxLayout()
        self.controlsRow.setSpacing(10)
        self.controlsRow.setObjectName(u"controlsRow")
        self.curveLabel = QLabel(self.centralwidget)
        self.curveLabel.setObjectName(u"curveLabel")

        self.controlsRow.addWidget(self.curveLabel)

        self.curveSlider = QSlider(self.centralwidget)
        self.curveSlider.setObjectName(u"curveSlider")
        self.curveSlider.setMinimum(0)
        self.curveSlider.setMaximum(100)
        self.curveSlider.setValue(50)
        self.curveSlider.setOrientation(Qt.Horizontal)

        self.controlsRow.addWidget(self.curveSlider)

        self.ribbonLabel = QLabel(self.centralwidget)
        self.ribbonLabel.setObjectName(u"ribbonLabel")

        self.controlsRow.addWidget(self.ribbonLabel)

        self.ribbonSlider = QSlider(self.centralwidget)
        self.ribbonSlider.setObjectName(u"ribbonSlider")
        self.ribbonSlider.setMinimum(5)
        self.ribbonSlider.setMaximum(100)
        self.ribbonSlider.setValue(40)
        self.ribbonSlider.setOrientation(Qt.Horizontal)

        self.controlsRow.addWidget(self.ribbonSlider)

        self.valuesButton = QPushButton(self.centralwidget)
        self.valuesButton.setObjectName(u"valuesButton")
        self.valuesButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.controlsRow.addWidget(self.valuesButton)

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
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"QCustomSankey", None))
        self.curveLabel.setText(QCoreApplication.translate("MainWindow", u"Curve", None))
        self.ribbonLabel.setText(QCoreApplication.translate("MainWindow", u"Ribbon", None))
        self.valuesButton.setText(QCoreApplication.translate("MainWindow", u"Values", None))
        self.themeButton.setText(QCoreApplication.translate("MainWindow", u"Light / dark", None))
        self.statusLabel.setText(QCoreApplication.translate("MainWindow", u"Hover a node or a ribbon", None))
    # retranslateUi

