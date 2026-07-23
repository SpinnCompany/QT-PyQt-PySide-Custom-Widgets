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
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

from Custom_Widgets.QCustomAvatar import QCustomAvatar
from Custom_Widgets.QCustomComponentContainer import QCustomComponentContainer
from Custom_Widgets.QCustomQMainWindow import QCustomQMainWindow
from Custom_Widgets.QCustomQStackedWidget import QCustomQStackedWidget
from Custom_Widgets.QCustomSidebar import QCustomSidebar
from Custom_Widgets.QCustomSidebarButton import QCustomSidebarButton
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1360, 840)
        MainWindow.setMinimumSize(QSize(1120, 720))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.rootLayout = QHBoxLayout(self.centralwidget)
        self.rootLayout.setSpacing(0)
        self.rootLayout.setObjectName(u"rootLayout")
        self.rootLayout.setContentsMargins(0, 0, 0, 0)
        self.sidebar = QCustomSidebar(self.centralwidget)
        self.sidebar.setObjectName(u"sidebar")
        self.sidebar.setMinimumSize(QSize(86, 0))
        self.sidebar.setMaximumSize(QSize(86, 16777215))
        self.sidebar.setProperty(u"collapsedWidth", 86)
        self.sidebar.setProperty(u"expandedWidth", 230)
        self.sidebar.setProperty(u"defaultWidth", 86)
        self.sidebar.setProperty(u"animationDuration", 300)
        self.sidebarLayout = QVBoxLayout(self.sidebar)
        self.sidebarLayout.setSpacing(8)
        self.sidebarLayout.setObjectName(u"sidebarLayout")
        self.sidebarLayout.setContentsMargins(18, 22, 18, 22)
        self.sidebarToggle = QPushButton(self.sidebar)
        self.sidebarToggle.setObjectName(u"sidebarToggle")
        self.sidebarToggle.setMinimumSize(QSize(50, 44))
        self.sidebarToggle.setMaximumSize(QSize(50, 44))
        self.sidebarToggle.setIconSize(QSize(22, 22))
        self.sidebarToggle.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.sidebarLayout.addWidget(self.sidebarToggle)

        self.navTopSpacer = QSpacerItem(10, 28, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.sidebarLayout.addItem(self.navTopSpacer)

        self.navDashboard = QCustomSidebarButton(self.sidebar)
        self.navDashboard.setObjectName(u"navDashboard")
        self.navDashboard.setMinimumSize(QSize(0, 46))
        self.navDashboard.setCheckable(True)
        self.navDashboard.setAutoExclusive(True)
        self.navDashboard.setChecked(True)
        self.navDashboard.setIconSize(QSize(22, 22))
        self.navDashboard.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.sidebarLayout.addWidget(self.navDashboard)

        self.navActivity = QCustomSidebarButton(self.sidebar)
        self.navActivity.setObjectName(u"navActivity")
        self.navActivity.setMinimumSize(QSize(0, 46))
        self.navActivity.setCheckable(True)
        self.navActivity.setAutoExclusive(True)
        self.navActivity.setIconSize(QSize(22, 22))
        self.navActivity.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.sidebarLayout.addWidget(self.navActivity)

        self.navCards = QCustomSidebarButton(self.sidebar)
        self.navCards.setObjectName(u"navCards")
        self.navCards.setMinimumSize(QSize(0, 46))
        self.navCards.setCheckable(True)
        self.navCards.setAutoExclusive(True)
        self.navCards.setIconSize(QSize(22, 22))
        self.navCards.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.sidebarLayout.addWidget(self.navCards)

        self.navSettings = QCustomSidebarButton(self.sidebar)
        self.navSettings.setObjectName(u"navSettings")
        self.navSettings.setMinimumSize(QSize(0, 46))
        self.navSettings.setCheckable(True)
        self.navSettings.setAutoExclusive(True)
        self.navSettings.setIconSize(QSize(22, 22))
        self.navSettings.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.sidebarLayout.addWidget(self.navSettings)

        self.navDivider = QFrame(self.sidebar)
        self.navDivider.setObjectName(u"navDivider")
        self.navDivider.setMinimumSize(QSize(34, 1))
        self.navDivider.setMaximumSize(QSize(16777215, 1))
        self.navDivider.setFrameShape(QFrame.StyledPanel)

        self.sidebarLayout.addWidget(self.navDivider)

        self.navAdd = QCustomSidebarButton(self.sidebar)
        self.navAdd.setObjectName(u"navAdd")
        self.navAdd.setMinimumSize(QSize(0, 46))
        self.navAdd.setIconSize(QSize(20, 20))
        self.navAdd.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.sidebarLayout.addWidget(self.navAdd)

        self.sidebarSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.sidebarLayout.addItem(self.sidebarSpacer)

        self.themeToggle = QCustomSidebarButton(self.sidebar)
        self.themeToggle.setObjectName(u"themeToggle")
        self.themeToggle.setMinimumSize(QSize(0, 46))
        self.themeToggle.setIconSize(QSize(20, 20))
        self.themeToggle.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.sidebarLayout.addWidget(self.themeToggle)

        self.avatarRow = QHBoxLayout()
        self.avatarRow.setObjectName(u"avatarRow")
        self.avatarRow.setContentsMargins(2, 6, -1, -1)
        self.sidebarAvatar = QCustomAvatar(self.sidebar)
        self.sidebarAvatar.setObjectName(u"sidebarAvatar")
        self.sidebarAvatar.setMinimumSize(QSize(44, 44))
        self.sidebarAvatar.setMaximumSize(QSize(44, 44))

        self.avatarRow.addWidget(self.sidebarAvatar)

        self.avatarName = QLabel(self.sidebar)
        self.avatarName.setObjectName(u"avatarName")

        self.avatarRow.addWidget(self.avatarName)

        self.avatarRowSpacer = QSpacerItem(10, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.avatarRow.addItem(self.avatarRowSpacer)


        self.sidebarLayout.addLayout(self.avatarRow)


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
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Finance \u2014 Dashboard", None))
        self.navDashboard.setProperty(u"labelText", QCoreApplication.translate("MainWindow", u"Dashboard", None))
        self.navActivity.setProperty(u"labelText", QCoreApplication.translate("MainWindow", u"Transactions", None))
        self.navCards.setProperty(u"labelText", QCoreApplication.translate("MainWindow", u"My cards", None))
        self.navSettings.setProperty(u"labelText", QCoreApplication.translate("MainWindow", u"Settings", None))
        self.navAdd.setProperty(u"labelText", QCoreApplication.translate("MainWindow", u"Add card", None))
        self.themeToggle.setProperty(u"labelText", QCoreApplication.translate("MainWindow", u"Dark mode", None))
        self.sidebarAvatar.setProperty(u"text", QCoreApplication.translate("MainWindow", u"M", None))
        self.avatarName.setText(QCoreApplication.translate("MainWindow", u"  Matt K.", None))
        self.avatarName.setProperty(u"role", QCoreApplication.translate("MainWindow", u"avatarName", None))
        self.dashboardContainer.setProperty(u"filePath", QCoreApplication.translate("MainWindow", u"ui/DashboardComponent.ui", None))
    # retranslateUi

