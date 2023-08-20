from .createBasePage import CreateBasePage
from ..qtUiFiles import ui_createDataSourceConfirmPage
from ..uiConstants import PageKeys

import typing

from PySide6 import QtWidgets, QtCore
import yaml


class CreateConfirmBasePage(CreateBasePage):
    def __init__(
        self,
        current_config: typing.Dict[str, typing.Any],
        top_text: str,
        add_start_page: PageKeys,
        parent: typing.Optional[QtWidgets.QWidget] = None,
    ):
        super().__init__(current_config, "test", parent=parent)

        self._ui = ui_createDataSourceConfirmPage.Ui_CreateDataSourceConfirmPage()
        self._ui.setupUi(self)
        self._ui.label.setText(top_text)
        self.add_start_page = add_start_page
        self.next_enabled = False

        self._ui.addButton.released.connect(lambda: self.manualExit.emit(self.EXIT))
        self._ui.confirmButton.released.connect(self.confirmConfig)

    @QtCore.Slot()
    def confirmConfig(self) -> None:
        # add temp config to full config, enable next and disable back
        self.getConfigSection().update(self.getTempConfig())
        self.getTempConfig().clear()
        self.enableNext.emit(True)
        self.enableBack.emit(False)
        self._ui.confirmButton.setEnabled(False)

    def getConfig(self, keys: typing.List[str]):
        def helper(i, curr):
            """For each key in keys go one level deeper in the dict, add the full config section at the end"""
            if i >= len(keys):
                return self.getTempConfig()
            curr[keys[i]] = helper(i + 1, {})
            return curr

        return helper(0, {})

    def loadPage(self, keys: typing.List[str]) -> None:
        """
        We want the confirm page to only show the section we've been working on.
        This is based on the passed in keys.
        We do this using the helper function below
        """
        super().loadPage(keys)

        self._ui.configTextView.setPlainText(
            yaml.dump(self.getConfig(keys), default_flow_style=False, indent=4)
        )

    def validate(self) -> bool:
        return True

    def reset(self) -> None:
        self._ui.addButton.setEnabled(True)
        self._ui.confirmButton.setEnabled(True)

    def save(self) -> None:
        # saving of the temp config to the full config is done via the confirm button
        pass

    def getKeysForNextPage(self) -> typing.Any:
        return [self.config_keys[0]]

    def getTutorialClasses(self) -> typing.List:
        return [self]


class CreateDataSourceConfirmPage(CreateConfirmBasePage):
    PAGE_KEY = PageKeys.CONFRIM_DATA_SOURCE
    TOP_TEXT = "The final config for your data source. Confirm to add or use the back buttons to go back and modify."

    def __init__(
        self,
        current_config: typing.Dict[str, typing.Any],
        parent: typing.Optional[QtWidgets.QWidget] = None,
    ):
        super().__init__(current_config, self.TOP_TEXT, parent)


class CreateActionConfirmPage(CreateConfirmBasePage):
    PAGE_KEY = PageKeys.CONFIRM_ACTION
    TOP_TEXT = "The final config for your action. Confirm to add or use the back buttons to go back and modify."

    def __init__(
        self,
        current_config: typing.Dict[str, typing.Any],
        parent: typing.Optional[QtWidgets.QWidget] = None,
    ):
        super().__init__(current_config, self.TOP_TEXT, parent)


class CreateFinalConfirmPage(CreateConfirmBasePage):
    PAGE_KEY = PageKeys.FINAL_CONFIRM
    EXIT = PageKeys.NO_PAGE
    EXIT_LABEL = "Exit Creator"
    TOP_TEXT = "The final config for the algo. Select start over to erase your create or click finish to add this algo to the control page."

    def __init__(
        self,
        current_config: typing.Dict[str, typing.Any],
        parent: typing.Optional[QtWidgets.QWidget] = None,
    ):
        super().__init__(current_config, self.TOP_TEXT, parent)
        # there's no confirm/add another next is finish and back is start over
        self.next_enabled = True
        self.back_enabled = False
        self._ui.addButton.setEnabled(False)
        self._ui.confirmButton.setEnabled(False)
        self._ui.buttonWidget.hide()

    def getConfig(self, keys: typing.List[str]):
        return self.current_config
