# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'new_ProductCard.ui'
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

from Custom_Widgets.QCustomDotMatrix import QCustomDotMatrix
class Ui_ProductCard(object):
    def setupUi(self, ProductCard):
        if not ProductCard.objectName():
            ProductCard.setObjectName(u"ProductCard")
        ProductCard.resize(340, 260)
        self.prodRoot = QVBoxLayout(ProductCard)
        self.prodRoot.setSpacing(0)
        self.prodRoot.setObjectName(u"prodRoot")
        self.prodRoot.setContentsMargins(0, 0, 0, 0)
        self.productCard = QFrame(ProductCard)
        self.productCard.setObjectName(u"productCard")
        self.productCard.setFrameShape(QFrame.StyledPanel)
        self.prodLayout = QVBoxLayout(self.productCard)
        self.prodLayout.setSpacing(10)
        self.prodLayout.setObjectName(u"prodLayout")
        self.prodLayout.setContentsMargins(20, 18, 20, 18)
        self.prodHeader = QHBoxLayout()
        self.prodHeader.setObjectName(u"prodHeader")
        self.prodTitle = QLabel(self.productCard)
        self.prodTitle.setObjectName(u"prodTitle")

        self.prodHeader.addWidget(self.prodTitle)

        self.prodHeaderSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.prodHeader.addItem(self.prodHeaderSpacer)

        self.productMenu = QPushButton(self.productCard)
        self.productMenu.setObjectName(u"productMenu")
        self.productMenu.setMinimumSize(QSize(30, 26))
        self.productMenu.setMaximumSize(QSize(30, 26))

        self.prodHeader.addWidget(self.productMenu)


        self.prodLayout.addLayout(self.prodHeader)

        self.prodStatsRow = QHBoxLayout()
        self.prodStatsRow.setSpacing(26)
        self.prodStatsRow.setObjectName(u"prodStatsRow")
        self.prodStat0 = QVBoxLayout()
        self.prodStat0.setSpacing(2)
        self.prodStat0.setObjectName(u"prodStat0")
        self.prodArrow0 = QLabel(self.productCard)
        self.prodArrow0.setObjectName(u"prodArrow0")
        self.prodArrow0.setMinimumSize(QSize(16, 16))
        self.prodArrow0.setMaximumSize(QSize(16, 16))

        self.prodStat0.addWidget(self.prodArrow0)

        self.prodValue0 = QLabel(self.productCard)
        self.prodValue0.setObjectName(u"prodValue0")

        self.prodStat0.addWidget(self.prodValue0)

        self.prodCap0 = QLabel(self.productCard)
        self.prodCap0.setObjectName(u"prodCap0")

        self.prodStat0.addWidget(self.prodCap0)


        self.prodStatsRow.addLayout(self.prodStat0)

        self.prodStat1 = QVBoxLayout()
        self.prodStat1.setSpacing(2)
        self.prodStat1.setObjectName(u"prodStat1")
        self.prodArrow1 = QLabel(self.productCard)
        self.prodArrow1.setObjectName(u"prodArrow1")
        self.prodArrow1.setMinimumSize(QSize(16, 16))
        self.prodArrow1.setMaximumSize(QSize(16, 16))

        self.prodStat1.addWidget(self.prodArrow1)

        self.prodValue1 = QLabel(self.productCard)
        self.prodValue1.setObjectName(u"prodValue1")

        self.prodStat1.addWidget(self.prodValue1)

        self.prodCap1 = QLabel(self.productCard)
        self.prodCap1.setObjectName(u"prodCap1")

        self.prodStat1.addWidget(self.prodCap1)


        self.prodStatsRow.addLayout(self.prodStat1)

        self.prodStatsSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.prodStatsRow.addItem(self.prodStatsSpacer)


        self.prodLayout.addLayout(self.prodStatsRow)

        self.productMatrix = QCustomDotMatrix(self.productCard)
        self.productMatrix.setObjectName(u"productMatrix")
        self.productMatrix.setMinimumSize(QSize(0, 96))
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.productMatrix.sizePolicy().hasHeightForWidth())
        self.productMatrix.setSizePolicy(sizePolicy)

        self.prodLayout.addWidget(self.productMatrix)


        self.prodRoot.addWidget(self.productCard)


        self.retranslateUi(ProductCard)

        QMetaObject.connectSlotsByName(ProductCard)
    # setupUi

    def retranslateUi(self, ProductCard):
        self.productCard.setProperty(u"role", QCoreApplication.translate("ProductCard", u"card", None))
        self.prodTitle.setText(QCoreApplication.translate("ProductCard", u"PRODUCT", None))
        self.prodTitle.setProperty(u"role", QCoreApplication.translate("ProductCard", u"cardTitle", None))
        self.productMenu.setText("")
        self.productMenu.setProperty(u"role", QCoreApplication.translate("ProductCard", u"menuBtn", None))
        self.prodArrow0.setText("")
        self.prodValue0.setText(QCoreApplication.translate("ProductCard", u"2,8%", None))
        self.prodValue0.setProperty(u"role", QCoreApplication.translate("ProductCard", u"statValue", None))
        self.prodCap0.setText(QCoreApplication.translate("ProductCard", u"Partners", None))
        self.prodCap0.setProperty(u"role", QCoreApplication.translate("ProductCard", u"statCap", None))
        self.prodArrow1.setText("")
        self.prodValue1.setText(QCoreApplication.translate("ProductCard", u"3,2%", None))
        self.prodValue1.setProperty(u"role", QCoreApplication.translate("ProductCard", u"statValue", None))
        self.prodCap1.setText(QCoreApplication.translate("ProductCard", u"Owners", None))
        self.prodCap1.setProperty(u"role", QCoreApplication.translate("ProductCard", u"statCap", None))
        pass
    # retranslateUi

