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
    QMainWindow, QPushButton, QSizePolicy, QVBoxLayout,
    QWidget)
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(568, 320)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralLayout = QHBoxLayout(self.centralwidget)
        self.centralLayout.setSpacing(0)
        self.centralLayout.setObjectName(u"centralLayout")
        self.mainBody = QFrame(self.centralwidget)
        self.mainBody.setObjectName(u"mainBody")
        self.mainBody.setFrameShape(QFrame.StyledPanel)
        self.mainBodyLayout = QVBoxLayout(self.mainBody)
        self.mainBodyLayout.setSpacing(0)
        self.mainBodyLayout.setObjectName(u"mainBodyLayout")
        self.headerWidget = QWidget(self.mainBody)
        self.headerWidget.setObjectName(u"headerWidget")
        self.headerLayout = QHBoxLayout(self.headerWidget)
        self.headerLayout.setSpacing(0)
        self.headerLayout.setObjectName(u"headerLayout")
        self.titleBarLabel = QLabel(self.headerWidget)
        self.titleBarLabel.setObjectName(u"titleBarLabel")

        self.headerLayout.addWidget(self.titleBarLabel)

        self.windowButtonsFrame = QFrame(self.headerWidget)
        self.windowButtonsFrame.setObjectName(u"windowButtonsFrame")
        self.windowButtonsFrame.setFrameShape(QFrame.StyledPanel)
        self.windowButtonsLayout = QHBoxLayout(self.windowButtonsFrame)
        self.windowButtonsLayout.setSpacing(0)
        self.windowButtonsLayout.setObjectName(u"windowButtonsLayout")
        self.minimizeWindowButton = QPushButton(self.windowButtonsFrame)
        self.minimizeWindowButton.setObjectName(u"minimizeWindowButton")
        self.minimizeWindowButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon = QIcon()
        icon.addFile(u"theme-icons:icons/feather/minus.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.minimizeWindowButton.setIcon(icon)

        self.windowButtonsLayout.addWidget(self.minimizeWindowButton)

        self.restoreWindowButton = QPushButton(self.windowButtonsFrame)
        self.restoreWindowButton.setObjectName(u"restoreWindowButton")
        self.restoreWindowButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon1 = QIcon()
        icon1.addFile(u"theme-icons:icons/feather/maximize-2.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.restoreWindowButton.setIcon(icon1)

        self.windowButtonsLayout.addWidget(self.restoreWindowButton)

        self.closeWindowButton = QPushButton(self.windowButtonsFrame)
        self.closeWindowButton.setObjectName(u"closeWindowButton")
        self.closeWindowButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon2 = QIcon()
        icon2.addFile(u"theme-icons:icons/feather/x.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.closeWindowButton.setIcon(icon2)

        self.windowButtonsLayout.addWidget(self.closeWindowButton)


        self.headerLayout.addWidget(self.windowButtonsFrame, 0, Qt.AlignRight|Qt.AlignTop)


        self.mainBodyLayout.addWidget(self.headerWidget)

        self.bodyFrame = QFrame(self.mainBody)
        self.bodyFrame.setObjectName(u"bodyFrame")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bodyFrame.sizePolicy().hasHeightForWidth())
        self.bodyFrame.setSizePolicy(sizePolicy)
        self.bodyFrame.setFrameShape(QFrame.StyledPanel)
        self.bodyLayout = QVBoxLayout(self.bodyFrame)
        self.bodyLayout.setSpacing(0)
        self.bodyLayout.setObjectName(u"bodyLayout")
        self.logoLabel = QLabel(self.bodyFrame)
        self.logoLabel.setObjectName(u"logoLabel")
        self.logoLabel.setMinimumSize(QSize(60, 60))
        self.logoLabel.setMaximumSize(QSize(60, 60))
        self.logoLabel.setPixmap(QPixmap(u"theme-icons:icons/feather/github.svg"))
        self.logoLabel.setAlignment(Qt.AlignCenter)

        self.bodyLayout.addWidget(self.logoLabel, 0, Qt.AlignHCenter|Qt.AlignBottom)

        self.brandLabel = QLabel(self.bodyFrame)
        self.brandLabel.setObjectName(u"brandLabel")
        self.brandLabel.setAlignment(Qt.AlignCenter)

        self.bodyLayout.addWidget(self.brandLabel, 0, Qt.AlignHCenter|Qt.AlignTop)

        self.footerFrame = QFrame(self.bodyFrame)
        self.footerFrame.setObjectName(u"footerFrame")
        self.footerFrame.setFrameShape(QFrame.StyledPanel)
        self.footerLayout = QHBoxLayout(self.footerFrame)
        self.footerLayout.setSpacing(0)
        self.footerLayout.setObjectName(u"footerLayout")
        self.sizeGrip = QFrame(self.footerFrame)
        self.sizeGrip.setObjectName(u"sizeGrip")
        self.sizeGrip.setMinimumSize(QSize(10, 10))
        self.sizeGrip.setMaximumSize(QSize(10, 10))
        self.sizeGrip.setFrameShape(QFrame.StyledPanel)

        self.footerLayout.addWidget(self.sizeGrip, 0, Qt.AlignRight|Qt.AlignBottom)


        self.bodyLayout.addWidget(self.footerFrame)


        self.mainBodyLayout.addWidget(self.bodyFrame)


        self.centralLayout.addWidget(self.mainBody)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"QCustomQMainWindow Starter", None))
        self.titleBarLabel.setText(QCoreApplication.translate("MainWindow", u"CUSTOM TITLE BAR", None))
        self.minimizeWindowButton.setText("")
        self.restoreWindowButton.setText("")
        self.closeWindowButton.setText("")
        self.logoLabel.setText("")
        self.brandLabel.setText(QCoreApplication.translate("MainWindow", u"GITHUB", None))
    # retranslateUi

