# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'new_PlayerBar.ui'
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
from PySide6.QtWidgets import (QApplication, QLabel, QPushButton, QSizePolicy,
    QVBoxLayout, QWidget)

from Custom_Widgets.QCustomPlayerBar import QCustomPlayerBar
class Ui_PlayerBar(object):
    def setupUi(self, playerRoot):
        if not playerRoot.objectName():
            playerRoot.setObjectName(u"playerRoot")
        playerRoot.resize(1200, 96)
        self.playerLayout = QVBoxLayout(playerRoot)
        self.playerLayout.setSpacing(0)
        self.playerLayout.setObjectName(u"playerLayout")
        self.playerLayout.setContentsMargins(18, 6, 18, 10)
        self.playerBar = QCustomPlayerBar(playerRoot)
        self.playerBar.setObjectName(u"playerBar")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.playerBar.sizePolicy().hasHeightForWidth())
        self.playerBar.setSizePolicy(sizePolicy)

        self.playerLayout.addWidget(self.playerBar)


        self.retranslateUi(playerRoot)

        QMetaObject.connectSlotsByName(playerRoot)
    # setupUi

    def retranslateUi(self, playerRoot):
        pass
    # retranslateUi

