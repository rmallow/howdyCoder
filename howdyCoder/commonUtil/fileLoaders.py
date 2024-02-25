import csv
import pathlib
import typing


def loadCSV(path: pathlib.Path) -> typing.List[typing.List[str]]:
    ret_rows = []
    with path.open("r") as f:
        try:
            reader = csv.reader(f)
            for row in reader:
                ret_rows.append(row)
        except csv.Error as _:
            pass
    return ret_rows
