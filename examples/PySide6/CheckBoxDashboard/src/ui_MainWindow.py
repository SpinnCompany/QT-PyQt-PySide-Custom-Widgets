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
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QLabel,
    QMainWindow, QPushButton, QSizePolicy, QVBoxLayout,
    QWidget)

from Custom_Widgets.QCustomComponentContainer import QCustomComponentContainer
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1280, 760)
        self.shell = QWidget(MainWindow)
        self.shell.setObjectName(u"shell")
        self.shellLayout = QVBoxLayout(self.shell)
        self.shellLayout.setSpacing(16)
        self.shellLayout.setObjectName(u"shellLayout")
        self.shellLayout.setContentsMargins(22, 18, 22, 18)
        self.topNavContainer = QCustomComponentContainer(self.shell)
        self.topNavContainer.setObjectName(u"topNavContainer")
        self.topNavContainer.setMinimumSize(QSize(0, 54))
        self.topNavContainer.setMaximumSize(QSize(16777215, 60))
        self.topNavContainer.setProperty(u"previewComponent", False)

        self.shellLayout.addWidget(self.topNavContainer)

        self.bodyRow = QHBoxLayout()
        self.bodyRow.setSpacing(16)
        self.bodyRow.setObjectName(u"bodyRow")
        self.railContainer = QCustomComponentContainer(self.shell)
        self.railContainer.setObjectName(u"railContainer")
        self.railContainer.setMinimumSize(QSize(64, 0))
        self.railContainer.setMaximumSize(QSize(64, 16777215))
        self.railContainer.setProperty(u"previewComponent", False)

        self.bodyRow.addWidget(self.railContainer)

        self.contentCol = QVBoxLayout()
        self.contentCol.setSpacing(16)
        self.contentCol.setObjectName(u"contentCol")
        self.headerContainer = QCustomComponentContainer(self.shell)
        self.headerContainer.setObjectName(u"headerContainer")
        self.headerContainer.setMinimumSize(QSize(0, 50))
        self.headerContainer.setMaximumSize(QSize(16777215, 58))
        self.headerContainer.setProperty(u"previewComponent", False)

        self.contentCol.addWidget(self.headerContainer)

        self.boardGrid = QGridLayout()
        self.boardGrid.setObjectName(u"boardGrid")
        self.boardGrid.setHorizontalSpacing(16)
        self.boardGrid.setVerticalSpacing(16)
        self.customerContainer = QCustomComponentContainer(self.shell)
        self.customerContainer.setObjectName(u"customerContainer")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.customerContainer.sizePolicy().hasHeightForWidth())
        self.customerContainer.setSizePolicy(sizePolicy)
        self.customerContainer.setProperty(u"previewComponent", False)

        self.boardGrid.addWidget(self.customerContainer, 0, 0, 1, 1)

        self.productContainer = QCustomComponentContainer(self.shell)
        self.productContainer.setObjectName(u"productContainer")
        sizePolicy.setHeightForWidth(self.productContainer.sizePolicy().hasHeightForWidth())
        self.productContainer.setSizePolicy(sizePolicy)
        self.productContainer.setProperty(u"previewComponent", False)

        self.boardGrid.addWidget(self.productContainer, 0, 1, 1, 1)

        self.timelineContainer = QCustomComponentContainer(self.shell)
        self.timelineContainer.setObjectName(u"timelineContainer")
        sizePolicy.setHeightForWidth(self.timelineContainer.sizePolicy().hasHeightForWidth())
        self.timelineContainer.setSizePolicy(sizePolicy)
        self.timelineContainer.setProperty(u"previewComponent", False)

        self.boardGrid.addWidget(self.timelineContainer, 0, 2, 2, 1)

        self.beeswarmContainer = QCustomComponentContainer(self.shell)
        self.beeswarmContainer.setObjectName(u"beeswarmContainer")
        sizePolicy.setHeightForWidth(self.beeswarmContainer.sizePolicy().hasHeightForWidth())
        self.beeswarmContainer.setSizePolicy(sizePolicy)
        self.beeswarmContainer.setProperty(u"previewComponent", False)

        self.boardGrid.addWidget(self.beeswarmContainer, 1, 0, 1, 2)

        self.boardGrid.setRowStretch(0, 5)
        self.boardGrid.setRowStretch(1, 6)
        self.boardGrid.setColumnStretch(0, 5)
        self.boardGrid.setColumnStretch(1, 5)
        self.boardGrid.setColumnStretch(2, 8)

        self.contentCol.addLayout(self.boardGrid)


        self.bodyRow.addLayout(self.contentCol)


        self.shellLayout.addLayout(self.bodyRow)

        MainWindow.setCentralWidget(self.shell)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Check Box \u2014 Dashboard", None))
        self.topNavContainer.setProperty(u"filePath", QCoreApplication.translate("MainWindow", u"ui/TopNav.ui", None))
        self.railContainer.setProperty(u"filePath", QCoreApplication.translate("MainWindow", u"ui/LeftRail.ui", None))
        self.headerContainer.setProperty(u"filePath", QCoreApplication.translate("MainWindow", u"ui/Header.ui", None))
        self.customerContainer.setProperty(u"filePath", QCoreApplication.translate("MainWindow", u"ui/CustomerCard.ui", None))
        self.productContainer.setProperty(u"filePath", QCoreApplication.translate("MainWindow", u"ui/ProductCard.ui", None))
        self.timelineContainer.setProperty(u"filePath", QCoreApplication.translate("MainWindow", u"ui/TimelineCard.ui", None))
        self.beeswarmContainer.setProperty(u"filePath", QCoreApplication.translate("MainWindow", u"ui/BeeswarmCard.ui", None))
    # retranslateUi

