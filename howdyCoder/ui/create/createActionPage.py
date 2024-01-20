from ...core.dataStructs import ActionSettings, ItemSettings
from .createBasePage import CreateBasePage, ItemValidity
from ..uiConstants import PageKeys
from ..qtUiFiles import ui_createActionPage


from ...core.commonGlobals import (
    ActionTypeEnum,
)
import typing

from PySide6 import QtWidgets, QtGui, QtCore


class CreateActionPage(CreateBasePage):
    PAGE_KEY = PageKeys.ACTION

    def __init__(
        self,
        current_config: ItemSettings,
        parent: typing.Optional[QtWidgets.QWidget] = None,
    ):
        super().__init__(current_config, "None", parent=parent)

        self._ui = ui_createActionPage.Ui_CreateActionPage()
        self._ui.setupUi(self)
        self._action_type = None

        for x in range(self._ui.stacked_widget.count()):
            self._ui.stacked_widget.widget(x).parent_page = self

    def loadPage(self) -> None:
        super().loadPage()
        curr_settings: ActionSettings = self.getConfig()
        if curr_settings.type_:
            enum_type = ActionTypeEnum(curr_settings.type_)
            self._action_type = enum_type
            if (
                self._action_type == ActionTypeEnum.EVENT
                or self._action_type == ActionTypeEnum.TRIGGER
            ):
                self._ui.stacked_widget.setCurrentWidget(
                    self._ui.create_function_action
                )
        self._ui.stacked_widget.currentWidget().loadPage()

    def validate(self) -> typing.Dict[QtWidgets.QWidget | str, ItemValidity]:
        return self._ui.stacked_widget.currentWidget().validate()

    def reset(self) -> None:
        self._ui.stacked_widget.currentWidget().reset()

    def save(self) -> None:
        self._ui.stacked_widget.currentWidget().save()

    def getTutorialClasses(self) -> typing.List:
        return self._ui.stacked_widget.currentWidget().getTutorialClasses()
