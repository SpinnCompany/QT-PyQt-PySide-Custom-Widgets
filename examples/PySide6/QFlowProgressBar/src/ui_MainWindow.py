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
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.mainLayout = QVBoxLayout(self.centralwidget)
        self.mainLayout.setSpacing(16)
        self.mainLayout.setObjectName(u"mainLayout")
        self.mainLayout.setContentsMargins(24, 24, 24, 24)
        self.titleLabel = QLabel(self.centralwidget)
        self.titleLabel.setObjectName(u"titleLabel")

        self.mainLayout.addWidget(self.titleLabel)

        self.circularCard = QFrame(self.centralwidget)
        self.circularCard.setObjectName(u"circularCard")
        self.circularCard.setFrameShape(QFrame.StyledPanel)
        self.circularCardLayout = QVBoxLayout(self.circularCard)
        self.circularCardLayout.setSpacing(8)
        self.circularCardLayout.setObjectName(u"circularCardLayout")
        self.circularLabel = QLabel(self.circularCard)
        self.circularLabel.setObjectName(u"circularLabel")

        self.circularCardLayout.addWidget(self.circularLabel)

        self.circularHolder = QVBoxLayout()
        self.circularHolder.setObjectName(u"circularHolder")

        self.circularCardLayout.addLayout(self.circularHolder)


        self.mainLayout.addWidget(self.circularCard)

        self.flatCard = QFrame(self.centralwidget)
        self.flatCard.setObjectName(u"flatCard")
        self.flatCard.setFrameShape(QFrame.StyledPanel)
        self.flatCardLayout = QVBoxLayout(self.flatCard)
        self.flatCardLayout.setSpacing(8)
        self.flatCardLayout.setObjectName(u"flatCardLayout")
        self.flatLabel = QLabel(self.flatCard)
        self.flatLabel.setObjectName(u"flatLabel")

        self.flatCardLayout.addWidget(self.flatLabel)

        self.flatHolder = QVBoxLayout()
        self.flatHolder.setObjectName(u"flatHolder")

        self.flatCardLayout.addLayout(self.flatHolder)


        self.mainLayout.addWidget(self.flatCard)

        self.squareCard = QFrame(self.centralwidget)
        self.squareCard.setObjectName(u"squareCard")
        self.squareCard.setFrameShape(QFrame.StyledPanel)
        self.squareCardLayout = QVBoxLayout(self.squareCard)
        self.squareCardLayout.setSpacing(8)
        self.squareCardLayout.setObjectName(u"squareCardLayout")
        self.squareLabel = QLabel(self.squareCard)
        self.squareLabel.setObjectName(u"squareLabel")

        self.squareCardLayout.addWidget(self.squareLabel)

        self.squareHolder = QVBoxLayout()
        self.squareHolder.setObjectName(u"squareHolder")

        self.squareCardLayout.addLayout(self.squareHolder)


        self.mainLayout.addWidget(self.squareCard)

        self.buttonRow = QHBoxLayout()
        self.buttonRow.setSpacing(8)
        self.buttonRow.setObjectName(u"buttonRow")
        self.nextButton = QPushButton(self.centralwidget)
        self.nextButton.setObjectName(u"nextButton")

        self.buttonRow.addWidget(self.nextButton)

        self.prevButton = QPushButton(self.centralwidget)
        self.prevButton.setObjectName(u"prevButton")

        self.buttonRow.addWidget(self.prevButton)

        self.buttonSpacer = QSpacerItem(10, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.buttonRow.addItem(self.buttonSpacer)


        self.mainLayout.addLayout(self.buttonRow)

        self.bottomSpacer = QSpacerItem(10, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.mainLayout.addItem(self.bottomSpacer)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"QFlowProgressBar", None))
        self.titleLabel.setText(QCoreApplication.translate("MainWindow", u"Flow Progress Bars", None))
        self.circularLabel.setText(QCoreApplication.translate("MainWindow", u"Circular style", None))
        self.flatLabel.setText(QCoreApplication.translate("MainWindow", u"Flat style", None))
        self.squareLabel.setText(QCoreApplication.translate("MainWindow", u"Square style", None))
        self.nextButton.setText(QCoreApplication.translate("MainWindow", u"Next Step", None))
        self.prevButton.setText(QCoreApplication.translate("MainWindow", u"Previous Step", None))
    # retranslateUi

