# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'actionCreator.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from ..enumComboBox import EnumComboBox
from ..editableTable import EditableTableView


class Ui_ActionCreator(object):
    def setupUi(self, ActionCreator):
        if not ActionCreator.objectName():
            ActionCreator.setObjectName(u"ActionCreator")
        ActionCreator.resize(1039, 922)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(ActionCreator.sizePolicy().hasHeightForWidth())
        ActionCreator.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(ActionCreator)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(6, 6, 6, 6)
        self.actionNameWidget = QWidget(ActionCreator)
        self.actionNameWidget.setObjectName(u"actionNameWidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.actionNameWidget.sizePolicy().hasHeightForWidth())
        self.actionNameWidget.setSizePolicy(sizePolicy1)
        self.horizontalLayout = QHBoxLayout(self.actionNameWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.actionNameLabel = QLabel(self.actionNameWidget)
        self.actionNameLabel.setObjectName(u"actionNameLabel")

        self.horizontalLayout.addWidget(self.actionNameLabel)

        self.actionNameLineEdit = QLineEdit(self.actionNameWidget)
        self.actionNameLineEdit.setObjectName(u"actionNameLineEdit")

        self.horizontalLayout.addWidget(self.actionNameLineEdit)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_4)

        self.actionNameSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.actionNameSpacer)


        self.verticalLayout.addWidget(self.actionNameWidget)

        self.selectActionWidget = QWidget(ActionCreator)
        self.selectActionWidget.setObjectName(u"selectActionWidget")
        self.horizontalLayout_2 = QHBoxLayout(self.selectActionWidget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.selectFuncButton = QPushButton(self.selectActionWidget)
        self.selectFuncButton.setObjectName(u"selectFuncButton")

        self.horizontalLayout_2.addWidget(self.selectFuncButton)

        self.actionFuncLabel = QLabel(self.selectActionWidget)
        self.actionFuncLabel.setObjectName(u"actionFuncLabel")

        self.horizontalLayout_2.addWidget(self.actionFuncLabel)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)


        self.verticalLayout.addWidget(self.selectActionWidget)

        self.inputColumnWidget = QWidget(ActionCreator)
        self.inputColumnWidget.setObjectName(u"inputColumnWidget")
        sizePolicy2 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.inputColumnWidget.sizePolicy().hasHeightForWidth())
        self.inputColumnWidget.setSizePolicy(sizePolicy2)
        self.horizontalLayout_3 = QHBoxLayout(self.inputColumnWidget)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.widget_2 = QWidget(self.inputColumnWidget)
        self.widget_2.setObjectName(u"widget_2")
        sizePolicy3 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy3.setHorizontalStretch(2)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.widget_2.sizePolicy().hasHeightForWidth())
        self.widget_2.setSizePolicy(sizePolicy3)
        self.verticalLayout_2 = QVBoxLayout(self.widget_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_3 = QLabel(self.widget_2)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setAlignment(Qt.AlignCenter)

        self.verticalLayout_2.addWidget(self.label_3)

        self.dataSetView = QTableView(self.widget_2)
        self.dataSetView.setObjectName(u"dataSetView")
        self.dataSetView.setToolTipDuration(-1)
        self.dataSetView.setDragEnabled(True)
        self.dataSetView.setDragDropMode(QAbstractItemView.DragDrop)
        self.dataSetView.setDefaultDropAction(Qt.MoveAction)
        self.dataSetView.setSelectionMode(QAbstractItemView.SingleSelection)
        self.dataSetView.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.dataSetView.horizontalHeader().setVisible(False)
        self.dataSetView.verticalHeader().setCascadingSectionResizes(False)

        self.verticalLayout_2.addWidget(self.dataSetView)


        self.horizontalLayout_3.addWidget(self.widget_2)

        self.widget_4 = QWidget(self.inputColumnWidget)
        self.widget_4.setObjectName(u"widget_4")
        self.verticalLayout_5 = QVBoxLayout(self.widget_4)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.label_9 = QLabel(self.widget_4)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setAlignment(Qt.AlignCenter)

        self.verticalLayout_5.addWidget(self.label_9)

        self.functionDescription = QTextEdit(self.widget_4)
        self.functionDescription.setObjectName(u"functionDescription")
        self.functionDescription.setTextInteractionFlags(Qt.NoTextInteraction)

        self.verticalLayout_5.addWidget(self.functionDescription)


        self.horizontalLayout_3.addWidget(self.widget_4)

        self.label_2 = QLabel(self.inputColumnWidget)
        self.label_2.setObjectName(u"label_2")
        sizePolicy4 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy4.setHorizontalStretch(1)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy4)
        self.label_2.setScaledContents(False)
        self.label_2.setWordWrap(True)

        self.horizontalLayout_3.addWidget(self.label_2)


        self.verticalLayout.addWidget(self.inputColumnWidget)

        self.widget_7 = QWidget(ActionCreator)
        self.widget_7.setObjectName(u"widget_7")
        self.horizontalLayout_4 = QHBoxLayout(self.widget_7)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_6)

        self.addColButton = QPushButton(self.widget_7)
        self.addColButton.setObjectName(u"addColButton")
        self.addColButton.setEnabled(False)
        sizePolicy5 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.addColButton.sizePolicy().hasHeightForWidth())
        self.addColButton.setSizePolicy(sizePolicy5)

        self.horizontalLayout_4.addWidget(self.addColButton)

        self.removeColButton = QPushButton(self.widget_7)
        self.removeColButton.setObjectName(u"removeColButton")
        self.removeColButton.setEnabled(False)

        self.horizontalLayout_4.addWidget(self.removeColButton)

        self.clearColButton = QPushButton(self.widget_7)
        self.clearColButton.setObjectName(u"clearColButton")
        self.clearColButton.setEnabled(False)
        sizePolicy5.setHeightForWidth(self.clearColButton.sizePolicy().hasHeightForWidth())
        self.clearColButton.setSizePolicy(sizePolicy5)

        self.horizontalLayout_4.addWidget(self.clearColButton)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_5)


        self.verticalLayout.addWidget(self.widget_7)

        self.label_4 = QLabel(ActionCreator)
        self.label_4.setObjectName(u"label_4")
        font = QFont()
        font.setPointSize(13)
        font.setBold(False)
        font.setWeight(50)
        self.label_4.setFont(font)
        self.label_4.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label_4)

        self.actionTypeWidget = QWidget(ActionCreator)
        self.actionTypeWidget.setObjectName(u"actionTypeWidget")
        self.horizontalLayout_5 = QHBoxLayout(self.actionTypeWidget)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.actionTypeLabel = QLabel(self.actionTypeWidget)
        self.actionTypeLabel.setObjectName(u"actionTypeLabel")
        self.actionTypeLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_5.addWidget(self.actionTypeLabel)

        self.actionTypeComboBox = EnumComboBox(self.actionTypeWidget)
        self.actionTypeComboBox.setObjectName(u"actionTypeComboBox")
        self.actionTypeComboBox.setEnabled(False)

        self.horizontalLayout_5.addWidget(self.actionTypeComboBox)

        self.label_6 = QLabel(self.actionTypeWidget)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_5.addWidget(self.label_6)

        self.periodSpinBox = QSpinBox(self.actionTypeWidget)
        self.periodSpinBox.setObjectName(u"periodSpinBox")
        self.periodSpinBox.setEnabled(False)
        self.periodSpinBox.setWrapping(False)
        self.periodSpinBox.setMinimum(1)
        self.periodSpinBox.setMaximum(999999999)

        self.horizontalLayout_5.addWidget(self.periodSpinBox)

        self.label_7 = QLabel(self.actionTypeWidget)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_5.addWidget(self.label_7)

        self.aggregateComboBox = EnumComboBox(self.actionTypeWidget)
        self.aggregateComboBox.setObjectName(u"aggregateComboBox")
        self.aggregateComboBox.setEnabled(False)

        self.horizontalLayout_5.addWidget(self.aggregateComboBox)


        self.verticalLayout.addWidget(self.actionTypeWidget)

        self.triggerTypeWidget = QWidget(ActionCreator)
        self.triggerTypeWidget.setObjectName(u"triggerTypeWidget")
        self.horizontalLayout_8 = QHBoxLayout(self.triggerTypeWidget)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.triggerTypeWidget)
        self.label.setObjectName(u"label")

        self.horizontalLayout_8.addWidget(self.label)

        self.triggerTypeComboBox = EnumComboBox(self.triggerTypeWidget)
        self.triggerTypeComboBox.setObjectName(u"triggerTypeComboBox")

        self.horizontalLayout_8.addWidget(self.triggerTypeComboBox)

        self.selectOutputFuncButton = QPushButton(self.triggerTypeWidget)
        self.selectOutputFuncButton.setObjectName(u"selectOutputFuncButton")
        self.selectOutputFuncButton.setEnabled(False)

        self.horizontalLayout_8.addWidget(self.selectOutputFuncButton)

        self.outputFuncLabel = QLabel(self.triggerTypeWidget)
        self.outputFuncLabel.setObjectName(u"outputFuncLabel")
        self.outputFuncLabel.setEnabled(False)

        self.horizontalLayout_8.addWidget(self.outputFuncLabel)


        self.verticalLayout.addWidget(self.triggerTypeWidget)

        self.parameterWidget = QWidget(ActionCreator)
        self.parameterWidget.setObjectName(u"parameterWidget")
        sizePolicy2.setHeightForWidth(self.parameterWidget.sizePolicy().hasHeightForWidth())
        self.parameterWidget.setSizePolicy(sizePolicy2)
        self.horizontalLayout_6 = QHBoxLayout(self.parameterWidget)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.widget_5 = QWidget(self.parameterWidget)
        self.widget_5.setObjectName(u"widget_5")
        self.verticalLayout_3 = QVBoxLayout(self.widget_5)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_8 = QLabel(self.widget_5)
        self.label_8.setObjectName(u"label_8")
        font1 = QFont()
        font1.setPointSize(12)
        self.label_8.setFont(font1)
        self.label_8.setAlignment(Qt.AlignBottom|Qt.AlignHCenter)

        self.verticalLayout_3.addWidget(self.label_8)

        self.parameterView = EditableTableView(self.widget_5)
        self.parameterView.setObjectName(u"parameterView")
        self.parameterView.setToolTipDuration(5)
        self.parameterView.setSelectionMode(QAbstractItemView.SingleSelection)
        self.parameterView.horizontalHeader().setMinimumSectionSize(30)
        self.parameterView.verticalHeader().setMinimumSectionSize(30)

        self.verticalLayout_3.addWidget(self.parameterView)

        self.widget_3 = QWidget(self.widget_5)
        self.widget_3.setObjectName(u"widget_3")
        self.horizontalLayout_7 = QHBoxLayout(self.widget_3)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_2)

        self.addParameterButton = QPushButton(self.widget_3)
        self.addParameterButton.setObjectName(u"addParameterButton")
        self.addParameterButton.setEnabled(False)

        self.horizontalLayout_7.addWidget(self.addParameterButton)

        self.removeParameterButton = QPushButton(self.widget_3)
        self.removeParameterButton.setObjectName(u"removeParameterButton")
        self.removeParameterButton.setEnabled(False)

        self.horizontalLayout_7.addWidget(self.removeParameterButton)

        self.clearParameterButton = QPushButton(self.widget_3)
        self.clearParameterButton.setObjectName(u"clearParameterButton")
        self.clearParameterButton.setEnabled(False)

        self.horizontalLayout_7.addWidget(self.clearParameterButton)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_3)


        self.verticalLayout_3.addWidget(self.widget_3)


        self.horizontalLayout_6.addWidget(self.widget_5)


        self.verticalLayout.addWidget(self.parameterWidget)


        self.retranslateUi(ActionCreator)

        self.actionTypeComboBox.setCurrentIndex(-1)
        self.aggregateComboBox.setCurrentIndex(-1)


        QMetaObject.connectSlotsByName(ActionCreator)
    # setupUi

    def retranslateUi(self, ActionCreator):
        ActionCreator.setWindowTitle(QCoreApplication.translate("ActionCreator", u"actionCreator", None))
        self.actionNameLabel.setText(QCoreApplication.translate("ActionCreator", u"Name:", None))
        self.selectFuncButton.setText(QCoreApplication.translate("ActionCreator", u"Select an action function", None))
        self.actionFuncLabel.setText(QCoreApplication.translate("ActionCreator", u"Select an action function to proceed", None))
        self.label_3.setText(QCoreApplication.translate("ActionCreator", u"Input Column Table", None))
