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
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QHBoxLayout,
    QLabel, QMainWindow, QPushButton, QSizePolicy,
    QVBoxLayout, QWidget)

from Custom_Widgets.QCustomQPushButton import QCustomQPushButton
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(640, 480)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.rootLayout = QVBoxLayout(self.centralwidget)
        self.rootLayout.setSpacing(0)
        self.rootLayout.setObjectName(u"rootLayout")
        self.rootLayout.setContentsMargins(0, 0, 0, 0)
        self.header = QFrame(self.centralwidget)
        self.header.setObjectName(u"header")
        self.header.setMinimumSize(QSize(0, 120))
        self.header.setMaximumSize(QSize(16777215, 120))
        self.header.setFrameShape(QFrame.Shape.StyledPanel)
        self.headerLayout = QVBoxLayout(self.header)
        self.headerLayout.setSpacing(8)
        self.headerLayout.setObjectName(u"headerLayout")
        self.headerLayout.setContentsMargins(32, 32, 32, 24)
        self.title = QLabel(self.header)
        self.title.setObjectName(u"title")

        self.headerLayout.addWidget(self.title)

        self.subtitle = QLabel(self.header)
        self.subtitle.setObjectName(u"subtitle")
        self.subtitle.setWordWrap(True)

        self.headerLayout.addWidget(self.subtitle)


        self.rootLayout.addWidget(self.header)

        self.content = QFrame(self.centralwidget)
        self.content.setObjectName(u"content")
        self.content.setFrameShape(QFrame.Shape.StyledPanel)
        self.contentLayout = QVBoxLayout(self.content)
        self.contentLayout.setSpacing(16)
        self.contentLayout.setObjectName(u"contentLayout")
        self.contentLayout.setContentsMargins(32, 24, 32, 32)
        self.card = QFrame(self.content)
        self.card.setObjectName(u"card")
        self.card.setFrameShape(QFrame.Shape.StyledPanel)
        self.cardLayout = QVBoxLayout(self.card)
        self.cardLayout.setSpacing(12)
        self.cardLayout.setObjectName(u"cardLayout")
        self.cardLayout.setContentsMargins(20, 20, 20, 20)
        self.cardTitle = QLabel(self.card)
        self.cardTitle.setObjectName(u"cardTitle")

        self.cardLayout.addWidget(self.cardTitle)

        self.buttonGrid = QGridLayout()
        self.buttonGrid.setSpacing(12)
        self.buttonGrid.setObjectName(u"buttonGrid")
        self.infoBtn = QCustomQPushButton(self.card)
        self.infoBtn.setObjectName(u"infoBtn")
        self.infoBtn.setIconSize(QSize(18, 18))

        self.buttonGrid.addWidget(self.infoBtn, 0, 0, 1, 1)

        self.confirmBtn = QCustomQPushButton(self.card)
        self.confirmBtn.setObjectName(u"confirmBtn")
        self.confirmBtn.setIconSize(QSize(18, 18))

        self.buttonGrid.addWidget(self.confirmBtn, 0, 1, 1, 1)

        self.warningBtn = QCustomQPushButton(self.card)
        self.warningBtn.setObjectName(u"warningBtn")
        self.warningBtn.setIconSize(QSize(18, 18))

        self.buttonGrid.addWidget(self.warningBtn, 1, 0, 1, 1)

        self.errorBtn = QCustomQPushButton(self.card)
        self.errorBtn.setObjectName(u"errorBtn")
        self.errorBtn.setIconSize(QSize(18, 18))

        self.buttonGrid.addWidget(self.errorBtn, 1, 1, 1, 1)


        self.cardLayout.addLayout(self.buttonGrid)


        self.contentLayout.addWidget(self.card)

        self.statusCard = QFrame(self.content)
        self.statusCard.setObjectName(u"statusCard")
        self.statusCard.setFrameShape(QFrame.Shape.StyledPanel)
        self.statusLayout = QHBoxLayout(self.statusCard)
        self.statusLayout.setSpacing(12)
        self.statusLayout.setObjectName(u"statusLayout")
        self.statusLayout.setContentsMargins(16, 12, 16, 12)
        self.statusIcon = QLabel(self.statusCard)
        self.statusIcon.setObjectName(u"statusIcon")
        self.statusIcon.setMinimumSize(QSize(8, 8))
        self.statusIcon.setMaximumSize(QSize(8, 8))

        self.statusLayout.addWidget(self.statusIcon)

        self.statusLabel = QLabel(self.statusCard)
        self.statusLabel.setObjectName(u"statusLabel")

        self.statusLayout.addWidget(self.statusLabel)


        self.contentLayout.addWidget(self.statusCard)


        self.rootLayout.addWidget(self.content)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"QCustomQDialog Showcase", None))
        self.title.setText(QCoreApplication.translate("MainWindow", u"Dialog Showcase", None))
        self.subtitle.setText(QCoreApplication.translate("MainWindow", u"Click a button to trigger a styled dialog with animations and feedback", None))
        self.cardTitle.setText(QCoreApplication.translate("MainWindow", u"Dialog Types", None))
        self.infoBtn.setText(QCoreApplication.translate("MainWindow", u"Info", None))
        self.infoBtn.setProperty(u"variant", QCoreApplication.translate("MainWindow", u"primary", None))
        self.confirmBtn.setText(QCoreApplication.translate("MainWindow", u"Confirm", None))
        self.warningBtn.setText(QCoreApplication.translate("MainWindow", u"Warning", None))
        self.warningBtn.setProperty(u"sizeVariant", QCoreApplication.translate("MainWindow", u"md", None))
        self.errorBtn.setText(QCoreApplication.translate("MainWindow", u"Error", None))
        self.statusIcon.setText("")
        self.statusLabel.setText(QCoreApplication.translate("MainWindow", u"Click a dialog type above", None))
    # retranslateUi

