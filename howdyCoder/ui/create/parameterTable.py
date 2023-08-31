from ...core.dataStructs import ItemSettings, Parameter
from .. import editableTable

from ...core.commonGlobals import (
    ENUM_VALUE,
    ENUM_DISPLAY,
    ENUM_TYPE,
    ENUM_EDITOR_VALUES,
    ENUM_ENABLED,
)

import typing

from aenum import Enum
from PySide6 import QtCore


class ParameterEnum(Enum):
    """Used as the basis for editable table for parameter and setup func input"""

    _init_ = (
        f"{ENUM_VALUE} {ENUM_DISPLAY} {ENUM_TYPE} {ENUM_EDITOR_VALUES} {ENUM_ENABLED}"
    )

    NAME = 0, "Name", editableTable.EditorType.STRING, [], True
    TYPE = (
        1,
        "Type",
        editableTable.EditorType.COMBO,
        [
            editableTable.EditorType.STRING.display,
            editableTable.EditorType.NUMBER.display,
            editableTable.EditorType.FUNC.display,
        ],
        True,
    )
    DESCRIPTION = 2, "Description", editableTable.EditorType.STRING, [], False
    VALUE = 3, "Value", editableTable.EditorType.ANY, [], True


class ParameterTableModel(editableTable.EditableTableModelAddRows):
    def __init__(self, *args, **kwargs):
        super().__init__(ParameterEnum)
        self.values: typing.List[typing.Dict[ParameterEnum, str]] = []
        self.current_names: typing.Set[str] = set()

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
            role == QtCore.Qt.ToolTipRole
            and index.column() == ParameterEnum.DESCRIPTION.value
        ):
            valueKey = self.getValueKey(index)
            if ParameterEnum.DESCRIPTION in self.values[valueKey]:
                return self.values[valueKey][ParameterEnum.DESCRIPTION]
        return super().data(index, role)

    def getData(self, config: ItemSettings) -> typing.Dict[str, typing.Any]:
        """Return a dict that is the config of the parameter table"""
        returnConfig = {}
        for value in self.values:
            # Check for type value and name in value, and that Name is a valid string
            if (
                ParameterEnum.TYPE in value
                and ParameterEnum.VALUE in value
                and ParameterEnum.NAME in value
                and value[ParameterEnum.NAME]
            ):
                if value[ParameterEnum.TYPE] == editableTable.EditorType.FUNC.display:
                    """If it is a setup func add to that section instead of parameters"""
                    config.setup_functions[value[ParameterEnum.NAME]] = value[
                        ParameterEnum.VALUE
                    ]
                else:
                    """else add to parameter section as normal"""
                    config.parameters[value[ParameterEnum.NAME]] = Parameter(
                        value[ParameterEnum.NAME], value[ParameterEnum.VALUE]
                    )

        return returnConfig
