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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QMainWindow,
    QPushButton, QSizePolicy, QVBoxLayout, QWidget)
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 471)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(16)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(16, 16, 16, 16)
        self.cardRowTop = QWidget(self.centralwidget)
        self.cardRowTop.setObjectName(u"cardRowTop")
        self.cardRowTopLayout = QHBoxLayout(self.cardRowTop)
        self.cardRowTopLayout.setSpacing(16)
        self.cardRowTopLayout.setObjectName(u"cardRowTopLayout")
        self.card1 = QWidget(self.cardRowTop)
        self.card1.setObjectName(u"card1")
        self.card1Layout = QVBoxLayout(self.card1)
        self.card1Layout.setObjectName(u"card1Layout")
        self.cardLabel1 = QLabel(self.card1)
        self.cardLabel1.setObjectName(u"cardLabel1")
        self.cardLabel1.setAlignment(Qt.AlignCenter)

        self.card1Layout.addWidget(self.cardLabel1)


        self.cardRowTopLayout.addWidget(self.card1)

        self.card2 = QWidget(self.cardRowTop)
        self.card2.setObjectName(u"card2")
        self.card2Layout = QVBoxLayout(self.card2)
        self.card2Layout.setObjectName(u"card2Layout")
        self.cardLabel2 = QLabel(self.card2)
        self.cardLabel2.setObjectName(u"cardLabel2")
        self.cardLabel2.setAlignment(Qt.AlignCenter)

        self.card2Layout.addWidget(self.cardLabel2)


        self.cardRowTopLayout.addWidget(self.card2)

        self.card3 = QWidget(self.cardRowTop)
        self.card3.setObjectName(u"card3")
        self.card3Layout = QVBoxLayout(self.card3)
        self.card3Layout.setObjectName(u"card3Layout")
        self.cardLabel3 = QLabel(self.card3)
        self.cardLabel3.setObjectName(u"cardLabel3")
        self.cardLabel3.setAlignment(Qt.AlignCenter)

        self.card3Layout.addWidget(self.cardLabel3)


        self.cardRowTopLayout.addWidget(self.card3)


        self.verticalLayout.addWidget(self.cardRowTop)

        self.cardRowBottom = QWidget(self.centralwidget)
        self.cardRowBottom.setObjectName(u"cardRowBottom")
        self.cardRowBottomLayout = QHBoxLayout(self.cardRowBottom)
        self.cardRowBottomLayout.setSpacing(16)
        self.cardRowBottomLayout.setObjectName(u"cardRowBottomLayout")
        self.card4 = QWidget(self.cardRowBottom)
        self.card4.setObjectName(u"card4")
        self.card4Layout = QVBoxLayout(self.card4)
        self.card4Layout.setObjectName(u"card4Layout")
        self.cardLabel4 = QLabel(self.card4)
        self.cardLabel4.setObjectName(u"cardLabel4")
        self.cardLabel4.setAlignment(Qt.AlignCenter)

        self.card4Layout.addWidget(self.cardLabel4)


        self.cardRowBottomLayout.addWidget(self.card4)

        self.card5 = QWidget(self.cardRowBottom)
        self.card5.setObjectName(u"card5")
        self.card5Layout = QVBoxLayout(self.card5)
        self.card5Layout.setObjectName(u"card5Layout")
        self.cardLabel5 = QLabel(self.card5)
        self.cardLabel5.setObjectName(u"cardLabel5")
        self.cardLabel5.setAlignment(Qt.AlignCenter)

        self.card5Layout.addWidget(self.cardLabel5)


        self.cardRowBottomLayout.addWidget(self.card5)

        self.card6 = QWidget(self.cardRowBottom)
        self.card6.setObjectName(u"card6")
        self.card6Layout = QVBoxLayout(self.card6)
        self.card6Layout.setObjectName(u"card6Layout")
        self.cardLabel6 = QLabel(self.card6)
        self.cardLabel6.setObjectName(u"cardLabel6")
        self.cardLabel6.setAlignment(Qt.AlignCenter)

        self.card6Layout.addWidget(self.cardLabel6)


        self.cardRowBottomLayout.addWidget(self.card6)


        self.verticalLayout.addWidget(self.cardRowBottom)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"QCard Showcase", None))
        self.cardLabel1.setText(QCoreApplication.translate("MainWindow", u"Card 1", None))
        self.cardLabel2.setText(QCoreApplication.translate("MainWindow", u"Card 2", None))
        self.cardLabel3.setText(QCoreApplication.translate("MainWindow", u"Card 3", None))
        self.cardLabel4.setText(QCoreApplication.translate("MainWindow", u"Card 4", None))
        self.cardLabel5.setText(QCoreApplication.translate("MainWindow", u"Card 5", None))
        self.cardLabel6.setText(QCoreApplication.translate("MainWindow", u"Card 6", None))
    # retranslateUi

