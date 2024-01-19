# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'settingsWidgetContainer.ui'
##
## Created by: Qt User Interface Compiler version 6.5.2
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QSizePolicy,
    QSpacerItem, QWidget)

class Ui_SettingsWidgetContainer(object):
    def setupUi(self, SettingsWidgetContainer):
        if not SettingsWidgetContainer.objectName():
            SettingsWidgetContainer.setObjectName(u"SettingsWidgetContainer")
        SettingsWidgetContainer.resize(417, 141)
        self.horizontalLayout = QHBoxLayout(SettingsWidgetContainer)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(60, 20, QSizePolicy.Maximum, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.box = QWidget(SettingsWidgetContainer)
        self.box.setObjectName(u"box")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.box.sizePolicy().hasHeightForWidth())
        self.box.setSizePolicy(sizePolicy)
        self.horizontalLayout_2 = QHBoxLayout(self.box)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.setting_label = QLabel(self.box)
        self.setting_label.setObjectName(u"setting_label")
        sizePolicy1 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(1)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.setting_label.sizePolicy().hasHeightForWidth())
        self.setting_label.setSizePolicy(sizePolicy1)
        self.setting_label.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_2.addWidget(self.setting_label)

        self.settings_widget = QWidget(self.box)
        self.settings_widget.setObjectName(u"settings_widget")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(3)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.settings_widget.sizePolicy().hasHeightForWidth())
        self.settings_widget.setSizePolicy(sizePolicy2)

        self.horizontalLayout_2.addWidget(self.settings_widget)

        self.setting_description = QLabel(self.box)
        self.setting_description.setObjectName(u"setting_description")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(2)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.setting_description.sizePolicy().hasHeightForWidth())
        self.setting_description.setSizePolicy(sizePolicy3)
        self.setting_description.setWordWrap(True)

        self.horizontalLayout_2.addWidget(self.setting_description)


        self.horizontalLayout.addWidget(self.box)

        self.horizontalSpacer_2 = QSpacerItem(60, 20, QSizePolicy.Maximum, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)


        self.retranslateUi(SettingsWidgetContainer)

        QMetaObject.connectSlotsByName(SettingsWidgetContainer)
    # setupUi

    def retranslateUi(self, SettingsWidgetContainer):
        SettingsWidgetContainer.setWindowTitle(QCoreApplication.translate("SettingsWidgetContainer", u"SettingsWidgetContainer", None))
        self.setting_label.setText(QCoreApplication.translate("SettingsWidgetContainer", u"Label", None))
        self.setting_description.setText(QCoreApplication.translate("SettingsWidgetContainer", u"Description", None))
    # retranslateUi

