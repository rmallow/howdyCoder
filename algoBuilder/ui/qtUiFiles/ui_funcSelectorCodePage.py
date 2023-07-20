# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'funcSelectorCodePage.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_FuncSelectorCodePage(object):
    def setupUi(self, FuncSelectorCodePage):
        if not FuncSelectorCodePage.objectName():
            FuncSelectorCodePage.setObjectName(u"FuncSelectorCodePage")
        FuncSelectorCodePage.resize(493, 351)
        self.verticalLayout = QVBoxLayout(FuncSelectorCodePage)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.infoLabel = QLabel(FuncSelectorCodePage)
        self.infoLabel.setObjectName(u"infoLabel")
        self.infoLabel.setWordWrap(True)

        self.verticalLayout.addWidget(self.infoLabel)

        self.codeEdit = QPlainTextEdit(FuncSelectorCodePage)
        self.codeEdit.setObjectName(u"codeEdit")
        self.codeEdit.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.codeEdit.setTabStopWidth(4)

        self.verticalLayout.addWidget(self.codeEdit)

        self.statusLabel = QLabel(FuncSelectorCodePage)
        self.statusLabel.setObjectName(u"statusLabel")
        self.statusLabel.setWordWrap(True)

        self.verticalLayout.addWidget(self.statusLabel)

        self.widget = QWidget(FuncSelectorCodePage)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.saveStatusLabel = QLabel(self.widget)
        self.saveStatusLabel.setObjectName(u"saveStatusLabel")

        self.horizontalLayout.addWidget(self.saveStatusLabel)

        self.saveButton = QPushButton(self.widget)
        self.saveButton.setObjectName(u"saveButton")

        self.horizontalLayout.addWidget(self.saveButton)

        self.selectButton = QPushButton(self.widget)
        self.selectButton.setObjectName(u"selectButton")

        self.horizontalLayout.addWidget(self.selectButton)


        self.verticalLayout.addWidget(self.widget)


        self.retranslateUi(FuncSelectorCodePage)

        QMetaObject.connectSlotsByName(FuncSelectorCodePage)
    # setupUi

    def retranslateUi(self, FuncSelectorCodePage):
        FuncSelectorCodePage.setWindowTitle(QCoreApplication.translate("FuncSelectorCodePage", u"FuncSelectorCodePage", None))
        self.infoLabel.setText(QCoreApplication.translate("FuncSelectorCodePage", u"Enter code from an AI code generator, such as ChatGPT.  See documentation for prompts to use.", None))
        self.codeEdit.setPlaceholderText(QCoreApplication.translate("FuncSelectorCodePage", u"Enter Code Here", None))
        self.statusLabel.setText("")
        self.saveStatusLabel.setText("")
        self.saveButton.setText(QCoreApplication.translate("FuncSelectorCodePage", u"Save", None))
        self.selectButton.setText(QCoreApplication.translate("FuncSelectorCodePage", u"Select", None))
    # retranslateUi

