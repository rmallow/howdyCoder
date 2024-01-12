from ...core.dataStructs import AlgoSettings
from .createBasePage import CreateBasePage, ItemValidity
from ..qtUiFiles import ui_createDataSourceConfirmPage
from ..uiConstants import PageKeys

from ...core.commonGlobals import DATA_SOURCES, ACTION_LIST, NONE_GROUP

import typing
import copy

from dataclass_wizard import asdict
from PySide6 import QtWidgets, QtCore
import yaml


class CreateConfirmBasePage(CreateBasePage):
    def __init__(
        self,
        current_config: AlgoSettings,
        top_text: str,
        resouce_prefix: str,
        parent: typing.Optional[QtWidgets.QWidget] = None,
    ):
        super().__init__(current_config, resouce_prefix, parent=parent)

        self._ui = ui_createDataSourceConfirmPage.Ui_CreateDataSourceConfirmPage()
        self._ui.setupUi(self)
        self._ui.label.setText(top_text)

    def getConfigForView(self):
        return {self.getConfig().name: asdict(self.getConfig())}

    def loadPage(self) -> None:
        """
        We want the confirm page to only show the section we've been working on.
        """
        super().loadPage()

        self._ui.configTextView.setPlainText(
            yaml.dump(self.getConfigForView(), default_flow_style=False, indent=4)
        )

    def save(self) -> None:
        # saving of the temp config to the full config is done via the confirm button
        pass

    def getTutorialClasses(self) -> typing.List:
        return [self]


class CreateDataSourceConfirmPage(CreateConfirmBasePage):
    PAGE_KEY = PageKeys.CONFRIM_DATA_SOURCE
    TOP_TEXT = "The final config for your data source. Confirm to add or use the back buttons to go back and modify."
    GROUP = DATA_SOURCES
    TUTORIAL_RESOURCE_PREFIX = "CreateConfirm"

    def __init__(
        self,
        current_config: AlgoSettings,
        parent: typing.Optional[QtWidgets.QWidget] = None,
    ):
        super().__init__(
            current_config, self.TOP_TEXT, self.TUTORIAL_RESOURCE_PREFIX, parent
        )


class CreateActionConfirmPage(CreateConfirmBasePage):
    PAGE_KEY = PageKeys.CONFIRM_ACTION
    TOP_TEXT = "The final config for your action. Confirm to add or use the back buttons to go back and modify."
    GROUP = ACTION_LIST
    TUTORIAL_RESOURCE_PREFIX = "CreateConfirm"

    def __init__(
        self,
        current_config: AlgoSettings,
        parent: typing.Optional[QtWidgets.QWidget] = None,
    ):
        super().__init__(
            current_config, self.TOP_TEXT, self.TUTORIAL_RESOURCE_PREFIX, parent
        )


class CreateFinalConfirmPage(CreateConfirmBasePage):
    PAGE_KEY = PageKeys.FINAL_CONFIRM
    EXIT = PageKeys.NO_PAGE
    EXIT_LABEL = "Exit Creator"
    TOP_TEXT = "The final config for the algo. Select start over to erase your create or click finish to add this algo to the control page."
    GROUP = NONE_GROUP
    TUTORIAL_RESOURCE_PREFIX = "CreateFinalConfirm"

    def __init__(
        self,
        current_config: AlgoSettings,
        parent: typing.Optional[QtWidgets.QWidget] = None,
    ):
        super().__init__(
            current_config, self.TOP_TEXT, self.TUTORIAL_RESOURCE_PREFIX, parent
        )
        # there's no confirm/add another next is finish and back is start over
        self.back_enabled = False
        self._ui.buttonWidget.hide()

    def getConfigForView(self):
        return {self.getConfig().name: asdict(self.getConfig())}
