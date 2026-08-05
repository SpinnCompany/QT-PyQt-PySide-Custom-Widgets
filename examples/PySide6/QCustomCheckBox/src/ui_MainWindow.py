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

from Custom_Widgets.QCustomCheckBox import QCustomCheckBox
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(520, 260)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.titleLabel = QLabel(self.centralwidget)
        self.titleLabel.setObjectName(u"titleLabel")

        self.verticalLayout.addWidget(self.titleLabel)

        self.card = QFrame(self.centralwidget)
        self.card.setObjectName(u"card")
        self.card.setFrameShape(QFrame.StyledPanel)
        self.card.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.card)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.checkBox_3 = QCustomCheckBox(self.card)
        self.checkBox_3.setObjectName(u"checkBox_3")
        self.checkBox_3.setMinimumSize(QSize(140, 28))
        self.checkBox_3.setChecked(True)
        self.checkBox_3.setProperty(u"animationDuration", 500)
        self.checkBox_3.setProperty(u"animationEasingCurve", 7)

        self.horizontalLayout.addWidget(self.checkBox_3)

        self.checkBox_2 = QCustomCheckBox(self.card)
        self.checkBox_2.setObjectName(u"checkBox_2")
        self.checkBox_2.setMinimumSize(QSize(140, 28))

        self.horizontalLayout.addWidget(self.checkBox_2)

        self.checkBox = QCustomCheckBox(self.card)
        self.checkBox.setObjectName(u"checkBox")
        self.checkBox.setMinimumSize(QSize(140, 28))
        self.checkBox.setProperty(u"animationDuration", 200)
        self.checkBox.setProperty(u"animationEasingCurve", 0)

        self.horizontalLayout.addWidget(self.checkBox)


        self.verticalLayout.addWidget(self.card)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"QCustomCheckBox Showcase", None))
        self.titleLabel.setText(QCoreApplication.translate("MainWindow", u"Animated Toggle Checkboxes", None))
        self.checkBox_3.setText(QCoreApplication.translate("MainWindow", u"CheckBox 1", None))
        self.checkBox_2.setText(QCoreApplication.translate("MainWindow", u"CheckBox 2", None))
        self.checkBox.setText(QCoreApplication.translate("MainWindow", u"CheckBox 3", None))
    # retranslateUi

