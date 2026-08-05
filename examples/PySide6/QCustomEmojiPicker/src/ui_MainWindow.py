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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QLineEdit,
    QMainWindow, QPushButton, QSizePolicy, QTextEdit,
    QVBoxLayout, QWidget)
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(600, 400)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(12)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(16, 16, 16, 16)
        self.titleLabel = QLabel(self.centralwidget)
        self.titleLabel.setObjectName(u"titleLabel")

        self.verticalLayout.addWidget(self.titleLabel)

        self.editorsRow = QHBoxLayout()
        self.editorsRow.setSpacing(8)
        self.editorsRow.setObjectName(u"editorsRow")
        self.lineEdit = QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName(u"lineEdit")

        self.editorsRow.addWidget(self.lineEdit)

        self.lineEditBtn = QPushButton(self.centralwidget)
        self.lineEditBtn.setObjectName(u"lineEditBtn")

        self.editorsRow.addWidget(self.lineEditBtn)

        self.textEdit = QTextEdit(self.centralwidget)
        self.textEdit.setObjectName(u"textEdit")

        self.editorsRow.addWidget(self.textEdit)

        self.textEditBtn = QPushButton(self.centralwidget)
        self.textEditBtn.setObjectName(u"textEditBtn")

        self.editorsRow.addWidget(self.textEditBtn)


        self.verticalLayout.addLayout(self.editorsRow)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"QCustomEmojiPicker Example", None))
        self.titleLabel.setText(QCoreApplication.translate("MainWindow", u"Pick emojis into a line edit or a text edit", None))
#if QT_CONFIG(tooltip)
        self.lineEditBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Insert emoji into the line edit", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.textEditBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Insert emoji into the text edit", None))
#endif // QT_CONFIG(tooltip)
    # retranslateUi

