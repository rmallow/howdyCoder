from ...core.dataStructs import ItemSettings
from .createBasePage import CreateBasePage, ItemValidity
from ..qtUiFiles import ui_createDataSourceParametersPage
from ..uiConstants import PageKeys
from .. import parameterTable

from ...core.commonGlobals import (
    DATA_SOURCES,
    ACTION_LIST,
    DATA_SET,
)

import typing
from ...commonUtil import helpers

from PySide6 import QtWidgets, QtCore


class CreateParametersPage(CreateBasePage):
    PAGE_KEY = PageKeys.PARAMETERS

    def __init__(
        self,
        current_config: ItemSettings,
        parent: typing.Optional[QtWidgets.QWidget] = None,
    ):
        super().__init__(current_config, "None", parent=parent)

        self._ui = ui_createDataSourceParametersPage.Ui_CreateDataSourceParametersPage()
        self._ui.setupUi(self)

        self._parameterModel = parameterTable.ParameterTableModel()
        self._ui.parameterView.setModel(self._parameterModel)

        # parameter connections
        self._ui.addParameterButton.pressed.connect(self._parameterModel.appendValue)
        self._ui.removeParameterButton.pressed.connect(
            lambda: self._parameterModel.removeValue(
                self._ui.parameterView.getSelected()
            )
        )
        self._parameterModel.dataChanged.connect(self.setParametersLabel)
        self._ui.clearParameterButton.pressed.connect(self._parameterModel.clear)

    def save(self) -> None:
        """
        Checking if temp config exists gets around an issue with exiting from a section
        If exit is hit, it will try to save the parameters page, this is becuase the parameters page
        at the time of writing this is ALWAYS valid even without input. Issue is temp config has been reset
        when we exit, so when the save is called on this page (because it's technically valid) it throws
        an error trying to save to a temp config that doesn't exist
        """
        if self.getConfig():
            curr = self.getConfig()
            self._parameterModel.getData(curr)

    def reset(self) -> None:
        self._parameterModel.clear()

    def loadPage(self) -> None:
        curr = self.getConfig()
        self._parameterModel.clear()
        self._parameterModel.setDataFromSettings(curr)
        self.setParametersLabel()
        return super().loadPage()

    def setParametersLabel(self, *args, **kwrags):
        suggested_parmesean = [
            param
            for param in self.getHelperData().suggested_parameters
            + self._parameterModel.getSuggestedParameters()
            if param != DATA_SET
        ]
        self.addToSuggestedListWidget(
            self._ui.parameter_list_widget,
            self._parameterModel.current_names,
            suggested_parmesean,
        )
        self._ui.parameterView.itemDelegate().setCompleterStrings(suggested_parmesean)

    def getTutorialClasses(self) -> typing.List:
        return [self]

    def validate(self) -> typing.Dict[QtWidgets.QWidget | str, ItemValidity]:
        return {
            "Some suggested parameters have not been added.": self.suggested_validity,
        }
