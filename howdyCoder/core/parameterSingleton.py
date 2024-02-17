from .dataStructs import AllParameters, Parameter, FunctionSettings
from . import datalocator
from .commonGlobals import EditorType

import typing

import yaml
from dataclass_wizard import fromdict, asdict

PARAMETERS = "Parameters"


_parameters = AllParameters()

settings_config = datalocator.getConfig(datalocator.PARAMETERS)
if settings_config is not None:
    _parameters = fromdict(AllParameters, settings_config)


def getType(type_: EditorType) -> typing.List[Parameter | FunctionSettings]:
    return (
        [
            param
            for param in _parameters.parameters.values()
            if param.type_ == type_.display
        ]
        if type_ != EditorType.FUNC
        else list(_parameters.setup_functions.values())
    )


def getNonType(type_: EditorType) -> typing.List[Parameter | FunctionSettings]:
    return (
        [
            param
            for param in _parameters.parameters.values()
            if param.type_ != type_.display
        ]
        + list(_parameters.setup_functions.values())
        if type_ != EditorType.FUNC
        else []
    )


def getKeys() -> typing.List[Parameter]:
    return getType(EditorType.KEY)


def getNonKeys() -> typing.List[Parameter | FunctionSettings]:
    return getNonType(EditorType.KEY)


def clearParameters() -> None:
    global _parameters
    _parameters = AllParameters()


def setParameters(new_parameters: AllParameters) -> None:
    global _parameters
    _parameters = new_parameters


def getParameters() -> AllParameters:
    global _parameters
    return _parameters


def getParameter(name: str) -> typing.Any | None:
    if name in _parameters.parameters:
        return _parameters.parameters[name]
    elif name in _parameters.setup_functions:
        return _parameters.setup_functions[name]
    else:
        return None


def saveParameters() -> None:
    global _parameters
    with open(datalocator.getDataFilePath(datalocator.PARAMETERS), "w") as f:
        yaml.dump(
            asdict(_parameters),
            f,
            default_flow_style=False,
        )
