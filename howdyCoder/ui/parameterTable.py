from ..core.dataStructs import ItemSettings, Parameter, FunctionSettings
from . import pathSelector
from . import editableTable

from .util import helperData

from ..core.commonGlobals import (
    ENUM_VALUE,
    ENUM_DISPLAY,
    ENUM_TYPE,
    ENUM_EDITOR_VALUES,
    ENUM_ENABLED,
    EditorType,
)

import typing

from aenum import Enum
from PySide6 import QtCore


class ParameterEnum(Enum):
    """Used as the basis for editable table for parameter and setup func input"""

    _init_ = (
        f"{ENUM_VALUE} {ENUM_DISPLAY} {ENUM_TYPE} {ENUM_EDITOR_VALUES} {ENUM_ENABLED}"
    )

    NAME = 0, "Name", EditorType.STRING, [], True
    TYPE = (
        1,
        "Type",
        EditorType.COMBO,
        [
            EditorType.STRING.display,
            EditorType.INTEGER.display,
            EditorType.DECIMAL.display,
            EditorType.FUNC.display,
            EditorType.FILE.display,
            EditorType.FOLDER.display,
            EditorType.GLOBAL_PARAMETER.display,
            EditorType.KEY.display,
        ],
        True,
    )
    VALUE = 2, "Value", EditorType.ANY, [], True


class ParameterTableModel(editableTable.EditableTableModelAddRows):
    def __init__(self, *args, combo_hide_values=None, **kwargs):
        super().__init__(ParameterEnum, combo_hide_values=combo_hide_values)
        self.values: typing.List[typing.Dict[ParameterEnum, str]] = []
        self.current_names: typing.Set[str] = set()

    def clear(self):
        self.current_names.clear()
        super().clear()

    def setData(
        self,
        index: QtCore.QModelIndex,
        value: typing.Any,
        role: int = QtCore.Qt.DisplayRole,
    ) -> bool:
        if (
            (role == QtCore.Qt.EditRole or role == QtCore.Qt.DisplayRole)
            and index.column() == getattr(ParameterEnum.NAME, ENUM_VALUE)
            and index.row() < len(self.values)
        ):
            self.current_names.discard(
                self.values[index.row()].get(ParameterEnum.NAME, "")
            )
            self.current_names.add(value)
        return super().setData(index, value, role)

    def data(
        self, index: QtCore.QModelIndex, role: int = QtCore.Qt.DisplayRole
    ) -> typing.Any:
        if (
            role == QtCore.Qt.ItemDataRole.DisplayRole
            or role == QtCore.Qt.ItemDataRole.EditRole
        ):
            if index in self.selector_widgets:
                return ""
        return super().data(index, role)

    def getSuggestedParameters(self):
        suggested = []
        for value in self.values:
            if (
                ParameterEnum.TYPE in value
                and ParameterEnum.VALUE in value
                and ParameterEnum.NAME in value
                and value[ParameterEnum.NAME]
                and value[ParameterEnum.VALUE]
            ):
                if value[ParameterEnum.TYPE] == getattr(EditorType.FUNC, ENUM_DISPLAY):
                    suggested.extend(value[ParameterEnum.VALUE].suggested_parameters)
        return suggested

    def getParameterByRow(self, row: int):
        ret_val = None
        if row < len(self.values):
            value = self.values[row]
            # Check for type value and name in value, and that Name is a valid string
            if (
                ParameterEnum.TYPE in value
                and ParameterEnum.VALUE in value
                and ParameterEnum.NAME in value
                and value[ParameterEnum.NAME]
                and value[ParameterEnum.VALUE] is not None
            ):
                ret_val = Parameter(
                    value[ParameterEnum.NAME],
                    (
                        value[ParameterEnum.VALUE]
                        if value[ParameterEnum.TYPE] != EditorType.FUNC.display
                        else value[ParameterEnum.VALUE].function_settings
                    ),
                    value[ParameterEnum.TYPE],
                )
        return ret_val

    def getParameterByIndex(self, index: QtCore.QModelIndex):
        return self.getParameterByRow(index.row())

    def getData(self) -> typing.Dict[str, Parameter]:
        """Return a dict that is the config of the parameter table"""
        return_parameters = {}
        for row in range(len(self.values)):
            row_parameter = self.getParameterByRow(row)
            if row_parameter is not None:
                return_parameters[row_parameter.name] = row_parameter

        return return_parameters

    def addItemToTable(self, parameter: Parameter):
        self.appendValue()
        index = self.index(self.rowCount() - 1, getattr(ParameterEnum.NAME, ENUM_VALUE))
        self.setData(index, parameter.name)
        self.setData(
            index.siblingAtColumn(getattr(ParameterEnum.TYPE, ENUM_VALUE)),
            parameter.type_,
        )
        if parameter.type_ in editableTable.SELECTOR_TYPES:
            with_helper_data = helperData.addHelperData(parameter.value)
            with_helper_data.index = index.siblingAtColumn(
                getattr(ParameterEnum.VALUE, ENUM_VALUE)
            )
            self.itemSelected(with_helper_data)
        else:
            self.setData(
                index.siblingAtColumn(getattr(ParameterEnum.VALUE, ENUM_VALUE)),
                parameter.value,
            )

    def setDataFromSettings(self, settings: typing.Dict[str, Parameter]) -> None:
        self.clear()
        for param_settings in settings.values():
            self.addItemToTable(param_settings)
