# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'outputSelectType.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_OutputSelectType(object):
    def setupUi(self, OutputSelectType):
        if not OutputSelectType.objectName():
            OutputSelectType.setObjectName(u"OutputSelectType")
        OutputSelectType.resize(400, 97)
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(OutputSelectType.sizePolicy().hasHeightForWidth())
        OutputSelectType.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(OutputSelectType)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.itemLabel = QLabel(OutputSelectType)
        self.itemLabel.setObjectName(u"itemLabel")

        self.verticalLayout.addWidget(self.itemLabel)

        self.vLayout = QVBoxLayout()
        self.vLayout.setSpacing(0)
        self.vLayout.setObjectName(u"vLayout")
        self.label = QLabel(OutputSelectType)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignCenter)

        self.vLayout.addWidget(self.label)

        self.typeComboBox = QComboBox(OutputSelectType)
        self.typeComboBox.setObjectName(u"typeComboBox")
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.typeComboBox.sizePolicy().hasHeightForWidth())
        self.typeComboBox.setSizePolicy(sizePolicy1)

        self.vLayout.addWidget(self.typeComboBox)


        self.verticalLayout.addLayout(self.vLayout)


        self.retranslateUi(OutputSelectType)

        QMetaObject.connectSlotsByName(OutputSelectType)
    # setupUi

    def retranslateUi(self, OutputSelectType):
        OutputSelectType.setWindowTitle(QCoreApplication.translate("OutputSelectType", u"outputSelectType", None))
        self.itemLabel.setText(QCoreApplication.translate("OutputSelectType", u"Item Label", None))
        self.label.setText(QCoreApplication.translate("OutputSelectType", u"Select Output Type", None))
    # retranslateUi

