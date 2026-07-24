# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'new_CustomerCard.ui'
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

from Custom_Widgets.QCustomSparkline import QCustomSparkline
class Ui_CustomerCard(object):
    def setupUi(self, CustomerCard):
        if not CustomerCard.objectName():
            CustomerCard.setObjectName(u"CustomerCard")
        CustomerCard.resize(340, 260)
        self.custRoot = QVBoxLayout(CustomerCard)
        self.custRoot.setSpacing(0)
        self.custRoot.setObjectName(u"custRoot")
        self.custRoot.setContentsMargins(0, 0, 0, 0)
        self.customerCard = QFrame(CustomerCard)
        self.customerCard.setObjectName(u"customerCard")
        self.customerCard.setFrameShape(QFrame.StyledPanel)
        self.custLayout = QVBoxLayout(self.customerCard)
        self.custLayout.setSpacing(10)
        self.custLayout.setObjectName(u"custLayout")
        self.custLayout.setContentsMargins(20, 18, 20, 18)
        self.custHeader = QHBoxLayout()
        self.custHeader.setObjectName(u"custHeader")
        self.custTitle = QLabel(self.customerCard)
        self.custTitle.setObjectName(u"custTitle")

        self.custHeader.addWidget(self.custTitle)

        self.custHeaderSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.custHeader.addItem(self.custHeaderSpacer)

        self.customerMenu = QPushButton(self.customerCard)
        self.customerMenu.setObjectName(u"customerMenu")
        self.customerMenu.setMinimumSize(QSize(30, 26))
        self.customerMenu.setMaximumSize(QSize(30, 26))

        self.custHeader.addWidget(self.customerMenu)


        self.custLayout.addLayout(self.custHeader)

        self.custStatsRow = QHBoxLayout()
        self.custStatsRow.setSpacing(26)
        self.custStatsRow.setObjectName(u"custStatsRow")
        self.custStat0 = QVBoxLayout()
        self.custStat0.setSpacing(2)
        self.custStat0.setObjectName(u"custStat0")
        self.custArrow0 = QLabel(self.customerCard)
        self.custArrow0.setObjectName(u"custArrow0")
        self.custArrow0.setMinimumSize(QSize(16, 16))
        self.custArrow0.setMaximumSize(QSize(16, 16))

        self.custStat0.addWidget(self.custArrow0)

        self.custValue0 = QLabel(self.customerCard)
        self.custValue0.setObjectName(u"custValue0")

        self.custStat0.addWidget(self.custValue0)

        self.custCap0 = QLabel(self.customerCard)
        self.custCap0.setObjectName(u"custCap0")

        self.custStat0.addWidget(self.custCap0)


        self.custStatsRow.addLayout(self.custStat0)

        self.custStat1 = QVBoxLayout()
        self.custStat1.setSpacing(2)
        self.custStat1.setObjectName(u"custStat1")
        self.custArrow1 = QLabel(self.customerCard)
        self.custArrow1.setObjectName(u"custArrow1")
        self.custArrow1.setMinimumSize(QSize(16, 16))
        self.custArrow1.setMaximumSize(QSize(16, 16))

        self.custStat1.addWidget(self.custArrow1)

        self.custValue1 = QLabel(self.customerCard)
        self.custValue1.setObjectName(u"custValue1")

        self.custStat1.addWidget(self.custValue1)

        self.custCap1 = QLabel(self.customerCard)
        self.custCap1.setObjectName(u"custCap1")

        self.custStat1.addWidget(self.custCap1)


        self.custStatsRow.addLayout(self.custStat1)

        self.custStatsSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.custStatsRow.addItem(self.custStatsSpacer)


        self.custLayout.addLayout(self.custStatsRow)

        self.customerLines = QCustomSparkline(self.customerCard)
        self.customerLines.setObjectName(u"customerLines")
        self.customerLines.setMinimumSize(QSize(0, 84))
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.customerLines.sizePolicy().hasHeightForWidth())
        self.customerLines.setSizePolicy(sizePolicy)
        self.customerLines.setProperty(u"lineWidth", 2.600000000000000)
        self.customerLines.setProperty(u"fillEnabled", False)

        self.custLayout.addWidget(self.customerLines)


        self.custRoot.addWidget(self.customerCard)


        self.retranslateUi(CustomerCard)

        QMetaObject.connectSlotsByName(CustomerCard)
    # setupUi

    def retranslateUi(self, CustomerCard):
        self.customerCard.setProperty(u"role", QCoreApplication.translate("CustomerCard", u"card", None))
        self.custTitle.setText(QCoreApplication.translate("CustomerCard", u"CUSTOMER", None))
        self.custTitle.setProperty(u"role", QCoreApplication.translate("CustomerCard", u"cardTitle", None))
        self.customerMenu.setText("")
        self.customerMenu.setProperty(u"role", QCoreApplication.translate("CustomerCard", u"menuBtn", None))
        self.custArrow0.setText("")
        self.custValue0.setText(QCoreApplication.translate("CustomerCard", u"2,4%", None))
        self.custValue0.setProperty(u"role", QCoreApplication.translate("CustomerCard", u"statValue", None))
        self.custCap0.setText(QCoreApplication.translate("CustomerCard", u"Web Surfing", None))
        self.custCap0.setProperty(u"role", QCoreApplication.translate("CustomerCard", u"statCap", None))
        self.custArrow1.setText("")
        self.custValue1.setText(QCoreApplication.translate("CustomerCard", u"1,1%", None))
        self.custValue1.setProperty(u"role", QCoreApplication.translate("CustomerCard", u"statValue", None))
        self.custCap1.setText(QCoreApplication.translate("CustomerCard", u"Radio Station", None))
        self.custCap1.setProperty(u"role", QCoreApplication.translate("CustomerCard", u"statCap", None))
        pass
    # retranslateUi

