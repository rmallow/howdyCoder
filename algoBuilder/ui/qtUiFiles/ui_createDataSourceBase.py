# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'createDataSourceBase.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from ..create.createDataSourceAdd import CreateDataSourceAdd


class Ui_CreateDataSourceBase(object):
    def setupUi(self, CreateDataSourceBase):
        if not CreateDataSourceBase.objectName():
            CreateDataSourceBase.setObjectName(u"CreateDataSourceBase")
        CreateDataSourceBase.resize(735, 583)
        self.verticalLayout = QVBoxLayout(CreateDataSourceBase)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(CreateDataSourceBase)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(30)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label)

        self.stackedWidget = QStackedWidget(CreateDataSourceBase)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.addPage = CreateDataSourceAdd()
        self.addPage.setObjectName(u"addPage")
        self.stackedWidget.addWidget(self.addPage)
        self.typePage = CreateDataSourceAdd()
        self.typePage.setObjectName(u"typePage")
        self.stackedWidget.addWidget(self.typePage)

        self.verticalLayout.addWidget(self.stackedWidget)


        self.retranslateUi(CreateDataSourceBase)

        QMetaObject.connectSlotsByName(CreateDataSourceBase)
    # setupUi

    def retranslateUi(self, CreateDataSourceBase):
        CreateDataSourceBase.setWindowTitle(QCoreApplication.translate("CreateDataSourceBase", u"CreateDataSourceBase", None))
        self.label.setText(QCoreApplication.translate("CreateDataSourceBase", u"Create Data Sources", None))
    # retranslateUi

