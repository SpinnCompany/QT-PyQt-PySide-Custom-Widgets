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
from PySide6.QtWidgets import (QApplication, QComboBox, QGridLayout, QHBoxLayout,
    QLabel, QMainWindow, QPushButton, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

from Custom_Widgets.QCustomFeaturedIcon import QCustomFeaturedIcon
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(560, 360)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.mainLayout = QVBoxLayout(self.centralwidget)
        self.mainLayout.setSpacing(16)
        self.mainLayout.setObjectName(u"mainLayout")
        self.mainLayout.setContentsMargins(24, 24, 24, 24)
        self.tileGrid = QGridLayout()
        self.tileGrid.setSpacing(14)
        self.tileGrid.setObjectName(u"tileGrid")
        self.tileTintedRounded = QCustomFeaturedIcon(self.centralwidget)
        self.tileTintedRounded.setObjectName(u"tileTintedRounded")

        self.tileGrid.addWidget(self.tileTintedRounded, 0, 0, 1, 1)

        self.tileTintedCircle = QCustomFeaturedIcon(self.centralwidget)
        self.tileTintedCircle.setObjectName(u"tileTintedCircle")

        self.tileGrid.addWidget(self.tileTintedCircle, 1, 0, 1, 1)

        self.tileTintedSquare = QCustomFeaturedIcon(self.centralwidget)
        self.tileTintedSquare.setObjectName(u"tileTintedSquare")

        self.tileGrid.addWidget(self.tileTintedSquare, 2, 0, 1, 1)

        self.tileFilledRounded = QCustomFeaturedIcon(self.centralwidget)
        self.tileFilledRounded.setObjectName(u"tileFilledRounded")

        self.tileGrid.addWidget(self.tileFilledRounded, 0, 1, 1, 1)

        self.tileFilledCircle = QCustomFeaturedIcon(self.centralwidget)
        self.tileFilledCircle.setObjectName(u"tileFilledCircle")

        self.tileGrid.addWidget(self.tileFilledCircle, 1, 1, 1, 1)

        self.tileFilledSquare = QCustomFeaturedIcon(self.centralwidget)
        self.tileFilledSquare.setObjectName(u"tileFilledSquare")

        self.tileGrid.addWidget(self.tileFilledSquare, 2, 1, 1, 1)

        self.tileOutlineRounded = QCustomFeaturedIcon(self.centralwidget)
        self.tileOutlineRounded.setObjectName(u"tileOutlineRounded")

        self.tileGrid.addWidget(self.tileOutlineRounded, 0, 2, 1, 1)

        self.tileOutlineCircle = QCustomFeaturedIcon(self.centralwidget)
        self.tileOutlineCircle.setObjectName(u"tileOutlineCircle")

        self.tileGrid.addWidget(self.tileOutlineCircle, 1, 2, 1, 1)

        self.tileOutlineSquare = QCustomFeaturedIcon(self.centralwidget)
        self.tileOutlineSquare.setObjectName(u"tileOutlineSquare")

        self.tileGrid.addWidget(self.tileOutlineSquare, 2, 2, 1, 1)

        self.tileGradientRounded = QCustomFeaturedIcon(self.centralwidget)
        self.tileGradientRounded.setObjectName(u"tileGradientRounded")

        self.tileGrid.addWidget(self.tileGradientRounded, 0, 3, 1, 1)

        self.tileGradientCircle = QCustomFeaturedIcon(self.centralwidget)
        self.tileGradientCircle.setObjectName(u"tileGradientCircle")

        self.tileGrid.addWidget(self.tileGradientCircle, 1, 3, 1, 1)

        self.tileGradientSquare = QCustomFeaturedIcon(self.centralwidget)
        self.tileGradientSquare.setObjectName(u"tileGradientSquare")

        self.tileGrid.addWidget(self.tileGradientSquare, 2, 3, 1, 1)


        self.mainLayout.addLayout(self.tileGrid)

        self.statusLabel = QLabel(self.centralwidget)
        self.statusLabel.setObjectName(u"statusLabel")

        self.mainLayout.addWidget(self.statusLabel)

        self.controlsRow = QHBoxLayout()
        self.controlsRow.setSpacing(10)
        self.controlsRow.setObjectName(u"controlsRow")
        self.sizeCaption = QLabel(self.centralwidget)
        self.sizeCaption.setObjectName(u"sizeCaption")

        self.controlsRow.addWidget(self.sizeCaption)

        self.sizeCombo = QComboBox(self.centralwidget)
        self.sizeCombo.addItem("")
        self.sizeCombo.addItem("")
        self.sizeCombo.addItem("")
        self.sizeCombo.addItem("")
        self.sizeCombo.setObjectName(u"sizeCombo")

        self.controlsRow.addWidget(self.sizeCombo)

        self.themeBtn = QPushButton(self.centralwidget)
        self.themeBtn.setObjectName(u"themeBtn")

        self.controlsRow.addWidget(self.themeBtn)

        self.controlsSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.controlsRow.addItem(self.controlsSpacer)


        self.mainLayout.addLayout(self.controlsRow)

        self.bottomSpacer = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.mainLayout.addItem(self.bottomSpacer)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"QCustomFeaturedIcon", None))
        self.tileTintedRounded.setProperty(u"iconPath", QCoreApplication.translate("MainWindow", u"Qss/icons/icons/feather/send.svg", None))
        self.tileTintedRounded.setProperty(u"variant", QCoreApplication.translate("MainWindow", u"tinted", None))
        self.tileTintedRounded.setProperty(u"shape", QCoreApplication.translate("MainWindow", u"rounded", None))
        self.tileTintedRounded.setProperty(u"sizeVariant", QCoreApplication.translate("MainWindow", u"lg", None))
        self.tileTintedCircle.setProperty(u"iconPath", QCoreApplication.translate("MainWindow", u"Qss/icons/icons/feather/send.svg", None))
        self.tileTintedCircle.setProperty(u"variant", QCoreApplication.translate("MainWindow", u"tinted", None))
        self.tileTintedCircle.setProperty(u"shape", QCoreApplication.translate("MainWindow", u"circle", None))
        self.tileTintedCircle.setProperty(u"sizeVariant", QCoreApplication.translate("MainWindow", u"lg", None))
        self.tileTintedSquare.setProperty(u"iconPath", QCoreApplication.translate("MainWindow", u"Qss/icons/icons/feather/send.svg", None))
        self.tileTintedSquare.setProperty(u"variant", QCoreApplication.translate("MainWindow", u"tinted", None))
        self.tileTintedSquare.setProperty(u"shape", QCoreApplication.translate("MainWindow", u"square", None))
        self.tileTintedSquare.setProperty(u"sizeVariant", QCoreApplication.translate("MainWindow", u"lg", None))
        self.tileFilledRounded.setProperty(u"iconPath", QCoreApplication.translate("MainWindow", u"Qss/icons/icons/feather/send.svg", None))
        self.tileFilledRounded.setProperty(u"variant", QCoreApplication.translate("MainWindow", u"filled", None))
        self.tileFilledRounded.setProperty(u"shape", QCoreApplication.translate("MainWindow", u"rounded", None))
        self.tileFilledRounded.setProperty(u"sizeVariant", QCoreApplication.translate("MainWindow", u"lg", None))
        self.tileFilledCircle.setProperty(u"iconPath", QCoreApplication.translate("MainWindow", u"Qss/icons/icons/feather/send.svg", None))
        self.tileFilledCircle.setProperty(u"variant", QCoreApplication.translate("MainWindow", u"filled", None))
        self.tileFilledCircle.setProperty(u"shape", QCoreApplication.translate("MainWindow", u"circle", None))
        self.tileFilledCircle.setProperty(u"sizeVariant", QCoreApplication.translate("MainWindow", u"lg", None))
        self.tileFilledSquare.setProperty(u"iconPath", QCoreApplication.translate("MainWindow", u"Qss/icons/icons/feather/send.svg", None))
        self.tileFilledSquare.setProperty(u"variant", QCoreApplication.translate("MainWindow", u"filled", None))
        self.tileFilledSquare.setProperty(u"shape", QCoreApplication.translate("MainWindow", u"square", None))
        self.tileFilledSquare.setProperty(u"sizeVariant", QCoreApplication.translate("MainWindow", u"lg", None))
        self.tileOutlineRounded.setProperty(u"iconPath", QCoreApplication.translate("MainWindow", u"Qss/icons/icons/feather/send.svg", None))
        self.tileOutlineRounded.setProperty(u"variant", QCoreApplication.translate("MainWindow", u"outline", None))
        self.tileOutlineRounded.setProperty(u"shape", QCoreApplication.translate("MainWindow", u"rounded", None))
        self.tileOutlineRounded.setProperty(u"sizeVariant", QCoreApplication.translate("MainWindow", u"lg", None))
        self.tileOutlineCircle.setProperty(u"iconPath", QCoreApplication.translate("MainWindow", u"Qss/icons/icons/feather/send.svg", None))
        self.tileOutlineCircle.setProperty(u"variant", QCoreApplication.translate("MainWindow", u"outline", None))
        self.tileOutlineCircle.setProperty(u"shape", QCoreApplication.translate("MainWindow", u"circle", None))
        self.tileOutlineCircle.setProperty(u"sizeVariant", QCoreApplication.translate("MainWindow", u"lg", None))
        self.tileOutlineSquare.setProperty(u"iconPath", QCoreApplication.translate("MainWindow", u"Qss/icons/icons/feather/send.svg", None))
        self.tileOutlineSquare.setProperty(u"variant", QCoreApplication.translate("MainWindow", u"outline", None))
        self.tileOutlineSquare.setProperty(u"shape", QCoreApplication.translate("MainWindow", u"square", None))
        self.tileOutlineSquare.setProperty(u"sizeVariant", QCoreApplication.translate("MainWindow", u"lg", None))
        self.tileGradientRounded.setProperty(u"iconPath", QCoreApplication.translate("MainWindow", u"Qss/icons/icons/feather/send.svg", None))
        self.tileGradientRounded.setProperty(u"variant", QCoreApplication.translate("MainWindow", u"gradient", None))
        self.tileGradientRounded.setProperty(u"shape", QCoreApplication.translate("MainWindow", u"rounded", None))
        self.tileGradientRounded.setProperty(u"sizeVariant", QCoreApplication.translate("MainWindow", u"lg", None))
        self.tileGradientCircle.setProperty(u"iconPath", QCoreApplication.translate("MainWindow", u"Qss/icons/icons/feather/send.svg", None))
        self.tileGradientCircle.setProperty(u"variant", QCoreApplication.translate("MainWindow", u"gradient", None))
        self.tileGradientCircle.setProperty(u"shape", QCoreApplication.translate("MainWindow", u"circle", None))
        self.tileGradientCircle.setProperty(u"sizeVariant", QCoreApplication.translate("MainWindow", u"lg", None))
        self.tileGradientSquare.setProperty(u"iconPath", QCoreApplication.translate("MainWindow", u"Qss/icons/icons/feather/send.svg", None))
        self.tileGradientSquare.setProperty(u"variant", QCoreApplication.translate("MainWindow", u"gradient", None))
        self.tileGradientSquare.setProperty(u"shape", QCoreApplication.translate("MainWindow", u"square", None))
        self.tileGradientSquare.setProperty(u"sizeVariant", QCoreApplication.translate("MainWindow", u"lg", None))
        self.statusLabel.setText(QCoreApplication.translate("MainWindow", u"Click a tile", None))
        self.sizeCaption.setText(QCoreApplication.translate("MainWindow", u"Size", None))
        self.sizeCombo.setItemText(0, QCoreApplication.translate("MainWindow", u"sm", None))
        self.sizeCombo.setItemText(1, QCoreApplication.translate("MainWindow", u"md", None))
        self.sizeCombo.setItemText(2, QCoreApplication.translate("MainWindow", u"lg", None))
        self.sizeCombo.setItemText(3, QCoreApplication.translate("MainWindow", u"xl", None))

        self.themeBtn.setText(QCoreApplication.translate("MainWindow", u"Light / dark", None))
    # retranslateUi

