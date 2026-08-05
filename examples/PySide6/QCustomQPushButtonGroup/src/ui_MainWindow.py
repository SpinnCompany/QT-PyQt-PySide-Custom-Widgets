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
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(520, 300)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.group1Caption = QLabel(self.centralwidget)
        self.group1Caption.setObjectName(u"group1Caption")

        self.verticalLayout.addWidget(self.group1Caption)

        self.group1Frame = QFrame(self.centralwidget)
        self.group1Frame.setObjectName(u"group1Frame")
        self.group1Frame.setFrameShape(QFrame.StyledPanel)
        self.group1Frame.setFrameShadow(QFrame.Raised)
        self.group1Layout = QHBoxLayout(self.group1Frame)
        self.group1Layout.setObjectName(u"group1Layout")
        self.group1Btn1 = QPushButton(self.group1Frame)
        self.group1Btn1.setObjectName(u"group1Btn1")

        self.group1Layout.addWidget(self.group1Btn1)

        self.group1Btn2 = QPushButton(self.group1Frame)
        self.group1Btn2.setObjectName(u"group1Btn2")

        self.group1Layout.addWidget(self.group1Btn2)

        self.group1Btn3 = QPushButton(self.group1Frame)
        self.group1Btn3.setObjectName(u"group1Btn3")

        self.group1Layout.addWidget(self.group1Btn3)

        self.group1Btn4 = QPushButton(self.group1Frame)
        self.group1Btn4.setObjectName(u"group1Btn4")

        self.group1Layout.addWidget(self.group1Btn4)


        self.verticalLayout.addWidget(self.group1Frame, 0, Qt.AlignTop)

        self.group2Caption = QLabel(self.centralwidget)
        self.group2Caption.setObjectName(u"group2Caption")

        self.verticalLayout.addWidget(self.group2Caption)

        self.group2Frame = QFrame(self.centralwidget)
        self.group2Frame.setObjectName(u"group2Frame")
        self.group2Frame.setFrameShape(QFrame.StyledPanel)
        self.group2Frame.setFrameShadow(QFrame.Raised)
        self.group2Layout = QHBoxLayout(self.group2Frame)
        self.group2Layout.setObjectName(u"group2Layout")
        self.group2Btn1 = QPushButton(self.group2Frame)
        self.group2Btn1.setObjectName(u"group2Btn1")

        self.group2Layout.addWidget(self.group2Btn1)

        self.group2Btn2 = QPushButton(self.group2Frame)
        self.group2Btn2.setObjectName(u"group2Btn2")

        self.group2Layout.addWidget(self.group2Btn2)

        self.group2Btn3 = QPushButton(self.group2Frame)
        self.group2Btn3.setObjectName(u"group2Btn3")

        self.group2Layout.addWidget(self.group2Btn3)


        self.verticalLayout.addWidget(self.group2Frame, 0, Qt.AlignBottom)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"QCustomQPushButtonGroup Showcase", None))
        self.group1Caption.setText(QCoreApplication.translate("MainWindow", u"Group 1", None))
        self.group1Btn1.setText(QCoreApplication.translate("MainWindow", u"Button 1", None))
        self.group1Btn2.setText(QCoreApplication.translate("MainWindow", u"Button 2", None))
        self.group1Btn3.setText(QCoreApplication.translate("MainWindow", u"Button 3", None))
        self.group1Btn4.setText(QCoreApplication.translate("MainWindow", u"Button 4", None))
        self.group2Caption.setText(QCoreApplication.translate("MainWindow", u"Group 2", None))
        self.group2Btn1.setText(QCoreApplication.translate("MainWindow", u"Button A", None))
        self.group2Btn2.setText(QCoreApplication.translate("MainWindow", u"Button B", None))
        self.group2Btn3.setText(QCoreApplication.translate("MainWindow", u"Button C", None))
    # retranslateUi

