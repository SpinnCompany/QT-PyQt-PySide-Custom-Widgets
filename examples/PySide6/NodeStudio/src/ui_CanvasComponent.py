# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'new_CanvasComponent.ui'
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
from Custom_Widgets.QCustomNodeGraph import QCustomNodeGraph
class Ui_CanvasComponent(object):
    def setupUi(self, CanvasComponent):
        if not CanvasComponent.objectName():
            CanvasComponent.setObjectName(u"CanvasComponent")
        CanvasComponent.resize(640, 520)
        self.canvasOuter = QVBoxLayout(CanvasComponent)
        self.canvasOuter.setSpacing(0)
        self.canvasOuter.setObjectName(u"canvasOuter")
        self.canvasOuter.setContentsMargins(0, 0, 0, 0)
        self.canvasFrame = QFrame(CanvasComponent)
        self.canvasFrame.setObjectName(u"canvasFrame")
        self.canvasFrame.setFrameShape(QFrame.StyledPanel)
        self.canvasLayout = QVBoxLayout(self.canvasFrame)
        self.canvasLayout.setSpacing(0)
        self.canvasLayout.setObjectName(u"canvasLayout")
        self.canvasLayout.setContentsMargins(10, 10, 10, 10)
        self.nodeGraph = QCustomNodeGraph(self.canvasFrame)
        self.nodeGraph.setObjectName(u"nodeGraph")

        self.canvasLayout.addWidget(self.nodeGraph)


        self.canvasOuter.addWidget(self.canvasFrame)


        self.retranslateUi(CanvasComponent)

        QMetaObject.connectSlotsByName(CanvasComponent)
    # setupUi

    def retranslateUi(self, CanvasComponent):
        pass
    # retranslateUi

