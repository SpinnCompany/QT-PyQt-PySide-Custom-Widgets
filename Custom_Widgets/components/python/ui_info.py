# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'infoEebOdu.ui'
##
## Created by: Qt User Interface Compiler version 6.7.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from qtpy.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from qtpy.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from qtpy.QtWidgets import (QApplication, QHBoxLayout, QLabel, QPushButton,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(444, 79)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)
        self.header = QWidget(Form)
        self.header.setObjectName(u"header")
        self.horizontalLayout = QHBoxLayout(self.header)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.iconlabel = QLabel(self.header)
        self.iconlabel.setObjectName(u"iconlabel")
        self.iconlabel.setMinimumSize(QSize(20, 20))
        self.iconlabel.setMaximumSize(QSize(20, 20))
        self.iconlabel.setScaledContents(True)

        self.horizontalLayout.addWidget(self.iconlabel, 0, Qt.AlignmentFlag.AlignLeft)

        self.titlelabel = QLabel(self.header)
        self.titlelabel.setObjectName(u"titlelabel")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.titlelabel.sizePolicy().hasHeightForWidth())
        self.titlelabel.setSizePolicy(sizePolicy)
        font = QFont()
        font.setBold(True)
        self.titlelabel.setFont(font)
        self.titlelabel.setWordWrap(True)

        self.horizontalLayout.addWidget(self.titlelabel)

        self.closeButton = QPushButton(self.header)
        self.closeButton.setObjectName(u"closeButton")
        self.closeButton.setCursor(QCursor(Qt.PointingHandCursor))
        icon = QIcon(QIcon.fromTheme(u"application-exit"))
        self.closeButton.setIcon(icon)

        self.horizontalLayout.addWidget(self.closeButton, 0, Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTop)


        self.verticalLayout.addWidget(self.header)

        self.body = QWidget(Form)
        self.body.setObjectName(u"body")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.body.sizePolicy().hasHeightForWidth())
        self.body.setSizePolicy(sizePolicy1)
        self.verticalLayout_2 = QVBoxLayout(self.body)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.bodyLabel = QLabel(self.body)
        self.bodyLabel.setObjectName(u"bodyLabel")
        self.bodyLabel.setWordWrap(True)

        self.verticalLayout_2.addWidget(self.bodyLabel)


        self.verticalLayout.addWidget(self.body)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.iconlabel.setText("")
        self.titlelabel.setText(QCoreApplication.translate("Form", u"Title", None))
        self.closeButton.setText("")
        self.bodyLabel.setText(QCoreApplication.translate("Form", u"Body", None))
    # retranslateUi

