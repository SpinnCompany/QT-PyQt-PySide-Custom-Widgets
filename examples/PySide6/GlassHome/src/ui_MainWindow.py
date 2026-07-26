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
from Custom_Widgets.QCustomGlassFrame import QCustomGlassFrame
from Custom_Widgets.QCustomWallpaper import QCustomWallpaper
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1400, 860)
        self.shell = QWidget(MainWindow)
        self.shell.setObjectName(u"shell")
        self.shellGrid = QGridLayout(self.shell)
        self.shellGrid.setSpacing(0)
        self.shellGrid.setObjectName(u"shellGrid")
        self.shellGrid.setContentsMargins(0, 0, 0, 0)
        self.wallpaper = QCustomWallpaper(self.shell)
        self.wallpaper.setObjectName(u"wallpaper")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.wallpaper.sizePolicy().hasHeightForWidth())
        self.wallpaper.setSizePolicy(sizePolicy)

        self.shellGrid.addWidget(self.wallpaper, 0, 0, 1, 1)

        self.overlay = QWidget(self.shell)
        self.overlay.setObjectName(u"overlay")
        self.overlayLayout = QHBoxLayout(self.overlay)
        self.overlayLayout.setSpacing(18)
        self.overlayLayout.setObjectName(u"overlayLayout")
        self.overlayLayout.setContentsMargins(22, 22, 22, 16)
        self.navRailContainer = QCustomComponentContainer(self.overlay)
        self.navRailContainer.setObjectName(u"navRailContainer")
        self.navRailContainer.setMinimumSize(QSize(84, 0))
        self.navRailContainer.setMaximumSize(QSize(84, 16777215))
        self.navRailContainer.setProperty(u"previewComponent", False)

        self.overlayLayout.addWidget(self.navRailContainer)

        self.mainCol = QVBoxLayout()
        self.mainCol.setSpacing(12)
        self.mainCol.setObjectName(u"mainCol")
        self.sheetGlass = QCustomGlassFrame(self.overlay)
        self.sheetGlass.setObjectName(u"sheetGlass")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.sheetGlass.sizePolicy().hasHeightForWidth())
        self.sheetGlass.setSizePolicy(sizePolicy1)
        self.sheetGlass.setProperty(u"cornerRadius", 34)
        self.sheetGlass.setProperty(u"liquidEdge", True)
        self.sheetGlass.setProperty(u"edgeIntensity", 0.400000000000000)
        self.sheetGrid = QGridLayout(self.sheetGlass)
        self.sheetGrid.setObjectName(u"sheetGrid")
        self.sheetGrid.setHorizontalSpacing(16)
        self.sheetGrid.setVerticalSpacing(16)
        self.sheetGrid.setContentsMargins(20, 20, 20, 20)
        self.heroContainer = QCustomComponentContainer(self.sheetGlass)
        self.heroContainer.setObjectName(u"heroContainer")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy2.setHorizontalStretch(5)
        sizePolicy2.setVerticalStretch(3)
        sizePolicy2.setHeightForWidth(self.heroContainer.sizePolicy().hasHeightForWidth())
        self.heroContainer.setSizePolicy(sizePolicy2)
        self.heroContainer.setProperty(u"previewComponent", False)

        self.sheetGrid.addWidget(self.heroContainer, 0, 0, 1, 1)

        self.powerContainer = QCustomComponentContainer(self.sheetGlass)
        self.powerContainer.setObjectName(u"powerContainer")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy3.setHorizontalStretch(4)
        sizePolicy3.setVerticalStretch(3)
        sizePolicy3.setHeightForWidth(self.powerContainer.sizePolicy().hasHeightForWidth())
        self.powerContainer.setSizePolicy(sizePolicy3)
        self.powerContainer.setProperty(u"previewComponent", False)

        self.sheetGrid.addWidget(self.powerContainer, 0, 1, 1, 1)

        self.statsRow = QHBoxLayout()
        self.statsRow.setSpacing(16)
        self.statsRow.setObjectName(u"statsRow")
        self.statCurrentContainer = QCustomComponentContainer(self.sheetGlass)
        self.statCurrentContainer.setObjectName(u"statCurrentContainer")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy4.setHorizontalStretch(1)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.statCurrentContainer.sizePolicy().hasHeightForWidth())
        self.statCurrentContainer.setSizePolicy(sizePolicy4)
        self.statCurrentContainer.setProperty(u"previewComponent", False)

        self.statsRow.addWidget(self.statCurrentContainer)

        self.statHumidityContainer = QCustomComponentContainer(self.sheetGlass)
        self.statHumidityContainer.setObjectName(u"statHumidityContainer")
        sizePolicy4.setHeightForWidth(self.statHumidityContainer.sizePolicy().hasHeightForWidth())
        self.statHumidityContainer.setSizePolicy(sizePolicy4)
        self.statHumidityContainer.setProperty(u"previewComponent", False)

        self.statsRow.addWidget(self.statHumidityContainer)

        self.statTempContainer = QCustomComponentContainer(self.sheetGlass)
        self.statTempContainer.setObjectName(u"statTempContainer")
        sizePolicy4.setHeightForWidth(self.statTempContainer.sizePolicy().hasHeightForWidth())
        self.statTempContainer.setSizePolicy(sizePolicy4)
        self.statTempContainer.setProperty(u"previewComponent", False)

        self.statsRow.addWidget(self.statTempContainer)


        self.sheetGrid.addLayout(self.statsRow, 1, 0, 1, 2)

        self.tilesRow = QHBoxLayout()
        self.tilesRow.setSpacing(16)
        self.tilesRow.setObjectName(u"tilesRow")
        self.tileHumidifierContainer = QCustomComponentContainer(self.sheetGlass)
        self.tileHumidifierContainer.setObjectName(u"tileHumidifierContainer")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy5.setHorizontalStretch(1)
        sizePolicy5.setVerticalStretch(1)
        sizePolicy5.setHeightForWidth(self.tileHumidifierContainer.sizePolicy().hasHeightForWidth())
        self.tileHumidifierContainer.setSizePolicy(sizePolicy5)
        self.tileHumidifierContainer.setProperty(u"previewComponent", False)

        self.tilesRow.addWidget(self.tileHumidifierContainer)

        self.tileSpeakerContainer = QCustomComponentContainer(self.sheetGlass)
        self.tileSpeakerContainer.setObjectName(u"tileSpeakerContainer")
        sizePolicy5.setHeightForWidth(self.tileSpeakerContainer.sizePolicy().hasHeightForWidth())
        self.tileSpeakerContainer.setSizePolicy(sizePolicy5)
        self.tileSpeakerContainer.setProperty(u"previewComponent", False)

        self.tilesRow.addWidget(self.tileSpeakerContainer)

        self.tileLampContainer = QCustomComponentContainer(self.sheetGlass)
        self.tileLampContainer.setObjectName(u"tileLampContainer")
        sizePolicy5.setHeightForWidth(self.tileLampContainer.sizePolicy().hasHeightForWidth())
        self.tileLampContainer.setSizePolicy(sizePolicy5)
        self.tileLampContainer.setProperty(u"previewComponent", False)

        self.tilesRow.addWidget(self.tileLampContainer)

        self.tileCameraContainer = QCustomComponentContainer(self.sheetGlass)
        self.tileCameraContainer.setObjectName(u"tileCameraContainer")
        sizePolicy5.setHeightForWidth(self.tileCameraContainer.sizePolicy().hasHeightForWidth())
        self.tileCameraContainer.setSizePolicy(sizePolicy5)
        self.tileCameraContainer.setProperty(u"previewComponent", False)

        self.tilesRow.addWidget(self.tileCameraContainer)


        self.sheetGrid.addLayout(self.tilesRow, 2, 0, 1, 2)

        self.rightGlass = QCustomGlassFrame(self.sheetGlass)
        self.rightGlass.setObjectName(u"rightGlass")
        sizePolicy6 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.rightGlass.sizePolicy().hasHeightForWidth())
        self.rightGlass.setSizePolicy(sizePolicy6)
        self.rightGlass.setMinimumSize(QSize(300, 0))
        self.rightGlass.setMaximumSize(QSize(300, 16777215))
        self.rightGlass.setProperty(u"cornerRadius", 26)
        self.rightLayout = QVBoxLayout(self.rightGlass)
        self.rightLayout.setSpacing(14)
        self.rightLayout.setObjectName(u"rightLayout")
        self.rightLayout.setContentsMargins(18, 18, 18, 16)
        self.thermoContainer = QCustomComponentContainer(self.rightGlass)
        self.thermoContainer.setObjectName(u"thermoContainer")
        sizePolicy7 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(1)
        sizePolicy7.setHeightForWidth(self.thermoContainer.sizePolicy().hasHeightForWidth())
        self.thermoContainer.setSizePolicy(sizePolicy7)
        self.thermoContainer.setProperty(u"previewComponent", False)

        self.rightLayout.addWidget(self.thermoContainer)

        self.modeContainer = QCustomComponentContainer(self.rightGlass)
        self.modeContainer.setObjectName(u"modeContainer")
        self.modeContainer.setMinimumSize(QSize(0, 66))
        self.modeContainer.setMaximumSize(QSize(16777215, 66))
        self.modeContainer.setProperty(u"previewComponent", False)

        self.rightLayout.addWidget(self.modeContainer)

        self.playerContainer = QCustomComponentContainer(self.rightGlass)
        self.playerContainer.setObjectName(u"playerContainer")
        self.playerContainer.setMinimumSize(QSize(0, 150))
        self.playerContainer.setMaximumSize(QSize(16777215, 165))
        self.playerContainer.setProperty(u"previewComponent", False)

        self.rightLayout.addWidget(self.playerContainer)


        self.sheetGrid.addWidget(self.rightGlass, 0, 2, 3, 1)


        self.mainCol.addWidget(self.sheetGlass)

        self.roomTabsContainer = QCustomComponentContainer(self.overlay)
        self.roomTabsContainer.setObjectName(u"roomTabsContainer")
        self.roomTabsContainer.setMinimumSize(QSize(0, 78))
        self.roomTabsContainer.setMaximumSize(QSize(16777215, 78))
        self.roomTabsContainer.setProperty(u"previewComponent", False)

        self.mainCol.addWidget(self.roomTabsContainer)


        self.overlayLayout.addLayout(self.mainCol)


        self.shellGrid.addWidget(self.overlay, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.shell)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"GlassHome \u2014 Smart Home", None))
        self.wallpaper.setProperty(u"imageSource", QCoreApplication.translate("MainWindow", u"https://picsum.photos/seed/glasshome/1600/1000", None))
        self.navRailContainer.setProperty(u"filePath", QCoreApplication.translate("MainWindow", u"ui/NavRail.ui", None))
        self.sheetGlass.setProperty(u"backdropSource", QCoreApplication.translate("MainWindow", u"wallpaper", None))
        self.heroContainer.setProperty(u"filePath", QCoreApplication.translate("MainWindow", u"ui/DeviceHero.ui", None))
        self.powerContainer.setProperty(u"filePath", QCoreApplication.translate("MainWindow", u"ui/PowerChart.ui", None))
        self.statCurrentContainer.setProperty(u"filePath", QCoreApplication.translate("MainWindow", u"ui/StatCard.ui", None))
        self.statHumidityContainer.setProperty(u"filePath", QCoreApplication.translate("MainWindow", u"ui/StatCard.ui", None))
        self.statTempContainer.setProperty(u"filePath", QCoreApplication.translate("MainWindow", u"ui/StatCard.ui", None))
        self.tileHumidifierContainer.setProperty(u"filePath", QCoreApplication.translate("MainWindow", u"ui/DeviceTile.ui", None))
        self.tileSpeakerContainer.setProperty(u"filePath", QCoreApplication.translate("MainWindow", u"ui/DeviceTile.ui", None))
        self.tileLampContainer.setProperty(u"filePath", QCoreApplication.translate("MainWindow", u"ui/DeviceTile.ui", None))
        self.tileCameraContainer.setProperty(u"filePath", QCoreApplication.translate("MainWindow", u"ui/DeviceTile.ui", None))
        self.rightGlass.setProperty(u"backdropSource", QCoreApplication.translate("MainWindow", u"wallpaper", None))
        self.thermoContainer.setProperty(u"filePath", QCoreApplication.translate("MainWindow", u"ui/ThermostatPanel.ui", None))
        self.modeContainer.setProperty(u"filePath", QCoreApplication.translate("MainWindow", u"ui/ModeRow.ui", None))
        self.playerContainer.setProperty(u"filePath", QCoreApplication.translate("MainWindow", u"ui/PlayerCard.ui", None))
        self.roomTabsContainer.setProperty(u"filePath", QCoreApplication.translate("MainWindow", u"ui/RoomTabs.ui", None))
    # retranslateUi

