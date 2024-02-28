import csv
import pathlib
import typing

import pandas as pd


def loadCSV(file: typing.IO) -> typing.List[typing.List[str]]:
    ret_rows = []
    try:
        reader = csv.reader(file)
        for row in reader:
            ret_rows.append(row)
    except csv.Error as _:
        pass
    return ret_rows


def loadExcel(file: typing.IO) -> pd.DataFrame:
    ret = pd.DataFrame()
    try:
        ret = pd.read_excel(
            file, sheet_name=None, engine="calamine", header=None, index_col=None
        )
    except Exception as e:
        pass
    return ret
