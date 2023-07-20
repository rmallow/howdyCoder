from algoBuilder.ui.actionUIConstant import ActionFuncEnum
from .. import editableTable

from ...commonUtil import helpers

from ...core.configConstants import (
    SETUP_FUNCS,
    PARAMETERS,
)
from ...core.commonGlobals import (
    ENUM_VALUE,
    ENUM_DISPLAY,
    ENUM_TYPE,
    ENUM_EDITOR_VALUES,
    ENUM_ENABLED,
)

import typing

from aenum import Enum
from PySide2 import QtCore


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

    def getData(self) -> typing.Dict[str, typing.Any]:
        """Return a dict that is the config of the parameter table"""
        returnConfig = {}
        for value in self.values:
            # Check for type value and name in value, and that Name is a valid string
            if (
                ParameterEnum.TYPE in value
                and ParameterEnum.VALUE in value
                and ParameterEnum.NAME in value
                and value[ParameterEnum.NAME]
                and value[ParameterEnum.VALUE]
            ):

                if value[ParameterEnum.TYPE] == editableTable.EditorType.FUNC.display:
                    """If it is a setup func add to that section instead of parameters"""
                    configSection = SETUP_FUNCS
                else:
                    """else add to parameter section as normal"""
                    configSection = PARAMETERS
                if configSection not in returnConfig:
                    returnConfig[configSection] = {}
                returnConfig[configSection][value[ParameterEnum.NAME]] = value[
                    ParameterEnum.VALUE
                ]

        return returnConfig

    def setValues(self, values: typing.Dict[str, typing.Any]):
        """The base class expects values to be a list, if that's what we were passed in then do that
        But when we output config from this class, it is in dict form, so have special handling for that"""
        self.clear()
        if isinstance(values, list):
            super().setValues(values)
        else:
            # it should be a dict, with two top level keys, SETUP_FUNCS and PARAMETERS
            # the config parser handles these separately, but here we lump them all into one list
            for param_section_type, param_section_values in values.items():
                for param_key, param_value in param_section_values.items():
                    param_type = editableTable.EditorType.ANY
                    if PARAMETERS == param_section_type:
                        # we know these are all not functions, but for the delegate determine the type
                        try:
                            float(param_value)
                            param_type = editableTable.EditorType.NUMBER
                        except:
                            # so it's most likely a string but for redundancy
                            if isinstance(param_value, str):
                                param_type = editableTable.EditorType.STRING

                    elif SETUP_FUNCS == param_section_type:
                        param_type = editableTable.EditorType.FUNC

                    self.appendValue()
                    self.setData(
                        self.index(self.rowCount() - 1, ParameterEnum.NAME.value),
                        param_key,
                    )
                    self.setData(
                        self.index(self.rowCount() - 1, ParameterEnum.TYPE.value),
                        param_type.display,
                    )
                    if param_type == editableTable.EditorType.FUNC:
                        param_value[ActionFuncEnum.INDEX] = self.index(
                            self.rowCount() - 1, ParameterEnum.VALUE.value
                        )

                    self.setData(
                        self.index(self.rowCount() - 1, ParameterEnum.VALUE.value),
                        param_value,
                    )

                    if param_type == editableTable.EditorType.FUNC:
                        self.itemSelected(param_value)


def convertToConfig(
    parameter_dict: typing.Dict[ParameterEnum, str]
) -> typing.Dict[str, str]:
    """This parameter dict should be the output from parameter table getData
    This will convert it from data that makes sense to the UI to config for the block manager"""
    return_config = {}
    if PARAMETERS in parameter_dict:
        return_config[PARAMETERS] = parameter_dict[PARAMETERS]

    if SETUP_FUNCS in parameter_dict:
        # we need to filter out what we actualy want from the setup funcs config
        setup_funcs_dict = parameter_dict[SETUP_FUNCS].copy()

        for key in setup_funcs_dict.keys():
            setup_funcs_dict[key] = helpers.getConfigFromEnumDict(setup_funcs_dict[key])

        return_config[SETUP_FUNCS] = setup_funcs_dict

    return return_config
