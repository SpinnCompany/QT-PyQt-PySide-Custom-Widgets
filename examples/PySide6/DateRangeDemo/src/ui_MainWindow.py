# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'new_MainWindow.ui'
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
    QMainWindow, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

from Custom_Widgets.QCustomDateRangePicker import QCustomDateRangePicker
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1000, 720)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.outerLayout = QVBoxLayout(self.centralwidget)
        self.outerLayout.setSpacing(20)
        self.outerLayout.setObjectName(u"outerLayout")
        self.outerLayout.setContentsMargins(28, 28, 28, 28)
        self.lightCard = QFrame(self.centralwidget)
        self.lightCard.setObjectName(u"lightCard")
        self.lightCard.setFrameShape(QFrame.NoFrame)
        self.cardLayout = QVBoxLayout(self.lightCard)
        self.cardLayout.setSpacing(16)
        self.cardLayout.setObjectName(u"cardLayout")
        self.cardLayout.setContentsMargins(24, 22, 24, 22)
        self.lightTitle = QLabel(self.lightCard)
        self.lightTitle.setObjectName(u"lightTitle")

        self.cardLayout.addWidget(self.lightTitle)

        self.picker = QCustomDateRangePicker(self.lightCard)
        self.picker.setObjectName(u"picker")
        self.picker.setMinimumSize(QSize(0, 320))
        self.picker.setProperty(u"monthsVisible", 2)

        self.cardLayout.addWidget(self.picker)

        self.fieldsRow = QHBoxLayout()
        self.fieldsRow.setSpacing(12)
        self.fieldsRow.setObjectName(u"fieldsRow")
        self.startField = QFrame(self.lightCard)
        self.startField.setObjectName(u"startField")
        self.startField.setFrameShape(QFrame.NoFrame)
        self.startFieldLayout = QVBoxLayout(self.startField)
        self.startFieldLayout.setSpacing(0)
        self.startFieldLayout.setObjectName(u"startFieldLayout")
        self.startFieldLayout.setContentsMargins(14, 8, 14, 8)
        self.startCap = QLabel(self.startField)
        self.startCap.setObjectName(u"startCap")

        self.startFieldLayout.addWidget(self.startCap)

        self.startVal = QLabel(self.startField)
        self.startVal.setObjectName(u"startVal")

        self.startFieldLayout.addWidget(self.startVal)


        self.fieldsRow.addWidget(self.startField)

        self.endField = QFrame(self.lightCard)
        self.endField.setObjectName(u"endField")
        self.endField.setFrameShape(QFrame.NoFrame)
        self.endFieldLayout = QVBoxLayout(self.endField)
        self.endFieldLayout.setSpacing(0)
        self.endFieldLayout.setObjectName(u"endFieldLayout")
        self.endFieldLayout.setContentsMargins(14, 8, 14, 8)
        self.endCap = QLabel(self.endField)
        self.endCap.setObjectName(u"endCap")

        self.endFieldLayout.addWidget(self.endCap)

        self.endVal = QLabel(self.endField)
        self.endVal.setObjectName(u"endVal")

        self.endFieldLayout.addWidget(self.endVal)


        self.fieldsRow.addWidget(self.endField)

        self.fieldsSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.fieldsRow.addItem(self.fieldsSpacer)

        self.saveButton = QPushButton(self.lightCard)
        self.saveButton.setObjectName(u"saveButton")
        self.saveButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.fieldsRow.addWidget(self.saveButton)


        self.cardLayout.addLayout(self.fieldsRow)

        self.cardLayout.setStretch(1, 1)

        self.outerLayout.addWidget(self.lightCard)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"QCustomDateRangePicker \u2014 preview", None))
        self.lightTitle.setText(QCoreApplication.translate("MainWindow", u"Select your travel dates", None))
        self.startCap.setText(QCoreApplication.translate("MainWindow", u"Start date", None))
        self.startVal.setText(QCoreApplication.translate("MainWindow", u"\u2014", None))
        self.endCap.setText(QCoreApplication.translate("MainWindow", u"End date", None))
        self.endVal.setText(QCoreApplication.translate("MainWindow", u"\u2014", None))
        self.saveButton.setText(QCoreApplication.translate("MainWindow", u"Save dates", None))
    # retranslateUi

