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

from Custom_Widgets.QCustomPagination import QCustomPagination
from Custom_Widgets.QCustomQPushButton import QCustomQPushButton
from Custom_Widgets.QCustomSegmentedControl import QCustomSegmentedControl
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(520, 380)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.viewCaption = QLabel(self.centralwidget)
        self.viewCaption.setObjectName(u"viewCaption")

        self.verticalLayout.addWidget(self.viewCaption)

        self.segRow = QHBoxLayout()
        self.segRow.setObjectName(u"segRow")
        self.segmentedControl = QCustomSegmentedControl(self.centralwidget)
        self.segmentedControl.setObjectName(u"segmentedControl")

        self.segRow.addWidget(self.segmentedControl)

        self.segSpacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.segRow.addItem(self.segSpacer)


        self.verticalLayout.addLayout(self.segRow)

        self.popoverCaption = QLabel(self.centralwidget)
        self.popoverCaption.setObjectName(u"popoverCaption")

        self.verticalLayout.addWidget(self.popoverCaption)

        self.popRow = QHBoxLayout()
        self.popRow.setObjectName(u"popRow")
        self.popoverTrigger = QCustomQPushButton(self.centralwidget)
        self.popoverTrigger.setObjectName(u"popoverTrigger")

        self.popRow.addWidget(self.popoverTrigger)

        self.popSpacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.popRow.addItem(self.popSpacer)


        self.verticalLayout.addLayout(self.popRow)

        self.bodySpacer = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.bodySpacer)

        self.pager = QCustomPagination(self.centralwidget)
        self.pager.setObjectName(u"pager")

        self.verticalLayout.addWidget(self.pager)

        self.statusLabel = QLabel(self.centralwidget)
        self.statusLabel.setObjectName(u"statusLabel")

        self.verticalLayout.addWidget(self.statusLabel)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Pagination / Popover / Segmented", None))
        self.viewCaption.setText(QCoreApplication.translate("MainWindow", u"View:", None))
        self.popoverCaption.setText(QCoreApplication.translate("MainWindow", u"Popover:", None))
        self.popoverTrigger.setText(QCoreApplication.translate("MainWindow", u"Show details", None))
        self.popoverTrigger.setProperty(u"variant", QCoreApplication.translate("MainWindow", u"outline", None))
        self.statusLabel.setText(QCoreApplication.translate("MainWindow", u"-", None))
    # retranslateUi

