from algoBuilder.core.commonGlobals import ENUM_DISPLAY
from ..actionUIConstant import (
    ActionEnum,
    ActionFuncEnum,
    DataSetEnum,
    INVALID_ACTION_KEY,
    ActionTypeEnum,
    TriggerTypeEnum,
    AggregateTypeEnum,
)
from ..funcSelector import FuncSelector
from .. import editableTable
from ..create import parameterTable

from .qtUiFiles import ui_actionCreator
from ...commonUtil.helpers import createErrorLabel

import typing
import copy
from PySide2 import QtWidgets, QtGui, QtCore


class DataSetTableModel(editableTable.EditableTableModelAddColumn):
    """
    Derived class for implementing Action Data Set Table
    """

    def __init__(self, parent: typing.Optional[QtCore.QObject] = None) -> None:
        super().__init__(DataSetEnum, parent=parent)
        self.values: typing.List[typing.Dict[DataSetEnum, typing.Any]] = []

    def setData(
        self,
        index: QtCore.QModelIndex,
        value: typing.Any,
        role: int = QtCore.Qt.DisplayRole,
    ) -> bool:
        if role == QtCore.Qt.EditRole or role == QtCore.Qt.DisplayRole:
            # if the user modified the container then replace the value in inputs
            enumKey = DataSetEnum(index.row())
            if enumKey == DataSetEnum.INDEX:
                # make sure not a negative value
                if value < 0:
                    value = 0
                # make sure it's a valid index, as in it's not any of the other indexes
                for curValue in self.values:
                    if value == curValue[DataSetEnum.INDEX]:
                        return False
            elif enumKey == DataSetEnum.SOURCE:
                # make sure it's not an empty string
                if value == "":
                    return False
            self.values[index.column()][enumKey] = value
            return True
        else:
            return super().setData(index, value, role)

    def getNextIndex(self):
        highest = -1
        for value in self.values:
            if value[DataSetEnum.INDEX] > highest:
                highest = value[DataSetEnum.INDEX]
        return highest + 1

    @QtCore.Slot()
    def addColumn(self):
        newCol = {
            DataSetEnum.SOURCE: "",
            DataSetEnum.INDEX: self.getNextIndex(),
            DataSetEnum.MAPPING: "",
        }
        super().appendValue(newCol)

    def getValuesCopy(self):
        """This list could be cleared after but we'd still need to retain the values elsewhere"""
        return copy.deepcopy(self.values)


