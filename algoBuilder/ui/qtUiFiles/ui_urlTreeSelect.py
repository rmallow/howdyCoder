# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'urlTreeSelect.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_UrlTreeSelect(object):
    def setupUi(self, UrlTreeSelect):
        if not UrlTreeSelect.objectName():
            UrlTreeSelect.setObjectName(u"UrlTreeSelect")
        UrlTreeSelect.resize(532, 634)
        self.verticalLayout = QVBoxLayout(UrlTreeSelect)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.TestLabel = QLabel(UrlTreeSelect)
        self.TestLabel.setObjectName(u"TestLabel")

        self.horizontalLayout.addWidget(self.TestLabel)

        self.urlInput = QLineEdit(UrlTreeSelect)
        self.urlInput.setObjectName(u"urlInput")

        self.horizontalLayout.addWidget(self.urlInput)

        self.testButton = QPushButton(UrlTreeSelect)
        self.testButton.setObjectName(u"testButton")

        self.horizontalLayout.addWidget(self.testButton)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.widget = QWidget(UrlTreeSelect)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout_3 = QHBoxLayout(self.widget)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.apiOutputLabel = QLabel(self.widget)
        self.apiOutputLabel.setObjectName(u"apiOutputLabel")

        self.horizontalLayout_3.addWidget(self.apiOutputLabel)


        self.verticalLayout.addWidget(self.widget)

        self.label = QLabel(UrlTreeSelect)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(15)
        self.label.setFont(font)
        self.label.setWordWrap(True)

        self.verticalLayout.addWidget(self.label)

        self.expandButton = QPushButton(UrlTreeSelect)
        self.expandButton.setObjectName(u"expandButton")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.expandButton.sizePolicy().hasHeightForWidth())
        self.expandButton.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.expandButton)

        self.outputTreeView = QTreeView(UrlTreeSelect)
        self.outputTreeView.setObjectName(u"outputTreeView")
        self.outputTreeView.setMouseTracking(True)
        self.outputTreeView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.outputTreeView.setSelectionMode(QAbstractItemView.NoSelection)
        self.outputTreeView.setHeaderHidden(True)

        self.verticalLayout.addWidget(self.outputTreeView)

        self.selectedOutputLabel = QLabel(UrlTreeSelect)
        self.selectedOutputLabel.setObjectName(u"selectedOutputLabel")
        self.selectedOutputLabel.setFont(font)
        self.selectedOutputLabel.setWordWrap(True)

        self.verticalLayout.addWidget(self.selectedOutputLabel)

        self.selectedTableView = QTableView(UrlTreeSelect)
        self.selectedTableView.setObjectName(u"selectedTableView")
        self.selectedTableView.setEditTriggers(QAbstractItemView.DoubleClicked)
        self.selectedTableView.setShowGrid(False)
        self.selectedTableView.horizontalHeader().setHighlightSections(False)
        self.selectedTableView.verticalHeader().setVisible(False)

        self.verticalLayout.addWidget(self.selectedTableView)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.removeButton = QPushButton(UrlTreeSelect)
        self.removeButton.setObjectName(u"removeButton")

        self.horizontalLayout_2.addWidget(self.removeButton)

        self.clearButton = QPushButton(UrlTreeSelect)
        self.clearButton.setObjectName(u"clearButton")

        self.horizontalLayout_2.addWidget(self.clearButton)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.widget_2 = QWidget(UrlTreeSelect)
        self.widget_2.setObjectName(u"widget_2")
        self.horizontalLayout_4 = QHBoxLayout(self.widget_2)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer)

        self.doneButton = QPushButton(self.widget_2)
        self.doneButton.setObjectName(u"doneButton")

        self.horizontalLayout_4.addWidget(self.doneButton)


        self.verticalLayout.addWidget(self.widget_2)


        self.retranslateUi(UrlTreeSelect)

        QMetaObject.connectSlotsByName(UrlTreeSelect)
    # setupUi

    def retranslateUi(self, UrlTreeSelect):
        UrlTreeSelect.setWindowTitle(QCoreApplication.translate("UrlTreeSelect", u"URL Tree Select", None))
        self.TestLabel.setText(QCoreApplication.translate("UrlTreeSelect", u"Enter an API URL:", None))
        self.testButton.setText(QCoreApplication.translate("UrlTreeSelect", u"Execute", None))
        self.apiOutputLabel.setText(QCoreApplication.translate("UrlTreeSelect", u"API Output:", None))
        self.label.setText(QCoreApplication.translate("UrlTreeSelect", u"Expand and navigate the url output, after entering and executing above.  Select the data that you want to use as part of your data source.  Each selection will be added to the bottom table.", None))
        self.expandButton.setText(QCoreApplication.translate("UrlTreeSelect", u"Expand All", None))
        self.selectedOutputLabel.setText(QCoreApplication.translate("UrlTreeSelect", u"Selected Output - Click on the names in the right column to rename them. The items in the left column are what have been selected from above.", None))
        self.removeButton.setText(QCoreApplication.translate("UrlTreeSelect", u"Remove", None))
        self.clearButton.setText(QCoreApplication.translate("UrlTreeSelect", u"Clear All", None))
        self.doneButton.setText(QCoreApplication.translate("UrlTreeSelect", u"Done", None))
    # retranslateUi

