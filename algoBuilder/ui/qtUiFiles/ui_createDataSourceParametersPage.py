# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'createDataSourceParametersPage.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from ..editableTable import EditableTableView


class Ui_CreateDataSourceParametersPage(object):
    def setupUi(self, CreateDataSourceParametersPage):
        if not CreateDataSourceParametersPage.objectName():
            CreateDataSourceParametersPage.setObjectName(u"CreateDataSourceParametersPage")
        CreateDataSourceParametersPage.resize(861, 884)
        self.verticalLayout = QVBoxLayout(CreateDataSourceParametersPage)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.widget = QWidget(CreateDataSourceParametersPage)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.widget_2 = QWidget(self.widget)
        self.widget_2.setObjectName(u"widget_2")
        self.verticalLayout_2 = QVBoxLayout(self.widget_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.periodLabel = QLabel(self.widget_2)
        self.periodLabel.setObjectName(u"periodLabel")
        font = QFont()
        font.setPointSize(15)
        self.periodLabel.setFont(font)
        self.periodLabel.setWordWrap(True)

        self.verticalLayout_2.addWidget(self.periodLabel)

        self.widget_11 = QWidget(self.widget_2)
        self.widget_11.setObjectName(u"widget_11")
        self.horizontalLayout_9 = QHBoxLayout(self.widget_11)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.label_3 = QLabel(self.widget_11)
        self.label_3.setObjectName(u"label_3")
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_9.addWidget(self.label_3)

        self.periodSpinBox = QSpinBox(self.widget_11)
        self.periodSpinBox.setObjectName(u"periodSpinBox")
        self.periodSpinBox.setEnabled(True)
        sizePolicy1 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.periodSpinBox.sizePolicy().hasHeightForWidth())
        self.periodSpinBox.setSizePolicy(sizePolicy1)
        self.periodSpinBox.setMinimumSize(QSize(100, 0))
        self.periodSpinBox.setMinimum(1)
        self.periodSpinBox.setMaximum(999999)

        self.horizontalLayout_9.addWidget(self.periodSpinBox)


        self.verticalLayout_2.addWidget(self.widget_11)


        self.horizontalLayout.addWidget(self.widget_2)

        self.widget_3 = QWidget(self.widget)
        self.widget_3.setObjectName(u"widget_3")
        self.verticalLayout_3 = QVBoxLayout(self.widget_3)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label = QLabel(self.widget_3)
        self.label.setObjectName(u"label")
        self.label.setFont(font)
        self.label.setWordWrap(True)

        self.verticalLayout_3.addWidget(self.label)

        self.widget_4 = QWidget(self.widget_3)
        self.widget_4.setObjectName(u"widget_4")
        self.widget_4.setLayoutDirection(Qt.LeftToRight)
        self.horizontalLayout_2 = QHBoxLayout(self.widget_4)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(12, -1, -1, -1)
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.flattenedCheck = QCheckBox(self.widget_4)
        self.flattenedCheck.setObjectName(u"flattenedCheck")
        self.flattenedCheck.setFont(font)
        self.flattenedCheck.setChecked(True)

        self.horizontalLayout_2.addWidget(self.flattenedCheck)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)


        self.verticalLayout_3.addWidget(self.widget_4)


        self.horizontalLayout.addWidget(self.widget_3)


        self.verticalLayout.addWidget(self.widget)

        self.label_4 = QLabel(CreateDataSourceParametersPage)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setFont(font)
        self.label_4.setWordWrap(True)

        self.verticalLayout.addWidget(self.label_4)

        self.widget_6 = QWidget(CreateDataSourceParametersPage)
        self.widget_6.setObjectName(u"widget_6")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(1)
        sizePolicy2.setVerticalStretch(3)
        sizePolicy2.setHeightForWidth(self.widget_6.sizePolicy().hasHeightForWidth())
        self.widget_6.setSizePolicy(sizePolicy2)
        self.horizontalLayout_6 = QHBoxLayout(self.widget_6)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.widget_7 = QWidget(self.widget_6)
        self.widget_7.setObjectName(u"widget_7")
        self.verticalLayout_4 = QVBoxLayout(self.widget_7)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.label_2 = QLabel(self.widget_7)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setAlignment(Qt.AlignCenter)

        self.verticalLayout_4.addWidget(self.label_2)

        self.parameterView = EditableTableView(self.widget_7)
        self.parameterView.setObjectName(u"parameterView")
        self.parameterView.setEnabled(True)

        self.verticalLayout_4.addWidget(self.parameterView)

        self.buttonWidget = QWidget(self.widget_7)
        self.buttonWidget.setObjectName(u"buttonWidget")
        self.horizontalLayout_7 = QHBoxLayout(self.buttonWidget)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.addParameterButton = QPushButton(self.buttonWidget)
        self.addParameterButton.setObjectName(u"addParameterButton")
        self.addParameterButton.setEnabled(True)

        self.horizontalLayout_7.addWidget(self.addParameterButton)

        self.removeParameterButton = QPushButton(self.buttonWidget)
        self.removeParameterButton.setObjectName(u"removeParameterButton")
        self.removeParameterButton.setEnabled(True)

        self.horizontalLayout_7.addWidget(self.removeParameterButton)

        self.clearParameterButton = QPushButton(self.buttonWidget)
        self.clearParameterButton.setObjectName(u"clearParameterButton")
        self.clearParameterButton.setEnabled(True)

        self.horizontalLayout_7.addWidget(self.clearParameterButton)


        self.verticalLayout_4.addWidget(self.buttonWidget)


        self.horizontalLayout_6.addWidget(self.widget_7)


        self.verticalLayout.addWidget(self.widget_6)


        self.retranslateUi(CreateDataSourceParametersPage)

        QMetaObject.connectSlotsByName(CreateDataSourceParametersPage)
    # setupUi

    def retranslateUi(self, CreateDataSourceParametersPage):
        CreateDataSourceParametersPage.setWindowTitle(QCoreApplication.translate("CreateDataSourceParametersPage", u"CreateDataSourceParametersPage", None))
        self.periodLabel.setText(QCoreApplication.translate("CreateDataSourceParametersPage", u"Set the period for the data source. The period is how often the data source will query the input.  IE if it is a stream data source, it will call the API URL every period number of seconds.", None))
        self.label_3.setText(QCoreApplication.translate("CreateDataSourceParametersPage", u"Period", None))
        self.label.setText(QCoreApplication.translate("CreateDataSourceParametersPage", u"Set if the output should be flattened. If any of the output is lists, flattening will cause each data point to be counted as individual data. If the ouput is a dict and contains multiple lists, flattening will only happen if all lists are the same length.", None))
        self.flattenedCheck.setText(QCoreApplication.translate("CreateDataSourceParametersPage", u"Flatten", None))
        self.label_4.setText(QCoreApplication.translate("CreateDataSourceParametersPage", u"(Advanced) Set extra parameters to be used.  This is for if your function requires any extra values set or your api url needs values filled in.  Use the buttons beneath the table to add, remove or clear all parameters. Once added, click in the name, type and value columns to modify.", None))
        self.label_2.setText(QCoreApplication.translate("CreateDataSourceParametersPage", u"Parameters", None))
        self.addParameterButton.setText(QCoreApplication.translate("CreateDataSourceParametersPage", u"Add", None))
        self.removeParameterButton.setText(QCoreApplication.translate("CreateDataSourceParametersPage", u"Remove", None))
        self.clearParameterButton.setText(QCoreApplication.translate("CreateDataSourceParametersPage", u"Clear", None))
    # retranslateUi

