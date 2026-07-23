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
from Custom_Widgets.QCustomThemeDarkLightToggle import QCustomThemeDarkLightToggle
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1200, 760)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.rootLayout = QHBoxLayout(self.centralwidget)
        self.rootLayout.setSpacing(0)
        self.rootLayout.setObjectName(u"rootLayout")
        self.rootLayout.setContentsMargins(0, 0, 0, 0)
        self.sidebar = QCustomSidebar(self.centralwidget)
        self.sidebar.setObjectName(u"sidebar")
        self.sidebar.setMinimumSize(QSize(216, 0))
        self.sidebar.setMaximumSize(QSize(216, 16777215))
        self.sidebar.setProperty(u"collapsedWidth", 64)
        self.sidebar.setProperty(u"expandedWidth", 216)
        self.sidebar.setProperty(u"defaultWidth", 216)
        self.sidebar.setProperty(u"animationDuration", 320)
        self.sidebarLayout = QVBoxLayout(self.sidebar)
        self.sidebarLayout.setSpacing(8)
        self.sidebarLayout.setObjectName(u"sidebarLayout")
        self.sidebarLayout.setContentsMargins(12, 14, 12, 14)
        self.sidebarToggle = QPushButton(self.sidebar)
        self.sidebarToggle.setObjectName(u"sidebarToggle")
        self.sidebarToggle.setMinimumSize(QSize(0, 34))
        self.sidebarToggle.setIconSize(QSize(20, 20))

        self.sidebarLayout.addWidget(self.sidebarToggle)

        self.brandLabel = QCustomSidebarLabel(self.sidebar)
        self.brandLabel.setObjectName(u"brandLabel")
        self.brandLabel.setProperty(u"iconSize", QSize(22, 22))

        self.sidebarLayout.addWidget(self.brandLabel)

        self.navOverview = QCustomSidebarButton(self.sidebar)
        self.navOverview.setObjectName(u"navOverview")
        self.navOverview.setMinimumSize(QSize(0, 40))
        self.navOverview.setCheckable(True)
        self.navOverview.setAutoExclusive(True)
        self.navOverview.setChecked(True)
        self.navOverview.setIconSize(QSize(20, 20))

        self.sidebarLayout.addWidget(self.navOverview)

        self.navStations = QCustomSidebarButton(self.sidebar)
        self.navStations.setObjectName(u"navStations")
        self.navStations.setMinimumSize(QSize(0, 40))
        self.navStations.setCheckable(True)
        self.navStations.setAutoExclusive(True)
        self.navStations.setIconSize(QSize(20, 20))

        self.sidebarLayout.addWidget(self.navStations)

        self.navForecast = QCustomSidebarButton(self.sidebar)
        self.navForecast.setObjectName(u"navForecast")
        self.navForecast.setMinimumSize(QSize(0, 40))
        self.navForecast.setCheckable(True)
        self.navForecast.setAutoExclusive(True)
        self.navForecast.setIconSize(QSize(20, 20))

        self.sidebarLayout.addWidget(self.navForecast)

        self.navAnalytics = QCustomSidebarButton(self.sidebar)
        self.navAnalytics.setObjectName(u"navAnalytics")
        self.navAnalytics.setMinimumSize(QSize(0, 40))
        self.navAnalytics.setCheckable(True)
        self.navAnalytics.setAutoExclusive(True)
        self.navAnalytics.setIconSize(QSize(20, 20))

        self.sidebarLayout.addWidget(self.navAnalytics)

        self.navGallery = QCustomSidebarButton(self.sidebar)
        self.navGallery.setObjectName(u"navGallery")
        self.navGallery.setMinimumSize(QSize(0, 40))
        self.navGallery.setCheckable(True)
        self.navGallery.setAutoExclusive(True)
        self.navGallery.setIconSize(QSize(20, 20))

        self.sidebarLayout.addWidget(self.navGallery)

        self.navSettings = QCustomSidebarButton(self.sidebar)
        self.navSettings.setObjectName(u"navSettings")
        self.navSettings.setMinimumSize(QSize(0, 40))
        self.navSettings.setCheckable(True)
        self.navSettings.setAutoExclusive(True)
        self.navSettings.setIconSize(QSize(20, 20))

        self.sidebarLayout.addWidget(self.navSettings)

        self.sidebarSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.sidebarLayout.addItem(self.sidebarSpacer)

        self.themeToggle = QCustomThemeDarkLightToggle(self.sidebar)
        self.themeToggle.setObjectName(u"themeToggle")
        self.themeToggle.setMinimumSize(QSize(0, 36))

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
        self.pageStack.setProperty(u"transitionTime", 420)
        self.overviewContainer = QCustomComponentContainer()
        self.overviewContainer.setObjectName(u"overviewContainer")
        self.overviewContainer.setProperty(u"previewComponent", False)
        self.pageStack.addWidget(self.overviewContainer)
        self.stationsContainer = QCustomComponentContainer()
        self.stationsContainer.setObjectName(u"stationsContainer")
        self.stationsContainer.setProperty(u"previewComponent", False)
        self.pageStack.addWidget(self.stationsContainer)
        self.forecastContainer = QCustomComponentContainer()
        self.forecastContainer.setObjectName(u"forecastContainer")
        self.forecastContainer.setProperty(u"previewComponent", False)
        self.pageStack.addWidget(self.forecastContainer)
        self.analyticsContainer = QCustomComponentContainer()
        self.analyticsContainer.setObjectName(u"analyticsContainer")
        self.analyticsContainer.setProperty(u"previewComponent", False)
        self.pageStack.addWidget(self.analyticsContainer)
        self.galleryContainer = QCustomComponentContainer()
        self.galleryContainer.setObjectName(u"galleryContainer")
        self.galleryContainer.setProperty(u"previewComponent", False)
        self.pageStack.addWidget(self.galleryContainer)
        self.settingsContainer = QCustomComponentContainer()
        self.settingsContainer.setObjectName(u"settingsContainer")
        self.settingsContainer.setProperty(u"previewComponent", False)
        self.pageStack.addWidget(self.settingsContainer)

        self.rootLayout.addWidget(self.pageStack)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Aurora Deck Pro", None))
        self.sidebar.setProperty(u"toggleButtonName", QCoreApplication.translate("MainWindow", u"sidebarToggle", None))
        self.sidebarToggle.setText("")
        self.brandLabel.setProperty(u"text", QCoreApplication.translate("MainWindow", u"AURORA", None))
        self.navOverview.setProperty(u"labelText", QCoreApplication.translate("MainWindow", u"Overview", None))
        self.navStations.setProperty(u"labelText", QCoreApplication.translate("MainWindow", u"Stations", None))
        self.navForecast.setProperty(u"labelText", QCoreApplication.translate("MainWindow", u"Forecast", None))
        self.navAnalytics.setProperty(u"labelText", QCoreApplication.translate("MainWindow", u"Analytics", None))
        self.navGallery.setProperty(u"labelText", QCoreApplication.translate("MainWindow", u"Gallery", None))
        self.navSettings.setProperty(u"labelText", QCoreApplication.translate("MainWindow", u"Settings", None))
        self.themeToggle.setText(QCoreApplication.translate("MainWindow", u"Theme", None))
        self.overviewContainer.setProperty(u"filePath", QCoreApplication.translate("MainWindow", u"ui/OverviewComponent.ui", None))
        self.stationsContainer.setProperty(u"filePath", QCoreApplication.translate("MainWindow", u"ui/StationsComponent.ui", None))
        self.forecastContainer.setProperty(u"filePath", QCoreApplication.translate("MainWindow", u"ui/ForecastComponent.ui", None))
        self.analyticsContainer.setProperty(u"filePath", QCoreApplication.translate("MainWindow", u"ui/AnalyticsComponent.ui", None))
        self.galleryContainer.setProperty(u"filePath", QCoreApplication.translate("MainWindow", u"ui/GalleryComponent.ui", None))
        self.settingsContainer.setProperty(u"filePath", QCoreApplication.translate("MainWindow", u"ui/SettingsComponent.ui", None))
    # retranslateUi

