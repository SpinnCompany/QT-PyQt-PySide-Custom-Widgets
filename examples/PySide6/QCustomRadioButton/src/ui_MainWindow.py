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

from Custom_Widgets.QCustomRadioButton import QCustomRadioButton
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(480, 560)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.mainLayout = QVBoxLayout(self.centralwidget)
        self.mainLayout.setSpacing(18)
        self.mainLayout.setObjectName(u"mainLayout")
        self.mainLayout.setContentsMargins(24, 24, 24, 24)
        self.planCard = QFrame(self.centralwidget)
        self.planCard.setObjectName(u"planCard")
        self.planCard.setFrameShape(QFrame.StyledPanel)
        self.planCardLayout = QVBoxLayout(self.planCard)
        self.planCardLayout.setSpacing(10)
        self.planCardLayout.setObjectName(u"planCardLayout")
        self.planHeading = QLabel(self.planCard)
        self.planHeading.setObjectName(u"planHeading")

        self.planCardLayout.addWidget(self.planHeading)

        self.plansBox = QWidget(self.planCard)
        self.plansBox.setObjectName(u"plansBox")
        self.plansBoxLayout = QVBoxLayout(self.plansBox)
        self.plansBoxLayout.setSpacing(10)
        self.plansBoxLayout.setObjectName(u"plansBoxLayout")
        self.plansBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.radioPlanFree = QCustomRadioButton(self.plansBox)
        self.radioPlanFree.setObjectName(u"radioPlanFree")
        self.radioPlanFree.setProperty(u"text", u"Community - free forever")
        self.radioPlanFree.setProperty(u"value", u"free")
        self.radioPlanFree.setProperty(u"checked", True)

        self.plansBoxLayout.addWidget(self.radioPlanFree)

        self.radioPlanPro = QCustomRadioButton(self.plansBox)
        self.radioPlanPro.setObjectName(u"radioPlanPro")
        self.radioPlanPro.setProperty(u"text", u"Pro - $12/month")
        self.radioPlanPro.setProperty(u"value", u"pro")

        self.plansBoxLayout.addWidget(self.radioPlanPro)

        self.radioPlanStudio = QCustomRadioButton(self.plansBox)
        self.radioPlanStudio.setObjectName(u"radioPlanStudio")
        self.radioPlanStudio.setProperty(u"text", u"Studio - $29/month")
        self.radioPlanStudio.setProperty(u"value", u"studio")

        self.plansBoxLayout.addWidget(self.radioPlanStudio)


        self.planCardLayout.addWidget(self.plansBox)


        self.mainLayout.addWidget(self.planCard)

        self.sizeCard = QFrame(self.centralwidget)
        self.sizeCard.setObjectName(u"sizeCard")
        self.sizeCard.setFrameShape(QFrame.StyledPanel)
        self.sizeCardLayout = QVBoxLayout(self.sizeCard)
        self.sizeCardLayout.setSpacing(10)
        self.sizeCardLayout.setObjectName(u"sizeCardLayout")
        self.sizeHeading = QLabel(self.sizeCard)
        self.sizeHeading.setObjectName(u"sizeHeading")

        self.sizeCardLayout.addWidget(self.sizeHeading)

        self.sizesBox = QWidget(self.sizeCard)
        self.sizesBox.setObjectName(u"sizesBox")
        self.sizesBoxLayout = QHBoxLayout(self.sizesBox)
        self.sizesBoxLayout.setSpacing(24)
        self.sizesBoxLayout.setObjectName(u"sizesBoxLayout")
        self.sizesBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.radioSizeSm = QCustomRadioButton(self.sizesBox)
        self.radioSizeSm.setObjectName(u"radioSizeSm")
        self.radioSizeSm.setProperty(u"text", u"sm")
        self.radioSizeSm.setProperty(u"value", u"sm")
        self.radioSizeSm.setProperty(u"sizeVariant", u"sm")

        self.sizesBoxLayout.addWidget(self.radioSizeSm)

        self.radioSizeMd = QCustomRadioButton(self.sizesBox)
        self.radioSizeMd.setObjectName(u"radioSizeMd")
        self.radioSizeMd.setProperty(u"text", u"md")
        self.radioSizeMd.setProperty(u"value", u"md")
        self.radioSizeMd.setProperty(u"sizeVariant", u"md")
        self.radioSizeMd.setProperty(u"checked", True)

        self.sizesBoxLayout.addWidget(self.radioSizeMd)

        self.radioSizeLg = QCustomRadioButton(self.sizesBox)
        self.radioSizeLg.setObjectName(u"radioSizeLg")
        self.radioSizeLg.setProperty(u"text", u"lg")
        self.radioSizeLg.setProperty(u"value", u"lg")
        self.radioSizeLg.setProperty(u"sizeVariant", u"lg")

        self.sizesBoxLayout.addWidget(self.radioSizeLg)

        self.sizesSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.sizesBoxLayout.addItem(self.sizesSpacer)


        self.sizeCardLayout.addWidget(self.sizesBox)


        self.mainLayout.addWidget(self.sizeCard)

        self.looseCard = QFrame(self.centralwidget)
        self.looseCard.setObjectName(u"looseCard")
        self.looseCard.setFrameShape(QFrame.StyledPanel)
        self.looseCardLayout = QVBoxLayout(self.looseCard)
        self.looseCardLayout.setSpacing(10)
        self.looseCardLayout.setObjectName(u"looseCardLayout")
        self.looseHeading = QLabel(self.looseCard)
        self.looseHeading.setObjectName(u"looseHeading")

        self.looseCardLayout.addWidget(self.looseHeading)

        self.looseBox = QWidget(self.looseCard)
        self.looseBox.setObjectName(u"looseBox")
        self.looseBoxLayout = QHBoxLayout(self.looseBox)
        self.looseBoxLayout.setSpacing(24)
        self.looseBoxLayout.setObjectName(u"looseBoxLayout")
        self.looseBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.radioLooseA = QCustomRadioButton(self.looseBox)
        self.radioLooseA.setObjectName(u"radioLooseA")
        self.radioLooseA.setProperty(u"text", u"Independent A")
        self.radioLooseA.setProperty(u"autoExclusive", False)

        self.looseBoxLayout.addWidget(self.radioLooseA)

        self.radioLooseB = QCustomRadioButton(self.looseBox)
        self.radioLooseB.setObjectName(u"radioLooseB")
        self.radioLooseB.setProperty(u"text", u"Independent B")
        self.radioLooseB.setProperty(u"autoExclusive", False)

        self.looseBoxLayout.addWidget(self.radioLooseB)

        self.looseSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.looseBoxLayout.addItem(self.looseSpacer)


        self.looseCardLayout.addWidget(self.looseBox)


        self.mainLayout.addWidget(self.looseCard)

        self.mainSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.mainLayout.addItem(self.mainSpacer)

        self.statusLabel = QLabel(self.centralwidget)
        self.statusLabel.setObjectName(u"statusLabel")

        self.mainLayout.addWidget(self.statusLabel)

        self.themeButton = QPushButton(self.centralwidget)
        self.themeButton.setObjectName(u"themeButton")
        self.themeButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.mainLayout.addWidget(self.themeButton)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"QCustomRadioButton", None))
        self.planHeading.setText(QCoreApplication.translate("MainWindow", u"Choose a plan", None))
        self.sizeHeading.setText(QCoreApplication.translate("MainWindow", u"Size variants", None))
        self.looseHeading.setText(QCoreApplication.translate("MainWindow", u"autoExclusive = False", None))
        self.statusLabel.setText(QCoreApplication.translate("MainWindow", u"Selected plan: free", None))
        self.themeButton.setText(QCoreApplication.translate("MainWindow", u"Toggle light / dark", None))
    # retranslateUi

