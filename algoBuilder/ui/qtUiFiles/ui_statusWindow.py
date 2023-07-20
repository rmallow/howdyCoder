# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'statusWindow.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_StatusWindow(object):
    def setupUi(self, StatusWindow):
        if not StatusWindow.objectName():
            StatusWindow.setObjectName(u"StatusWindow")
        StatusWindow.resize(400, 300)
        self.horizontalLayout = QHBoxLayout(StatusWindow)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.processView = QTreeView(StatusWindow)
        self.processView.setObjectName(u"processView")

        self.horizontalLayout.addWidget(self.processView)


        self.retranslateUi(StatusWindow)

        QMetaObject.connectSlotsByName(StatusWindow)
    # setupUi

    def retranslateUi(self, StatusWindow):
        StatusWindow.setWindowTitle(QCoreApplication.translate("StatusWindow", u"Status Window", None))
    # retranslateUi

