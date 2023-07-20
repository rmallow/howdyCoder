# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'configLoader.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_ConfigLoader(object):
    def setupUi(self, ConfigLoader):
        if not ConfigLoader.objectName():
            ConfigLoader.setObjectName(u"ConfigLoader")
        ConfigLoader.resize(576, 320)
        self.gridLayout = QGridLayout(ConfigLoader)
        self.gridLayout.setObjectName(u"gridLayout")
        self.blockFileLine = QLineEdit(ConfigLoader)
        self.blockFileLine.setObjectName(u"blockFileLine")

        self.gridLayout.addWidget(self.blockFileLine, 1, 1, 1, 1)

        self.otherLoadButton = QPushButton(ConfigLoader)
        self.otherLoadButton.setObjectName(u"otherLoadButton")

        self.gridLayout.addWidget(self.otherLoadButton, 5, 2, 1, 1)

        self.otherFileLine = QLineEdit(ConfigLoader)
        self.otherFileLine.setObjectName(u"otherFileLine")

        self.gridLayout.addWidget(self.otherFileLine, 5, 1, 1, 1)

        self.otherDescription = QLabel(ConfigLoader)
        self.otherDescription.setObjectName(u"otherDescription")
        self.otherDescription.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.gridLayout.addWidget(self.otherDescription, 6, 1, 1, 1)

        self.blockDescription = QLabel(ConfigLoader)
        self.blockDescription.setObjectName(u"blockDescription")
        self.blockDescription.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.gridLayout.addWidget(self.blockDescription, 2, 1, 1, 1)

        self.blockLoadButton = QPushButton(ConfigLoader)
        self.blockLoadButton.setObjectName(u"blockLoadButton")

        self.gridLayout.addWidget(self.blockLoadButton, 1, 2, 1, 1)

        self.handlerFileLine = QLineEdit(ConfigLoader)
        self.handlerFileLine.setObjectName(u"handlerFileLine")

        self.gridLayout.addWidget(self.handlerFileLine, 3, 1, 1, 1)

        self.handlerDescription = QLabel(ConfigLoader)
        self.handlerDescription.setObjectName(u"handlerDescription")
        self.handlerDescription.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.gridLayout.addWidget(self.handlerDescription, 4, 1, 1, 1)

        self.handlerLoadButton = QPushButton(ConfigLoader)
        self.handlerLoadButton.setObjectName(u"handlerLoadButton")

        self.gridLayout.addWidget(self.handlerLoadButton, 3, 2, 1, 1)

        self.blockLabel = QLabel(ConfigLoader)
        self.blockLabel.setObjectName(u"blockLabel")

        self.gridLayout.addWidget(self.blockLabel, 1, 0, 1, 1)

        self.handlerLabel = QLabel(ConfigLoader)
        self.handlerLabel.setObjectName(u"handlerLabel")

        self.gridLayout.addWidget(self.handlerLabel, 3, 0, 1, 1)

        self.otherLabel = QLabel(ConfigLoader)
        self.otherLabel.setObjectName(u"otherLabel")

        self.gridLayout.addWidget(self.otherLabel, 5, 0, 1, 1)

        self.windowDescription = QLabel(ConfigLoader)
        self.windowDescription.setObjectName(u"windowDescription")

        self.gridLayout.addWidget(self.windowDescription, 0, 0, 1, 2)

        self.loadConfigsButton = QPushButton(ConfigLoader)
        self.loadConfigsButton.setObjectName(u"loadConfigsButton")

        self.gridLayout.addWidget(self.loadConfigsButton, 0, 2, 1, 1)


        self.retranslateUi(ConfigLoader)

        QMetaObject.connectSlotsByName(ConfigLoader)
    # setupUi

    def retranslateUi(self, ConfigLoader):
        ConfigLoader.setWindowTitle(QCoreApplication.translate("ConfigLoader", u"Configs", None))
        self.otherLoadButton.setText(QCoreApplication.translate("ConfigLoader", u"Load File", None))
        self.otherDescription.setText(QCoreApplication.translate("ConfigLoader", u"Other Label", None))
        self.blockDescription.setText(QCoreApplication.translate("ConfigLoader", u"Block Label", None))
        self.blockLoadButton.setText(QCoreApplication.translate("ConfigLoader", u"Load File", None))
        self.handlerDescription.setText(QCoreApplication.translate("ConfigLoader", u"Handler Label", None))
        self.handlerLoadButton.setText(QCoreApplication.translate("ConfigLoader", u"Load File", None))
        self.blockLabel.setText(QCoreApplication.translate("ConfigLoader", u"Block Config", None))
        self.handlerLabel.setText(QCoreApplication.translate("ConfigLoader", u"Handler Config", None))
        self.otherLabel.setText(QCoreApplication.translate("ConfigLoader", u"Other Config", None))
        self.windowDescription.setText(QCoreApplication.translate("ConfigLoader", u"Select Files to be loaded.", None))
        self.loadConfigsButton.setText(QCoreApplication.translate("ConfigLoader", u"Load Configs", None))
    # retranslateUi

