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

from Custom_Widgets.QCustomAlert import QCustomAlert
from Custom_Widgets.QCustomNumberInput import QCustomNumberInput
from Custom_Widgets.QCustomSwitch import QCustomSwitch
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(460, 560)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.rootLayout = QVBoxLayout(self.centralwidget)
        self.rootLayout.setSpacing(12)
        self.rootLayout.setObjectName(u"rootLayout")
        self.rootLayout.setContentsMargins(14, 14, 14, 14)
        self.notifRow = QHBoxLayout()
        self.notifRow.setObjectName(u"notifRow")
        self.notifLabel = QLabel(self.centralwidget)
        self.notifLabel.setObjectName(u"notifLabel")

        self.notifRow.addWidget(self.notifLabel)

        self.notifSpacer = QSpacerItem(10, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.notifRow.addItem(self.notifSpacer)

        self.notifSwitch = QCustomSwitch(self.centralwidget)
        self.notifSwitch.setObjectName(u"notifSwitch")
        self.notifSwitch.setProperty(u"checked", True)

        self.notifRow.addWidget(self.notifSwitch)


        self.rootLayout.addLayout(self.notifRow)

        self.darkRow = QHBoxLayout()
        self.darkRow.setObjectName(u"darkRow")
        self.darkLabel = QLabel(self.centralwidget)
        self.darkLabel.setObjectName(u"darkLabel")

        self.darkRow.addWidget(self.darkLabel)

        self.darkSpacer = QSpacerItem(10, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.darkRow.addItem(self.darkSpacer)

        self.darkSwitch = QCustomSwitch(self.centralwidget)
        self.darkSwitch.setObjectName(u"darkSwitch")

        self.darkRow.addWidget(self.darkSwitch)


        self.rootLayout.addLayout(self.darkRow)

        self.qtyRow = QHBoxLayout()
        self.qtyRow.setObjectName(u"qtyRow")
        self.qtyLabel = QLabel(self.centralwidget)
        self.qtyLabel.setObjectName(u"qtyLabel")

        self.qtyRow.addWidget(self.qtyLabel)

        self.qtySpacer = QSpacerItem(10, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.qtyRow.addItem(self.qtySpacer)

        self.qtyInput = QCustomNumberInput(self.centralwidget)
        self.qtyInput.setObjectName(u"qtyInput")
        self.qtyInput.setMaximumSize(QSize(140, 16777215))

        self.qtyRow.addWidget(self.qtyInput)


        self.rootLayout.addLayout(self.qtyRow)

        self.priceRow = QHBoxLayout()
        self.priceRow.setObjectName(u"priceRow")
        self.priceLabel = QLabel(self.centralwidget)
        self.priceLabel.setObjectName(u"priceLabel")

        self.priceRow.addWidget(self.priceLabel)

        self.priceSpacer = QSpacerItem(10, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.priceRow.addItem(self.priceSpacer)

        self.priceInput = QCustomNumberInput(self.centralwidget)
        self.priceInput.setObjectName(u"priceInput")
        self.priceInput.setMaximumSize(QSize(140, 16777215))

        self.priceRow.addWidget(self.priceInput)


        self.rootLayout.addLayout(self.priceRow)

        self.alertInfo = QCustomAlert(self.centralwidget)
        self.alertInfo.setObjectName(u"alertInfo")

        self.rootLayout.addWidget(self.alertInfo)

        self.alertSuccess = QCustomAlert(self.centralwidget)
        self.alertSuccess.setObjectName(u"alertSuccess")

        self.rootLayout.addWidget(self.alertSuccess)

        self.alertWarning = QCustomAlert(self.centralwidget)
        self.alertWarning.setObjectName(u"alertWarning")
        self.alertWarning.setProperty(u"dismissible", True)

        self.rootLayout.addWidget(self.alertWarning)

        self.alertError = QCustomAlert(self.centralwidget)
        self.alertError.setObjectName(u"alertError")
        self.alertError.setProperty(u"dismissible", True)

        self.rootLayout.addWidget(self.alertError)

        self.bottomSpacer = QSpacerItem(10, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.rootLayout.addItem(self.bottomSpacer)

        self.statusLabel = QLabel(self.centralwidget)
        self.statusLabel.setObjectName(u"statusLabel")

        self.rootLayout.addWidget(self.statusLabel)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Switch / Number / Alert", None))
        self.notifLabel.setText(QCoreApplication.translate("MainWindow", u"Enable notifications", None))
        self.darkLabel.setText(QCoreApplication.translate("MainWindow", u"Dark mode", None))
        self.qtyLabel.setText(QCoreApplication.translate("MainWindow", u"Quantity", None))
        self.priceLabel.setText(QCoreApplication.translate("MainWindow", u"Unit price", None))
        self.alertInfo.setProperty(u"title", QCoreApplication.translate("MainWindow", u"Heads up", None))
        self.alertInfo.setProperty(u"text", QCoreApplication.translate("MainWindow", u"Your trial ends in 3 days.", None))
        self.alertInfo.setProperty(u"variant", QCoreApplication.translate("MainWindow", u"info", None))
        self.alertSuccess.setProperty(u"title", QCoreApplication.translate("MainWindow", u"Saved", None))
        self.alertSuccess.setProperty(u"text", QCoreApplication.translate("MainWindow", u"Settings updated successfully.", None))
        self.alertSuccess.setProperty(u"variant", QCoreApplication.translate("MainWindow", u"success", None))
        self.alertWarning.setProperty(u"title", QCoreApplication.translate("MainWindow", u"Careful", None))
        self.alertWarning.setProperty(u"text", QCoreApplication.translate("MainWindow", u"This action can't be undone.", None))
        self.alertWarning.setProperty(u"variant", QCoreApplication.translate("MainWindow", u"warning", None))
        self.alertError.setProperty(u"title", QCoreApplication.translate("MainWindow", u"Error", None))
        self.alertError.setProperty(u"text", QCoreApplication.translate("MainWindow", u"Payment failed. Try another card.", None))
        self.alertError.setProperty(u"variant", QCoreApplication.translate("MainWindow", u"destructive", None))
        self.statusLabel.setText(QCoreApplication.translate("MainWindow", u"-", None))
    # retranslateUi

