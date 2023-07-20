# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'createActionSettingsPage.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_CreateActionSettingsPage(object):
    def setupUi(self, CreateActionSettingsPage):
        if not CreateActionSettingsPage.objectName():
            CreateActionSettingsPage.setObjectName(u"CreateActionSettingsPage")
        CreateActionSettingsPage.resize(792, 561)
        self.verticalLayout = QVBoxLayout(CreateActionSettingsPage)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(CreateActionSettingsPage)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(15)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setWordWrap(True)

        self.verticalLayout.addWidget(self.label)

        self.widget = QWidget(CreateActionSettingsPage)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.widget_2 = QWidget(self.widget)
        self.widget_2.setObjectName(u"widget_2")
        self.verticalLayout_3 = QVBoxLayout(self.widget_2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_2 = QLabel(self.widget_2)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setAlignment(Qt.AlignCenter)

        self.verticalLayout_3.addWidget(self.label_2)

        self.availableInputTable = QTableView(self.widget_2)
        self.availableInputTable.setObjectName(u"availableInputTable")
        font1 = QFont()
        font1.setPointSize(18)
        self.availableInputTable.setFont(font1)
        self.availableInputTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.availableInputTable.setSelectionMode(QAbstractItemView.NoSelection)

        self.verticalLayout_3.addWidget(self.availableInputTable)


        self.horizontalLayout.addWidget(self.widget_2)

        self.widget_3 = QWidget(self.widget)
        self.widget_3.setObjectName(u"widget_3")
        self.verticalLayout_2 = QVBoxLayout(self.widget_3)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_3 = QLabel(self.widget_3)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setAlignment(Qt.AlignCenter)

        self.verticalLayout_2.addWidget(self.label_3)

        self.selectedInputTable = QTableView(self.widget_3)
        self.selectedInputTable.setObjectName(u"selectedInputTable")
        self.selectedInputTable.setFont(font1)
        self.selectedInputTable.setSelectionMode(QAbstractItemView.SingleSelection)

        self.verticalLayout_2.addWidget(self.selectedInputTable)

        self.widget_4 = QWidget(self.widget_3)
        self.widget_4.setObjectName(u"widget_4")
        self.horizontalLayout_4 = QHBoxLayout(self.widget_4)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.removeButton = QPushButton(self.widget_4)
        self.removeButton.setObjectName(u"removeButton")

        self.horizontalLayout_4.addWidget(self.removeButton)


        self.verticalLayout_2.addWidget(self.widget_4)


        self.horizontalLayout.addWidget(self.widget_3)


        self.verticalLayout.addWidget(self.widget)

        self.label_4 = QLabel(CreateActionSettingsPage)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setFont(font)
        self.label_4.setAlignment(Qt.AlignCenter)
        self.label_4.setWordWrap(True)

        self.verticalLayout.addWidget(self.label_4)

        self.calcFuncWidget = QWidget(CreateActionSettingsPage)
        self.calcFuncWidget.setObjectName(u"calcFuncWidget")
        self.horizontalLayout_2 = QHBoxLayout(self.calcFuncWidget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")

        self.verticalLayout.addWidget(self.calcFuncWidget)

        self.widget_5 = QWidget(CreateActionSettingsPage)
        self.widget_5.setObjectName(u"widget_5")
        self.horizontalLayout_5 = QHBoxLayout(self.widget_5)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_5 = QLabel(self.widget_5)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setFont(font)

        self.horizontalLayout_5.addWidget(self.label_5)

        self.dataTypeCombo = QComboBox(self.widget_5)
        self.dataTypeCombo.setObjectName(u"dataTypeCombo")
        self.dataTypeCombo.setFont(font)

        self.horizontalLayout_5.addWidget(self.dataTypeCombo)


        self.verticalLayout.addWidget(self.widget_5)

        self.triggerWidget = QWidget(CreateActionSettingsPage)
        self.triggerWidget.setObjectName(u"triggerWidget")
        self.verticalLayout_4 = QVBoxLayout(self.triggerWidget)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.label_6 = QLabel(self.triggerWidget)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setFont(font)
        self.label_6.setAlignment(Qt.AlignCenter)
        self.label_6.setWordWrap(True)

        self.verticalLayout_4.addWidget(self.label_6)

        self.outputFuncWidget = QWidget(self.triggerWidget)
        self.outputFuncWidget.setObjectName(u"outputFuncWidget")
        self.horizontalLayout_3 = QHBoxLayout(self.outputFuncWidget)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")

        self.verticalLayout_4.addWidget(self.outputFuncWidget)


        self.verticalLayout.addWidget(self.triggerWidget)


        self.retranslateUi(CreateActionSettingsPage)

        QMetaObject.connectSlotsByName(CreateActionSettingsPage)
    # setupUi

    def retranslateUi(self, CreateActionSettingsPage):
        CreateActionSettingsPage.setWindowTitle(QCoreApplication.translate("CreateActionSettingsPage", u"CreateActionSettingsPage", None))
        self.label.setText(QCoreApplication.translate("CreateActionSettingsPage", u"From the left table,  select which columns you'd need as input. These will be added to the table on the right.  For use in the function, you can rename them in the table on the right as needed. To remove, select a row in the input table and then hit the remove button.", None))
        self.label_2.setText(QCoreApplication.translate("CreateActionSettingsPage", u"Available Inputs", None))
        self.label_3.setText(QCoreApplication.translate("CreateActionSettingsPage", u"Selected Input", None))
        self.removeButton.setText(QCoreApplication.translate("CreateActionSettingsPage", u"Remove", None))
        self.label_4.setText(QCoreApplication.translate("CreateActionSettingsPage", u"Select the function that will operate on the data. Select by hitting the button below which will open a window for selection. The function selected determines what input is needed, so when selecting a function make sure the input you've seleced above works with that function. For more information on required input, see the documentation or guides. Extra parameters will be set on the next page.", None))
        self.label_5.setText(QCoreApplication.translate("CreateActionSettingsPage", u"Select the data type that you'd like to be the input for your function", None))
        self.label_6.setText(QCoreApplication.translate("CreateActionSettingsPage", u"For triggers, assign a output function to be performed if the above function returns true. The splitting of these functions is done to enable reusability of functions. Although, you can just do your intended outputting in the above function. This makes the below output function not required.", None))
    # retranslateUi

