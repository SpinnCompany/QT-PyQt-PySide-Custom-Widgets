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

from Custom_Widgets.QCustomImagePicker import QCustomImagePicker
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(640, 480)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(16)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(24, 24, 24, 24)
        self.topRow = QHBoxLayout()
        self.topRow.setSpacing(20)
        self.topRow.setObjectName(u"topRow")
        self.avatarBox = QVBoxLayout()
        self.avatarBox.setObjectName(u"avatarBox")
        self.avatarHeading = QLabel(self.centralwidget)
        self.avatarHeading.setObjectName(u"avatarHeading")
        font = QFont()
        font.setBold(True)
        self.avatarHeading.setFont(font)

        self.avatarBox.addWidget(self.avatarHeading)

        self.avatarPicker = QCustomImagePicker(self.centralwidget)
        self.avatarPicker.setObjectName(u"avatarPicker")
        self.avatarPicker.setMinimumSize(QSize(130, 130))
        self.avatarPicker.setMaximumSize(QSize(130, 130))

        self.avatarBox.addWidget(self.avatarPicker)

        self.avatarSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.avatarBox.addItem(self.avatarSpacer)


        self.topRow.addLayout(self.avatarBox)

        self.coverBox = QVBoxLayout()
        self.coverBox.setObjectName(u"coverBox")
        self.coverHeading = QLabel(self.centralwidget)
        self.coverHeading.setObjectName(u"coverHeading")
        self.coverHeading.setFont(font)

        self.coverBox.addWidget(self.coverHeading)

        self.coverPicker = QCustomImagePicker(self.centralwidget)
        self.coverPicker.setObjectName(u"coverPicker")
        self.coverPicker.setMinimumSize(QSize(0, 130))

        self.coverBox.addWidget(self.coverPicker)

        self.containPicker = QCustomImagePicker(self.centralwidget)
        self.containPicker.setObjectName(u"containPicker")
        self.containPicker.setMinimumSize(QSize(0, 130))

        self.coverBox.addWidget(self.containPicker)


        self.topRow.addLayout(self.coverBox)

        self.topRow.setStretch(1, 1)

        self.verticalLayout.addLayout(self.topRow)

        self.controlsRow = QHBoxLayout()
        self.controlsRow.setObjectName(u"controlsRow")
        self.browseButton = QPushButton(self.centralwidget)
        self.browseButton.setObjectName(u"browseButton")

        self.controlsRow.addWidget(self.browseButton)

        self.clearButton = QPushButton(self.centralwidget)
        self.clearButton.setObjectName(u"clearButton")

        self.controlsRow.addWidget(self.clearButton)

        self.themeButton = QPushButton(self.centralwidget)
        self.themeButton.setObjectName(u"themeButton")

        self.controlsRow.addWidget(self.themeButton)

        self.controlsSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.controlsRow.addItem(self.controlsSpacer)


        self.verticalLayout.addLayout(self.controlsRow)

        self.statusLabel = QLabel(self.centralwidget)
        self.statusLabel.setObjectName(u"statusLabel")

        self.verticalLayout.addWidget(self.statusLabel)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"QCustomImagePicker", None))
        self.avatarHeading.setText(QCoreApplication.translate("MainWindow", u"Avatar", None))
        self.avatarPicker.setProperty(u"placeholderText", QCoreApplication.translate("MainWindow", u"Drop a photo", None))
        self.avatarPicker.setProperty(u"shape", QCoreApplication.translate("MainWindow", u"circle", None))
        self.coverHeading.setText(QCoreApplication.translate("MainWindow", u"Cover (cover / contain)", None))
        self.coverPicker.setProperty(u"placeholderText", QCoreApplication.translate("MainWindow", u"Drop a wide image", None))
        self.containPicker.setProperty(u"placeholderText", QCoreApplication.translate("MainWindow", u"same image, contain", None))
        self.containPicker.setProperty(u"fitMode", QCoreApplication.translate("MainWindow", u"contain", None))
        self.browseButton.setText(QCoreApplication.translate("MainWindow", u"Browse avatar", None))
        self.clearButton.setText(QCoreApplication.translate("MainWindow", u"Clear all", None))
        self.themeButton.setText(QCoreApplication.translate("MainWindow", u"Light / dark", None))
        self.statusLabel.setText(QCoreApplication.translate("MainWindow", u"Drop an image, or click a field to browse. Non-images and files over 5 MB are refused.", None))
    # retranslateUi

