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
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QMainWindow,
    QMenu, QMenuBar, QPushButton, QScrollArea,
    QSizePolicy, QSpacerItem, QStatusBar, QVBoxLayout,
    QWidget)
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(862, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setSpacing(10)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(10, 10, 10, 10)
        self.leftBar = QWidget(self.centralwidget)
        self.leftBar.setObjectName(u"leftBar")
        self.leftBar.setMinimumSize(QSize(200, 0))
        self.leftBarLayout = QVBoxLayout(self.leftBar)
        self.leftBarLayout.setObjectName(u"leftBarLayout")
        self.addWindowBtn = QPushButton(self.leftBar)
        self.addWindowBtn.setObjectName(u"addWindowBtn")

        self.leftBarLayout.addWidget(self.addWindowBtn)

        self.leftLabel = QLabel(self.leftBar)
        self.leftLabel.setObjectName(u"leftLabel")

        self.leftBarLayout.addWidget(self.leftLabel)

        self.leftSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.leftBarLayout.addItem(self.leftSpacer)


        self.horizontalLayout.addWidget(self.leftBar)

        self.scrollArea = QScrollArea(self.centralwidget)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 430, 526))
        self.scrollLayout = QVBoxLayout(self.scrollAreaWidgetContents)
        self.scrollLayout.setObjectName(u"scrollLayout")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.horizontalLayout.addWidget(self.scrollArea)

        self.rightBar = QWidget(self.centralwidget)
        self.rightBar.setObjectName(u"rightBar")
        self.rightBar.setMinimumSize(QSize(200, 0))
        self.rightBarLayout = QVBoxLayout(self.rightBar)
        self.rightBarLayout.setObjectName(u"rightBarLayout")
        self.rightLabel = QLabel(self.rightBar)
        self.rightLabel.setObjectName(u"rightLabel")

        self.rightBarLayout.addWidget(self.rightLabel)

        self.rightSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.rightBarLayout.addItem(self.rightSpacer)


        self.horizontalLayout.addWidget(self.rightBar)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 862, 33))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuNew = QMenu(self.menubar)
        self.menuNew.setObjectName(u"menuNew")
        self.menuAnother = QMenu(self.menubar)
        self.menuAnother.setObjectName(u"menuAnother")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuNew.menuAction())
        self.menubar.addAction(self.menuAnother.menuAction())

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"QCustomEmbeddedWindow Example", None))
        self.addWindowBtn.setText(QCoreApplication.translate("MainWindow", u"Add embedded window", None))
        self.leftLabel.setText(QCoreApplication.translate("MainWindow", u"Left bar", None))
        self.rightLabel.setText(QCoreApplication.translate("MainWindow", u"Right bar", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"menu", None))
        self.menuNew.setTitle(QCoreApplication.translate("MainWindow", u"new menu", None))
        self.menuAnother.setTitle(QCoreApplication.translate("MainWindow", u"another menu", None))
    # retranslateUi

