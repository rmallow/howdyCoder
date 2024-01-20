from . import datalocator

from ..commonUtil import astUtil
from ..commonUtil import mpLogging
from .dataStructs import FunctionSettings

import configparser
from dataclasses import dataclass
import typing
import os
import pathlib
import copy
import ast
import traceback
import yaml
from functools import cache

from dataclass_wizard import asdict, fromdict


@dataclass
class Library:
    name: str
    group: str
    functions: typing.List[FunctionSettings]


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
    if file_path is not None and file_path != "" and pathlib.Path(file_path).exists():
        root = None
        with open(file_path) as f:
            all_code = f.read()
            try:
                root = ast.parse(all_code, file_path)
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
                        FunctionSettings(f.name, all_code, imports, import_statements)
                        for f in functions
                        if functionCompiles(ast.unparse(f), file_path)
                    ],
                )
    return lib


def getConfigFromFile(file_path, warning_if_not_exist=True):
    """Returns None if file cannot be loaded due to an exception"""
    config = None
    if pathlib.Path(file_path).exists() and pathlib.Path(file_path).is_file():
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
    if file_path is not None and file_path != "" and pathlib.Path(file_path).exists():
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


def pyToAfl(
    file_path,
    name,
    group,
    specific_function="",
    internal_setup_functions=None,
    suggested_output=None,
):
    pass
