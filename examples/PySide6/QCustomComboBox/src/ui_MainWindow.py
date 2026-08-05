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

from Custom_Widgets.QCustomComboBox import QCustomComboBox
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(420, 200)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.formLayout = QFormLayout(self.centralwidget)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setHorizontalSpacing(12)
        self.formLayout.setVerticalSpacing(12)
        self.formLayout.setContentsMargins(16, 16, 16, 16)
        self.autocompleteLabel = QLabel(self.centralwidget)
        self.autocompleteLabel.setObjectName(u"autocompleteLabel")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.autocompleteLabel)

        self.searchCombo = QCustomComboBox(self.centralwidget)
        self.searchCombo.setObjectName(u"searchCombo")
        self.searchCombo.setEditable(True)

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.searchCombo)

        self.selectLabel = QLabel(self.centralwidget)
        self.selectLabel.setObjectName(u"selectLabel")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.selectLabel)

        self.pickerCombo = QCustomComboBox(self.centralwidget)
        self.pickerCombo.setObjectName(u"pickerCombo")
        self.pickerCombo.setEditable(False)

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.pickerCombo)

        self.resultCaption = QLabel(self.centralwidget)
        self.resultCaption.setObjectName(u"resultCaption")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.resultCaption)

        self.resultLabel = QLabel(self.centralwidget)
        self.resultLabel.setObjectName(u"resultLabel")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.resultLabel)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"QCustomComboBox Example", None))
        self.autocompleteLabel.setText(QCoreApplication.translate("MainWindow", u"Autocomplete:", None))
        self.selectLabel.setText(QCoreApplication.translate("MainWindow", u"Select:", None))
        self.resultCaption.setText(QCoreApplication.translate("MainWindow", u"Result:", None))
        self.resultLabel.setText(QCoreApplication.translate("MainWindow", u"-", None))
    # retranslateUi

