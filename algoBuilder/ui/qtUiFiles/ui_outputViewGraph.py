# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'outputViewGraph.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_OutputViewGraph(object):
    def setupUi(self, OutputViewGraph):
        if not OutputViewGraph.objectName():
            OutputViewGraph.setObjectName(u"OutputViewGraph")
        OutputViewGraph.resize(1115, 535)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(OutputViewGraph.sizePolicy().hasHeightForWidth())
        OutputViewGraph.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(OutputViewGraph)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.itemFrame = QFrame(OutputViewGraph)
        self.itemFrame.setObjectName(u"itemFrame")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.itemFrame.sizePolicy().hasHeightForWidth())
        self.itemFrame.setSizePolicy(sizePolicy1)
        self.itemFrame.setFrameShape(QFrame.StyledPanel)
        self.itemFrame.setFrameShadow(QFrame.Raised)

        self.verticalLayout.addWidget(self.itemFrame)


        self.retranslateUi(OutputViewGraph)

        QMetaObject.connectSlotsByName(OutputViewGraph)
    # setupUi

    def retranslateUi(self, OutputViewGraph):
        OutputViewGraph.setWindowTitle(QCoreApplication.translate("OutputViewGraph", u"outputViewGraph", None))
    # retranslateUi

