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
from PySide6.QtWidgets import (QApplication, QFormLayout, QLabel, QMainWindow,
    QPushButton, QSizePolicy, QWidget)

from Custom_Widgets.QCustomDateTimeEdit import (QCustomDateEdit, QCustomDateRangeEdit, QCustomTimeEdit)
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(460, 240)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.formLayout = QFormLayout(self.centralwidget)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setHorizontalSpacing(12)
        self.formLayout.setVerticalSpacing(12)
        self.formLayout.setContentsMargins(20, 20, 20, 20)
        self.dateLabel = QLabel(self.centralwidget)
        self.dateLabel.setObjectName(u"dateLabel")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.dateLabel)

        self.dateEdit = QCustomDateEdit(self.centralwidget)
        self.dateEdit.setObjectName(u"dateEdit")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.dateEdit)

        self.timeLabel = QLabel(self.centralwidget)
        self.timeLabel.setObjectName(u"timeLabel")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.timeLabel)

        self.timeEdit = QCustomTimeEdit(self.centralwidget)
        self.timeEdit.setObjectName(u"timeEdit")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.timeEdit)

        self.rangeLabel = QLabel(self.centralwidget)
        self.rangeLabel.setObjectName(u"rangeLabel")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.rangeLabel)

        self.rangeEdit = QCustomDateRangeEdit(self.centralwidget)
        self.rangeEdit.setObjectName(u"rangeEdit")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.rangeEdit)

        self.resultCaption = QLabel(self.centralwidget)
        self.resultCaption.setObjectName(u"resultCaption")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.LabelRole, self.resultCaption)

        self.resultLabel = QLabel(self.centralwidget)
        self.resultLabel.setObjectName(u"resultLabel")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.FieldRole, self.resultLabel)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"QCustomDateTimeEdit Example", None))
        self.dateLabel.setText(QCoreApplication.translate("MainWindow", u"Date:", None))
        self.timeLabel.setText(QCoreApplication.translate("MainWindow", u"Time:", None))
        self.rangeLabel.setText(QCoreApplication.translate("MainWindow", u"Range:", None))
        self.resultCaption.setText(QCoreApplication.translate("MainWindow", u"Result:", None))
        self.resultLabel.setText(QCoreApplication.translate("MainWindow", u"-", None))
    # retranslateUi

