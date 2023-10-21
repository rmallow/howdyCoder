from . import datalocator
from ..commonUtil import keyringUtil

import typing
from dataclasses import dataclass

KEYS = "Keys"


@dataclass
class KeyStatus:
    current: str = ""
    valid: bool = False
    retrieve: bool = False


@dataclass
class KeySetData:
    key_name: str
    set_function: typing.Callable
    validation_function: typing.Callable


key_set_data_mapping: typing.Dict[str, KeySetData] = {}
key_status: typing.Dict[str, KeyStatus] = {}


def addKeySetData(display_name: str, data: KeySetData):
    assert display_name not in key_set_data_mapping
    key_set_data_mapping[display_name] = data
    if display_name in key_status:
        if key_status[display_name].retrieve:
            key_status[display_name].current = keyringUtil.getKey(data.key_name)
        if key_status[display_name].current:
            key_status[display_name].valid = data.validation_function(
                key_status[display_name].current
            )
            if key_status[display_name].valid:
                data.set_function(key_status[display_name].current)
    else:
        key_status[display_name] = KeyStatus()
        datalocator.modifyValue(datalocator.SETTINGS, KEYS, display_name, str(False))


settings_config = datalocator.getConfig(datalocator.SETTINGS)
if KEYS in settings_config:
    for k, v in settings_config[KEYS].items():
        if v == str(True):
            key_status[k] = KeyStatus("", False, True)
