from ...core.dataStructs import ActionSettings, AlgoSettings, DataSourceSettings
from .createBasePage import CreateBasePage
from ..qtUiFiles import ui_createDataSourceParametersPage
from ..uiConstants import PageKeys
from . import parameterTable
from ..util import qtResourceManager

from ...core.commonGlobals import (
    DATA_SOURCES,
    ACTION_LIST,
    NONE_GROUP,
    DataSourcesTypeEnum,
    ENUM_DISPLAY,
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
        self._parameterModel.dataChanged.connect(self.checkParameterNames)
        self._ui.clearParameterButton.pressed.connect(self._parameterModel.clear)
        self._ui.single_shot_check.stateChanged.connect(self.singleShotStateChanged)

    @QtCore.Slot()
    def singleShotStateChanged(self, _):
        self._ui.time_edit.setEnabled(not self._ui.single_shot_check.isChecked())

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
            self._parameterModel.getData(curr)
            curr.flatten = self._ui.flattenedCheck.isChecked()

    def reset(self) -> None:
        self._parameterModel.clear()
        self._ui.time_edit.setTime(QtCore.QTime(0, 0, 1))
        self._ui.flattenedCheck.setChecked(True)
        self._ui.single_shot_check.setChecked(False)

    def loadPage(self) -> None:
        curr = self.getTempConfig()
        time = QtCore.QTime()
        time.addSecs(curr.period)
        self._ui.time_edit.setTime(time)
        self._ui.flattenedCheck.setChecked(curr.flatten)
        self._ui.single_shot_check.setChecked(curr.single_shot)
        self.setParametersLabel()
        return super().loadPage()

    def setParametersLabel(self):
        helper_data = self.getHelperData()
        self._ui.parameter_list_widget.clear()
        for param in helper_data.suggested_parameters:
            icon = qtResourceManager.getResourceByName(
                "icons",
                (
                    "checkmark_green.png"
                    if param in self._parameterModel.current_names
                    else "x_red.png"
                ),
            )
            self._ui.parameter_list_widget.addItem(
                QtWidgets.QListWidgetItem(icon, param)
            )

    def getTutorialClasses(self) -> typing.List:
        return [self]

    def checkParameterNames(self):
        for x in range(self._ui.parameter_list_widget.count()):
            self._ui.parameter_list_widget.item(x).setIcon(
                qtResourceManager.getResourceByName(
                    "icons",
                    (
                        "checkmark_green.png"
                        if self._ui.parameter_list_widget.item(x).text()
                        in self._parameterModel.current_names
                        else "x_red.png"
                    ),
                )
            )


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
            self._ui.flattenWidgetBox.hide()
            self._ui.periodWidgetBox.hide()
        else:
            self._ui.flattenWidgetBox.show()
            self._ui.periodWidgetBox.show()

    def save(self):
        super().save()
        curr: DataSourceSettings = self.getTempConfig()
        curr.period = max(1, QtCore.QTime(0, 0, 0).secsTo(self._ui.time_edit.time()))
        curr.single_shot = self._ui.single_shot_check.isChecked()


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
