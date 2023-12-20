from ...core.dataStructs import ActionSettings, AlgoSettings, DataSourceSettings
from .createBasePage import CreateBasePage, ItemValidity
from ..qtUiFiles import ui_createDataSourceParametersPage
from ..uiConstants import PageKeys
from . import parameterTable
from ..util import qtResourceManager

from ...core.commonGlobals import (
    DATA_SOURCES,
    ACTION_LIST,
    NONE_GROUP,
    DataSourcesTypeEnum,
    ActionTypeEnum,
    ENUM_DISPLAY,
    DATA_SET,
)

import typing
from ...commonUtil import helpers

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
        self._parameterModel.dataChanged.connect(self.setParametersLabel)
        self._ui.clearParameterButton.pressed.connect(self._parameterModel.clear)
        self._ui.single_shot_check.stateChanged.connect(self.singleShotStateChanged)

    @QtCore.Slot()
    def singleShotStateChanged(self, _):
        self._ui.time_edit.setEnabled(not self._ui.single_shot_check.isChecked())

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
            self._parameterModel.getData(curr)
            curr.flatten = self._ui.flattenedCheck.isChecked()
            curr.period = max(
                1, QtCore.QTime(0, 0, 0).secsTo(self._ui.time_edit.time())
            )
            curr.single_shot = self._ui.single_shot_check.isChecked()

    def reset(self) -> None:
        self._parameterModel.clear()
        self._ui.time_edit.setTime(QtCore.QTime(0, 0, 1))
        self._ui.flattenedCheck.setChecked(True)
        self._ui.single_shot_check.setChecked(False)

    def loadPage(self) -> None:
        curr = self.getTempConfig()
        self._ui.time_edit.setTime(QtCore.QTime(0, 0, 0).addSecs(curr.period))
        self._ui.flattenedCheck.setChecked(curr.flatten)
        self._ui.single_shot_check.setChecked(curr.single_shot)
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

    def loadPage(self):
        super().loadPage()
        if self.getTempConfig().type_ == getattr(
            DataSourcesTypeEnum.INPUT, ENUM_DISPLAY, ""
        ):
            self._ui.period_and_flatten_box.hide()
        else:
            self._ui.period_and_flatten_box.show()


class CreateActionParametersPage(CreateBaseParametersPage):
    PAGE_KEY = PageKeys.ACTION_PARAMETERS
    # no text for action as period is determined on settings page per input
    # and single shot doesn't apply
    ACTION_TEXT = """"""

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
        self._ui.periodWidgetBox.hide()

    def loadPage(self) -> None:
        if self.getTempConfig().type_ == getattr(
            ActionTypeEnum.TRIGGER, ENUM_DISPLAY, ""
        ):
            self._ui.period_and_flatten_box.hide()
        else:
            self._ui.period_and_flatten_box.show()
        return super().loadPage()


class CreateScriptParametersPage(CreateBaseParametersPage):
    PAGE_KEY = PageKeys.SCRIPT_PARAMETERS
    SCRIPT_TEXT = """Set how often you'd like this to script in the period section or set single shot if you want it to run only once."""

    TUTORIAL_RESOURCE_PREFIX = "test"
    GROUP = NONE_GROUP

    def __init__(
        self,
        current_config: AlgoSettings,
        parent: typing.Optional[QtWidgets.QWidget] = None,
    ):
        super().__init__(
            current_config,
            self.SCRIPT_TEXT,
            self.TUTORIAL_RESOURCE_PREFIX,
            parent=parent,
        )
        self._ui.flattenWidgetBox.hide()

    def getTempConfig(self) -> ActionSettings:
        return self.getConfig().action
