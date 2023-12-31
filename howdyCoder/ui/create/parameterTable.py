from ...core.dataStructs import ItemSettings, Parameter
from .. import pathSelector
from .. import funcSelector
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
            editableTable.EditorType.INTEGER.display,
            editableTable.EditorType.DECIMAL.display,
            editableTable.EditorType.FUNC.display,
            editableTable.EditorType.FILE.display,
            editableTable.EditorType.FOLDER.display,
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
            role == QtCore.Qt.ToolTipRole
            and index.column() == ParameterEnum.DESCRIPTION.value
        ):
            valueKey = self.getValueKey(index)
            if ParameterEnum.DESCRIPTION in self.values[valueKey]:
                return self.values[valueKey][ParameterEnum.DESCRIPTION]
        elif (
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
                if value[ParameterEnum.TYPE] == getattr(
                    editableTable.EditorType.FUNC, ENUM_DISPLAY
                ):
                    suggested.extend(value[ParameterEnum.VALUE].suggested_parameters)
        return suggested

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
                and value[ParameterEnum.VALUE] is not None
            ):
                if value[ParameterEnum.TYPE] == editableTable.EditorType.FUNC.display:
                    """If it is a setup func add to that section instead of parameters"""
                    config.setup_functions[value[ParameterEnum.NAME]] = value[
                        ParameterEnum.VALUE
                    ].function_settings
                else:
                    """else add to parameter section as normal"""
                    config.parameters[value[ParameterEnum.NAME]] = Parameter(
                        value[ParameterEnum.NAME],
                        value[ParameterEnum.VALUE],
                        value[ParameterEnum.TYPE],
                    )

        return returnConfig

    def setDataFromSettings(self, settings: ItemSettings) -> None:
        for name, param_settings in settings.parameters.items():
            self.appendValue()
            index = self.index(
                self.rowCount() - 1, getattr(ParameterEnum.NAME, ENUM_VALUE)
            )
            self.setData(index, name)
            self.setData(
                index.siblingAtColumn(getattr(ParameterEnum.TYPE, ENUM_VALUE)),
                param_settings.type_,
            )
            if param_settings.type_ in editableTable.SELECTOR_TYPES:
                self.itemSelected(
                    pathSelector.PathWithHelperData(
                        index.siblingAtColumn(getattr(ParameterEnum.VALUE, ENUM_VALUE)),
                        param_settings.value,
                    )
                )
            else:
                self.setData(
                    index.siblingAtColumn(getattr(ParameterEnum.VALUE, ENUM_VALUE)),
                    param_settings.value,
                )
        for name, setup_func_settings in settings.setup_functions.items():
            self.appendValue()
            index = self.index(
                self.rowCount() - 1, getattr(ParameterEnum.NAME, ENUM_VALUE)
            )
            self.setData(index, name)
            self.setData(
                index.siblingAtColumn(getattr(ParameterEnum.TYPE, ENUM_VALUE)),
                editableTable.EditorType.FUNC,
            )
            with_helper = funcSelector.addHelperData(setup_func_settings)
            with_helper.index = index.siblingAtColumn(
                getattr(ParameterEnum.VALUE, ENUM_VALUE)
            )
            self.itemSelected(with_helper)
