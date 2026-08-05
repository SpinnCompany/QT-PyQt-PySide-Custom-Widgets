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

from Custom_Widgets.QCustomQPushButton import QCustomQPushButton
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(640, 320)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.titleLabel = QLabel(self.centralwidget)
        self.titleLabel.setObjectName(u"titleLabel")

        self.verticalLayout.addWidget(self.titleLabel)

        self.subtitleLabel = QLabel(self.centralwidget)
        self.subtitleLabel.setObjectName(u"subtitleLabel")
        self.subtitleLabel.setWordWrap(True)

        self.verticalLayout.addWidget(self.subtitleLabel)

        self.buttonCard = QFrame(self.centralwidget)
        self.buttonCard.setObjectName(u"buttonCard")
        self.buttonCard.setFrameShape(QFrame.StyledPanel)
        self.buttonCardLayout = QHBoxLayout(self.buttonCard)
        self.buttonCardLayout.setSpacing(0)
        self.buttonCardLayout.setObjectName(u"buttonCardLayout")
        self.customThemeButton = QCustomQPushButton(self.buttonCard)
        self.customThemeButton.setObjectName(u"customThemeButton")
        self.customThemeButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon = QIcon()
        icon.addFile(u"theme-icons:icons/feather/settings.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.customThemeButton.setIcon(icon)
        self.customThemeButton.setIconSize(QSize(22, 22))

        self.buttonCardLayout.addWidget(self.customThemeButton)

        self.shadowThemeButton = QCustomQPushButton(self.buttonCard)
        self.shadowThemeButton.setObjectName(u"shadowThemeButton")
        self.shadowThemeButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon1 = QIcon()
        icon1.addFile(u"theme-icons:icons/feather/loader.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.shadowThemeButton.setIcon(icon1)
        self.shadowThemeButton.setIconSize(QSize(22, 22))

        self.buttonCardLayout.addWidget(self.shadowThemeButton)

        self.borderThemeButton = QCustomQPushButton(self.buttonCard)
        self.borderThemeButton.setObjectName(u"borderThemeButton")
        self.borderThemeButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon2 = QIcon()
        icon2.addFile(u"theme-icons:icons/feather/shopping-cart.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.borderThemeButton.setIcon(icon2)
        self.borderThemeButton.setIconSize(QSize(22, 22))

        self.buttonCardLayout.addWidget(self.borderThemeButton)


        self.verticalLayout.addWidget(self.buttonCard)

        self.hintLabel = QLabel(self.centralwidget)
        self.hintLabel.setObjectName(u"hintLabel")

        self.verticalLayout.addWidget(self.hintLabel)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"QCustomQPushButton Showcase", None))
        self.titleLabel.setText(QCoreApplication.translate("MainWindow", u"Animated Push Buttons", None))
        self.subtitleLabel.setText(QCoreApplication.translate("MainWindow", u"Themes, hover / click animations and animated shadows \u2014 styled from json-styles/style.json", None))
        self.customThemeButton.setText(QCoreApplication.translate("MainWindow", u"Custom Theme", None))
        self.shadowThemeButton.setText(QCoreApplication.translate("MainWindow", u"Click Shadow", None))
        self.borderThemeButton.setText(QCoreApplication.translate("MainWindow", u"Border Animation", None))
        self.hintLabel.setText(QCoreApplication.translate("MainWindow", u"Hover or click the buttons to play their animations.", None))
    # retranslateUi

