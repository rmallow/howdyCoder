from ...core.dataStructs import ScriptSettings, ActionSettings
from .createBasePage import CreateBasePage, ItemValidity
from ..uiConstants import PageKeys
from ..qtUiFiles.ui_createScriptSettingsPage import Ui_CreateScriptSettingsPage
from ..funcSelector import FunctionSettingsWithHelperData, addHelperData

from ...core.commonGlobals import NONE_GROUP, ActionTypeEnum, ENUM_DISPLAY

import typing
import copy

from dataclass_wizard import asdict
from PySide6 import QtWidgets, QtCore


class CreateScriptSettingsPage(CreateBasePage):
    PAGE_KEY = PageKeys.SCRIPT_SETTINGS
    EXIT = PageKeys.NAME
    EXIT_LABEL = "Exit Script Creator"

    TUTORIAL_RESOURCE_PREFIX = "test"

    GROUP = NONE_GROUP

    def __init__(
        self,
        current_config: ScriptSettings,
        parent: typing.Optional[QtWidgets.QWidget] = None,
    ):
        super().__init__(current_config, self.TUTORIAL_RESOURCE_PREFIX, parent=parent)
        self._ui = Ui_CreateScriptSettingsPage()
        self._ui.setupUi(self)
        self._ui.funcSelectorWidget.embedded = True

        self._current_settings: FunctionSettingsWithHelperData = None
        self._ui.funcSelectorWidget.itemSelected.connect(self.settingsSelected)
        self._ui.funcSelectorWidget.setDefaultPrompt("Script")

    def loadPage(self):
        curr: ActionSettings = self.getConfig().action
        if curr is not None:
            self._ui.funcSelectorWidget.updateChildData()
            self._ui.funcSelectorWidget.setData(curr.calc_function)

    def getTutorialClasses(self) -> typing.List:
        return [self] + self._ui.funcSelectorWidget.getTutorialClasses()

    def validate(self) -> typing.Dict[QtWidgets.QWidget | str, ItemValidity]:
        return {
            self._ui.funcSelectorWidget: ItemValidity.getEnum(
                self._current_settings is not None
            )
        }

    def save(self) -> None:
        self.getHelperData().suggested_parameters = (
            self._current_settings.suggested_parameters
        )
        if self.getConfig().action is None:
            self.getConfig().action = ActionSettings(
                getattr(ActionTypeEnum.SCRIPT, ENUM_DISPLAY),
                getattr(ActionTypeEnum.SCRIPT, ENUM_DISPLAY),
            )
        self.getConfig().action.calc_function = self._current_settings.function_settings

    def settingsSelected(self, function_settings: FunctionSettingsWithHelperData):
        self._current_settings = function_settings

    def reset(self) -> None:
        self._current_settings = None
