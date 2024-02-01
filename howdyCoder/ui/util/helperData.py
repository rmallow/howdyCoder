from ...core.dataStructs import FunctionSettings
from ...commonUtil import astUtil

import ast, typing
from dataclasses import dataclass, field
from functools import singledispatch

from PySide6 import QtCore


@dataclass
class HelperData:
    index: QtCore.QModelIndex = None


@dataclass
class FunctionSettingsWithHelperData(HelperData):
    function_settings: FunctionSettings = FunctionSettings()
    suggested_parameters: typing.List[str] = field(default_factory=list)
    suggested_data: typing.List[str] = field(default_factory=list)


@dataclass
class PathWithHelperData(HelperData):
    path: str = ""


@singledispatch
def addHelperData(value):
    return value


@addHelperData.register
def _(
    value: str,
) -> PathWithHelperData:
    return PathWithHelperData(None, value)


@addHelperData.register
def _(
    value: FunctionSettings,
) -> FunctionSettingsWithHelperData:
    root = ast.parse(value.code, "<string>")
    return FunctionSettingsWithHelperData(
        None,
        value,
        astUtil.getSuggestedParameterNames(root, value),
        astUtil.getSuggestedDataSetNames(root),
    )
