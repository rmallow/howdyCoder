# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'controlWidget.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_ControlWidget(object):
    def setupUi(self, ControlWidget):
        if not ControlWidget.objectName():
            ControlWidget.setObjectName(u"ControlWidget")
        ControlWidget.resize(582, 487)
        self.verticalLayout = QVBoxLayout(ControlWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.mainWidget = QWidget(ControlWidget)
        self.mainWidget.setObjectName(u"mainWidget")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(5)
        sizePolicy.setHeightForWidth(self.mainWidget.sizePolicy().hasHeightForWidth())
        self.mainWidget.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.mainWidget)

        self.widget = QWidget(ControlWidget)
        self.widget.setObjectName(u"widget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(1)
        sizePolicy1.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy1)
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.controlAllButton = QPushButton(self.widget)
        self.controlAllButton.setObjectName(u"controlAllButton")
        sizePolicy2 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.controlAllButton.sizePolicy().hasHeightForWidth())
        self.controlAllButton.setSizePolicy(sizePolicy2)
        self.controlAllButton.setMinimumSize(QSize(150, 50))

        self.horizontalLayout.addWidget(self.controlAllButton)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addWidget(self.widget)


        self.retranslateUi(ControlWidget)

        QMetaObject.connectSlotsByName(ControlWidget)
    # setupUi

    def retranslateUi(self, ControlWidget):
        ControlWidget.setWindowTitle(QCoreApplication.translate("ControlWidget", u"Control Widget", None))
        self.controlAllButton.setText(QCoreApplication.translate("ControlWidget", u"Start All", None))
    # retranslateUi

