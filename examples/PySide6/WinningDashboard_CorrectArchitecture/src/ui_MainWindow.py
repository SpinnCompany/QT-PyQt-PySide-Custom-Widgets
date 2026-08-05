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
from Custom_Widgets.QCustomSidebarLabel import QCustomSidebarLabel
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1560, 920)
        MainWindow.setMinimumSize(QSize(1120, 680))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.rootLayout = QHBoxLayout(self.centralwidget)
        self.rootLayout.setSpacing(0)
        self.rootLayout.setObjectName(u"rootLayout")
        self.rootLayout.setContentsMargins(0, 0, 0, 0)
        self.sidebar = QCustomSidebar(self.centralwidget)
        self.sidebar.setObjectName(u"sidebar")
        self.sidebar.setMinimumSize(QSize(230, 0))
        self.sidebar.setMaximumSize(QSize(230, 16777215))
        self.sidebar.setProperty(u"collapsedWidth", 72)
        self.sidebar.setProperty(u"expandedWidth", 230)
        self.sidebar.setProperty(u"defaultWidth", 230)
        self.sidebar.setProperty(u"animationDuration", 320)
        self.sidebarLayout = QVBoxLayout(self.sidebar)
        self.sidebarLayout.setSpacing(6)
        self.sidebarLayout.setObjectName(u"sidebarLayout")
        self.sidebarLayout.setContentsMargins(14, 16, 14, 16)
        self.brandLabel = QCustomSidebarLabel(self.sidebar)
        self.brandLabel.setObjectName(u"brandLabel")
        self.brandLabel.setProperty(u"iconSize", QSize(24, 24))

        self.sidebarLayout.addWidget(self.brandLabel)

        self.sidebarToggle = QPushButton(self.sidebar)
        self.sidebarToggle.setObjectName(u"sidebarToggle")
        self.sidebarToggle.setMinimumSize(QSize(0, 32))
        self.sidebarToggle.setIconSize(QSize(18, 18))

        self.sidebarLayout.addWidget(self.sidebarToggle)

        self.secGeneral = QCustomSidebarLabel(self.sidebar)
        self.secGeneral.setObjectName(u"secGeneral")

        self.sidebarLayout.addWidget(self.secGeneral)

        self.navDashboard = QCustomSidebarButton(self.sidebar)
        self.navDashboard.setObjectName(u"navDashboard")
        self.navDashboard.setMinimumSize(QSize(0, 42))
        self.navDashboard.setCheckable(True)
        self.navDashboard.setAutoExclusive(True)
        self.navDashboard.setChecked(True)
        self.navDashboard.setIconSize(QSize(20, 20))

        self.sidebarLayout.addWidget(self.navDashboard)

        self.navProducts = QCustomSidebarButton(self.sidebar)
        self.navProducts.setObjectName(u"navProducts")
        self.navProducts.setMinimumSize(QSize(0, 42))
        self.navProducts.setCheckable(True)
        self.navProducts.setAutoExclusive(True)
        self.navProducts.setIconSize(QSize(20, 20))

        self.sidebarLayout.addWidget(self.navProducts)

        self.navOrders = QCustomSidebarButton(self.sidebar)
        self.navOrders.setObjectName(u"navOrders")
        self.navOrders.setMinimumSize(QSize(0, 42))
        self.navOrders.setCheckable(True)
        self.navOrders.setAutoExclusive(True)
        self.navOrders.setIconSize(QSize(20, 20))

        self.sidebarLayout.addWidget(self.navOrders)

        self.navCustomers = QCustomSidebarButton(self.sidebar)
        self.navCustomers.setObjectName(u"navCustomers")
        self.navCustomers.setMinimumSize(QSize(0, 42))
        self.navCustomers.setCheckable(True)
        self.navCustomers.setAutoExclusive(True)
        self.navCustomers.setIconSize(QSize(20, 20))

        self.sidebarLayout.addWidget(self.navCustomers)

        self.secOther = QCustomSidebarLabel(self.sidebar)
        self.secOther.setObjectName(u"secOther")

        self.sidebarLayout.addWidget(self.secOther)

        self.navMarketing = QCustomSidebarButton(self.sidebar)
        self.navMarketing.setObjectName(u"navMarketing")
        self.navMarketing.setMinimumSize(QSize(0, 42))
        self.navMarketing.setCheckable(True)
        self.navMarketing.setAutoExclusive(True)
        self.navMarketing.setIconSize(QSize(20, 20))

        self.sidebarLayout.addWidget(self.navMarketing)

        self.navAnalytics = QCustomSidebarButton(self.sidebar)
        self.navAnalytics.setObjectName(u"navAnalytics")
        self.navAnalytics.setMinimumSize(QSize(0, 42))
        self.navAnalytics.setCheckable(True)
        self.navAnalytics.setAutoExclusive(True)
        self.navAnalytics.setIconSize(QSize(20, 20))

        self.sidebarLayout.addWidget(self.navAnalytics)

        self.secSupport = QCustomSidebarLabel(self.sidebar)
        self.secSupport.setObjectName(u"secSupport")

        self.sidebarLayout.addWidget(self.secSupport)

        self.navSettings = QCustomSidebarButton(self.sidebar)
        self.navSettings.setObjectName(u"navSettings")
        self.navSettings.setMinimumSize(QSize(0, 42))
        self.navSettings.setCheckable(True)
        self.navSettings.setAutoExclusive(True)
        self.navSettings.setIconSize(QSize(20, 20))

        self.sidebarLayout.addWidget(self.navSettings)

        self.navHelp = QCustomSidebarButton(self.sidebar)
        self.navHelp.setObjectName(u"navHelp")
        self.navHelp.setMinimumSize(QSize(0, 42))
        self.navHelp.setCheckable(True)
        self.navHelp.setAutoExclusive(True)
        self.navHelp.setIconSize(QSize(20, 20))

        self.sidebarLayout.addWidget(self.navHelp)

        self.sidebarSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.sidebarLayout.addItem(self.sidebarSpacer)

        self.themeToggle = QPushButton(self.sidebar)
        self.themeToggle.setObjectName(u"themeToggle")
        self.themeToggle.setMinimumSize(QSize(0, 38))
        self.themeToggle.setIconSize(QSize(18, 18))

        self.sidebarLayout.addWidget(self.themeToggle)


        self.rootLayout.addWidget(self.sidebar)

        self.pageStack = QCustomQStackedWidget(self.centralwidget)
        self.pageStack.setObjectName(u"pageStack")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pageStack.sizePolicy().hasHeightForWidth())
        self.pageStack.setSizePolicy(sizePolicy)
        self.pageStack.setProperty(u"slideTransition", True)
        self.pageStack.setProperty(u"transitionTime", 360)
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
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Winning \u2014 Analytics (Correct Architecture)", None))
        self.brandLabel.setProperty(u"text", QCoreApplication.translate("MainWindow", u"Winning", None))
        self.sidebarToggle.setText(QCoreApplication.translate("MainWindow", u"  Collapse", None))
        self.secGeneral.setProperty(u"text", QCoreApplication.translate("MainWindow", u"GENERAL", None))
        self.navDashboard.setProperty(u"labelText", QCoreApplication.translate("MainWindow", u"Dashboard", None))
        self.navProducts.setProperty(u"labelText", QCoreApplication.translate("MainWindow", u"Products", None))
        self.navOrders.setProperty(u"labelText", QCoreApplication.translate("MainWindow", u"Orders", None))
        self.navCustomers.setProperty(u"labelText", QCoreApplication.translate("MainWindow", u"Customers", None))
        self.secOther.setProperty(u"text", QCoreApplication.translate("MainWindow", u"OTHER", None))
        self.navMarketing.setProperty(u"labelText", QCoreApplication.translate("MainWindow", u"Marketing", None))
        self.navAnalytics.setProperty(u"labelText", QCoreApplication.translate("MainWindow", u"Analytics", None))
        self.secSupport.setProperty(u"text", QCoreApplication.translate("MainWindow", u"SUPPORT", None))
        self.navSettings.setProperty(u"labelText", QCoreApplication.translate("MainWindow", u"Settings", None))
        self.navHelp.setProperty(u"labelText", QCoreApplication.translate("MainWindow", u"Help", None))
        self.themeToggle.setText(QCoreApplication.translate("MainWindow", u"  Light theme", None))
        self.dashboardContainer.setProperty(u"filePath", QCoreApplication.translate("MainWindow", u"ui/DashboardComponent.ui", None))
    # retranslateUi

