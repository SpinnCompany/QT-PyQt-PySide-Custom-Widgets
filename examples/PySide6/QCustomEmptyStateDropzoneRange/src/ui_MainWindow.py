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
    QPushButton, QSizePolicy, QVBoxLayout, QWidget)

from Custom_Widgets.QCustomEmptyState import QCustomEmptyState
from Custom_Widgets.QCustomFileDropZone import QCustomFileDropZone
from Custom_Widgets.QCustomRangeSlider import QCustomRangeSlider
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(440, 480)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.mainLayout = QVBoxLayout(self.centralwidget)
        self.mainLayout.setSpacing(14)
        self.mainLayout.setObjectName(u"mainLayout")
        self.mainLayout.setContentsMargins(18, 18, 18, 18)
        self.emptyState = QCustomEmptyState(self.centralwidget)
        self.emptyState.setObjectName(u"emptyState")

        self.mainLayout.addWidget(self.emptyState)

        self.dropZone = QCustomFileDropZone(self.centralwidget)
        self.dropZone.setObjectName(u"dropZone")
        self.dropZone.setMinimumSize(QSize(0, 110))

        self.mainLayout.addWidget(self.dropZone)

        self.rangeCaption = QLabel(self.centralwidget)
        self.rangeCaption.setObjectName(u"rangeCaption")

        self.mainLayout.addWidget(self.rangeCaption)

        self.rangeRow = QHBoxLayout()
        self.rangeRow.setSpacing(12)
        self.rangeRow.setObjectName(u"rangeRow")
        self.priceRange = QCustomRangeSlider(self.centralwidget)
        self.priceRange.setObjectName(u"priceRange")
        self.priceRange.setProperty(u"minimum", 0)
        self.priceRange.setProperty(u"maximum", 1000)
        self.priceRange.setProperty(u"upperValue", 750)
        self.priceRange.setProperty(u"lowerValue", 200)

        self.rangeRow.addWidget(self.priceRange)

        self.rangeValue = QLabel(self.centralwidget)
        self.rangeValue.setObjectName(u"rangeValue")

        self.rangeRow.addWidget(self.rangeValue)


        self.mainLayout.addLayout(self.rangeRow)

        self.statusLabel = QLabel(self.centralwidget)
        self.statusLabel.setObjectName(u"statusLabel")

        self.mainLayout.addWidget(self.statusLabel)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Empty state / Dropzone / Range", None))
        self.rangeCaption.setText(QCoreApplication.translate("MainWindow", u"Price range:", None))
        self.rangeValue.setText(QCoreApplication.translate("MainWindow", u"$200 - $750", None))
        self.statusLabel.setText(QCoreApplication.translate("MainWindow", u"-", None))
    # retranslateUi

