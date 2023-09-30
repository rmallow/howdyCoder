from ..core import datalocator

from ..commonUtil import astUtil
from ..commonUtil import mpLogging
from ..core.dataStructs import FunctionSettings

import configparser
from dataclasses import dataclass
import typing
import os
import pathlib
import copy
import ast
import traceback
import yaml

from dataclass_wizard import asdict, fromdict


@dataclass
class Library:
    name: str
    group: str
    functions: typing.List[FunctionSettings]


"""Used to store the loaded library values between func selectors"""
_libraries: typing.List[Library] = []


def functionCompiles(function_string: str, file_path: str) -> bool:
    try:
        compile(function_string, "<string>", "exec")
    except Exception as e:
        mpLogging.warning(
            "Exception while compiling a function when loading a library",
            description=f"Library: {file_path}, exception: {traceback.format_exc()}",
        )
        return False
    else:
        return True


def loadLibraryPy(file_path: str) -> Library:
    """
    Load a library file in, if name is none use the file name
    """
    lib = None
    if file_path is not None and file_path != "":
        filePathObj = pathlib.Path(file_path)
        if filePathObj.exists():
            root = None
            with open(file_path) as f:
                try:
                    root = ast.parse(f.read(), file_path)
                except Exception as e:
                    mpLogging.error(
                        "Exception while parsing a library",
                        description=f"Library: {file_path}, exception: {traceback.format_exc()}",
                    )
                else:
                    # no attempt to differentiate imports needed per function will be done
                    functions = astUtil.getFunctions(root)

                    imports, import_statements = astUtil.getImportsUnique(root)
                    lib = Library(
                        "",
                        "",
                        [
                            FunctionSettings(
                                f.name, ast.unparse(f), imports, import_statements
                            )
                            for f in functions
                            if functionCompiles(ast.unparse(f), file_path)
                        ],
                    )
    return lib


def getConfigFromFile(file_path, warning_if_not_exist=True):
    """Returns None if file cannot be loaded due to an exception"""
    config = None
    if pathlib.Path(file_path).exists():
        if pathlib.Path(file_path).is_file():
            with open(file_path, "r") as file:
                try:
                    config = yaml.safe_load(file)
                except yaml.YAMLError as e:
                    description = (
                        f"Library: {file_path}, exception: {traceback.format_exc()}"
                    )
                    if hasattr(e, "problem_mark"):
                        mark = e.problem_mark
                        description = (
                            f"Error position {mark.line + 1}:{mark.column+1}\n\n"
                            + description
                        )
                    mpLogging.warning(
                        "Attemped to Load to an invalid AFL file",
                        description=description,
                    )
    elif warning_if_not_exist:
        mpLogging.warning(
            "Attemped to load an AFL from an invalid path",
            description=f"Library: {file_path}",
        )
    return config


def loadLibraryAfl(file_path: str):
    lib = None
    if file_path is not None and file_path != "":
        filePathObj = pathlib.Path(file_path)
        if filePathObj.exists():
            config = {}
            if res := getConfigFromFile(file_path):
                config = fromdict(Library, res)
            lib = Library(
                config.name,
                config.group,
                [
                    function_setting
                    for function_setting in config.functions
                    if functionCompiles(
                        function_setting.code,
                        file_path,
                    )
                ],
            )
    return lib


def loadLibrary(file_path: str, name: str = "", group: str = "") -> Library:
    lib = None
    if file_path.lower().endswith(".py"):
        lib = loadLibraryPy(file_path)
    elif file_path.lower().endswith(".afl"):
        lib = loadLibraryAfl(file_path)
    if lib:
        if not lib.name:
            lib.name = name if name else pathlib.Path(file_path).stem
        if not lib.group:
            lib.group = group
        _libraries.append(lib)
    return lib


def saveToLibrary(
    file_path: str,
    function_config: FunctionSettings,
    name: str = "",
    group: str = "",
):
    settings_to_save = Library(name, group, [])

    if res := getConfigFromFile(file_path, warning_if_not_exist=False):
        settings_to_save = fromdict(Library, res)
    if pathlib.Path(file_path).parent.exists():
        with open(file_path, "w") as file:
            settings_to_save.functions.append(function_config)
            yaml.dump(asdict(settings_to_save), file, default_flow_style=False)


def getLibraries() -> typing.List[Library]:
    """Return a copy of the libraries so they can't be modified"""
    return [copy.deepcopy(lib) for lib in _libraries]


"""If the library singleton is being loaded for the first time run some initalization code"""
# we'll make sure we're not parsing any default keys
for section_key, section_config in datalocator.getConfig(datalocator.LIBRARIES).items():
    if section_key != "locations":
        for key, value in section_config.items():
            loadLibrary(value, key, section_key)
