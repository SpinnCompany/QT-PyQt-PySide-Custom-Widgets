# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'new_ThreadComponent.ui'
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
    QPushButton, QSizePolicy, QVBoxLayout, QWidget)

from Custom_Widgets.QCustomChatThread import QCustomChatThread
from Custom_Widgets.QCustomComponent import QCustomComponent
from Custom_Widgets.QCustomComponentContainer import QCustomComponentContainer
class Ui_ThreadComponent(object):
    def setupUi(self, ThreadComponent):
        if not ThreadComponent.objectName():
            ThreadComponent.setObjectName(u"ThreadComponent")
        ThreadComponent.resize(700, 794)
        self.threadComponentOuter = QVBoxLayout(ThreadComponent)
        self.threadComponentOuter.setSpacing(0)
        self.threadComponentOuter.setObjectName(u"threadComponentOuter")
        self.threadComponentOuter.setContentsMargins(0, 0, 0, 0)
        self.threadPanel = QFrame(ThreadComponent)
        self.threadPanel.setObjectName(u"threadPanel")
        self.threadPanel.setFrameShape(QFrame.StyledPanel)
        self.threadLayoutOuter = QVBoxLayout(self.threadPanel)
        self.threadLayoutOuter.setSpacing(0)
        self.threadLayoutOuter.setObjectName(u"threadLayoutOuter")
        self.threadLayoutOuter.setContentsMargins(0, 0, 0, 0)
        self.threadHeaderContainer = QCustomComponentContainer(self.threadPanel)
        self.threadHeaderContainer.setObjectName(u"threadHeaderContainer")
        self.threadHeaderContainer.setMinimumSize(QSize(0, 78))
        self.threadHeaderContainer.setMaximumSize(QSize(16777215, 78))
        self.threadHeaderContainer.setProperty(u"previewComponent", False)

        self.threadLayoutOuter.addWidget(self.threadHeaderContainer)

        self.creditsBanner = QFrame(self.threadPanel)
        self.creditsBanner.setObjectName(u"creditsBanner")
        self.creditsBanner.setMinimumSize(QSize(0, 34))
        self.creditsBanner.setMaximumSize(QSize(16777215, 34))
        self.creditsBanner.setFrameShape(QFrame.StyledPanel)
        self.creditsRow = QHBoxLayout(self.creditsBanner)
        self.creditsRow.setObjectName(u"creditsRow")
        self.creditsRow.setContentsMargins(24, 0, 24, 0)
        self.creditsLabel = QLabel(self.creditsBanner)
        self.creditsLabel.setObjectName(u"creditsLabel")
        self.creditsLabel.setAlignment(Qt.AlignCenter)

        self.creditsRow.addWidget(self.creditsLabel)


        self.threadLayoutOuter.addWidget(self.creditsBanner)

        self.chatThread = QCustomChatThread(self.threadPanel)
        self.chatThread.setObjectName(u"chatThread")

        self.threadLayoutOuter.addWidget(self.chatThread)

        self.composerContainer = QCustomComponentContainer(self.threadPanel)
        self.composerContainer.setObjectName(u"composerContainer")
        self.composerContainer.setMinimumSize(QSize(0, 74))
        self.composerContainer.setMaximumSize(QSize(16777215, 74))
        self.composerContainer.setProperty(u"previewComponent", False)

        self.threadLayoutOuter.addWidget(self.composerContainer)


        self.threadComponentOuter.addWidget(self.threadPanel)


        self.retranslateUi(ThreadComponent)

        QMetaObject.connectSlotsByName(ThreadComponent)
    # setupUi

    def retranslateUi(self, ThreadComponent):
        self.threadHeaderContainer.setProperty(u"filePath", QCoreApplication.translate("ThreadComponent", u"ui/ThreadHeaderComponent.ui", None))
        self.creditsLabel.setText(QCoreApplication.translate("ThreadComponent", u"CREDITS AVAILABLE:  5", None))
        self.creditsLabel.setProperty(u"role", QCoreApplication.translate("ThreadComponent", u"creditsLabel", None))
        self.composerContainer.setProperty(u"filePath", QCoreApplication.translate("ThreadComponent", u"ui/ComposerComponent.ui", None))
        pass
    # retranslateUi

