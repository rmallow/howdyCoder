from .createBasePage import CreateBasePage
from ..qtUiFiles import ui_createDataSourceParametersPage
from ..uiConstants import PageKeys
from . import parameterTable

from ...core.configConstants import PERIOD, FLATTEN

import typing

from PySide2 import QtWidgets


class CreateBaseParametersPage(CreateBasePage):
    def __init__(
        self,
        current_config: typing.Dict[str, typing.Any],
        period_text: str,
        parent: typing.Optional[QtWidgets.QWidget] = None,
    ):
        super().__init__(current_config, parent=parent)

        self._ui = ui_createDataSourceParametersPage.Ui_CreateDataSourceParametersPage()
        self._ui.setupUi(self)
        self._ui.periodLabel.setText(period_text)

        self._parameterModel = parameterTable.ParameterTableModel()
        self._ui.parameterView.setModel(self._parameterModel)

        # parameter connections
        self._ui.addParameterButton.pressed.connect(self._parameterModel.appendValue)
        self._ui.removeParameterButton.pressed.connect(
            lambda: self._parameterModel.removeValue(
                self._ui.parameterView.getSelected()
            )
        )
        self._ui.clearParameterButton.pressed.connect(self._parameterModel.clear)

    def validate(self) -> bool:
        return True

    def save(self) -> None:
        curr = self.getTempConfigFirstValue()
        curr |= parameterTable.convertToConfig(self._parameterModel.getData())
        curr[PERIOD] = self._ui.periodSpinBox.value()
        curr[FLATTEN] = self._ui.flattenedCheck.isChecked()

    def reset(self) -> None:
        self._parameterModel.clear()
        self._ui.periodSpinBox.setValue(1)
        self._ui.flattenedCheck.setChecked(True)


class CreateDataSourceParametersPage(CreateBaseParametersPage):
    PAGE_KEY = PageKeys.DATA_SOURCE_PARAMETERS
    DATA_SOURCE_TEXT = "Set the period for the data source. The period is how often the data source will query the input.  IE if it is a stream data source, it will call the API URL every period number of seconds."

    def __init__(
        self,
        current_config: typing.Dict[str, typing.Any],
        parent: typing.Optional[QtWidgets.QWidget] = None,
    ):
        super().__init__(current_config, self.DATA_SOURCE_TEXT, parent=parent)


class CreateActionParametersPage(CreateBaseParametersPage):
    PAGE_KEY = PageKeys.ACTION_PARAMETERS
    ACTION_TEXT = """Set the period for the action. 
    This determines how much data will be pulled in for the calculating function.
    For example if the calcuating function detrmines an average and the period is set to 5, then it will be performing an average of the last 5 pieces of data in the input."""

    def __init__(
        self,
        current_config: typing.Dict[str, typing.Any],
        parent: typing.Optional[QtWidgets.QWidget] = None,
    ):
        super().__init__(current_config, self.ACTION_TEXT, parent=parent)
