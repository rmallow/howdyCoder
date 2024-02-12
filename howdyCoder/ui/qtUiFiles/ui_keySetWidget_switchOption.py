# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'keySetWidget_switchOption.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_KeySetWidget(object):
    def setupUi(self, KeySetWidget):
        if not KeySetWidget.objectName():
            KeySetWidget.setObjectName(u"KeySetWidget")
        KeySetWidget.resize(673, 440)
        self.verticalLayout = QVBoxLayout(KeySetWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
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

        self.key_choice_combo = QComboBox(KeySetWidget)
        self.key_choice_combo.setObjectName(u"key_choice_combo")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(1)
        sizePolicy2.setHeightForWidth(self.key_choice_combo.sizePolicy().hasHeightForWidth())
        self.key_choice_combo.setSizePolicy(sizePolicy2)

        self.verticalLayout.addWidget(self.key_choice_combo)

        self.label = QLabel(KeySetWidget)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setWordWrap(True)

        self.verticalLayout.addWidget(self.label)

        self.widget_3 = QWidget(KeySetWidget)
        self.widget_3.setObjectName(u"widget_3")
        self.widget_3.setMinimumSize(QSize(0, 50))
        self.horizontalLayout_5 = QHBoxLayout(self.widget_3)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_4 = QLabel(self.widget_3)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_5.addWidget(self.label_4)

        self.toggle_switch_box = QWidget(self.widget_3)
        self.toggle_switch_box.setObjectName(u"toggle_switch_box")
        self.toggle_switch_box.setMinimumSize(QSize(0, 50))

        self.horizontalLayout_5.addWidget(self.toggle_switch_box)

        self.label_5 = QLabel(self.widget_3)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_5.addWidget(self.label_5)


        self.verticalLayout.addWidget(self.widget_3)

        self.api_box = QWidget(KeySetWidget)
        self.api_box.setObjectName(u"api_box")
        self.horizontalLayout = QHBoxLayout(self.api_box)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.api_key_edit = QLineEdit(self.api_box)
        self.api_key_edit.setObjectName(u"api_key_edit")
        sizePolicy3 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(1)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.api_key_edit.sizePolicy().hasHeightForWidth())
        self.api_key_edit.setSizePolicy(sizePolicy3)
        self.api_key_edit.setMinimumSize(QSize(200, 0))

        self.horizontalLayout.addWidget(self.api_key_edit)

        self.horizontalSpacer = QSpacerItem(80, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.key_select_combo = QComboBox(self.api_box)
        self.key_select_combo.setObjectName(u"key_select_combo")
        sizePolicy4 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy4.setHorizontalStretch(1)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.key_select_combo.sizePolicy().hasHeightForWidth())
        self.key_select_combo.setSizePolicy(sizePolicy4)
        self.key_select_combo.setMinimumSize(QSize(200, 0))

        self.horizontalLayout.addWidget(self.key_select_combo)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_3)


        self.verticalLayout.addWidget(self.api_box)

        self.status_box = QWidget(KeySetWidget)
        self.status_box.setObjectName(u"status_box")
        sizePolicy.setHeightForWidth(self.status_box.sizePolicy().hasHeightForWidth())
        self.status_box.setSizePolicy(sizePolicy)
        self.horizontalLayout_2 = QHBoxLayout(self.status_box)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.status_icon_label = QLabel(self.status_box)
        self.status_icon_label.setObjectName(u"status_icon_label")
        sizePolicy5 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.status_icon_label.sizePolicy().hasHeightForWidth())
        self.status_icon_label.setSizePolicy(sizePolicy5)
        self.status_icon_label.setMinimumSize(QSize(16, 16))
        self.status_icon_label.setMaximumSize(QSize(16, 16))

        self.horizontalLayout_2.addWidget(self.status_icon_label)

        self.status_text_label = QLabel(self.status_box)
        self.status_text_label.setObjectName(u"status_text_label")
        sizePolicy.setHeightForWidth(self.status_text_label.sizePolicy().hasHeightForWidth())
        self.status_text_label.setSizePolicy(sizePolicy)

        self.horizontalLayout_2.addWidget(self.status_text_label)


        self.verticalLayout.addWidget(self.status_box)

        self.widget = QWidget(KeySetWidget)
        self.widget.setObjectName(u"widget")
        self.widget.setMinimumSize(QSize(0, 50))
        self.horizontalLayout_3 = QHBoxLayout(self.widget)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(12, 12, 12, 12)
        self.set_button = QPushButton(self.widget)
        self.set_button.setObjectName(u"set_button")

        self.horizontalLayout_3.addWidget(self.set_button)


        self.verticalLayout.addWidget(self.widget)


        self.retranslateUi(KeySetWidget)

        QMetaObject.connectSlotsByName(KeySetWidget)
    # setupUi

    def retranslateUi(self, KeySetWidget):
        KeySetWidget.setWindowTitle(QCoreApplication.translate("KeySetWidget", u"API Key Set Widget", None))
        self.label_2.setText(QCoreApplication.translate("KeySetWidget", u"For more information on keys, look at the User Manual ->", None))
        self.user_manual_button.setText(QCoreApplication.translate("KeySetWidget", u"User Manual", None))
        self.label.setText(QCoreApplication.translate("KeySetWidget", u"Enter or select a key you've already set in the space below. Once set, this key will be retreived each time the application is loaded.", None))
        self.label_4.setText(QCoreApplication.translate("KeySetWidget", u"Set", None))
        self.label_5.setText(QCoreApplication.translate("KeySetWidget", u"Select", None))
        self.status_icon_label.setText("")
        self.status_text_label.setText("")
        self.set_button.setText(QCoreApplication.translate("KeySetWidget", u"Set", None))
    # retranslateUi

