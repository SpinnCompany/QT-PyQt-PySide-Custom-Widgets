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
    QLineEdit, QMainWindow, QPushButton, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

from Custom_Widgets.QCustomBubbleChart import QCustomBubbleChart
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1040, 620)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.cardsRow = QHBoxLayout(self.centralwidget)
        self.cardsRow.setSpacing(20)
        self.cardsRow.setObjectName(u"cardsRow")
        self.cardsRow.setContentsMargins(24, 24, 24, 24)
        self.sentCard = QFrame(self.centralwidget)
        self.sentCard.setObjectName(u"sentCard")
        self.sentCard.setFrameShape(QFrame.NoFrame)
        self.sentLayout = QVBoxLayout(self.sentCard)
        self.sentLayout.setSpacing(10)
        self.sentLayout.setObjectName(u"sentLayout")
        self.sentLayout.setContentsMargins(20, 16, 20, 16)
        self.sentHead = QHBoxLayout()
        self.sentHead.setObjectName(u"sentHead")
        self.sentTitle = QLabel(self.sentCard)
        self.sentTitle.setObjectName(u"sentTitle")

        self.sentHead.addWidget(self.sentTitle)

        self.sentHeadSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.sentHead.addItem(self.sentHeadSpacer)

        self.sentSearch = QLineEdit(self.sentCard)
        self.sentSearch.setObjectName(u"sentSearch")
        self.sentSearch.setMaximumSize(QSize(180, 16777215))

        self.sentHead.addWidget(self.sentSearch)


        self.sentLayout.addLayout(self.sentHead)

        self.sentChart = QCustomBubbleChart(self.sentCard)
        self.sentChart.setObjectName(u"sentChart")
        self.sentChart.setProperty(u"groupByCategory", True)

        self.sentLayout.addWidget(self.sentChart)

        self.sentLayout.setStretch(1, 1)

        self.cardsRow.addWidget(self.sentCard)

        self.shareCard = QFrame(self.centralwidget)
        self.shareCard.setObjectName(u"shareCard")
        self.shareCard.setFrameShape(QFrame.NoFrame)
        self.shareLayout = QVBoxLayout(self.shareCard)
        self.shareLayout.setSpacing(10)
        self.shareLayout.setObjectName(u"shareLayout")
        self.shareLayout.setContentsMargins(20, 16, 20, 16)
        self.shareHead = QHBoxLayout()
        self.shareHead.setObjectName(u"shareHead")
        self.shareTitle = QLabel(self.shareCard)
        self.shareTitle.setObjectName(u"shareTitle")

        self.shareHead.addWidget(self.shareTitle)

        self.shareHeadSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.shareHead.addItem(self.shareHeadSpacer)

        self.shareSearch = QLineEdit(self.shareCard)
        self.shareSearch.setObjectName(u"shareSearch")
        self.shareSearch.setMaximumSize(QSize(180, 16777215))

        self.shareHead.addWidget(self.shareSearch)


        self.shareLayout.addLayout(self.shareHead)

        self.shareChart = QCustomBubbleChart(self.shareCard)
        self.shareChart.setObjectName(u"shareChart")
        self.shareChart.setProperty(u"minLabelRadius", 12.000000000000000)

        self.shareLayout.addWidget(self.shareChart)

        self.shareLayout.setStretch(1, 1)

        self.cardsRow.addWidget(self.shareCard)

        self.cardsRow.setStretch(0, 1)
        self.cardsRow.setStretch(1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"QCustomBubbleChart \u2014 preview", None))
        self.sentTitle.setText(QCoreApplication.translate("MainWindow", u"Customer sentiment", None))
        self.sentSearch.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Search\u2026", None))
        self.shareTitle.setText(QCoreApplication.translate("MainWindow", u"Browser share", None))
        self.shareSearch.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Search\u2026", None))
    # retranslateUi

