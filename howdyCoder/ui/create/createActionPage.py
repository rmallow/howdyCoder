from ...core.dataStructs import ActionSettings, ItemSettings
from .createBasePage import PagePassThrough, ItemValidity
from ..uiConstants import PageKeys
from ..qtUiFiles import ui_createActionPage


from ...core.commonGlobals import (
    ActionTypeEnum,
)
import typing

from PySide6 import QtWidgets, QtGui, QtCore


class CreateActionPage(PagePassThrough):
    PAGE_KEY = PageKeys.ACTION

    def __init__(
        self,
        current_config: ItemSettings,
        parent: typing.Optional[QtWidgets.QWidget] = None,
    ):
        super().__init__(
            current_config,
            "None",
            parent=parent,
        )

        self._ui = ui_createActionPage.Ui_CreateActionPage()
        self._ui.setupUi(self)
        self.stacked_widget = self._ui.stacked_widget

        for x in range(self._ui.stacked_widget.count()):
            self._ui.stacked_widget.widget(x).parent_page = self

    def getWidgetForStack(self):
        curr_settings: ActionSettings = self.getConfig()
        return_widget = None
        if curr_settings.type_:
            enum_type = ActionTypeEnum(curr_settings.type_)
            if enum_type == ActionTypeEnum.EVENT or enum_type == ActionTypeEnum.TRIGGER:
                return_widget = self._ui.create_function_action
            elif enum_type == ActionTypeEnum.TEXT_MERGER:
                return_widget = self._ui.create_built_in_action
        return return_widget
