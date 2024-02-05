from .dataStructs import AllParameters
from . import datalocator
from .commonGlobals import EditorType

import yaml
from dataclass_wizard import fromdict, asdict

PARAMETERS = "Parameters"


_parameters = AllParameters()

settings_config = datalocator.getConfig(datalocator.PARAMETERS)
if settings_config is not None:
    _parameters = fromdict(AllParameters, settings_config)


def getKeys() -> None:
    return [
        param
        for param in _parameters.parameters.values()
        if param.type_ == EditorType.KEY
    ]


def getNonKeys() -> None:
    return [
        name
        for name, param in _parameters.parameters.items()
        if param.type_ != EditorType.KEY
    ] + list(_parameters.setup_functions.keys())


def clearParameters() -> None:
    global _parameters
    _parameters = AllParameters()


def setParameters(new_parameters: AllParameters) -> None:
    global _parameters
    _parameters = new_parameters


def getParameters() -> AllParameters:
    global _parameters
    return _parameters


def saveParameters() -> None:
    global _parameters
    with open(datalocator.getDataFilePath(datalocator.PARAMETERS), "w") as f:
        yaml.dump(
            asdict(_parameters),
            f,
            default_flow_style=False,
        )
