import csv
import pathlib
import typing
import itertools

import python_calamine

CSV_EXT = ".csv"
EXCEL_EXT_LIST = [".xlsx", ".xlsm", ".xls", ".xlsb", ".ods"]


def _loadCSV(
    file: typing.IO, skip_first: bool = False
) -> typing.List[typing.List[typing.Any]] | None:
    ret_rows = []
    try:
        reader = csv.reader(file)
        if skip_first:
            next(reader)
        for row in reader:
            ret_rows.append(row)
    except csv.Error as _:
        ret_rows = None
    return ret_rows


def _loadExcel(
    file: typing.IO, skip_first: bool = False
) -> typing.Dict[str, typing.List[typing.List[typing.Any]]] | None:
    ret_sheets = {}
    try:
        reader = python_calamine.CalamineWorkbook.from_filelike(file)
        for name in reader.sheet_names:
            if skip_first:
                ret_sheets[name] = reader.get_sheet_by_name(name).to_python()[1:]
            else:
                ret_sheets[name] = reader.get_sheet_by_name(name).to_python()
    except python_calamine.CalamineError as _:
        ret_sheets = None
    return ret_sheets


def loadFile(
    file_path: str | pathlib.Path,
    pass_through_exception=False,
    skip_first=False,
) -> typing.Any | None:
    abs_path = pathlib.Path(file_path).resolve()
    file_type = abs_path.suffix
    data = None
    if canLoadFile(abs_path):
        try:
            open_format = "r" + ("b" if file_type in EXCEL_EXT_LIST else "")
            with abs_path.open(open_format) as file:
                data = _LOADERS[file_type](file, skip_first=skip_first)
        except (IOError, FileNotFoundError) as e:
            data = None
            if pass_through_exception:
                raise e
    return data


def canLoadFile(file_path: str | pathlib.Path) -> bool:
    return pathlib.Path(file_path).suffix in _LOADERS


def loadFileList(
    file_path_list: typing.List[str],
    skip_first_list: typing.List[bool] = None,
) -> typing.Dict[str, typing.Any | None]:
    return {
        file_path: loadFile(file_path, False, skip_first)
        for file_path, skip_first in itertools.zip_longest(
            file_path_list,
            skip_first_list if skip_first_list is not None else [],
            fillvalue=False,
        )
    }


_LOADERS = {CSV_EXT: _loadCSV} | {k: _loadExcel for k in EXCEL_EXT_LIST}
