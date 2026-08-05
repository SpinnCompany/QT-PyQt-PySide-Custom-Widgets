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

from Custom_Widgets.QCustomLoadingIndicators import QCustomQProgressBar
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(900, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.mainLayout = QVBoxLayout(self.centralwidget)
        self.mainLayout.setSpacing(16)
        self.mainLayout.setObjectName(u"mainLayout")
        self.mainLayout.setContentsMargins(24, 24, 24, 24)
        self.titleLabel = QLabel(self.centralwidget)
        self.titleLabel.setObjectName(u"titleLabel")

        self.mainLayout.addWidget(self.titleLabel)

        self.topRow = QHBoxLayout()
        self.topRow.setSpacing(16)
        self.topRow.setObjectName(u"topRow")
        self.arcCard = QFrame(self.centralwidget)
        self.arcCard.setObjectName(u"arcCard")
        self.arcCard.setFrameShape(QFrame.StyledPanel)
        self.arcCardLayout = QVBoxLayout(self.arcCard)
        self.arcCardLayout.setSpacing(8)
        self.arcCardLayout.setObjectName(u"arcCardLayout")
        self.arcLabel = QLabel(self.arcCard)
        self.arcLabel.setObjectName(u"arcLabel")

        self.arcCardLayout.addWidget(self.arcLabel)

        self.arcHolder = QVBoxLayout()
        self.arcHolder.setObjectName(u"arcHolder")

        self.arcCardLayout.addLayout(self.arcHolder)


        self.topRow.addWidget(self.arcCard)

        self.circlesCard = QFrame(self.centralwidget)
        self.circlesCard.setObjectName(u"circlesCard")
        self.circlesCard.setFrameShape(QFrame.StyledPanel)
        self.circlesCardLayout = QVBoxLayout(self.circlesCard)
        self.circlesCardLayout.setSpacing(8)
        self.circlesCardLayout.setObjectName(u"circlesCardLayout")
        self.circlesLabel = QLabel(self.circlesCard)
        self.circlesLabel.setObjectName(u"circlesLabel")

        self.circlesCardLayout.addWidget(self.circlesLabel)

        self.circlesHolder = QVBoxLayout()
        self.circlesHolder.setObjectName(u"circlesHolder")

        self.circlesCardLayout.addLayout(self.circlesHolder)


        self.topRow.addWidget(self.circlesCard)

        self.spinnerCard = QFrame(self.centralwidget)
        self.spinnerCard.setObjectName(u"spinnerCard")
        self.spinnerCard.setFrameShape(QFrame.StyledPanel)
        self.spinnerCardLayout = QVBoxLayout(self.spinnerCard)
        self.spinnerCardLayout.setSpacing(8)
        self.spinnerCardLayout.setObjectName(u"spinnerCardLayout")
        self.spinnerLabel = QLabel(self.spinnerCard)
        self.spinnerLabel.setObjectName(u"spinnerLabel")

        self.spinnerCardLayout.addWidget(self.spinnerLabel)

        self.spinnerHolder = QHBoxLayout()
        self.spinnerHolder.setObjectName(u"spinnerHolder")

        self.spinnerCardLayout.addLayout(self.spinnerHolder)


        self.topRow.addWidget(self.spinnerCard)


        self.mainLayout.addLayout(self.topRow)

        self.bottomRow = QHBoxLayout()
        self.bottomRow.setSpacing(16)
        self.bottomRow.setObjectName(u"bottomRow")
        self.perlinCard = QFrame(self.centralwidget)
        self.perlinCard.setObjectName(u"perlinCard")
        self.perlinCard.setFrameShape(QFrame.StyledPanel)
        self.perlinCardLayout = QVBoxLayout(self.perlinCard)
        self.perlinCardLayout.setSpacing(8)
        self.perlinCardLayout.setObjectName(u"perlinCardLayout")
        self.perlinLabel = QLabel(self.perlinCard)
        self.perlinLabel.setObjectName(u"perlinLabel")

        self.perlinCardLayout.addWidget(self.perlinLabel)

        self.perlinHolder = QVBoxLayout()
        self.perlinHolder.setObjectName(u"perlinHolder")

        self.perlinCardLayout.addLayout(self.perlinHolder)


        self.bottomRow.addWidget(self.perlinCard)

        self.progressCard = QFrame(self.centralwidget)
        self.progressCard.setObjectName(u"progressCard")
        self.progressCard.setFrameShape(QFrame.StyledPanel)
        self.progressCardLayout = QVBoxLayout(self.progressCard)
        self.progressCardLayout.setSpacing(12)
        self.progressCardLayout.setObjectName(u"progressCardLayout")
        self.progressLabel = QLabel(self.progressCard)
        self.progressLabel.setObjectName(u"progressLabel")

        self.progressCardLayout.addWidget(self.progressLabel)

        self.inProgressBar = QCustomQProgressBar(self.progressCard)
        self.inProgressBar.setObjectName(u"inProgressBar")

        self.progressCardLayout.addWidget(self.inProgressBar)

        self.pauseButton = QPushButton(self.progressCard)
        self.pauseButton.setObjectName(u"pauseButton")

        self.progressCardLayout.addWidget(self.pauseButton, 0, Qt.AlignHCenter)

        self.progressSpacer = QSpacerItem(10, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.progressCardLayout.addItem(self.progressSpacer)


        self.bottomRow.addWidget(self.progressCard)


        self.mainLayout.addLayout(self.bottomRow)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Loading Indicators", None))
        self.titleLabel.setText(QCoreApplication.translate("MainWindow", u"Loading Indicators", None))
        self.arcLabel.setText(QCoreApplication.translate("MainWindow", u"QCustomArcLoader", None))
        self.circlesLabel.setText(QCoreApplication.translate("MainWindow", u"QCustom3CirclesLoader", None))
        self.spinnerLabel.setText(QCoreApplication.translate("MainWindow", u"QCustomSpinner \u2014 Bounce and Smooth", None))
        self.perlinLabel.setText(QCoreApplication.translate("MainWindow", u"QCustomPerlinLoader", None))
        self.progressLabel.setText(QCoreApplication.translate("MainWindow", u"QCustomQProgressBar \u2014 indeterminate", None))
        self.pauseButton.setText(QCoreApplication.translate("MainWindow", u"Pause", None))
    # retranslateUi

