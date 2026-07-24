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
    QPushButton, QSizePolicy, QVBoxLayout, QWidget)

from Custom_Widgets.QCustomComponentContainer import QCustomComponentContainer
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1200, 720)
        self.shell = QWidget(MainWindow)
        self.shell.setObjectName(u"shell")
        self.shellLayout = QVBoxLayout(self.shell)
        self.shellLayout.setSpacing(0)
        self.shellLayout.setObjectName(u"shellLayout")
        self.shellLayout.setContentsMargins(0, 0, 0, 0)
        self.topBarContainer = QCustomComponentContainer(self.shell)
        self.topBarContainer.setObjectName(u"topBarContainer")
        self.topBarContainer.setMinimumSize(QSize(0, 92))
        self.topBarContainer.setMaximumSize(QSize(16777215, 92))
        self.topBarContainer.setProperty(u"previewComponent", False)

        self.shellLayout.addWidget(self.topBarContainer)

        self.content = QWidget(self.shell)
        self.content.setObjectName(u"content")
        self.boardGrid = QGridLayout(self.content)
        self.boardGrid.setObjectName(u"boardGrid")
        self.boardGrid.setHorizontalSpacing(16)
        self.boardGrid.setVerticalSpacing(16)
        self.boardGrid.setContentsMargins(22, 18, 22, 22)
        self.helloContainer = QCustomComponentContainer(self.content)
        self.helloContainer.setObjectName(u"helloContainer")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.helloContainer.sizePolicy().hasHeightForWidth())
        self.helloContainer.setSizePolicy(sizePolicy)
        self.helloContainer.setProperty(u"previewComponent", False)

        self.boardGrid.addWidget(self.helloContainer, 0, 0, 1, 2)

        self.gaugesContainer = QCustomComponentContainer(self.content)
        self.gaugesContainer.setObjectName(u"gaugesContainer")
        sizePolicy.setHeightForWidth(self.gaugesContainer.sizePolicy().hasHeightForWidth())
        self.gaugesContainer.setSizePolicy(sizePolicy)
        self.gaugesContainer.setProperty(u"previewComponent", False)

        self.boardGrid.addWidget(self.gaugesContainer, 0, 2, 1, 2)

        self.devicesContainer = QCustomComponentContainer(self.content)
        self.devicesContainer.setObjectName(u"devicesContainer")
        sizePolicy.setHeightForWidth(self.devicesContainer.sizePolicy().hasHeightForWidth())
        self.devicesContainer.setSizePolicy(sizePolicy)
        self.devicesContainer.setProperty(u"previewComponent", False)

        self.boardGrid.addWidget(self.devicesContainer, 1, 0, 1, 2)

        self.lightingContainer = QCustomComponentContainer(self.content)
        self.lightingContainer.setObjectName(u"lightingContainer")
        sizePolicy.setHeightForWidth(self.lightingContainer.sizePolicy().hasHeightForWidth())
        self.lightingContainer.setSizePolicy(sizePolicy)
        self.lightingContainer.setProperty(u"previewComponent", False)

        self.boardGrid.addWidget(self.lightingContainer, 1, 2, 1, 1)

        self.securityContainer = QCustomComponentContainer(self.content)
        self.securityContainer.setObjectName(u"securityContainer")
        sizePolicy.setHeightForWidth(self.securityContainer.sizePolicy().hasHeightForWidth())
        self.securityContainer.setSizePolicy(sizePolicy)
        self.securityContainer.setProperty(u"previewComponent", False)

        self.boardGrid.addWidget(self.securityContainer, 1, 3, 1, 1)

        self.boardGrid.setRowStretch(0, 5)
        self.boardGrid.setRowStretch(1, 6)
        self.boardGrid.setColumnStretch(0, 3)
        self.boardGrid.setColumnStretch(1, 3)
        self.boardGrid.setColumnStretch(2, 3)
        self.boardGrid.setColumnStretch(3, 3)

        self.shellLayout.addWidget(self.content)

        MainWindow.setCentralWidget(self.shell)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"My Home \u2014 Smart Home Dashboard", None))
        self.topBarContainer.setProperty(u"filePath", QCoreApplication.translate("MainWindow", u"ui/TopBar.ui", None))
        self.helloContainer.setProperty(u"filePath", QCoreApplication.translate("MainWindow", u"ui/HelloCard.ui", None))
        self.gaugesContainer.setProperty(u"filePath", QCoreApplication.translate("MainWindow", u"ui/GaugesCard.ui", None))
        self.devicesContainer.setProperty(u"filePath", QCoreApplication.translate("MainWindow", u"ui/DevicesCard.ui", None))
        self.lightingContainer.setProperty(u"filePath", QCoreApplication.translate("MainWindow", u"ui/LightingCard.ui", None))
        self.securityContainer.setProperty(u"filePath", QCoreApplication.translate("MainWindow", u"ui/SecurityCard.ui", None))
    # retranslateUi

