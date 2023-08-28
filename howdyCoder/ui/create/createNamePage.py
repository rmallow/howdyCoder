from .createBasePage import CreateBasePage
from ..uiConstants import PageKeys
from ..qtUiFiles import ui_createNamePage

from ...core.commonGlobals import AlgoSettings, NONE_GROUP

import typing

from PySide6 import QtWidgets, QtCore


class CreateNamePage(CreateBasePage):
    PAGE_KEY = PageKeys.NAME
    EXIT = PageKeys.NO_PAGE
    EXIT_LABEL = "Exit Creator"

    TUTORIAL_RESOURCE_PREFIX = "None"

    GROUP = NONE_GROUP

    doesAlgoNameExist = QtCore.Signal(str)

    def __init__(
        self,
        current_config: AlgoSettings,
        parent: typing.Optional[QtWidgets.QWidget] = None,
    ):
        super().__init__(current_config, self.TUTORIAL_RESOURCE_PREFIX, parent=parent)

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
        """Replace the name in the settings"""
        self.getConfig().name = self._ui.nameEdit.text().strip()

    def reset(self) -> None:
        self.next_enabled = False
        self._ui.nameEdit.clear()

    def loadPage(self) -> None:
        return super().loadPage()

    @QtCore.Slot()
    def doesNameExistSlot(self, exists_already: bool) -> None:
        self.next_enabled = not exists_already
        self.enableNext.emit(self.next_enabled)

    def getTutorialClasses(self) -> typing.List:
        return [self]
