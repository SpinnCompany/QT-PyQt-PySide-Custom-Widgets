# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'new_BeeswarmCard.ui'
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
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

from Custom_Widgets.QCustomBeeswarm import QCustomBeeswarm
class Ui_BeeswarmCard(object):
    def setupUi(self, BeeswarmCard):
        if not BeeswarmCard.objectName():
            BeeswarmCard.setObjectName(u"BeeswarmCard")
        BeeswarmCard.resize(700, 320)
        self.beeRoot = QVBoxLayout(BeeswarmCard)
        self.beeRoot.setSpacing(0)
        self.beeRoot.setObjectName(u"beeRoot")
        self.beeRoot.setContentsMargins(0, 0, 0, 0)
        self.beeswarmCard = QFrame(BeeswarmCard)
        self.beeswarmCard.setObjectName(u"beeswarmCard")
        self.beeswarmCard.setFrameShape(QFrame.StyledPanel)
        self.beeLayout = QVBoxLayout(self.beeswarmCard)
        self.beeLayout.setSpacing(10)
        self.beeLayout.setObjectName(u"beeLayout")
        self.beeLayout.setContentsMargins(20, 18, 20, 18)
        self.beeHeader = QHBoxLayout()
        self.beeHeader.setObjectName(u"beeHeader")
        self.beeTitle = QLabel(self.beeswarmCard)
        self.beeTitle.setObjectName(u"beeTitle")

        self.beeHeader.addWidget(self.beeTitle)

        self.beeHeaderSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.beeHeader.addItem(self.beeHeaderSpacer)

        self.beeswarmMenu = QPushButton(self.beeswarmCard)
        self.beeswarmMenu.setObjectName(u"beeswarmMenu")
        self.beeswarmMenu.setMinimumSize(QSize(30, 26))
        self.beeswarmMenu.setMaximumSize(QSize(30, 26))

        self.beeHeader.addWidget(self.beeswarmMenu)


        self.beeLayout.addLayout(self.beeHeader)

        self.beeswarm = QCustomBeeswarm(self.beeswarmCard)
        self.beeswarm.setObjectName(u"beeswarm")
        self.beeswarm.setMinimumSize(QSize(0, 190))
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.beeswarm.sizePolicy().hasHeightForWidth())
        self.beeswarm.setSizePolicy(sizePolicy)

        self.beeLayout.addWidget(self.beeswarm)

        self.beeFooter = QHBoxLayout()
        self.beeFooter.setSpacing(18)
        self.beeFooter.setObjectName(u"beeFooter")
        self.beeswarmLegend = QWidget(self.beeswarmCard)
        self.beeswarmLegend.setObjectName(u"beeswarmLegend")
        self.beeLegendLayout = QHBoxLayout(self.beeswarmLegend)
        self.beeLegendLayout.setSpacing(18)
        self.beeLegendLayout.setObjectName(u"beeLegendLayout")
        self.beeLegendLayout.setContentsMargins(0, 0, 0, 0)

        self.beeFooter.addWidget(self.beeswarmLegend)

        self.beeFooterSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.beeFooter.addItem(self.beeFooterSpacer)

        self.beeswarmTotal = QLabel(self.beeswarmCard)
        self.beeswarmTotal.setObjectName(u"beeswarmTotal")

        self.beeFooter.addWidget(self.beeswarmTotal)


        self.beeLayout.addLayout(self.beeFooter)


        self.beeRoot.addWidget(self.beeswarmCard)


        self.retranslateUi(BeeswarmCard)

        QMetaObject.connectSlotsByName(BeeswarmCard)
    # setupUi

    def retranslateUi(self, BeeswarmCard):
        self.beeswarmCard.setProperty(u"role", QCoreApplication.translate("BeeswarmCard", u"card", None))
        self.beeTitle.setText(QCoreApplication.translate("BeeswarmCard", u"PRODUCT", None))
        self.beeTitle.setProperty(u"role", QCoreApplication.translate("BeeswarmCard", u"cardTitle", None))
        self.beeswarmMenu.setText("")
        self.beeswarmMenu.setProperty(u"role", QCoreApplication.translate("BeeswarmCard", u"menuBtn", None))
        self.beeswarmTotal.setText(QCoreApplication.translate("BeeswarmCard", u"Total: 1,012", None))
        self.beeswarmTotal.setProperty(u"role", QCoreApplication.translate("BeeswarmCard", u"total", None))
        pass
    # retranslateUi