#if QT_CONFIG(tooltip)
        self.dataSetView.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.label_9.setText(QCoreApplication.translate("ActionCreator", u"Function Description", None))
        self.label_2.setText(QCoreApplication.translate("ActionCreator", u"Fill in the input column table to the left.  To select a colum from the table above either select the input column to the left and shift click above, or right click on the table above. ", None))
        self.addColButton.setText(QCoreApplication.translate("ActionCreator", u"Add Data Column", None))
        self.removeColButton.setText(QCoreApplication.translate("ActionCreator", u"Remove Data Column", None))
        self.clearColButton.setText(QCoreApplication.translate("ActionCreator", u"Clear Data Columns", None))
        self.label_4.setText(QCoreApplication.translate("ActionCreator", u"Parameters", None))
#if QT_CONFIG(tooltip)
        self.actionTypeLabel.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.actionTypeLabel.setText(QCoreApplication.translate("ActionCreator", u"ActionType:", None))
        self.actionTypeComboBox.setCurrentText("")
        self.actionTypeComboBox.setPlaceholderText("")
        self.label_6.setText(QCoreApplication.translate("ActionCreator", u"Period:", None))
        self.label_7.setText(QCoreApplication.translate("ActionCreator", u"Aggregate:", None))
        self.label.setText(QCoreApplication.translate("ActionCreator", u"Trigger Output Type:", None))
        self.selectOutputFuncButton.setText(QCoreApplication.translate("ActionCreator", u"Select an output function", None))
        self.outputFuncLabel.setText(QCoreApplication.translate("ActionCreator", u"Select an output function", None))
        self.label_8.setText(QCoreApplication.translate("ActionCreator", u"Parameters", None))
#if QT_CONFIG(tooltip)
        self.parameterView.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.addParameterButton.setText(QCoreApplication.translate("ActionCreator", u"Add", None))
        self.removeParameterButton.setText(QCoreApplication.translate("ActionCreator", u"Remove", None))
        self.clearParameterButton.setText(QCoreApplication.translate("ActionCreator", u"Clear", None))
    # retranslateUi

