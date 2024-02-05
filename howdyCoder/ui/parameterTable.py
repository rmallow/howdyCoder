from ..core.dataStructs import ItemSettings, Parameter, FunctionSettings, AllParameters
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

    def getData(self) -> AllParameters:
        """Return a dict that is the config of the parameter table"""
        return_settings = AllParameters()
        for value in self.values:
            # Check for type value and name in value, and that Name is a valid string
            if (
                ParameterEnum.TYPE in value
                and ParameterEnum.VALUE in value
                and ParameterEnum.NAME in value
                and value[ParameterEnum.NAME]
                and value[ParameterEnum.VALUE] is not None
            ):
                if value[ParameterEnum.TYPE] == EditorType.FUNC.display:
                    """If it is a setup func add to that section instead of parameters"""
                    return_settings.setup_functions[value[ParameterEnum.NAME]] = value[
                        ParameterEnum.VALUE
                    ].function_settings
                else:
                    """else add to parameter section as normal"""
                    return_settings.parameters[value[ParameterEnum.NAME]] = Parameter(
                        value[ParameterEnum.NAME],
                        value[ParameterEnum.VALUE],
                        value[ParameterEnum.TYPE],
                    )

        return return_settings

    def addItemToTable(
        self, name, type_: str, val: typing.Any | str | FunctionSettings
    ):
        self.appendValue()
        index = self.index(self.rowCount() - 1, getattr(ParameterEnum.NAME, ENUM_VALUE))
        self.setData(index, name)
        self.setData(
            index.siblingAtColumn(getattr(ParameterEnum.TYPE, ENUM_VALUE)),
            type_,
        )
        if type_ in editableTable.SELECTOR_TYPES:
            with_helper_data = helperData.addHelperData(val)
            with_helper_data.index = index.siblingAtColumn(
                getattr(ParameterEnum.VALUE, ENUM_VALUE)
            )
            self.itemSelected(with_helper_data)
        else:
            self.setData(
                index.siblingAtColumn(getattr(ParameterEnum.VALUE, ENUM_VALUE)),
                val,
            )

    def setDataFromSettings(self, settings: AllParameters) -> None:
        self.clear()
        for name, param_settings in settings.parameters.items():
            self.addItemToTable(name, param_settings.type_, param_settings.value)
        for (
            name,
            setup_func_settings,
        ) in settings.setup_functions.items():
            self.addItemToTable(name, EditorType.FUNC.display, setup_func_settings)
