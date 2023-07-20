# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'loadingScreen.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_LoadingScreen(object):
    def setupUi(self, LoadingScreen):
        if not LoadingScreen.objectName():
            LoadingScreen.setObjectName(u"LoadingScreen")
        LoadingScreen.resize(450, 75)
        self.verticalLayout = QVBoxLayout(LoadingScreen)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(LoadingScreen)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label)

        self.progressBar = QProgressBar(LoadingScreen)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setValue(0)

        self.verticalLayout.addWidget(self.progressBar)


        self.retranslateUi(LoadingScreen)

        QMetaObject.connectSlotsByName(LoadingScreen)
    # setupUi

    def retranslateUi(self, LoadingScreen):
        LoadingScreen.setWindowTitle(QCoreApplication.translate("LoadingScreen", u"Loading Items", None))
        self.label.setText(QCoreApplication.translate("LoadingScreen", u"Loading", None))
    # retranslateUi

