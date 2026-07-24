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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QPushButton,
    QSizePolicy, QWidget)

from Custom_Widgets.QCustomComponentContainer import QCustomComponentContainer
from Custom_Widgets.QCustomQMainWindow import QCustomQMainWindow
from Custom_Widgets.QCustomQStackedWidget import QCustomQStackedWidget
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1440, 880)
        MainWindow.setMinimumSize(QSize(1200, 760))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.rootLayout = QHBoxLayout(self.centralwidget)
        self.rootLayout.setSpacing(0)
        self.rootLayout.setObjectName(u"rootLayout")
        self.rootLayout.setContentsMargins(0, 0, 0, 0)
        self.sidebarContainer = QCustomComponentContainer(self.centralwidget)
        self.sidebarContainer.setObjectName(u"sidebarContainer")
        self.sidebarContainer.setMinimumSize(QSize(212, 0))
        self.sidebarContainer.setMaximumSize(QSize(212, 16777215))
        self.sidebarContainer.setProperty(u"previewComponent", False)

        self.rootLayout.addWidget(self.sidebarContainer)

        self.pageStack = QCustomQStackedWidget(self.centralwidget)
        self.pageStack.setObjectName(u"pageStack")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pageStack.sizePolicy().hasHeightForWidth())
        self.pageStack.setSizePolicy(sizePolicy)
        self.pageStack.setProperty(u"slideTransition", True)
        self.pageStack.setProperty(u"transitionTime", 300)
        self.chatContainer = QCustomComponentContainer()
        self.chatContainer.setObjectName(u"chatContainer")
        self.chatContainer.setProperty(u"previewComponent", False)
        self.pageStack.addWidget(self.chatContainer)

        self.rootLayout.addWidget(self.pageStack)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Aurora \u2014 Chat", None))
        self.sidebarContainer.setProperty(u"filePath", QCoreApplication.translate("MainWindow", u"ui/SidebarComponent.ui", None))
        self.chatContainer.setProperty(u"filePath", QCoreApplication.translate("MainWindow", u"ui/ChatComponent.ui", None))
    # retranslateUi

