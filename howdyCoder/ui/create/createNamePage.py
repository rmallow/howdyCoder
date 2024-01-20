from ...core.dataStructs import ItemSettings
from .createBasePage import CreateBasePage, ItemValidity
from ..uiConstants import PageKeys
from ..qtUiFiles import ui_createNamePage


import typing

from PySide6 import QtWidgets, QtCore

LABEL_TEXT_LEFT = "Enter a name for the "
LABEL_TEXT_RIGHT = " for reference"


class CreateNamePage(CreateBasePage):
    PAGE_KEY = PageKeys.NAME

    TUTORIAL_RESOURCE_PREFIX = "None"

    def __init__(
        self,
        current_config: ItemSettings,
        parent: typing.Optional[QtWidgets.QWidget] = None,
    ):
        super().__init__(current_config, self.TUTORIAL_RESOURCE_PREFIX, parent=parent)

        self._ui = ui_createNamePage.Ui_CreateNamePage()
        self._ui.setupUi(self)
        self._last_name = ""

    def validate(self) -> typing.Dict[QtWidgets.QWidget | str, ItemValidity]:
        """Check if the name is entered and valid, if it is then check if it exists in the configs already"""
        return {
            self._ui.nameEdit: ItemValidity.getEnum(
                self.validateText(self._ui.nameEdit.text())
            )
        }

    def save(self) -> None:
        """Replace the name in the settings"""
        self.getConfig().name = self._ui.nameEdit.text().strip()

    def reset(self) -> None:
        self._ui.label.setText(
            f"{LABEL_TEXT_LEFT}{self.creator_type.value}{LABEL_TEXT_RIGHT}"
        )
        self._ui.nameEdit.clear()

    def loadPage(self) -> None:
        self._ui.label.setText(
            f"{LABEL_TEXT_LEFT}{self.creator_type.value}{LABEL_TEXT_RIGHT}"
        )
        self._ui.nameEdit.setText(self.getConfig().name)
        return super().loadPage()

    def getTutorialClasses(self) -> typing.List:
        return [self]
