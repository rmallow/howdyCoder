from ...core.dataStructs import ScriptSettings, ActionSettings
from .createBasePage import CreateBasePage, ItemValidity
from ..uiConstants import PageKeys
from ..qtUiFiles.ui_createScriptPage import Ui_CreateScriptPage
from ..funcSelector import FunctionSettingsWithHelperData


import typing
import copy

from dataclass_wizard import asdict
from PySide6 import QtWidgets, QtCore


class CreateScriptPage(CreateBasePage):
    PAGE_KEY = PageKeys.SCRIPT
    EXIT = PageKeys.NAME

    TUTORIAL_RESOURCE_PREFIX = "test"

    def __init__(
        self,
        current_config: ScriptSettings,
        parent: typing.Optional[QtWidgets.QWidget] = None,
    ):
        super().__init__(current_config, self.TUTORIAL_RESOURCE_PREFIX, parent=parent)
        self._ui = Ui_CreateScriptPage()
        self._ui.setupUi(self)
        self._ui.funcSelectorWidget.embedded = True

        self._current_settings: FunctionSettingsWithHelperData = None
        self._ui.funcSelectorWidget.itemSelected.connect(self.settingsSelected)
        self._ui.funcSelectorWidget.setDefaultPrompt("Script")

    def loadPage(self):
        curr: ActionSettings = self.getConfig()
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
        self.getConfig().calc_function = self._current_settings.function_settings

    def settingsSelected(self, function_settings: FunctionSettingsWithHelperData):
        self._current_settings = function_settings

    def reset(self) -> None:
        self._current_settings = None
