from .createTypeBasePage import CreateTypeBasePage
from ..uiConstants import PageKeys
from ...core.configConstants import ActionTypeEnum

import typing

from PySide2 import QtWidgets


TYPE_DESCRIPTION = {
    ActionTypeEnum.TRIGGER.display: """
    Executes an output function based on the given conditions. \n
    Does not create new data and triggers will not expect functions called to return data.
    """,
    ActionTypeEnum.EVENT.display: """
    Takes input data and creates new data based on the given function. \n
    For events, the name of the event will be the name of the output data. \n
    The functions called by events will be expected to return data.
    """,
}


class CreateActionTypePage(CreateTypeBasePage):
    PAGE_KEY = PageKeys.ACTION_TYPE
    EXIT = PageKeys.ADD_ACTION

    def __init__(
        self,
        current_config: typing.Dict[str, typing.Any],
        parent: typing.Optional[QtWidgets.QWidget] = None,
    ):
        super().__init__(current_config, "Action Type", TYPE_DESCRIPTION, parent=parent)
