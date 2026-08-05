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
    QMainWindow, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

from Custom_Widgets.QCustomCarousel import QCustomCarousel
from Custom_Widgets.QCustomKbd import QCustomKbd
from Custom_Widgets.QCustomSplitter import QCustomSplitter
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(720, 620)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(14)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(18, 18, 18, 18)
        self.kbdSectionLabel = QLabel(self.centralwidget)
        self.kbdSectionLabel.setObjectName(u"kbdSectionLabel")

        self.verticalLayout.addWidget(self.kbdSectionLabel)

        self.kbdRow = QHBoxLayout()
        self.kbdRow.setSpacing(16)
        self.kbdRow.setObjectName(u"kbdRow")
        self.paletteLabel = QLabel(self.centralwidget)
        self.paletteLabel.setObjectName(u"paletteLabel")

        self.kbdRow.addWidget(self.paletteLabel)

        self.paletteKbd = QCustomKbd(self.centralwidget)
        self.paletteKbd.setObjectName(u"paletteKbd")

        self.kbdRow.addWidget(self.paletteKbd)

        self.saveLabel = QLabel(self.centralwidget)
        self.saveLabel.setObjectName(u"saveLabel")

        self.kbdRow.addWidget(self.saveLabel)

        self.saveKbd = QCustomKbd(self.centralwidget)
        self.saveKbd.setObjectName(u"saveKbd")

        self.kbdRow.addWidget(self.saveKbd)

        self.closeLabel = QLabel(self.centralwidget)
        self.closeLabel.setObjectName(u"closeLabel")

        self.kbdRow.addWidget(self.closeLabel)

        self.closeKbd = QCustomKbd(self.centralwidget)
        self.closeKbd.setObjectName(u"closeKbd")

        self.kbdRow.addWidget(self.closeKbd)

        self.kbdSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.kbdRow.addItem(self.kbdSpacer)


        self.verticalLayout.addLayout(self.kbdRow)

        self.splitterSectionLabel = QLabel(self.centralwidget)
        self.splitterSectionLabel.setObjectName(u"splitterSectionLabel")

        self.verticalLayout.addWidget(self.splitterSectionLabel)

        self.splitter = QCustomSplitter(self.centralwidget)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setMinimumSize(QSize(0, 150))
        self.splitter.setOrientation(Qt.Horizontal)
        self.sidebarPanel = QFrame(self.splitter)
        self.sidebarPanel.setObjectName(u"sidebarPanel")
        self.sidebarLayout = QVBoxLayout(self.sidebarPanel)
        self.sidebarLayout.setObjectName(u"sidebarLayout")
        self.sidebarLayout.setContentsMargins(16, 16, 16, 16)
        self.sidebarTitle = QLabel(self.sidebarPanel)
        self.sidebarTitle.setObjectName(u"sidebarTitle")

        self.sidebarLayout.addWidget(self.sidebarTitle)

        self.sidebarBody = QLabel(self.sidebarPanel)
        self.sidebarBody.setObjectName(u"sidebarBody")
        self.sidebarBody.setWordWrap(True)
        self.sidebarBody.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.sidebarLayout.addWidget(self.sidebarBody)

        self.splitter.addWidget(self.sidebarPanel)
        self.editorPanel = QFrame(self.splitter)
        self.editorPanel.setObjectName(u"editorPanel")
        self.editorLayout = QVBoxLayout(self.editorPanel)
        self.editorLayout.setObjectName(u"editorLayout")
        self.editorLayout.setContentsMargins(16, 16, 16, 16)
        self.editorTitle = QLabel(self.editorPanel)
        self.editorTitle.setObjectName(u"editorTitle")

        self.editorLayout.addWidget(self.editorTitle)

        self.editorBody = QLabel(self.editorPanel)
        self.editorBody.setObjectName(u"editorBody")
        self.editorBody.setWordWrap(True)
        self.editorBody.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.editorLayout.addWidget(self.editorBody)

        self.splitter.addWidget(self.editorPanel)
        self.previewPanel = QFrame(self.splitter)
        self.previewPanel.setObjectName(u"previewPanel")
        self.previewLayout = QVBoxLayout(self.previewPanel)
        self.previewLayout.setObjectName(u"previewLayout")
        self.previewLayout.setContentsMargins(16, 16, 16, 16)
        self.previewTitle = QLabel(self.previewPanel)
        self.previewTitle.setObjectName(u"previewTitle")

        self.previewLayout.addWidget(self.previewTitle)

        self.previewBody = QLabel(self.previewPanel)
        self.previewBody.setObjectName(u"previewBody")
        self.previewBody.setWordWrap(True)
        self.previewBody.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.previewLayout.addWidget(self.previewBody)

        self.splitter.addWidget(self.previewPanel)

        self.verticalLayout.addWidget(self.splitter)

        self.carouselSectionLabel = QLabel(self.centralwidget)
        self.carouselSectionLabel.setObjectName(u"carouselSectionLabel")

        self.verticalLayout.addWidget(self.carouselSectionLabel)

        self.carousel = QCustomCarousel(self.centralwidget)
        self.carousel.setObjectName(u"carousel")
        self.carousel.setMinimumSize(QSize(0, 140))

        self.verticalLayout.addWidget(self.carousel)

        self.verticalLayout.setStretch(3, 1)
        self.verticalLayout.setStretch(5, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Kbd / Splitter / Carousel", None))
        self.kbdSectionLabel.setText(QCoreApplication.translate("MainWindow", u"Keyboard shortcuts", None))
        self.paletteLabel.setText(QCoreApplication.translate("MainWindow", u"Command palette", None))
        self.paletteKbd.setProperty(u"keys", QCoreApplication.translate("MainWindow", u"Ctrl+K", None))
        self.saveLabel.setText(QCoreApplication.translate("MainWindow", u"Save all", None))
        self.saveKbd.setProperty(u"keys", QCoreApplication.translate("MainWindow", u"Ctrl+Shift+S", None))
        self.closeLabel.setText(QCoreApplication.translate("MainWindow", u"Close", None))
        self.closeKbd.setProperty(u"keys", QCoreApplication.translate("MainWindow", u"Alt+F4", None))
        self.splitterSectionLabel.setText(QCoreApplication.translate("MainWindow", u"Resizable splitter (drag the handles)", None))
        self.sidebarTitle.setText(QCoreApplication.translate("MainWindow", u"Sidebar", None))
        self.sidebarBody.setText(QCoreApplication.translate("MainWindow", u"Navigation, files, and outline live here.", None))
        self.editorTitle.setText(QCoreApplication.translate("MainWindow", u"Editor", None))
        self.editorBody.setText(QCoreApplication.translate("MainWindow", u"The main working area. Drag a handle to resize.", None))
        self.previewTitle.setText(QCoreApplication.translate("MainWindow", u"Preview", None))
        self.previewBody.setText(QCoreApplication.translate("MainWindow", u"Live output / preview pane.", None))
        self.carouselSectionLabel.setText(QCoreApplication.translate("MainWindow", u"Carousel (auto-advances every 2.5s)", None))
    # retranslateUi

