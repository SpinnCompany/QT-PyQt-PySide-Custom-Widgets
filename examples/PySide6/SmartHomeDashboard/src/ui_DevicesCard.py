# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'new_DevicesCard.ui'
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
    QPushButton, QSizePolicy, QVBoxLayout, QWidget)

from Custom_Widgets.QCustomTileButton import QCustomTileButton
class Ui_DevicesCard(object):
    def setupUi(self, DevicesCard):
        if not DevicesCard.objectName():
            DevicesCard.setObjectName(u"DevicesCard")
        DevicesCard.resize(520, 300)
        self.devRoot = QVBoxLayout(DevicesCard)
        self.devRoot.setSpacing(0)
        self.devRoot.setObjectName(u"devRoot")
        self.devRoot.setContentsMargins(0, 0, 0, 0)
        self.devicesCard = QFrame(DevicesCard)
        self.devicesCard.setObjectName(u"devicesCard")
        self.devicesCard.setFrameShape(QFrame.StyledPanel)
        self.devGrid = QGridLayout(self.devicesCard)
        self.devGrid.setObjectName(u"devGrid")
        self.devGrid.setHorizontalSpacing(14)
        self.devGrid.setVerticalSpacing(14)
        self.devGrid.setContentsMargins(0, 0, 0, 0)
        self.tile0 = QCustomTileButton(self.devicesCard)
        self.tile0.setObjectName(u"tile0")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tile0.sizePolicy().hasHeightForWidth())
        self.tile0.setSizePolicy(sizePolicy)

        self.devGrid.addWidget(self.tile0, 0, 0, 1, 1)

        self.tile1 = QCustomTileButton(self.devicesCard)
        self.tile1.setObjectName(u"tile1")
        sizePolicy.setHeightForWidth(self.tile1.sizePolicy().hasHeightForWidth())
        self.tile1.setSizePolicy(sizePolicy)

        self.devGrid.addWidget(self.tile1, 0, 1, 1, 1)

        self.tile2 = QCustomTileButton(self.devicesCard)
        self.tile2.setObjectName(u"tile2")
        sizePolicy.setHeightForWidth(self.tile2.sizePolicy().hasHeightForWidth())
        self.tile2.setSizePolicy(sizePolicy)

        self.devGrid.addWidget(self.tile2, 0, 2, 1, 1)

        self.tile3 = QCustomTileButton(self.devicesCard)
        self.tile3.setObjectName(u"tile3")
        sizePolicy.setHeightForWidth(self.tile3.sizePolicy().hasHeightForWidth())
        self.tile3.setSizePolicy(sizePolicy)

        self.devGrid.addWidget(self.tile3, 0, 3, 1, 1)

        self.tile4 = QCustomTileButton(self.devicesCard)
        self.tile4.setObjectName(u"tile4")
        sizePolicy.setHeightForWidth(self.tile4.sizePolicy().hasHeightForWidth())
        self.tile4.setSizePolicy(sizePolicy)

        self.devGrid.addWidget(self.tile4, 1, 0, 1, 1)

        self.tile5 = QCustomTileButton(self.devicesCard)
        self.tile5.setObjectName(u"tile5")
        sizePolicy.setHeightForWidth(self.tile5.sizePolicy().hasHeightForWidth())
        self.tile5.setSizePolicy(sizePolicy)

        self.devGrid.addWidget(self.tile5, 1, 1, 1, 1)

        self.tile6 = QCustomTileButton(self.devicesCard)
        self.tile6.setObjectName(u"tile6")
        sizePolicy.setHeightForWidth(self.tile6.sizePolicy().hasHeightForWidth())
        self.tile6.setSizePolicy(sizePolicy)

        self.devGrid.addWidget(self.tile6, 1, 2, 1, 1)

        self.tile7 = QCustomTileButton(self.devicesCard)
        self.tile7.setObjectName(u"tile7")
        sizePolicy.setHeightForWidth(self.tile7.sizePolicy().hasHeightForWidth())
        self.tile7.setSizePolicy(sizePolicy)

        self.devGrid.addWidget(self.tile7, 1, 3, 1, 1)


        self.devRoot.addWidget(self.devicesCard)


        self.retranslateUi(DevicesCard)

        QMetaObject.connectSlotsByName(DevicesCard)
    # setupUi

    def retranslateUi(self, DevicesCard):
        self.devicesCard.setProperty(u"role", QCoreApplication.translate("DevicesCard", u"cardFlat", None))
        self.tile0.setProperty(u"caption", QCoreApplication.translate("DevicesCard", u"Lights", None))
        self.tile1.setProperty(u"caption", QCoreApplication.translate("DevicesCard", u"Heating", None))
        self.tile2.setProperty(u"caption", QCoreApplication.translate("DevicesCard", u"Air Conditioner", None))
        self.tile3.setProperty(u"caption", QCoreApplication.translate("DevicesCard", u"Cameras", None))
        self.tile4.setProperty(u"caption", QCoreApplication.translate("DevicesCard", u"Doors", None))
        self.tile5.setProperty(u"caption", QCoreApplication.translate("DevicesCard", u"Alarm", None))
        self.tile6.setProperty(u"caption", QCoreApplication.translate("DevicesCard", u"Garage", None))
        self.tile7.setProperty(u"caption", QCoreApplication.translate("DevicesCard", u"Garden", None))
        pass
    # retranslateUi

