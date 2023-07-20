# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'algoStatusWidget.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_AlgoStatusWidget(object):
    def setupUi(self, AlgoStatusWidget):
        if not AlgoStatusWidget.objectName():
            AlgoStatusWidget.setObjectName(u"AlgoStatusWidget")
        AlgoStatusWidget.resize(520, 209)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(AlgoStatusWidget.sizePolicy().hasHeightForWidth())
        AlgoStatusWidget.setSizePolicy(sizePolicy)
        AlgoStatusWidget.setMaximumSize(QSize(520, 209))
        AlgoStatusWidget.setStyleSheet(u"")
        self.horizontalLayout_3 = QHBoxLayout(AlgoStatusWidget)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.widget_3 = QWidget(AlgoStatusWidget)
        self.widget_3.setObjectName(u"widget_3")
        self.verticalLayout_2 = QVBoxLayout(self.widget_3)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.name_label = QLabel(self.widget_3)
        self.name_label.setObjectName(u"name_label")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(1)
        sizePolicy1.setHeightForWidth(self.name_label.sizePolicy().hasHeightForWidth())
        self.name_label.setSizePolicy(sizePolicy1)
        font = QFont()
        font.setPointSize(20)
        self.name_label.setFont(font)
        self.name_label.setAlignment(Qt.AlignCenter)

        self.verticalLayout_2.addWidget(self.name_label)

        self.status_label = QLabel(self.widget_3)
        self.status_label.setObjectName(u"status_label")
        sizePolicy1.setHeightForWidth(self.status_label.sizePolicy().hasHeightForWidth())
        self.status_label.setSizePolicy(sizePolicy1)
        self.status_label.setAutoFillBackground(True)
        self.status_label.setStyleSheet(u"")
        self.status_label.setAlignment(Qt.AlignCenter)

        self.verticalLayout_2.addWidget(self.status_label)


        self.horizontalLayout_3.addWidget(self.widget_3)

        self.widget_2 = QWidget(AlgoStatusWidget)
        self.widget_2.setObjectName(u"widget_2")
        self.verticalLayout = QVBoxLayout(self.widget_2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.runtimeBox = QWidget(self.widget_2)
        self.runtimeBox.setObjectName(u"runtimeBox")
        sizePolicy1.setHeightForWidth(self.runtimeBox.sizePolicy().hasHeightForWidth())
        self.runtimeBox.setSizePolicy(sizePolicy1)
        self.horizontalLayout = QHBoxLayout(self.runtimeBox)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.runtime_label = QLabel(self.runtimeBox)
        self.runtime_label.setObjectName(u"runtime_label")

        self.horizontalLayout.addWidget(self.runtime_label)

        self.runtime_value = QLabel(self.runtimeBox)
        self.runtime_value.setObjectName(u"runtime_value")

        self.horizontalLayout.addWidget(self.runtime_value)


        self.verticalLayout.addWidget(self.runtimeBox)

        self.feedLengthBox = QWidget(self.widget_2)
        self.feedLengthBox.setObjectName(u"feedLengthBox")
        sizePolicy1.setHeightForWidth(self.feedLengthBox.sizePolicy().hasHeightForWidth())
        self.feedLengthBox.setSizePolicy(sizePolicy1)
        self.horizontalLayout_5 = QHBoxLayout(self.feedLengthBox)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.data_count_label = QLabel(self.feedLengthBox)
        self.data_count_label.setObjectName(u"data_count_label")
        sizePolicy.setHeightForWidth(self.data_count_label.sizePolicy().hasHeightForWidth())
        self.data_count_label.setSizePolicy(sizePolicy)

        self.horizontalLayout_5.addWidget(self.data_count_label)

        self.data_count_value = QLabel(self.feedLengthBox)
        self.data_count_value.setObjectName(u"data_count_value")

        self.horizontalLayout_5.addWidget(self.data_count_value)


        self.verticalLayout.addWidget(self.feedLengthBox)

        self.widget_4 = QWidget(self.widget_2)
        self.widget_4.setObjectName(u"widget_4")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(3)
        sizePolicy2.setHeightForWidth(self.widget_4.sizePolicy().hasHeightForWidth())
        self.widget_4.setSizePolicy(sizePolicy2)
        self.horizontalLayout_4 = QHBoxLayout(self.widget_4)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.start_button = QPushButton(self.widget_4)
        self.start_button.setObjectName(u"start_button")
        sizePolicy3 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.start_button.sizePolicy().hasHeightForWidth())
        self.start_button.setSizePolicy(sizePolicy3)
        self.start_button.setMinimumSize(QSize(110, 40))
        self.start_button.setMaximumSize(QSize(110, 40))

        self.horizontalLayout_4.addWidget(self.start_button)


        self.verticalLayout.addWidget(self.widget_4)

        self.widget_5 = QWidget(self.widget_2)
        self.widget_5.setObjectName(u"widget_5")
        sizePolicy4 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(2)
        sizePolicy4.setHeightForWidth(self.widget_5.sizePolicy().hasHeightForWidth())
        self.widget_5.setSizePolicy(sizePolicy4)
        self.horizontalLayout_2 = QHBoxLayout(self.widget_5)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.save_button = QPushButton(self.widget_5)
        self.save_button.setObjectName(u"save_button")
        sizePolicy5 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.save_button.sizePolicy().hasHeightForWidth())
        self.save_button.setSizePolicy(sizePolicy5)
        self.save_button.setMinimumSize(QSize(110, 40))
        self.save_button.setMaximumSize(QSize(110, 40))

        self.horizontalLayout_2.addWidget(self.save_button)

        self.remove_button = QPushButton(self.widget_5)
        self.remove_button.setObjectName(u"remove_button")
        sizePolicy5.setHeightForWidth(self.remove_button.sizePolicy().hasHeightForWidth())
        self.remove_button.setSizePolicy(sizePolicy5)
        self.remove_button.setMinimumSize(QSize(110, 40))
        self.remove_button.setMaximumSize(QSize(110, 40))

        self.horizontalLayout_2.addWidget(self.remove_button)


        self.verticalLayout.addWidget(self.widget_5)


        self.horizontalLayout_3.addWidget(self.widget_2)


        self.retranslateUi(AlgoStatusWidget)

        QMetaObject.connectSlotsByName(AlgoStatusWidget)
    # setupUi

    def retranslateUi(self, AlgoStatusWidget):
        AlgoStatusWidget.setWindowTitle(QCoreApplication.translate("AlgoStatusWidget", u"Algo Status Widget", None))
        self.name_label.setText(QCoreApplication.translate("AlgoStatusWidget", u"example name", None))
        self.status_label.setText("")
        self.runtime_label.setText(QCoreApplication.translate("AlgoStatusWidget", u"Runtime:", None))
        self.runtime_value.setText("")
        self.data_count_label.setText(QCoreApplication.translate("AlgoStatusWidget", u"Data Count:", None))
        self.data_count_value.setText("")
        self.start_button.setText(QCoreApplication.translate("AlgoStatusWidget", u"Start", None))
        self.save_button.setText(QCoreApplication.translate("AlgoStatusWidget", u"Save Config", None))
        self.remove_button.setText(QCoreApplication.translate("AlgoStatusWidget", u"Remove", None))
    # retranslateUi

