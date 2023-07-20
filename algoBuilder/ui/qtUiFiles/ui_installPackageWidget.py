# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'installPackageWidget.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_InstallPackageWidget(object):
    def setupUi(self, InstallPackageWidget):
        if not InstallPackageWidget.objectName():
            InstallPackageWidget.setObjectName(u"InstallPackageWidget")
        InstallPackageWidget.resize(448, 332)
        self.verticalLayout = QVBoxLayout(InstallPackageWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.packageTable = QTableView(InstallPackageWidget)
        self.packageTable.setObjectName(u"packageTable")

        self.verticalLayout.addWidget(self.packageTable)

        self.widget = QWidget(InstallPackageWidget)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.installButton = QPushButton(self.widget)
        self.installButton.setObjectName(u"installButton")

        self.horizontalLayout.addWidget(self.installButton)


        self.verticalLayout.addWidget(self.widget)


        self.retranslateUi(InstallPackageWidget)

        QMetaObject.connectSlotsByName(InstallPackageWidget)
    # setupUi

    def retranslateUi(self, InstallPackageWidget):
        InstallPackageWidget.setWindowTitle(QCoreApplication.translate("InstallPackageWidget", u"InstallPacakgeWidget", None))
        self.installButton.setText(QCoreApplication.translate("InstallPackageWidget", u"Install", None))
    # retranslateUi

