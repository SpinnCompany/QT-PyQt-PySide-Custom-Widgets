# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'QCustomQMainWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
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
from PySide6.QtWidgets import (QApplication, QSizePolicy, QWidget)

from Custom_Widgets.QCustomQMainWindow import QCustomQMainWindow

class Ui_CustomMainWindow(object):
    def setupUi(self, CustomMainWindow):
        if not CustomMainWindow.objectName():
            CustomMainWindow.setObjectName(u"CustomMainWindow")
        CustomMainWindow.resize(800, 600)
        self.centralwidget = QWidget(CustomMainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        CustomMainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(CustomMainWindow)

        QMetaObject.connectSlotsByName(CustomMainWindow)
    # setupUi

    def retranslateUi(self, CustomMainWindow):
        CustomMainWindow.setWindowTitle(QCoreApplication.translate("CustomMainWindow", u"Custom MainWindow", None))
    # retranslateUi

