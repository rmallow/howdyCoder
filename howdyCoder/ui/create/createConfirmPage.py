from ...core.dataStructs import ItemSettings
from .createBasePage import CreateBasePage, ItemValidity
from ..qtUiFiles import ui_createDataSourceConfirmPage
from ..uiConstants import PageKeys

import typing
import copy

from dataclass_wizard import asdict
from PySide6 import QtWidgets, QtCore
import yaml


class CreateConfirmPage(CreateBasePage):
    PAGE_KEY = PageKeys.CONFRIM
    TOP_TEXT = "The final config for your data source. Confirm to add or use the back buttons to go back and modify."
    TUTORIAL_RESOURCE_PREFIX = "CreateConfirm"

    def __init__(
        self,
        current_config: ItemSettings,
        parent: typing.Optional[QtWidgets.QWidget] = None,
    ):
        super().__init__(current_config, self.TUTORIAL_RESOURCE_PREFIX, parent=parent)

        self._ui = ui_createDataSourceConfirmPage.Ui_CreateDataSourceConfirmPage()
        self._ui.setupUi(self)
        self._ui.label.setText(self.TOP_TEXT)

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
