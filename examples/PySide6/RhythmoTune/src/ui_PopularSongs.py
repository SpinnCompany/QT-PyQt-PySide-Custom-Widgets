# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'new_PopularSongs.ui'
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
    QPushButton, QScrollArea, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

from Custom_Widgets.QCustomCoverCard import QCustomCoverCard
from Custom_Widgets.QCustomQPushButton import QCustomQPushButton
class Ui_PopularSongs(object):
    def setupUi(self, popularRoot):
        if not popularRoot.objectName():
            popularRoot.setObjectName(u"popularRoot")
        popularRoot.resize(900, 230)
        self.popularLayout = QVBoxLayout(popularRoot)
        self.popularLayout.setSpacing(12)
        self.popularLayout.setObjectName(u"popularLayout")
        self.popularLayout.setContentsMargins(0, 4, 0, 0)
        self.popHeader = QHBoxLayout()
        self.popHeader.setSpacing(8)
        self.popHeader.setObjectName(u"popHeader")
        self.popularTitle = QLabel(popularRoot)
        self.popularTitle.setObjectName(u"popularTitle")

        self.popHeader.addWidget(self.popularTitle)

        self.popHeaderSpacer = QSpacerItem(40, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.popHeader.addItem(self.popHeaderSpacer)

        self.prevSongBtn = QCustomQPushButton(popularRoot)
        self.prevSongBtn.setObjectName(u"prevSongBtn")
        self.prevSongBtn.setMinimumSize(QSize(34, 34))
        self.prevSongBtn.setMaximumSize(QSize(34, 34))
        self.prevSongBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.prevSongBtn.setIconSize(QSize(16, 16))

        self.popHeader.addWidget(self.prevSongBtn)

        self.nextSongBtn = QCustomQPushButton(popularRoot)
        self.nextSongBtn.setObjectName(u"nextSongBtn")
        self.nextSongBtn.setMinimumSize(QSize(34, 34))
        self.nextSongBtn.setMaximumSize(QSize(34, 34))
        self.nextSongBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.nextSongBtn.setIconSize(QSize(16, 16))

        self.popHeader.addWidget(self.nextSongBtn)


        self.popularLayout.addLayout(self.popHeader)

        self.songsScroll = QScrollArea(popularRoot)
        self.songsScroll.setObjectName(u"songsScroll")
        self.songsScroll.setWidgetResizable(True)
        self.songsScroll.setFrameShape(QFrame.NoFrame)
        self.songsScroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.songsScroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.songsInner = QWidget()
        self.songsInner.setObjectName(u"songsInner")
        self.songsRow = QHBoxLayout(self.songsInner)
        self.songsRow.setSpacing(16)
        self.songsRow.setObjectName(u"songsRow")
        self.songsRow.setContentsMargins(0, 0, 0, 0)
        self.song0 = QCustomCoverCard(self.songsInner)
        self.song0.setObjectName(u"song0")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.song0.sizePolicy().hasHeightForWidth())
        self.song0.setSizePolicy(sizePolicy)
        self.song0.setMinimumSize(QSize(182, 150))
        self.song0.setMaximumSize(QSize(182, 16777215))

        self.songsRow.addWidget(self.song0)

        self.song1 = QCustomCoverCard(self.songsInner)
        self.song1.setObjectName(u"song1")
        sizePolicy.setHeightForWidth(self.song1.sizePolicy().hasHeightForWidth())
        self.song1.setSizePolicy(sizePolicy)
        self.song1.setMinimumSize(QSize(182, 150))
        self.song1.setMaximumSize(QSize(182, 16777215))

        self.songsRow.addWidget(self.song1)

        self.song2 = QCustomCoverCard(self.songsInner)
        self.song2.setObjectName(u"song2")
        sizePolicy.setHeightForWidth(self.song2.sizePolicy().hasHeightForWidth())
        self.song2.setSizePolicy(sizePolicy)
        self.song2.setMinimumSize(QSize(182, 150))
        self.song2.setMaximumSize(QSize(182, 16777215))

        self.songsRow.addWidget(self.song2)

        self.song3 = QCustomCoverCard(self.songsInner)
        self.song3.setObjectName(u"song3")
        sizePolicy.setHeightForWidth(self.song3.sizePolicy().hasHeightForWidth())
        self.song3.setSizePolicy(sizePolicy)
        self.song3.setMinimumSize(QSize(182, 150))
        self.song3.setMaximumSize(QSize(182, 16777215))

        self.songsRow.addWidget(self.song3)

        self.song4 = QCustomCoverCard(self.songsInner)
        self.song4.setObjectName(u"song4")
        sizePolicy.setHeightForWidth(self.song4.sizePolicy().hasHeightForWidth())
        self.song4.setSizePolicy(sizePolicy)
        self.song4.setMinimumSize(QSize(182, 150))
        self.song4.setMaximumSize(QSize(182, 16777215))

        self.songsRow.addWidget(self.song4)

        self.song5 = QCustomCoverCard(self.songsInner)
        self.song5.setObjectName(u"song5")
        sizePolicy.setHeightForWidth(self.song5.sizePolicy().hasHeightForWidth())
        self.song5.setSizePolicy(sizePolicy)
        self.song5.setMinimumSize(QSize(182, 150))
        self.song5.setMaximumSize(QSize(182, 16777215))

        self.songsRow.addWidget(self.song5)

        self.songsTail = QSpacerItem(0, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.songsRow.addItem(self.songsTail)

        self.songsScroll.setWidget(self.songsInner)

        self.popularLayout.addWidget(self.songsScroll)


        self.retranslateUi(popularRoot)

        QMetaObject.connectSlotsByName(popularRoot)
    # setupUi

    def retranslateUi(self, popularRoot):
        self.popularTitle.setText(QCoreApplication.translate("PopularSongs", u"Popular songs", None))
        self.prevSongBtn.setText("")
        self.prevSongBtn.setProperty(u"iconName", QCoreApplication.translate("PopularSongs", u"chevron-left", None))
        self.nextSongBtn.setText("")
        self.nextSongBtn.setProperty(u"iconName", QCoreApplication.translate("PopularSongs", u"chevron-right", None))
        pass
    # retranslateUi

