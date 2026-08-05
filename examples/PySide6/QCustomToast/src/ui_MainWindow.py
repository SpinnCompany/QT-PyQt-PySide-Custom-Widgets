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
from PySide6.QtWidgets import (QApplication, QComboBox, QGridLayout, QHBoxLayout,
    QLabel, QMainWindow, QPushButton, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

from Custom_Widgets.QCustomQPushButton import QCustomQPushButton
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(560, 360)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.rootLayout = QVBoxLayout(self.centralwidget)
        self.rootLayout.setSpacing(14)
        self.rootLayout.setObjectName(u"rootLayout")
        self.rootLayout.setContentsMargins(20, 20, 20, 20)
        self.cornerRow = QHBoxLayout()
        self.cornerRow.setSpacing(10)
        self.cornerRow.setObjectName(u"cornerRow")
        self.cornerLabel = QLabel(self.centralwidget)
        self.cornerLabel.setObjectName(u"cornerLabel")

        self.cornerRow.addWidget(self.cornerLabel)

        self.pos = QComboBox(self.centralwidget)
        self.pos.addItem("")
        self.pos.addItem("")
        self.pos.addItem("")
        self.pos.addItem("")
        self.pos.addItem("")
        self.pos.addItem("")
        self.pos.setObjectName(u"pos")

        self.cornerRow.addWidget(self.pos)

        self.cornerSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.cornerRow.addItem(self.cornerSpacer)


        self.rootLayout.addLayout(self.cornerRow)

        self.buttonGrid = QGridLayout()
        self.buttonGrid.setObjectName(u"buttonGrid")
        self.buttonGrid.setHorizontalSpacing(10)
        self.buttonGrid.setVerticalSpacing(10)
        self.successBtn = QCustomQPushButton(self.centralwidget)
        self.successBtn.setObjectName(u"successBtn")

        self.buttonGrid.addWidget(self.successBtn, 0, 0, 1, 1)

        self.errorBtn = QCustomQPushButton(self.centralwidget)
        self.errorBtn.setObjectName(u"errorBtn")

        self.buttonGrid.addWidget(self.errorBtn, 0, 1, 1, 1)

        self.warningBtn = QCustomQPushButton(self.centralwidget)
        self.warningBtn.setObjectName(u"warningBtn")

        self.buttonGrid.addWidget(self.warningBtn, 1, 0, 1, 1)

        self.infoBtn = QCustomQPushButton(self.centralwidget)
        self.infoBtn.setObjectName(u"infoBtn")

        self.buttonGrid.addWidget(self.infoBtn, 1, 1, 1, 1)


        self.rootLayout.addLayout(self.buttonGrid)

        self.bottomSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.rootLayout.addItem(self.bottomSpacer)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"QCustomToast Example", None))
        self.cornerLabel.setText(QCoreApplication.translate("MainWindow", u"Corner:", None))
        self.pos.setItemText(0, QCoreApplication.translate("MainWindow", u"top-right", None))
        self.pos.setItemText(1, QCoreApplication.translate("MainWindow", u"top-left", None))
        self.pos.setItemText(2, QCoreApplication.translate("MainWindow", u"bottom-right", None))
        self.pos.setItemText(3, QCoreApplication.translate("MainWindow", u"bottom-left", None))
        self.pos.setItemText(4, QCoreApplication.translate("MainWindow", u"top-center", None))
        self.pos.setItemText(5, QCoreApplication.translate("MainWindow", u"bottom-center", None))

        self.successBtn.setText(QCoreApplication.translate("MainWindow", u"Success", None))
        self.successBtn.setProperty(u"variant", QCoreApplication.translate("MainWindow", u"success", None))
        self.errorBtn.setText(QCoreApplication.translate("MainWindow", u"Error", None))
        self.errorBtn.setProperty(u"variant", QCoreApplication.translate("MainWindow", u"secondary", None))
        self.warningBtn.setText(QCoreApplication.translate("MainWindow", u"Warning", None))
        self.warningBtn.setProperty(u"variant", QCoreApplication.translate("MainWindow", u"secondary", None))
        self.infoBtn.setText(QCoreApplication.translate("MainWindow", u"Info", None))
        self.infoBtn.setProperty(u"variant", QCoreApplication.translate("MainWindow", u"primary", None))
    # retranslateUi

