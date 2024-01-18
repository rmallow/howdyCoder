# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'settingsWidgetFrequency.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QDateTimeEdit, QHBoxLayout,
    QLabel, QSizePolicy, QTimeEdit, QWidget)

class Ui_SettingsWidgetFrequency(object):
    def setupUi(self, SettingsWidgetFrequency):
        if not SettingsWidgetFrequency.objectName():
            SettingsWidgetFrequency.setObjectName(u"SettingsWidgetFrequency")
        SettingsWidgetFrequency.resize(370, 45)
        self.horizontalLayout = QHBoxLayout(SettingsWidgetFrequency)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_3 = QLabel(SettingsWidgetFrequency)
        self.label_3.setObjectName(u"label_3")
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.label_3)

        self.time_edit = QTimeEdit(SettingsWidgetFrequency)
        self.time_edit.setObjectName(u"time_edit")
        self.time_edit.setAlignment(Qt.AlignCenter)
        self.time_edit.setDate(QDate(2000, 1, 1))
        self.time_edit.setMinimumTime(QTime(0, 0, 1))
        self.time_edit.setCurrentSection(QDateTimeEdit.HourSection)
        self.time_edit.setCurrentSectionIndex(0)
        self.time_edit.setTime(QTime(0, 0, 1))

        self.horizontalLayout.addWidget(self.time_edit)

        self.single_shot_check = QCheckBox(SettingsWidgetFrequency)
        self.single_shot_check.setObjectName(u"single_shot_check")
        self.single_shot_check.setLayoutDirection(Qt.RightToLeft)

        self.horizontalLayout.addWidget(self.single_shot_check)


        self.retranslateUi(SettingsWidgetFrequency)

        QMetaObject.connectSlotsByName(SettingsWidgetFrequency)
    # setupUi

    def retranslateUi(self, SettingsWidgetFrequency):
        SettingsWidgetFrequency.setWindowTitle(QCoreApplication.translate("SettingsWidgetFrequency", u"SettingsWidgetFrequency", None))
        self.label_3.setText(QCoreApplication.translate("SettingsWidgetFrequency", u"Period (hh:mm:ss)", None))
        self.time_edit.setDisplayFormat(QCoreApplication.translate("SettingsWidgetFrequency", u"hh:mm:ss", None))
        self.single_shot_check.setText(QCoreApplication.translate("SettingsWidgetFrequency", u"Single Shot", None))
    # retranslateUi

