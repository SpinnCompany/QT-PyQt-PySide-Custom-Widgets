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

from Custom_Widgets.QCustomForm import QCustomForm
from Custom_Widgets.QCustomQPushButton import QCustomQPushButton
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(760, 560)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.mainLayout = QVBoxLayout(self.centralwidget)
        self.mainLayout.setSpacing(14)
        self.mainLayout.setObjectName(u"mainLayout")
        self.mainLayout.setContentsMargins(24, 24, 24, 24)
        self.titleLabel = QLabel(self.centralwidget)
        self.titleLabel.setObjectName(u"titleLabel")

        self.mainLayout.addWidget(self.titleLabel)

        self.signupForm = QCustomForm(self.centralwidget)
        self.signupForm.setObjectName(u"signupForm")

        self.mainLayout.addWidget(self.signupForm)

        self.prefLabel = QLabel(self.centralwidget)
        self.prefLabel.setObjectName(u"prefLabel")

        self.mainLayout.addWidget(self.prefLabel)

        self.prefsHolder = QHBoxLayout()
        self.prefsHolder.setObjectName(u"prefsHolder")

        self.mainLayout.addLayout(self.prefsHolder)

        self.submitButton = QCustomQPushButton(self.centralwidget)
        self.submitButton.setObjectName(u"submitButton")

        self.mainLayout.addWidget(self.submitButton)

        self.bottomSpacer = QSpacerItem(10, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.mainLayout.addItem(self.bottomSpacer)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Custom Widgets Release Starter", None))
        self.titleLabel.setText(QCoreApplication.translate("MainWindow", u"Release-ready starter app", None))
        self.prefLabel.setText(QCoreApplication.translate("MainWindow", u"Preference", None))
        self.submitButton.setText(QCoreApplication.translate("MainWindow", u"Submit sample", None))
    # retranslateUi

