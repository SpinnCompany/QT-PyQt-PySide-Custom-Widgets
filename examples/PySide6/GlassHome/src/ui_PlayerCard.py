# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'new_PlayerCard.ui'
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

from Custom_Widgets.QCustomGlassFrame import QCustomGlassFrame
from Custom_Widgets.QCustomPlayerBar import QCustomPlayerBar
class Ui_PlayerCard(object):
    def setupUi(self, PlayerCard):
        if not PlayerCard.objectName():
            PlayerCard.setObjectName(u"PlayerCard")
        PlayerCard.resize(280, 130)
        self.playerRoot = QVBoxLayout(PlayerCard)
        self.playerRoot.setSpacing(0)
        self.playerRoot.setObjectName(u"playerRoot")
        self.playerRoot.setContentsMargins(0, 0, 0, 0)
        self.playerGlass = QCustomGlassFrame(PlayerCard)
        self.playerGlass.setObjectName(u"playerGlass")
        self.playerGlass.setProperty(u"cornerRadius", 22)
        self.playerLayout = QVBoxLayout(self.playerGlass)
        self.playerLayout.setSpacing(0)
        self.playerLayout.setObjectName(u"playerLayout")
        self.playerLayout.setContentsMargins(6, 4, 6, 4)
        self.player = QCustomPlayerBar(self.playerGlass)
        self.player.setObjectName(u"player")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.player.sizePolicy().hasHeightForWidth())
        self.player.setSizePolicy(sizePolicy)
        self.player.setProperty(u"position", 0.230000000000000)
        self.player.setProperty(u"playing", True)
        self.player.setProperty(u"cornerRadius", 18)
        self.player.setProperty(u"compactMode", True)

        self.playerLayout.addWidget(self.player)


        self.playerRoot.addWidget(self.playerGlass)


        self.retranslateUi(PlayerCard)

        QMetaObject.connectSlotsByName(PlayerCard)
    # setupUi

    def retranslateUi(self, PlayerCard):
        self.playerGlass.setProperty(u"backdropSource", QCoreApplication.translate("PlayerCard", u"wallpaper", None))
        self.player.setProperty(u"title", QCoreApplication.translate("PlayerCard", u"Greater Than One", None))
        self.player.setProperty(u"artist", QCoreApplication.translate("PlayerCard", u"Ericdoa x Valorant", None))
        self.player.setProperty(u"elapsedText", QCoreApplication.translate("PlayerCard", u"0:34", None))
        self.player.setProperty(u"totalText", QCoreApplication.translate("PlayerCard", u"2:27", None))
        pass
    # retranslateUi

