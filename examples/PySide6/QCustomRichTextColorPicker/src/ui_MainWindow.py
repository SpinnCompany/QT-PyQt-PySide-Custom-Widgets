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

from Custom_Widgets.QCustomAvatar import QCustomAvatar
from Custom_Widgets.QCustomColorPicker import QCustomColorPicker
from Custom_Widgets.QCustomRichTextEditor import QCustomRichTextEditor
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(560, 460)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.mainLayout = QVBoxLayout(self.centralwidget)
        self.mainLayout.setSpacing(12)
        self.mainLayout.setObjectName(u"mainLayout")
        self.mainLayout.setContentsMargins(16, 16, 16, 16)
        self.editor = QCustomRichTextEditor(self.centralwidget)
        self.editor.setObjectName(u"editor")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.editor.sizePolicy().hasHeightForWidth())
        self.editor.setSizePolicy(sizePolicy)

        self.mainLayout.addWidget(self.editor)

        self.pickerRow = QHBoxLayout()
        self.pickerRow.setSpacing(10)
        self.pickerRow.setObjectName(u"pickerRow")
        self.accentLabel = QLabel(self.centralwidget)
        self.accentLabel.setObjectName(u"accentLabel")

        self.pickerRow.addWidget(self.accentLabel)

        self.picker = QCustomColorPicker(self.centralwidget)
        self.picker.setObjectName(u"picker")

        self.pickerRow.addWidget(self.picker)

        self.preview = QCustomAvatar(self.centralwidget)
        self.preview.setObjectName(u"preview")
        self.preview.setMinimumSize(QSize(36, 36))
        self.preview.setProperty(u"text", u"Aa")
        self.preview.setProperty(u"cornerRadius", 8)
        self.preview.setProperty(u"showStatus", False)

        self.pickerRow.addWidget(self.preview)

        self.pickerSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.pickerRow.addItem(self.pickerSpacer)


        self.mainLayout.addLayout(self.pickerRow)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Rich Text + Colour Picker", None))
        self.accentLabel.setText(QCoreApplication.translate("MainWindow", u"Accent colour:", None))
    # retranslateUi

