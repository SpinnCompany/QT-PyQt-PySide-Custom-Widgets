# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'new_CategoriesRow.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QPushButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

from Custom_Widgets.QCustomChip import QCustomChipGroup
from Custom_Widgets.QCustomQPushButton import QCustomQPushButton
class Ui_CategoriesRow(object):
    def setupUi(self, categoriesRoot):
        if not categoriesRoot.objectName():
            categoriesRoot.setObjectName(u"categoriesRoot")
        categoriesRoot.resize(900, 96)
        self.categoriesLayout = QVBoxLayout(categoriesRoot)
        self.categoriesLayout.setSpacing(12)
        self.categoriesLayout.setObjectName(u"categoriesLayout")
        self.categoriesLayout.setContentsMargins(0, 4, 0, 0)
        self.catHeader = QHBoxLayout()
        self.catHeader.setSpacing(8)
        self.catHeader.setObjectName(u"catHeader")
        self.categoriesTitle = QLabel(categoriesRoot)
        self.categoriesTitle.setObjectName(u"categoriesTitle")

        self.catHeader.addWidget(self.categoriesTitle)

        self.catHeaderSpacer = QSpacerItem(40, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.catHeader.addItem(self.catHeaderSpacer)

        self.prevCatBtn = QCustomQPushButton(categoriesRoot)
        self.prevCatBtn.setObjectName(u"prevCatBtn")
        self.prevCatBtn.setMinimumSize(QSize(34, 34))
        self.prevCatBtn.setMaximumSize(QSize(34, 34))
        self.prevCatBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.prevCatBtn.setIconSize(QSize(16, 16))

        self.catHeader.addWidget(self.prevCatBtn)

        self.nextCatBtn = QCustomQPushButton(categoriesRoot)
        self.nextCatBtn.setObjectName(u"nextCatBtn")
        self.nextCatBtn.setMinimumSize(QSize(34, 34))
        self.nextCatBtn.setMaximumSize(QSize(34, 34))
        self.nextCatBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.nextCatBtn.setIconSize(QSize(16, 16))

        self.catHeader.addWidget(self.nextCatBtn)


        self.categoriesLayout.addLayout(self.catHeader)

        self.chipGroup = QCustomChipGroup(categoriesRoot)
        self.chipGroup.setObjectName(u"chipGroup")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chipGroup.sizePolicy().hasHeightForWidth())
        self.chipGroup.setSizePolicy(sizePolicy)
        self.chipGroup.setMinimumSize(QSize(0, 40))
        self.chipGroup.setProperty(u"selectable", True)
        self.chipGroup.setProperty(u"exclusive", True)

        self.categoriesLayout.addWidget(self.chipGroup)


        self.retranslateUi(categoriesRoot)

        QMetaObject.connectSlotsByName(categoriesRoot)
    # setupUi

    def retranslateUi(self, categoriesRoot):
        self.categoriesTitle.setText(QCoreApplication.translate("CategoriesRow", u"Select Categories", None))
        self.prevCatBtn.setText("")
        self.prevCatBtn.setProperty(u"iconName", QCoreApplication.translate("CategoriesRow", u"chevron-left", None))
        self.nextCatBtn.setText("")
        self.nextCatBtn.setProperty(u"iconName", QCoreApplication.translate("CategoriesRow", u"chevron-right", None))
        pass
    # retranslateUi

