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

from Custom_Widgets.QCustomVerificationCode import QCustomVerificationCode
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(480, 520)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.mainLayout = QVBoxLayout(self.centralwidget)
        self.mainLayout.setSpacing(18)
        self.mainLayout.setObjectName(u"mainLayout")
        self.mainLayout.setContentsMargins(28, 28, 28, 28)
        self.mainHeading = QLabel(self.centralwidget)
        self.mainHeading.setObjectName(u"mainHeading")

        self.mainLayout.addWidget(self.mainHeading)

        self.hintLabel = QLabel(self.centralwidget)
        self.hintLabel.setObjectName(u"hintLabel")

        self.mainLayout.addWidget(self.hintLabel)

        self.codeInput = QCustomVerificationCode(self.centralwidget)
        self.codeInput.setObjectName(u"codeInput")
        self.codeInput.setProperty(u"digits", 6)

        self.mainLayout.addWidget(self.codeInput)

        self.groupedHeading = QLabel(self.centralwidget)
        self.groupedHeading.setObjectName(u"groupedHeading")

        self.mainLayout.addWidget(self.groupedHeading)

        self.groupedInput = QCustomVerificationCode(self.centralwidget)
        self.groupedInput.setObjectName(u"groupedInput")
        self.groupedInput.setProperty(u"digits", 6)
        self.groupedInput.setProperty(u"separatorAfter", 3)

        self.mainLayout.addWidget(self.groupedInput)

        self.maskedHeading = QLabel(self.centralwidget)
        self.maskedHeading.setObjectName(u"maskedHeading")

        self.mainLayout.addWidget(self.maskedHeading)

        self.maskedInput = QCustomVerificationCode(self.centralwidget)
        self.maskedInput.setObjectName(u"maskedInput")
        self.maskedInput.setProperty(u"digits", 8)
        self.maskedInput.setProperty(u"masked", True)
        self.maskedInput.setProperty(u"boxWidth", 34)

        self.mainLayout.addWidget(self.maskedInput)

        self.buttonRow = QHBoxLayout()
        self.buttonRow.setSpacing(8)
        self.buttonRow.setObjectName(u"buttonRow")
        self.clearButton = QPushButton(self.centralwidget)
        self.clearButton.setObjectName(u"clearButton")

        self.buttonRow.addWidget(self.clearButton)

        self.pasteButton = QPushButton(self.centralwidget)
        self.pasteButton.setObjectName(u"pasteButton")

        self.buttonRow.addWidget(self.pasteButton)

        self.themeButton = QPushButton(self.centralwidget)
        self.themeButton.setObjectName(u"themeButton")

        self.buttonRow.addWidget(self.themeButton)

        self.buttonSpacer = QSpacerItem(10, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.buttonRow.addItem(self.buttonSpacer)


        self.mainLayout.addLayout(self.buttonRow)

        self.statusLabel = QLabel(self.centralwidget)
        self.statusLabel.setObjectName(u"statusLabel")

        self.mainLayout.addWidget(self.statusLabel)

        self.bottomSpacer = QSpacerItem(10, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.mainLayout.addItem(self.bottomSpacer)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"QCustomVerificationCode", None))
        self.mainHeading.setText(QCoreApplication.translate("MainWindow", u"Enter the 6-digit code we emailed you", None))
        self.hintLabel.setText(QCoreApplication.translate("MainWindow", u"(the demo accepts 123456)", None))
        self.groupedHeading.setText(QCoreApplication.translate("MainWindow", u"Grouped 3 + 3", None))
        self.maskedHeading.setText(QCoreApplication.translate("MainWindow", u"Masked, alphanumeric, 8 characters", None))
        self.maskedInput.setProperty(u"inputMode", QCoreApplication.translate("MainWindow", u"alphanumeric", None))
        self.clearButton.setText(QCoreApplication.translate("MainWindow", u"Clear", None))
        self.pasteButton.setText(QCoreApplication.translate("MainWindow", u"Paste '123 456'", None))
        self.themeButton.setText(QCoreApplication.translate("MainWindow", u"Light / dark", None))
        self.statusLabel.setText(QCoreApplication.translate("MainWindow", u"Waiting for a code...", None))
    # retranslateUi

