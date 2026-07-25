# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'new_PreviewComponent.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QLabel, QPushButton,
    QSizePolicy, QVBoxLayout, QWidget)

from Custom_Widgets.QCustomComponent import QCustomComponent
class Ui_PreviewComponent(object):
    def setupUi(self, PreviewComponent):
        if not PreviewComponent.objectName():
            PreviewComponent.setObjectName(u"PreviewComponent")
        PreviewComponent.resize(380, 520)
        self.previewOuter = QVBoxLayout(PreviewComponent)
        self.previewOuter.setSpacing(0)
        self.previewOuter.setObjectName(u"previewOuter")
        self.previewOuter.setContentsMargins(0, 0, 0, 0)
        self.previewFrame = QFrame(PreviewComponent)
        self.previewFrame.setObjectName(u"previewFrame")
        self.previewFrame.setFrameShape(QFrame.StyledPanel)
        self.previewLayout = QVBoxLayout(self.previewFrame)
        self.previewLayout.setSpacing(0)
        self.previewLayout.setObjectName(u"previewLayout")
        self.previewLayout.setContentsMargins(0, 0, 0, 0)
        self.previewImage = QLabel(self.previewFrame)
        self.previewImage.setObjectName(u"previewImage")
        self.previewImage.setAlignment(Qt.AlignCenter)
        self.previewImage.setScaledContents(False)

        self.previewLayout.addWidget(self.previewImage)


        self.previewOuter.addWidget(self.previewFrame)


        self.retranslateUi(PreviewComponent)

        QMetaObject.connectSlotsByName(PreviewComponent)
    # setupUi

    def retranslateUi(self, PreviewComponent):
        self.previewImage.setText("")
        pass
    # retranslateUi

