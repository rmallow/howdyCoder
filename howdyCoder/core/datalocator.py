import os
import configparser
import typing
from dataclasses import dataclass, field


@dataclass
class DataFile:
    dir_path: str = ""
    file_path: str = ""
    config: typing.Dict[str, typing.Dict[str, str]] = field(default_factory=dict)


_data_path = ""
_config_values: typing.Dict[str, DataFile] = {}

LIBRARIES = "libraries"
SERVER = "server"
SETTINGS = "settings"
PROMPTS = "prompts"

REQUIRED = set([LIBRARIES, SERVER, SETTINGS, PROMPTS])


def getValue(group: str, section: str, key: str) -> str | None:
    """Returns None if either group or key don't exist"""
    if section is not None:
        return (
            _config_values.get(group, DataFile()).config.get(section, {}).get(key, None)
        )


def getDataFilePath(group: str):
    return _config_values.get(group, DataFile()).file_path


def getDataDirPath(group: str):
    return _config_values.get(group, DataFile()).dir_path


def getConfig(group: str) -> typing.Dict[str, str]:
    return _config_values.get(group, DataFile()).config


def modifyValue(group: str, section: str, key: str, value: str):
    if group in _config_values:
        _config_values[group].config[key] = value
        parser = configparser.ConfigParser()
        parser.optionxform = str
        file_path = getDataFilePath(group)
        parser.read(file_path)
        if section not in parser.sections():
            parser.add_section(section)
        parser.set(section, key, value)
        with open(file_path, "w") as file:
            parser.write(file)


def setDataPath(path: str):
    """
    Reads in the datalocator file and assigns it to the config values dictionary
    Also does basic check of required keys being there
    """

    FILES = "Files"
    DATA_LOCATOR_FILE_NAME = "datalocator.ini"
    global _data_path, _config_values
    _data_path = path
    _config_values.clear()

    config = configparser.ConfigParser()
    config.read(os.path.join(_data_path, DATA_LOCATOR_FILE_NAME))

    assert all(
        req in config[FILES] for req in REQUIRED
    ), "Missing a required datalocator section"

    for group in config[FILES]:
        inner_config = configparser.ConfigParser()
        inner_config.optionxform = str
        inner_data_file_path = os.path.join(_data_path, config.get(FILES, group))
        inner_config.read(inner_data_file_path)
        _config_values[group] = DataFile(
            os.path.dirname(inner_data_file_path), inner_data_file_path
        )
        for section in inner_config.sections():
            _config_values[group].config[section] = {}
            for option in inner_config.options(section):
                _config_values[group].config[section][option] = inner_config.get(
                    section, option
                )
