# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'displayTab.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class Ui_displayTab(object):
    def setupUi(self, displayTab):
        if not displayTab.objectName():
            displayTab.setObjectName("displayTab")
        displayTab.resize(1920, 1025)
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(displayTab.sizePolicy().hasHeightForWidth())
        displayTab.setSizePolicy(sizePolicy)
        self.gridLayout = QGridLayout(displayTab)
        self.gridLayout.setObjectName("gridLayout")
        self.addButton = QPushButton(displayTab)
        self.addButton.setObjectName("addButton")

        self.gridLayout.addWidget(self.addButton, 0, 0, 1, 1)

        self.deleteButton = QPushButton(displayTab)
        self.deleteButton.setObjectName("deleteButton")

        self.gridLayout.addWidget(self.deleteButton, 0, 1, 1, 1)

        self.scrollArea = QScrollArea(displayTab)
        self.scrollArea.setObjectName("scrollArea")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy1)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 1624, 999))
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.gridLayout.addWidget(self.scrollArea, 0, 2, 3, 1)

        self.listView = QListView(displayTab)
        self.listView.setObjectName("listView")
        sizePolicy2 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.listView.sizePolicy().hasHeightForWidth())
        self.listView.setSizePolicy(sizePolicy2)

        self.gridLayout.addWidget(self.listView, 2, 0, 1, 2)

        self.retranslateUi(displayTab)

        QMetaObject.connectSlotsByName(displayTab)

    # setupUi

    def retranslateUi(self, displayTab):
        displayTab.setWindowTitle(QCoreApplication.translate("displayTab", "Tab", None))
        self.addButton.setText(QCoreApplication.translate("displayTab", "Add", None))
        self.deleteButton.setText(
            QCoreApplication.translate("displayTab", "Delete", None)
        )

    # retranslateUi
