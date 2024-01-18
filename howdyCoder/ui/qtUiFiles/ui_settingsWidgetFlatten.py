# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'settingsWidgetFlatten.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QHBoxLayout, QSizePolicy,
    QWidget)

class Ui_SettingsWidgetFlatten(object):
    def setupUi(self, SettingsWidgetFlatten):
        if not SettingsWidgetFlatten.objectName():
            SettingsWidgetFlatten.setObjectName(u"SettingsWidgetFlatten")
        SettingsWidgetFlatten.resize(398, 68)
        self.horizontalLayout = QHBoxLayout(SettingsWidgetFlatten)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.widget_4 = QWidget(SettingsWidgetFlatten)
        self.widget_4.setObjectName(u"widget_4")
        self.widget_4.setLayoutDirection(Qt.LeftToRight)
        self.horizontalLayout_2 = QHBoxLayout(self.widget_4)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(12, -1, -1, -1)
        self.flattened_check = QCheckBox(self.widget_4)
        self.flattened_check.setObjectName(u"flattened_check")
        font = QFont()
        font.setPointSize(15)
        self.flattened_check.setFont(font)
        self.flattened_check.setChecked(True)

        self.horizontalLayout_2.addWidget(self.flattened_check)


        self.horizontalLayout.addWidget(self.widget_4)


        self.retranslateUi(SettingsWidgetFlatten)

        QMetaObject.connectSlotsByName(SettingsWidgetFlatten)
    # setupUi

    def retranslateUi(self, SettingsWidgetFlatten):
        SettingsWidgetFlatten.setWindowTitle(QCoreApplication.translate("SettingsWidgetFlatten", u"SettingsWidgetFlatten", None))
        self.flattened_check.setText("")
    # retranslateUi

