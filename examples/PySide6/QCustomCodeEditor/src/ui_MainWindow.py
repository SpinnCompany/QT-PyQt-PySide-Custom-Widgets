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

from Custom_Widgets.QCustomCodeEditor import QCustomCodeEditor
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(640, 560)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.rootLayout = QVBoxLayout(self.centralwidget)
        self.rootLayout.setSpacing(10)
        self.rootLayout.setObjectName(u"rootLayout")
        self.rootLayout.setContentsMargins(12, 12, 12, 12)
        self.themeRow = QHBoxLayout()
        self.themeRow.setSpacing(6)
        self.themeRow.setObjectName(u"themeRow")
        self.themeDefaultButton = QPushButton(self.centralwidget)
        self.themeDefaultButton.setObjectName(u"themeDefaultButton")

        self.themeRow.addWidget(self.themeDefaultButton)

        self.themeOneLightButton = QPushButton(self.centralwidget)
        self.themeOneLightButton.setObjectName(u"themeOneLightButton")

        self.themeRow.addWidget(self.themeOneLightButton)

        self.themeOneDarkButton = QPushButton(self.centralwidget)
        self.themeOneDarkButton.setObjectName(u"themeOneDarkButton")

        self.themeRow.addWidget(self.themeOneDarkButton)

        self.themeMonokaiButton = QPushButton(self.centralwidget)
        self.themeMonokaiButton.setObjectName(u"themeMonokaiButton")

        self.themeRow.addWidget(self.themeMonokaiButton)

        self.themeOceanicButton = QPushButton(self.centralwidget)
        self.themeOceanicButton.setObjectName(u"themeOceanicButton")

        self.themeRow.addWidget(self.themeOceanicButton)

        self.themeZenburnButton = QPushButton(self.centralwidget)
        self.themeZenburnButton.setObjectName(u"themeZenburnButton")

        self.themeRow.addWidget(self.themeZenburnButton)

        self.themeSpacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.themeRow.addItem(self.themeSpacer)


        self.rootLayout.addLayout(self.themeRow)

        self.editor1Label = QLabel(self.centralwidget)
        self.editor1Label.setObjectName(u"editor1Label")

        self.rootLayout.addWidget(self.editor1Label)

        self.editor1 = QCustomCodeEditor(self.centralwidget)
        self.editor1.setObjectName(u"editor1")

        self.rootLayout.addWidget(self.editor1)

        self.editor2Label = QLabel(self.centralwidget)
        self.editor2Label.setObjectName(u"editor2Label")

        self.rootLayout.addWidget(self.editor2Label)

        self.editor2 = QCustomCodeEditor(self.centralwidget)
        self.editor2.setObjectName(u"editor2")

        self.rootLayout.addWidget(self.editor2)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"QCustomCodeEditor", None))
        self.themeDefaultButton.setText(QCoreApplication.translate("MainWindow", u"Default", None))
        self.themeOneLightButton.setText(QCoreApplication.translate("MainWindow", u"One Light", None))
        self.themeOneDarkButton.setText(QCoreApplication.translate("MainWindow", u"One Dark", None))
        self.themeMonokaiButton.setText(QCoreApplication.translate("MainWindow", u"Monokai", None))
        self.themeOceanicButton.setText(QCoreApplication.translate("MainWindow", u"Oceanic", None))
        self.themeZenburnButton.setText(QCoreApplication.translate("MainWindow", u"Zenburn", None))
        self.editor1Label.setText(QCoreApplication.translate("MainWindow", u"Primary Code Editor", None))
        self.editor2Label.setText(QCoreApplication.translate("MainWindow", u"Embedded Code Editor", None))
    # retranslateUi

