# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'new_QCustomQMainWindow.ui'
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
from PySide6.QtWidgets import (QApplication, QLabel, QPushButton, QSizePolicy,
    QWidget)

from Custom_Widgets.QCustomQMainWindow import QCustomQMainWindow
class Ui_CustomMainWindow(object):
    def setupUi(self, CustomMainWindow):
        if not CustomMainWindow.objectName():
            CustomMainWindow.setObjectName(u"CustomMainWindow")
        CustomMainWindow.resize(800, 600)
        self.centralwidget = QWidget(CustomMainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(140, 160, 541, 71))
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.pushButton.setFont(font)
        icon = QIcon()
        icon.addFile(u":/font_awesome_brands/icons/font_awesome/brands/buffer.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton.setIcon(icon)
        self.pushButton.setIconSize(QSize(32, 32))
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(330, 240, 131, 16))
        font1 = QFont()
        font1.setItalic(True)
        self.label.setFont(font1)
        CustomMainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(CustomMainWindow)

        QMetaObject.connectSlotsByName(CustomMainWindow)
    # setupUi

    def retranslateUi(self, CustomMainWindow):
        CustomMainWindow.setWindowTitle(QCoreApplication.translate("CustomMainWindow", u"Custom MainWindow", None))
        self.pushButton.setText(QCoreApplication.translate("CustomMainWindow", u"25 Modern Desktop GUI", None))
        self.label.setText(QCoreApplication.translate("CustomMainWindow", u"Happy coding!", None))
    # retranslateUi

