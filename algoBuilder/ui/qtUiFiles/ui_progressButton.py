# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'progressButton.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_ProgressButton(object):
    def setupUi(self, ProgressButton):
        if not ProgressButton.objectName():
            ProgressButton.setObjectName(u"ProgressButton")
        ProgressButton.resize(73, 104)
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ProgressButton.sizePolicy().hasHeightForWidth())
        ProgressButton.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(ProgressButton)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.widget = QWidget(ProgressButton)
        self.widget.setObjectName(u"widget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy1)
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.button = QPushButton(self.widget)
        self.button.setObjectName(u"button")
        self.button.setStyleSheet(u" background-color: gray;\n"
" border-style: solid;\n"
" border-width:0px;\n"
" border-radius:20px;\n"
" max-width:40px;\n"
" max-height:40px;\n"
" min-width:40px;\n"
" min-height:40px;")

        self.horizontalLayout.addWidget(self.button)


        self.verticalLayout.addWidget(self.widget)

        self.label = QLabel(ProgressButton)
        self.label.setObjectName(u"label")
        sizePolicy1.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy1)
        self.label.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label)


        self.retranslateUi(ProgressButton)

        QMetaObject.connectSlotsByName(ProgressButton)
    # setupUi

    def retranslateUi(self, ProgressButton):
        ProgressButton.setWindowTitle(QCoreApplication.translate("ProgressButton", u"progressButton", None))
        self.button.setText("")
        self.label.setText("")
    # retranslateUi

