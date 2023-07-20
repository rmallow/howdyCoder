# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'createWidget.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from ..create.progressSteps import ProgressSteps


class Ui_CreateWidget(object):
    def setupUi(self, CreateWidget):
        if not CreateWidget.objectName():
            CreateWidget.setObjectName(u"CreateWidget")
        CreateWidget.resize(1005, 574)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(CreateWidget.sizePolicy().hasHeightForWidth())
        CreateWidget.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(CreateWidget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.widget = QWidget(CreateWidget)
        self.widget.setObjectName(u"widget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy1)
        self.widget.setMinimumSize(QSize(0, 0))
        self.widget.setMaximumSize(QSize(16777215, 16777215))
        self.widget.setLayoutDirection(Qt.LeftToRight)
        self.widget.setStyleSheet(u"")
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.progressSteps = ProgressSteps(self.widget)
        self.progressSteps.setObjectName(u"progressSteps")
        sizePolicy2 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Maximum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.progressSteps.sizePolicy().hasHeightForWidth())
        self.progressSteps.setSizePolicy(sizePolicy2)

        self.horizontalLayout.addWidget(self.progressSteps)


        self.verticalLayout.addWidget(self.widget)

        self.widget_3 = QWidget(CreateWidget)
        self.widget_3.setObjectName(u"widget_3")
        self.widget_3.setMinimumSize(QSize(0, 0))
        self.widget_3.setLayoutDirection(Qt.LeftToRight)
        self.horizontalLayout_3 = QHBoxLayout(self.widget_3)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.exitButton = QPushButton(self.widget_3)
        self.exitButton.setObjectName(u"exitButton")

        self.horizontalLayout_3.addWidget(self.exitButton)


        self.verticalLayout.addWidget(self.widget_3, 0, Qt.AlignRight)

        self.scrollArea = QScrollArea(CreateWidget)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 1003, 494))
        self.verticalLayout_2 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.createWidgetBox = QWidget(self.scrollAreaWidgetContents)
        self.createWidgetBox.setObjectName(u"createWidgetBox")
        sizePolicy3 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(10)
        sizePolicy3.setHeightForWidth(self.createWidgetBox.sizePolicy().hasHeightForWidth())
        self.createWidgetBox.setSizePolicy(sizePolicy3)
        self.createWidgetBox.setStyleSheet(u"")

        self.verticalLayout_2.addWidget(self.createWidgetBox)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout.addWidget(self.scrollArea)

        self.widget_2 = QWidget(CreateWidget)
        self.widget_2.setObjectName(u"widget_2")
        self.horizontalLayout_2 = QHBoxLayout(self.widget_2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(-1, 6, -1, 6)
        self.backButton = QPushButton(self.widget_2)
        self.backButton.setObjectName(u"backButton")
        sizePolicy4 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.backButton.sizePolicy().hasHeightForWidth())
        self.backButton.setSizePolicy(sizePolicy4)

        self.horizontalLayout_2.addWidget(self.backButton)

        self.nextButton = QPushButton(self.widget_2)
        self.nextButton.setObjectName(u"nextButton")
        sizePolicy4.setHeightForWidth(self.nextButton.sizePolicy().hasHeightForWidth())
        self.nextButton.setSizePolicy(sizePolicy4)

        self.horizontalLayout_2.addWidget(self.nextButton)


        self.verticalLayout.addWidget(self.widget_2, 0, Qt.AlignHCenter)


        self.retranslateUi(CreateWidget)

        QMetaObject.connectSlotsByName(CreateWidget)
    # setupUi

    def retranslateUi(self, CreateWidget):
        CreateWidget.setWindowTitle(QCoreApplication.translate("CreateWidget", u"createWidget", None))
        self.exitButton.setText(QCoreApplication.translate("CreateWidget", u"Exit Creator", None))
        self.backButton.setText(QCoreApplication.translate("CreateWidget", u"Back", None))
        self.nextButton.setText(QCoreApplication.translate("CreateWidget", u"Next", None))
    # retranslateUi

