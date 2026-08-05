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
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QHBoxLayout,
    QLabel, QMainWindow, QPushButton, QSizePolicy,
    QSlider, QSpacerItem, QVBoxLayout, QWidget)

from Custom_Widgets.map import QCustomMapView
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(900, 640)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(12)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(16, 16, 16, 16)
        self.headerRow = QHBoxLayout()
        self.headerRow.setObjectName(u"headerRow")
        self.titleLabel = QLabel(self.centralwidget)
        self.titleLabel.setObjectName(u"titleLabel")

        self.headerRow.addWidget(self.titleLabel)

        self.headerSpacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.headerRow.addItem(self.headerSpacer)

        self.offlineBadge = QLabel(self.centralwidget)
        self.offlineBadge.setObjectName(u"offlineBadge")

        self.headerRow.addWidget(self.offlineBadge)


        self.verticalLayout.addLayout(self.headerRow)

        self.mapCard = QFrame(self.centralwidget)
        self.mapCard.setObjectName(u"mapCard")
        self.mapCard.setFrameShape(QFrame.StyledPanel)
        self.mapCardLayout = QVBoxLayout(self.mapCard)
        self.mapCardLayout.setObjectName(u"mapCardLayout")
        self.mapCardLayout.setContentsMargins(8, 8, 8, 8)
        self.mapView = QCustomMapView(self.mapCard)
        self.mapView.setObjectName(u"mapView")
        self.mapView.setMinimumSize(QSize(0, 380))

        self.mapCardLayout.addWidget(self.mapView)


        self.verticalLayout.addWidget(self.mapCard)

        self.controlsCard = QFrame(self.centralwidget)
        self.controlsCard.setObjectName(u"controlsCard")
        self.controlsCard.setFrameShape(QFrame.StyledPanel)
        self.controlsLayout = QHBoxLayout(self.controlsCard)
        self.controlsLayout.setSpacing(8)
        self.controlsLayout.setObjectName(u"controlsLayout")
        self.controlsLayout.setContentsMargins(12, 8, 12, 8)
        self.styleCaption = QLabel(self.controlsCard)
        self.styleCaption.setObjectName(u"styleCaption")

        self.controlsLayout.addWidget(self.styleCaption)

        self.styleBox = QComboBox(self.controlsCard)
        self.styleBox.setObjectName(u"styleBox")
        self.styleBox.setMinimumSize(QSize(150, 0))

        self.controlsLayout.addWidget(self.styleBox)

        self.zoomCaption = QLabel(self.controlsCard)
        self.zoomCaption.setObjectName(u"zoomCaption")

        self.controlsLayout.addWidget(self.zoomCaption)

        self.zoomSlider = QSlider(self.controlsCard)
        self.zoomSlider.setObjectName(u"zoomSlider")
        self.zoomSlider.setMinimum(0)
        self.zoomSlider.setMaximum(20)
        self.zoomSlider.setValue(13)
        self.zoomSlider.setOrientation(Qt.Horizontal)

        self.controlsLayout.addWidget(self.zoomSlider)

        self.focusKbzBtn = QPushButton(self.controlsCard)
        self.focusKbzBtn.setObjectName(u"focusKbzBtn")

        self.controlsLayout.addWidget(self.focusKbzBtn)

        self.focusKcaBtn = QPushButton(self.controlsCard)
        self.focusKcaBtn.setObjectName(u"focusKcaBtn")

        self.controlsLayout.addWidget(self.focusKcaBtn)

        self.fitFleetBtn = QPushButton(self.controlsCard)
        self.fitFleetBtn.setObjectName(u"fitFleetBtn")

        self.controlsLayout.addWidget(self.fitFleetBtn)

        self.moveFleetBtn = QPushButton(self.controlsCard)
        self.moveFleetBtn.setObjectName(u"moveFleetBtn")

        self.controlsLayout.addWidget(self.moveFleetBtn)

        self.themeToggleBtn = QPushButton(self.controlsCard)
        self.themeToggleBtn.setObjectName(u"themeToggleBtn")

        self.controlsLayout.addWidget(self.themeToggleBtn)


        self.verticalLayout.addWidget(self.controlsCard)

        self.statusLabel = QLabel(self.centralwidget)
        self.statusLabel.setObjectName(u"statusLabel")

        self.verticalLayout.addWidget(self.statusLabel)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"QCustomMapView \u2014 Fleet Tracking", None))
        self.titleLabel.setText(QCoreApplication.translate("MainWindow", u"Fleet Tracking \u2014 QCustomMapView", None))
        self.offlineBadge.setText(QCoreApplication.translate("MainWindow", u"OFFLINE DEMO", None))
        self.styleCaption.setText(QCoreApplication.translate("MainWindow", u"Style", None))
        self.zoomCaption.setText(QCoreApplication.translate("MainWindow", u"Zoom", None))
        self.focusKbzBtn.setText(QCoreApplication.translate("MainWindow", u"Focus KBZ", None))
        self.focusKcaBtn.setText(QCoreApplication.translate("MainWindow", u"Focus KCA", None))
        self.fitFleetBtn.setText(QCoreApplication.translate("MainWindow", u"Fit fleet", None))
        self.moveFleetBtn.setText(QCoreApplication.translate("MainWindow", u"Move fleet", None))
        self.themeToggleBtn.setText(QCoreApplication.translate("MainWindow", u"Light / dark", None))
        self.statusLabel.setText(QCoreApplication.translate("MainWindow", u"starting the map engine...", None))
    # retranslateUi

