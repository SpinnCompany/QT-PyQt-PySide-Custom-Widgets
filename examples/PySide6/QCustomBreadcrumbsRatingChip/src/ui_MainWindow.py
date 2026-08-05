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

from Custom_Widgets.QCustomBreadcrumbs import QCustomBreadcrumbs
from Custom_Widgets.QCustomChip import QCustomChipGroup
from Custom_Widgets.QCustomRating import QCustomRating
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(480, 420)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.rootLayout = QVBoxLayout(self.centralwidget)
        self.rootLayout.setSpacing(12)
        self.rootLayout.setObjectName(u"rootLayout")
        self.rootLayout.setContentsMargins(16, 16, 16, 16)
        self.breadcrumbs = QCustomBreadcrumbs(self.centralwidget)
        self.breadcrumbs.setObjectName(u"breadcrumbs")

        self.rootLayout.addWidget(self.breadcrumbs)

        self.ratingRow = QHBoxLayout()
        self.ratingRow.setSpacing(8)
        self.ratingRow.setObjectName(u"ratingRow")
        self.rateLabel = QLabel(self.centralwidget)
        self.rateLabel.setObjectName(u"rateLabel")

        self.ratingRow.addWidget(self.rateLabel)

        self.rating = QCustomRating(self.centralwidget)
        self.rating.setObjectName(u"rating")
        self.rating.setProperty(u"maximum", 5)
        self.rating.setProperty(u"value", 3)

        self.ratingRow.addWidget(self.rating)

        self.ratingSpacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.ratingRow.addItem(self.ratingSpacer)


        self.rootLayout.addLayout(self.ratingRow)

        self.tagsLabel = QLabel(self.centralwidget)
        self.tagsLabel.setObjectName(u"tagsLabel")

        self.rootLayout.addWidget(self.tagsLabel)

        self.tagsGroup = QCustomChipGroup(self.centralwidget)
        self.tagsGroup.setObjectName(u"tagsGroup")

        self.rootLayout.addWidget(self.tagsGroup)

        self.filtersLabel = QLabel(self.centralwidget)
        self.filtersLabel.setObjectName(u"filtersLabel")

        self.rootLayout.addWidget(self.filtersLabel)

        self.filtersGroup = QCustomChipGroup(self.centralwidget)
        self.filtersGroup.setObjectName(u"filtersGroup")

        self.rootLayout.addWidget(self.filtersGroup)

        self.bottomSpacer = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.rootLayout.addItem(self.bottomSpacer)

        self.statusLabel = QLabel(self.centralwidget)
        self.statusLabel.setObjectName(u"statusLabel")

        self.rootLayout.addWidget(self.statusLabel)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Breadcrumbs / Rating / Chips", None))
        self.rateLabel.setText(QCoreApplication.translate("MainWindow", u"Rate:", None))
        self.tagsLabel.setText(QCoreApplication.translate("MainWindow", u"Removable tags:", None))
        self.filtersLabel.setText(QCoreApplication.translate("MainWindow", u"Filter (multi-select):", None))
        self.statusLabel.setText(QCoreApplication.translate("MainWindow", u"-", None))
    # retranslateUi

