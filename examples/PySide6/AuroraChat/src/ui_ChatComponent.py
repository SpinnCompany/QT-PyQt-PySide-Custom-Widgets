# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'new_ChatComponent.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QPushButton,
    QSizePolicy, QWidget)

from Custom_Widgets.QCustomComponent import QCustomComponent
from Custom_Widgets.QCustomComponentContainer import QCustomComponentContainer
class Ui_ChatComponent(object):
    def setupUi(self, ChatComponent):
        if not ChatComponent.objectName():
            ChatComponent.setObjectName(u"ChatComponent")
        ChatComponent.resize(1228, 880)
        self.chatOuter = QHBoxLayout(ChatComponent)
        self.chatOuter.setSpacing(0)
        self.chatOuter.setObjectName(u"chatOuter")
        self.chatOuter.setContentsMargins(0, 0, 0, 0)
        self.chatsContainer = QCustomComponentContainer(ChatComponent)
        self.chatsContainer.setObjectName(u"chatsContainer")
        self.chatsContainer.setMinimumSize(QSize(336, 0))
        self.chatsContainer.setMaximumSize(QSize(336, 16777215))
        self.chatsContainer.setProperty(u"previewComponent", False)

        self.chatOuter.addWidget(self.chatsContainer)

        self.threadContainer = QCustomComponentContainer(ChatComponent)
        self.threadContainer.setObjectName(u"threadContainer")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.threadContainer.sizePolicy().hasHeightForWidth())
        self.threadContainer.setSizePolicy(sizePolicy)
        self.threadContainer.setProperty(u"previewComponent", False)

        self.chatOuter.addWidget(self.threadContainer)

        self.profileContainer = QCustomComponentContainer(ChatComponent)
        self.profileContainer.setObjectName(u"profileContainer")
        self.profileContainer.setMinimumSize(QSize(304, 0))
        self.profileContainer.setMaximumSize(QSize(304, 16777215))
        self.profileContainer.setProperty(u"previewComponent", False)

        self.chatOuter.addWidget(self.profileContainer)


        self.retranslateUi(ChatComponent)

        QMetaObject.connectSlotsByName(ChatComponent)
    # setupUi

    def retranslateUi(self, ChatComponent):
        self.chatsContainer.setProperty(u"filePath", QCoreApplication.translate("ChatComponent", u"ui/ChatsListComponent.ui", None))
        self.threadContainer.setProperty(u"filePath", QCoreApplication.translate("ChatComponent", u"ui/ThreadComponent.ui", None))
        self.profileContainer.setProperty(u"filePath", QCoreApplication.translate("ChatComponent", u"ui/ProfileComponent.ui", None))
        pass
    # retranslateUi

