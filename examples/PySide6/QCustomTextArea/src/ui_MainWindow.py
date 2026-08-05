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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QMainWindow,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

from Custom_Widgets.QCustomTextArea import QCustomTextArea
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(520, 640)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.rootLayout = QVBoxLayout(self.centralwidget)
        self.rootLayout.setSpacing(16)
        self.rootLayout.setObjectName(u"rootLayout")
        self.rootLayout.setContentsMargins(24, 24, 24, 24)
        self.bioHeading = QLabel(self.centralwidget)
        self.bioHeading.setObjectName(u"bioHeading")

        self.rootLayout.addWidget(self.bioHeading)

        self.bio = QCustomTextArea(self.centralwidget)
        self.bio.setObjectName(u"bio")
        self.bio.setProperty(u"maxLength", 140)
        self.bio.setProperty(u"showCounter", True)
        self.bio.setProperty(u"minRows", 3)

        self.rootLayout.addWidget(self.bio)

        self.messageHeading = QLabel(self.centralwidget)
        self.messageHeading.setObjectName(u"messageHeading")

        self.rootLayout.addWidget(self.messageHeading)

        self.message = QCustomTextArea(self.centralwidget)
        self.message.setObjectName(u"message")
        self.message.setProperty(u"minRows", 2)
        self.message.setProperty(u"maxRows", 6)
        self.message.setProperty(u"autoGrow", True)

        self.rootLayout.addWidget(self.message)

        self.notesHeading = QLabel(self.centralwidget)
        self.notesHeading.setObjectName(u"notesHeading")

        self.rootLayout.addWidget(self.notesHeading)

        self.notes = QCustomTextArea(self.centralwidget)
        self.notes.setObjectName(u"notes")
        self.notes.setProperty(u"minRows", 2)

        self.rootLayout.addWidget(self.notes)

        self.actionsRow = QHBoxLayout()
        self.actionsRow.setSpacing(8)
        self.actionsRow.setObjectName(u"actionsRow")
        self.validateBtn = QPushButton(self.centralwidget)
        self.validateBtn.setObjectName(u"validateBtn")

        self.actionsRow.addWidget(self.validateBtn)

        self.sizeSmBtn = QPushButton(self.centralwidget)
        self.sizeSmBtn.setObjectName(u"sizeSmBtn")

        self.actionsRow.addWidget(self.sizeSmBtn)

        self.sizeMdBtn = QPushButton(self.centralwidget)
        self.sizeMdBtn.setObjectName(u"sizeMdBtn")

        self.actionsRow.addWidget(self.sizeMdBtn)

        self.sizeLgBtn = QPushButton(self.centralwidget)
        self.sizeLgBtn.setObjectName(u"sizeLgBtn")

        self.actionsRow.addWidget(self.sizeLgBtn)

        self.themeBtn = QPushButton(self.centralwidget)
        self.themeBtn.setObjectName(u"themeBtn")

        self.actionsRow.addWidget(self.themeBtn)

        self.actionsSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.actionsRow.addItem(self.actionsSpacer)


        self.rootLayout.addLayout(self.actionsRow)

        self.status = QLabel(self.centralwidget)
        self.status.setObjectName(u"status")

        self.rootLayout.addWidget(self.status)

        self.bottomSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.rootLayout.addItem(self.bottomSpacer)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"QCustomTextArea", None))
        self.bioHeading.setText(QCoreApplication.translate("MainWindow", u"Bio (limited to 140 characters)", None))
        self.bio.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Tell people about yourself...", None))
        self.messageHeading.setText(QCoreApplication.translate("MainWindow", u"Message (grows from 2 to 6 rows)", None))
        self.message.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Type several lines...", None))
        self.notesHeading.setText(QCoreApplication.translate("MainWindow", u"Notes (validated on demand)", None))
        self.notes.setPlaceholderText(QCoreApplication.translate("MainWindow", u"At least 10 characters", None))
        self.validateBtn.setText(QCoreApplication.translate("MainWindow", u"Validate notes", None))
        self.sizeSmBtn.setText(QCoreApplication.translate("MainWindow", u"size sm", None))
        self.sizeMdBtn.setText(QCoreApplication.translate("MainWindow", u"size md", None))
        self.sizeLgBtn.setText(QCoreApplication.translate("MainWindow", u"size lg", None))
        self.themeBtn.setText(QCoreApplication.translate("MainWindow", u"Light / dark", None))
        self.status.setText(QCoreApplication.translate("MainWindow", u"Bio: 0/140", None))
    # retranslateUi

