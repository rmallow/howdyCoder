# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'createSettingsBasePage.ui'
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
from PySide6.QtWidgets import (QApplication, QLabel, QSizePolicy, QVBoxLayout,
    QWidget)

class Ui_CreateSettingsBasePage(object):
    def setupUi(self, CreateSettingsBasePage):
        if not CreateSettingsBasePage.objectName():
            CreateSettingsBasePage.setObjectName(u"CreateSettingsBasePage")
        CreateSettingsBasePage.resize(400, 300)
        self.verticalLayout = QVBoxLayout(CreateSettingsBasePage)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(CreateSettingsBasePage)
        self.label.setObjectName(u"label")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        font = QFont()
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label)

        self.settings_list = QWidget(CreateSettingsBasePage)
        self.settings_list.setObjectName(u"settings_list")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(10)
        sizePolicy1.setHeightForWidth(self.settings_list.sizePolicy().hasHeightForWidth())
        self.settings_list.setSizePolicy(sizePolicy1)

        self.verticalLayout.addWidget(self.settings_list)


        self.retranslateUi(CreateSettingsBasePage)

        QMetaObject.connectSlotsByName(CreateSettingsBasePage)
    # setupUi

    def retranslateUi(self, CreateSettingsBasePage):
        CreateSettingsBasePage.setWindowTitle(QCoreApplication.translate("CreateSettingsBasePage", u"CreateSettingsBasePage", None))
        self.label.setText(QCoreApplication.translate("CreateSettingsBasePage", u"Settings", None))
    # retranslateUi

