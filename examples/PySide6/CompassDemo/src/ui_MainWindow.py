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
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QLabel,
    QMainWindow, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

from Custom_Widgets.QCustomCompass import QCustomCompass
from Custom_Widgets.QCustomCompassDial import QCustomCompassDial
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(880, 560)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.cardsGrid = QGridLayout(self.centralwidget)
        self.cardsGrid.setObjectName(u"cardsGrid")
        self.cardsGrid.setHorizontalSpacing(20)
        self.cardsGrid.setVerticalSpacing(20)
        self.cardsGrid.setContentsMargins(24, 24, 24, 24)
        self.roseCard = QFrame(self.centralwidget)
        self.roseCard.setObjectName(u"roseCard")
        self.roseCard.setFrameShape(QFrame.NoFrame)
        self.roseLayout = QVBoxLayout(self.roseCard)
        self.roseLayout.setSpacing(2)
        self.roseLayout.setObjectName(u"roseLayout")
        self.roseLayout.setContentsMargins(20, 16, 20, 16)
        self.roseTitle = QLabel(self.roseCard)
        self.roseTitle.setObjectName(u"roseTitle")

        self.roseLayout.addWidget(self.roseTitle)

        self.roseSub = QLabel(self.roseCard)
        self.roseSub.setObjectName(u"roseSub")

        self.roseLayout.addWidget(self.roseSub)

        self.roseSpacer = QSpacerItem(0, 8, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.roseLayout.addItem(self.roseSpacer)

        self.roseCompass = QCustomCompass(self.roseCard)
        self.roseCompass.setObjectName(u"roseCompass")
        self.roseCompass.setProperty(u"heading", 315.000000000000000)

        self.roseLayout.addWidget(self.roseCompass)

        self.roseLayout.setStretch(3, 1)

        self.cardsGrid.addWidget(self.roseCard, 0, 0, 1, 1)

        self.courseCard = QFrame(self.centralwidget)
        self.courseCard.setObjectName(u"courseCard")
        self.courseCard.setFrameShape(QFrame.NoFrame)
        self.courseLayout = QVBoxLayout(self.courseCard)
        self.courseLayout.setSpacing(2)
        self.courseLayout.setObjectName(u"courseLayout")
        self.courseLayout.setContentsMargins(20, 16, 20, 16)
        self.courseTitle = QLabel(self.courseCard)
        self.courseTitle.setObjectName(u"courseTitle")

        self.courseLayout.addWidget(self.courseTitle)

        self.courseSub = QLabel(self.courseCard)
        self.courseSub.setObjectName(u"courseSub")

        self.courseLayout.addWidget(self.courseSub)

        self.courseSpacer = QSpacerItem(0, 8, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.courseLayout.addItem(self.courseSpacer)

        self.courseCompass = QCustomCompass(self.courseCard)
        self.courseCompass.setObjectName(u"courseCompass")
        self.courseCompass.setProperty(u"heading", 120.000000000000000)
        self.courseCompass.setProperty(u"rotateBezel", True)

        self.courseLayout.addWidget(self.courseCompass)

        self.courseLayout.setStretch(3, 1)

        self.cardsGrid.addWidget(self.courseCard, 0, 1, 1, 1)

        self.miniCard = QFrame(self.centralwidget)
        self.miniCard.setObjectName(u"miniCard")
        self.miniCard.setFrameShape(QFrame.NoFrame)
        self.miniLayout = QVBoxLayout(self.miniCard)
        self.miniLayout.setSpacing(2)
        self.miniLayout.setObjectName(u"miniLayout")
        self.miniLayout.setContentsMargins(20, 16, 20, 16)
        self.miniTitle = QLabel(self.miniCard)
        self.miniTitle.setObjectName(u"miniTitle")

        self.miniLayout.addWidget(self.miniTitle)

        self.miniSub = QLabel(self.miniCard)
        self.miniSub.setObjectName(u"miniSub")

        self.miniLayout.addWidget(self.miniSub)

        self.miniSpacer = QSpacerItem(0, 8, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.miniLayout.addItem(self.miniSpacer)

        self.miniCompass = QCustomCompass(self.miniCard)
        self.miniCompass.setObjectName(u"miniCompass")
        self.miniCompass.setProperty(u"heading", 45.000000000000000)
        self.miniCompass.setProperty(u"showIntercardinals", False)

        self.miniLayout.addWidget(self.miniCompass)

        self.miniLayout.setStretch(3, 1)

        self.cardsGrid.addWidget(self.miniCard, 1, 0, 1, 1)

        self.dialCard = QFrame(self.centralwidget)
        self.dialCard.setObjectName(u"dialCard")
        self.dialCard.setFrameShape(QFrame.NoFrame)
        self.dialLayout = QVBoxLayout(self.dialCard)
        self.dialLayout.setSpacing(2)
        self.dialLayout.setObjectName(u"dialLayout")
        self.dialLayout.setContentsMargins(20, 16, 20, 16)
        self.dialTitle = QLabel(self.dialCard)
        self.dialTitle.setObjectName(u"dialTitle")

        self.dialLayout.addWidget(self.dialTitle)

        self.dialSub = QLabel(self.dialCard)
        self.dialSub.setObjectName(u"dialSub")

        self.dialLayout.addWidget(self.dialSub)

        self.dialSpacer = QSpacerItem(0, 8, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.dialLayout.addItem(self.dialSpacer)

        self.dialCompass = QCustomCompassDial(self.dialCard)
        self.dialCompass.setObjectName(u"dialCompass")
        self.dialCompass.setProperty(u"heading", 315.000000000000000)

        self.dialLayout.addWidget(self.dialCompass)

        self.dialLayout.setStretch(3, 1)

        self.cardsGrid.addWidget(self.dialCard, 1, 1, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"QCustomCompass \u2014 preview", None))
        self.roseTitle.setText(QCoreApplication.translate("MainWindow", u"Heading", None))
        self.roseSub.setText(QCoreApplication.translate("MainWindow", u"Drag or watch it drift", None))
        self.courseTitle.setText(QCoreApplication.translate("MainWindow", u"Course (rotating card)", None))
        self.courseSub.setText(QCoreApplication.translate("MainWindow", u"N stays on the card", None))
        self.miniTitle.setText(QCoreApplication.translate("MainWindow", u"Map heading", None))
        self.miniSub.setText(QCoreApplication.translate("MainWindow", u"NE \u00b7 compact", None))
        self.dialTitle.setText(QCoreApplication.translate("MainWindow", u"Vehicle heading (dial)", None))
        self.dialSub.setText(QCoreApplication.translate("MainWindow", u"Premium beveled", None))
    # retranslateUi

