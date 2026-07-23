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
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

from Custom_Widgets.QCustomComponentContainer import QCustomComponentContainer
from Custom_Widgets.QCustomQMainWindow import QCustomQMainWindow
from Custom_Widgets.QCustomQStackedWidget import QCustomQStackedWidget
from Custom_Widgets.QCustomSidebar import QCustomSidebar
from Custom_Widgets.QCustomSidebarButton import QCustomSidebarButton
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1440, 900)
        MainWindow.setMinimumSize(QSize(1200, 780))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.rootLayout = QHBoxLayout(self.centralwidget)
        self.rootLayout.setSpacing(22)
        self.rootLayout.setObjectName(u"rootLayout")
        self.rootLayout.setContentsMargins(22, 22, 22, 22)
        self.sidebar = QCustomSidebar(self.centralwidget)
        self.sidebar.setObjectName(u"sidebar")
        self.sidebar.setMinimumSize(QSize(84, 0))
        self.sidebar.setMaximumSize(QSize(230, 16777215))
        self.sidebar.setProperty(u"collapsedWidth", 84)
        self.sidebar.setProperty(u"expandedWidth", 230)
        self.sidebar.setProperty(u"defaultWidth", 84)
        self.sidebar.setProperty(u"animationDuration", 300)
        self.sidebarLayout = QVBoxLayout(self.sidebar)
        self.sidebarLayout.setSpacing(6)
        self.sidebarLayout.setObjectName(u"sidebarLayout")
        self.sidebarLayout.setContentsMargins(16, 18, 16, 18)
        self.brandRow = QHBoxLayout()
        self.brandRow.setSpacing(10)
        self.brandRow.setObjectName(u"brandRow")
        self.logoBtn = QPushButton(self.sidebar)
        self.logoBtn.setObjectName(u"logoBtn")
        self.logoBtn.setMinimumSize(QSize(52, 52))
        self.logoBtn.setMaximumSize(QSize(52, 52))
        self.logoBtn.setIconSize(QSize(24, 24))
        self.logoBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.brandRow.addWidget(self.logoBtn)

        self.brandName = QLabel(self.sidebar)
        self.brandName.setObjectName(u"brandName")

        self.brandRow.addWidget(self.brandName)

        self.brandSpacer = QSpacerItem(6, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.brandRow.addItem(self.brandSpacer)


        self.sidebarLayout.addLayout(self.brandRow)

        self.sidebarToggle = QPushButton(self.sidebar)
        self.sidebarToggle.setObjectName(u"sidebarToggle")
        self.sidebarToggle.setMinimumSize(QSize(0, 44))
        self.sidebarToggle.setIconSize(QSize(20, 20))
        self.sidebarToggle.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.sidebarLayout.addWidget(self.sidebarToggle)

        self.navTopSpacer = QSpacerItem(10, 14, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.sidebarLayout.addItem(self.navTopSpacer)

        self.navDashboard = QCustomSidebarButton(self.sidebar)
        self.navDashboard.setObjectName(u"navDashboard")
        self.navDashboard.setMinimumSize(QSize(0, 48))
        self.navDashboard.setCheckable(True)
        self.navDashboard.setAutoExclusive(True)
        self.navDashboard.setChecked(True)
        self.navDashboard.setIconSize(QSize(22, 22))
        self.navDashboard.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.sidebarLayout.addWidget(self.navDashboard)

        self.navMarkets = QCustomSidebarButton(self.sidebar)
        self.navMarkets.setObjectName(u"navMarkets")
        self.navMarkets.setMinimumSize(QSize(0, 48))
        self.navMarkets.setCheckable(True)
        self.navMarkets.setAutoExclusive(True)
        self.navMarkets.setIconSize(QSize(22, 22))
        self.navMarkets.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.sidebarLayout.addWidget(self.navMarkets)

        self.navWallet = QCustomSidebarButton(self.sidebar)
        self.navWallet.setObjectName(u"navWallet")
        self.navWallet.setMinimumSize(QSize(0, 48))
        self.navWallet.setCheckable(True)
        self.navWallet.setAutoExclusive(True)
        self.navWallet.setIconSize(QSize(22, 22))
        self.navWallet.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.sidebarLayout.addWidget(self.navWallet)

        self.navReports = QCustomSidebarButton(self.sidebar)
        self.navReports.setObjectName(u"navReports")
        self.navReports.setMinimumSize(QSize(0, 48))
        self.navReports.setCheckable(True)
        self.navReports.setAutoExclusive(True)
        self.navReports.setIconSize(QSize(22, 22))
        self.navReports.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.sidebarLayout.addWidget(self.navReports)

        self.navExchange = QCustomSidebarButton(self.sidebar)
        self.navExchange.setObjectName(u"navExchange")
        self.navExchange.setMinimumSize(QSize(0, 48))
        self.navExchange.setCheckable(True)
        self.navExchange.setAutoExclusive(True)
        self.navExchange.setIconSize(QSize(22, 22))
        self.navExchange.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.sidebarLayout.addWidget(self.navExchange)

        self.navStats = QCustomSidebarButton(self.sidebar)
        self.navStats.setObjectName(u"navStats")
        self.navStats.setMinimumSize(QSize(0, 48))
        self.navStats.setCheckable(True)
        self.navStats.setAutoExclusive(True)
        self.navStats.setIconSize(QSize(22, 22))
        self.navStats.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.sidebarLayout.addWidget(self.navStats)

        self.navContacts = QCustomSidebarButton(self.sidebar)
        self.navContacts.setObjectName(u"navContacts")
        self.navContacts.setMinimumSize(QSize(0, 48))
        self.navContacts.setCheckable(True)
        self.navContacts.setAutoExclusive(True)
        self.navContacts.setIconSize(QSize(22, 22))
        self.navContacts.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.sidebarLayout.addWidget(self.navContacts)

        self.sidebarSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.sidebarLayout.addItem(self.sidebarSpacer)

        self.themeToggle = QCustomSidebarButton(self.sidebar)
        self.themeToggle.setObjectName(u"themeToggle")
        self.themeToggle.setMinimumSize(QSize(0, 46))
        self.themeToggle.setIconSize(QSize(20, 20))
        self.themeToggle.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.sidebarLayout.addWidget(self.themeToggle)

        self.navDocs = QCustomSidebarButton(self.sidebar)
        self.navDocs.setObjectName(u"navDocs")
        self.navDocs.setMinimumSize(QSize(0, 46))
        self.navDocs.setIconSize(QSize(20, 20))
        self.navDocs.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.sidebarLayout.addWidget(self.navDocs)

        self.navSettings = QCustomSidebarButton(self.sidebar)
        self.navSettings.setObjectName(u"navSettings")
        self.navSettings.setMinimumSize(QSize(0, 46))
        self.navSettings.setIconSize(QSize(20, 20))
        self.navSettings.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.sidebarLayout.addWidget(self.navSettings)


        self.rootLayout.addWidget(self.sidebar)

        self.pageStack = QCustomQStackedWidget(self.centralwidget)
        self.pageStack.setObjectName(u"pageStack")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pageStack.sizePolicy().hasHeightForWidth())
        self.pageStack.setSizePolicy(sizePolicy)
        self.pageStack.setProperty(u"slideTransition", True)
        self.pageStack.setProperty(u"transitionTime", 320)
        self.dashboardContainer = QCustomComponentContainer()
        self.dashboardContainer.setObjectName(u"dashboardContainer")
        self.dashboardContainer.setProperty(u"previewComponent", False)
        self.pageStack.addWidget(self.dashboardContainer)

        self.rootLayout.addWidget(self.pageStack)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Crypto \u2014 Dashboard", None))
        self.logoBtn.setText("")
        self.brandName.setText(QCoreApplication.translate("MainWindow", u"Kripton", None))
        self.brandName.setProperty(u"role", QCoreApplication.translate("MainWindow", u"brandName", None))
        self.sidebarToggle.setText("")
        self.navDashboard.setProperty(u"labelText", QCoreApplication.translate("MainWindow", u"Dashboard", None))
        self.navMarkets.setProperty(u"labelText", QCoreApplication.translate("MainWindow", u"Markets", None))
        self.navWallet.setProperty(u"labelText", QCoreApplication.translate("MainWindow", u"Wallet", None))
        self.navReports.setProperty(u"labelText", QCoreApplication.translate("MainWindow", u"Reports", None))
        self.navExchange.setProperty(u"labelText", QCoreApplication.translate("MainWindow", u"Exchange", None))
        self.navStats.setProperty(u"labelText", QCoreApplication.translate("MainWindow", u"Statistics", None))
        self.navContacts.setProperty(u"labelText", QCoreApplication.translate("MainWindow", u"Contacts", None))
        self.themeToggle.setProperty(u"labelText", QCoreApplication.translate("MainWindow", u"Dark mode", None))
        self.navDocs.setProperty(u"labelText", QCoreApplication.translate("MainWindow", u"Docs", None))
        self.navSettings.setProperty(u"labelText", QCoreApplication.translate("MainWindow", u"Settings", None))
        self.dashboardContainer.setProperty(u"filePath", QCoreApplication.translate("MainWindow", u"ui/DashboardComponent.ui", None))
    # retranslateUi

