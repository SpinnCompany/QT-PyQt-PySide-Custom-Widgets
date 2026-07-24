# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'new_ThreadHeaderComponent.ui'
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

from Custom_Widgets.QCustomAvatar import QCustomAvatar
from Custom_Widgets.QCustomComponent import QCustomComponent
class Ui_ThreadHeaderComponent(object):
    def setupUi(self, ThreadHeaderComponent):
        if not ThreadHeaderComponent.objectName():
            ThreadHeaderComponent.setObjectName(u"ThreadHeaderComponent")
        ThreadHeaderComponent.resize(700, 78)
        self.threadHeaderOuter = QVBoxLayout(ThreadHeaderComponent)
        self.threadHeaderOuter.setSpacing(0)
        self.threadHeaderOuter.setObjectName(u"threadHeaderOuter")
        self.threadHeaderOuter.setContentsMargins(0, 0, 0, 0)
        self.threadHeader = QFrame(ThreadHeaderComponent)
        self.threadHeader.setObjectName(u"threadHeader")
        self.threadHeader.setMinimumSize(QSize(0, 78))
        self.threadHeader.setFrameShape(QFrame.StyledPanel)
        self.threadHeaderRow = QHBoxLayout(self.threadHeader)
        self.threadHeaderRow.setSpacing(12)
        self.threadHeaderRow.setObjectName(u"threadHeaderRow")
        self.threadHeaderRow.setContentsMargins(24, 14, 24, 14)
        self.threadAvatar = QCustomAvatar(self.threadHeader)
        self.threadAvatar.setObjectName(u"threadAvatar")
        self.threadAvatar.setMinimumSize(QSize(44, 44))
        self.threadAvatar.setMaximumSize(QSize(44, 44))

        self.threadHeaderRow.addWidget(self.threadAvatar)

        self.threadTitleCol = QVBoxLayout()
        self.threadTitleCol.setSpacing(2)
        self.threadTitleCol.setObjectName(u"threadTitleCol")
        self.threadName = QLabel(self.threadHeader)
        self.threadName.setObjectName(u"threadName")

        self.threadTitleCol.addWidget(self.threadName)

        self.threadStatus = QLabel(self.threadHeader)
        self.threadStatus.setObjectName(u"threadStatus")

        self.threadTitleCol.addWidget(self.threadStatus)


        self.threadHeaderRow.addLayout(self.threadTitleCol)

        self.threadHeaderSpacer = QSpacerItem(40, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.threadHeaderRow.addItem(self.threadHeaderSpacer)

        self.callBtn = QPushButton(self.threadHeader)
        self.callBtn.setObjectName(u"callBtn")
        self.callBtn.setMinimumSize(QSize(40, 40))
        self.callBtn.setMaximumSize(QSize(40, 40))
        self.callBtn.setIconSize(QSize(19, 19))
        self.callBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.threadHeaderRow.addWidget(self.callBtn)

        self.videoBtn = QPushButton(self.threadHeader)
        self.videoBtn.setObjectName(u"videoBtn")
        self.videoBtn.setMinimumSize(QSize(40, 40))
        self.videoBtn.setMaximumSize(QSize(40, 40))
        self.videoBtn.setIconSize(QSize(19, 19))
        self.videoBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.threadHeaderRow.addWidget(self.videoBtn)

        self.moreBtn = QPushButton(self.threadHeader)
        self.moreBtn.setObjectName(u"moreBtn")
        self.moreBtn.setMinimumSize(QSize(40, 40))
        self.moreBtn.setMaximumSize(QSize(40, 40))
        self.moreBtn.setIconSize(QSize(19, 19))
        self.moreBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.threadHeaderRow.addWidget(self.moreBtn)


        self.threadHeaderOuter.addWidget(self.threadHeader)


        self.retranslateUi(ThreadHeaderComponent)

        QMetaObject.connectSlotsByName(ThreadHeaderComponent)
    # setupUi

    def retranslateUi(self, ThreadHeaderComponent):
        self.threadAvatar.setProperty(u"text", QCoreApplication.translate("ThreadHeaderComponent", u"R", None))
        self.threadName.setText(QCoreApplication.translate("ThreadHeaderComponent", u"Ricky Smith", None))
        self.threadName.setProperty(u"role", QCoreApplication.translate("ThreadHeaderComponent", u"threadName", None))
        self.threadStatus.setText(QCoreApplication.translate("ThreadHeaderComponent", u"Online", None))
        self.threadStatus.setProperty(u"role", QCoreApplication.translate("ThreadHeaderComponent", u"threadStatus", None))
        self.callBtn.setProperty(u"role", QCoreApplication.translate("ThreadHeaderComponent", u"iconChip", None))
        self.videoBtn.setProperty(u"role", QCoreApplication.translate("ThreadHeaderComponent", u"iconChip", None))
        self.moreBtn.setProperty(u"role", QCoreApplication.translate("ThreadHeaderComponent", u"iconChip", None))
        pass
    # retranslateUi

