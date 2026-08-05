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
    QMainWindow, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

from Custom_Widgets.QCustomHeaderNav import QCustomHeaderNav
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(720, 320)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(16)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(24, 24, 24, 24)
        self.headerNav = QCustomHeaderNav(self.centralwidget)
        self.headerNav.setObjectName(u"headerNav")

        self.verticalLayout.addWidget(self.headerNav)

        self.statusLabel = QLabel(self.centralwidget)
        self.statusLabel.setObjectName(u"statusLabel")

        self.verticalLayout.addWidget(self.statusLabel)

        self.controlsRow = QHBoxLayout()
        self.controlsRow.setObjectName(u"controlsRow")
        self.indicatorLabel = QLabel(self.centralwidget)
        self.indicatorLabel.setObjectName(u"indicatorLabel")

        self.controlsRow.addWidget(self.indicatorLabel)

        self.indicatorCombo = QComboBox(self.centralwidget)
        self.indicatorCombo.addItem("")
        self.indicatorCombo.addItem("")
        self.indicatorCombo.addItem("")
        self.indicatorCombo.setObjectName(u"indicatorCombo")

        self.controlsRow.addWidget(self.indicatorCombo)

        self.alignLabel = QLabel(self.centralwidget)
        self.alignLabel.setObjectName(u"alignLabel")

        self.controlsRow.addWidget(self.alignLabel)

        self.alignCombo = QComboBox(self.centralwidget)
        self.alignCombo.addItem("")
        self.alignCombo.addItem("")
        self.alignCombo.addItem("")
        self.alignCombo.setObjectName(u"alignCombo")

        self.controlsRow.addWidget(self.alignCombo)

        self.themeButton = QPushButton(self.centralwidget)
        self.themeButton.setObjectName(u"themeButton")

        self.controlsRow.addWidget(self.themeButton)

        self.controlsSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.controlsRow.addItem(self.controlsSpacer)


        self.verticalLayout.addLayout(self.controlsRow)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"QCustomHeaderNav", None))
        self.headerNav.setProperty(u"itemsCsv", QCoreApplication.translate("MainWindow", u"home=Home,docs=Docs,pricing=Pricing,blog=Blog,changelog=Changelog", None))
        self.headerNav.setProperty(u"brandText", QCoreApplication.translate("MainWindow", u"Spinn UI", None))
        self.statusLabel.setText(QCoreApplication.translate("MainWindow", u"selected home", None))
        self.indicatorLabel.setText(QCoreApplication.translate("MainWindow", u"Indicator", None))
        self.indicatorCombo.setItemText(0, QCoreApplication.translate("MainWindow", u"underline", None))
        self.indicatorCombo.setItemText(1, QCoreApplication.translate("MainWindow", u"pill", None))
        self.indicatorCombo.setItemText(2, QCoreApplication.translate("MainWindow", u"none", None))

        self.alignLabel.setText(QCoreApplication.translate("MainWindow", u"Align", None))
        self.alignCombo.setItemText(0, QCoreApplication.translate("MainWindow", u"left", None))
        self.alignCombo.setItemText(1, QCoreApplication.translate("MainWindow", u"center", None))
        self.alignCombo.setItemText(2, QCoreApplication.translate("MainWindow", u"right", None))

        self.themeButton.setText(QCoreApplication.translate("MainWindow", u"Light / dark", None))
    # retranslateUi