class ActionCreator(QtWidgets.QWidget):
    addAction = QtCore.Signal(dict)
    """
    Widget for creating an action
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        # Load UI file

        self._ui = ui_actionCreator.Ui_ActionCreator()
        self._ui.setupUi(self)
        self._ui.triggerTypeWidget.hide()

        self._ui.actionTypeComboBox.setEnum(ActionTypeEnum)
        self._ui.aggregateComboBox.setEnum(AggregateTypeEnum)
        self._ui.triggerTypeComboBox.setEnum(TriggerTypeEnum)

        # Create func selector and its configurations
        self._funcSelector = FuncSelector()
        self._functionConfig = None
        self._outputFuncConfig = None
        self._actionFuncBeingSelected = True

        # Create Models and setup views
        self._dataSetModel = DataSetTableModel()
        self._ui.dataSetView.setModel(self._dataSetModel)
        self._ui.dataSetView.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.Stretch
        )

        self._parameterModel = parameterTable.ParameterTableModel()
        self._ui.parameterView.setModel(self._parameterModel)

        # connect signal and slots
        self._ui.selectFuncButton.pressed.connect(self.showFuncSelector)
        self._funcSelector.itemSelected.connect(self.itemSelected)
        # dataSet connections
        self._ui.addColButton.pressed.connect(self._dataSetModel.addColumn)
        self._ui.clearColButton.pressed.connect(self._dataSetModel.clear)
        self._ui.removeColButton.pressed.connect(self.removeSelectedDataSet)
        # parameter connections
        self._ui.addParameterButton.pressed.connect(self._parameterModel.appendValue)
        self._ui.removeParameterButton.pressed.connect(
            lambda: self._parameterModel.removeValue(
                self._ui.parameterView.getSelected()
            )
        )
        self._ui.clearParameterButton.pressed.connect(self._parameterModel.clear)
        self._ui.actionTypeComboBox.currentTextChanged.connect(self.actionTypeChanged)
        self._ui.triggerTypeComboBox.currentTextChanged.connect(self.triggerTypeChanged)
        self._ui.selectOutputFuncButton.pressed.connect(
            lambda: self.showFuncSelector(False)
        )

    @QtCore.Slot()
    def validateAction(self):
        """Package up the action from the ui settings and send in a signal or send error if invalid"""
        actionDict = {}
        errorList = []

        # Populate the required fields or add an error
        if self._ui.actionNameLineEdit.text() != "":
            actionDict[ActionEnum.NAME] = self._ui.actionNameLineEdit.text()
        else:
            errorList.append("name not selected")

        if self._functionConfig is not None:
            actionDict[ActionEnum.ACTION_FUNC] = self._functionConfig
        else:
            errorList.append("action func not selected")

        if self._ui.actionTypeComboBox.currentIndex() != -1:
            currentText = self._ui.actionTypeComboBox.currentText()
            actionDict[ActionEnum.TYPE] = currentText
            if currentText == ActionTypeEnum.TRIGGER.display:
                triggerType = self._ui.triggerTypeComboBox.currentText()
                actionDict[ActionEnum.TRIGGER_TYPE] = triggerType
                if triggerType == TriggerTypeEnum.FUNCTION.display:
                    if self._outputFuncConfig is not None:
                        actionDict[ActionEnum.OUTPUT_FUNC] = self._outputFuncConfig
                    else:
                        errorList.append("ouput func not selected")
        else:
            errorList.append("invalid type selected")

        if self._ui.aggregateComboBox.currentIndex() != -1:
            actionDict[ActionEnum.AGGREGATE] = self._ui.aggregateComboBox.currentText()
        else:
            errorList.append("invalid aggregate type selected")

        actionDict[ActionEnum.INPUT] = self._dataSetModel.getValuesCopy()
        actionDict[ActionEnum.PERIOD] = self._ui.periodSpinBox.value()
        actionDict[ActionEnum.PARAMETER] = self._parameterModel.getData()

        if len(errorList) > 0:
            # overwrite action dict with just error
            actionDict = {
                INVALID_ACTION_KEY: createErrorLabel(
                    "Invalid Action Config:", errorList
                )
            }
        else:
            # if there were no errors than we have a valid action, reset the creator
            self.reset()
        # emit valid or not
        self.addAction.emit(actionDict)

    def receiveActionData(self, actionDict: typing.Dict[ActionEnum, typing.Any]):
        if ActionEnum.NAME in actionDict:
            self._ui.actionNameLineEdit.setText(actionDict[ActionEnum.NAME])

    @QtCore.Slot()
    def showFuncSelector(self, actionFunc: bool = True) -> None:
        """
        Show the func selector

        Args:
            actionFunc:
                bool for whether the actionFunc button initiated the window or not
        """
        self._actionFuncBeingSelected = actionFunc
        self._funcSelector.show()
        self._funcSelector.showNormal()

    def removeSelectedDataSet(self):
        """Remove selected item from data set view"""
        indexes = self._ui.dataSetView.selectionModel().selectedIndexes()
        for index in indexes:
            self._dataSetModel.removeValue(index.column())

    @QtCore.Slot()
    def itemSelected(self, functionConfig: typing.Dict[ActionFuncEnum, str]) -> None:
        if self._actionFuncBeingSelected:
            self._functionConfig = functionConfig
            self._ui.actionFuncLabel.setText(functionConfig[ActionFuncEnum.NAME])
            self._ui.functionDescription.document().setPlainText(
                functionConfig[ActionFuncEnum.DOC_STR]
            )

            self.setControlsEnabled(True)
        else:
            self._outputFuncConfig = functionConfig
            self._ui.outputFuncLabel.setText(functionConfig[ActionFuncEnum.NAME])

    @QtCore.Slot()
    def nameSelected(self, name: typing.AnyStr):
        indexes = self._ui.dataSetView.selectionModel().selectedIndexes()
        for index in indexes:
            if index.isValid():
                sourceIndex = index.siblingAtRow(DataSetEnum.SOURCE.value)
                if sourceIndex.isValid():
                    self._dataSetModel.setData(sourceIndex, name)

    def setControlsEnabled(self, isEnabled: bool) -> None:
        """
        Enable/Disable the controls aside from the name edit and the func selector
        """
        # dataset buttons
        self._ui.addColButton.setEnabled(isEnabled)
        self._ui.removeColButton.setEnabled(isEnabled)
        self._ui.clearColButton.setEnabled(isEnabled)

        # required parameters
        self._ui.actionTypeComboBox.setEnabled(isEnabled)
        self._ui.periodSpinBox.setEnabled(isEnabled)
        self._ui.aggregateComboBox.setEnabled(isEnabled)

        # extra parameters
        self._ui.addParameterButton.setEnabled(isEnabled)
        self._ui.removeParameterButton.setEnabled(isEnabled)
        self._ui.clearParameterButton.setEnabled(isEnabled)

    @QtCore.Slot()
    def actionTypeChanged(self, text: str) -> None:
        if text == ActionTypeEnum.TRIGGER.display:
            self._ui.triggerTypeWidget.show()
        else:
            self._ui.triggerTypeWidget.hide()

    @QtCore.Slot()
    def triggerTypeChanged(self, text: str) -> None:
        if text == TriggerTypeEnum.FUNCTION.display:
            self.setEnabledTriggerFunc(True)
        else:
            self.setEnabledTriggerFunc(False)

    def setEnabledTriggerFunc(self, isEnabled: bool) -> None:
        self._ui.selectOutputFuncButton.setEnabled(isEnabled)
        self._ui.outputFuncLabel.setEnabled(isEnabled)

    @QtCore.Slot()
    def reset(self) -> None:
        """
        Reset the action creator back to default values
        """
        self._ui.actionNameLineEdit.setText("")

        self._functionConfg = None
        self._outputFuncConfig = None
        self._ui.actionFuncLabel.setText("Select an action function to proceed")

        self._ui.functionDescription.document().setPlainText("")
        self._dataSetModel.clear()

        self._ui.periodSpinBox.setValue(1)
        self._ui.actionTypeComboBox.setCurrentIndex(0)
        self._ui.aggregateComboBox.setCurrentIndex(0)
        self._ui.triggerTypeComboBox.setCurrentIndex(0)

        self._ui.outputFuncLabel.setText("Select an output function")

        self._parameterModel.clear()

        self.setControlsEnabled(False)
        self.setEnabledTriggerFunc(False)

    def modifyAction(self, actionDict: typing.Dict[ActionEnum, typing.Any]) -> None:
        self.reset()

        if ActionEnum.NAME in actionDict:
            self._ui.actionNameLineEdit.setText(actionDict[ActionEnum.NAME])

        if ActionEnum.TYPE in actionDict:
            self._ui.actionTypeComboBox.setItemByEnumAttribute(
                ENUM_DISPLAY, actionDict[ActionEnum.TYPE]
            )

        if ActionEnum.ACTION_FUNC in actionDict:
            self._functionConfig = actionDict[ActionEnum.ACTION_FUNC]
            self._ui.actionFuncLabel.setText(
                actionDict[ActionEnum.ACTION_FUNC][ActionFuncEnum.NAME]
            )

        if ActionEnum.INPUT in actionDict:
            self._dataSetModel.setValues(actionDict[ActionEnum.INPUT])

        if ActionEnum.AGGREGATE in actionDict:
            self._ui.aggregateComboBox.setItemByEnumAttribute(
                ENUM_DISPLAY, actionDict[ActionEnum.AGGREGATE]
            )

        if ActionEnum.TRIGGER_TYPE in actionDict:
            self._ui.triggerTypeComboBox.setItemByEnumAttribute(
                ENUM_DISPLAY, actionDict[ActionEnum.TRIGGER_TYPE]
            )

        if ActionEnum.OUTPUT_FUNC in actionDict:
            self._outputFuncConfig = actionDict[ActionEnum.OUTPUT_FUNC]
            self._ui.actionFuncLabel.setText(
                actionDict[ActionEnum.OUTPUT_FUNC][ActionFuncEnum.NAME]
            )

        if ActionEnum.PERIOD in actionDict:
            self._ui.periodSpinBox.setValue(actionDict[ActionEnum.PERIOD])

        if ActionEnum.PARAMETER in actionDict:
            self._parameterModel.setValues(actionDict[ActionEnum.PARAMETER])
