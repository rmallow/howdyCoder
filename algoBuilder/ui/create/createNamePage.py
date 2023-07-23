from .createBasePage import CreateBasePage
from ..uiConstants import PageKeys
from ..qtUiFiles import ui_createNamePage

import typing

from PySide6 import QtWidgets, QtCore


class CreateNamePage(CreateBasePage):
    PAGE_KEY = PageKeys.NAME
    EXIT = PageKeys.NO_PAGE
    EXIT_LABEL = "Exit Creator"

    doesAlgoNameExist = QtCore.Signal(str)

    def __init__(
        self,
        current_config: typing.Dict[str, typing.Any],
        parent: typing.Optional[QtWidgets.QWidget] = None,
    ):
        super().__init__(current_config, parent=parent)

        self.next_enabled = False
        self._ui = ui_createNamePage.Ui_CreateNamePage()
        self._ui.setupUi(self)
        self._last_name = ""

        self._ui.nameEdit.textChanged.connect(self.validate)

    def validate(self) -> bool:
        """Check if the name is entered and valid, if it is then check if it exists in the configs already"""
        if self._ui.nameEdit.text().strip() != self._last_name and self.validateText(
            self._ui.nameEdit.text()
        ):
            self._last_name = self._ui.nameEdit.text().strip()
            self.doesAlgoNameExist.emit(self._last_name)
        return True

    def save(self) -> None:
        """We don't want to keep adding keys to the dict so make sure there is only one"""
        old_value = {}
        if len(self.current_config):
            old_value = self.current_config[next(iter(self.current_config.keys()))]
            # clear out the config just to be safe
            self.current_config.clear()
        self.current_config[self._ui.nameEdit.text().strip()] = old_value

    def getKeysForNextPage(self) -> typing.Any:
        return [next(iter(self.current_config.keys()))]

    def reset(self) -> None:
        self.next_enabled = False
        self._ui.nameEdit.clear()

    def loadPage(self, keys: typing.List[str]) -> None:
        return super().loadPage(keys)

    @QtCore.Slot()
    def doesNameExistSlot(self, exists_already: bool) -> None:
        self.next_enabled = not exists_already
        self.enableNext.emit(self.next_enabled)
