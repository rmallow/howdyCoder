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
    QPushButton, QSizePolicy, QVBoxLayout, QWidget)

class Ui_KeySetWidget(object):
    def setupUi(self, KeySetWidget):
        if not KeySetWidget.objectName():
            KeySetWidget.setObjectName(u"KeySetWidget")
        KeySetWidget.resize(768, 296)
        self.verticalLayout = QVBoxLayout(KeySetWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(6, 6, 6, 6)
        self.label = QLabel(KeySetWidget)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.widget_2 = QWidget(KeySetWidget)
        self.widget_2.setObjectName(u"widget_2")
        self.horizontalLayout_4 = QHBoxLayout(self.widget_2)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_2 = QLabel(self.widget_2)
        self.label_2.setObjectName(u"label_2")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setAlignment(Qt.AlignCenter)
        self.label_2.setWordWrap(True)

        self.horizontalLayout_4.addWidget(self.label_2)

        self.user_manual_button = QPushButton(self.widget_2)
        self.user_manual_button.setObjectName(u"user_manual_button")
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(1)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.user_manual_button.sizePolicy().hasHeightForWidth())
        self.user_manual_button.setSizePolicy(sizePolicy1)

        self.horizontalLayout_4.addWidget(self.user_manual_button)


        self.verticalLayout.addWidget(self.widget_2)

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


        self.verticalLayout.addWidget(self.api_box)

        self.widget = QWidget(KeySetWidget)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout_3 = QHBoxLayout(self.widget)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.set_button = QPushButton(self.widget)
        self.set_button.setObjectName(u"set_button")

        self.horizontalLayout_3.addWidget(self.set_button)

        self.store_button = QPushButton(self.widget)
        self.store_button.setObjectName(u"store_button")

        self.horizontalLayout_3.addWidget(self.store_button)

        self.retrieve_button = QPushButton(self.widget)
        self.retrieve_button.setObjectName(u"retrieve_button")

        self.horizontalLayout_3.addWidget(self.retrieve_button)

        self.always_retrieve_button = QPushButton(self.widget)
        self.always_retrieve_button.setObjectName(u"always_retrieve_button")

        self.horizontalLayout_3.addWidget(self.always_retrieve_button)


        self.verticalLayout.addWidget(self.widget)

        self.status_box = QWidget(KeySetWidget)
        self.status_box.setObjectName(u"status_box")
        sizePolicy.setHeightForWidth(self.status_box.sizePolicy().hasHeightForWidth())
        self.status_box.setSizePolicy(sizePolicy)
        self.horizontalLayout_2 = QHBoxLayout(self.status_box)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.status_icon_label = QLabel(self.status_box)
        self.status_icon_label.setObjectName(u"status_icon_label")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.status_icon_label.sizePolicy().hasHeightForWidth())
        self.status_icon_label.setSizePolicy(sizePolicy2)
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
        self.label.setText(QCoreApplication.translate("KeySetWidget", u"Enter the API Key in the space below. \n"
" Hit Set to save that key for the current instance. \n"
" Hit Store to hold the key in a secure location to be retrieved later. \n"
" Hit Retrieve to set the current stored key. \n"
" Hit Always Retrieve to always retrieve the key on startup of the application.", None))
        self.label_2.setText(QCoreApplication.translate("KeySetWidget", u"For information on where to get API Keys, look at the User Manual ->", None))
        self.user_manual_button.setText(QCoreApplication.translate("KeySetWidget", u"User Manual", None))
        self.api_label.setText(QCoreApplication.translate("KeySetWidget", u"Enter your API Key here:", None))
        self.set_button.setText(QCoreApplication.translate("KeySetWidget", u"Set", None))
        self.store_button.setText(QCoreApplication.translate("KeySetWidget", u"Set and Store", None))
        self.retrieve_button.setText(QCoreApplication.translate("KeySetWidget", u"Retrieve", None))
        self.always_retrieve_button.setText(QCoreApplication.translate("KeySetWidget", u"Always Retrieve", None))
        self.status_icon_label.setText("")
        self.status_text_label.setText("")
    # retranslateUi

