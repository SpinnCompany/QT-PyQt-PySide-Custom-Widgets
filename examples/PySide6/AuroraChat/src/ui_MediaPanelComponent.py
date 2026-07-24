# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'new_MediaPanelComponent.ui'
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
from PySide6.QtWidgets import (QApplication, QLabel, QPushButton, QSizePolicy,
    QSpacerItem, QStackedWidget, QVBoxLayout, QWidget)

from Custom_Widgets.QCustomComponent import QCustomComponent
from Custom_Widgets.QCustomFileCard import QCustomFileCard
from Custom_Widgets.QCustomLinkPreview import QCustomLinkPreview
from Custom_Widgets.QCustomMediaGrid import QCustomMediaGrid
from Custom_Widgets.QCustomSegmentedControl import QCustomSegmentedControl
class Ui_MediaPanelComponent(object):
    def setupUi(self, MediaPanelComponent):
        if not MediaPanelComponent.objectName():
            MediaPanelComponent.setObjectName(u"MediaPanelComponent")
        MediaPanelComponent.resize(304, 420)
        self.mediaPanelLayout = QVBoxLayout(MediaPanelComponent)
        self.mediaPanelLayout.setSpacing(12)
        self.mediaPanelLayout.setObjectName(u"mediaPanelLayout")
        self.mediaPanelLayout.setContentsMargins(0, 0, 0, 0)
        self.mediaTitle = QLabel(MediaPanelComponent)
        self.mediaTitle.setObjectName(u"mediaTitle")

        self.mediaPanelLayout.addWidget(self.mediaTitle)

        self.mediaTabs = QCustomSegmentedControl(MediaPanelComponent)
        self.mediaTabs.setObjectName(u"mediaTabs")
        self.mediaTabs.setMinimumSize(QSize(0, 36))
        self.mediaTabs.setProperty(u"currentSegment", 0)

        self.mediaPanelLayout.addWidget(self.mediaTabs)

        self.mediaStack = QStackedWidget(MediaPanelComponent)
        self.mediaStack.setObjectName(u"mediaStack")
        self.mediaPage = QWidget()
        self.mediaPage.setObjectName(u"mediaPage")
        self.mediaPageLayout = QVBoxLayout(self.mediaPage)
        self.mediaPageLayout.setSpacing(0)
        self.mediaPageLayout.setObjectName(u"mediaPageLayout")
        self.mediaPageLayout.setContentsMargins(0, 0, 0, 0)
        self.mediaGrid = QCustomMediaGrid(self.mediaPage)
        self.mediaGrid.setObjectName(u"mediaGrid")
        self.mediaGrid.setMinimumSize(QSize(0, 200))
        self.mediaGrid.setProperty(u"columns", 3)
        self.mediaGrid.setProperty(u"tileHeight", 60)

        self.mediaPageLayout.addWidget(self.mediaGrid)

        self.mediaPageSpacer = QSpacerItem(10, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.mediaPageLayout.addItem(self.mediaPageSpacer)

        self.mediaStack.addWidget(self.mediaPage)
        self.filesPage = QWidget()
        self.filesPage.setObjectName(u"filesPage")
        self.filesList = QVBoxLayout(self.filesPage)
        self.filesList.setSpacing(8)
        self.filesList.setObjectName(u"filesList")
        self.filesList.setContentsMargins(0, 0, 0, 0)
        self.file1 = QCustomFileCard(self.filesPage)
        self.file1.setObjectName(u"file1")

        self.filesList.addWidget(self.file1)

        self.file2 = QCustomFileCard(self.filesPage)
        self.file2.setObjectName(u"file2")

        self.filesList.addWidget(self.file2)

        self.file3 = QCustomFileCard(self.filesPage)
        self.file3.setObjectName(u"file3")

        self.filesList.addWidget(self.file3)

        self.file4 = QCustomFileCard(self.filesPage)
        self.file4.setObjectName(u"file4")

        self.filesList.addWidget(self.file4)

        self.filesSpacer = QSpacerItem(10, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.filesList.addItem(self.filesSpacer)

        self.mediaStack.addWidget(self.filesPage)
        self.linksPage = QWidget()
        self.linksPage.setObjectName(u"linksPage")
        self.linksList = QVBoxLayout(self.linksPage)
        self.linksList.setSpacing(8)
        self.linksList.setObjectName(u"linksList")
        self.linksList.setContentsMargins(0, 0, 0, 0)
        self.link1 = QCustomLinkPreview(self.linksPage)
        self.link1.setObjectName(u"link1")

        self.linksList.addWidget(self.link1)

        self.link2 = QCustomLinkPreview(self.linksPage)
        self.link2.setObjectName(u"link2")

        self.linksList.addWidget(self.link2)

        self.link3 = QCustomLinkPreview(self.linksPage)
        self.link3.setObjectName(u"link3")

        self.linksList.addWidget(self.link3)

        self.linksSpacer = QSpacerItem(10, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.linksList.addItem(self.linksSpacer)

        self.mediaStack.addWidget(self.linksPage)

        self.mediaPanelLayout.addWidget(self.mediaStack)


        self.retranslateUi(MediaPanelComponent)

        self.mediaStack.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MediaPanelComponent)
    # setupUi

    def retranslateUi(self, MediaPanelComponent):
        self.mediaTitle.setText(QCoreApplication.translate("MediaPanelComponent", u"Media, Files And Links", None))
        self.mediaTitle.setProperty(u"role", QCoreApplication.translate("MediaPanelComponent", u"accordionTitle", None))
        self.mediaTabs.setProperty(u"segments", QCoreApplication.translate("MediaPanelComponent", u"Media,Files,Links", None))
        self.file1.setProperty(u"fileName", QCoreApplication.translate("MediaPanelComponent", u"Project Brief.pdf", None))
        self.file1.setProperty(u"fileSize", QCoreApplication.translate("MediaPanelComponent", u"2.4 MB  \u00b7  Jul 21", None))
        self.file2.setProperty(u"fileName", QCoreApplication.translate("MediaPanelComponent", u"Budget Q3.xlsx", None))
        self.file2.setProperty(u"fileSize", QCoreApplication.translate("MediaPanelComponent", u"845 KB  \u00b7  Jul 19", None))
        self.file3.setProperty(u"fileName", QCoreApplication.translate("MediaPanelComponent", u"Mockups.zip", None))
        self.file3.setProperty(u"fileSize", QCoreApplication.translate("MediaPanelComponent", u"18.2 MB  \u00b7  Jul 15", None))
        self.file4.setProperty(u"fileName", QCoreApplication.translate("MediaPanelComponent", u"Meeting Notes.txt", None))
        self.file4.setProperty(u"fileSize", QCoreApplication.translate("MediaPanelComponent", u"4 KB  \u00b7  Jul 12", None))
        self.link1.setProperty(u"title", QCoreApplication.translate("MediaPanelComponent", u"Aurora Design System", None))
        self.link1.setProperty(u"url", QCoreApplication.translate("MediaPanelComponent", u"https://dribbble.com/aurora", None))
        self.link1.setProperty(u"description", QCoreApplication.translate("MediaPanelComponent", u"Modern UI kit for chat apps", None))
        self.link2.setProperty(u"title", QCoreApplication.translate("MediaPanelComponent", u"Feather Icons", None))
        self.link2.setProperty(u"url", QCoreApplication.translate("MediaPanelComponent", u"https://feathericons.com", None))
        self.link3.setProperty(u"title", QCoreApplication.translate("MediaPanelComponent", u"Picsum Photos", None))
        self.link3.setProperty(u"url", QCoreApplication.translate("MediaPanelComponent", u"https://picsum.photos", None))
        self.link3.setProperty(u"description", QCoreApplication.translate("MediaPanelComponent", u"Lorem Ipsum for photos", None))
        pass
    # retranslateUi

