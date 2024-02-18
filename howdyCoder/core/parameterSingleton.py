from .dataStructs import Parameter, FunctionSettings
from . import datalocator
from .commonGlobals import EditorType

import typing

import yaml
from dataclass_wizard import fromdict, asdict

PARAMETERS = "Parameters"


_parameters: typing.Dict[str, Parameter] = {}

settings_config = datalocator.getConfig(datalocator.PARAMETERS)
if settings_config is not None:
    _parameters = {k: fromdict(Parameter, v) for k, v in settings_config.items()}


def getType(type_: EditorType) -> typing.List[Parameter]:
    return [param for param in _parameters.values() if param.type_ == type_.display]


def getNonType(type_: EditorType) -> typing.List[Parameter]:
    return [param for param in _parameters.values() if param.type_ != type_.display]


def getKeys() -> typing.List[Parameter]:
    return getType(EditorType.KEY)


def getNonKeys() -> typing.List[Parameter]:
    return getNonType(EditorType.KEY)


def clearParameters() -> None:
    global _parameters
    _parameters = {}


def setParameters(new_parameters: typing.Dict[str, Parameter]) -> None:
    global _parameters
    _parameters = new_parameters


def getParameters() -> typing.Dict[str, Parameter]:
    global _parameters
    return _parameters


def getParameter(name: str) -> Parameter | None:
    global _parameters
    return _parameters.get(name, None)


def saveParameters() -> None:
    global _parameters
    with open(datalocator.getDataFilePath(datalocator.PARAMETERS), "w") as f:
        yaml.dump(
            {k: asdict(v) for k, v in _parameters.items()},
            f,
            default_flow_style=False,
        )
