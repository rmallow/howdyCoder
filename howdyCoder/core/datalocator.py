import os
import configparser
import typing
import pathlib
import yaml
from dataclasses import dataclass, field


def getDictFromYmlFile(path):
    contents = {}
    try:
        with open(path) as file:
            contents = yaml.safe_load(file)
    except OSError:
        assert False, "Error reading yaml file"
    return contents


@dataclass
class DataFile:
    dir_path: str = ""
    file_path: str = ""
    config: typing.Dict[str, typing.Dict[str, str]] = field(default_factory=dict)


_root_path = pathlib.Path(os.path.abspath(__file__)).parent.parent.parent

_data_path = ""
_config_values: typing.Dict[str, DataFile] = {}

LIBRARIES = "libraries"
SERVER = "server"
SETTINGS = "settings"
PROMPTS = "prompts"
PARAMETERS = "parameters"

REQUIRED = set([LIBRARIES, SERVER, SETTINGS, PROMPTS, PARAMETERS])


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
        inner_data_file_path = os.path.join(_data_path, config.get(FILES, group))
        _config_values[group] = DataFile(
            os.path.dirname(inner_data_file_path), inner_data_file_path
        )
        if inner_data_file_path.endswith(".ini"):
            inner_config = configparser.ConfigParser(
                interpolation=configparser.ExtendedInterpolation(),
                defaults={"root": str(_root_path)},
            )
            inner_config.optionxform = str
            inner_config.read(inner_data_file_path)
            for section in inner_config.sections():
                _config_values[group].config[section] = {}
                for option in inner_config.options(section):
                    _config_values[group].config[section][option] = inner_config.get(
                        section, option
                    )
        elif inner_data_file_path.endswith(".yml"):
            _config_values[group].config = getDictFromYmlFile(inner_data_file_path)
