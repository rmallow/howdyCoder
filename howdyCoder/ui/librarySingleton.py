from ..data.datalocator import LIBRARIES_FILE

from ..commonUtil import helpers
from ..commonUtil import astUtil
from ..commonUtil import mpLogging
from ..core.commonGlobals import ENUM_DISPLAY
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

from dataclass_wizard import asdict, fromlist


"""
AFL Constants
"""
NAME_KEY = "name"
GROUP_KEY = "group"
FUNCTIONS_KEY = "functions"


@dataclass
class FunctionData:
    function: ast.FunctionDef
    imports: list
    import_statements: list


@dataclass
class Library:
    name: str
    group: str
    function_list: typing.List[FunctionData]


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
                            FunctionData(f, imports, import_statements)
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
            function_data_list = []
            res = getConfigFromFile(file_path)
            config = {}
            if res is not None:
                config = res
            for function_setting in fromlist(
                FunctionSettings, config.get(FUNCTIONS_KEY, [])
            ):
                if functionCompiles(
                    function_setting.code,
                    file_path,
                ):
                    function_data_list.append(
                        FunctionData(
                            astUtil.getFunctions(ast.parse(function_setting.code))[0],
                            function_setting.imports,
                            function_setting.import_statements,
                        )
                    )
                lib = Library(
                    config.get(NAME_KEY, ""),
                    config.get(GROUP_KEY, ""),
                    function_data_list,
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
    dict_to_save = {NAME_KEY: name, GROUP_KEY: group, FUNCTIONS_KEY: []}

    if res := getConfigFromFile(file_path, warning_if_not_exist=False):
        dict_to_save = res
    if pathlib.Path(file_path).parent.exists():
        with open(file_path, "w") as file:
            dict_to_save[FUNCTIONS_KEY].append(asdict(function_config))
            yaml.dump(dict_to_save, file, default_flow_style=False)


def getLibraries() -> typing.List[Library]:
    """Return a copy of the libraries so they can't be modified"""
    return [copy.deepcopy(lib) for lib in _libraries]


"""If the library singleton is being loaded for the first time run some initalization code"""
first_import = True
if first_import == True:
    first_import = False
    """Load libraries from library file using ExtendedInterpolation
        ExtendedInterpolation will expand the variables in the file for us"""
    config = configparser.ConfigParser(
        interpolation=configparser.ExtendedInterpolation(),
        defaults={"root": os.path.dirname(LIBRARIES_FILE)},
        allow_no_value=True,
    )
    config.read(LIBRARIES_FILE)

    # we don't want to try to load any default values
    # these default values are only for making parsing easier
    ignore_defaults = set()
    for key, _ in config.items(config.default_section):
        ignore_defaults.add(key)

    # we'll make sure we're not parsing any default keys
    for section in config.sections():
        if section != "locations":
            for key, value in config.items(section):
                if key not in ignore_defaults:
                    loadLibrary(value, key, section)
