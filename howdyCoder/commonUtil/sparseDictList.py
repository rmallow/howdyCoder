from __future__ import annotations
from typing import Any
import typing
from dataclasses import dataclass
import csv
from collections import defaultdict


def isDictOrList(data):
    if isinstance(data, str):
        return False
    try:
        len(data)
    except AttributeError:
        return False
    return True


def determienMaxLenOfData(data, flatten, transpose):
    """
    potential data 		    	- 		len
    not flatten                 -       1
    num/str/any non iter	    -		1
    dict of iter/non iter 	    -		len(iter/non iter)
    list of iter/non iter 		-		len(list) if tranpose else len(iter/non iter)

    a string is iterable but not something we want to iterate so also ignore that
    """
    max_len = 1
    if flatten and not isinstance(data, str):
        final_iter = data
        try:
            len(data)
        except TypeError as _:
            return 1
        else:
            # it's some iterable value, check if dictionary
            try:
                final_iter = data.values()
            except AttributeError as _:
                # at this point it must be a list
                if transpose:
                    return len(data)

        for v in final_iter:
            try:
                max_len = max(max_len, len(v))
            except TypeError as _:
                pass
    return max_len


@dataclass()
class SparseData:
    index: int
    value: Any

    def to_string(self, show_index: bool = False):
        return f"{self.index} : {str(self.value)}" if show_index else str(self.value)


class SparseDictList(dict):
    """
    Conveince Class for supporting dicts that are dict[key] -> list
    """

    def __init__(self):
        super().__init__()
        self.indexKey = None
        self.longest_list = 0

    def __setitem__(self, key: str, value: Any) -> Any:
        super().__setitem__(key, value)
        # without this hasattr check there is some weird pickling issues
        if hasattr(self, "longest_list") and len(self[key]) > self.longest_list:
            self.longest_list = len(self[key])

    """
    TODO
    Experimenting with removing these for speed issues
    Removed on 3/11/2024
    If no error, remove later.
    def __getattribute__(self, name: str) -> Any:
        if name == "index":
            if self.indexKey is not None:
                return self[self.indexKey]
            else:
                return None
        else:
            return super().__getattribute__(name)

    def __getstate__(self):
        #because we overrided __getattribute__ we must explicitly define these for pickling
        return self.__dict__

    def __setstate__(self, d):
        #because we overrided __getattribute__ we must explicitly define these for pickling
        self.__dict__.update(d)
    """

    def setIndex(self, indexKey: str) -> None:
        if indexKey in self:
            self.indexKey = indexKey
        else:
            self.indexKey = None

    def getNthKey(self, index: int = 0) -> Any:
        # For large dict list, very slow, consider storing keys
        if index < 0:
            index += len(self)
        for i, key in enumerate(self):
            if index == i:
                return key

    def appendDictList(self, b: dict):
        if b is not None:
            for key in b.keys():
                if key not in self:
                    self[key] = []
                if isinstance(b[key], list):
                    self[key].extend(b[key])
                else:
                    self[key].append(b[key])
                if len(self[key]) > self.longest_list:
                    self.longest_list = len(self[key])

    def sliceDictListEnd(self, length: int) -> SparseDictList:
        returnDict = SparseDictList()
        for key, value in self.items():
            returnDict[key] = value[(-1 * length) :]
        return returnDict

    def sliceDictList(self, start: int, end: int) -> SparseDictList:
        returnDict = SparseDictList()
        for key, value in self.items():
            returnDict[key] = value[start:end]
        return returnDict

    def getLengthOfLongestList(self) -> int:
        return self.longest_list

    def getFirstListLength(self) -> int:
        return len(next(iter(self.values())))

    def appendDataList(self, data_list: typing.List) -> int:
        """
        For inserting 3.5m data points, this function takes < 10s on avg.
        Slowest parts (happens each data point):
            1. Creating dataclasses
            2. Appending to the list
            3. Access internal map
        If necessary could be improved in the future by not storing each individual data point as a dataclass
        i.e. could store lists of data points with their indexes
        """
        max_len = 1 if data_list else 0
        # first determine the max_len of the data_list
        for data, _1, flatten, transpose, _2 in data_list:
            max_len = max(max_len, determienMaxLenOfData(data, flatten, transpose))

        def getRealKeyAndCheck(code, key):
            valid_key = f"{code}-{key}" if code else key
            if valid_key not in self:
                self[valid_key] = []
            return valid_key

        # now that we have the max len, we can use that for setting index
        # remember, if max len is 10, but one list only has 5 data points, its indexes will be: 9, 8, 7, 6, 5
        for data, code, flatten, transpose, output_list in data_list:
            if isDictOrList(data):
                try:
                    data.items()
                except AttributeError as _:
                    # top level structure must be a list
                    true_output_list = [
                        getRealKeyAndCheck(code, o) for o in output_list
                    ]
                    all_sub_lists = all(
                        isinstance(v, list) or isinstance(v, tuple) for v in data
                    )
                    if all_sub_lists and transpose and flatten:
                        n = len(data)
                        for row in range(n):
                            for col in range(
                                min(len(data[row]), len(true_output_list))
                            ):
                                valid_key = true_output_list[col]
                                self[valid_key].append(
                                    SparseData(
                                        self.longest_list + max_len - n + row,
                                        data[row][col],
                                    )
                                )
                    elif all_sub_lists and not transpose and flatten:
                        for row in range(min(len(data), len(true_output_list))):
                            valid_key = true_output_list[row]
                            n = len(data[row])
                            for col in range(n):
                                self[valid_key].append(
                                    SparseData(
                                        self.longest_list + max_len - n + col,
                                        data[row][col],
                                    )
                                )
                    elif flatten:
                        valid_key = true_output_list[0]
                        n = len(data)
                        for x in range(n):
                            self[valid_key].append(
                                SparseData(self.longest_list + max_len - n + x, data[x])
                            )
                    else:
                        valid_key = true_output_list[0]
                        self[valid_key].append(
                            SparseData(self.longest_list + max_len - 1, data)
                        )
                else:
                    # must be a dict
                    for key, value in data.items():
                        valid_key = getRealKeyAndCheck(code, key)
                        if isinstance(value, list) and flatten:
                            n = len(value)
                            for x in range(n):
                                self[valid_key].append(
                                    SparseData(
                                        self.longest_list + max_len - n + x,
                                        value[x],
                                    )
                                )
                        else:
                            self[valid_key].append(
                                SparseData(self.longest_list + max_len - 1, value)
                            )
            else:
                # not a dict or list, base case
                valid_key = getRealKeyAndCheck(code, output_list[0])
                self[valid_key].append(
                    SparseData(self.longest_list + max_len - 1, data)
                )
        self.longest_list += max_len
        return max_len

    def appendData(self, key: str, index: int, value: typing.Any):
        if key not in self:
            self[key] = []
        self[key].append(SparseData(index, value))

    def writeToCsv(self, file_path):
        with open(file_path, "w") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(self.keys())
            current_indexes = defaultdict(int)
            max_index = 0
            for v in self.values():
                max_index = max(v[-1].index, max_index)
            for x in range(max_index + 1):
                row = []
                for k in self.keys():
                    if (
                        current_indexes[k] < len(self[k])
                        and self[k][current_indexes[k]].index == x
                    ):
                        row.append(self[k][current_indexes[k]].value)
                        current_indexes[k] += 1
                    else:
                        row.append("")
                writer.writerow(row)
