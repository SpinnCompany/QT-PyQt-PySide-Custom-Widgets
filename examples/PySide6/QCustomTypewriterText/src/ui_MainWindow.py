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
    QMainWindow, QPushButton, QSizePolicy, QSlider,
    QSpacerItem, QVBoxLayout, QWidget)

from Custom_Widgets.QCustomTypewriterText import QCustomTypewriterText
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(620, 300)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.mainLayout = QVBoxLayout(self.centralwidget)
        self.mainLayout.setSpacing(16)
        self.mainLayout.setObjectName(u"mainLayout")
        self.mainLayout.setContentsMargins(24, 24, 24, 24)
        self.typerCard = QFrame(self.centralwidget)
        self.typerCard.setObjectName(u"typerCard")
        self.typerCard.setFrameShape(QFrame.StyledPanel)
        self.typerCardLayout = QVBoxLayout(self.typerCard)
        self.typerCardLayout.setSpacing(12)
        self.typerCardLayout.setObjectName(u"typerCardLayout")
        self.typewriterText = QCustomTypewriterText(self.typerCard)
        self.typewriterText.setObjectName(u"typewriterText")
        self.typewriterText.setProperty(u"typeSpeed", 65)

        self.typerCardLayout.addWidget(self.typewriterText)

        self.statusLabel = QLabel(self.typerCard)
        self.statusLabel.setObjectName(u"statusLabel")

        self.typerCardLayout.addWidget(self.statusLabel)


        self.mainLayout.addWidget(self.typerCard)

        self.controlsRow = QHBoxLayout()
        self.controlsRow.setSpacing(8)
        self.controlsRow.setObjectName(u"controlsRow")
        self.speedLabel = QLabel(self.centralwidget)
        self.speedLabel.setObjectName(u"speedLabel")

        self.controlsRow.addWidget(self.speedLabel)

        self.speedSlider = QSlider(self.centralwidget)
        self.speedSlider.setObjectName(u"speedSlider")
        self.speedSlider.setMinimum(10)
        self.speedSlider.setMaximum(200)
        self.speedSlider.setValue(65)
        self.speedSlider.setOrientation(Qt.Horizontal)

        self.controlsRow.addWidget(self.speedSlider)

        self.startButton = QPushButton(self.centralwidget)
        self.startButton.setObjectName(u"startButton")

        self.controlsRow.addWidget(self.startButton)

        self.stopButton = QPushButton(self.centralwidget)
        self.stopButton.setObjectName(u"stopButton")

        self.controlsRow.addWidget(self.stopButton)

        self.skipButton = QPushButton(self.centralwidget)
        self.skipButton.setObjectName(u"skipButton")

        self.controlsRow.addWidget(self.skipButton)

        self.caretButton = QPushButton(self.centralwidget)
        self.caretButton.setObjectName(u"caretButton")

        self.controlsRow.addWidget(self.caretButton)

        self.themeButton = QPushButton(self.centralwidget)
        self.themeButton.setObjectName(u"themeButton")

        self.controlsRow.addWidget(self.themeButton)

        self.controlsSpacer = QSpacerItem(10, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.controlsRow.addItem(self.controlsSpacer)


        self.mainLayout.addLayout(self.controlsRow)

        self.bottomSpacer = QSpacerItem(10, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.mainLayout.addItem(self.bottomSpacer)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"QCustomTypewriterText", None))
        self.statusLabel.setText(QCoreApplication.translate("MainWindow", u"typing...", None))
        self.speedLabel.setText(QCoreApplication.translate("MainWindow", u"Speed", None))
        self.startButton.setText(QCoreApplication.translate("MainWindow", u"Start", None))
        self.stopButton.setText(QCoreApplication.translate("MainWindow", u"Stop", None))
        self.skipButton.setText(QCoreApplication.translate("MainWindow", u"Skip", None))
        self.caretButton.setText(QCoreApplication.translate("MainWindow", u"Caret", None))
        self.themeButton.setText(QCoreApplication.translate("MainWindow", u"Light / dark", None))
    # retranslateUi

