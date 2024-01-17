from dataclasses import dataclass
from enum import Enum
import typing

from PySide6 import QtWidgets, QtCore


class ContextResultType(Enum):
    REMOVE = "Remove"
    EDIT = "Edit"
    COPY = "Copy"
    ADD_DATA_SOURCE = "Add Data Source"
    ADD_ACTION = "Add Action"
    SAVE = "Save"
    INPUT = "Input"
    EXPORT = "Export"


@dataclass(frozen=True)
class ContextResult:
    type_: ContextResultType = ContextResultType.REMOVE
    name: str = ""


def createAndDisplayMenu(
    pos: QtCore.QPoint,
    context_result_type_list: typing.List[ContextResultType],
    signal: QtCore.SignalInstance,
    name="",
):
    menu = QtWidgets.QMenu()
    for context_type_enum in context_result_type_list:
        action = menu.addAction(context_type_enum.value)
        context_res = ContextResult(context_type_enum, name)
        action.triggered.connect(lambda _=None, val=context_res: signal.emit(val))
    menu.exec(pos)


def handleContextResult(
    obj: object,
    context_result: ContextResult,
    function_dictionary: typing.Dict[ContextResultType, typing.Callable],
):
    if context_result.type_ in function_dictionary:
        function_dictionary[context_result.type_](obj, context_result.name)
