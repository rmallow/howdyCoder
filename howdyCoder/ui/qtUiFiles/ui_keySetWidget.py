# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'keySetWidget.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_KeySetWidget(object):
    def setupUi(self, KeySetWidget):
        if not KeySetWidget.objectName():
            KeySetWidget.setObjectName(u"KeySetWidget")
        KeySetWidget.resize(763, 745)
        self.verticalLayout = QVBoxLayout(KeySetWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.api_box = QWidget(KeySetWidget)
        self.api_box.setObjectName(u"api_box")
        self.horizontalLayout = QHBoxLayout(self.api_box)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.api_label = QLabel(self.api_box)
        self.api_label.setObjectName(u"api_label")

        self.horizontalLayout.addWidget(self.api_label)

        self.api_key_edit = QLineEdit(self.api_box)
        self.api_key_edit.setObjectName(u"api_key_edit")
        self.api_key_edit.setMinimumSize(QSize(200, 0))

        self.horizontalLayout.addWidget(self.api_key_edit)

        self.api_key_button = QPushButton(self.api_box)
        self.api_key_button.setObjectName(u"api_key_button")

        self.horizontalLayout.addWidget(self.api_key_button)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout.addWidget(self.api_box)

        self.status_box = QWidget(KeySetWidget)
        self.status_box.setObjectName(u"status_box")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.status_box.sizePolicy().hasHeightForWidth())
        self.status_box.setSizePolicy(sizePolicy)
        self.horizontalLayout_2 = QHBoxLayout(self.status_box)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.status_icon_label = QLabel(self.status_box)
        self.status_icon_label.setObjectName(u"status_icon_label")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.status_icon_label.sizePolicy().hasHeightForWidth())
        self.status_icon_label.setSizePolicy(sizePolicy1)
        self.status_icon_label.setMinimumSize(QSize(16, 16))
        self.status_icon_label.setMaximumSize(QSize(16, 16))

        self.horizontalLayout_2.addWidget(self.status_icon_label)

        self.status_text_label = QLabel(self.status_box)
        self.status_text_label.setObjectName(u"status_text_label")
        sizePolicy.setHeightForWidth(self.status_text_label.sizePolicy().hasHeightForWidth())
        self.status_text_label.setSizePolicy(sizePolicy)

        self.horizontalLayout_2.addWidget(self.status_text_label)


        self.verticalLayout.addWidget(self.status_box)


        self.retranslateUi(KeySetWidget)

        QMetaObject.connectSlotsByName(KeySetWidget)
    # setupUi

    def retranslateUi(self, KeySetWidget):
        KeySetWidget.setWindowTitle(QCoreApplication.translate("KeySetWidget", u"API Key Set Widget", None))
        self.api_label.setText(QCoreApplication.translate("KeySetWidget", u"Enter your API Key here:", None))
        self.api_key_button.setText(QCoreApplication.translate("KeySetWidget", u"Set", None))
        self.status_icon_label.setText("")
        self.status_text_label.setText("")
    # retranslateUi

