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
from PySide6.QtWidgets import (QApplication, QGridLayout, QLabel, QMainWindow,
    QPushButton, QSizePolicy, QWidget)
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(860, 420)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.buttonGrid = QGridLayout(self.centralwidget)
        self.buttonGrid.setObjectName(u"buttonGrid")
        self.buttonGrid.setHorizontalSpacing(12)
        self.buttonGrid.setVerticalSpacing(12)
        self.buttonGrid.setContentsMargins(24, 24, 24, 24)
        self.btnAuto1 = QPushButton(self.centralwidget)
        self.btnAuto1.setObjectName(u"btnAuto1")

        self.buttonGrid.addWidget(self.btnAuto1, 0, 0, 1, 1)

        self.btnTopLeft = QPushButton(self.centralwidget)
        self.btnTopLeft.setObjectName(u"btnTopLeft")

        self.buttonGrid.addWidget(self.btnTopLeft, 0, 1, 1, 1)

        self.btnTopCenter = QPushButton(self.centralwidget)
        self.btnTopCenter.setObjectName(u"btnTopCenter")

        self.buttonGrid.addWidget(self.btnTopCenter, 0, 2, 1, 1)

        self.btnTopRight = QPushButton(self.centralwidget)
        self.btnTopRight.setObjectName(u"btnTopRight")

        self.buttonGrid.addWidget(self.btnTopRight, 0, 3, 1, 1)

        self.btnBottomLeft = QPushButton(self.centralwidget)
        self.btnBottomLeft.setObjectName(u"btnBottomLeft")

        self.buttonGrid.addWidget(self.btnBottomLeft, 0, 4, 1, 1)

        self.btnBottomCenter = QPushButton(self.centralwidget)
        self.btnBottomCenter.setObjectName(u"btnBottomCenter")

        self.buttonGrid.addWidget(self.btnBottomCenter, 1, 0, 1, 1)

        self.btnBottomRight = QPushButton(self.centralwidget)
        self.btnBottomRight.setObjectName(u"btnBottomRight")

        self.buttonGrid.addWidget(self.btnBottomRight, 1, 1, 1, 1)

        self.btnAuto2 = QPushButton(self.centralwidget)
        self.btnAuto2.setObjectName(u"btnAuto2")

        self.buttonGrid.addWidget(self.btnAuto2, 1, 2, 1, 1)

        self.btnLeftTop = QPushButton(self.centralwidget)
        self.btnLeftTop.setObjectName(u"btnLeftTop")

        self.buttonGrid.addWidget(self.btnLeftTop, 1, 3, 1, 1)

        self.btnLeftBottom = QPushButton(self.centralwidget)
        self.btnLeftBottom.setObjectName(u"btnLeftBottom")

        self.buttonGrid.addWidget(self.btnLeftBottom, 1, 4, 1, 1)

        self.btnRightTop = QPushButton(self.centralwidget)
        self.btnRightTop.setObjectName(u"btnRightTop")

        self.buttonGrid.addWidget(self.btnRightTop, 2, 0, 1, 1)

        self.btnRightBottom = QPushButton(self.centralwidget)
        self.btnRightBottom.setObjectName(u"btnRightBottom")

        self.buttonGrid.addWidget(self.btnRightBottom, 2, 1, 1, 1)

        self.btnLeftCenter = QPushButton(self.centralwidget)
        self.btnLeftCenter.setObjectName(u"btnLeftCenter")

        self.buttonGrid.addWidget(self.btnLeftCenter, 2, 2, 1, 1)

        self.btnRightCenter = QPushButton(self.centralwidget)
        self.btnRightCenter.setObjectName(u"btnRightCenter")

        self.buttonGrid.addWidget(self.btnRightCenter, 2, 3, 1, 1)

        self.btnAuto3 = QPushButton(self.centralwidget)
        self.btnAuto3.setObjectName(u"btnAuto3")

        self.buttonGrid.addWidget(self.btnAuto3, 2, 4, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"QCustomTipOverlay Tail Position Test", None))
        self.btnAuto1.setText(QCoreApplication.translate("MainWindow", u"Auto", None))
        self.btnTopLeft.setText(QCoreApplication.translate("MainWindow", u"Top-Left", None))
        self.btnTopCenter.setText(QCoreApplication.translate("MainWindow", u"Top-Center", None))
        self.btnTopRight.setText(QCoreApplication.translate("MainWindow", u"Top-Right", None))
        self.btnBottomLeft.setText(QCoreApplication.translate("MainWindow", u"Bottom-Left", None))
        self.btnBottomCenter.setText(QCoreApplication.translate("MainWindow", u"Bottom-Center", None))
        self.btnBottomRight.setText(QCoreApplication.translate("MainWindow", u"Bottom-Right", None))
        self.btnAuto2.setText(QCoreApplication.translate("MainWindow", u"Auto", None))
        self.btnLeftTop.setText(QCoreApplication.translate("MainWindow", u"Left-Top", None))
        self.btnLeftBottom.setText(QCoreApplication.translate("MainWindow", u"Left-Bottom", None))
        self.btnRightTop.setText(QCoreApplication.translate("MainWindow", u"Right-Top", None))
        self.btnRightBottom.setText(QCoreApplication.translate("MainWindow", u"Right-Bottom", None))
        self.btnLeftCenter.setText(QCoreApplication.translate("MainWindow", u"Left-Center", None))
        self.btnRightCenter.setText(QCoreApplication.translate("MainWindow", u"Right-Center", None))
        self.btnAuto3.setText(QCoreApplication.translate("MainWindow", u"Auto", None))
    # retranslateUi

