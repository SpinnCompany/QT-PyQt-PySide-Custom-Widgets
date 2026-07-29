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
    QMainWindow, QPushButton, QScrollArea, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

from Custom_Widgets.QCustomComponentContainer import QCustomComponentContainer
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1240, 884)
        self.shell = QWidget(MainWindow)
        self.shell.setObjectName(u"shell")
        self.shellLayout = QVBoxLayout(self.shell)
        self.shellLayout.setSpacing(0)
        self.shellLayout.setObjectName(u"shellLayout")
        self.shellLayout.setContentsMargins(0, 0, 0, 0)
        self.mainRow = QHBoxLayout()
        self.mainRow.setSpacing(0)
        self.mainRow.setObjectName(u"mainRow")
        self.mainRow.setContentsMargins(0, 0, 0, 0)
        self.sidebarContainer = QCustomComponentContainer(self.shell)
        self.sidebarContainer.setObjectName(u"sidebarContainer")
        self.sidebarContainer.setMinimumSize(QSize(244, 0))
        self.sidebarContainer.setMaximumSize(QSize(244, 16777215))
        self.sidebarContainer.setProperty(u"previewComponent", False)

        self.mainRow.addWidget(self.sidebarContainer)

        self.rightCol = QWidget(self.shell)
        self.rightCol.setObjectName(u"rightCol")
        self.rightColLayout = QVBoxLayout(self.rightCol)
        self.rightColLayout.setSpacing(0)
        self.rightColLayout.setObjectName(u"rightColLayout")
        self.rightColLayout.setContentsMargins(0, 0, 0, 0)
        self.topBarContainer = QCustomComponentContainer(self.rightCol)
        self.topBarContainer.setObjectName(u"topBarContainer")
        self.topBarContainer.setMinimumSize(QSize(0, 84))
        self.topBarContainer.setMaximumSize(QSize(16777215, 84))
        self.topBarContainer.setProperty(u"previewComponent", False)

        self.rightColLayout.addWidget(self.topBarContainer)

        self.contentScroll = QScrollArea(self.rightCol)
        self.contentScroll.setObjectName(u"contentScroll")
        self.contentScroll.setWidgetResizable(True)
        self.contentScroll.setFrameShape(QFrame.NoFrame)
        self.contentScroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.contentInner = QWidget()
        self.contentInner.setObjectName(u"contentInner")
        self.contentLayout = QVBoxLayout(self.contentInner)
        self.contentLayout.setSpacing(6)
        self.contentLayout.setObjectName(u"contentLayout")
        self.contentLayout.setContentsMargins(24, 6, 24, 18)
        self.heroContainer = QCustomComponentContainer(self.contentInner)
        self.heroContainer.setObjectName(u"heroContainer")
        self.heroContainer.setMinimumSize(QSize(0, 330))
        self.heroContainer.setMaximumSize(QSize(16777215, 348))
        self.heroContainer.setProperty(u"previewComponent", False)

        self.contentLayout.addWidget(self.heroContainer)

        self.categoriesContainer = QCustomComponentContainer(self.contentInner)
        self.categoriesContainer.setObjectName(u"categoriesContainer")
        self.categoriesContainer.setMinimumSize(QSize(0, 92))
        self.categoriesContainer.setMaximumSize(QSize(16777215, 100))
        self.categoriesContainer.setProperty(u"previewComponent", False)

        self.contentLayout.addWidget(self.categoriesContainer)

        self.popularContainer = QCustomComponentContainer(self.contentInner)
        self.popularContainer.setObjectName(u"popularContainer")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.popularContainer.sizePolicy().hasHeightForWidth())
        self.popularContainer.setSizePolicy(sizePolicy)
        self.popularContainer.setMinimumSize(QSize(0, 210))
        self.popularContainer.setProperty(u"previewComponent", False)

        self.contentLayout.addWidget(self.popularContainer)

        self.contentStretch = QSpacerItem(10, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.contentLayout.addItem(self.contentStretch)

        self.contentScroll.setWidget(self.contentInner)

        self.rightColLayout.addWidget(self.contentScroll)


        self.mainRow.addWidget(self.rightCol)


        self.shellLayout.addLayout(self.mainRow)

        self.playerContainer = QCustomComponentContainer(self.shell)
        self.playerContainer.setObjectName(u"playerContainer")
        self.playerContainer.setMinimumSize(QSize(0, 96))
        self.playerContainer.setMaximumSize(QSize(16777215, 96))
        self.playerContainer.setProperty(u"previewComponent", False)

        self.shellLayout.addWidget(self.playerContainer)

        MainWindow.setCentralWidget(self.shell)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"RhythmoTune \u2014 Music Dashboard", None))
        self.sidebarContainer.setProperty(u"filePath", QCoreApplication.translate("MainWindow", u"ui/Sidebar.ui", None))
        self.topBarContainer.setProperty(u"filePath", QCoreApplication.translate("MainWindow", u"ui/TopBar.ui", None))
        self.heroContainer.setProperty(u"filePath", QCoreApplication.translate("MainWindow", u"ui/HeroCard.ui", None))
        self.categoriesContainer.setProperty(u"filePath", QCoreApplication.translate("MainWindow", u"ui/CategoriesRow.ui", None))
        self.popularContainer.setProperty(u"filePath", QCoreApplication.translate("MainWindow", u"ui/PopularSongs.ui", None))
        self.playerContainer.setProperty(u"filePath", QCoreApplication.translate("MainWindow", u"ui/PlayerBar.ui", None))
    # retranslateUi

