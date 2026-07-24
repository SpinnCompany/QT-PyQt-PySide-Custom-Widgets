# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'new_ComposerComponent.ui'
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

from Custom_Widgets.QCustomChatInput import QCustomChatInput
from Custom_Widgets.QCustomComponent import QCustomComponent
class Ui_ComposerComponent(object):
    def setupUi(self, ComposerComponent):
        if not ComposerComponent.objectName():
            ComposerComponent.setObjectName(u"ComposerComponent")
        ComposerComponent.resize(700, 74)
        self.composerOuter = QVBoxLayout(ComposerComponent)
        self.composerOuter.setSpacing(0)
        self.composerOuter.setObjectName(u"composerOuter")
        self.composerOuter.setContentsMargins(0, 0, 0, 0)
        self.chatInput = QCustomChatInput(ComposerComponent)
        self.chatInput.setObjectName(u"chatInput")
        self.chatInput.setMinimumSize(QSize(0, 74))

        self.composerOuter.addWidget(self.chatInput)


        self.retranslateUi(ComposerComponent)

        QMetaObject.connectSlotsByName(ComposerComponent)
    # setupUi

    def retranslateUi(self, ComposerComponent):
        pass
    # retranslateUi

