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
    QMainWindow, QPushButton, QScrollArea, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

from Custom_Widgets.QCustomAgendaList import QCustomAgendaList
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(820, 620)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.cardsRow = QHBoxLayout(self.centralwidget)
        self.cardsRow.setSpacing(20)
        self.cardsRow.setObjectName(u"cardsRow")
        self.cardsRow.setContentsMargins(24, 24, 24, 24)
        self.planCard = QFrame(self.centralwidget)
        self.planCard.setObjectName(u"planCard")
        self.planCard.setFrameShape(QFrame.NoFrame)
        self.planLayout = QVBoxLayout(self.planCard)
        self.planLayout.setSpacing(2)
        self.planLayout.setObjectName(u"planLayout")
        self.planLayout.setContentsMargins(20, 18, 12, 18)
        self.planTitle = QLabel(self.planCard)
        self.planTitle.setObjectName(u"planTitle")

        self.planLayout.addWidget(self.planTitle)

        self.planSub = QLabel(self.planCard)
        self.planSub.setObjectName(u"planSub")

        self.planLayout.addWidget(self.planSub)

        self.planSpacer = QSpacerItem(0, 8, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.planLayout.addItem(self.planSpacer)

        self.planScroll = QScrollArea(self.planCard)
        self.planScroll.setObjectName(u"planScroll")
        self.planScroll.setFrameShape(QFrame.NoFrame)
        self.planScroll.setWidgetResizable(True)
        self.planAgenda = QCustomAgendaList()
        self.planAgenda.setObjectName(u"planAgenda")
        self.planScroll.setWidget(self.planAgenda)

        self.planLayout.addWidget(self.planScroll)


        self.cardsRow.addWidget(self.planCard)

        self.meetCard = QFrame(self.centralwidget)
        self.meetCard.setObjectName(u"meetCard")
        self.meetCard.setFrameShape(QFrame.NoFrame)
        self.meetLayout = QVBoxLayout(self.meetCard)
        self.meetLayout.setSpacing(2)
        self.meetLayout.setObjectName(u"meetLayout")
        self.meetLayout.setContentsMargins(20, 18, 12, 18)
        self.meetTitle = QLabel(self.meetCard)
        self.meetTitle.setObjectName(u"meetTitle")

        self.meetLayout.addWidget(self.meetTitle)

        self.meetSub = QLabel(self.meetCard)
        self.meetSub.setObjectName(u"meetSub")

        self.meetLayout.addWidget(self.meetSub)

        self.meetSpacer = QSpacerItem(0, 8, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.meetLayout.addItem(self.meetSpacer)

        self.meetScroll = QScrollArea(self.meetCard)
        self.meetScroll.setObjectName(u"meetScroll")
        self.meetScroll.setFrameShape(QFrame.NoFrame)
        self.meetScroll.setWidgetResizable(True)
        self.meetAgenda = QCustomAgendaList()
        self.meetAgenda.setObjectName(u"meetAgenda")
        self.meetScroll.setWidget(self.meetAgenda)

        self.meetLayout.addWidget(self.meetScroll)


        self.cardsRow.addWidget(self.meetCard)

        self.cardsRow.setStretch(0, 1)
        self.cardsRow.setStretch(1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"QCustomAgendaList \u2014 preview", None))
        self.planTitle.setText(QCoreApplication.translate("MainWindow", u"Today's plan", None))
        self.planSub.setText(QCoreApplication.translate("MainWindow", u"4 activities", None))
        self.meetTitle.setText(QCoreApplication.translate("MainWindow", u"Meetings", None))
        self.meetSub.setText(QCoreApplication.translate("MainWindow", u"Wednesday, 24 Jul", None))
    # retranslateUi

