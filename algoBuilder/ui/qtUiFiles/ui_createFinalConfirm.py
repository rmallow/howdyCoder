# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'createFinalConfirm.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class Ui_CreateFinalConfirm(object):
    def setupUi(self, CreateFinalConfirm):
        if not CreateFinalConfirm.objectName():
            CreateFinalConfirm.setObjectName("CreateFinalConfirm")
        CreateFinalConfirm.resize(400, 300)
        self.verticalLayout = QVBoxLayout(CreateFinalConfirm)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QLabel(CreateFinalConfirm)
        self.label.setObjectName("label")
        font = QFont()
        font.setPointSize(15)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setWordWrap(True)

        self.verticalLayout.addWidget(self.label)

        self.config_text_view = QPlainTextEdit(CreateFinalConfirm)
        self.config_text_view.setObjectName("config_text_view")
        self.config_text_view.setFont(font)
        self.config_text_view.setUndoRedoEnabled(False)
        self.config_text_view.setTextInteractionFlags(Qt.NoTextInteraction)

        self.verticalLayout.addWidget(self.config_text_view)

        self.retranslateUi(CreateFinalConfirm)

        QMetaObject.connectSlotsByName(CreateFinalConfirm)

    # setupUi

    def retranslateUi(self, CreateFinalConfirm):
        CreateFinalConfirm.setWindowTitle(
            QCoreApplication.translate("CreateFinalConfirm", "CreateFinalConfirm", None)
        )
        self.label.setText(
            QCoreApplication.translate(
                "CreateFinalConfirm",
                "The final config. Hit start over to start new with a new config or hit finish to add this algo.",
                None,
            )
        )

    # retranslateUi
