# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'new_ChatsListComponent.ui'
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
    QLineEdit, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

from Custom_Widgets.QCustomChatList import QCustomChatList
from Custom_Widgets.QCustomComponent import QCustomComponent
class Ui_ChatsListComponent(object):
    def setupUi(self, ChatsListComponent):
        if not ChatsListComponent.objectName():
            ChatsListComponent.setObjectName(u"ChatsListComponent")
        ChatsListComponent.resize(336, 794)
        ChatsListComponent.setMinimumSize(QSize(336, 0))
        ChatsListComponent.setMaximumSize(QSize(336, 16777215))
        self.chatsListOuter = QVBoxLayout(ChatsListComponent)
        self.chatsListOuter.setSpacing(0)
        self.chatsListOuter.setObjectName(u"chatsListOuter")
        self.chatsListOuter.setContentsMargins(0, 0, 0, 0)
        self.chatsPanel = QFrame(ChatsListComponent)
        self.chatsPanel.setObjectName(u"chatsPanel")
        self.chatsPanel.setFrameShape(QFrame.StyledPanel)
        self.chatsLayout = QVBoxLayout(self.chatsPanel)
        self.chatsLayout.setSpacing(14)
        self.chatsLayout.setObjectName(u"chatsLayout")
        self.chatsLayout.setContentsMargins(18, 22, 18, 16)
        self.chatsHeaderRow = QHBoxLayout()
        self.chatsHeaderRow.setObjectName(u"chatsHeaderRow")
        self.chatsTitle = QLabel(self.chatsPanel)
        self.chatsTitle.setObjectName(u"chatsTitle")

        self.chatsHeaderRow.addWidget(self.chatsTitle)

        self.chatsHeaderSpacer = QSpacerItem(10, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.chatsHeaderRow.addItem(self.chatsHeaderSpacer)

        self.newGroupBtn = QPushButton(self.chatsPanel)
        self.newGroupBtn.setObjectName(u"newGroupBtn")
        self.newGroupBtn.setMinimumSize(QSize(34, 34))
        self.newGroupBtn.setMaximumSize(QSize(34, 34))
        self.newGroupBtn.setIconSize(QSize(18, 18))
        self.newGroupBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.chatsHeaderRow.addWidget(self.newGroupBtn)

        self.newChatBtn = QPushButton(self.chatsPanel)
        self.newChatBtn.setObjectName(u"newChatBtn")
        self.newChatBtn.setMinimumSize(QSize(34, 34))
        self.newChatBtn.setMaximumSize(QSize(34, 34))
        self.newChatBtn.setIconSize(QSize(18, 18))
        self.newChatBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.chatsHeaderRow.addWidget(self.newChatBtn)


        self.chatsLayout.addLayout(self.chatsHeaderRow)

        self.searchEdit = QLineEdit(self.chatsPanel)
        self.searchEdit.setObjectName(u"searchEdit")
        self.searchEdit.setMinimumSize(QSize(0, 42))

        self.chatsLayout.addWidget(self.searchEdit)

        self.chatList = QCustomChatList(self.chatsPanel)
        self.chatList.setObjectName(u"chatList")

        self.chatsLayout.addWidget(self.chatList)


        self.chatsListOuter.addWidget(self.chatsPanel)


        self.retranslateUi(ChatsListComponent)

        QMetaObject.connectSlotsByName(ChatsListComponent)
    # setupUi

    def retranslateUi(self, ChatsListComponent):
        self.chatsTitle.setText(QCoreApplication.translate("ChatsListComponent", u"Chats", None))
        self.chatsTitle.setProperty(u"role", QCoreApplication.translate("ChatsListComponent", u"panelTitle", None))
        self.newGroupBtn.setProperty(u"role", QCoreApplication.translate("ChatsListComponent", u"iconChip", None))
        self.newChatBtn.setProperty(u"role", QCoreApplication.translate("ChatsListComponent", u"iconChip", None))
        self.searchEdit.setPlaceholderText(QCoreApplication.translate("ChatsListComponent", u"   Search Messenger..", None))
        pass
    # retranslateUi

