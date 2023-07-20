# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'createDataSourceSettingsPage.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_CreateDataSourceSettingsPage(object):
    def setupUi(self, CreateDataSourceSettingsPage):
        if not CreateDataSourceSettingsPage.objectName():
            CreateDataSourceSettingsPage.setObjectName(u"CreateDataSourceSettingsPage")
        CreateDataSourceSettingsPage.resize(502, 416)
        self.verticalLayout = QVBoxLayout(CreateDataSourceSettingsPage)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(CreateDataSourceSettingsPage)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label)

        self.stackedWidget = QStackedWidget(CreateDataSourceSettingsPage)
        self.stackedWidget.setObjectName(u"stackedWidget")

        self.verticalLayout.addWidget(self.stackedWidget)

        self.label_2 = QLabel(CreateDataSourceSettingsPage)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label_2)

        self.outputView = QListView(CreateDataSourceSettingsPage)
        self.outputView.setObjectName(u"outputView")
        font = QFont()
        font.setPointSize(30)
        self.outputView.setFont(font)

        self.verticalLayout.addWidget(self.outputView)

        self.widget_8 = QWidget(CreateDataSourceSettingsPage)
        self.widget_8.setObjectName(u"widget_8")
        self.horizontalLayout_5 = QHBoxLayout(self.widget_8)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.addOutputButton = QPushButton(self.widget_8)
        self.addOutputButton.setObjectName(u"addOutputButton")
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.addOutputButton.sizePolicy().hasHeightForWidth())
        self.addOutputButton.setSizePolicy(sizePolicy)

        self.horizontalLayout_5.addWidget(self.addOutputButton)

        self.removeOutputButton = QPushButton(self.widget_8)
        self.removeOutputButton.setObjectName(u"removeOutputButton")
        sizePolicy.setHeightForWidth(self.removeOutputButton.sizePolicy().hasHeightForWidth())
        self.removeOutputButton.setSizePolicy(sizePolicy)

        self.horizontalLayout_5.addWidget(self.removeOutputButton)


        self.verticalLayout.addWidget(self.widget_8)

        self.outputHelpText = QLabel(CreateDataSourceSettingsPage)
        self.outputHelpText.setObjectName(u"outputHelpText")
        self.outputHelpText.setAlignment(Qt.AlignCenter)
        self.outputHelpText.setWordWrap(True)

        self.verticalLayout.addWidget(self.outputHelpText)


        self.retranslateUi(CreateDataSourceSettingsPage)

        QMetaObject.connectSlotsByName(CreateDataSourceSettingsPage)
    # setupUi

    def retranslateUi(self, CreateDataSourceSettingsPage):
        CreateDataSourceSettingsPage.setWindowTitle(QCoreApplication.translate("CreateDataSourceSettingsPage", u"CreateDataSourceSettingsPage", None))
        self.label.setText(QCoreApplication.translate("CreateDataSourceSettingsPage", u"Select Settings Based on the Type", None))
        self.label_2.setText(QCoreApplication.translate("CreateDataSourceSettingsPage", u"Output from Selection", None))
        self.addOutputButton.setText(QCoreApplication.translate("CreateDataSourceSettingsPage", u"+", None))
        self.removeOutputButton.setText(QCoreApplication.translate("CreateDataSourceSettingsPage", u"-", None))
        self.outputHelpText.setText("")
    # retranslateUi

