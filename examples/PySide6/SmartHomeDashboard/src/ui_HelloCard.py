# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'new_HelloCard.ui'
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
class Ui_HelloCard(object):
    def setupUi(self, HelloCard):
        if not HelloCard.objectName():
            HelloCard.setObjectName(u"HelloCard")
        HelloCard.resize(560, 280)
        self.helloRoot = QVBoxLayout(HelloCard)
        self.helloRoot.setSpacing(0)
        self.helloRoot.setObjectName(u"helloRoot")
        self.helloRoot.setContentsMargins(0, 0, 0, 0)
        self.helloCard = QFrame(HelloCard)
        self.helloCard.setObjectName(u"helloCard")
        self.helloCard.setFrameShape(QFrame.StyledPanel)
        self.helloLayout = QVBoxLayout(self.helloCard)
        self.helloLayout.setSpacing(10)
        self.helloLayout.setObjectName(u"helloLayout")
        self.helloLayout.setContentsMargins(32, 28, 32, 28)
        self.helloHeader = QHBoxLayout()
        self.helloHeader.setObjectName(u"helloHeader")
        self.helloTitle = QLabel(self.helloCard)
        self.helloTitle.setObjectName(u"helloTitle")

        self.helloHeader.addWidget(self.helloTitle)

        self.helloHeaderSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.helloHeader.addItem(self.helloHeaderSpacer)

        self.helloMenu = QPushButton(self.helloCard)
        self.helloMenu.setObjectName(u"helloMenu")
        self.helloMenu.setMinimumSize(QSize(30, 26))
        self.helloMenu.setMaximumSize(QSize(30, 26))

        self.helloHeader.addWidget(self.helloMenu)


        self.helloLayout.addLayout(self.helloHeader)

        self.welcome = QLabel(self.helloCard)
        self.welcome.setObjectName(u"welcome")
        self.welcome.setWordWrap(True)

        self.helloLayout.addWidget(self.welcome)

        self.helloMid = QSpacerItem(20, 16, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.helloLayout.addItem(self.helloMid)

        self.weatherRow = QHBoxLayout()
        self.weatherRow.setSpacing(10)
        self.weatherRow.setObjectName(u"weatherRow")
        self.wTile0 = QVBoxLayout()
        self.wTile0.setSpacing(6)
        self.wTile0.setObjectName(u"wTile0")
        self.wIcon0 = QLabel(self.helloCard)
        self.wIcon0.setObjectName(u"wIcon0")
        self.wIcon0.setMinimumSize(QSize(42, 42))
        self.wIcon0.setMaximumSize(QSize(42, 42))

        self.wTile0.addWidget(self.wIcon0)

        self.wValue0 = QLabel(self.helloCard)
        self.wValue0.setObjectName(u"wValue0")

        self.wTile0.addWidget(self.wValue0)

        self.wLabel0 = QLabel(self.helloCard)
        self.wLabel0.setObjectName(u"wLabel0")
        self.wLabel0.setWordWrap(True)

        self.wTile0.addWidget(self.wLabel0)


        self.weatherRow.addLayout(self.wTile0)

        self.wTile1 = QVBoxLayout()
        self.wTile1.setSpacing(6)
        self.wTile1.setObjectName(u"wTile1")
        self.wIcon1 = QLabel(self.helloCard)
        self.wIcon1.setObjectName(u"wIcon1")
        self.wIcon1.setMinimumSize(QSize(42, 42))
        self.wIcon1.setMaximumSize(QSize(42, 42))

        self.wTile1.addWidget(self.wIcon1)

        self.wValue1 = QLabel(self.helloCard)
        self.wValue1.setObjectName(u"wValue1")

        self.wTile1.addWidget(self.wValue1)

        self.wLabel1 = QLabel(self.helloCard)
        self.wLabel1.setObjectName(u"wLabel1")
        self.wLabel1.setWordWrap(True)

        self.wTile1.addWidget(self.wLabel1)


        self.weatherRow.addLayout(self.wTile1)

        self.wTile2 = QVBoxLayout()
        self.wTile2.setSpacing(6)
        self.wTile2.setObjectName(u"wTile2")
        self.wIcon2 = QLabel(self.helloCard)
        self.wIcon2.setObjectName(u"wIcon2")
        self.wIcon2.setMinimumSize(QSize(42, 42))
        self.wIcon2.setMaximumSize(QSize(42, 42))

        self.wTile2.addWidget(self.wIcon2)

        self.wValue2 = QLabel(self.helloCard)
        self.wValue2.setObjectName(u"wValue2")

        self.wTile2.addWidget(self.wValue2)

        self.wLabel2 = QLabel(self.helloCard)
        self.wLabel2.setObjectName(u"wLabel2")
        self.wLabel2.setWordWrap(True)

        self.wTile2.addWidget(self.wLabel2)


        self.weatherRow.addLayout(self.wTile2)

        self.wTile3 = QVBoxLayout()
        self.wTile3.setSpacing(6)
        self.wTile3.setObjectName(u"wTile3")
        self.wIcon3 = QLabel(self.helloCard)
        self.wIcon3.setObjectName(u"wIcon3")
        self.wIcon3.setMinimumSize(QSize(42, 42))
        self.wIcon3.setMaximumSize(QSize(42, 42))

        self.wTile3.addWidget(self.wIcon3)

        self.wValue3 = QLabel(self.helloCard)
        self.wValue3.setObjectName(u"wValue3")

        self.wTile3.addWidget(self.wValue3)

        self.wLabel3 = QLabel(self.helloCard)
        self.wLabel3.setObjectName(u"wLabel3")
        self.wLabel3.setWordWrap(True)

        self.wTile3.addWidget(self.wLabel3)


        self.weatherRow.addLayout(self.wTile3)


        self.helloLayout.addLayout(self.weatherRow)


        self.helloRoot.addWidget(self.helloCard)


        self.retranslateUi(HelloCard)

        QMetaObject.connectSlotsByName(HelloCard)
    # setupUi

    def retranslateUi(self, HelloCard):
        self.helloCard.setProperty(u"role", QCoreApplication.translate("HelloCard", u"card", None))
        self.helloTitle.setText(QCoreApplication.translate("HelloCard", u"Hello, Ana!", None))
        self.helloTitle.setProperty(u"role", QCoreApplication.translate("HelloCard", u"helloTitle", None))
        self.helloMenu.setText("")
        self.helloMenu.setProperty(u"role", QCoreApplication.translate("HelloCard", u"menuBtn", None))
        self.welcome.setText(QCoreApplication.translate("HelloCard", u"Welcome home, Ana.", None))
        self.welcome.setProperty(u"role", QCoreApplication.translate("HelloCard", u"welcome", None))
        self.wIcon0.setText("")
        self.wValue0.setText(QCoreApplication.translate("HelloCard", u"15\u00b0", None))
        self.wValue0.setProperty(u"role", QCoreApplication.translate("HelloCard", u"wValue", None))
        self.wLabel0.setText(QCoreApplication.translate("HelloCard", u"Weather", None))
        self.wLabel0.setProperty(u"role", QCoreApplication.translate("HelloCard", u"wLabel", None))
        self.wIcon1.setText("")
        self.wValue1.setText(QCoreApplication.translate("HelloCard", u"45%", None))
        self.wValue1.setProperty(u"role", QCoreApplication.translate("HelloCard", u"wValue", None))
        self.wLabel1.setText(QCoreApplication.translate("HelloCard", u"Outdoor Humidity", None))
        self.wLabel1.setProperty(u"role", QCoreApplication.translate("HelloCard", u"wLabel", None))
        self.wIcon2.setText("")
        self.wValue2.setText(QCoreApplication.translate("HelloCard", u"22\u00b0", None))
        self.wValue2.setProperty(u"role", QCoreApplication.translate("HelloCard", u"wValue", None))
        self.wLabel2.setText(QCoreApplication.translate("HelloCard", u"Indoor Temperature", None))
        self.wLabel2.setProperty(u"role", QCoreApplication.translate("HelloCard", u"wLabel", None))
        self.wIcon3.setText("")
        self.wValue3.setText("")
        self.wValue3.setProperty(u"role", QCoreApplication.translate("HelloCard", u"wValue", None))
        self.wLabel3.setText(QCoreApplication.translate("HelloCard", u"Add Data", None))
        self.wLabel3.setProperty(u"role", QCoreApplication.translate("HelloCard", u"wLabelMuted", None))
        pass
    # retranslateUi

