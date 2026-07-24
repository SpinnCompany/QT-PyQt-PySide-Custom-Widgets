# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'new_ProfileComponent.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

from Custom_Widgets.QCustomActionButton import QCustomActionButton
from Custom_Widgets.QCustomAvatar import QCustomAvatar
from Custom_Widgets.QCustomComponent import QCustomComponent
from Custom_Widgets.QCustomComponentContainer import QCustomComponentContainer
from Custom_Widgets.QCustomThemeList import QCustomThemeList
class Ui_ProfileComponent(object):
    def setupUi(self, ProfileComponent):
        if not ProfileComponent.objectName():
            ProfileComponent.setObjectName(u"ProfileComponent")
        ProfileComponent.resize(304, 794)
        ProfileComponent.setMinimumSize(QSize(304, 0))
        ProfileComponent.setMaximumSize(QSize(304, 16777215))
        self.profileComponentOuter = QVBoxLayout(ProfileComponent)
        self.profileComponentOuter.setSpacing(0)
        self.profileComponentOuter.setObjectName(u"profileComponentOuter")
        self.profileComponentOuter.setContentsMargins(0, 0, 0, 0)
        self.profilePanel = QFrame(ProfileComponent)
        self.profilePanel.setObjectName(u"profilePanel")
        self.profilePanel.setFrameShape(QFrame.StyledPanel)
        self.profileLayout = QVBoxLayout(self.profilePanel)
        self.profileLayout.setSpacing(14)
        self.profileLayout.setObjectName(u"profileLayout")
        self.profileLayout.setContentsMargins(22, 18, 22, 18)
        self.profileCloseRow = QHBoxLayout()
        self.profileCloseRow.setObjectName(u"profileCloseRow")
        self.profileCloseSpacer = QSpacerItem(10, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.profileCloseRow.addItem(self.profileCloseSpacer)

        self.profileClose = QPushButton(self.profilePanel)
        self.profileClose.setObjectName(u"profileClose")
        self.profileClose.setMinimumSize(QSize(34, 34))
        self.profileClose.setMaximumSize(QSize(34, 34))
        self.profileClose.setIconSize(QSize(17, 17))
        self.profileClose.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.profileCloseRow.addWidget(self.profileClose)


        self.profileLayout.addLayout(self.profileCloseRow)

        self.profileAvatar = QCustomAvatar(self.profilePanel)
        self.profileAvatar.setObjectName(u"profileAvatar")
        self.profileAvatar.setMinimumSize(QSize(112, 112))
        self.profileAvatar.setMaximumSize(QSize(112, 112))
        self.profileAvatar.setProperty(u"showStatus", False)

        self.profileLayout.addWidget(self.profileAvatar)

        self.profileNameRow = QHBoxLayout()
        self.profileNameRow.setSpacing(6)
        self.profileNameRow.setObjectName(u"profileNameRow")
        self.pnLeft = QSpacerItem(10, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.profileNameRow.addItem(self.pnLeft)

        self.profileName = QLabel(self.profilePanel)
        self.profileName.setObjectName(u"profileName")

        self.profileNameRow.addWidget(self.profileName)

        self.profileVerified = QLabel(self.profilePanel)
        self.profileVerified.setObjectName(u"profileVerified")
        self.profileVerified.setMinimumSize(QSize(20, 20))
        self.profileVerified.setMaximumSize(QSize(20, 20))
        self.profileVerified.setScaledContents(True)

        self.profileNameRow.addWidget(self.profileVerified)

        self.pnRight = QSpacerItem(10, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.profileNameRow.addItem(self.pnRight)


        self.profileLayout.addLayout(self.profileNameRow)

        self.profileStatus = QLabel(self.profilePanel)
        self.profileStatus.setObjectName(u"profileStatus")
        self.profileStatus.setAlignment(Qt.AlignHCenter|Qt.AlignVCenter)

        self.profileLayout.addWidget(self.profileStatus)

        self.profileActionsRow = QHBoxLayout()
        self.profileActionsRow.setSpacing(10)
        self.profileActionsRow.setObjectName(u"profileActionsRow")
        self.actProfile = QCustomActionButton(self.profilePanel)
        self.actProfile.setObjectName(u"actProfile")

        self.profileActionsRow.addWidget(self.actProfile)

        self.actMute = QCustomActionButton(self.profilePanel)
        self.actMute.setObjectName(u"actMute")

        self.profileActionsRow.addWidget(self.actMute)

        self.actSearch = QCustomActionButton(self.profilePanel)
        self.actSearch.setObjectName(u"actSearch")

        self.profileActionsRow.addWidget(self.actSearch)


        self.profileLayout.addLayout(self.profileActionsRow)

        self.customizeHeader = QFrame(self.profilePanel)
        self.customizeHeader.setObjectName(u"customizeHeader")
        self.customizeHeader.setMinimumSize(QSize(0, 44))
        self.customizeHeader.setFrameShape(QFrame.StyledPanel)
        self.customizeHeader.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.customizeRow = QHBoxLayout(self.customizeHeader)
        self.customizeRow.setObjectName(u"customizeRow")
        self.customizeRow.setContentsMargins(4, -1, 4, -1)
        self.customizeTitle = QLabel(self.customizeHeader)
        self.customizeTitle.setObjectName(u"customizeTitle")

        self.customizeRow.addWidget(self.customizeTitle)

        self.customizeSpacer = QSpacerItem(10, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.customizeRow.addItem(self.customizeSpacer)

        self.customizeChevron = QPushButton(self.customizeHeader)
        self.customizeChevron.setObjectName(u"customizeChevron")
        self.customizeChevron.setMinimumSize(QSize(26, 26))
        self.customizeChevron.setMaximumSize(QSize(26, 26))
        self.customizeChevron.setIconSize(QSize(16, 16))

        self.customizeRow.addWidget(self.customizeChevron)


        self.profileLayout.addWidget(self.customizeHeader)

        self.themeList = QCustomThemeList(self.profilePanel)
        self.themeList.setObjectName(u"themeList")
        self.themeList.setMinimumSize(QSize(0, 36))

        self.profileLayout.addWidget(self.themeList)

        self.mediaContainer = QCustomComponentContainer(self.profilePanel)
        self.mediaContainer.setObjectName(u"mediaContainer")
        self.mediaContainer.setProperty(u"previewComponent", False)

        self.profileLayout.addWidget(self.mediaContainer)

        self.profileSpacer = QSpacerItem(10, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.profileLayout.addItem(self.profileSpacer)

        self.privacyHeader = QFrame(self.profilePanel)
        self.privacyHeader.setObjectName(u"privacyHeader")
        self.privacyHeader.setMinimumSize(QSize(0, 44))
        self.privacyHeader.setFrameShape(QFrame.StyledPanel)
        self.privacyHeader.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.privacyRow = QHBoxLayout(self.privacyHeader)
        self.privacyRow.setObjectName(u"privacyRow")
        self.privacyRow.setContentsMargins(4, -1, 4, -1)
        self.privacyTitle = QLabel(self.privacyHeader)
        self.privacyTitle.setObjectName(u"privacyTitle")

        self.privacyRow.addWidget(self.privacyTitle)

        self.privacySpacer = QSpacerItem(10, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.privacyRow.addItem(self.privacySpacer)

        self.privacyChevron = QPushButton(self.privacyHeader)
        self.privacyChevron.setObjectName(u"privacyChevron")
        self.privacyChevron.setMinimumSize(QSize(26, 26))
        self.privacyChevron.setMaximumSize(QSize(26, 26))
        self.privacyChevron.setIconSize(QSize(16, 16))

        self.privacyRow.addWidget(self.privacyChevron)


        self.profileLayout.addWidget(self.privacyHeader)


        self.profileComponentOuter.addWidget(self.profilePanel)


        self.retranslateUi(ProfileComponent)

        QMetaObject.connectSlotsByName(ProfileComponent)
    # setupUi

    def retranslateUi(self, ProfileComponent):
        self.profileClose.setProperty(u"role", QCoreApplication.translate("ProfileComponent", u"iconChip", None))
        self.profileAvatar.setProperty(u"text", QCoreApplication.translate("ProfileComponent", u"R", None))
        self.profileName.setText(QCoreApplication.translate("ProfileComponent", u"Ricky Smith", None))
        self.profileName.setProperty(u"role", QCoreApplication.translate("ProfileComponent", u"profileName", None))
        self.profileStatus.setText(QCoreApplication.translate("ProfileComponent", u"Online", None))
        self.profileStatus.setProperty(u"role", QCoreApplication.translate("ProfileComponent", u"profileStatus", None))
        self.actProfile.setProperty(u"caption", QCoreApplication.translate("ProfileComponent", u"Profile", None))
        self.actMute.setProperty(u"caption", QCoreApplication.translate("ProfileComponent", u"Mute", None))
        self.actSearch.setProperty(u"caption", QCoreApplication.translate("ProfileComponent", u"Search", None))
        self.customizeHeader.setProperty(u"role", QCoreApplication.translate("ProfileComponent", u"accordionHeader", None))
        self.customizeTitle.setText(QCoreApplication.translate("ProfileComponent", u"Customize Chat", None))
        self.customizeTitle.setProperty(u"role", QCoreApplication.translate("ProfileComponent", u"accordionTitle", None))
        self.customizeChevron.setProperty(u"role", QCoreApplication.translate("ProfileComponent", u"chevron", None))
        self.mediaContainer.setProperty(u"filePath", QCoreApplication.translate("ProfileComponent", u"ui/MediaPanelComponent.ui", None))
        self.privacyHeader.setProperty(u"role", QCoreApplication.translate("ProfileComponent", u"accordionHeader", None))
        self.privacyTitle.setText(QCoreApplication.translate("ProfileComponent", u"Privacy and Support", None))
        self.privacyTitle.setProperty(u"role", QCoreApplication.translate("ProfileComponent", u"accordionTitle", None))
        self.privacyChevron.setProperty(u"role", QCoreApplication.translate("ProfileComponent", u"chevron", None))
        pass
    # retranslateUi

