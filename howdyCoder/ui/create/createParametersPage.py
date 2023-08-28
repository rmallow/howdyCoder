from .createBasePage import CreateBasePage
from ..qtUiFiles import ui_createDataSourceParametersPage
from ..uiConstants import PageKeys
from . import parameterTable

from ...core.configConstants import PERIOD, FLATTEN, SINGLE_SHOT

from ...core.commonGlobals import (
    AlgoSettings,
    DATA_SOURCES,
    ACTION_LIST,
    DataSourceSettings,
    ActionSettings,
)

import typing

from PySide6 import QtWidgets, QtCore


class CreateBaseParametersPage(CreateBasePage):
    def __init__(
        self,
        current_config: AlgoSettings,
        period_text: str,
        resource_preifx: str,
        parent: typing.Optional[QtWidgets.QWidget] = None,
    ):
        super().__init__(current_config, resource_preifx, parent=parent)

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
        self._ui.single_shot_check.stateChanged.connect(self.singleShotStateChanged)

    @QtCore.Slot()
    def singleShotStateChanged(self, _):
        self._ui.periodSpinBox.setEnabled(not self._ui.single_shot_check.isChecked())

    def validate(self) -> bool:
        return True

    def save(self) -> None:
        """
        Checking if temp config exists gets around an issue with exiting from a section
        If exit is hit, it will try to save the parameters page, this is becuase the parameters page
        at the time of writing this is ALWAYS valid even without input. Issue is temp config has been reset
        when we exit, so when the save is called on this page (because it's technically valid) it throws
        an error trying to save to a temp config that doesn't exist
        """
        if self.getTempConfig():
            curr = self.getTempConfig()
            parameterTable.addToConfig(curr, self._parameterModel.getData())
            curr.flatten = self._ui.flattenedCheck.isChecked()

    def reset(self) -> None:
        self._parameterModel.clear()
        self._ui.periodSpinBox.setValue(1)
        self._ui.flattenedCheck.setChecked(True)
        self._ui.single_shot_check.setChecked(False)

    def loadPage(self) -> None:
        curr = self.getTempConfig()
        self._ui.periodSpinBox.setValue(curr.period)
        self._ui.flattenedCheck.setChecked(curr.flatten)
        self._ui.single_shot_check.setChecked(curr.single_shot)
        return super().loadPage()

    def getTutorialClasses(self) -> typing.List:
        return [self]


class CreateDataSourceParametersPage(CreateBaseParametersPage):
    PAGE_KEY = PageKeys.DATA_SOURCE_PARAMETERS
    DATA_SOURCE_TEXT = "Set the period for the data source. The period is how often the data source will query the input.  IE if it is a stream data source, it will call the API URL every period number of seconds. Or set singleshot which will make the data source run only once, regardless of period."
    TUTORIAL_RESOURCE_PREFIX = "CreateParameterDataSource"
    GROUP = DATA_SOURCES

    def __init__(
        self,
        current_config: AlgoSettings,
        parent: typing.Optional[QtWidgets.QWidget] = None,
    ):
        super().__init__(
            current_config,
            self.DATA_SOURCE_TEXT,
            self.TUTORIAL_RESOURCE_PREFIX,
            parent=parent,
        )

    def save(self):
        super().save()
        curr: DataSourceSettings = self.getTempConfig()
        curr.period = self._ui.periodSpinBox.value()
        curr.single_shot = self._ui.single_shot_check.isChecked()


class CreateActionParametersPage(CreateBaseParametersPage):
    PAGE_KEY = PageKeys.ACTION_PARAMETERS
    ACTION_TEXT = """Set the period for the action. 
    This determines how much data will be pulled in for the calculating function.
    For example if the calcuating function detrmines an average and the period is set to 5, then it will be performing an average of the last 5 pieces of data in the input."""

    TUTORIAL_RESOURCE_PREFIX = "CreateParameterAction"
    GROUP = ACTION_LIST

    def __init__(
        self,
        current_config: AlgoSettings,
        parent: typing.Optional[QtWidgets.QWidget] = None,
    ):
        super().__init__(
            current_config,
            self.ACTION_TEXT,
            self.TUTORIAL_RESOURCE_PREFIX,
            parent=parent,
        )
        policy = self._ui.periodWidgetBox.sizePolicy()
        policy.setHorizontalStretch(
            self._ui.flattenWidgetBox.sizePolicy().horizontalStretch()
        )
        self._ui.periodWidgetBox.setSizePolicy(policy)
        self._ui.single_shot_check.hide()
