import csv
import pathlib
import typing

import python_calamine


def loadCSV(file: typing.IO) -> typing.List[typing.List[typing.Any]]:
    ret_rows = []
    try:
        reader = csv.reader(file)
        for row in reader:
            ret_rows.append(row)
    except csv.Error as _:
        pass
    return ret_rows


def loadExcel(
    file: typing.IO,
) -> typing.Dict[str, typing.List[typing.List[typing.Any]]]:
    ret_sheets = {}
    try:
        reader = python_calamine.CalamineWorkbook.from_filelike(file)
        for name in reader.sheet_names:
            ret_sheets[name] = reader.get_sheet_by_name(name).to_python()
    except python_calamine.CalamineError as _:
        pass
    return ret_sheets
