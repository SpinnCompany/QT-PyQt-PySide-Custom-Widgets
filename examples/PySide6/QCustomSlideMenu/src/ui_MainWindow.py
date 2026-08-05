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
from PySide6.QtWidgets import (QApplication, QFrame, QLabel, QMainWindow,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

from Custom_Widgets.QCustomSlideMenu import QCustomSlideMenu
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(520, 420)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.titleLabel = QLabel(self.centralwidget)
        self.titleLabel.setObjectName(u"titleLabel")

        self.verticalLayout.addWidget(self.titleLabel)

        self.menuToggleButton = QPushButton(self.centralwidget)
        self.menuToggleButton.setObjectName(u"menuToggleButton")
        self.menuToggleButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.menuToggleButton.setIconSize(QSize(18, 18))

        self.verticalLayout.addWidget(self.menuToggleButton)

        self.slideMenu = QCustomSlideMenu(self.centralwidget)
        self.slideMenu.setObjectName(u"slideMenu")
        self.slideMenuLayout = QVBoxLayout(self.slideMenu)
        self.slideMenuLayout.setObjectName(u"slideMenuLayout")
        self.menuContentFrame = QFrame(self.slideMenu)
        self.menuContentFrame.setObjectName(u"menuContentFrame")
        self.menuContentFrame.setFrameShape(QFrame.StyledPanel)
        self.menuContentLayout = QVBoxLayout(self.menuContentFrame)
        self.menuContentLayout.setObjectName(u"menuContentLayout")
        self.menuContentLabel = QLabel(self.menuContentFrame)
        self.menuContentLabel.setObjectName(u"menuContentLabel")
        self.menuContentLabel.setAlignment(Qt.AlignCenter)

        self.menuContentLayout.addWidget(self.menuContentLabel)

        self.menuHintLabel = QLabel(self.menuContentFrame)
        self.menuHintLabel.setObjectName(u"menuHintLabel")
        self.menuHintLabel.setWordWrap(True)
        self.menuHintLabel.setAlignment(Qt.AlignCenter)

        self.menuContentLayout.addWidget(self.menuHintLabel)


        self.slideMenuLayout.addWidget(self.menuContentFrame)


        self.verticalLayout.addWidget(self.slideMenu)

        self.bottomSpacer = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.bottomSpacer)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"QCustomSlideMenu Showcase", None))
        self.titleLabel.setText(QCoreApplication.translate("MainWindow", u"Sliding Menu / Container", None))
        self.menuToggleButton.setText(QCoreApplication.translate("MainWindow", u"Toggle Menu", None))
        self.menuContentLabel.setText(QCoreApplication.translate("MainWindow", u"My Responsive Widget", None))
        self.menuHintLabel.setText(QCoreApplication.translate("MainWindow", u"This container expands and collapses with an animated slide. Its expanded size is \"auto\" \u2014 it grows to fit this content.", None))
    # retranslateUi

