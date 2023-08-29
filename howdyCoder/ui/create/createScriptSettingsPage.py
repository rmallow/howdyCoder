from ...core.dataStructs import ScriptSettings
from .createBasePage import CreateBasePage
from ..qtUiFiles import ui_createDataSourceConfirmPage
from ..uiConstants import PageKeys
from ..qtUiFiles.ui_createScriptSettingsPage import Ui_CreateScriptSettingsPage

from ...core.commonGlobals import NONE_GROUP

import typing
import copy

from dataclass_wizard import asdict
from PySide6 import QtWidgets, QtCore


class CreateScriptSettingsPage(CreateBasePage):
    PAGE_KEY = PageKeys.SCRIPT_SETTINGS
    EXIT = PageKeys.NO_PAGE
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

    def loadPage(self):
        pass

    def getTutorialClasses(self) -> typing.List:
        return [self]

    def validate(self) -> bool:
        return True

    def save(self) -> None:
        pass

    def reset(self) -> None:
        pass
