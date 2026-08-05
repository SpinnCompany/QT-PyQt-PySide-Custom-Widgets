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

from Custom_Widgets.QCustomMultiSelect import QCustomMultiSelect
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(520, 520)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(16)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(24, 24, 24, 24)
        self.coloursHeading = QLabel(self.centralwidget)
        self.coloursHeading.setObjectName(u"coloursHeading")
        font = QFont()
        font.setBold(True)
        self.coloursHeading.setFont(font)

        self.verticalLayout.addWidget(self.coloursHeading)

        self.coloursSelect = QCustomMultiSelect(self.centralwidget)
        self.coloursSelect.setObjectName(u"coloursSelect")

        self.verticalLayout.addWidget(self.coloursSelect)

        self.languagesHeading = QLabel(self.centralwidget)
        self.languagesHeading.setObjectName(u"languagesHeading")
        self.languagesHeading.setFont(font)

        self.verticalLayout.addWidget(self.languagesHeading)

        self.languagesSelect = QCustomMultiSelect(self.centralwidget)
        self.languagesSelect.setObjectName(u"languagesSelect")
        self.languagesSelect.setProperty(u"searchable", True)

        self.verticalLayout.addWidget(self.languagesSelect)

        self.cappedHeading = QLabel(self.centralwidget)
        self.cappedHeading.setObjectName(u"cappedHeading")
        self.cappedHeading.setFont(font)

        self.verticalLayout.addWidget(self.cappedHeading)

        self.cappedSelect = QCustomMultiSelect(self.centralwidget)
        self.cappedSelect.setObjectName(u"cappedSelect")
        self.cappedSelect.setProperty(u"maxSelection", 3)

        self.verticalLayout.addWidget(self.cappedSelect)

        self.collapsedHeading = QLabel(self.centralwidget)
        self.collapsedHeading.setObjectName(u"collapsedHeading")
        self.collapsedHeading.setFont(font)

        self.verticalLayout.addWidget(self.collapsedHeading)

        self.collapsedSelect = QCustomMultiSelect(self.centralwidget)
        self.collapsedSelect.setObjectName(u"collapsedSelect")
        self.collapsedSelect.setProperty(u"maxChips", 2)

        self.verticalLayout.addWidget(self.collapsedSelect)

        self.controlsRow = QHBoxLayout()
        self.controlsRow.setObjectName(u"controlsRow")
        self.clearButton = QPushButton(self.centralwidget)
        self.clearButton.setObjectName(u"clearButton")

        self.controlsRow.addWidget(self.clearButton)

        self.selectAllButton = QPushButton(self.centralwidget)
        self.selectAllButton.setObjectName(u"selectAllButton")

        self.controlsRow.addWidget(self.selectAllButton)

        self.themeButton = QPushButton(self.centralwidget)
        self.themeButton.setObjectName(u"themeButton")

        self.controlsRow.addWidget(self.themeButton)

        self.controlsSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.controlsRow.addItem(self.controlsSpacer)


        self.verticalLayout.addLayout(self.controlsRow)

        self.statusLabel = QLabel(self.centralwidget)
        self.statusLabel.setObjectName(u"statusLabel")

        self.verticalLayout.addWidget(self.statusLabel)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"QCustomMultiSelect", None))
        self.coloursHeading.setText(QCoreApplication.translate("MainWindow", u"Colours", None))
        self.coloursSelect.setProperty(u"optionsCsv", QCoreApplication.translate("MainWindow", u"Red,Green,Blue", None))
        self.coloursSelect.setProperty(u"placeholderText", QCoreApplication.translate("MainWindow", u"Choose colours", None))
        self.languagesHeading.setText(QCoreApplication.translate("MainWindow", u"Languages (searchable)", None))
        self.languagesSelect.setProperty(u"optionsCsv", QCoreApplication.translate("MainWindow", u"py=Python,js=JavaScript,rs=Rust,go=Go,cpp=C++,rb=Ruby,kt=Kotlin,swift=Swift,ts=TypeScript", None))
        self.languagesSelect.setProperty(u"placeholderText", QCoreApplication.translate("MainWindow", u"Search and pick", None))
        self.cappedHeading.setText(QCoreApplication.translate("MainWindow", u"Pick at most 3", None))
        self.cappedSelect.setProperty(u"optionsCsv", QCoreApplication.translate("MainWindow", u"py=Python,js=JavaScript,rs=Rust,go=Go,cpp=C++,rb=Ruby,kt=Kotlin,swift=Swift,ts=TypeScript", None))
        self.cappedSelect.setProperty(u"placeholderText", QCoreApplication.translate("MainWindow", u"Up to three", None))
        self.collapsedHeading.setText(QCoreApplication.translate("MainWindow", u"Collapses past 2 chips", None))
        self.collapsedSelect.setProperty(u"optionsCsv", QCoreApplication.translate("MainWindow", u"py=Python,js=JavaScript,rs=Rust,go=Go,cpp=C++,rb=Ruby,kt=Kotlin,swift=Swift,ts=TypeScript", None))
        self.collapsedSelect.setProperty(u"selectedCsv", QCoreApplication.translate("MainWindow", u"py,js,rs,go", None))
        self.clearButton.setText(QCoreApplication.translate("MainWindow", u"Clear colours", None))
        self.selectAllButton.setText(QCoreApplication.translate("MainWindow", u"Select all languages", None))
        self.themeButton.setText(QCoreApplication.translate("MainWindow", u"Light / dark", None))
        self.statusLabel.setText(QCoreApplication.translate("MainWindow", u"Nothing selected yet", None))
    # retranslateUi

