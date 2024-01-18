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
    QWidget)

class Ui_SettingsWidgetContainer(object):
    def setupUi(self, SettingsWidgetContainer):
        if not SettingsWidgetContainer.objectName():
            SettingsWidgetContainer.setObjectName(u"SettingsWidgetContainer")
        SettingsWidgetContainer.resize(417, 141)
        self.horizontalLayout = QHBoxLayout(SettingsWidgetContainer)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.setting_label = QLabel(SettingsWidgetContainer)
        self.setting_label.setObjectName(u"setting_label")
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.setting_label.sizePolicy().hasHeightForWidth())
        self.setting_label.setSizePolicy(sizePolicy)
        self.setting_label.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.setting_label)

        self.settings_widget = QWidget(SettingsWidgetContainer)
        self.settings_widget.setObjectName(u"settings_widget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(3)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.settings_widget.sizePolicy().hasHeightForWidth())
        self.settings_widget.setSizePolicy(sizePolicy1)

        self.horizontalLayout.addWidget(self.settings_widget)

        self.setting_description = QLabel(SettingsWidgetContainer)
        self.setting_description.setObjectName(u"setting_description")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(2)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.setting_description.sizePolicy().hasHeightForWidth())
        self.setting_description.setSizePolicy(sizePolicy2)
        self.setting_description.setWordWrap(True)

        self.horizontalLayout.addWidget(self.setting_description)


        self.retranslateUi(SettingsWidgetContainer)

        QMetaObject.connectSlotsByName(SettingsWidgetContainer)
    # setupUi

    def retranslateUi(self, SettingsWidgetContainer):
        SettingsWidgetContainer.setWindowTitle(QCoreApplication.translate("SettingsWidgetContainer", u"SettingsWidgetContainer", None))
        self.setting_label.setText(QCoreApplication.translate("SettingsWidgetContainer", u"Label", None))
        self.setting_description.setText(QCoreApplication.translate("SettingsWidgetContainer", u"Description", None))
    # retranslateUi

