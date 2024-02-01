from algoBuilder.core.configConstants import ACTION_LIST
from ..actionUIConstant import (
    ActionEnum,
    INVALID_ACTION_KEY,
    DataSetEnum,
)

from .. import parameterTable
from . import feedView

from .qtUiFiles import ui_actionListCreator

from ...core.configConstants import (
    TYPE,
    CALC_FUNC,
    PERIOD,
    INPUT_COLS,
)
from ...commonUtil import helpers
from dataclasses import dataclass
import typing

from PySide2 import QtWidgets, QtCore

ADD_TEXT = "Add Action"
APPLY_TEXT = "Apply Action"
CANCEL_TEXT = "Cancel"
MODIFY_TEXT = "Modify"


@dataclass
class DataSourceInputSettings:
    pass


class ActionListCreator(QtWidgets.QWidget):
    """
    Widget for creating an action list

    Contains both the Feed View and the Action Creator
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        # Load UI file
        self._ui = ui_actionListCreator.Ui_ActionListCreator()
        self._ui.setupUi(self)

        self._modifyIndex = None

        self._ui.errorLabel.setStyleSheet("color: red;")

        # create models and delegates for feed
        self.feedModel = feedView.FeedTableModel()
        self._feedDelegate = feedView.FeedViewDelegate()
        self._ui.feedView.setModel(self.feedModel)
        self._ui.feedView.setItemDelegate(self._feedDelegate)

        # connect signal and slots
        self._ui.actionCreator.addAction.connect(self.checkActionValidity)
        self._ui.removeActionButton.pressed.connect(self.removeButtonPressed)
        self._ui.addActionButton.pressed.connect(self._ui.actionCreator.validateAction)
        self._ui.clearActionButton.pressed.connect(self.resetModifyStatus)
        self._ui.feedView.rightClickName.connect(self._ui.actionCreator.nameSelected)
        self._ui.modifyActionButton.pressed.connect(self.modifyActionPressed)

    @QtCore.Slot()
    def removeButtonPressed(self):
        for index in self.getFeedSelectedColumnIndex():
            self.feedModel.remove(index)

    def getFeedSelectedColumnIndex(self):
        indexes = self._ui.feedView.selectionModel().selectedIndexes()
        removedColumns = set()
        if indexes is not None:
            for index in indexes:
                if index.column() not in removedColumns:
                    removedColumns.add(index.column())
                    yield index

    def checkActionValidity(
        self,
        actionDict: typing.Dict[typing.Union[ActionEnum, str], typing.Any],
    ):
        if INVALID_ACTION_KEY in actionDict:
            # handle the error
            self._ui.errorLabel.setText(actionDict[INVALID_ACTION_KEY])
        else:
            self._ui.errorLabel.setText("")
            self.feedModel.insert(actionDict, self.feedModel.columnCount())

    def modifyActionPressed(self):
        if self._modifyIndex is None:
            # get the index to be modified and set it in the action creator
            indexGenerator = self.getFeedSelectedColumnIndex()
            if indexGenerator is not None:
                index = next(indexGenerator)
                if index.column() + 1 > self.feedModel.numDataSourceColumns:
                    actionDict = self.feedModel.columns[index.column()]
                    self._ui.actionCreator.modifyAction(actionDict)
                    self._modifyIndex = index

                    self._ui.modifyActionButton.setText(CANCEL_TEXT)
                    self._ui.addActionButton.setText(APPLY_TEXT)
        else:
            self.resetModifyStatus()

    def resetModifyStatus(self):
        self._modifyIndex = None
        self._ui.actionCreator.reset()
        self._ui.modifyActionButton.setText(MODIFY_TEXT)
        self._ui.addActionButton.setText(ADD_TEXT)

    def update(self) -> None:
        self.feedModel.beginResetModel()
        self.feedModel.endResetModel()
        self._ui.actionCreator._dataSetModel.beginResetModel()
        self._ui.actionCreator._dataSetModel.endResetModel()
        return super().update()

    def validate(self) -> bool:
        """Called by createActionListPage to see if there's a valid action list"""
        return True

    def getConfig(self) -> typing.Dict:
        """Called by createActionListPage to get the page config"""
        action_list_dict = {}
        for action in self.feedModel.getActionColumns():
            # translate the feed table to config
            try:
                action_config = {
                    TYPE: action[ActionEnum.TYPE],
                    CALC_FUNC: helpers.getConfigFromEnumDict(
                        action[ActionEnum.ACTION_FUNC]
                    ),
                    PERIOD: action[ActionEnum.PERIOD],
                }

                action_config |= parameterTable.convertToConfig(
                    action[ActionEnum.PARAMETER]
                )

                # input columns aren't stored in the way we want for the config
                sorted_input_col_list = sorted(
                    action[ActionEnum.INPUT],
                    key=lambda input_col: input_col[DataSetEnum.INDEX],
                )
                # now they're sorted by index
                input_col_dict = {}
                for input_col in sorted_input_col_list:
                    # if no mapping is present then just keep the name as the source
                    mapping = ""
                    if input_col[DataSetEnum.MAPPING]:
                        mapping = input_col[DataSetEnum.MAPPING]
                    else:
                        mapping = input_col[DataSetEnum.SOURCE]
                    input_col_dict[input_col[DataSetEnum.SOURCE]] = mapping
                action_config[INPUT_COLS] = input_col_dict
                # now the dict is complete pass in the action_config to the
                # action list dict with the name as the key
                action_list_dict[action[ActionEnum.NAME]] = action_config
            except KeyError:
                # an invalid action was returned from the feed
                # (this should never happen)
                pass
        return {ACTION_LIST: action_list_dict}
